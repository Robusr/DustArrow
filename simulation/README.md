# Simulation

`cfd/` contains the idealised-model study copied from
`图纸/正式/理想化模型/`:

- Three SolidWorks idealised models: X60 Y60, X60 Y90 and X90 Y90.
- Two solver cases, `1/` and `2/`, with `.fld`, `.fbd`, `.cpt`, `.geom`, `.gdb`
  and `.stdout` solver output. Transient logs and `.bak` files remain in the
  source archive and are not tracked.
- Two short AVI renders of the flow field.

The archive does not contain a solver project description, mesh-convergence
study, boundary-condition table or validation against experiment. The case names
suggest geometric variants; this repository does not infer their exact meaning.
Treat the output as a qualitative demonstration, not a validated CFD result.

The animation `动画 1.avi` from the same study is also stored in
`../media/videos/cfd_demo_alt.avi`.
