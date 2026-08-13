# re-mesh — mesh-independence (GCI) study & grid-converged cold-plate models

This folder documents the **grid-convergence (GCI) study** that drove the cold-plate
heat-exchanger models from an under-resolved uniform mesh to a grid-converged, near-wall-graded
mesh. The **grid-converged models are now the canonical ones** in the parent folder
(`../Buoyancy_50K_Microchannel_Re2300` = He, `../stage1_microchannel_LN2_77K_Re2300` = LN2) —
they have **replaced** the old uniform-mesh versions to avoid old-vs-new confusion.

## Why the re-mesh was needed
A 3-mesh GCI on the original **uniform 43k mesh failed**: Nu grew monotonically with refinement
(7.9 → 11.6 → 16.8) with apparent order p≈0.5 and GCI≈160% — nowhere near grid-independent.
Root cause: only 6–8 *uniform* cells across the duct, so the thermal/velocity boundary layers
(especially the thin high-Pr LN2 thermal layer) were unresolved.

## What was done
Rebuilt with **two-sided `simpleGrading` (expansion 6)** clustering cells at all four no-slip
walls. 3-mesh GCI at r=1.5 (Celik 2008), see `GCI_study/`:

| mesh | cells | Nu | f (Darcy) |
|---|---|---|---|
| coarse | 86,400 | 33.6 | 0.111 |
| medium (production) | 291,600 | 33.0 | 0.116 |
| fine | 984,150 | 31.9 | 0.121 |

- **Nu is grid-converged**: apparent order p=1.63, Richardson-extrapolated ≈30.6,
  medium-mesh GCI 2.4% / fine 4.8%.
- **f is not fully converged**: GCI ≈17% (still rising) — locking f<3% needs ~2–5M cells,
  beyond the current VM (we hit 100% disk at 984k). f is reported with this uncertainty band.

## Headline impact
The original uniform mesh **under-resolved the load badly**: grid-converged **Nu ≈ 31 (vs 11.7, ~3×)**
and **f ≈ 0.13 (vs 0.067, ~2×)**. The under-resolution hit the high-Pr LN2 case hardest, so it had
*understated* nitrogen's advantage. On the grid-converged mesh LN2 beats He by **~18× in h**
(was 8.4×), with **~40× less exergy destruction** — nitrogen's superiority is even clearer.

## Contents
- `GCI_study/` — `GCI_report_LN2.txt` (Celik GCI on Nu, f, h), `gci_convergence.csv`.
- `He_vs_N2_comparison_REMESH.{txt,csv}` — grid-converged head-to-head (also copied to the parent
  folder). Includes Re, Nu, f, h, NTU/ε, Mouromtseff, Graetz L_t/L, axial-conduction λ_ax, and
  EGM/entropy (Ṡ_thermal, Ṡ_viscous, Bejan irreversibility, exergy destruction).
- `compare_remesh.py`, `gate_check.py`, `gci_compute.py` — reproducible post-processing/QA.

## Related
- Cooling-requirement (HX duty) lock: `../../Cascade_GCI_cooling_requirement/ASSESSMENT.md`.
- Canonical grid-converged models + per-case READMEs: the two parent model folders.

## Honest caveats
1. f carries a ~17% GCI uncertainty (VM-limited); Nu is converged (~5%).
2. High-aspect graded cells leave a p_rgh residual floor (energy balance ~2–5%); solutions are
   steady (TWall to <1e-4) but not as tight as a uniform mesh.
3. LN2 Nu/Nu∞≈9 is high vs simple thermal-Graetz; attributable to Gz=181 + Pr=2.36 + one-wall
   heating + the global-Nu definition (worth a correlation cross-check for publication).
