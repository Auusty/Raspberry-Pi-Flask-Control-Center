#!/bin/bash

# Resolve project root dynamically
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

LOG="$BASE_DIR/logs/chromium.log"
echo "$(date) Exit kiosk requested" >> "$LOG"

# Kill Chromium
pkill -x chromium || true
pkill -x chromium-browser || true

# Kill the kiosk loop script
pkill -f "$BASE_DIR/scripts/start_chromium.sh" || true

sleep 1

# Restore desktop (Pi-specific, expected)
DISPLAY=:0 lxpanel-pi >/dev/null 2>&1 &
DISPLAY=:0 pcmanfm --desktop >/dev/null 2>&1 &

echo "$(date) Desktop restored" >> "$LOG"
exit 0
