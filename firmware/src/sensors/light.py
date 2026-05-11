"""BH1750 ambient light sensor over I2C (shared bus with ADS1115)."""

from micropython import const
import time

_ADDR        = const(0x23)
_CONT_HI_RES = const(0x10)   # Continuous high-resolution mode, 1 lux resolution


class BH1750:
    def __init__(self, i2c):
        self._i2c = i2c
        self._i2c.writeto(_ADDR, bytes([_CONT_HI_RES]))
        time.sleep_ms(180)   # first measurement takes up to 180 ms

    def lux(self):
        data = self._i2c.readfrom(_ADDR, 2)
        raw = (data[0] << 8) | data[1]
        return round(raw / 1.2, 1)


def read(i2c):
    """Return illuminance in lux (float) or None on error."""
    try:
        sensor = BH1750(i2c)
        return sensor.lux()
    except Exception:
        return None
