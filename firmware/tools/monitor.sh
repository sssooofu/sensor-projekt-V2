#!/usr/bin/env bash
# Monitor serial output from Pico W (print statements in firmware).
# Ctrl-X to exit.
#
# If /dev/ttyACM0 is wrong, check: ls /dev/ttyACM*

PORT="${1:-/dev/ttyACM0}"
echo "Monitoring $PORT — Ctrl-X to exit."
python3 -m mpremote connect "$PORT" repl
