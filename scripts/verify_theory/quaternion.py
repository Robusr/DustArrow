"""Minimal Hamilton quaternion utilities used by the verification suite.

Convention used everywhere in this repository:
    q = (w, x, y, z), scalar first
    Hamilton product
    active rotation from body frame to inertial frame
"""

import math


def normalize(q):
    n = math.sqrt(sum(c * c for c in q))
    if n == 0.0:
        raise ValueError("cannot normalize a zero quaternion")
    return tuple(c / n for c in q)


def multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return (
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    )


def conjugate(q):
    return (q[0], -q[1], -q[2], -q[3])


def rotate(q, v):
    """Rotate vector v from body to inertial using body-to-inertial q."""
    qv = (0.0, v[0], v[1], v[2])
    out = multiply(multiply(q, qv), conjugate(q))
    return (out[1], out[2], out[3])


def to_matrix(q):
    w, x, y, z = normalize(q)
    return [
        [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
    ]


def from_euler_zyx(roll, pitch, yaw):
    """Body-to-inertial rotation, R = Rz(yaw) @ Ry(pitch) @ Rx(roll)."""
    cr, sr = math.cos(roll / 2), math.sin(roll / 2)
    cp, sp = math.cos(pitch / 2), math.sin(pitch / 2)
    cy, sy = math.cos(yaw / 2), math.sin(yaw / 2)
    qx = (cr, sr, 0.0, 0.0)
    qy = (cp, 0.0, sp, 0.0)
    qz = (cy, 0.0, 0.0, sy)
    return normalize(multiply(qz, multiply(qy, qx)))


def to_euler_zyx(q):
    w, x, y, z = normalize(q)
    roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    s = max(-1.0, min(1.0, 2 * (w * y - z * x)))
    pitch = math.asin(s)
    yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return roll, pitch, yaw


def geodesic_error(q1, q2):
    q1 = normalize(q1)
    q2 = normalize(q2)
    dot = abs(sum(a * b for a, b in zip(q1, q2)))
    dot = max(-1.0, min(1.0, dot))
    return 2.0 * math.acos(dot)


def integrate_body_rate(q, omega, dt):
    """Integrate q_dot = 0.5 * q x [0, omega_body] and renormalize."""
    wq = (0.0, omega[0], omega[1], omega[2])
    dq = multiply(q, wq)
    q_new = tuple(q[i] + 0.5 * dq[i] * dt for i in range(4))
    return normalize(q_new)
