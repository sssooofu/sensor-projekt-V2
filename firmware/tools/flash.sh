#!/usr/bin/env bash
# Copy all src/ files to Pico W flash (release build).
# Use this when deploying a finished build, not during development.
# For daily dev, use tools/mount.sh instead.
#
# Workflow: unplug the Pico W, replug it, then run this script within 5 s.
# boot.py opens a 5 s flash window on power-on before main.py starts.
# The device is in lightsleep after the first cycle — unplug/replug resets it.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/../src"

echo "Flashing $SRC_DIR to Pico W..."
mpremote cp -r "$SRC_DIR/." :
echo "Flash complete. Resetting device..."
mpremote reset
echo "Done."
