# scripts/govee_lan.py
import socket
import json
import os
from dotenv import load_dotenv
import time

load_dotenv("envs/Govee_Keys.env")

DEVICE_IP = os.getenv("GOVEE_DEVICE_LAN_ID")
if not DEVICE_IP:
    raise RuntimeError("GOVEE_DEVICE_LAN_ID not set")

print("GOVEE LAN TARGET:", DEVICE_IP)

PORT = 4003
TIMEOUT = 1.0


def _send(payload: dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(payload).encode("utf-8"), (DEVICE_IP, PORT))
    sock.close()


def power(on: bool):
    _send({
        "msg": {
            "cmd": "turn",
            "data": {"value": 1 if on else 0}
        }
    })


def brightness(value: int):
    _send({
        "msg": {
            "cmd": "brightness",
            "data": {"value": int(value)}
        }
    })


def color(r: int, g: int, b: int):
    _send({
        "msg": {
            "cmd": "colorwc",
            "data": {
                "color": {"r": r, "g": g, "b": b},
                "colorTemInKelvin": 0
            }
        }
    })

def color_temp(kelvin: int):
    _send({
        "msg": {
            "cmd": "colorwc",
            "data": {
                "color": {"r": 0, "g": 0, "b": 0},
                "colorTemInKelvin": int(kelvin)
            }
        }
    })

def query_status():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    # Bind so the device can reply
    sock.bind(("0.0.0.0", 0))

    # Send devStatus query
    sock.sendto(
        json.dumps({
            "msg": {"cmd": "devStatus"}
        }).encode("utf-8"),
        (DEVICE_IP, PORT)
    )

    try:
        data, _ = sock.recvfrom(4096)
        payload = json.loads(data.decode("utf-8"))
    except socket.timeout:
        return None
    finally:
        sock.close()

    # Validate structure
    msg = payload.get("msg", {})
    if msg.get("cmd") != "devStatus":
        return None

    return msg.get("data", {})

def normalize_status(data: dict):
    if not data:
        return {}

    return {
        "power": bool(data.get("onOff")),
        "brightness": data.get("brightness"),
        "color": data.get("color"),
        "kelvin": data.get("colorTemInKelvin"),
    }
