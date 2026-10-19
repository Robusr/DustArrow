import math
import unittest

from quaternion import conjugate, from_euler_zyx, rotate


G = 9.80665


def gravity_body(roll, pitch, yaw=0.0, thrust=0.0):
    """Accelerometer reading for z-up gravity plus axial thrust."""
    q = from_euler_zyx(roll, pitch, yaw)
    g_body = rotate(conjugate(q), (0.0, 0.0, G))
    return (g_body[0] + thrust, g_body[1], g_body[2])


def roll_atan2(a):
    return math.degrees(math.atan2(a[1], a[2]))


def roll_atan(a):
    return math.degrees(math.atan(a[1] / a[2]))


def pitch_atan2(a):
    return math.degrees(math.atan2(-a[0], math.sqrt(a[1] ** 2 + a[2] ** 2)))


def complementary_filter(accel_deg, gyro_dps, dt, tau, steps, bias_dps=0.0):
    angle = 0.0
    k = tau / (tau + dt)
    for _ in range(steps):
        predicted = angle + (gyro_dps + bias_dps) * dt
        angle = k * accel_deg + (1.0 - k) * predicted
    return angle


class AttitudeTests(unittest.TestCase):
    def test_roll_atan2_all_quadrants(self):
        for deg in [0.0, 30.0, 90.0, 150.0, -150.0]:
            a = gravity_body(math.radians(deg), 0.0)
            self.assertAlmostEqual(roll_atan2(a), deg, places=5)

    def test_atan_loses_quadrant(self):
        a = gravity_body(math.radians(150.0), 0.0)
        self.assertAlmostEqual(roll_atan2(a), 150.0, places=5)
        self.assertAlmostEqual(roll_atan(a), -30.0, places=5)
        self.assertGreater(abs(roll_atan(a) - 150.0), 100.0)

    def test_pitch_estimate(self):
        for deg in [-70.0, -20.0, 0.0, 25.0, 70.0]:
            a = gravity_body(0.0, math.radians(deg))
            self.assertAlmostEqual(pitch_atan2(a), deg, places=5)

    def test_complementary_filter_converges_without_bias(self):
        angle = complementary_filter(20.0, 0.0, 0.01, 0.5, 2000)
        self.assertLess(abs(angle - 20.0), 0.01)

    def test_complementary_filter_rejects_constant_bias(self):
        # With k = tau/(tau+dt), the steady offset is bias*dt^2/tau.
        angle = complementary_filter(20.0, 0.0, 0.01, 0.5, 5000, bias_dps=0.5)
        expected_offset = 0.5 * 0.01 ** 2 / 0.5
        self.assertLess(abs(angle - 20.0 - expected_offset), 0.001)

    def test_pure_gyro_integration_drifts(self):
        bias = 0.5
        drift = sum(bias * 0.01 for _ in range(1000))
        self.assertGreater(abs(drift), 4.9)

    def test_fixed_k_depends_on_sample_rate(self):
        tau = 0.5
        k_fast = tau / (tau + 0.005)
        k_slow = tau / (tau + 0.05)
        self.assertGreater(k_fast - k_slow, 0.05)

    def test_yaw_not_observable_from_gravity(self):
        a0 = gravity_body(0.2, -0.1, yaw=0.0)
        a1 = gravity_body(0.2, -0.1, yaw=math.radians(45.0))
        for x, y in zip(a0, a1):
            self.assertAlmostEqual(x, y, places=12)

    def test_thrust_corrupts_accelerometer_angle(self):
        a = gravity_body(0.0, 0.0, thrust=20.0)
        error = abs(pitch_atan2(a) - 0.0)
        self.assertGreater(error, 30.0)


if __name__ == "__main__":
    unittest.main()
