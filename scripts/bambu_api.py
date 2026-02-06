import threading
import time
import json
from pathlib import Path
from collections import deque
from dotenv import load_dotenv

from bambulab import BambuAuthenticator, BambuClient, MQTTClient

# ============================================================
# Paths / Environment
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "p1s_full_state.json"
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / "envs" / "Bambu_Keys.env")

# ============================================================
# Authenticate
# ============================================================

auth = BambuAuthenticator()
token = auth.get_or_create_token()

client = BambuClient(token=token)
profile = client.get_user_profile()

UID = str(profile["uid"])
SERIAL = client.get_devices()[0]["dev_id"]

# ============================================================
# Shared State
# ============================================================

_lock = threading.Lock()

_state = {
    "state": "UNKNOWN",
    "progress": 0,
    "eta_minutes": None,
    "nozzle": None,
    "nozzle_target": None,
    "bed": None,
    "bed_target": None,
    "connected": False,
    "last_update_ts": None,  #exposed for helper modules
}

_master = {"print": {}}
_last_update_ts = None
_last_messages = deque(maxlen=25)

# ============================================================
# Recursive merge
# ============================================================

def _merge(master, delta):
    for k, v in delta.items():
        if isinstance(v, dict) and isinstance(master.get(k), dict):
            _merge(master[k], v)
        else:
            master[k] = v

def _to_int(val, fallback):
    try:
        return int(val)
    except (TypeError, ValueError):
        return fallback

def _round(val, fallback):
    try:
        return round(float(val), 1)
    except (TypeError, ValueError):
        return fallback

# ============================================================
# Load snapshot (seed state)
# ============================================================

if DATA_PATH.exists():
    try:
        with open(DATA_PATH) as f:
            saved = json.load(f)

        if isinstance(saved.get("print"), dict):
            with _lock:
                _merge(_master["print"], saved["print"])
                _last_update_ts = saved.get("last_update_ts")

                p = _master["print"]
                _state.update({
                    "state": p.get("gcode_state", "UNKNOWN"),
                    "progress": _to_int(p.get("mc_percent"), 0),
                    "eta_minutes": _to_int(p.get("mc_remaining_time"), None),
                    "nozzle": _round(p.get("nozzle_temper"), None),
                    "nozzle_target": _round(p.get("nozzle_target_temper"), None),
                    "bed": _round(p.get("bed_temper"), None),
                    "bed_target": _round(p.get("bed_target_temper"), None),
                    "connected": True,
                    "last_update_ts": _last_update_ts,
                })
    except Exception as e:
        print("Snapshot load failed:", e)

# ============================================================
# MQTT callback
# ============================================================

def _on_message(device_id, data):
    global _last_update_ts

    if not isinstance(data, dict):
        return

    delta = data.get("print")
    if not isinstance(delta, dict):
        return

    with _lock:
        _merge(_master["print"], delta)
        _last_update_ts = time.time()

        p = _master["print"]
        state = p.get("gcode_state", _state["state"])

        # ---- Live updates ----
        _state["state"] = state
        _state["progress"] = _to_int(p.get("mc_percent"), _state["progress"])
        _state["eta_minutes"] = _to_int(
            p.get("mc_remaining_time"), _state["eta_minutes"]
        )

        _state["nozzle"] = _round(p.get("nozzle_temper"), _state["nozzle"])
        _state["nozzle_target"] = _round(
            p.get("nozzle_target_temper"), _state["nozzle_target"]
        )

        _state["bed"] = _round(p.get("bed_temper"), _state["bed"])
        _state["bed_target"] = _round(
            p.get("bed_target_temper"), _state["bed_target"]
        )

        _state["connected"] = True
        _state["last_update_ts"] = _last_update_ts

        # ---- FINISH / IDLE normalization ----
        if state in ("FINISH", "IDLE"):
            _state["state"] = "FINISH"
            _state["progress"] = 100
            _state["eta_minutes"] = None
            _state["nozzle_target"] = 0
            _state["bed_target"] = 0
            return

        # ---- ETA sanity (Bambu reports 0 early) ----
        if state == "RUNNING" and _state["eta_minutes"] == 0:
            _state["eta_minutes"] = None

# ============================================================
# Persistence
# ============================================================

def _persist_loop():
    while True:
        time.sleep(30)
        try:
            with _lock:
                snapshot = {
                    "print": _master["print"],
                    "last_update_ts": _last_update_ts,
                }

            with open(DATA_PATH, "w") as f:
                json.dump(snapshot, f, indent=2)

        except Exception as e:
            print("Persist error:", e)

threading.Thread(target=_persist_loop, daemon=True).start()

# ============================================================
# Keep-alive (periodic pushall)
# ============================================================

def _keepalive_loop():
    while True:
        time.sleep(180)  # every 3 minutes
        try:
            mqtt = MQTTClient(UID, token, SERIAL)
            mqtt.publish(
                f"device/{SERIAL}/request",
                {"pushing": {"command": "pushall"}}
            )
        except Exception:
            pass

threading.Thread(target=_keepalive_loop, daemon=True).start()

# ============================================================
# MQTT start
# ============================================================

_started = False

def start_bambu():
    global _started
    if _started:
        return
    _started = True

    def _run():
        mqtt = MQTTClient(UID, token, SERIAL, on_message=_on_message)
        mqtt.connect(blocking=True)

        mqtt.publish(
            f"device/{SERIAL}/request",
            {"pushing": {"command": "pushall"}}
        )

    threading.Thread(target=_run, daemon=True).start()

# Auto-start on import
start_bambu()

# ============================================================
# Public API
# ============================================================

def get_raw_state():
    """
    Returns raw printer state for bambu_helper.py
    Compatible keys:
      - eta_minutes
      - eta_seconds
      - last_update
    """
    with _lock:
        if not _state["connected"]:
            return {"connected": False}

        now = time.time()
        last = _last_update_ts or 0
        age = now - last

        state = _state.get("state")
        progress = _state.get("progress", 0)

        out = dict(_state)

        # ------------------------------------------------
        # Silent FINISH detection
        # ------------------------------------------------
        stale = age > 300  # 5 minutes

        if state == "RUNNING" and stale:
            # Case 1: normal near-100% finish
            if progress >= 99:
                out.update({
                    "state": "FINISH",
                    "progress": 100,
                    "eta_minutes": None,
                })

            # Case 2: Bambu silent finish (bed cooled)
            elif (
                out.get("bed_target") == 0
                and (out.get("nozzle_target") in (0, None) or out.get("nozzle_target", 0) < 50)
            ):
                out.update({
                    "state": "FINISH",
                    "progress": 100,
                    "eta_minutes": None,
                })

            else:
                return {"connected": False}

        # ------------------------------------------------
        # Helper compatibility keys
        # ------------------------------------------------
        out["last_update"] = last

        if out.get("eta_minutes") is None:
            out["eta_seconds"] = None
        else:
            out["eta_seconds"] = int(out["eta_minutes"]) * 60

        return out
        
       
def get_active_ams_tray():
    """
    Returns active AMS tray index (0–3) or None
    """
    with _lock:
        ams = _master.get("print", {}).get("ams", {})
        tray_now = ams.get("tray_now")

    try:
        tray = int(tray_now)
    except (TypeError, ValueError):
        return None

    return tray if 0 <= tray <= 3 else None


