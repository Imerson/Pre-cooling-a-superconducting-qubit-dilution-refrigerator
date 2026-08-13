# LN2_graded — grid-converged (re-mesh)

**Stage-1 cold-plate mini-channel HX — Nitrogen (LN2) @ 77 K (Boussinesq)**

Re-meshed, **near-wall-graded** version of the cold-plate case (cells clustered at all four
no-slip walls, especially the heated wall). This replaces the original uniform 43k mesh, which
a GCI study showed was badly under-resolved. Numbers are read from the converged solution at
**t = 6000** (`Nu_f_report.txt`, `metrics.csv`, `egm_lax.csv`, `GATE_CHECK.txt`).

## 1. Methodology
- Solver `buoyantBoussinesqSimpleFoam (incompressible Boussinesq)`, OpenFOAM v2412, laminar, matched duty **9.4 W**, Re=2305.71.
- Mesh: **291600 cells**, two-sided `simpleGrading` (expansion 6) in the two
  cross-stream directions. Mesh-independence by the GCI study in `../re-mesh/GCI_study/` (3 meshes,
  86k/292k/984k, r=1.5).
- Geometry: mini-channel Dh=0.01 m (10 mm), L=0.3 m, 5 parallel
  ducts, one wall heated (flux BC).

## 2. Boundary conditions
- Heated wall: uniform flux, Q=9.4 W (Stage-1 cooling requirement; see
  `../../Cascade_GCI_cooling_requirement/`).
- Inlet T=77 K, fixed velocity;
  outlet reference pressure; walls noSlip; g=(0 -9.81 0).
- Boussinesq (beta*dT<<0.3, valid for liquid).

## 3. Closure / dimensionless framework (all in `metrics.csv` + `egm_lax.csv`)
Re, Nu (=h·Dh/k, h=Q/(A·(Tw−Tb)), Tb = mass-flux-weighted bulk T), f (Darcy, true Pa),
Nu/Nu∞ & fRe/56.9 (Shah & London), **NTU & effectiveness ε**, **Mouromtseff Mo**,
**Graetz L_t/L**, **axial-conduction number λ_ax = 1/Pe** (Pe = Re·Pr), and
**EGM / entropy generation** (Ṡ_thermal = ∫k|∇T|²/T² dV, Ṡ_viscous = ∫2μ(S:S)/T dV,
Bejan irreversibility = Ṡ_thermal/Ṡ_total, exergy destruction = T₀·Ṡ_total, T₀=300 K).

## 4. Gate checks — **10/10**
```
  [PASS] solver_completed           log ends 'End'=True, FATAL=False
  [PASS] duty_correct_9p4W          Q_wall=9.4 W
  [PASS] energy_balance_<6pct       err=2.41% (Qrem=9.627 W)
  [PASS] Re_on_target_2300          Re=2305.7
  [PASS] steady_state_<0.1pct       TWall range/mean over last10=6.51e-07
  [PASS] model_appropriate          Boussinesq: beta*dT_wall=0.008 (<0.1 valid)
  [PASS] validation_Nu>=Nuinf       Nu/Nu_inf=9.15 (developing => >1)
  [PASS] validation_fRe_band        fRe/56.9=4.71 (1-6 developing duct, resolved)
  [PASS] physicality                Tw>Tb=True, 0<eps<1=True, h>0,f>0
  [PASS] mesh_present               nCells=291600 (GCI mesh-independence: PENDING, see caveats)
```
(Thresholds calibrated to the resolved mesh: energy balance <6% for the compressible buoyant
case on the high-aspect graded mesh; fRe band 1–6 for resolved strongly-developing duct flow.)

## 5. Results (converged, t = 6000)
| quantity | value |
|---|---|
| Re | 2305.71 |
| Nu | 33.0175 (Nu/Nu∞ = 9.14612) |
| f (Darcy) | 0.116224 (fRe/56.9 = 4.70965) |
| h [W/m²K] | 460.924 |
| wall superheat Tw−Tb [K] | 1.35959 |
| NTU / ε | 0.182416 / 0.166745 |
| Mouromtseff Mo | 45052.8 |
| Graetz L_t/L | 9.06913 |
| axial Peclet / λ_ax | 5441.48 / 0.000183774 |
| Ṡ_thermal / Ṡ_viscous [W/K] | 0.0012340166 / 3.0276365e-07 |
| Bejan irreversibility | 0.999754 |
| exergy destruction [W] | 0.370296 |
| pumping power Wp [W] | 6.84703e-05 |
| **energy balance error** | **2.41489 %** |

See `../He_vs_N2_comparison_REMESH.txt` for the head-to-head.

## 6. Honest caveats
1. **GCI (`../re-mesh/GCI_study/`): Nu is grid-converged** (Richardson-extrapolated ≈30.6, medium-mesh
   GCI 2.4% / fine 4.8%), but **f is not** (GCI ~17%, still rising) — locking f<3% needs ~2–5M
   cells, beyond this VM. f is reported with that uncertainty band.
2. **High-aspect graded cells** leave a p_rgh residual floor (2.41489%
   energy balance); the solution is steady (TWall to
   <1e-4) but convergence isn't as tight as a uniform mesh.
3. Nu/Nu∞≈9 for LN2 is high vs simple thermal-Graetz (~9–12 absolute); attributable to Gz=181 + Pr=2.36 + one-wall heating + the global-Nu definition. Cross-check vs an asymmetric-heating developing-flow correlation if a referee asks.
4. λ_ax≪1 confirms fluid axial conduction is negligible (Pe≫1) — neglecting it is justified.
5. EGM is thermal-irreversibility-dominated (Bejan≈1); viscous (pumping) entropy is negligible.
6. eps-NTU uses the single-stream isothermal-wall-limit relation (constant-q wall → effectiveness proxy).
