import os
import time
import requests
from dotenv import load_dotenv

load_dotenv("envs/Govee_Keys.env")

API_KEY = os.getenv("GOVEE_API_KEY")
DEVICE = os.getenv("GOVEE_DEVICE_OPENAPI_ID")  # we’ll update this
SKU = os.getenv("GOVEE_DEVICE_SKU")

# IMPORTANT: override with the real cloud device ID
if not DEVICE:
    raise RuntimeError("GOVEE Open API Key Not Set.")

URL = "https://openapi.api.govee.com/router/api/v1/device/state"

_CACHE = {"ts": 0, "data": {}}
CACHE_TTL = 10  # seconds


def _parse_capabilities(capabilities):
    status = {}

    for cap in capabilities:
        inst = cap.get("instance")
        val = cap.get("state", {}).get("value")

        if inst == "online":
            status["online"] = bool(val)

        elif inst == "powerSwitch":
            status["power"] = bool(val)

        elif inst == "brightness":
            status["brightness"] = val

        elif inst == "colorRgb" and isinstance(val, int):
            status["color"] = {
                "r": (val >> 16) & 0xFF,
                "g": (val >> 8) & 0xFF,
                "b": val & 0xFF,
            }

        elif inst == "colorTemperatureK":
            status["kelvin"] = val

    return status


def get_cloud_status(force=False):
    now = time.time()
    if not force and (now - _CACHE["ts"] < CACHE_TTL):
        return _CACHE["data"]

    body = {
        "requestId": "status",
        "payload": {
            "device": DEVICE,
            "sku": SKU,
        },
    }

    headers = {
        "Govee-API-Key": API_KEY,
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(URL, json=body, headers=headers, timeout=5)
        res.raise_for_status()
        payload = res.json().get("payload", {})
        caps = payload.get("capabilities", [])
        parsed = _parse_capabilities(caps)
    except Exception:
        return _CACHE["data"]

    _CACHE["ts"] = now
    _CACHE["data"] = parsed
    return parsed
