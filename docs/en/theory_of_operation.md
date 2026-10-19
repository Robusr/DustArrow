# Theory of Operation

## Scope

This document explains the attitude and telemetry mathematics used by the
DustArrow X prototype. The original report contains a short derivation; this
text restates it with explicit conventions, identifies its limits and links each
correction to `../errata.md` and `../verification.md`.

## Evidence status

| Item | Status | Source |
|---|---|---|
| 40.0 mm airframe diameter | Measured | STL bounding box, `scripts/verify_theory/test_geometry.py` |
| 25.0 × 25.1 mm power board | Measured | Gerber outline |
| Roll and pitch from gravity | Derived | This document, verified numerically |
| Complementary-filter weights | Report text, incomplete | Original report, section 2 |
| Yaw from MPU6050 alone | Not observable | 6-axis IMU has no magnetometer |
| Kilometre-scale telemetry | Unverified design target | Report claim; no link budget or range test in the archive |
| PID flight control | Not implemented | Report states the algorithm is still exploratory |

## Coordinate convention

The report defines roll as rotation about $x$, pitch about $y$ and yaw about
$z$, but does not state the axis directions or the sensor mounting. The
verification suite uses the following convention:

- Body frame: $x$ forward, $y$ right, $z$ up, right-handed.
- Inertial frame: local level, $z$ up.
- Quaternion $q$ rotates a vector from the body frame to the inertial frame.
- Gravity in the inertial frame is $\mathbf{g}_i = [0, 0, g]^T$, with
  $g = 9.80665\ \mathrm{m/s^2}$.

If the flight board uses another mounting, every sign below must be checked
before flight. This is recorded as `[待确认]` in the errata.

## Static attitude from gravity

For a level, non-accelerating vehicle the accelerometer measures the reaction to
gravity:

$$
\mathbf{a}_b = R(q)^T \mathbf{g}_i .
$$

With roll $\phi$ and pitch $\theta$, the gravity components are

$$
a_x = -g \sin\theta, \qquad
a_y = g \sin\phi \cos\theta, \qquad
a_z = g \cos\phi \cos\theta .
$$

The roll and pitch estimates follow as

$$
\phi = \operatorname{atan2}(a_y, a_z),
$$

$$
\theta = \operatorname{atan2}\!\left(-a_x,\sqrt{a_y^2+a_z^2}\right).
$$

The report writes $\phi = \arctan(a_y/a_z)$. That form loses the quadrant and
is undefined when $a_z = 0$. At $\phi = 150^\circ$ it returns
$-30^\circ$. The errata changes the formula to `atan2`; the numerical test
reproduces the error.

The report also shows an embedded pitch equation of the form
$\sin\theta = a_x/\sqrt{a_y^2+a_z^2}$. This is equivalent to the expression
above only after the axis signs are fixed. It is marked `[待确认]` because the
report does not define the mounting direction.

## Complementary filter

The report gives

$$
\theta_k = k\,\theta_{\mathrm{acc},k} + (1-k)\,\theta_{\mathrm{gyro},k},
\qquad
\theta_{\mathrm{gyro},k} = \theta_{k-1} + \omega_y \Delta t .
$$

This is a first-order complementary filter. The archived text does not state
$\Delta t$, the sample rate, the initial condition or the gyro bias. A
reproducible form uses a time constant $\tau$:

$$
\alpha = \frac{\tau}{\tau+\Delta t},
$$

$$
\theta_k = \alpha\,\theta_{\mathrm{acc},k}
+ (1-\alpha)\left(\theta_{k-1} + \omega_y \Delta t\right).
$$

The filter trusts the accelerometer at low frequency and the gyroscope at high
frequency. It does not make the accelerometer valid during thrust. With
$\alpha = \tau/(\tau+\Delta t)$, a constant gyro bias $b$ produces a small
steady offset $b\,\Delta t^2/\tau$ in this discrete form, while a raw gyro
integrator drifts by $b t$. The verification suite checks both behaviours and
also shows that a fixed $k$ changes the cutoff frequency when $\Delta t$
changes.

## Yaw and the limits of a 6-axis IMU

Gravity carries no heading information. A yaw rotation leaves
$\mathbf{a}_b = [0,0,g]^T$ unchanged, so roll and pitch are observable but yaw
is not. The MPU6050 has no magnetometer. The ground-station cube is therefore a
roll/pitch indicator, not a full 3D attitude display. Any heading estimate needs
a magnetometer, GNSS course over ground, or a known initial yaw with gyro
propagation and drift monitoring.

## Dynamic acceleration

During motor burn the accelerometer measures thrust plus gravity. For a level
vehicle with 20 m/s² axial thrust, the static pitch formula returns about
$-64^\circ$ instead of $0^\circ$. A complementary filter reduces the effect
during short transients but cannot remove a sustained acceleration. No flight
acceleration data is present in the archive, so this error is not quantified for
the real vehicle.

## Telemetry framing

The archived ground station uses the regular expression
`X(.+)Y(.+)GX(.+)GY(.+)GZ(.+)`. It has no header, length or checksum. A packet
split across two serial reads is discarded, and two concatenated packets are
misparsed because `.+` is greedy.

The verified replacement frame is:

```
0x24 | LEN (1 byte) | PAYLOAD (0..64 bytes) | CRC-16/CCITT-FALSE (2 bytes) | 0x2A
```

It resynchronizes on the header, accepts byte-by-byte delivery, rejects a bad
CRC and supports multiple frames per read. The parser and tests are in
`../../scripts/verify_theory/test_protocol.py`. This frame is a recommendation,
not a description of the archived firmware.

## Quaternions

The report does not use quaternions. The reference implementation in
`../../scripts/verify_theory/quaternion.py` fixes the convention used by this
repository:

- Hamilton product.
- Scalar first, $q = [w,x,y,z]$.
- Active rotation from body to inertial.
- Normalization after every integration step.
- Attitude error as the geodesic angle
  $2\arccos(|\langle q_1,q_2\rangle|)$, not a component-wise difference.

These conventions are tested for identity, 90° and 180° rotations, composition
order, inverse, rotation-matrix orthonormality, Euler round-trip, sign
equivalence and constant-rate integration. They are provided as a foundation
for a future full-attitude estimator; they do not claim that the original
firmware used quaternions.

## Verification

Run:

```bash
python scripts/verify_theory/run_verification.py
```

The exact test counts, the one corrected test expectation and the remaining
unverified items are recorded in `../verification.md` and `../errata.md`.
