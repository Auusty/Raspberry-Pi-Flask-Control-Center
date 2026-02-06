import flask
import json
import asyncio
import os
from pathlib import Path
import sys
import subprocess
import pexpect
import threading
import importlib
import time

from govee import Device, GoveeClient
from scripts.govee import govee_diy_scenes
from scripts.govee import govee_diy_scene_aliases
from scripts.govee.govee_devices import H6061_7122D005C1061F48
from scripts.govee import govee_scenes

# Source for manual LAN controls
from scripts.govee_hexa import (
    set_power as hexa_set_power,
    set_brightness as hexa_set_brightness,
    set_color as hexa_set_color,
)

hexa_bp = flask.Blueprint("hexa", __name__)
GOVEE_BRIGHTNESS_LOCK = threading.Lock()
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# Global Variables
# ==================================================
GOVEE_REFRESH_LOCK = threading.Lock()

# ==================================================
# Paths
# ==================================================
STATE_DATA_PATH = BASE_DIR / "data" / "hexa_state.json"
SCENE_DATA_PATH = BASE_DIR / "data" / "hexa_scenes.json"

# ==================================================
# Environment
# ==================================================
GOVEE_API_KEY = os.getenv("GOVEE_API_KEY")
if not GOVEE_API_KEY:
    raise RuntimeError("GOVEE_API_KEY not found")

# ==================================================
# helper function (govee-sync refresh)
# ==================================================
def run_govee_refresh(log_path: Path, scripts_dir: Path, fixer_path: Path):
    try:
        with log_path.open("w") as log:
            def log_write(msg):
                log.write(msg + "\n")
                log.flush()

            log_write("=== DIY scene refresh started ===")

            # 1️⃣ Run your refresh script
            result = subprocess.run(
                [sys.executable, "refresh_diy_scenes.py"],
                cwd=str(scripts_dir),
                capture_output=True,
                text=True,
            )

            log_write("=== refresh_diy_scenes.py stdout ===")
            log_write(result.stdout)
            log_write("=== refresh_diy_scenes.py stderr ===")
            log_write(result.stderr)

            # 2️⃣ Run fixer
            if fixer_path.exists():
                fix = subprocess.run(
                    [sys.executable, str(fixer_path)],
                    cwd=str(fixer_path.parent),
                    capture_output=True,
                    text=True,
                )
                log_write("=== fixer stdout ===")
                log_write(fix.stdout)
                log_write("=== fixer stderr ===")
                log_write(fix.stderr)

            log_write("=== refresh completed ===")

    finally:
        if GOVEE_REFRESH_LOCK.locked():
            GOVEE_REFRESH_LOCK.release()

# ==================================================
# Helpers (state persistence)
# ==================================================
def _atomic_write(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2))
    tmp.replace(path)

def _ensure_defaults(cfg):
    cfg.setdefault("CURRENT_POWER", False)
    cfg.setdefault("CURRENT_BRIGHTNESS", 100)
    cfg.setdefault("CURRENT_COLOR", {"r": 255, "g": 255, "b": 255})
    cfg.setdefault("CURRENT_MODE", "color")
    cfg.setdefault("CURRENT_SCENE", None)

def load_state():
    if STATE_DATA_PATH.exists():
        try:
            data = json.loads(STATE_DATA_PATH.read_text())
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def save_state(cfg):
    _ensure_defaults(cfg)
    _atomic_write(
        STATE_DATA_PATH,
        {
            "power": bool(cfg["CURRENT_POWER"]),
            "brightness": int(cfg["CURRENT_BRIGHTNESS"]),
            "color": cfg["CURRENT_COLOR"],
            "kelvin": int(cfg.get("CURRENT_KELVIN", 6500)),
            "mode": cfg["CURRENT_MODE"],
            "active_scene": cfg["CURRENT_SCENE"],
        },
    )

def restore_state(cfg):
    _ensure_defaults(cfg)
    data = load_state()
    if not data:
        return

    cfg["CURRENT_POWER"] = bool(data.get("power", cfg["CURRENT_POWER"]))
    cfg["CURRENT_BRIGHTNESS"] = int(data.get("brightness", cfg["CURRENT_BRIGHTNESS"]))
    cfg["CURRENT_COLOR"] = data.get("color", cfg["CURRENT_COLOR"]) or cfg["CURRENT_COLOR"]
    cfg["CURRENT_MODE"] = data.get("mode", cfg["CURRENT_MODE"]) or "color"
    cfg["CURRENT_SCENE"] = data.get("active_scene", None)
    cfg["CURRENT_KELVIN"] = int(data.get("kelvin", cfg.get("CURRENT_KELVIN", 6500)))


# ==================================================
# Scenes: slot loader
# ==================================================
def load_scene_slots():
    if SCENE_DATA_PATH.exists():
        try:
            data = json.loads(SCENE_DATA_PATH.read_text())
            return data if isinstance(data, dict) else {}
        except Exception:
            pass

    return {
        "slot_1": {"key": None, "name": "Slot 1"},
        "slot_2": {"key": None, "name": "Slot 2"},
        "slot_3": {"key": None, "name": "Slot 3"},
    }

# ==================================================
# Scenes: alias lookup (default load)
# ==================================================
def build_alias_lookup(module_aliases):
    lookup = {}
    # Support both older and newer generated formats
    for name in dir(module_aliases):
        if not name.startswith("H6061_"):
            continue
        alias = getattr(module_aliases, name)
        # Common possibilities: (scene_id,name) OR (id,name)
        if hasattr(alias, "scene_id") and hasattr(alias, "name"):
            lookup[getattr(alias, "scene_id")] = alias
        elif hasattr(alias, "id") and hasattr(alias, "name"):
            lookup[getattr(alias, "id")] = alias
    return lookup

# ==================================================
# Pages
# ==================================================
@hexa_bp.route("/Hexa_Glide")
def hexa_glide():
    cfg = flask.current_app.config
    device: Device = cfg.get("HEXAGON_LIGHTS")

    restore_state(cfg)
    save_state(cfg)

    return flask.render_template(
        "hexa_glide/hexa_glide.html",
        device_name=device.name if device else "Hexa Glide",
        power_state="on" if cfg["CURRENT_POWER"] else "off",
        brightness=cfg["CURRENT_BRIGHTNESS"],
        current_color=cfg["CURRENT_COLOR"],
        mode=cfg["CURRENT_MODE"],
        active_scene=cfg["CURRENT_SCENE"],
    )

@hexa_bp.route("/Hexa_Glide/Scenes")
def hexa_glide_scenes():
    cfg = flask.current_app.config
    restore_state(cfg)

    # -------------------------------------------------
    # Reload scene modules (no Flask restart)
    # -------------------------------------------------
    import scripts.govee.govee_diy_scenes as diy_mod
    import scripts.govee.govee_diy_scene_aliases as aliases_mod
    import scripts.govee.govee_scenes as govee_mod

    importlib.reload(diy_mod)
    importlib.reload(aliases_mod)
    importlib.reload(govee_mod)

    alias_lookup = build_alias_lookup(aliases_mod)
    scene_slots = load_scene_slots()

    # -------------------------------------------------
    # USER (DIY) SCENES — ALL of them
    # -------------------------------------------------
    user_scenes: list[dict] = []

    for name in getattr(diy_mod, "__all__", []):
        scene = getattr(diy_mod, name, None)
        if not scene:
            continue

        alias = alias_lookup.get(getattr(scene, "id", None))

        user_scenes.append({
            "key": name,
            "name": alias.name if alias else scene.name,
        })

    # -------------------------------------------------
    # BUILT-IN GOVEE SCENES
    # -------------------------------------------------
    govee_scenes: list[dict] = []

    for name in getattr(govee_mod, "__all__", []):
        scene = getattr(govee_mod, name, None)
        if not scene:
            continue

        govee_scenes.append({
            "key": name,
            "name": scene.name,
        })

    # -------------------------------------------------
    # Combined list (for random button)
    # -------------------------------------------------
    all_scenes = user_scenes

    # -------------------------------------------------
    # Render
    # -------------------------------------------------
    return flask.render_template(
        "hexa_glide/hexa_glide_scenes.html",
        power_state="on" if cfg["CURRENT_POWER"] else "off",
        scene_slots=scene_slots,
        govee_scenes=govee_scenes,
        user_scenes=user_scenes,
        all_scenes=all_scenes,
        active_scene=cfg.get("CURRENT_SCENE"),
    )


# ==================================================
# API — POWER (LAN via scripts/govee_hexa.py)
# ==================================================
@hexa_bp.route("/api/power", methods=["POST"])
def api_power():
    cfg = flask.current_app.config
    restore_state(cfg)

    new_state = not bool(cfg["CURRENT_POWER"])
    try:
        hexa_set_power(cfg, new_state)
    except Exception as e:
        print("LAN power failed:", e, flush=True)
        return {"success": False, "error": str(e)}, 500

    save_state(cfg)
    return {
        "success": True,
        "power": "on" if cfg["CURRENT_POWER"] else "off",
        "mode": cfg["CURRENT_MODE"],
        "active_scene": cfg["CURRENT_SCENE"],
    }

# ==================================================
# API — BRIGHTNESS (LAN via scripts/govee_hexa.py)
# ==================================================
@hexa_bp.route("/api/brightness", methods=["POST"])
def api_brightness():
    if not GOVEE_BRIGHTNESS_LOCK.acquire(blocking=False):
        return {"success": False, "error": "busy"}, 429

    try:
        cfg = flask.current_app.config
        payload = flask.request.get_json(silent=True) or {}

        raw = payload.get("brightness")
        if raw is None:
            return {"success": False, "error": "missing brightness"}, 400

        try:
            value = int(raw)
            value = max(1, min(100, value))
        except (TypeError, ValueError):
            return {"success": False, "error": "invalid brightness"}, 400

        #DO NOT restore_state here
        prev_mode = cfg["CURRENT_MODE"]
        prev_scene = cfg["CURRENT_SCENE"]

        hexa_set_brightness(cfg, value)

        # preserve mode
        cfg["CURRENT_MODE"] = prev_mode
        cfg["CURRENT_SCENE"] = prev_scene

        save_state(cfg)

        return {
            "success": True,
            "brightness": value,
            "mode": cfg["CURRENT_MODE"],
            "active_scene": cfg["CURRENT_SCENE"],
        }

    except Exception as e:
        print("brightness crash:", e, flush=True)
        return {"success": False}, 500

    finally:
        GOVEE_BRIGHTNESS_LOCK.release()

# ==================================================
# API — Color (LAN via scripts/govee_hexa.py)
# ==================================================

@hexa_bp.route("/api/color", methods=["POST"])
def api_color():
    cfg = flask.current_app.config
    payload = flask.request.get_json(silent=True) or {}

    try:
        c = payload.get("color") or {}
        r = max(0, min(255, int(c.get("r"))))
        g = max(0, min(255, int(c.get("g"))))
        b = max(0, min(255, int(c.get("b"))))
    except Exception:
        return {"success": False, "error": "invalid color"}, 400

    cfg["CURRENT_POWER"] = True
    cfg["CURRENT_MODE"] = "color"
    cfg["CURRENT_SCENE"] = None

    try:
        hexa_set_color(cfg, r, g, b)
    except Exception as e:
        print("LAN color failed:", e, flush=True)
        return {"success": False, "error": str(e)}, 500
    
    save_state(cfg)

    return {
        "success": True,
        "power": "on",
        "color": cfg["CURRENT_COLOR"],
        "mode": cfg["CURRENT_MODE"],
        "active_scene": None,
    }

# ==================================================
# API — Kelvin (LAN via scripts/govee_hexa.py)
# ==================================================
@hexa_bp.route("/api/kelvin", methods=["POST"])
def api_kelvin():
    cfg = flask.current_app.config
    payload = flask.request.get_json(silent=True) or {}

    try:
        kelvin = int(payload.get("kelvin"))
    except Exception:
        return {"success": False}, 400

    from scripts.govee_hexa import set_kelvin
    set_kelvin(cfg, kelvin)
    save_state(cfg)

    return {
        "success": True,
        "kelvin": kelvin,
        "mode": "kelvin",
    }

# ==================================================
# API — STATUS (LAN truth + persisted intent)
# ==================================================
@hexa_bp.route("/api/hexa/status")
def api_hexa_status():
    persisted = load_state()

    # LAN status (usually empty for Hexa devices)
    live = {}
    try:
        from scripts.govee_lan import query_status, normalize_status
        live = normalize_status(query_status()) or {}
    except Exception:
        live = {}

    # Cloud fallback (authoritative state)
    if not live:
        try:
            from scripts.govee_cloud_status import get_cloud_status
            live = get_cloud_status() or {}
        except Exception:
            live = {}

    return {
        "success": True,

        # Physical device state
        "power": (
            "on" if live.get("power") is True
            else "off" if live.get("power") is False
            else "on" if persisted.get("power")
            else "off"
        ),

        "brightness": live.get("brightness", persisted.get("brightness", 100)),
        "color": live.get("color", persisted.get("color")),
        "kelvin": live.get("kelvin"),

        # Logical intent (local state only)
        "mode": persisted.get("mode", "color"),
        "active_scene": persisted.get("active_scene"),
    }

# ==================================================
# API — SCENE REFRESH (background govee-sync)
# ==================================================
@hexa_bp.route("/api/hexa/scenes/refresh", methods=["POST"])
def refresh_scenes():
    # Prevent overlap
    if not GOVEE_REFRESH_LOCK.acquire(blocking=False):
        return {"success": False, "error": "refresh already running"}, 409

    log_path = BASE_DIR / "logs" / "govee_sync_refresh.log"
    scripts_dir = BASE_DIR / "scripts" / "govee"
    fixer_path = BASE_DIR / "scripts" / "govee_fix_aliases.py"

    t = threading.Thread(
        target=run_govee_refresh,
        args=(log_path, scripts_dir, fixer_path),
        daemon=True,
    )
    t.start()

    return {"success": True, "redirect": "/Hexa_Glide/Scenes"}

# ==================================================
# API — SCENE SLOT ASSIGN
# ==================================================
@hexa_bp.route("/api/hexa/scene/assign", methods=["POST"])
def api_assign_scene():
    payload = flask.request.json or {}
    slot = payload.get("slot")
    key = payload.get("key")
    name = payload.get("name")

    if slot not in {"slot_1", "slot_2", "slot_3"}:
        return {"success": False, "error": "invalid slot"}, 400
    if not key:
        return {"success": False, "error": "missing scene key"}, 400

    slots = load_scene_slots()
    slots[slot] = {"key": key, "name": name or key}
    _atomic_write(SCENE_DATA_PATH, slots)
    return {"success": True}

@hexa_bp.route("/api/hexa/scene/apply", methods=["POST"])
def api_apply_scene():
    payload = flask.request.json or {}
    scene_key = payload.get("scene_key")
    if not scene_key:
        return {"success": False, "error": "missing scene_key"}, 400

    #DIY ONLY
    scene = getattr(govee_diy_scenes, scene_key, None)
    if not scene:
        return {"success": False, "error": "DIY scene not found"}, 404

    async def run():
        client = GoveeClient(
            api_key=GOVEE_API_KEY,
            prefer_lan=True,
        )
        await client.apply_scene(
            H6061_7122D005C1061F48,
            scene,
        )

    try:
        asyncio.run(run())
    except Exception as e:
        print("DIY apply_scene failed:", e, flush=True)
        return {"success": False, "error": str(e)}, 500

    cfg = flask.current_app.config
    restore_state(cfg)

    cfg["CURRENT_POWER"] = True
    cfg["CURRENT_MODE"] = "scene"
    cfg["CURRENT_SCENE"] = {
        "key": scene_key,
        "name": scene.name,
    }

    save_state(cfg)

    return {
        "success": True,
        "active_scene": cfg["CURRENT_SCENE"],
    }

@hexa_bp.route("/api/hexa/scenes/user")
def api_user_scenes():
    import scripts.govee.govee_diy_scenes as diy_mod
    import scripts.govee.govee_diy_scene_aliases as aliases_mod
    importlib.reload(diy_mod)
    importlib.reload(aliases_mod)

    alias_lookup = build_alias_lookup(aliases_mod)

    diy_ids_path = BASE_DIR / "scripts" / "govee" / "diy_scene_ids.json"
    try:
        diy_ids = set(json.loads(diy_ids_path.read_text()))
    except Exception:
        diy_ids = set()

    user_scenes = []

    for name in dir(diy_mod):
        if not name.startswith("H6061_"):
            continue

        scene = getattr(diy_mod, name)
        scene_id = getattr(scene, "id", None)
        if scene_id not in diy_ids:
            continue

        alias = alias_lookup.get(scene_id)
        user_scenes.append({
            "key": name,
            "name": alias.name if alias else scene.name,
        })

    return {"success": True, "user_scenes": user_scenes}
