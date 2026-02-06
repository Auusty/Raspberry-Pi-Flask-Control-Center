# ==================================================
# Environment (MUST be first)
# ==================================================
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / "envs" / "Network_Ip.env")
load_dotenv(BASE_DIR / "envs" / "Govee_Keys.env")
load_dotenv(BASE_DIR / "envs" / "system.env")
load_dotenv(BASE_DIR / "envs" / "Bambu_Keys.env")
load_dotenv(BASE_DIR / "envs" / "Weather.env")
load_dotenv(BASE_DIR / "envs" / "Discord.env")
load_dotenv(BASE_DIR / "envs" / "Discord_Text.env")
load_dotenv(BASE_DIR / "envs" / "app.env")

# ==================================================
# FORCE SDK govee import
# ==================================================
import sys
import site

for p in site.getsitepackages():
    if p not in sys.path:
        sys.path.insert(0, p)

# ==================================================
# Imports
# ==================================================
import flask
import time
import threading
from scripts import discord_service

from govee.client import GoveeClient
from govee.models import Device
from govee import Colors


from scripts import bambu_api
from scripts.bambu_camera_mjpeg import BambuMJPEGCamera

# ==================================================
# Blueprints
# ==================================================

from routes.websites import websites_bp
from routes.system import system_bp
from routes.steam import steam_bp
from routes.p1s import p1s_bp
from routes.hexa_glide import hexa_bp
from routes.uploads import uploads_bp, upload_bp
from routes.weather import weather_bp
from routes.discord import discord_bp

# ==================================================
# Flask setup
# ==================================================
flask_client = flask.Flask(__name__)
flask_client.secret_key = os.getenv("FLASK_SECRET", "dev_fallback_key")

SYSTEM_PIN = os.getenv("SYSTEM_PIN", "0000")
flask_client.config["SYSTEM_PIN"] = SYSTEM_PIN

# ==================================================
# App Info
# ==================================================
APP_NAME = os.getenv("APP_NAME", "FlaskControlCenter")
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")

APP_DEBUG = os.getenv("APP_DEBUG", "false").lower() in ("1", "true", "yes")
APP_START_TIME = time.time()

# ==================================================
# Get uptime of Pi
# ==================================================

def get_uptime():
    seconds = int(time.time() - APP_START_TIME)

    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    human = []
    if days:
        human.append(f"{days}d")
    if hours:
        human.append(f"{hours}h")
    if minutes:
        human.append(f"{minutes}m")
    human.append(f"{seconds}s")

    return {
        "seconds": int(time.time() - APP_START_TIME),
        "human": " ".join(human),
    }

def get_start_time():
    return time.strftime(
        "%b %d, %Y %I:%M %p",
        time.localtime(APP_START_TIME)
    )

# ==================================================
# Runtime state (Lights)
# ==================================================
current_BRIGHTNESS = 100
current_POWER = False
current_COLOR = {"r": 255, "g": 255, "b": 255}

# ==================================================
# Bambu (Printer) setup
# ==================================================
BAMBU_DEVICE_NAME = os.getenv("BAMBU_DEVICE_NAME", "P1S")
BAMBU_P1S_LAN_ID = os.getenv("BAMBU_P1S_LAN_ID")
BAMBU_P1S_ACCESS_CODE = os.getenv("BAMBU_P1S_ACCESS_CODE")

if not BAMBU_P1S_LAN_ID or not BAMBU_P1S_ACCESS_CODE:
    print("Bambu credentials missing — printer features disabled", flush=True)
    bambu_camera = None
else:
    bambu_camera = BambuMJPEGCamera(
        BAMBU_P1S_LAN_ID,
        BAMBU_P1S_ACCESS_CODE
    )
    bambu_api.start_bambu()
    bambu_camera.start()

flask_client.config["BAMBU_CAMERA"] = bambu_camera

# ==================================================
# Network (PC bridge)
# ==================================================
flask_client.config["PC_IP"] = os.getenv("PC_IP")
flask_client.config["PC_PORT"] = os.getenv("PC_PORT")
flask_client.config["SECRET_TOKEN"] = os.getenv("SECRET_TOKEN")

# ==================================================
# Govee (Lights)
# ==================================================
govee_api_key = os.getenv("GOVEE_API_KEY")
govee_device_lan_id = os.getenv("GOVEE_DEVICE_LAN_ID")
govee_device_name = os.getenv("GOVEE_DEVICE_NAME")
govee_device_sku = os.getenv("GOVEE_DEVICE_SKU")

if not all([govee_api_key, govee_device_lan_id, govee_device_name, govee_device_sku]):
    print("Govee credentials missing — Hexa Glide disabled", flush=True)
    govee_client = None
    hexagon_lights = None
else:
    govee_client = GoveeClient(api_key=govee_api_key)
    hexagon_lights = Device(
        id=None,
        ip=govee_device_lan_id,
        name=govee_device_name,
        sku=govee_device_sku,
    )
# ==================================================
# Sync initial Govee power state (IMPORTANT)
# ==================================================

current_POWER = False  # default fallback

try:
    if govee_client is not None and hexagon_lights is not None:
        state = govee_client.get_device_state(hexagon_lights) or {}

        # Govee may return: {"power": "on"}, {"power": "off"}, {"on": True}, etc.
        power_raw = state.get("power", state.get("on"))

        if isinstance(power_raw, bool):
            current_POWER = power_raw
        elif isinstance(power_raw, str):
            current_POWER = power_raw.strip().lower() == "on"
        else:
            current_POWER = False

        print(
            f"Hexa Glide initial power sync → raw={power_raw!r}, parsed={current_POWER}",
            flush=True
        )
    else:
        print("Govee client or device missing — assuming power OFF", flush=True)

except Exception as e:
    print("Failed to sync Hexa Glide power state:", e, flush=True)
    current_POWER = False


# Store synced state in Flask config
flask_client.config["GOVEE_CLIENT"] = govee_client
flask_client.config["HEXAGON_LIGHTS"] = hexagon_lights
flask_client.config["CURRENT_BRIGHTNESS"] = current_BRIGHTNESS
flask_client.config["CURRENT_POWER"] = current_POWER
flask_client.config["CURRENT_COLOR"] = current_COLOR

# ==================================================
# Register Blueprints
# ==================================================
flask_client.register_blueprint(websites_bp)
flask_client.register_blueprint(system_bp)
flask_client.register_blueprint(steam_bp)
flask_client.register_blueprint(p1s_bp)
flask_client.register_blueprint(hexa_bp)
flask_client.register_blueprint(uploads_bp)
flask_client.register_blueprint(upload_bp)
flask_client.register_blueprint(weather_bp)
flask_client.register_blueprint(discord_bp)

# ==================================================
# Core Routes
# ==================================================
@flask_client.route("/")
def index():
    return flask.render_template("index.html")

@flask_client.route("/health")
def health():
    return "OK", 200

@flask_client.route("/version")
def version():
    uptime = get_uptime()
    starttime = get_start_time()

    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "python": sys.version.split()[0],
        "debug": flask_client.debug,
        "started_at": starttime,
        "uptime": uptime,
    }, 200


# ==================================================
# Programs
# ==================================================
@flask_client.route("/programs")
def programs():
    return flask.render_template("programs/programs.html")


@flask_client.route("/upload")
def upload_page():
    return flask.render_template("programs/upload/upload.html")



# ==================================================
# Discord 
# ==================================================

def start_discord_service():
    print("Discord thread entered", flush=True)
    try:
        discord_service.run_forever()
    except Exception as e:
        print("Discord service failed to start:", e, flush=True)



# ==================================================
# Run
# ==================================================

if __name__ == "__main__":

    threading.Thread(
        target=start_discord_service,
        daemon=True
    ).start()

    flask_client.run(
        host="0.0.0.0",
        port=5000,
        debug=APP_DEBUG,
        use_reloader=False
    )
