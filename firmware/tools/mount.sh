#!/usr/bin/env bash
# Mount src/ on the Pico W for live development.
# Edit files normally in your editor — press Ctrl-D in this terminal to reload.
# No file copying needed during development.
#
# WARNING: Do NOT press Ctrl-D followed immediately by Ctrl-C.
# That triggers MicroPython bug #10898 which can corrupt the filesystem.
# Always wait for the >>> prompt before pressing Ctrl-C.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/../src"

echo "Mounting $SRC_DIR on Pico W..."
echo "Ctrl-D = soft-reset and reload   |   Ctrl-X = exit mpremote"
echo ""

mpremote mount "$SRC_DIR" repl
