# Migration Notes

## Source

- Original folder: `F:\Desktop\DustArrow X` (490 MB, unchanged).
- Target repository: `F:\Desktop\dev\DustArrow`, branch `chore/repo-organization`.
- The original folder was never modified, moved or deleted.

## Top-level mapping

| Original path | New path | Notes |
|---|---|---|
| `图纸/正式/` | `mechanical/source/formal/` | Internal Chinese folder and part names preserved for SolidWorks references |
| `图纸/正式/理想化模型/` | `simulation/cfd/` | CFD project, `.fld`, `.fbd`, `.cpt`, animations and logs |
| `图纸/正式/3D打印/打印文件/` | `mechanical/output/3dp/` | STL exports renamed to English snake_case |
| `图纸/正式/装配/整体装配.STEP` | `mechanical/output/step/overall_assembly.step` | Exported assembly |
| `图纸/初稿/` | `mechanical/source/draft/` | Early concepts, including the image bay and four-channel canard study |
| `图纸/发射修改/` | `mechanical/source/launch_revision/` | Pre-launch changes |
| `录制补印/STL/` | `mechanical/output/reprint/` | 15 reprint STLs renamed with a mapping CSV |
| `录制补印/模型/` | `mechanical/source/reprint_models/` | 8 revised SolidWorks parts |
| `电子/BOM/` | `electronics/output/bom/` | Nine module BOMs, renamed |
| `电子/PCB_Gerber/` | `electronics/output/gerber/` | Ten Gerber archives, renamed |
| `电子/丝印图标/` | `electronics/output/silkscreen/` | Silkscreen artwork, renamed |
| `资料/电子元件资料/` | `electronics/datasheets/` | Manufacturer datasheets, renamed |
| `DustArrow Beta/资料素材/PCB_PCB_DustArrow_2023-05-02.json` | `electronics/source/easyeda_legacy/` | Legacy EasyEDA board JSON |
| `DustArrow Beta/资料素材/OBJ_PCB_DustArrow_2023-05-02/` | `electronics/output/pcb_3d/` | Legacy PCB 3D export |
| `DustArrow Beta/资料素材/BOM_*.csv` | `electronics/output/legacy/bom/` | Earlier-generation BOMs |
| `DustArrow Beta/资料素材/Gerber_*.zip` | `electronics/output/legacy/gerber/` | Earlier-generation Gerbers |
| `DustArrow Beta/资料素材/PickAndPlace_*.csv` | `electronics/output/legacy/pick_and_place/` | Earlier-generation placement files |
| `DustArrow Beta/DustArrow_Ground_Monitor/*.py`, `*.ui`, `*.bat` | `software/ground_station/` | Active DustArrow X prototype |
| `DustArrow Beta/DustArrow_Ground_Monitor/QtApp/` | `software/ground_station/QtApp/` and `docs/archive/software_legacy/qt_scaffold/` | Images and Qt resource file kept with the app; empty C++ scaffold archived |
| `DustArrow Beta/DustArrow_Ground_Monitor/Theta_Air_Beta/` | `docs/archive/software_legacy/Theta_Air_Beta/` | Source only; build/dist removed |
| `DustArrow Beta/DustArrow_Ground_Monitor/Theta_Ground_V1.0 （参赛）/` | `docs/archive/software_legacy/Theta_Ground_V1.0 （参赛）/` | Source only; build/dist removed |
| `沙尘利“箭”.pdf`, `.docx` | `docs/archive/report/` | Original report, unchanged |
| `答辩/答辩.pptx` | `docs/archive/presentation/` | Original presentation, unchanged |
| `展板/展板文字.docx` | `docs/archive/display_board/` | Original display-board text |
| `渲染图/` | `media/photos/project/` | Renamed renders |
| `演示图片/` | `media/photos/project/cad_renders/` | 26 CAD/PCB screenshots, numbered `cad_render_01..26` |
| `CFD演示.mp4`, `动画 1.avi` | `media/videos/` | Original CFD videos |
| `QQ录屏20230720063132.mp4` | `media/videos/canard_parachute_animation.mp4` | Canard and parachute animation |
| `沙尘利“箭”.docx` embedded images | `media/photos/reference/` | 20 report figures and equations extracted |
| `资料/冯卡门曲线.txt` | `docs/references/von_karman_formula.txt` | One-line profile formula |

## Renaming rules

- Top-level directories, documentation and output files use English `snake_case`.
- Mechanical source files and their internal directories keep their original
  Chinese names. SolidWorks assemblies reference part filenames and relative
  paths; renaming them would break the assemblies. This is a documented
  exception to the naming rule.
- STL outputs were renamed because they are stand-alone manufacturing files.
  The mapping is stored next to them in `part_name_mapping.csv`.
- Electronics outputs were renamed with an explicit mapping in this document and
  in `BOM/README.md`.

## Excluded from Git

| Path | Reason | Size |
|---|---|---|
| `Theta_Ground_V1.0 （参赛）/build/` | PyInstaller intermediate output | about 45 MB |
| `Theta_Ground_V1.0 （参赛）/dist/` | PyInstaller bundle | about 203 MB |
| `**/__pycache__/`, `*.pyc` | Python cache | small |
| `data.txt` | Empty runtime file | 0 B |
| `~$*.SLDPRT`, `~$*.SLDASM` | SolidWorks lock files | 75 files |
| `答辩.zip` | Duplicate of `答辩/` | 23 MB |
| `答辩/WeChat_20230821040001.mp4` | Defense recording, not a project demo | 10.6 MB |
| `DustArrow Beta/模型/` | Duplicate of formal CAD parts | 7.9 MB |
| `DustArrow Beta/资料素材/` duplicates | Duplicates of electronics outputs | small |

All excluded files remain in the original source folder.

## Missing material

- No flight firmware source, `.uf2`, `.hex` or `.bin` was found.
- No flight-test log, telemetry log or sensor calibration record was found. The
  January 2024 TV feature documents a test flight and partial recovery, but not a
  telemetry log.
- No current price quotes or supplier links were found; BOM prices are historical.
- The report says BMP-180, while the BOM uses GY-BMP280. This is recorded in
  `docs/errata.md` as `[待确认]`.
- The report says the RP2040 is soldered as an SMT footprint, while the BOM
  lists a Raspberry Pi Pico module on the Exploration board. Recorded as
  `[待确认]`.

## Reference updates

- `appMain.py` icon path changed from the missing `UAV.ico` to the bundled
  `rocket.ico`.
- Unused `pandas`, `xlwings` and `math` imports were removed.
- `matplotlib.use("Qt5Agg")` moved before `pyplot` import.
- `uic.bat` now generates `ui_MainWindow.py` from the local `mainwindow.ui` and
  `res_rc.py` from `QtApp/res.qrc`.
- No behaviour of the archived GUI was otherwise changed.

## External material added after reorganization

The Shanghai TV feature `F:\Desktop\Robusr\《少年爱迪生》郭沫晗.mp4` was analyzed
but the full video was not copied into the repository. Five stills and two short
GIF excerpts are committed under `media/photos/project/tv_*`. They are a
third-party production; metadata, SHA-256, rights and a fact-check are in
`docs/*/media_coverage.md`. The full transcript is not committed.
