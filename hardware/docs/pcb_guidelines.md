# PCB Layout Guidelines

Board: 100 × 80 mm, 2-layer FR4 1.6 mm, ENIG finish, 1 oz copper both layers.

---

## Zone Map

```
┌──────────────────────────────────────────────────────────────────────┐
│  100 mm × 80 mm — TOP VIEW                                           │
│                                                                      │
│  ┌─────────────────┐  ┌───────────────────────────────────────────┐  │
│  │  ANALOG ZONE    │  │          DIGITAL ZONE                     │  │
│  │  (keepout: no   │  │                                           │  │
│  │  digital traces)│  │  ┌────────────────────────────────────┐   │  │
│  │                 │  │  │     RASPBERRY PI PICO W            │   │  │
│  │  [BNC]──[10MΩ]  │  │  │     (castellated, center-right)   │   │  │
│  │     │           │  │  └────────────────────────────────────┘   │  │
│  │  [BAV99]        │  │                                           │  │
│  │     │           │  │  [ADS1115]   [BH1750]                    │  │
│  │  [AD8603]       │  │                                           │  │
│  │     │           │  │  [LMP91200]                              │  │
│  │  [VREF divider] │  │                                           │  │
│  │                 │  │  [AP2112K]   [K1 RELAY + Q1/D2]         │  │
│  └────────┬────────┘  └───────────────────────────────────────────┘  │
│  AGND─────┘ (single-point join at ADS1115 AGND)                      │
│                                                                      │
│  ╔══╦══╦══╦══╦══╦══╗                                                │
│  ║W1║W2║W3║W4║W5║W6║  ← Wago connectors, bottom board edge          │
│  ╚══╩══╩══╩══╩══╩══╝                                                │
│                                                                      │
│  [J8 EC 4-pin terminal]            [USB-C panel header]             │
│  [HDR1 debug 1×4]                  [Spare ADC header]               │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Analog Zone Rules

1. **Keepout**: copper pour prohibition on both layers under AD8603, R1 (10 MΩ), R2 (10 MΩ), and NODE_A trace. No digital signal routing allowed in this zone.

2. **Guard trace on NODE_A**: route the trace from R1 to AD8603 IN+ with a surrounding copper ring on both layers. Connect the ring to AD8603 OUT (the unity-gain output). This eliminates PCB surface leakage in parallel with the 10 MΩ input resistor.

3. **VREF filter**: place C1 (100 nF on VREF_MID) directly at the divider midpoint node, not at the op-amp pin.

4. **Ground plane**: solid GND_ANA pour in analog zone (bottom layer). Join to GND_DIG pour at a single point — the ADS1115 AGND pad. Use a 0 Ω link or ferrite bead at the join.

5. **BNC connector**: right-angle mount at left board edge. The board edge should align with the enclosure wall knockout. Leave 3 mm clearance between BNC body and any component.

6. **AP2112K**: place at the boundary between analog and digital zones. Its output connects to 3V3_ANA pour. Input from 3V3_DIG.

---

## Digital Zone Rules

7. **Pico W**: center-right placement, castellated pads soldered directly (no socket). Saves 3 mm board height for enclosure fit.

8. **ADS1115**: place at the analog/digital boundary. AGND pad connects to GND_ANA; VDD connects to 3V3_ANA; SDA/SCL to GND_DIG. 100 nF decoupling within 0.5 mm of VDD pin.

9. **LMP91200**: place near J8 (EC terminal). SPI traces (GP4–GP7) route as a bundle, away from analog zone. Keep SPI trace lengths within 10 mm of each other.

10. **BH1750**: near ADS1115 (shares I2C bus). Place 100 nF decoupling at VCC pin.

11. **I2C pullups**: place R10 and R11 (4.7 kΩ) close to Pico W GP2/GP3 pads, not at the sensor end.

---

## Relay Zone Rules

12. **Relay (K1)**: right board edge. Orient so contacts face away from logic area.

13. **Creepage**: 4 mm minimum clearance between relay contact traces (RELAY_COM, RELAY_NO, RELAY_NC) and any logic or coil trace. This is a safety requirement for mains-rated relay contacts.

14. **Flyback diode (D2)**: place 1N4148 directly across K1 coil pads. Cathode toward VSYS.

15. **Q1 (BC817)**: place adjacent to K1. Base resistor R8 (1 kΩ) within 3 mm of Q1 base pad.

---

## Power Entry

16. USB-C panel header connector at right board edge. Route VSYS trace as a 0.8 mm wide polygon from connector to Pico W VSYS and K1 coil+. Add 10 µF + 100 nF directly at the header connector.

17. AP2112K input/output both need 10 µF + 100 nF. Place caps within 2 mm of IC pads.

---

## Trace Widths

| Net type | Minimum width |
|----------|--------------|
| Signal (logic, SPI, I2C) | 0.15 mm |
| Power (3V3_DIG, 3V3_ANA) | 0.3 mm |
| VSYS | 0.8 mm |
| Relay contacts | 1.0 mm |
| pH analog (NODE_A) | 0.15 mm with guard ring |

---

## Silkscreen

Label all Wago connectors: W1=DS18B20, W2=DHT22, W3=PIR, W4=GP16, W5=GP17, W6=RELAY.  
Label BNC connector: PH (pH probe).  
Label EC terminal: EC (W=White, Y=Yellow, R=NTC+, B=NTC–).  
Mark board version and date on silkscreen.

---

## Manufacturing Checklist (before ordering)

- [ ] DRC passes with 0 errors
- [ ] Minimum trace/space ≥ 0.15 mm / 0.15 mm
- [ ] Minimum via drill ≥ 0.3 mm
- [ ] BNC and USB-C footprints match physical connector dimensions
- [ ] Relay contact pads have ≥ 4 mm clearance from logic traces
- [ ] 4× M3 mounting holes at board corners (3.2 mm drill, no copper pad)
- [ ] Gerbers exported: F.Cu, B.Cu, F.Mask, B.Mask, F.SilkS, Edge.Cuts, Drill
