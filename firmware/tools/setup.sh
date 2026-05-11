#!/usr/bin/env bash
# Install mpremote and verify Pico W is connected.
set -e

echo "=== Sensor Hub Firmware Setup ==="

if ! command -v mpremote &>/dev/null; then
    echo "Installing mpremote..."
    pip install --user mpremote
fi

echo "mpremote version: $(mpremote version 2>/dev/null || echo 'check failed')"
echo ""
echo "Checking for Pico W..."

if ls /dev/ttyACM* 2>/dev/null; then
    echo "Device found."
else
    echo "No /dev/ttyACM* found."
    echo "  -> Make sure Pico W is connected via USB"
    echo "  -> If freshly flashed, wait a few seconds after boot"
    echo "  -> Check: ls /dev/ttyACM*"
    exit 1
fi

echo ""
echo "Setup complete. Use tools/mount.sh to start developing."
