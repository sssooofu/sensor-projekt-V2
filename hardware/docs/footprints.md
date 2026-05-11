# KiCad Footprint Reference

Map every BOM line to its KiCad library footprint before starting schematic entry.
Flags: ⚠ = verify against datasheet before placing; ✗ = DNP v1.

---

## ICs

| Ref | Part | Package | KiCad footprint |
|-----|------|---------|-----------------|
| U1 | Pico W SC0918 | Castellated | `MicrocontrollerBoard:RaspberryPi_PicoW` |
| U2 | ADS1115IDGSR | VSSOP-10 | `Package_SO:VSSOP-10_3x3mm_P0.5mm` |
| U3 ✗ | LMP91200SD/NOPB | SOIC-14 | `Package_SO:SOIC-14_3.9x8.65mm_P1.27mm` |
| U4 | AD8603ARTZ-R2 | SC70-5 | `Package_TO_SOT_SMD:SOT-23-5` |
| U5 | AP2112K-3.3TRG1 | SOT-23-5 | `Package_TO_SOT_SMD:SOT-23-5` |
| U6 | VEML7700-TT | ODFN-6 2×2 mm | `Package_DFN_QFN:DFN-6-1EP_2x2mm_P0.65mm_EP0.7x1.6mm` ⚠ |

**U2 note**: the BOM description previously said "SOIC-16" — that is wrong. DGS suffix = VSSOP-10 (3×3 mm, 0.5 mm pitch). Use the footprint above.

**U6 note**: verify the exposed-pad dimensions of the ODFN-6 footprint against the VEML7700-TT datasheet (Vishay document 84471) before placing. Pad size is 0.35×0.65 mm typ.

---

## Discretes

| Ref | Part | Package | KiCad footprint |
|-----|------|---------|-----------------|
| D1 | BAV99 | SOT-23 | `Package_TO_SOT_SMD:SOT-23` |
| D2 | 1N4148W | SOD-123 | `Diode_SMD:D_SOD-123` |
| Q1 | BC817-40 | SOT-23 | `Package_TO_SOT_SMD:SOT-23` |
| Q2 | BSS84PXUMA1 | SOT-23 | `Package_TO_SOT_SMD:SOT-23` |
| K1 | SRD-05VDC-SL-C | THT relay | `Relay_THT:Relay_SPDT_Songle_SRD-xxVDC-SL-C` ⚠ |

**K1 note**: confirm coil pin 1/2 and contact COM/NO/NC orientation against the Songle datasheet — the footprint pin numbers must match before routing.

---

## Passives

All resistors use the same footprint. Capacitors split by case size.

| Ref | Value | Package | KiCad footprint |
|-----|-------|---------|-----------------|
| R1–R17 (all) | various | 0603 | `Resistor_SMD:R_0603_1608Metric` |
| R15–R16 ✗ | 10 kΩ DNP | 0603 | same — place footprint, do not populate |
| C1–C2, C6–C12 | 100 nF | 0603 | `Capacitor_SMD:C_0603_1608Metric` |
| C3–C5 ✗ | 100 nF DNP | 0603 | same — place footprint, do not populate |
| C13–C16 | 10 µF | 0805 | `Capacitor_SMD:C_0805_2012Metric` |
| C17–C18 | 1 µF | 0603 | `Capacitor_SMD:C_0603_1608Metric` |

---

## Connectors

| Ref | Part | Type | KiCad footprint |
|-----|------|------|-----------------|
| J1 | TE 5-1634500-1 | RA BNC, SMD | `Connector_Coaxial:BNC_TE-Connectivity_1-1634500-1_Horizontal` ⚠ |
| J2–J7 | Wago 2060-453 | THT 3-pin 5 mm | `TerminalBlock_Wago:TerminalBlock_Wago_2060-453_1x03_P5.00mm_Horizontal` ⚠ |
| J8 | Phoenix PT 1.5/4-3.5-H | THT 4-pin 3.5 mm | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5_4-3,5-H_1x04_P3.50mm_Horizontal` ⚠ |
| J9 | Phoenix PT 1.5/2-5-H | THT 2-pin 5 mm | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5_2-5,0-H_1x02_P5.00mm_Horizontal` ⚠ |
| HDR1 | PEC04SAAN | 2.54 mm 1×4 | `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` |

**J1 note**: KiCad may list this as `1-1634500-1` (TE sometimes strips the leading `5-` packaging prefix). Open footprint in KiCad 3D viewer and compare to the TE datasheet drawing before finalising — the SMD pads and 4× through-hole mounting posts must align.

**J2–J7 note**: the Wago 2060 footprint exists in KiCad 7+ standard library. If missing, the 3-pin 5 mm Phoenix MSTB footprint (`Connector_Phoenix_MSTB:PhoenixContact_MSTB_2,5_3-G_1x03_P5.00mm_Horizontal`) is dimensionally compatible for prototyping.

**J8/J9 note**: Phoenix PT 3.5 mm and 5 mm footprints are in the `TerminalBlock_Phoenix` library. If the exact variant isn't present search by pitch — horizontal (H) and vertical variants share the pad layout.

---

## Mounting holes

Four M3 mounting holes at board corners — no component in BOM, add manually in KiCad:

`MountingHole:MountingHole_3.2mm_M3` — 3.2 mm drill, no copper pad, 4× at corners.

Board outline: 100 × 80 mm rectangle on `Edge.Cuts` layer.
