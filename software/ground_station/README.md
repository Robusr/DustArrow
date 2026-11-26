# DustArrow X Ground Station

Archived PyQt5 telemetry dashboard. This is a **UI prototype**, not a validated
flight console.

## What works in the archived code

- Serial-port enumeration and open/close at 9600 baud, 8-N-1.
- A regular expression extracts `X...Y...GX...GY...GZ...` fields from incoming
  text and writes `X...Y...` to `data.txt`.
- Six Matplotlib canvases and a start/stop control exist in the window.

## What is not implemented

- The six plots show the placeholder curve `y = x^2`; they are not updated from
  serial data.
- The command buttons (emergency parachute, coordinate request, high-altitude
  sampling, attitude calibration, data refresh, self-test) are not connected.
- The OpenGL widget is constructed and draws a static cube; the archived UI has
  no live attitude update.
- There is no timestamped logger, checksum, frame parser or command uplink.
- `data.txt` is overwritten on every received frame.

## Run

```bash
python -m pip install -r requirements.txt
python appMain.py
```

The app expects a serial adapter on the port selected in the drop-down list. It
uses the text protocol emitted by the archived flight firmware, which is not
included in this repository. The archived code calls `ctypes.windll` at import,
so it is Windows-only and does not start on macOS or Linux.

## Known defects

- `data.txt` is a runtime file and is ignored by Git.
- The OpenGL widget is constructed by the generated UI and draws a static cube.
  Its live `paintCube` update is commented out; a mouse click reads `data.txt`
  and rotates the cube.
- A serial chunk that does not match `X...Y...GX...GY...GZ...` can raise
  `AttributeError` in `DATA()` before `self.Gyrox` is assigned.
- Only roll and pitch are parsed, so the display cannot represent full 3D
  attitude or heading.
