#!/usr/bin/env bash
# Monitor serial output from Pico W (print statements in firmware).
# Ctrl-A then Ctrl-X to exit minicom.
#
# If /dev/ttyACM0 is wrong, check: ls /dev/ttyACM*

PORT="${1:-/dev/ttyACM0}"
echo "Monitoring $PORT at 115200 baud. Ctrl-A then X to exit."
minicom -b 115200 -o -D "$PORT"
