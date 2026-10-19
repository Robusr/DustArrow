# Changelog

All notable changes to this repository are documented here. The project follows
Keep a Changelog and Semantic Versioning.

## [Unreleased]

### Added

- Media-coverage documentation in English, Chinese and French, including the
  January 2024 *Young Edison* feature, video fingerprint and a fact-check table.
- Errata item E-16 on the TV-documented test flight and its limits.
- External TV feature metadata in `media/README.md`; the full video is not
  redistributed.
- Five TV stills and two six-second GIF excerpts in `media/photos/project/`,
  embedded in all three READMEs with captions and rights notes.

### Changed

- README name origin now explains that X means infinite possibilities.
- The flight-test specification now records the TV-documented partial recovery.
- The three READMEs were rewritten and synchronized; provisional, pending-update
  and known-issue wording was replaced by definitive project, verification and
  media-coverage sections.
- Architecture-diagram labels now describe the system rather than implementation
  status.

## [0.1.0] - 2026-10-20

### Added

- Organized repository structure for mechanical CAD, electronics outputs,
  software, documentation and media.
- Consolidated BOM across nine PCB modules, with a known-cost summary.
- Theory errata for accelerometer attitude estimation, complementary filtering,
  telemetry framing and documentation inconsistencies.
- Pure-Python verification suite for quaternions, attitude formulas, frame
  parsing, the von Kármán profile and measured geometry.
- Two GIF demonstrations with poster frames, report figures and project renders.
- English, Chinese and French READMEs and long-form documents.
- Migration notes, license, contribution guide and GitHub templates.

### Changed

- Ground-station icon path now points to the bundled `rocket.ico`.
- Unused `pandas`, `xlwings` and `math` imports were removed from the GUI.
- Matplotlib backend selection now happens before `pyplot` is imported.
- Electronics and STL output filenames were normalized to English snake_case;
  original Chinese names are recorded in `MIGRATION_NOTES.md`.

### Excluded

- PyInstaller build outputs, `__pycache__`, SolidWorks lock files and duplicate
  copies. Original files remain in the source archive.
