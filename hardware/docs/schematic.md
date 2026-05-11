# Schematic — Pico W Sensor Hub

Use this as the reference for KiCad entry. Every connection in `bom.csv` traces back here.

---

## System Block Diagram

```
USB-C 5V (power bank)
│
├─ VSYS ──────────────────────────────── Pico W VSYS
│                                         Relay coil (+)
│
└─ Pico W 3V3(OUT)
     ├─ Digital 3V3 ─── BH1750, DS18B20, DHT22, PIR, LMP91200, BC817 pullups
     └─ AP2112K IN ──── AP2112K OUT (Analog 3V3) ─── ADS1115, AD8603, VREF divider, NTC pullup

I2C Bus (GP2/GP3, 4.7kΩ pullups to 3V3_DIG)
  ├── ADS1115  addr 0x48 (ADDR pin → GND)
  └── BH1750   addr 0x23 (ADDR pin → GND via 10kΩ)

SPI Bus (GP4/GP5/GP6/GP7)
  └── LMP91200 (EC analog frontend)

1-Wire (GP8, 4.7kΩ pullup to 3V3_DIG)
  └── DS18B20 temperature sensor (Wago port 1)

GPIO direct:
  GP9  ── DHT22 data (Wago port 2, 10kΩ pullup)
  GP10 ── Relay driver (→ BC817 base)
  GP11 ── PIR output (Wago port 3, 10kΩ pullup, wake IRQ)
  GP12 ── PIR MOSFET gate (power gate for PIR)
  GP13 ── EC excitation PWM A → RC filter → LMP91200
  GP14 ── EC excitation PWM B (complement) → RC filter → LMP91200
  GP15 ── BH1750 ADDR (tied low = 0x23)
  GP16 ── Wago port 4 signal (generic)
  GP17 ── Wago port 5 signal (generic)
```

---

## Net List

### Power Nets

| Net | Source | Destinations |
|-----|--------|-------------|
| VSYS | USB-C VBUS | Pico W VSYS, K1 coil (+), AP2112K VIN |
| 3V3_DIG | Pico W 3V3(OUT) | BH1750 VCC, DS18B20 VDD, DHT22 VDD, LMP91200 VDD, BC817 pull, I2C pullup tops |
| 3V3_ANA | AP2112K VOUT | ADS1115 VDD+AVDD, AD8603 VS+, VREF_TOP (pH divider), NTC pullup top |
| GND_DIG | Pico W GND | All digital IC GND, BC817 emitter, K1 coil (–) via BC817 collector |
| GND_ANA | ADS1115 AGND | AD8603 VS–, pH divider bottom, NTC low side |
| VREF_MID | pH divider midpoint | BNC shield, AD8603 IN– via 100kΩ, C_vref 100nF to GND_ANA |

Single-point AGND/DGND join at ADS1115 AGND pin. Optional: 0Ω link or ferrite bead.

---

## pH Analog Frontend

```
BNC_CENTER ──── R1(10MΩ) ──── NODE_A ──── AD8603 IN+
                                │
                             BAV99 (SOT-23)
                                │ Pin2 = NODE_A
                                │ Pin1 → GND_ANA
                                │ Pin3 → 3V3_ANA

3V3_ANA ── R2(100kΩ) ── NODE_VREF ── R3(100kΩ) ── GND_ANA
                              │
                           C1(100nF) → GND_ANA      [filter cap]
                              │
                           R4(100kΩ) → AD8603 IN–   [sets mid-rail reference]

AD8603 OUT ──── AD8603 IN– (short/0Ω, unity gain)
AD8603 OUT ──── ADS1115 AIN0

BNC_SHIELD ──── NODE_VREF   (reference electrode biased at 1.65V)

AD8603 VS+  ──── 3V3_ANA + C2(100nF) to GND_ANA
AD8603 VS–  ──── GND_ANA
```

**Transfer function**: pH electrode output ±414 mV (pH 0–14 at 25°C) is offset by VREF = 1.65V.
ADS1115 AIN0 sees 1.236V (pH 0) to 2.064V (pH 14). Use ±2.048V PGA setting.

**Guard trace**: surround NODE_A trace with a guard ring connected to AD8603 OUT on the PCB.

---

## EC Analog Frontend (LMP91200)

```
GP13 (PWM A) ── R5(10kΩ) ── C3(100nF) to GND ── LMP91200 excitation IN+
GP14 (PWM B) ── R6(10kΩ) ── C4(100nF) to GND ── LMP91200 excitation IN–

LMP91200 ── SPI ── Pico W (GP4 MISO, GP5 MOSI, GP6 SCK, GP7 CS)
LMP91200 VDD ──── 3V3_DIG + C5(100nF) to GND_DIG
LMP91200 GND ──── GND_DIG

EC 4-wire terminal (J8, Phoenix Contact 4-pin):
  Pin 1 (White) ── LMP91200 Working Electrode (WE)
  Pin 2 (Yellow) ── LMP91200 Reference Electrode (RE)
  Pin 3 (Red)   ── NTC thermistor signal → NODE_NTC
  Pin 4 (Black) ── NTC GND → GND_ANA
```

### NTC Thermistor Divider

```
3V3_ANA ── R7(10kΩ) ── NODE_NTC ── J8 Pin3 (NTC hot side)
                           │
                        C6(100nF) to GND_ANA    [anti-alias]
                           │
                        ADS1115 AIN1

J8 Pin4 (NTC GND) ── GND_ANA
```

---

## ADS1115 Channel Assignments

| Channel | Signal | Sensor |
|---------|--------|--------|
| AIN0 | pH buffer output (AD8603 OUT) | pH electrode |
| AIN1 | NTC divider (NODE_NTC) | EC sensor temperature |
| AIN2 | Soil moisture analog out (Wago port 4 or 5) | Capacitive soil sensor |
| AIN3 | Spare | — |

ADS1115 I2C address: 0x48 (ADDR pin → GND_DIG)

---

## Relay Driver

```
GP10 ── R8(1kΩ) ── Q1(BC817) BASE
Q1 EMITTER ──────── GND_DIG
Q1 COLLECTOR ─┬──── K1 coil (–)
              └──── D2(1N4148) cathode
K1 coil (+) ──┴──── D2(1N4148) anode ──── VSYS

K1 COM ─── J7 Wago port 6 pin 1
K1 NO  ─── J7 Wago port 6 pin 2
K1 NC  ─── J7 Wago port 6 pin 3
```

---

## Wago Ports

| Port | Pin 1 | Pin 2 | Pin 3 | Default sensor |
|------|-------|-------|-------|---------------|
| J2 (Wago 1) | 3V3_DIG | GND_DIG | GP8 (1-Wire) | DS18B20 temperature |
| J3 (Wago 2) | 3V3_DIG | GND_DIG | GP9 (DHT data) | DHT22 temp+humidity |
| J4 (Wago 3) | 3V3_DIG | GND_DIG | GP11 (PIR out) | PIR motion |
| J5 (Wago 4) | 3V3_DIG | GND_DIG | GP16 | Generic / soil moisture signal |
| J6 (Wago 5) | 3V3_DIG | GND_DIG | GP17 | Generic |
| J7 (Wago 6) | K1 COM | K1 NO | K1 NC | Relay SPDT contacts |

**PIR power gate**: a P-channel MOSFET (or NPN switching) controlled by GP12 switches the 3V3 supply to the PIR on Wago port 3. This avoids the 50–65 mA PIR standby current during sleep.

---

## Decoupling Summary

| Location | Cap value | Notes |
|----------|-----------|-------|
| Pico W VSYS entry | 10 µF + 100 nF | Before anything else |
| AP2112K output | 10 µF + 100 nF | Per datasheet |
| ADS1115 VDD | 10 µF + 100 nF | AVDD and VDD pins |
| AD8603 VS+ | 100 nF | Within 0.5 mm of pin |
| LMP91200 VDD | 100 nF | |
| VREF_MID | 100 nF to GND_ANA | Filters virtual mid-rail |
| BC817 collector trace | — | No cap; just keep trace short |
