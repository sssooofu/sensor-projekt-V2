"""
PIR motion sensor on GP11, power-gated via MOSFET on GP12.

The PIR (HC-SR501) draws 50-65 mA continuously. Gating it to only the
5-second scan window saves ~30% battery life at 30-minute poll intervals.
"""

from machine import Pin
import time


def read(pir_pin_num=11, gate_pin_num=12, scan_duration_s=5):
    """
    Power the PIR, wait for warm-up + scan window, return True/False or None.
    """
    gate = Pin(gate_pin_num, Pin.OUT, value=0)
    pir = Pin(pir_pin_num, Pin.IN)
    try:
        gate.value(1)
        # HC-SR501 needs ~1 s after power-on before output is stable
        time.sleep_ms(1200)
        detected = False
        deadline = time.ticks_add(time.ticks_ms(), scan_duration_s * 1000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            if pir.value():
                detected = True
                break
            time.sleep_ms(100)
        return detected
    except Exception:
        return None
    finally:
        gate.value(0)
