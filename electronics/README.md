# Electronics

## Source

- `source/easyeda_legacy/` — an EasyEDA board JSON from 2023-05-02. It belongs to
  the earlier DustArrow board, not to every DustArrow X module. No complete
  native EasyEDA project for the X boards was found in the archive.

## Output

- `output/bom/` — nine module BOMs, exported 2023-08-15 and normalized to English
  filenames.
- `output/gerber/` — ten Gerber archives. `co_sensor_hat_gerber.zip` has no
  matching BOM.
- `output/silkscreen/` — module artwork and logos.
- `output/pcb_3d/` — legacy OBJ/MTL board model.
- `output/legacy/` — earlier BOM, Gerber and pick-and-place files.

## Datasheets

`datasheets/` holds manufacturer datasheets and connector drawings collected
during the design. They are third-party documents and are not relicensed under
MIT.

## Measured outlines

The Gerber outline layer gives 30 × 40 mm for Command A, 32 × 101 mm for Data,
32 × 76 mm for Exploration, 25.0 × 25.1 mm for Power and 25 × 25.9 mm for
ServoHAT. Other boards were not measured. Board dimensions are checked in
`../scripts/verify_theory/test_geometry.py`.
