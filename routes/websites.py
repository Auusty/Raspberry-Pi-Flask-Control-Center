import flask
import requests
from flask import current_app

websites_bp = flask.Blueprint("websites", __name__)

@websites_bp.route("/websites", endpoint="websites")
def websites():
    sites = [
        {"name": "YouTube", "icon": "youtube.svg"},
        {"name": "Google", "icon": "google.svg"},
        {"name": "Twitch", "icon": "twitch.svg"},
        {"name": "ChatGPT", "icon": "chatgpt.svg"},
    ]
    return flask.render_template("programs/websites/websites.html", sites=sites)


@websites_bp.route("/open_site/<site_name>")
def open_site(site_name):
    pc_ip = current_app.config["PC_IP"]
    pc_port = current_app.config["PC_PORT"]
    secret_token = current_app.config["SECRET_TOKEN"]

    site_map = {
        "YouTube": "https://www.youtube.com",
        "Google": "https://www.google.com",
        "Twitch": "https://twitch.tv",
        "ChatGPT": "https://chat.openai.com"
    }

    url = site_map.get(site_name)
    if not url:
        return flask.jsonify({"success": False, "error": "Unknown site"}), 404

    requests.get(
        f"http://{pc_ip}:{pc_port}/open",
        params={"url": url, "token": secret_token},
        timeout=5
    )

    return flask.jsonify({"success": True, "site": site_name})
