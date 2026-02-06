from flask import Blueprint, jsonify, render_template
from scripts.weather import get_weather, get_weather_full

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/weather")
def weather_page():
    return render_template("weather.html")

@weather_bp.route("/api/weather")
def api_weather():
    try:
        return jsonify(get_weather())
    except Exception as e:
        return jsonify({"error": "weather unavailable"}), 500

@weather_bp.route("/api/weather/full")
def api_weather_full():
        return jsonify(get_weather_full())