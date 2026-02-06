import json
from pathlib import Path

from scripts.steam_api import steamApi, STEAM_ID

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# =========================
# PINNED GAMES
# =========================

PINNED_GAMES_FILE = DATA_DIR / "pinned_games.json"

def ensure_pinned_games_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not PINNED_GAMES_FILE.exists():
        PINNED_GAMES_FILE.write_text(json.dumps({
            "slot_1": None,
            "slot_2": None,
            "slot_3": None,
            "slot_4": None
        }, indent=4))

def load_pinned_games():
    ensure_pinned_games_file()
    return json.loads(PINNED_GAMES_FILE.read_text())

def save_pinned_games(data):
    ensure_pinned_games_file()
    PINNED_GAMES_FILE.write_text(json.dumps(data, indent=4))


# ================
# PINNED FRIENDS 
# ================

PINNED_FRIENDS_FILE = DATA_DIR / "pinned_friends.json"

def ensure_pinned_friends_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not PINNED_FRIENDS_FILE.exists():
        PINNED_FRIENDS_FILE.write_text(json.dumps({
            "slot_1": None,
            "slot_2": None,
            "slot_3": None,
            "slot_4": None
        }, indent=4))

def load_pinned_friends():
    ensure_pinned_friends_file()
    return json.loads(PINNED_FRIENDS_FILE.read_text())

def save_pinned_friends(data):
    ensure_pinned_friends_file()
    PINNED_FRIENDS_FILE.write_text(json.dumps(data, indent=4))


# ==============
# OWNED GAMES 
# ==============

def get_owned_games():
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

    games = owned.get("response", {}).get("games", [])

    return [
        {
            "appid": int(g["appid"]),
            "name": g["name"],
            "hours": round(g.get("playtime_forever", 0) / 60, 1)
        }
        for g in games
        if "appid" in g and "name" in g
    ]
