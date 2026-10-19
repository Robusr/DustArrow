# Contributing

## Scope

This repository documents a student sounding-rocket project. Contributions that
improve reproducibility, documentation, analysis or the ground-station prototype
are welcome. Do not add propellant formulations, ignition procedures or launch
instructions.

## Workflow

1. Open an issue describing the change.
2. Create a branch from `main`, for example `feat/framed-protocol`.
3. Keep binary CAD and media changes separate from source changes.
4. Run the verification suite and repository checks before opening a pull
   request:

```bash
python scripts/verify_theory/run_verification.py
python scripts/validate_repo.py
```

5. Use Conventional Commits, for example `fix(protocol): reject bad CRC`.

## Data and media rules

- Do not fabricate measurements, flight data or citations.
- Label every number as measured, simulated, a design target or a literature
  value.
- Do not commit build outputs, `__pycache__`, `data.txt` or CAD lock files.
- Third-party datasheets and logos must not be relicensed under MIT. Record the
  source and authorization status in `docs/references/README.md`.
- GIFs must be under 10 MB, loop, and have a poster image.

## Language

The English README is the source of truth. When a change affects a documented
fact, update `README.md`, `README.zh-CN.md` and `README.fr.md` in the same pull
request.

## Code style

- Python 3.11, standard library preferred for verification scripts.
- Keep the archived GUI behavior unchanged unless a fix is documented in
  `CHANGELOG.md`.
- New public functions need tests under `scripts/verify_theory/`.
