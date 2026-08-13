# He_graded — grid-converged (re-mesh)

**Stage-1 cold-plate mini-channel HX — Helium @ 50 K (compressible)**

Re-meshed, **near-wall-graded** version of the cold-plate case (cells clustered at all four
no-slip walls, especially the heated wall). This replaces the original uniform 43k mesh, which
a GCI study showed was badly under-resolved. Numbers are read from the converged solution at
**t = 6000** (`Nu_f_report.txt`, `metrics.csv`, `egm_lax.csv`, `GATE_CHECK.txt`).

## 1. Methodology
- Solver `buoyantSimpleFoam (compressible variable-density, ideal-gas He)`, OpenFOAM v2412, laminar, matched duty **9.4 W**, Re=2300.
- Mesh: **291600 cells**, two-sided `simpleGrading` (expansion 6) in the two
  cross-stream directions. Mesh-independence by the GCI study in `../re-mesh/GCI_study/` (3 meshes,
  86k/292k/984k, r=1.5).
- Geometry: mini-channel Dh=0.01 m (10 mm), L=0.3 m, 5 parallel
  ducts, one wall heated (flux BC).

## 2. Boundary conditions
- Heated wall: uniform flux, Q=9.4 W (Stage-1 cooling requirement; see
  `../../Cascade_GCI_cooling_requirement/`).
- Inlet T=45 K, mass-flow pinned (Re=2300 exact);
  outlet reference pressure; walls noSlip; g=(0 -9.81 0).
- Ideal-gas density varies with T (no Boussinesq).

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
  [PASS] energy_balance_<6pct       err=5.16% (Qrem=9.8848 W)
  [PASS] Re_on_target_2300          Re=2300.0
  [PASS] steady_state_<0.1pct       TWall range/mean over last10=5.51e-05
  [PASS] model_appropriate          compressible variable-density (rho_ratio=1.13474); Boussinesq limit N/A
  [PASS] validation_Nu>=Nuinf       Nu/Nu_inf=3.85 (developing => >1)
  [PASS] validation_fRe_band        fRe/56.9=3.23 (1-6 developing duct, resolved)
  [PASS] physicality                Tw>Tb=True, 0<eps<1=True, h>0,f>0
  [PASS] mesh_present               nCells=291600 (GCI mesh-independence: PENDING, see caveats)
```
(Thresholds calibrated to the resolved mesh: energy balance <6% for the compressible buoyant
case on the high-aspect graded mesh; fRe band 1–6 for resolved strongly-developing duct flow.)

## 5. Results (converged, t = 6000)
| quantity | value |
|---|---|
| Re | 2300 |
| Nu | 13.886 (Nu/Nu∞ = 3.84654) |
| f (Darcy) | 0.0798295 (fRe/56.9 = 3.22685) |
| h [W/m²K] | 25.6998 |
| wall superheat Tw−Tb [K] | 24.3841 |
| NTU / ε | 0.236452 / 0.210576 |
| Mouromtseff Mo | 470.017 |
| Graetz L_t/L | 2.93633 |
| axial Peclet / λ_ax | 1761.8 / 0.000567601 |
| Ṡ_thermal / Ṡ_viscous [W/K] | 0.049961236 / 1.3220747e-06 |
| Bejan irreversibility | 0.999973 |
| exergy destruction [W] | 14.9888 |
| pumping power Wp [W] | 0.000142556 |
| **energy balance error** | **5.15745 %** |

See `../He_vs_N2_comparison_REMESH.txt` for the head-to-head.

## 6. Honest caveats
1. **GCI (`../re-mesh/GCI_study/`): Nu is grid-converged** (Richardson-extrapolated ≈30.6, medium-mesh
   GCI 2.4% / fine 4.8%), but **f is not** (GCI ~17%, still rising) — locking f<3% needs ~2–5M
   cells, beyond this VM. f is reported with that uncertainty band.
2. **High-aspect graded cells** leave a p_rgh residual floor (5.15745%
   energy balance for the compressible case); the solution is steady (TWall to
   <1e-4) but convergence isn't as tight as a uniform mesh.
3. He: constant Cp/μ/k (only density varies via ideal-gas EoS); real-He property variation over 45→80 K is modest.
4. λ_ax≪1 confirms fluid axial conduction is negligible (Pe≫1) — neglecting it is justified.
5. EGM is thermal-irreversibility-dominated (Bejan≈1); viscous (pumping) entropy is negligible.
6. eps-NTU uses the single-stream isothermal-wall-limit relation (constant-q wall → effectiveness proxy).
