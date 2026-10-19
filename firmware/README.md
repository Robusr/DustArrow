# Flight Firmware

**The flight firmware is not present in this archive.**

The report states that the RP2040 firmware was written in MicroPython and that
it ran attitude estimation and sensor preprocessing in two threads. No `.py`,
`.uf2`, `.hex`, `.bin` or project file for the flight computer was found in the
source folder. The hardware BOM and board designs were recovered, but the code
that ran on the rocket cannot be reproduced from this repository.

## What the firmware must provide

Based on the report and the ground-station parser, a replacement firmware should:

1. Initialize the MPU6050, BMP280 and ATGM336H over I2C/UART and sample them at a
   fixed rate.
2. Estimate roll and pitch from gravity with `atan2`, and fuse gyro rate with a
   complementary filter that uses an explicit sample period.
3. Emit a framed telemetry packet over the A39C serial modem at 9600 baud.
4. Accept framed uplink commands for parachute, sampling, calibration and
   self-test, with an explicit arming state.
5. Log raw sensor values locally so that attitude estimates can be replayed.

## Recommended frame

The archived ground station used a free-form text stream parsed by a regular
expression. That format has no framing, no length and no integrity check. A
replacement should use the frame described in
`../media/photos/project/telemetry_frame.svg`:

```
0x24 | LEN (1 byte) | PAYLOAD (0..64 bytes) | CRC-16/CCITT-FALSE (2 bytes) | 0x2A
```

The payload should use fixed-width binary fields or tag-length-value records.
The implementation and test vectors are in `../scripts/verify_theory/test_protocol.py`.

## Safety

This repository documents a student sounding-rocket project. It does not contain
propellant formulations, ignition circuits or launch procedures. Any flight
campaign must follow local law and range safety rules and must be supervised by
qualified adults.
