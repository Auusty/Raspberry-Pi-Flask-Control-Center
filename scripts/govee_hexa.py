# scripts/govee_hexa.py
from scripts.govee_lan import power, brightness, color, color_temp


def ensure_defaults(cfg):
    cfg.setdefault("CURRENT_POWER", False)
    cfg.setdefault("CURRENT_BRIGHTNESS", 100)
    cfg.setdefault("CURRENT_COLOR", {"r": 255, "g": 255, "b": 255})
    cfg.setdefault("CURRENT_MODE", "color")
    cfg.setdefault("CURRENT_SCENE", None)
    cfg.setdefault("CURRENT_KELVIN", 6500)


def exit_scene_mode(cfg):
    cfg["CURRENT_MODE"] = "color"
    cfg["CURRENT_SCENE"] = None


def set_power(cfg, on: bool):
    ensure_defaults(cfg)
    power(on)
    cfg["CURRENT_POWER"] = on


def set_brightness(cfg, value: int):
    ensure_defaults(cfg)
    brightness(value)
    cfg["CURRENT_POWER"] = True
    cfg["CURRENT_BRIGHTNESS"] = value


def set_color(cfg, r: int, g: int, b: int):
    ensure_defaults(cfg)
    color(r, g, b)
    cfg["CURRENT_POWER"] = True
    cfg["CURRENT_COLOR"] = {"r": r, "g": g, "b": b}
    cfg["CURRENT_SCENE"] = None
    cfg["CURRENT_MODE"] = "color"

def set_kelvin(cfg, kelvin: int):
    ensure_defaults(cfg)

    kelvin = max(2000, min(9000, int(kelvin)))

    color_temp(kelvin)

    cfg["CURRENT_POWER"] = True
    cfg["CURRENT_MODE"] = "kelvin"
    cfg["CURRENT_SCENE"] = None
    cfg["CURRENT_KELVIN"] = kelvin
