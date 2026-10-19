import csv
import math
import re
import struct
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def von_karman(x, length, radius):
    if x < 0 or x > length:
        raise ValueError("x must lie in [0, L]")
    theta = math.acos(1.0 - 2.0 * x / length)
    return radius / math.sqrt(math.pi) * math.sqrt(theta - math.sin(2.0 * theta) / 2.0)


def stl_bounds(path):
    data = path.read_bytes()
    count = (len(data) - 84) // 50
    if 84 + count * 50 != len(data):
        raise ValueError("not a binary STL: %s" % path)
    xs, ys, zs = [], [], []
    for i in range(count):
        offset = 84 + i * 50
        values = struct.unpack("<12f", data[offset : offset + 48])
        for j in range(3):
            xs.append(values[3 + j * 3])
            ys.append(values[4 + j * 3])
            zs.append(values[5 + j * 3])
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))


def gerber_outline_mm(zip_path):
    with zipfile.ZipFile(zip_path) as archive:
        name = next(n for n in archive.namelist() if "GKO" in n or "Outline" in n)
        text = archive.read(name).decode("utf-8", "replace")
    unit = "IN" if "%MOIN" in text else "MM"
    match = re.search(r"%FSLAX(\d)(\d)Y", text)
    if not match:
        raise ValueError("cannot find Gerber format specification")
    decimals = int(match.group(2))
    xs, ys = [], []
    for point in re.finditer(r"X(-?\d+)Y(-?\d+)", text):
        xs.append(int(point.group(1)))
        ys.append(int(point.group(2)))
    scale = 25.4 if unit == "IN" else 1.0
    return (
        (max(xs) - min(xs)) / (10 ** decimals) * scale,
        (max(ys) - min(ys)) / (10 ** decimals) * scale,
    )


class GeometryTests(unittest.TestCase):
    def test_von_karman_endpoints_and_monotonicity(self):
        length, radius = 162.0, 20.0
        self.assertAlmostEqual(von_karman(0.0, length, radius), 0.0, places=9)
        self.assertAlmostEqual(von_karman(length, length, radius), radius, places=9)
        previous = -1.0
        for i in range(1001):
            y = von_karman(length * i / 1000.0, length, radius)
            self.assertTrue(math.isfinite(y))
            self.assertGreaterEqual(y, previous - 1e-12)
            previous = y

    def test_airframe_diameter_from_stl(self):
        path = ROOT / "mechanical/output/3dp/telemetry_module_body.stl"
        dx, dy, dz = stl_bounds(path)
        self.assertAlmostEqual(max(dx, dz), 40.0, delta=0.6)
        self.assertGreater(dy, 100.0)

    def test_power_board_outline(self):
        width, height = gerber_outline_mm(
            ROOT / "electronics/output/gerber/power_gerber.zip"
        )
        self.assertAlmostEqual(width, 25.0, delta=0.5)
        self.assertAlmostEqual(height, 25.1, delta=0.5)

    def test_bom_known_cost(self):
        total = 0.0
        with (ROOT / "BOM/bill_of_materials.csv").open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row["line_total_cny"]:
                    total += float(row["line_total_cny"])
        self.assertAlmostEqual(total, 31.44, delta=0.01)

    def test_nine_modules_in_bom_summary(self):
        with (ROOT / "BOM/bom_summary.csv").open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 9)
        self.assertEqual(sum(int(r["total_parts"]) for r in rows), 57)


if __name__ == "__main__":
    unittest.main()
