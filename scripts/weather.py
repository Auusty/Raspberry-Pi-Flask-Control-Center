import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

# =====================================================
# Config
# =====================================================
LOCAL_TZ = ZoneInfo("America/Los_Angeles")

load_dotenv("envs/Weather.env")

API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
LAT = os.getenv("WEATHER_LAT", "").strip()
LON = os.getenv("WEATHER_LON", "").strip()


# =====================================================
# Helpers
# =====================================================
def force_day_icon(icon: str) -> str:
    """
    OpenWeather sometimes returns night icons even at noon.
    For daily forecasts, force daytime icons.
    """
    if icon.endswith("n"):
        return icon[:-1] + "d"
    return icon


# =====================================================
# Simple current-only weather
# =====================================================
def get_weather():
    if not API_KEY or not LAT or not LON:
        raise RuntimeError("Weather env vars missing")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "imperial",
    }

    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    d = r.json()

    return {
        "temp": round(d["main"]["temp"]),
        "feels_like": round(d["main"]["feels_like"]),
        "humidity": d["main"]["humidity"],
        "wind": round(d["wind"]["speed"]),
        "condition": d["weather"][0]["main"],
        "description": d["weather"][0]["description"].title(),
        "icon": d["weather"][0]["icon"],  # current can be day or night
    }


# =====================================================
# Full weather (current + hourly + daily)
# =====================================================
def get_weather_full():
    if not API_KEY or not LAT or not LON:
        raise RuntimeError("Weather env vars missing")

    current_url = "https://api.openweathermap.org/data/2.5/weather"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": LAT,
        "lon": LON,
        "appid": API_KEY,
        "units": "imperial",
    }

    current = requests.get(current_url, params=params, timeout=5).json()
    forecast = requests.get(forecast_url, params=params, timeout=5).json()

    # -------------------------------------------------
    # Hourly (next 24h, 3-hour steps)
    # -------------------------------------------------
    hourly = [
        {
            "dt": h["dt"],
            "temp": round(h["main"]["temp"]),
            "icon": h["weather"][0]["icon"],  # hourly keeps night icons
        }
        for h in forecast["list"][:8]  # 8 × 3h = 24h
    ]

    # -------------------------------------------------
    # Daily (LOCAL date, noon-based icon, forced DAY)
    # -------------------------------------------------
    daily_map = {}

    for h in forecast["list"]:
        local_dt = datetime.fromtimestamp(h["dt"], tz=LOCAL_TZ)
        local_date = local_dt.date()
        hour = local_dt.hour

        temp = h["main"]["temp"]
        icon = h["weather"][0]["icon"]
        diff_from_noon = abs(hour - 12)

        if local_date not in daily_map:
            daily_map[local_date] = {
                "min": temp,
                "max": temp,
                "icon": force_day_icon(icon),
                "dt": h["dt"],
                "icon_hour_diff": diff_from_noon,
            }
        else:
            daily_map[local_date]["min"] = min(daily_map[local_date]["min"], temp)
            daily_map[local_date]["max"] = max(daily_map[local_date]["max"], temp)

            # choose icon closest to noon
            if diff_from_noon < daily_map[local_date]["icon_hour_diff"]:
                daily_map[local_date]["icon"] = force_day_icon(icon)
                daily_map[local_date]["dt"] = h["dt"]
                daily_map[local_date]["icon_hour_diff"] = diff_from_noon

    daily = [
        {
            "dt": v["dt"],
            "min": round(v["min"]),
            "max": round(v["max"]),
            "icon": v["icon"],
        }
        for v in list(daily_map.values())[:5]
    ]

    # -------------------------------------------------
    # Final payload
    # -------------------------------------------------
    return {
        "current": {
            "temp": round(current["main"]["temp"]),
            "feels_like": round(current["main"]["feels_like"]),
            "humidity": current["main"]["humidity"],
            "wind": round(current["wind"]["speed"]),
            "condition": current["weather"][0]["main"],
            "description": current["weather"][0]["description"].title(),
            "icon": current["weather"][0]["icon"],
        },
        "hourly": hourly,
        "daily": daily,
    }
