"""
Desktop unit tests for pH, EC, and soil calibration math.
Run with: python3 firmware/tests/test_calibration.py
No hardware required.
"""

import sys
import math


# ── pH calibration (mirrored from sensors/ph.py) ─────────────────────────────

def ph_from_voltage(v, cal):
    v4 = cal["v_at_ph4"]
    v7 = cal["v_at_ph7"]
    if v4 == v7:
        return None
    slope = (7.0 - 4.0) / (v7 - v4)
    ph = 7.0 + slope * (v - v7)
    return max(0.0, min(14.0, round(ph, 2)))


def test_ph_calibration():
    cal = {"v_at_ph4": 1.855, "v_at_ph7": 1.650}

    assert ph_from_voltage(1.650, cal) == 7.00, "pH 7 at v_at_ph7"
    assert ph_from_voltage(1.855, cal) == 4.00, "pH 4 at v_at_ph4"

    mid_v = (cal["v_at_ph4"] + cal["v_at_ph7"]) / 2
    mid_ph = ph_from_voltage(mid_v, cal)
    assert abs(mid_ph - 5.5) < 0.05, f"pH midpoint off: {mid_ph}"

    # With this calibration, voltage and pH are inversely related:
    # higher voltage → lower pH; lower voltage → higher pH.
    assert ph_from_voltage(3.3, cal) == 0.0,  "high voltage → pH clamped to 0"
    assert ph_from_voltage(0.0, cal) == 14.0, "low voltage → pH clamped to 14"

    # Degenerate: same voltages for both buffers
    bad_cal = {"v_at_ph4": 1.65, "v_at_ph7": 1.65}
    assert ph_from_voltage(1.65, bad_cal) is None, "degenerate cal returns None"

    print("PASS  test_ph_calibration")


# ── EC temperature compensation ───────────────────────────────────────────────

def ec_temp_compensate(ec_raw, temp_c, ref_temp_c=25.0):
    return ec_raw / (1.0 + 0.02 * (temp_c - ref_temp_c))


def test_ec_temp_compensation():
    ec_at_25 = 1413.0

    # At reference temp, no correction
    assert abs(ec_temp_compensate(ec_at_25, 25.0) - 1413.0) < 0.01

    # At 35 °C the raw reading is ~20% higher; correction brings it back
    ec_raw_at_35 = 1413.0 * 1.2
    corrected = ec_temp_compensate(ec_raw_at_35, 35.0)
    assert abs(corrected - 1413.0) < 1.0, f"EC temp correction off: {corrected}"

    print("PASS  test_ec_temp_compensation")


# ── Soil moisture calibration ─────────────────────────────────────────────────

def soil_pct(raw, cal):
    dry = cal["dry_count"]
    wet = cal["wet_count"]
    if dry == wet:
        return None
    pct = (dry - raw) / (dry - wet) * 100.0
    return max(0.0, min(100.0, round(pct, 1)))


def test_soil_calibration():
    cal = {"dry_count": 26000, "wet_count": 13000}

    assert soil_pct(26000, cal) == 0.0,   "dry soil = 0%"
    assert soil_pct(13000, cal) == 100.0, "wet soil = 100%"

    mid = (26000 + 13000) // 2
    assert abs(soil_pct(mid, cal) - 50.0) < 0.1, "midpoint ~50%"

    assert soil_pct(30000, cal) == 0.0,  "over-range clamps to 0"
    assert soil_pct(5000, cal)  == 100.0, "under-range clamps to 100"

    bad_cal = {"dry_count": 20000, "wet_count": 20000}
    assert soil_pct(20000, bad_cal) is None, "degenerate cal returns None"

    print("PASS  test_soil_calibration")


# ── NTC thermistor voltage → temperature ─────────────────────────────────────

def ntc_temp_c(v_ntc, ref_voltage=3.3, pullup=10000, r0=10000, b=3950):
    if v_ntc <= 0 or v_ntc >= ref_voltage:
        return None
    r_ntc = pullup * v_ntc / (ref_voltage - v_ntc)
    temp_k = 1.0 / (math.log(r_ntc / r0) / b + 1.0 / 298.15)
    return round(temp_k - 273.15, 1)


def test_ntc():
    # At 25 °C, NTC = R0 = 10kΩ; voltage divider: V = 3.3 * 10k/(10k+10k) = 1.65V
    t = ntc_temp_c(1.65, ref_voltage=3.3)
    assert t is not None and abs(t - 25.0) < 0.5, f"NTC 25°C: got {t}"

    assert ntc_temp_c(0.0) is None, "zero voltage returns None"
    assert ntc_temp_c(3.3) is None, "rail voltage returns None"

    print("PASS  test_ntc")


if __name__ == "__main__":
    failures = 0
    tests = [test_ph_calibration, test_ec_temp_compensation,
             test_soil_calibration, test_ntc]
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failures += 1
        except Exception as e:
            print(f"ERROR {t.__name__}: {e}")
            failures += 1

    if failures:
        sys.exit(1)
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
