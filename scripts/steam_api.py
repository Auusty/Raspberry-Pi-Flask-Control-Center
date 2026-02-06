import os
from dotenv import load_dotenv
from steam.webapi import WebAPI
from pathlib import Path
from datetime import datetime

# ============================================================
# Environment
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "envs" / "steam.env")

STEAM_ID = os.getenv("STEAM_ID")
STEAM_KEY = os.getenv("STEAM_KEY")

if not STEAM_ID:
    raise RuntimeError("STEAM_ID not found")

if not STEAM_KEY:
    raise RuntimeError("STEAM_KEY not found")

steamApi = WebAPI(STEAM_KEY)

# ============================================================
# Profile / Status
# ============================================================

def get_last_online():
    profile = steamApi.ISteamUser.GetPlayerSummaries(steamids=STEAM_ID)
    players = profile["response"].get("players", [])

    if not players:
        return {
            "status": "unknown",
            "text": "Unknown",
            "avatar": None
        }

    p = players[0]
    avatar = p.get("avatarfull")

    if p.get("gameextrainfo"):
        return {
            "status": "ingame",
            "text": f"In Game: {p['gameextrainfo']}",
            "avatar": avatar
        }

    persona = p.get("personastate", 0)

    if persona in (1, 2, 5, 6):
        return {
            "status": "online",
            "text": "Online",
            "avatar": avatar
        }

    if persona in (3, 4):
        return {
            "status": "away",
            "text": "Away",
            "avatar": avatar
        }

    last = p.get("lastlogoff")
    if last:
        last_seen = datetime.fromtimestamp(last)
        return {
            "status": "offline",
            "text": f"Last online: {last_seen.strftime('%b %d, %I:%M %p')}",
            "avatar": avatar
        }

    return {
        "status": "unknown",
        "text": "Unknown",
        "avatar": avatar
    }

# ============================================================
# Games
# ============================================================

def get_recent_games(limit=4):
    recent = steamApi.call(
        "IPlayerService.GetRecentlyPlayedGames",
        steamid=STEAM_ID,
        count=limit
    )

    games = recent["response"].get("games", [])
    return [
        {
            "appid": g["appid"],
            "name": g["name"],
            "hours": round(g.get("playtime_2weeks", 0) / 60, 1)
        }
        for g in games[:limit]
    ]


def get_top_games(limit=4):
    owned = steamApi.call(
        "IPlayerService.GetOwnedGames",
        steamid=STEAM_ID,
        appids_filter=[],
        include_appinfo=True,
        include_played_free_games=True,
        include_free_sub=False,
        language="en",
        include_extended_appinfo=True
    )

    games = owned["response"].get("games", [])
    games.sort(key=lambda g: g.get("playtime_forever", 0), reverse=True)

    return [
        {
            "appid": g["appid"],
            "name": g["name"],
            "hours": round(g.get("playtime_forever", 0) / 60, 1)
        }
        for g in games[:limit]
    ]

# ============================================================
# Friends (NOW INCLUDES GAMEID)
# ============================================================

def get_friends_status(limit=None):
    friends_data = steamApi.ISteamUser.GetFriendList(
        steamid=STEAM_ID,
        relationship="friend"
    )

    friends = friends_data.get("friendslist", {}).get("friends", [])
    if not friends:
        return []

    steam_ids = [f["steamid"] for f in friends]
    if limit:
        steam_ids = steam_ids[:limit]

    summaries = steamApi.ISteamUser.GetPlayerSummaries(
        steamids=",".join(steam_ids)
    )

    players = summaries["response"].get("players", [])
    results = []

    for p in players:
        gameid = None

        if p.get("gameextrainfo"):
            status = "ingame"
            text = f"In Game: {p['gameextrainfo']}"
            gameid = int(p.get("gameid")) if p.get("gameid") else None
        else:
            persona = p.get("personastate", 0)
            if persona in (1, 2, 5, 6):
                status, text = "online", "Online"
            elif persona in (3, 4):
                status, text = "away", "Away"
            else:
                status = "offline"
                last = p.get("lastlogoff")
                if last:
                    last_seen = datetime.fromtimestamp(last)
                    text = f"Last online: {last_seen.strftime('%b %d, %I:%M %p')}"
                else:
                    text = "Offline"

        results.append({
            "steamid": p["steamid"],
            "name": p["personaname"],
            "status": status,
            "text": text,
            "avatar": p.get("avatarfull"),
            "gameid": gameid
        })

    return results
