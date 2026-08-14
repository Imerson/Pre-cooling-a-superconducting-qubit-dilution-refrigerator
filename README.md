# Pre-cooling a superconducting-qubit dilution refrigerator

Support material for:

> I. Joao, *Pre-cooling a superconducting-qubit dilution refrigerator:
> cascade heat-budget penalty and helium-versus-nitrogen cold-plate coolant
> selection by CFD*, submitted to **Cryogenics** (2026).

This repository contains the OpenFOAM case definitions, calibration and
post-processing scripts, and figure-generation code needed to reproduce the
results of the paper. Solution fields and meshes are **not** stored; every
mesh is regenerated from the dictionaries and scripts provided.

## Requirements

- OpenFOAM **v2412** (OpenCFD/ESI line) — `chtMultiRegionSimpleFoam`,
  `buoyantBoussinesqSimpleFoam`, `blockMesh`, `snappyHexMesh`
- Python 3.10+ with `numpy`, `pandas`, `matplotlib` (for the extraction and
  figure scripts)
- ParaView 5.x (optional, for field visualisation)

## Repository layout

```
paper/                         The manuscript and Supplementary Information
  precooling_paper.pdf
  precooling_supplementary_v2.pdf

enclosure_CHT/                 Passive study: multi-region conjugate heat
                               transfer of the cryostat enclosure (Sec. 2.1)
  stage1_shield_50K_v2/        Stage 1, 300 K -> 50 K helium-route shield
  stage1_shield_77K_v2/        Stage 1, 300 K -> 77 K LN2-route shield
  stage2_4K_from50K_v2/        Stage 2, 50 K -> 4 K span
  stage2_4K_from77K_v2/        Stage 2, 77 K -> 4 K span
  cascade_GCI/                 View-factor agglomeration sweep and cascade
                               convergence study
  gate_check_suite/            Closed-form energy-balance audits (SI)

cold_plate_HX/                 Active study: cold-plate heat exchanger,
                               He vs LN2 at matched duty and Re (Sec. 2.2)
  stage1_microchannel_LN2_77K_Re2300/   buoyantBoussinesqSimpleFoam, LN2 at 77 K
  Buoyancy_50K_Microchannel_Re2300/     compressible variable-density, He at 50 K
  re-mesh/                     Three-grid GCI study (Celik et al. procedure)

paper_figures/                 Scripts that generate the paper figures
```

## How to read this repository alongside the paper

The paper is included in [paper/precooling_paper.pdf](paper/precooling_paper.pdf)
(Supplementary Information:
[paper/precooling_supplementary_v2.pdf](paper/precooling_supplementary_v2.pdf)).
Each part of the paper maps onto a folder here:

| Paper | What it describes | Where in this repo |
|---|---|---|
| Sec. 2.1, enclosure CHT model + domain figure | Multi-region enclosure geometry, BCs, solver setup | [enclosure_CHT/](enclosure_CHT/) — start with [README_master.md](enclosure_CHT/README_master.md) |
| Sec. 2.1, radiation view-factor sweep figure | Agglomeration-level convergence of the Stage-1 radiative load | [enclosure_CHT/cascade_GCI/](enclosure_CHT/cascade_GCI/) |
| Sec. 2.2, cold-plate HX model + three-grid GCI figure | Microchannel geometry, matched-duty/Re method, mesh independence | [cold_plate_HX/](cold_plate_HX/) — method notes in [_DIMENSIONLESS_FRAMEWORK.md](cold_plate_HX/_DIMENSIONLESS_FRAMEWORK.md), GCI in [re-mesh/](cold_plate_HX/re-mesh/) |
| Sec. 3.1, stage heat loads + mechanism decomposition figures | The four enclosure cases behind the cascade heat budget | [enclosure_CHT/stage1_shield_50K_v2/](enclosure_CHT/stage1_shield_50K_v2/), [stage1_shield_77K_v2/](enclosure_CHT/stage1_shield_77K_v2/), [stage2_4K_from50K_v2/](enclosure_CHT/stage2_4K_from50K_v2/), [stage2_4K_from77K_v2/](enclosure_CHT/stage2_4K_from77K_v2/) — each keeps its converged `postProcessing/` output |
| Sec. 3.2, LN2-versus-He verdict figure | The two matched cold-plate cases | [cold_plate_HX/stage1_microchannel_LN2_77K_Re2300/](cold_plate_HX/stage1_microchannel_LN2_77K_Re2300/) and [cold_plate_HX/Buoyancy_50K_Microchannel_Re2300/](cold_plate_HX/Buoyancy_50K_Microchannel_Re2300/) |
| Sec. 3.3, COP wall-power ledger figure | Combining stage loads and Carnot COP into the route comparison | [paper_figures/make_paper_figs.py](paper_figures/make_paper_figs.py) |
| SI, energy-balance gate checks | The ten-gate audit that every reported case passes | [enclosure_CHT/gate_check_suite/](enclosure_CHT/gate_check_suite/) and [cold_plate_HX/gate_check.py](cold_plate_HX/gate_check.py) |

Suggested route for a reader: skim the paper's Sec. 2, open the matching
model folder and its README, check the numbers in that case's
`postProcessing/` output, then regenerate the figures from
[paper_figures/](paper_figures/).

Each case folder keeps the standard OpenFOAM structure (`0/`, `constant/`,
`system/`) plus:

- `build_pipeline_reference.sh` — mesh generation and region splitting
- `extract_heat_loads.py` / `gate_check.py` — wall-flux extraction and the
  closed-form energy-balance audits described in the paper
- `postProcessing/` — converged wall-flux and residual summaries (text),
  retained so the reported numbers can be checked without re-running

## Reproducing the results

1. Build a case mesh: `cd enclosure_CHT/stage1_shield_50K_v2 &&
   ./build_pipeline_reference.sh`
2. Run the solver: `chtMultiRegionSimpleFoam` (enclosure cases) or the
   solver named in each case README (cold plate).
3. Extract the heat budget: `python3 extract_heat_loads.py`
4. Regenerate the paper figures: `cd paper_figures && python3
   make_paper_figs.py`

Convergence criteria, boundary conditions, and validation anchors are
documented in the paper (Sec. 2) and its Supplementary Information; per-case
details are in each folder's README.

## Data availability and licence

Code and case dictionaries are released under the MIT Licence (see
`LICENSE`). If you use this material, please cite the paper above.

## Contact

Imerson Joao — pemb7049@ox.ac.uk/ifnj2@cantab.ac.uk
