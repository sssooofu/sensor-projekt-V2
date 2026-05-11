"""Relay driver with mandatory safety timeout."""

from machine import Pin
import time

_DEFAULT_MAX_S = 600   # 10 minutes absolute ceiling


class Relay:
    def __init__(self, pin_num, max_on_s=_DEFAULT_MAX_S):
        self._pin = Pin(pin_num, Pin.OUT, value=0)
        self._max_on_ms = max_on_s * 1000
        self._on_at = None

    def on(self, duration_s):
        """Energise relay for at most min(duration_s, max_on_s) seconds."""
        duration_ms = min(duration_s * 1000, self._max_on_ms)
        self._pin.value(1)
        self._on_at = time.ticks_ms()
        time.sleep_ms(duration_ms)
        self._pin.value(0)
        self._on_at = None

    def off(self):
        self._pin.value(0)
        self._on_at = None

    def tick(self):
        """Call regularly if on() is not blocking (not used in default flow)."""
        if self._on_at is not None:
            if time.ticks_diff(time.ticks_ms(), self._on_at) >= self._max_on_ms:
                self.off()

    @property
    def is_on(self):
        return bool(self._pin.value())
