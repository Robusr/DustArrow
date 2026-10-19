#!/usr/bin/env python3
"""Build a Windows one-folder release of the DustArrow ground station.

Run from any directory:

    python scripts/build_ground_station.py

The script writes build intermediates to build/ground_station, the executable
folder to dist/DustArrowGroundMonitor and the zip plus SHA-256 file to release/.
"""

import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path


VERSION = "0.1.0"
NAME = "DustArrowGroundMonitor"
ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "software" / "ground_station"
BUILD = ROOT / "build" / "ground_station"
DIST = ROOT / "dist"
RELEASE = ROOT / "release"


def require(module):
    if importlib.util.find_spec(module) is None:
        raise SystemExit(
            "Missing dependency %s. Install it with:\n"
            "  python -m pip install -r software/ground_station/requirements.txt pyinstaller"
            % module
        )


def readme_text():
    return """DustArrow Ground Station %s
================================

Run DustArrowGroundMonitor.exe.

1. Connect the USB serial receiver.
2. Select the COM port in the application.
3. Open the port at 9600 baud, 8-N-1.
4. Start the stream.

The application parses X, Y, GX, GY, GZ fields and writes data.txt next to the
executable. See the repository documentation for the protocol and the
implemented data path.

License: MIT for the application source and documentation. Third-party
datasheets, programme stills and the contest logo are excluded.
""" % VERSION


def main():
    for module in ["PyInstaller", "PyQt5", "matplotlib", "numpy", "serial", "OpenGL"]:
        require(module)

    BUILD.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    RELEASE.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        NAME,
        "--icon",
        str(APP / "QtApp" / "images" / "rocket.ico"),
        "--add-data",
        str(APP / "QtApp" / "images") + os.pathsep + "QtApp/images",
        "--hidden-import",
        "serial.tools.list_ports",
        "--hidden-import",
        "PyQt5.QtOpenGL",
        "--hidden-import",
        "matplotlib.backends.backend_qt5agg",
        "--collect-submodules",
        "OpenGL",
        "--collect-submodules",
        "serial",
        "--distpath",
        str(DIST),
        "--workpath",
        str(BUILD),
        "--specpath",
        str(BUILD),
        "appMain.py",
    ]

    print("Running:", " ".join(command))
    subprocess.run(command, cwd=str(APP), check=True)

    bundle = DIST / NAME
    if not (bundle / (NAME + ".exe")).exists():
        raise SystemExit("Build did not produce %s.exe" % (bundle / NAME))

    (bundle / "README.txt").write_text(readme_text(), encoding="utf-8", newline="\r\n")
    shutil.copy2(ROOT / "LICENSE", bundle / "LICENSE")

    archive_base = RELEASE / ("%s-v%s-win64" % (NAME, VERSION))
    archive_path = Path(shutil.make_archive(str(archive_base), "zip", root_dir=str(DIST), base_dir=NAME))

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path = archive_path.with_suffix(archive_path.suffix + ".sha256")
    checksum_path.write_text("%s  %s\n" % (digest, archive_path.name), encoding="utf-8")

    print("ARTIFACT", archive_path)
    print("SIZE_MB", round(archive_path.stat().st_size / 1024 / 1024, 2))
    print("SHA256", digest)


if __name__ == "__main__":
    main()
