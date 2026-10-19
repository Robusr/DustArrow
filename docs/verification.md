# Verification Record

## Environment

- OS: Windows 11 (build 10.0.26200)
- Python: 3.11 (Windows, 64-bit)
- Dependencies: standard library only for the verification suite
- Date: 2026-10-20

## Commands

```bash
python scripts/verify_theory/run_verification.py
```

The runner discovers `test_*.py` in `scripts/verify_theory/` and prints a
summary. It exits non-zero if any test fails.

## Final result

```
Ran 32 tests in 0.031s

OK

SUMMARY tests=32 failures=0 errors=0 skipped=0
```

| Test file | Tests | Coverage |
|---|---:|---|
| `test_quaternion.py` | 9 | Identity, 90° rotation, composition order, inverse, matrix orthonormality, Euler round-trip, geodesic error, constant-rate integration, renormalization |
| `test_attitude.py` | 9 | Roll in four quadrants, `atan` versus `atan2`, pitch estimate, complementary-filter convergence, bias rejection, fixed-\(k\) sample-rate dependence, yaw observability, thrust corruption |
| `test_protocol.py` | 9 | Archived regex on complete, split and concatenated packets; proposed frame round-trip, byte-by-byte reassembly, noise resync, bad-CRC rejection, two frames per read, CRC known vector |
| `test_geometry.py` | 5 | von Kármán endpoints and monotonicity, 40 mm airframe from STL, power-board outline from Gerber, BOM cost, nine-module summary |

## First run and correction

The first run executed 31 tests and reported one failure:

```
FAIL: test_complementary_filter_bias_offset
AssertionError: 0.24990000000000023 not less than 0.05
```

The test expected a steady-state bias offset of `bias * tau`. For the discrete
update implemented here, with \(\alpha=\tau/(\tau+\Delta t)\), the actual offset
is `bias * dt^2 / tau`. The test expectation was wrong, not the filter. It was
replaced by:

- `test_complementary_filter_rejects_constant_bias`, which checks the correct
  steady offset, and
- `test_pure_gyro_integration_drifts`, which shows that a raw gyro integrator
  drifts by `bias * t`.

This failure and correction are recorded instead of being hidden. It does not
change any report formula or conclusion.

## Numerical cross-checks

| Check | Input | Result | Test |
|---|---|---|---|
| Roll quadrant | True roll \(150^\circ\) | `atan2` = \(150^\circ\); `atan` = \(-30^\circ\) | `test_atan_loses_quadrant` |
| Pitch | True pitch \(-70^\circ\) to \(70^\circ\) | Error < \(10^{-5}\) deg under stated axes | `test_pitch_estimate` |
| Complementary filter | 20°, \(\Delta t=0.01\) s, \(\tau=0.5\) s | Error < 0.01° after 20 s | `test_complementary_filter_converges_without_bias` |
| Bias rejection | 0.5°/s bias, same filter | Offset ≈ 0.0001° | `test_complementary_filter_rejects_constant_bias` |
| Raw gyro drift | 0.5°/s for 10 s | 5° | `test_pure_gyro_integration_drifts` |
| Yaw observability | Yaw 0° versus 45° | Gravity vector difference < \(10^{-12}\) | `test_yaw_not_observable_from_gravity` |
| Thrust corruption | 20 m/s² axial thrust, level | Pitch estimate ≈ \(-64^\circ\) | `test_thrust_corrupts_accelerometer_angle` |
| Frame fragmentation | Byte-by-byte feed | All bytes reassembled, payload intact | `test_byte_by_byte_reassembly` |
| CRC vector | ASCII `123456789` | `0x29B1` | `test_crc_known_vector` |
| Airframe diameter | Binary STL | \(40.0 \times 125.4 \times 40.0\) mm | `test_airframe_diameter_from_stl` |
| Power board | Gerber outline | \(25.0 \times 25.1\) mm | `test_power_board_outline` |
| BOM known cost | Nine module BOMs | 57 parts, CNY 31.44 known | `test_bom_known_cost` |

## What is not verified

- No flight firmware, so behaviour on the RP2040 is not tested.
- No flight or bench telemetry log, so the attitude error envelope is unknown.
  The January 2024 TV feature documents a flight and partial recovery, but it
  provides no telemetry log or quantitative sensor data. The 80% recovery figure
  is the student’s on-camera estimate, not an independent measurement.
- No link budget or range test, so the kilometre-scale claim is unverified.
- No sensor calibration data, so accelerometer/gyro bias and scale factors are
  not quantified.
- No real-time GUI test; the archived PyQt application requires PyQt5 and a
  serial adapter, and its plots are placeholders.

These gaps are also listed in `docs/errata.md` and in the README roadmap.
