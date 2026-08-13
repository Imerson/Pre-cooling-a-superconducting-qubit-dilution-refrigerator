# Figure-generation scripts (Cryogenics pre-cooling paper)

`make_paper_figs.py` regenerates Figs. 2-6 of the manuscript from the model
data. Edit the two paths at the top if folders move, then run
`python3 make_paper_figs.py`. Requirements: numpy, pandas, matplotlib.

| Figure | Output file | Data source |
|---|---|---|
| Fig. 2 | `fig2_cascade_loads.png` | `1-CHT models/*/heat_load_comparison_ALL.csv` (production radiation values) |
| Fig. 3 | `fig3_radiation_sweep.png` | `2-Stage 1 Heat exchanger/Cascade_GCI_cooling_requirement/cascade_convergence.csv` |
| Fig. 4 | `fig4_hx_gci.png` | `2-Stage 1 Heat exchanger/re-mesh/GCI_study/gci_convergence.csv` |
| Fig. 5 | `fig5_ln2_he_ratios.png` | `2-Stage 1 Heat exchanger/He_vs_N2_comparison_REMESH.csv` |
| Fig. 6 | `fig6_cop_ledger.png` | stage loads above + Carnot multipliers (Sec. 2.3) |

Fig. 1 (`fig1_domain.png`) is a ParaView export of the enclosure case and is
not generated here; the two `\figstub` placeholders in the manuscript
(enclosure field/flux maps, cold-plate channel fields) are likewise reserved
for ParaView cut views.
