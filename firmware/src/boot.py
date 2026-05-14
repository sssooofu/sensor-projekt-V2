import machine
import time

# On power-on or hard reset, wait 5 s before main.py starts so that
# mpremote (flash.sh) can connect. Skipped on soft reset (Ctrl-D) to
# keep the dev loop fast.
if machine.reset_cause() != machine.SOFT_RESET:
    print("Sensor hub — 5 s flash window (Ctrl-C to stay in REPL)")
    time.sleep(5)
