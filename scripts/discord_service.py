import os
import discord
from collections import deque

TEXT_BUFFER_SIZE = 25

text_buffers = {}  # {channel_name: deque([...])}

# ---- Global state Flask will read ----
discord_ready = False

# ---- Intents (what data Discord will send us) ----
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.members = True
intents.presences = True
intents.messages = True
intents.message_content = True

# ---- Shared Discord client ----
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    channel = message.channel.name

    if channel not in text_buffers:
        text_buffers[channel] = deque(maxlen=TEXT_BUFFER_SIZE)

    attachments = []

    for a in message.attachments:
        if a.content_type and a.content_type.startswith("image/"):
            attachments.append(a.url)

    text_buffers[channel].append({
        "author": message.author.display_name,
        "avatar": message.author.display_avatar.url,
        "content": message.content,
        "attachments": attachments,
        "timestamp": message.created_at.isoformat()
    })

    print(
        f"[TEXT] #{channel} | {message.author.display_name}: {message.content}",
        flush=True
    )

@client.event
async def on_ready():
    global discord_ready
    discord_ready = True

    print("Discord service connected", flush=True)
    print(f"Logged in as: {client.user} (id={client.user.id})", flush=True)

    for guild in client.guilds:
        print(f" - {guild.name}", flush=True)

        for channel in guild.text_channels:
            if not channel.permissions_for(guild.me).read_message_history:
                continue

            history = []
            async for msg in channel.history(limit=TEXT_BUFFER_SIZE):
                if msg.author.bot:
                    continue

                images = []
                for a in msg.attachments:
                    if a.content_type and a.content_type.startswith("image/"):
                        images.append(a.url)

                history.append({
                    "author": msg.author.display_name,
                    "avatar": msg.author.display_avatar.url,
                    "content": msg.content,
                    "attachments": images,
                    "timestamp": msg.created_at.isoformat()
                })


            if history:
                text_buffers[channel.name] = deque(
                    reversed(history),
                    maxlen=TEXT_BUFFER_SIZE
                )

                print(
                    f"Preloaded {len(history)} messages from #{channel.name}",
                    flush=True
                )


def get_voice_snapshot():
    """
    {
      "Server": {
        "Voice Channel": [
          {
            "name": str,
            "avatar": str,
            "muted": bool,
            "deafened": bool,
            "streaming": bool,
            "video": bool,
            "playing": bool
          }
        ]
      }
    }
    """
    out = {}

    for guild in client.guilds:
        channels = {}

        for vc in guild.voice_channels:
            members = []

            for member in vc.members:
                vs = member.voice
                if not vs:
                    continue

                # Is Discord detecting a game/app?
                playing = False
                game_name = None

                for a in member.activities:
                    if a.type == discord.ActivityType.playing:
                        playing = True
                        game_name = a.name
                        break


                members.append({
                    "name": member.display_name,
                    "avatar": member.display_avatar.url,

                    # voice state
                    "muted": bool(vs.mute or vs.self_mute),
                    "deafened": bool(vs.deaf or vs.self_deaf),

                    # stream / camera
                    "streaming": bool(vs.self_stream),
                    "video": bool(vs.self_video),

                    # is palying
                    "playing": playing,
                    "game": game_name,
                })

            channels[vc.name] = members

        out[guild.name] = channels

    return out


def run_forever():
    """
    Run the Discord client forever (called from Flask thread).
    """
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN not found in environment")

    client.run(token)

def get_text_snapshot(channel_name, limit=10):
    buf = text_buffers.get(channel_name, [])
    return list(buf)[-limit:]
