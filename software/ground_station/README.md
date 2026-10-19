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
- The OpenGL attitude widget is constructed but commented out; the archived UI
  path does not render live attitude.
- There is no timestamped logger, checksum, frame parser or command uplink.
- `data.txt` is overwritten on every received frame.

## Run

```bash
python -m pip install -r requirements.txt
python appMain.py
```

The app expects a serial adapter on the port selected in the drop-down list. It
uses the text protocol emitted by the archived flight firmware, which is not
included in this repository.

## Known defects

- `data.txt` is a runtime file and is ignored by Git.
- The legacy UI generates the attitude cube only when its (commented-out) widget
  is enabled and is clicked.
- Only roll and pitch are parsed, so the display cannot represent full 3D
  attitude or heading.
