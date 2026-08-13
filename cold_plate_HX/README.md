# Cold-plate heat-exchanger study (paper Sec. 2.2, 3.2)

Helium (50 K, compressible variable-density) versus LN2 (77 K, Boussinesq)
in a channelled cold plate at matched duty (9.4 W) and Reynolds number
(Re = 2300).

- `Buoyancy_50K_Microchannel_Re2300/` — He case (graded production mesh)
- `stage1_microchannel_LN2_77K_Re2300/` — LN2 case (graded production mesh)
- `re-mesh/` — three-grid GCI study (86k / 292k / 984k cells, r = 1.5),
  Celik et al. procedure; `GCI_study/` holds the convergence table and report
- `_DIMENSIONLESS_FRAMEWORK.md` — definitions of every reported group
  (Nu, f, NTU/effectiveness, Mouromtseff, Graetz, entropy generation)
- `gate_check.py` / `compare_remesh.py` — QA gates and the He-vs-LN2
  comparison table generator (`He_vs_N2_comparison_REMESH.csv` in `re-mesh/`)

Each case folder carries `metrics.csv` (full converged metric set),
`egm_lax.csv` (entropy-generation / axial-conduction), `Nu_f_report.txt`,
and `GATE_CHECK.txt`. Case dictionaries (`0/`, `constant/`, `system/`) are
added by `finish_repo.sh` (see repo root) or on request.
