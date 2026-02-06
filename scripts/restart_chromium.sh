#!/bin/bash
set -e

# Resolve project root dynamically
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

LOGFILE="$BASE_DIR/logs/chromium.log"

echo "$(date) restart requested" >> "$LOGFILE"

# Kill only real Chromium binaries
pkill -x chromium || true
pkill -x chromium-browser || true

sleep 2

# Relaunch kiosk detached from terminal
nohup "$BASE_DIR/scripts/start_chromium.sh" \
  >> "$LOGFILE" 2>&1 &

echo "$(date) restart command issued" >> "$LOGFILE"
exit 0
