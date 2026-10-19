# Replication Guide

## What can and cannot be reproduced

| Asset | Reproducible | Notes |
|---|---|---|
| Mechanical CAD | Yes | SolidWorks sources and STL exports are included |
| PCB fabrication | Yes | Gerber packages and BOMs are included |
| Ground-station UI | Partly | Source runs, but plots and commands are placeholders |
| Flight firmware | No | Not present in the archive |
| Flight data | No | No log, calibration or range test is included |
| Link range | No | Kilometre-scale operation is an unverified design target |

## Prerequisites

- SolidWorks 2021 or later, or a viewer that can open `.SLDPRT` / `.SLDASM`.
- An FDM 3D printer and a slicer.
- A PCB fabricator that accepts Gerber archives.
- Python 3.11 for the ground station.
- A 3.3 V serial adapter for bench tests.

## 1. Review the mechanical revision

Start with `mechanical/source/formal/`. The assemblies are
`装配/整体装配.SLDASM` and `装配/分体装配.SLDASM`. Keep the original Chinese part
and folder names: the assemblies reference them. If you rename a part, open the
assembly in SolidWorks and repair the reference.

STL exports are in `mechanical/output/3dp/`; the second print set is in
`mechanical/output/reprint/`. The print settings are not recorded in the
archive. Choose material, layer height and infill for your own loads and record
them in your build log.

## 2. Fabricate the electronics

1. Send the nine Gerber archives in `electronics/output/gerber/` to a fabricator.
2. Order parts from `BOM/bill_of_materials.csv`. Sixteen lines have no price or
   supplier part; resolve them before ordering.
3. Check the board outlines against the printed bays. The measured outlines are
   listed in `docs/en/system_design.md`.
4. Inspect the gold-finger edges and FPC connectors before soldering.

## 3. Assemble and bench-test

1. Stack the bays without glue first and check alignment.
2. Verify continuity on every gold-finger contact.
3. Power the board from a current-limited supply before connecting the battery.
4. Confirm the 3.3 V rail and the sensor I2C addresses.
5. Do not install a motor or energetic device during bench tests.

## 4. Run the ground station

```bash
cd software/ground_station
python -m pip install -r requirements.txt
python appMain.py
```

Select the serial port, open it at 9600 baud, and start the stream. The archived
code parses `X`, `Y`, `GX`, `GY`, `GZ` fields and writes `data.txt`. The six
plots show `y = x^2`; they are not live data. The OpenGL cube is disabled.

## 5. Verify the software

```bash
python scripts/verify_theory/run_verification.py
```

The suite checks the attitude formulas, complementary filter, proposed frame
format, quaternion conventions, von Kármán profile and measured geometry. It
does not test the GUI or any hardware.

## 6. What a flight build still needs

- Firmware for the RP2040 with a fixed-rate scheduler.
- The framed protocol in `media/photos/project/telemetry_frame.svg`.
- A timestamped logger and a post-flight replay tool.
- A link budget, antenna selection and a range test.
- An arming state machine, continuity checks and a launch checklist.
- A flight-test plan approved by a qualified range safety officer.

## Safety

This repository documents a student project. It does not contain propellant
formulations, ignition circuits or launch procedures. Do not attempt flight
without qualified supervision, legal authorization and a suitable range.
