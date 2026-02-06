#!/bin/bash
set -e

# Resolve project root dynamically
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

VENV_BIN="$BASE_DIR/venv/bin"
LOG="$BASE_DIR/logs/govee_sync_refresh.log"
SCRIPTS="$BASE_DIR/scripts"

echo "=== refresh started $(date) ===" >> "$LOG"

cd "$SCRIPTS"

"$VENV_BIN/govee-sync" <<EOF >> "$LOG"
2

0
EOF

python3 "$SCRIPTS/govee/post_sync_fix.py" >> "$LOG"

echo "=== refresh completed $(date) ===" >> "$LOG"
