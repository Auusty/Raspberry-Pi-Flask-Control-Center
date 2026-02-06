let lastLightPower = undefined;   // undefined = not initialized yet
let watcherStarted = false;

async function pollSystemState() {
    try {
        const res = await fetch("/api/hexa/status", { cache: "no-store" });
        if (!res.ok) return;

        const data = await res.json();
        const power = data.power === "on";

        // First run: initialize state only, no notification
        if (lastLightPower === undefined) {
            lastLightPower = power;
            return;
        }

        // Notify on ON ↔ OFF transition
        if (power !== lastLightPower) {
            showNotify(
                power ? "Lights were turned on" : "Lights were turned off",
                "Hexa Glide",
                { icon: "/static/icons/light.svg" }
            );
        }

        lastLightPower = power;

    } catch {
        // Silent by design — system watcher should never spam
    }
}

let lastDiscordState = undefined;

async function pollDiscordVoice() {
    try {
        const res = await fetch("/api/discord/voice", { cache: "no-store" });
        if (!res.ok) return;

        const data = await res.json();

        /*
          Normalize to:
          {
            channelName: {
              username: {
                avatar: string | null,
                streaming: boolean,
                video: boolean
              }
            }
          }
        */
        const currentState = {};

        for (const server of Object.values(data)) {
            for (const [channel, members] of Object.entries(server)) {
                currentState[channel] = {};

                for (const m of members) {
                    currentState[channel][m.name] = {
                        avatar: m.avatar || null,
                        streaming: !!m.streaming,
                        video: !!m.video
                    };
                }
            }
        }

        // First run — initialize only
        if (lastDiscordState === undefined) {
            lastDiscordState = currentState;
            return;
        }

        // Compare previous vs current
        for (const channel of Object.keys(currentState)) {
            const prevUsers = lastDiscordState[channel] || {};
            const currUsers = currentState[channel];

            /* ===== JOIN ===== */
            for (const name of Object.keys(currUsers)) {
                if (!prevUsers[name]) {
                    showNotify(
                        `${name} joined ${channel}`,
                        "Discord",
                        {
                            avatar: currUsers[name].avatar,
                            fallbackIcon: "/static/icons/discord.svg"
                        }
                    );
                }
            }

            /* ===== LEAVE ===== */
            for (const name of Object.keys(prevUsers)) {
                if (!currUsers[name]) {
                    showNotify(
                        `${name} left ${channel}`,
                        "Discord",
                        {
                            avatar: prevUsers[name].avatar,
                            fallbackIcon: "/static/icons/discord.svg"
                        }
                    );
                }
            }

            /* ===== STREAM / CAMERA ===== */
            for (const [name, curr] of Object.entries(currUsers)) {
                const prev = prevUsers[name];
                if (!prev) continue;

                if (!prev.streaming && curr.streaming) {
                    showNotify(
                        `${name} started streaming in ${channel}`,
                        "Discord",
                        {
                            avatar: curr.avatar,
                            fallbackIcon: "/static/icons/screen_share.svg"
                        }
                    );
                }

                if (prev.streaming && !curr.streaming) {
                    showNotify(
                        `${name} stopped streaming in ${channel}`,
                        "Discord",
                        {
                            avatar: curr.avatar,
                            fallbackIcon: "/static/icons/stop_screen_share.svg"
                        }
                    );
                }

                if (!prev.video && curr.video) {
                    showNotify(
                        `${name} turned on camera in ${channel}`,
                        "Discord",
                        {
                            avatar: curr.avatar,
                            fallbackIcon: "/static/icons/video_camera_person.svg"
                        }
                    );
                }

                if (prev.video && !curr.video) {
                    showNotify(
                        `${name} turned off camera in ${channel}`,
                        "Discord",
                        {
                            avatar: curr.avatar,
                            fallbackIcon: "/static/icons/video_camera_person_off.svg"
                        }
                    );
                }
            }
        }

        lastDiscordState = currentState;

    } catch {
        // silent by design
    }
}


let lastBambuState = undefined;

async function pollBambuState() {
    try {
        const res = await fetch("/api/p1s/status", { cache: "no-store" });
        if (!res.ok) return;

        const data = await res.json();
        const state = data.state; // e.g. "Printing", "Complete"

        // First run: initialize only
        if (lastBambuState === undefined) {
            lastBambuState = state;
            return;
        }

        // Notify on real state transitions
        if (state !== lastBambuState) {

            if (state === "Printing") {
                showNotify(
                    "Print started",
                    "Bambu P1S",
                    { icon: "/static/icons/printer.svg" }
                );
            }

            if (state === "Complete") {
                showNotify(
                    "Print finished",
                    "Bambu P1S",
                    { icon: "/static/icons/printer.svg" }
                );
            }

            if (state === "Paused") {
                showNotify(
                    "Print paused",
                    "Bambu P1S",
                    { icon: "/static/icons/printer.svg" }
                );
            }

            if (state === "Error") {
                showNotify(
                    "Printer error",
                    "Bambu P1S",
                    { icon: "/static/icons/printer.svg" }
                );
            }
        }

        lastBambuState = state;

    } catch {
        // silent by design
    }
}

let pinnedSteamIDs = new Set();

async function loadPinnedSteamFriends() {
    try {
        const res = await fetch("/api/steam/friends/pinned", { cache: "no-store" });
        if (!res.ok) return;

        const data = await res.json();

        pinnedSteamIDs = new Set(
            Object.values(data).filter(id => typeof id === "string" && id.length)
        );
    } catch {
        // silent by design
    }
}

let lastSteamState = undefined;

async function pollSteamFriends() {
    try {
        const res = await fetch("/api/steam/friends", { cache: "no-store" });
        if (!res.ok) return;

        const friends = await res.json();

        /*
          Normalize to:
          {
            steamid: {
              name: string,
              avatar: string | null,
              status: "online" | "offline" | "away" | "ingame",
              gameid: number | null,
              game: string | null
            }
          }
        */
        const currentState = {};

        for (const f of friends) {
            currentState[f.steamid] = {
                name: f.name,
                avatar: f.avatar || null,
                status: f.status,
                gameid: f.gameid ?? null,
                game: f.text?.startsWith("In Game:")
                    ? f.text.replace("In Game: ", "")
                    : null
            };
        }

        // First run — initialize only (no notifications)
        if (lastSteamState === undefined) {
            lastSteamState = currentState;
            return;
        }

        // Compare previous vs current
        for (const [steamid, curr] of Object.entries(currentState)) {
            const prev = lastSteamState[steamid];
            if (!prev) continue;

            const isPinned = pinnedSteamIDs?.has(steamid);

            const notifyOpts = {
                avatar: curr.avatar,
                fallbackIcon: "/static/icons/steam.svg"
            };

            /* ===== ONLINE / OFFLINE (PINNED ONLY) ===== */
            if (isPinned && prev.status !== curr.status) {

                if (prev.status !== "online" && curr.status === "online") {
                    showNotify(
                        `${curr.name} is now online`,
                        "Steam",
                        notifyOpts
                    );
                }

                if (prev.status === "online" && curr.status !== "online") {
                    showNotify(
                        `${curr.name} went offline`,
                        "Steam",
                        notifyOpts
                    );
                }
            }

            /* ===== START PLAYING (EVERYONE) ===== */
            if (!prev.gameid && curr.gameid) {
                showNotify(
                    `${curr.name} started playing ${curr.game}`,
                    "Steam",
                    notifyOpts
                );
            }

            /* ===== SWITCHED GAMES ===== */
            if (prev.gameid && curr.gameid && prev.gameid !== curr.gameid) {
                showNotify(
                    `${curr.name} switched to ${curr.game}`,
                    "Steam",
                    notifyOpts
                );
            }

            /* ===== STOPPED PLAYING ===== */
            if (prev.gameid && !curr.gameid) {
                showNotify(
                    `${curr.name} stopped playing`,
                    "Steam",
                    notifyOpts
                );
            }
        }

        lastSteamState = currentState;

    } catch {
        // silent by design
    }
}

function startSystemWatcher() {
    if (watcherStarted) return;
    watcherStarted = true;

    setTimeout(async () => {
        pollSystemState();

        await loadPinnedSteamFriends();

        setInterval(pollSystemState, 2000);
        setInterval(pollDiscordVoice, 2000);
        setInterval(pollSteamFriends, 5000);
        setInterval(pollBambuState, 5000);
    }, 800);
}


startSystemWatcher();
