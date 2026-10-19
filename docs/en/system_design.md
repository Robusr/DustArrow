# System Design

## Airframe

DustArrow X is a 40.0 mm diameter, modular sounding-rocket airframe. The
mechanical source is organized by revision:

- `mechanical/source/draft/` — early concepts, including an image bay and a
  four-channel canard study.
- `mechanical/source/launch_revision/` — pre-launch changes.
- `mechanical/source/formal/` — final bays and assemblies.
- `mechanical/source/reprint_models/` — eight revised parts prepared for a
  second print run.

The formal airframe has ten functional sections:

1. Nose cone and parachute bay
2. Telemetry bay
3. Data bay
4. Power bay
5. Dust-sensor bay
6. Gas-sensor bay
7. Smoke-sensor bay
8. Main-control bay
9. Canard bay
10. Propulsion and fin bay

The printed output set contains 28 STL files in `mechanical/output/3dp/` and 15
reprint STLs in `mechanical/output/reprint/`. The nose profile follows the von
Kármán formula recorded in `docs/references/von_karman_formula.txt`.

## Mechanical interfaces

- Modules are stacked along the body axis and joined by gold-finger
  board-to-board contacts.
- Inside each bay, a flexible printed circuit carries signals from the board to
  the connector.
- The parachute bay uses one servo and a large-angle hatch; the canard bay uses a
  two-channel air-rudder mechanism.
- The printed parts are designed for FDM printing. The report does not record
  material, infill, layer height or print time; those values are not invented
  here.

## Electronics

The archive contains nine module BOMs, ten Gerber packages and one legacy
EasyEDA board file. Board outlines were measured from the Gerber outline layer.

| Module | Outline | Key parts | Function |
|---|---|---|---|
| Command A | 30 × 40 mm | FPC connector, GNSS header, 2× board-to-board | Command and GNSS interface |
| Command B | not measured | MPU6050, BMP280, MCU header, FPC | Sensing and control |
| Data | 32 × 101 mm | A39C-T400A22D1a LoRa modem, JST power | Downlink |
| Power | 25 × 25.1 mm | IP5306, USB, charge LEDs | Power management |
| Exploration | 32 × 76 mm | Raspberry Pi Pico, switch, LEDs | Controller / experiment board |
| DustSensor Up | not measured | GP2Y1014AU0F, ZH1.5 connectors | Dust measurement |
| DustSensor Down | 25 × 25 mm | MQ-2, MQ-135 | Gas measurement |
| GasSensorHAT | not measured | MQ-135, gold-finger plug | Gas sensor shield |
| ServoHAT | 25 × 25.9 mm | Servo header, three LEDs | Canard / parachute servo |
| COSensorHAT | Gerber only | no BOM in archive | CO sensor shield |

The consolidated BOM has 48 line items and 57 parts. Sixteen lines have no
price; the known total is CNY 31.44 and is a historical lower bound.

## Ground station

The archived application is a PyQt5 prototype:

```
serial port (9600, 8-N-1)
        │
        ▼
regex parser  X...Y...GX...GY...GZ...
        │
        ├── data.txt (overwritten each frame)
        ├── six Matplotlib canvases (placeholder y = x²)
        └── OpenGL cube (disabled in the archived code)
```

The six planned plots are altitude, pressure, temperature, humidity, visibility
and PM1.0. The six command buttons are emergency parachute, coordinate request,
high-altitude sampling, attitude calibration, data refresh and self-test. None
of the buttons is connected to a transmit path.

## Data flow and protocol

The downlink is a free-form text stream at 9600 baud. The proposed replacement
is a binary frame with a one-byte length and CRC-16/CCITT-FALSE. The frame can
be reassembled from arbitrary serial chunks and rejects corrupted payloads.
See `media/photos/project/telemetry_frame.svg` and
`scripts/verify_theory/test_protocol.py`.

## Power and safety

The power bay uses an IP5306 power-bank controller with USB charging and
single-cell Li-ion input. The archive contains no battery model, capacity,
discharge test or protection review. The propulsion section is a mount for a
commercial solid motor; no motor specification, ignition circuit or launch
procedure is included. Any flight work requires qualified supervision and
compliance with local range-safety rules.
