"""VEML7700 ambient light sensor over I2C (shared bus with ADS1115)."""

from micropython import const
import time

_ADDR      = const(0x10)
_REG_CONF  = const(0x00)
_REG_ALS   = const(0x04)

# gain=1/8x (bits 12:11=0b10), IT=25ms (bits 9:6=0b1100), SD=0 → 0x1300
# Resolution 0.9216 lux/count, max ~60k lux — suits outdoor garden use
_CONF      = bytes([0x00, 0x13])
_LUX_COEFF = 0.9216


class VEML7700:
    def __init__(self, i2c):
        self._i2c = i2c
        self._i2c.writeto_mem(_ADDR, _REG_CONF, _CONF)
        time.sleep_ms(30)

    def lux(self):
        data = self._i2c.readfrom_mem(_ADDR, _REG_ALS, 2)
        raw = data[0] | (data[1] << 8)
        return round(raw * _LUX_COEFF, 1)


def read(i2c):
    """Return illuminance in lux (float) or None on error."""
    try:
        sensor = VEML7700(i2c)
        return sensor.lux()
    except Exception:
        return None
