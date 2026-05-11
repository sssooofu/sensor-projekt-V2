"""Capacitive soil moisture sensor via ADS1115 AIN2."""


def read(ads, cal, channel=2):
    """
    Return soil moisture as percentage (0-100) or None on error.
    cal = { "dry_count": int, "wet_count": int }
    Higher ADC count = drier (capacitive sensor inverts moisture).
    """
    try:
        raw = ads.read_raw(channel)
    except Exception:
        return None

    dry = cal["dry_count"]
    wet = cal["wet_count"]
    if dry == wet:
        return None

    pct = (dry - raw) / (dry - wet) * 100.0
    pct = max(0.0, min(100.0, pct))
    return round(pct, 1)
