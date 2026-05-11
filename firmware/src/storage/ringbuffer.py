"""
48-slot circular buffer persisted to flash as readings.json.

Reads that fail to upload are queued here and retried next cycle.
Flash endurance: W25Q16JV rated 100k cycles/sector; at 48 writes/day → ~5.7 years.
"""

import json
import os

_PATH = "/readings.json"


class RingBuffer:
    def __init__(self, max_slots=48):
        self._max = max_slots
        self._slots = []
        self._load()

    def _load(self):
        try:
            with open(_PATH) as f:
                self._slots = json.load(f)
        except Exception:
            self._slots = []

    def _save(self):
        with open(_PATH, "w") as f:
            json.dump(self._slots, f)

    def push(self, reading):
        """Add a reading dict. Drops oldest if full."""
        if len(self._slots) >= self._max:
            self._slots.pop(0)
        self._slots.append(reading)
        self._save()

    def peek_all(self):
        """Return all buffered readings without removing them."""
        return list(self._slots)

    def clear(self):
        """Remove all buffered readings after successful upload."""
        self._slots = []
        try:
            os.remove(_PATH)
        except Exception:
            pass

    def __len__(self):
        return len(self._slots)
