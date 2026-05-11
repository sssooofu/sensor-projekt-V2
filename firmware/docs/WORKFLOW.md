# Pico W Firmware Development Workflow

## One-Time Setup

### 1. Flash MicroPython to the Pico W

1. Hold the **BOOTSEL** button on the Pico W while plugging in USB.
2. The device appears as a USB drive named `RPI-RP2`.
3. Download the latest MicroPython UF2 for **Pico W** (not the generic RP2040 build):
   `https://micropython.org/download/RPI_PICO_W/`
   (Current stable: v1.28.0 — `RPI_PICO_W-20241025-v1.28.0.uf2`)
4. Drag the UF2 file onto the `RPI-RP2` drive.
5. The Pico W reboots automatically. MicroPython is now running.

### 2. Install dev tools

```bash
./tools/setup.sh
```

This installs `mpremote` and checks that `/dev/ttyACM0` is detected.

---

## Daily Development Loop

Use `mount.sh` — it mounts your local `src/` directory on the device without copying files. Edit normally in your editor; press Ctrl-D in the mpremote terminal to reload.

```bash
./tools/mount.sh
```

Inside the mpremote session:
- **Ctrl-D** — soft-reset and re-run `main.py` (picks up your latest edits instantly)
- **Ctrl-X** — exit mpremote cleanly

> **WARNING — filesystem corruption bug (MicroPython issue #10898)**
> After pressing Ctrl-D, wait for the `>>>` prompt before pressing Ctrl-C.
> Pressing Ctrl-C immediately after Ctrl-D triggers a known bug that can corrupt
> the entire Pico W filesystem. If that happens, re-flash MicroPython via BOOTSEL.

---

## Inspecting the Device

Open a REPL to run snippets, check sensor values, or poke at module state:

```bash
./tools/repl.sh
```

Useful REPL snippets:

```python
# Check config
import json
with open('config.json') as f: print(json.load(f))

# Read temperature manually
from drivers.ads1115 import ADS1115
from machine import I2C, Pin
i2c = I2C(1, sda=Pin(2), scl=Pin(3))
adc = ADS1115(i2c)
print(adc.read(0))   # AIN0 = pH buffer output

# Check WiFi
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print(wlan.scan())
```

---

## Monitoring Serial Output

Watch `print()` output from `main.py` without entering the REPL:

```bash
./tools/monitor.sh             # uses /dev/ttyACM0
./tools/monitor.sh /dev/ttyACM1   # if ACM0 is wrong
```

Exit: **Ctrl-A then X**.

---

## Resetting the Device

Soft-reset (reruns `main.py`, same as Ctrl-D in the REPL):

```bash
./tools/reset.sh
```

---

## Deploying a Release Build

When development is done, copy all files to device flash (no more live mount):

```bash
./tools/flash.sh
```

This runs `mpremote cp -r src/ :` then `mpremote reset`. After reset the device runs standalone without a USB connection.

---

## Calibration Procedures

### pH (2-point calibration)

1. Edit `config.json` → `calibration.ph`:

```json
"ph": {
  "v_at_ph4": 1.855,
  "v_at_ph7": 1.650
}
```

2. Measure the actual ADS1115 voltage for each buffer solution:
   - pH 4.01 buffer → record voltage as `v_at_ph4`
   - pH 7.00 buffer → record voltage as `v_at_ph7`
3. The slope is `(7 - 4) / (v_at_ph7 - v_at_ph4)` — pH increases as voltage decreases.

### EC (1-point calibration)

1. Use 1413 µS/cm standard solution at a known temperature (25 °C ideal).
2. Edit `config.json` → `calibration.ec`:

```json
"ec": {
  "cell_constant": 1.0,
  "ref_voltage": 1.65,
  "ref_temp_c": 25.0
}
```

3. Adjust `cell_constant` until the reported value matches 1413 µS/cm.

### Soil moisture (2-point calibration)

1. Read raw ADC count in dry air → `dry_count`
2. Submerge sensor in water → `wet_count`
3. Edit `config.json` → `calibration.soil`:

```json
"soil": {
  "dry_count": 26000,
  "wet_count": 13000
}
```

---

## Running Desktop Unit Tests

The calibration math can be tested on any desktop Python (no hardware needed):

```bash
python3 firmware/tests/test_calibration.py
```

---

## Recovering a Boot-Looping Pico

If `main.py` crashes before the REPL loads and the device is stuck in a crash loop:

1. Hold **BOOTSEL**, plug in USB → `RPI-RP2` drive appears.
2. Flash the same MicroPython UF2 again.
3. This overwrites the filesystem — your code is gone. Re-flash with `./tools/flash.sh`.

To avoid this: always test new code changes in the REPL (`./tools/repl.sh`) before writing to `main.py`.

---

## GPIO Pinout Reference

| GPIO | Function | Notes |
|------|----------|-------|
| GP2  | I2C1 SDA | ADS1115, BH1750 |
| GP3  | I2C1 SCL | ADS1115, BH1750 |
| GP4  | SPI0 SCK | LMP91200 |
| GP5  | SPI0 MOSI | LMP91200 |
| GP6  | SPI0 MISO | LMP91200 |
| GP7  | SPI0 CS | LMP91200 |
| GP8  | 1-Wire | DS18B20 temperature |
| GP9  | DHT22 data | Humidity sensor |
| GP10 | Relay control | BC817 base via 1kΩ |
| GP11 | PIR signal | HC-SR501 output |
| GP12 | PIR power gate | MOSFET gate — powers PIR on/off |
| GP13 | EC PWM A | Complementary excitation signal A |
| GP14 | EC PWM B | Complementary excitation signal B (inverted) |
