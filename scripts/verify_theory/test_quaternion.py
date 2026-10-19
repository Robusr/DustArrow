import math
import unittest

from quaternion import (
    conjugate,
    from_euler_zyx,
    geodesic_error,
    integrate_body_rate,
    multiply,
    normalize,
    rotate,
    to_euler_zyx,
    to_matrix,
)


class QuaternionTests(unittest.TestCase):
    def test_identity_rotation(self):
        q = (1.0, 0.0, 0.0, 0.0)
        self.assertEqual(rotate(q, (1.0, 2.0, 3.0)), (1.0, 2.0, 3.0))

    def test_90deg_rotation_about_x(self):
        q = from_euler_zyx(math.pi / 2, 0.0, 0.0)
        x, y, z = rotate(q, (0.0, 1.0, 0.0))
        self.assertAlmostEqual(x, 0.0, places=12)
        self.assertAlmostEqual(y, 0.0, places=12)
        self.assertAlmostEqual(z, 1.0, places=12)

    def test_composition_order(self):
        qz = from_euler_zyx(0.0, 0.0, math.pi / 2)
        qx = from_euler_zyx(math.pi / 2, 0.0, 0.0)
        q = multiply(qz, qx)
        # First rotate about x: y -> z, then about z: z stays z.
        v = rotate(q, (0.0, 1.0, 0.0))
        for got, want in zip(v, (0.0, 0.0, 1.0)):
            self.assertAlmostEqual(got, want, places=12)

    def test_inverse_is_conjugate(self):
        q = normalize((0.7, -0.2, 0.4, 0.5))
        identity = multiply(q, conjugate(q))
        for got, want in zip(identity, (1.0, 0.0, 0.0, 0.0)):
            self.assertAlmostEqual(got, want, places=12)

    def test_rotation_matrix_is_orthonormal(self):
        q = from_euler_zyx(0.3, -0.5, 1.1)
        m = to_matrix(q)
        for i in range(3):
            for j in range(3):
                dot = sum(m[i][k] * m[j][k] for k in range(3))
                self.assertAlmostEqual(dot, 1.0 if i == j else 0.0, places=12)
        det = (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )
        self.assertAlmostEqual(det, 1.0, places=12)

    def test_euler_roundtrip(self):
        for angles in [
            (0.0, 0.0, 0.0),
            (0.3, -0.4, 0.5),
            (-1.2, 0.8, -2.0),
            (math.pi / 3, math.pi / 6, -math.pi / 4),
        ]:
            q = from_euler_zyx(*angles)
            got = to_euler_zyx(q)
            for a, b in zip(got, angles):
                self.assertAlmostEqual(a, b, places=10)

    def test_geodesic_error_handles_sign(self):
        q = from_euler_zyx(0.2, 0.1, -0.3)
        q_neg = tuple(-c for c in q)
        self.assertAlmostEqual(geodesic_error(q, q_neg), 0.0, places=12)
        q90 = from_euler_zyx(0.0, 0.0, math.pi / 2)
        self.assertAlmostEqual(geodesic_error((1, 0, 0, 0), q90), math.pi / 2, places=10)

    def test_constant_rate_integration(self):
        q = (1.0, 0.0, 0.0, 0.0)
        omega = (0.0, 0.0, math.pi / 2)
        for _ in range(1000):
            q = integrate_body_rate(q, omega, 0.001)
        expected = from_euler_zyx(0.0, 0.0, math.pi / 2)
        # First-order Euler integration; 0.1 degree tolerance is expected.
        self.assertLess(geodesic_error(q, expected), 0.002)
        self.assertAlmostEqual(sum(c * c for c in q), 1.0, places=12)

    def test_renormalization_after_many_steps(self):
        q = normalize((0.9, 0.1, -0.2, 0.3))
        for _ in range(10000):
            q = integrate_body_rate(q, (0.1, -0.2, 0.3), 0.001)
        self.assertAlmostEqual(sum(c * c for c in q), 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
