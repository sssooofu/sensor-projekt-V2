"""LMP91200 EC analog frontend SPI driver."""

from micropython import const
import time

# LMP91200 register map (8-bit addresses)
_REG_STATUS  = const(0x00)
_REG_LOCK    = const(0x01)
_REG_TIACN   = const(0x10)
_REG_REFCN   = const(0x11)
_REG_MODECN  = const(0x12)

# TIACN: TIA gain = 35 kΩ (bits[5:3] = 0b100)
_TIACN_GAIN_35K  = const(0x20)
# REFCN: internal reference, VREF = VCC/2 (INTZREF=1, REFSLCT=0)
_REFCN_INTREF    = const(0x80)
# MODECN: 3-lead amperometric cell mode
_MODECN_3LEAD    = const(0x03)

_UNLOCK = const(0x00)


class LMP91200:
    """
    SPI mode 0 (CPOL=0, CPHA=0), MSB first, max 1 MHz.
    CS is active low, managed manually for compatibility.
    """

    def __init__(self, spi, cs_pin):
        self._spi = spi
        self._cs = cs_pin
        self._cs.value(1)
        self._init()

    def _write(self, reg, value):
        buf = bytes([reg, value])
        self._cs.value(0)
        self._spi.write(buf)
        self._cs.value(1)

    def _read(self, reg):
        tx = bytes([reg | 0x80, 0x00])
        rx = bytearray(2)
        self._cs.value(0)
        self._spi.write_readinto(tx, rx)
        self._cs.value(1)
        return rx[1]

    def _init(self):
        self._write(_REG_LOCK, _UNLOCK)
        self._write(_REG_TIACN, _TIACN_GAIN_35K)
        self._write(_REG_REFCN, _REFCN_INTREF)
        self._write(_REG_MODECN, _MODECN_3LEAD)
        time.sleep_ms(2)

    def is_ready(self):
        return bool(self._read(_REG_STATUS) & 0x01)

    def shutdown(self):
        """Put LMP91200 into deep sleep."""
        self._write(_REG_MODECN, 0x00)

    def wake(self):
        self._init()
