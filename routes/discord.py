import os
import flask
import requests

from flask import Blueprint, current_app
from scripts import discord_service

discord_bp = Blueprint("discord", __name__)


@discord_bp.route("/discord")
def discord_page():
    return flask.render_template("programs/discord/discord.html")


@discord_bp.route("/health/discord")
def discord_health():
    return {
        "discord_connected": discord_service.discord_ready
    }


@discord_bp.route("/api/discord/voice")
def discord_voice():
    return discord_service.get_voice_snapshot()


@discord_bp.route("/api/discord/join", methods=["POST"])
def discord_join():
    data = flask.request.json or {}

    channel_name = data.get("channel_name")
    member_count = data.get("member_count", 0)

    if not channel_name:
        return {"success": False, "error": "missing channel_name"}, 400

    pc_ip = current_app.config.get("PC_IP")
    pc_port = current_app.config.get("PC_PORT")
    secret = current_app.config.get("SECRET_TOKEN")

    if not pc_ip or not pc_port:
        return {"success": False, "error": "PC not configured"}, 500

    try:
        res = requests.post(
            f"http://{pc_ip}:{pc_port}/discord/join",
            json={
                "channel_name": channel_name,
                "member_count": member_count,
                "token": secret
            },
            timeout=3
        )

        if not res.ok:
            return {"success": False, "error": "PC rejected request"}, 502

        return res.json()

    except Exception as e:
        print("Discord join forward failed:", e, flush=True)
        return {"success": False}, 500

@discord_bp.route("/api/discord/leave", methods=["POST"])
def discord_leave():
    pc_ip = current_app.config.get("PC_IP")
    pc_port = current_app.config.get("PC_PORT")
    secret = current_app.config.get("SECRET_TOKEN")

    if not pc_ip or not pc_port:
        return {"success": False, "error": "PC not configured"}, 500

    try:
        res = requests.post(
            f"http://{pc_ip}:{pc_port}/discord/leave",
            json={"token": secret},
            timeout=3
        )

        if not res.ok:
            return {"success": False, "error": "PC rejected request"}, 502

        return res.json()

    except Exception as e:
        print("Discord leave forward failed:", e, flush=True)
        return {"success": False}, 500


@discord_bp.route("/api/discord/text_channels")
def discord_text_channels():
    channels = []

    for key in os.environ:
        if key.startswith("DISCORD_TEXT_"):
            name = key.replace("DISCORD_TEXT_", "").lower().replace("_", "-")
            channels.append(name)

    channels.sort()
    return channels


@discord_bp.route("/api/discord/text/messages")
def discord_text_messages():
    channel = flask.request.args.get("channel")
    if not channel:
        return []

    return discord_service.get_text_snapshot(channel, limit=25)


@discord_bp.route("/api/discord/text/open", methods=["POST"])
def discord_text_open():
    data = flask.request.json or {}
    channel_name = data.get("channel_name")

    if not channel_name:
        return {"success": False, "error": "missing channel_name"}, 400

    pc_ip = current_app.config.get("PC_IP")
    pc_port = current_app.config.get("PC_PORT")
    secret = current_app.config.get("SECRET_TOKEN")

    if not pc_ip or not pc_port:
        return {"success": False, "error": "PC not configured"}, 500

    try:
        res = requests.post(
            f"http://{pc_ip}:{pc_port}/discord/text/open",
            json={
                "channel_name": channel_name,
                "token": secret
            },
            timeout=3
        )

        if not res.ok:
            return {"success": False, "error": "PC rejected request"}, 502

        return res.json()

    except Exception as e:
        print("Discord text open forward failed:", e, flush=True)
        return {"success": False}, 500

@discord_bp.route("/api/discord/screen_share", methods=["POST"])
def discord_screen_share():
    pc_ip = current_app.config.get("PC_IP")
    pc_port = current_app.config.get("PC_PORT")
    secret = current_app.config.get("SECRET_TOKEN")

    try:
        res = requests.post(
            f"http://{pc_ip}:{pc_port}/discord/screen_share",
            json={"token": secret},
            timeout=3
        )

        if not res.ok:
            return {"success": False}, 502

        return res.json()

    except Exception as e:
        print("Screen share forward failed:", e, flush=True)
        return {"success": False}, 500

@discord_bp.route("/api/discord/voice_action", methods=["POST"])
def discord_voice_action():
    data = flask.request.json or {}
    action = data.get("action")

    if action not in ("mute", "deafen"):
        return {"success": False, "error": "Invalid action"}, 400

    pc_ip = current_app.config.get("PC_IP")
    pc_port = current_app.config.get("PC_PORT")
    secret = current_app.config.get("SECRET_TOKEN")

    try:
        res = requests.post(
            f"http://{pc_ip}:{pc_port}/discord/voice_action",
            json={
                "action": action,
                "token": secret
            },
            timeout=3
        )

        if not res.ok:
            return {"success": False}, 502

        return res.json()

    except Exception as e:
        print("Voice action forward failed:", e, flush=True)
        return {"success": False}, 500
