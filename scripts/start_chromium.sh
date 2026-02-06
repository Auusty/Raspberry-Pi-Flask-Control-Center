#!/bin/bash
set -e

# Resolve project root dynamically
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

export DISPLAY=:0
export XAUTHORITY="$HOME/.Xauthority"

LOGFILE="$BASE_DIR/logs/chromium.log"

echo "========================" >> "$LOGFILE"
echo "$(date) Chromium start requested" >> "$LOGFILE"
echo "USER=$(whoami)" >> "$LOGFILE"
echo "DISPLAY=$DISPLAY" >> "$LOGFILE"
echo "BASE_DIR=$BASE_DIR" >> "$LOGFILE"

# Disable screen blanking & power management (X11)
xset s off || true
xset s noblank || true
xset -dpms || true

# Wait for Flask to be available
echo "$(date) Waiting for Flask..." >> "$LOGFILE"
until curl -s http://localhost:5000/health > /dev/null; do
  sleep 1
done
echo "$(date) Flask is up" >> "$LOGFILE"

# Kill existing Chromium instances (safety)
pkill -x chromium || true
pkill -x chromium-browser || true
sleep 1

# Launch Chromium in kiosk mode
/usr/bin/chromium \
  --kiosk http://localhost:5000 \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-translate \
  --disable-features=TranslateUI \
  --password-store=basic \
  --incognito \
  --autoplay-policy=no-user-gesture-required \
  >> "$LOGFILE" 2>&1 &

echo "$(date) Chromium launched" >> "$LOGFILE"
exit 0
