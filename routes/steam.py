import flask
import requests
from flask import current_app
from collections import Counter

from scripts.steam_api import (
    get_last_online,
    get_recent_games,
    get_top_games,
    get_friends_status
)
from scripts.steam_helpers import (
    load_pinned_games,
    save_pinned_games,
    get_owned_games,
    load_pinned_friends,
    save_pinned_friends
)

steam_bp = flask.Blueprint("steam", __name__)

@steam_bp.route("/api/steam/friends")
def api_steam_friends_debug():
    return flask.jsonify(get_friends_status())

@steam_bp.route("/api/steam/friends/pinned")
def api_steam_pinned_friends():
    return flask.jsonify(load_pinned_friends())

# -----------------------------
# Steam pages
# -----------------------------
@steam_bp.route("/programs/steam")
def steam_program():
    recent_games = get_recent_games()
    top_games = get_top_games()
    last_online = get_last_online()

    return flask.render_template(
        "programs/steam/steam_program.html",
        recent_games=recent_games,
        top_games=top_games,
        last_online=last_online
    )

@steam_bp.route("/programs/steam/recent")
def steam_recent():
    recent_games = get_recent_games()

    # NEW: get friends + count who is playing what
    friends = get_friends_status()

    friends_playing = Counter(
        f["gameid"] for f in friends
        if f.get("gameid")
    )
    last_online = get_last_online()

    return flask.render_template(
        "programs/steam/steam_recent.html",
        recent_games=recent_games,
        friends_playing=friends_playing,
        last_online=last_online
    )

@steam_bp.route("/steam/most-played")
def steam_most_played():
    games = get_top_games(limit=4)

    #get friends + count who is playing what
    friends = get_friends_status()

    friends_playing = Counter(
        f["gameid"] for f in friends
        if f.get("gameid")
    )
    last_online = get_last_online()

    return flask.render_template(
        "programs/steam/steam_most_played.html",
        games=games,
        friends_playing=friends_playing,
        last_online=last_online
    )


@steam_bp.route("/steam/pinned")
def steam_pinned():
    pinned = load_pinned_games()
    owned_games = get_owned_games()

    recent_games = get_recent_games(limit=6)
    recent_appids = {g["appid"] for g in recent_games}

    all_games = [
        g for g in reversed(owned_games)
        if g["appid"] not in recent_appids
    ]

    #get friends + count who is playing what
    friends = get_friends_status()

    friends_playing = Counter(
        f["gameid"] for f in friends
        if f.get("gameid")
    )
    last_online = get_last_online()

    return flask.render_template(
        "programs/steam/steam_pinned.html",
        pinned=pinned,
        recent_games=recent_games,
        all_games=all_games,
        owned_games=owned_games,
        friends_playing=friends_playing,
        last_online=last_online
    )


@steam_bp.route("/steam/friends")
def steam_friends():
    pinned = load_pinned_friends()
    friends = get_friends_status()
    last_online = get_last_online()

    return flask.render_template(
        "programs/steam/steam_friends.html",
        pinned=pinned,
        friends=friends,
        last_online=last_online
    )


# -----------------------------
# Steam APIs
# -----------------------------
@steam_bp.route("/api/steam-status")
def api_steam_status():
    return flask.jsonify(get_last_online())


@steam_bp.route("/api/steam/pin", methods=["POST"])
def api_steam_pin():
    data = flask.request.json
    pinned = load_pinned_games()

    pinned[data["slot"]] = int(data["appid"]) if data["appid"] else None
    save_pinned_games(pinned)

    return {"success": True}


@steam_bp.route("/api/steam/friends/pin", methods=["POST"])
def api_steam_friend_pin():
    data = flask.request.json
    pinned = load_pinned_friends()

    slot = data.get("slot")
    steamid = data.get("steamid")

    if slot not in pinned:
        return {"success": False, "error": "Invalid slot"}, 400

    pinned[slot] = steamid
    save_pinned_friends(pinned)

    return {"success": True}


# -----------------------------
# Steam action (launch game on PC)
# -----------------------------
@steam_bp.route("/open_steam/<appid>")
def open_steam_game(appid):
    pc_ip = current_app.config["PC_IP"]
    pc_port = current_app.config["PC_PORT"]
    secret_token = current_app.config["SECRET_TOKEN"]

    try:
        requests.get(
            f"http://{pc_ip}:{pc_port}/launch_steam",
            params={"appid": appid, "token": secret_token},
            timeout=5
        )
        return flask.jsonify({"success": True})
    except Exception as e:
        return flask.jsonify({"success": False, "error": str(e)}), 500
