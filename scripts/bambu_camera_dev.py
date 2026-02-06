import subprocess
import os
from bambulab import BambuAuthenticator, BambuClient
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "envs" / "Bambu_Keys.env")

DISPLAY = ":0"
WINDOW_MATCH = "Bambu"

env = os.environ.copy()
env["DISPLAY"] = DISPLAY


def camera_running():
    try:
        out = subprocess.check_output(
            ["pgrep", "-f", "bambu-camera"],
            stderr=subprocess.DEVNULL
        )
        return bool(out.strip())
    except subprocess.CalledProcessError:
        return False


#TOGGLE BEHAVIOR (PROCESS-BASED, NOT WINDOW-BASED)
if camera_running():
    subprocess.Popen(
        ["pkill", "-f", "bambu-camera"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Camera closed")
    raise SystemExit(0)


# ---- Launch camera ----

auth = BambuAuthenticator()
token = auth.get_or_create_token()

client = BambuClient(token=token)
device = client.get_devices()[0]

PRINTER_IP = os.getenv("BAMBU_P1S_LAN_ID")
if not PRINTER_IP:
    raise RuntimeError("BAMBU_P1S_LAN_ID not set")

ACCESS_CODE = device.get("dev_access_code")
MODEL = device.get("dev_product_name", "P1S")

subprocess.Popen(
    [
        "bambu-camera",
        "--ip", PRINTER_IP,
        "--code", ACCESS_CODE,
        "--model", MODEL
    ],
    env=env,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print("Camera opened (default size)")
