"""
lightsleep power manager.

The Pico W enters lightsleep between polling cycles. The PIR interrupt
(GP11) can wake the device early to capture a motion event.

lightsleep keeps the RTC running and wakes on GPIO edge or timer.
"""

import machine
import time


def sleep(duration_s, pir_pin_num=11):
    """
    Sleep for up to duration_s seconds. Returns True if woken by PIR, False if timer.
    """
    pir = machine.Pin(pir_pin_num, machine.Pin.IN)

    # lightsleep wakes on rising edge of PIR or after duration_ms
    try:
        machine.lightsleep(duration_s * 1000)
    except Exception:
        # Fallback: blocking sleep if lightsleep fails (e.g. during USB debugging)
        time.sleep(duration_s)
        return False

    return bool(pir.value())


def uptime_ms():
    return time.ticks_ms()
