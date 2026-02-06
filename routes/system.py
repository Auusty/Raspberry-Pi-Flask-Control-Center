import flask
import psutil
import time
import subprocess
from flask import current_app

system_bp = flask.Blueprint("system", __name__)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------
# System login (PIN keypad)
# ------------------
@system_bp.route("/system-login", methods=["GET", "POST"])
def system_login():
    if flask.request.method == "POST":
        pin = flask.request.form.get("pin")
        if pin == current_app.config.get("SYSTEM_PIN", "0000"):
            return flask.redirect(flask.url_for("system.system"))
        return flask.render_template("system/login.html", error="Wrong PIN")

    return flask.render_template("system/login.html")


# ------------------
# System pages
# ------------------
@system_bp.route("/system")
def system():
    last_boot = time.strftime(
        "%A, %b %d at %I:%M %p",
        time.localtime(psutil.boot_time())
    )
    return flask.render_template("system/system.html", last_boot=last_boot)


@system_bp.route("/system-stats")
def system_stats():
    return flask.render_template("system/system_stats.html")


# ------------------
# System APIs
# ------------------
@system_bp.route("/api/system-stats")
def api_system_stats():
    return flask.jsonify({
        "cpu": psutil.cpu_percent(interval=0.5),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    })


# ------------------
# System actions
# ------------------
@system_bp.route("/exit-kiosk", methods=["POST"])
def exit_kiosk():
    subprocess.Popen([str(BASE_DIR / "scripts" / "exit_kiosk.sh")])
    return flask.redirect(flask.url_for("index"))


@system_bp.route("/restart-chromium", methods=["POST"])
def restart_chromium():
    start_script = BASE_DIR / "scripts" / "start_chromium.sh"

    subprocess.run(["pkill", "-f", str(start_script)])
    subprocess.run(["sleep", "2"])
    subprocess.Popen([str(start_script)])

    return flask.redirect(flask.url_for("index"))



@system_bp.route("/reboot-pi", methods=["POST"])
def reboot_pi():
    subprocess.Popen(["sudo", "/sbin/reboot"])
    return flask.redirect(flask.url_for("index"))
