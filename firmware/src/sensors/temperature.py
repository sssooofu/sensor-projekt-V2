"""DS18B20 1-Wire temperature sensor on GP8."""

import onewire
import ds18x20
from machine import Pin
import time


def read(pin_num=8):
    """Return temperature in °C (float) or None on error."""
    try:
        ow = onewire.OneWire(Pin(pin_num))
        ds = ds18x20.DS18X20(ow)
        roms = ds.scan()
        if not roms:
            return None
        ds.convert_temp()
        time.sleep_ms(750)   # DS18B20 conversion time
        return round(ds.read_temp(roms[0]), 2)
    except Exception:
        return None
