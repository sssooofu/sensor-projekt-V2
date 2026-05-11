"""DHT22 humidity + temperature sensor on GP9."""

import dht
from machine import Pin


def read(pin_num=9):
    """Return (humidity_pct, temp_c) tuple or (None, None) on error."""
    try:
        sensor = dht.DHT22(Pin(pin_num))
        sensor.measure()
        return round(sensor.humidity(), 1), round(sensor.temperature(), 2)
    except Exception:
        return None, None
