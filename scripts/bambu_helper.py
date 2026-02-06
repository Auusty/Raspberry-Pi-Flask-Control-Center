import time
from scripts.bambu_api import get_raw_state


STATE_MAP = {
    "RUNNING": "Printing",
    "PAUSE": "Paused",
    "PAUSED": "Paused",
    "IDLE": "Idle",
    "FINISH": "Complete",
    "FAILED": "Error",
    "PREPARE": "Preparing",
}

STALE_TIMEOUT = 300  # seconds (5 minutes)


def _format_eta(minutes, state):
    """
    Format ETA safely.
    - "--" when unknown
    - "Done" ONLY when state is FINISH
    """
    if minutes is None:
        return "Done" if state == "FINISH" else "--"

    try:
        minutes = int(minutes)
    except (ValueError, TypeError):
        return "--"

    if minutes <= 0:
        return "Done" if state == "FINISH" else "--"

    if minutes < 60:
        return f"{minutes}m"

    h = minutes // 60
    m = minutes % 60
    return f"{h}h {m}m" if m else f"{h}h"


def get_p1s_status():
    raw = get_raw_state()

    # ---------- Offline / not ready ----------
    if not isinstance(raw, dict) or not raw.get("connected"):
        return {
            "state": "Offline",
            "progress": 0,
            "eta": "--",

            # keep shape stable
            "profile": "--",
            "layer_num": None,
            "total_layers": None,

            "nozzle": "--",
            "nozzle_target": "--",
            "bed": "--",
            "bed_target": "--",
        }

    state_raw = raw.get("state", "UNKNOWN")
    progress = raw.get("progress", 0)

    # ---------- ETA handling ----------
    eta_minutes = raw.get("eta_minutes")

    # ---------- Stale FINISH detection ----------
    last_update = raw.get("last_update", 0)
    now = time.time()

    # ---------- Stale FINISH detection ----------
    last_update = raw.get("last_update", 0)
    now = time.time()

    stale = last_update and (now - last_update) > STALE_TIMEOUT

        #Case 1: normal near-100% finish
    if state_raw == "RUNNING" and progress >= 99 and stale:
            state_raw = "FINISH"
            progress = 100
            eta_minutes = 0

        #Case 2: Bambu silent-finish (VERY common)
    elif (
            state_raw == "RUNNING"
            and stale
            and raw.get("bed_target") == 0
            and (raw.get("nozzle_target") in (0, None) or raw.get("nozzle_target", 0) < 50)
        ):
            state_raw = "FINISH"
            progress = 100
            eta_minutes = 0


    return {
        "state": STATE_MAP.get(state_raw, state_raw),
        "progress": int(progress) if isinstance(progress, (int, float)) else 0,
        "eta": _format_eta(eta_minutes, state_raw),

        #used by Current Print page
        "profile": raw.get("profile", "--"),
        "layer_num": raw.get("layer_num"),
        "total_layers": raw.get("total_layers"),

        "nozzle": raw.get("nozzle", "--"),
        "nozzle_target": raw.get("nozzle_target", "--"),
        "bed": raw.get("bed", "--"),
        "bed_target": raw.get("bed_target", "--"),
    }
