# Mechanical

## Source

- `source/draft/` — early concepts, including an image bay and a four-channel
  canard study.
- `source/launch_revision/` — parts revised before the launch attempt.
- `source/formal/` — final SolidWorks parts, sub-assemblies and the overall
  assembly.
- `source/reprint_models/` — eight revised parts prepared for a second print run.

The original Chinese filenames and internal folder names are preserved. The
SolidWorks assemblies resolve parts by filename; renaming them would break the
references. This is a documented exception to the repository naming convention.

## Output

- `output/3dp/` — 27 STL files exported from the formal parts, with a
  `part_name_mapping.csv`.
- `output/reprint/` — 15 reprint STLs, with a mapping CSV.
- `output/step/` — `overall_assembly.step`.

STL files carry no print settings. Material, layer height, infill and orientation
were not recorded in the archive and are not invented here.
