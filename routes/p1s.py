import flask
import json
from pathlib import Path
from flask import current_app
import requests
from pathlib import Path


from scripts.bambu_helper import get_p1s_status
from scripts.bambu_camera_mjpeg import BambuMJPEGCamera

print("LOADED routes/p1s.py")

p1s_bp = flask.Blueprint("p1s", __name__)
BASE_DIR = Path(__file__).resolve().parent.parent
# ==================================================
# Pages
# ==================================================

@p1s_bp.route("/p1s")
def p1s():
    return flask.render_template("p1s/p1s.html")

@p1s_bp.route("/p1s/currentprint")
def p1s_current_print():
    return flask.render_template("p1s/p1s_currentprint.html")


# ==================================================
# API
# ==================================================

@p1s_bp.route("/api/p1s/status")
def api_p1s_status():
    resp = flask.jsonify(get_p1s_status())
    resp.headers["Cache-Control"] = "no-store"
    return resp


@p1s_bp.route("/api/p1s/full")
def api_p1s_full():
    """
    Full raw printer state as JSON
    Used by Current Print page for:
    - profile name
    - layer numbers
    """
    path = BASE_DIR / "data" / "p1s_full_state.json"

    if not path.exists():
        return flask.jsonify({
            "error": "p1s_full_state.json not found"
        }), 404

    try:
        data = json.loads(path.read_text())
        resp = flask.jsonify(data)
        resp.headers["Cache-Control"] = "no-store"
        return resp
    except Exception as e:
        return flask.jsonify({
            "error": "failed to read json",
            "detail": str(e)
        }), 500

@p1s_bp.route("/api/p1s/launch_bambu", methods=["POST"])
def launch_bambu_studio():
    pc_ip = flask.current_app.config["PC_IP"]
    pc_port = flask.current_app.config["PC_PORT"]
    token = flask.current_app.config["SECRET_TOKEN"]

    try:
        import requests

        url = f"http://{pc_ip}:{pc_port}/launch_bambu"
        res = requests.get(url, params={"token": token}, timeout=3)

        if res.status_code != 200:
            return {"success": False}, 500

        return {"success": True}

    except Exception as e:
        print("Launch Bambu failed:", e, flush=True)
        return {"success": False}, 500

@p1s_bp.route("/api/p1s/pc_health")
def pc_health():
    pc_ip = flask.current_app.config["PC_IP"]
    pc_port = flask.current_app.config["PC_PORT"]

    try:
        import requests
        res = requests.get(f"http://{pc_ip}:{pc_port}/health", timeout=1.5)
        return {"online": res.status_code == 200}
    except Exception:
        return {"online": False}

# ==================================================
# Camera
# ==================================================

@p1s_bp.route("/p1s/camera")
def p1s_camera():
    bambu_camera: BambuMJPEGCamera = current_app.config["BAMBU_CAMERA"]

    return flask.Response(
        bambu_camera.mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@p1s_bp.route("/p1s/camera/view")
def p1s_camera_view():
    return flask.render_template("p1s/p1s_camera.html")


# ==================================================
# AMS
# ==================================================

@p1s_bp.route("/p1s/ams")
def p1s_ams():
    from scripts import bambu_api

    trays = []
    ams_humidity = None
    ams_temp = None
    active_tray = None

    # ---------- LIVE STATE (authoritative) ----------
    raw = bambu_api.get_raw_state()
    full = bambu_api._master.get("print", {})  # internal but correct

    # ---------- AMS trays ----------
    ams_block = full.get("ams", {})
    ams_list = ams_block.get("ams", [])

    if ams_list:
        trays = ams_list[0].get("tray", [])
        ams_humidity = ams_list[0].get("humidity")
        ams_temp = ams_list[0].get("temp")

    # ---------- ACTIVE TRAY (THE FIX) ----------
    tray_now = ams_block.get("tray_now")

    try:
        active_tray = int(tray_now)
        if active_tray not in range(4):
            active_tray = None
    except (TypeError, ValueError):
        active_tray = None

    return flask.render_template(
        "p1s/p1s_ams.html",
        trays=trays,
        ams_humidity=ams_humidity,
        ams_temp=ams_temp,
        active_tray=active_tray,
    )


