<p align="center">
  <img src="./media/photos/project/banner.png" alt="DustArrow X full assembly render" width="800"/>
</p>

<h1 align="center">DustArrow X · 沙尘利“箭”</h1>

<p align="center">
  <strong>A modular telemetry system for 40 mm meteorological sounding rockets</strong>
  <br>
  RP2040 sensing stack, LoRa downlink and a PyQt5 ground-station prototype
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/PyQt5-ground_station-41CD52?logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/SolidWorks-CAD-e63946" alt="SolidWorks">
  <img src="https://img.shields.io/badge/Status-prototype-f59e0b" alt="Status: prototype">
  <br>
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">中文</a> |
  <a href="./README.fr.md">Français</a>
</p>

---

## Name origin

The Chinese name «沙尘利“箭”» combines «沙尘» (sand and dust) with «利箭» (a sharp
arrow). It refers both to the sounding rocket and to the idea of a useful tool
against dust storms. The English name **DustArrow** is a direct rendering. The
modular architecture is inspired by the experiment racks on the Chinese space
station. The third generation adds **X**; in the January 2024 TV feature the
student says X means “infinite possibilities”.

## About the project

DustArrow X is the third documented generation of a student project from Guyuan
No. 1 Middle School, Ningxia, after Theta and Beta. It was presented at the China
Adolescents Science and Technology Innovation Contest. The goal is to measure the
vertical structure of the atmosphere during dust events with a low-cost
sounding rocket. The project was featured on Shanghai TV’s *Young Edison* Season 8
in January 2024.

The airframe is 40 mm in diameter and has ten functional sections. Modules are
joined by gold-finger board-to-board contacts, with a flexible printed circuit
inside each bay. The flight electronics centre on an RP2040 with an MPU6050, a
BMP280, an ATGM336H GNSS receiver, an A39C LoRa modem, a GP2Y1014AU0F dust
sensor and MQ-series gas sensors. The ground segment is a Python/PyQt5
telemetry dashboard.

This repository contains the mechanical CAD, Gerber files, BOM, ground-station
source, original report, presentation and media. It does **not** contain the
flight firmware, flight logs, sensor calibration or range tests. The archived
ground station is a UI prototype: the plots are placeholders and the command
buttons are not connected. See the [errata](docs/errata.md).

## Key features

- **40 mm modular airframe** — ten functional bays with gold-finger and FPC
  connections; printed parts can be replaced individually.
- **RP2040 sensing stack** — six-axis IMU, barometer, GNSS, dust and gas
  sensors.
- **LoRa downlink** — A39C-T400A22D1a serial modem received at 9600 baud.
- **PyQt5 ground-station prototype** — six plot panels, a 3D attitude cube and
  six command buttons.
- **Open fabrication files** — SolidWorks sources, STL, STEP, Gerber, BOM and
  silkscreen artwork.
- **Traceable verification** — sixteen reviewed errata and 32 Python tests, with
  failures reported rather than hidden.

## System architecture

<p align="center">
  <img src="./media/photos/project/system_architecture.svg" alt="DustArrow X system architecture" width="900"/>
  <br>
  <em>System architecture. Dashed links are wireless; the ground-station command path is not implemented in the archived code.</em>
</p>

- **Mechanical** — nose and parachute bay, telemetry bay, data bay, power bay,
  three sensor bays, main-control bay, canard bay and propulsion/fin bay. The
  parachute uses one servo with a large-angle hatch; the canard bay uses a
  two-channel air-rudder mechanism.
- **Electronics** — nine module BOMs and ten Gerber packages. The main boards
  centre on the RP2040, MPU6050, BMP280, ATGM336H and A39C.
- **Downlink** — a 9600 baud, 8-N-1 free-form text stream. The archived regular
  expression has no header, length or checksum; a binary frame with CRC-16 is
  recommended.
- **Ground station** — PyQt5, Matplotlib and OpenGL. In the archived version the
  six plots are placeholders, the OpenGL widget is commented out and the buttons
  do not transmit.

## Theory and design

At rest, the accelerometer measures the reaction to gravity. With \(x\) forward,
\(y\) right and \(z\) up:

\[
\phi = \operatorname{atan2}(a_y, a_z),
\qquad
\theta = \operatorname{atan2}\!\left(-a_x,\sqrt{a_y^2+a_z^2}\right).
\]

The first-order complementary filter in discrete form is

\[
\alpha = \frac{\tau}{\tau+\Delta t},
\qquad
\theta_k = \alpha\,\theta_{\mathrm{acc},k}
+ (1-\alpha)\left(\theta_{k-1} + \omega_y \Delta t\right).
\]

The report writes \(\arctan(a_y/a_z)\), which loses the quadrant: at
\(150^\circ\) it returns \(-30^\circ\). A six-axis IMU also cannot observe yaw.
The full derivation, limits and quaternion conventions are in
[Theory of operation](docs/en/theory_of_operation.md); every change is listed in
the [errata](docs/errata.md).

## Repository structure

```text
DustArrow/
├── BOM/                     # consolidated bill of materials
├── electronics/
│   ├── datasheets/          # manufacturer datasheets
│   ├── output/              # Gerber, BOM, silkscreen, PCB 3D
│   └── source/              # legacy EasyEDA project
├── mechanical/
│   ├── output/              # STL, STEP, reprint files
│   └── source/              # SolidWorks drafts, formal parts, reprints
├── simulation/cfd/          # CFD project and animations
├── software/ground_station/ # archived PyQt5 dashboard
├── firmware/                # status note only
├── docs/                    # trilingual docs, errata, verification, archive
├── media/                   # photos, GIFs, videos
├── scripts/verify_theory/   # reproducible tests
└── .github/                 # issue and PR templates
```

Mechanical sources keep their original Chinese filenames because SolidWorks
assemblies resolve parts by name. STL outputs use English names and include a
`part_name_mapping.csv`. The full path mapping is in
[MIGRATION_NOTES.md](MIGRATION_NOTES.md).

## Bill of materials

| Metric | Value |
|---|---:|
| PCB modules | 9 |
| BOM line items | 48 |
| Parts | 57 |
| Known cost | CNY 31.44 |
| Unpriced lines | 16 |

The known cost covers only lines with a price. Sixteen lines, including the
RP2040/Pico, LoRa modem, GNSS module and MQ sensors, have no price, so CNY 31.44
is a historical lower bound. See
[BOM/bill_of_materials.csv](BOM/bill_of_materials.csv) and
[BOM/README.md](BOM/README.md).

## Getting started

**Ground station** (Python 3.11):

```bash
cd software/ground_station
python -m pip install -r requirements.txt
python appMain.py
```

Select the serial port and open it at 9600 baud. The archived code parses `X`,
`Y`, `GX`, `GY`, `GZ` fields and writes `data.txt`; the plots and the 3D cube are
not live data. See
[software/ground_station/README.md](software/ground_station/README.md).

**Mechanical and electronics**: open the assemblies in
[mechanical/source/formal/](mechanical/source/formal/) or use the STL files in
[mechanical/output/3dp/](mechanical/output/3dp/). PCB fabrication files are in
[electronics/output/gerber/](electronics/output/gerber/). The step-by-step
procedure is in the [replication guide](docs/en/replication_guide.md).

**Verification**:

```bash
python scripts/verify_theory/run_verification.py
```

## Demo and testing

<p align="center">
  <img src="./media/photos/project/cfd_demo.gif" alt="CFD demonstration of the von Kármán nose and canards" width="800"/>
  <br>
  <em>CFD demonstration. Original videos are in media/videos/.</em>
</p>

<p align="center">
  <img src="./media/photos/project/canard_deployment.gif" alt="Canard deployment and nose separation mechanism animation" width="800"/>
  <br>
  <em>Mechanism animation: nose separation, canard deployment and recovery.</em>
</p>

<p align="center">
  <img src="./media/photos/project/ground_station_ui.png" alt="Archived ground-station interface" width="800"/>
  <br>
  <em>Archived ground-station interface. The six curves show y = x² placeholders, not measurements.</em>
</p>

Verification result: 32 tests pass, covering attitude formulas, complementary
filtering, quaternions, frame parsing, the von Kármán profile, STL geometry,
Gerber outlines and BOM cost. The test inventory and the corrected first-run
failure are recorded in [Verification](docs/verification.md).

## Media coverage

In January 2024, Shanghai TV’s youth science programme *Young Edison* Season 8,
*Tomorrow’s World*, featured the project. The episode follows a test flight near
Guyuan in late autumn or early winter 2023: remote ignition failed, the team
switched to wired ignition, the rocket left the rail, and the sensor section was
recovered while the parachute bay and propulsion module were lost. The student
estimates 80% recovery completeness. The broadcast calls the flight a success;
this repository describes it as a partial recovery, not a complete airframe
recovery.

The episode also explains that X means “infinite possibilities” and that the
ground station reads a text file for simple attitude feedback, which matches the
archived prototype. It provides no telemetry log or quantitative sensor data. The
TV video is not redistributed here.

- [Detailed media coverage](docs/en/media_coverage.md)
- Official pages: [preview](https://www.kankanews.com/detail/ELwxNKJWGy9),
  [episode](https://www.kankanews.com/detail/LMwVGm9WB2z),
  [season overview](https://www.kankanews.com/detail/boy4AKjBxQ1)

## Design specifications

| Parameter | Value | Source / status |
|---|---|---|
| Airframe diameter | 40.0 mm | Measured, STL bounding box |
| Nose profile | von Kármán curve | Report formula, checked numerically |
| Command A outline | 30 × 40 mm | Measured, Gerber outline |
| Power outline | 25.0 × 25.1 mm | Measured, Gerber outline |
| Data outline | 32 × 101 mm | Measured, Gerber outline |
| Exploration outline | 32 × 76 mm | Measured, Gerber outline |
| Microcontroller | RP2040 | BOM / report |
| IMU | MPU6050 | BOM |
| Barometer | BMP280 | BOM; the report says BMP-180, [to be confirmed] |
| GNSS | ATGM336H-5N | Report |
| Downlink | A39C-T400A22D1a | Report / BOM |
| Dust sensor | GP2Y1014AU0F | BOM |
| Gas sensors | MQ-2, MQ-135 | BOM |
| Ground serial | 9600, 8-N-1 | Source code |
| Link range | Kilometre-scale | Design target, unverified |
| Flight test | One TV-documented flight in late autumn/early winter 2023; sensor section recovered, parachute bay and propulsion module lost; no telemetry log | Broadcast evidence, partial recovery |
| Total mass | Not recorded | Not available |

## Errata and known issues

- The roll formula is changed from \(\arctan(a_y/a_z)\) to `atan2(a_y, a_z)` to
  fix the quadrant error.
- A six-axis IMU cannot observe yaw; the “3D attitude” cube shows only roll and
  pitch.
- The archived regular expression cannot handle split or concatenated packets; a
  frame with a length field and CRC-16 is proposed but not implemented in
  firmware.
- The archive has no flight firmware, flight data, calibration records or link
  budget.

See the full [errata](docs/errata.md) and the verification
[limits](docs/verification.md).

## Roadmap

1. Write RP2040 firmware using the CRC-16 binary frame and implement the command
   uplink.
2. Replace the placeholder plots with real-time plotting, timestamped logging
   and post-flight replay.
3. Run bench tests, a link budget and a range test, then publish anonymised data.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Do not submit propellant formulations,
ignition procedures or launch instructions.

## License

Code, documentation and original media are released under [MIT](LICENSE).
Third-party datasheets and the contest logo are excluded; see
[References](docs/references/README.md).

## Acknowledgments

Thanks to Guyuan No. 1 Middle School, Ningxia, and the China Adolescents Science
and Technology Innovation Contest for the platform. Thanks to Shanghai Media
Group and the *Young Edison* team for documenting the project. The project uses
SolidWorks, EasyEDA, Python, PyQt5, Matplotlib, PySerial and OpenGL. The original
report, presentation and legacy code are preserved in [docs/archive/](docs/archive/).
