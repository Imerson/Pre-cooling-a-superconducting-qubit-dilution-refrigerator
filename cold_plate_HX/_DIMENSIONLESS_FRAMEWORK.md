# Dimensionless Analysis Framework — Buoyancy/Channel Coolant Suite

This document is the **shared reference** for the "Dimensionless Analysis" section
that appears in each of the 12 per-model READMEs in `cold_improved_models/`
(`Buoyancy_50K_{Manifold,Microchannel,Serpentine}[_Re2300]` and
`stage1_{manifold,microchannel,serpentine}_LN2_77K[_Re2300]`).

Every case was post-processed by the **same script**,
`system/postProcess_dimensionless.sh`, which reads six surface-field time
series (`postProcessing/{TInlet,TOutlet,TWall,inletMassFlow,pInlet,pOutlet}`)
plus a case-specific `system/metricConstants` file, and writes `Nu_f_report.txt`.
Per-case READMEs should reproduce the relevant subset of this framework, fill in
the case's actual numbers from its `Nu_f_report.txt` (and, where one exists, the
hand-written "converged result" README/comparison note), and interpret them.

---

## 1. Why dimensionless analysis at all

The 12 cases compare **three channel topologies** (Manifold, Microchannel,
Serpentine) at **two temperature regimes** (50 K helium-4, 77 K liquid
nitrogen) and **two flow conditions** (a low "base" flow, and a flow matched
to **Re = 2300**, the canonical laminar/turbulent transition Reynolds number
for internal duct flow). The raw CFD outputs (T, p, U fields) are not directly
comparable across these 12 runs because the geometry, fluid, and flow rate all
differ simultaneously. Dimensionless groups collapse these differences into a
common, geometry- and fluid-independent basis so that:

- a Manifold run at Re≈183 (He) and a Microchannel run at Re=2300 (LN2) can be
  ranked on the same axes (Nu, f, Nu/f, PF);
- the result can be checked against textbook/laminar-duct correlations
  (Shah & London 1978) to flag numerical artefacts vs. genuine physics;
- the choice of coolant (He-4 vs LN2) and topology can be separated from the
  choice of geometry scale — the key trade-off the dissertation needs to make
  for the Stage-1 (50–77 K) shield cooling loop.

---

## 2. Hydraulic diameter, cross-section, flow length

For a non-circular duct, `D_h = 4·A_cs / P` (4× cross-section area / wetted
perimeter). All 12 cases use **D_h = 0.01 m** (10 mm square channels), but
`A_cs` (flow cross-section, `Acs`), `A_heated` (`Aheated`, the heated wall
area exposed to the imposed flux) and `L_flow` (`Lflow`, streamwise length)
differ by topology:

| Topology    | A_cs (m²) | A_heated (m²) | L_flow (m) | Notes |
|---|---|---|---|---|
| Manifold    | 5.0×10⁻⁴ | 0.0125 | 0.25  | 5 parallel branches, headers excluded from L |
| Microchannel| 5.0×10⁻⁴ | 0.015  | 0.30  | 5 parallel straight channels |
| Serpentine  | 1.0×10⁻⁴ | 0.0154 | 1.58  | 1 channel, 5 passes + 4 bends |

These constants live in each case's `system/metricConstants` and are the
basis for every formula below.

---

## 3. Reynolds number — Re

```
Re = ρ·U_mean·D_h / μ        (= U_mean·D_h / ν)
```

`U_mean = |Q_vol| / A_cs`, where `Q_vol` is the volumetric flow rate read from
`postProcessing/inletMassFlow` (named "mass flow" but is volumetric here since
ρ is uniform within each case).

**Meaning**: ratio of inertial to viscous forces. Re ≈ 2300 is the classic
upper bound of laminar pipe/duct flow — the suite deliberately includes a
"base" condition (Re ≈ 180–920, well inside laminar) and a "**_Re2300**"
condition (matched across all six geometry/fluid pairs) so that topology
performance is compared *at the edge of the laminar regime*, the most
demanding laminar operating point and the one most relevant to a real cooling
loop sized for maximum throughput before transition.

---

## 4. Nusselt number — Nu, and the heat-transfer coefficient h

```
T_b = ½(T_in + T_out)                      bulk (mean) fluid temperature
h   = Q_wall / (A_heated · (T_wall − T_b)) convective heat-transfer coefficient [W/m²K]
Nu  = h · D_h / k_fluid                     Nusselt number [-]
```

**Meaning**: Nu is the ratio of convective to conductive heat transfer across
the fluid boundary layer — Nu = 1 would mean the fluid layer conducts heat as
if it were stagnant; Nu > 1 quantifies the enhancement from advection/mixing.
For fully-developed laminar flow in a square duct with one heated wall, the
**Shah & London (1978)** constant-flux correlation gives **Nu∞ ≈ 3.61**. Each
case's computed Nu is compared against this 3.61 baseline: Nu/Nu∞ > 1
indicates entrance-region and/or bend-induced (Dean vortex) enhancement above
the fully-developed value.

**⚠ Known data issue — `Qwall_W` constant.** Every `system/metricConstants`
in this suite carries `Qwall_W=8.70`, a stale value. The boundary condition
actually imposed on the heated wall (`fixedGradient`, documented in the
converged-case READMEs) corresponds to **Q_wall = 13.4183 W**
(`q_w = Q_wall/A_heated`, gradient = `q_w/k_fluid`). Because `h` and therefore
`Nu`, `St`, `j_Colburn`, `Nu/f` and `j/f` are all directly proportional to `Q`,
**every value of h, Nu, St, j_Colburn, Nu/f, j/f in `Nu_f_report.txt` is low
by a factor of 13.4183/8.70 ≈ 1.542** relative to the true imposed load.
Where a hand-derived "converged Re=2300" result exists (it uses Q=13.4183 W
directly), that number is the dissertation-quality one; the `Nu_f_report.txt`
values are reported as-is with this factor flagged.

---

## 5. Friction factor — f (Darcy)

```
f = 2·ΔP·D_h / (ρ·U_mean²·L_flow)         Darcy friction factor [-]
```

`ΔP = |p_in − p_out|` (true pressure, Pa). For fully-developed laminar duct
flow, `f·Re ≈ 56.9` (square duct, Shah & London 1978), i.e.
`f_theory = 56.9/Re`.

**Meaning**: f is the normalised pressure drop per unit length — the
"hydraulic cost" of moving fluid through the channel. `f/f_theory` close to 1
indicates fully-developed, bend-free laminar flow; large `f/f_theory`
indicates entrance effects, bend (secondary-flow) losses, or — at very low
Re — buoyancy-driven recirculation inflating the apparent pressure drop.

**⚠ Known data issue — RESOLVED (revised 2026-06).** An earlier version of
this framework flagged that `postProcess_dimensionless.sh` computes
`f = 2·ΔP·D_h/(U_mean²·L_flow)` with **ρ omitted** from the denominator, and
stated that for the LN2 cases (ρ = 807 kg/m³) the reported `f` would
therefore be ≈807× too large and need dividing by ρ. **That guidance is
incorrect and is retracted.** The correct picture, established by
cross-checking `Nu_f_report.txt` against the independently hand-derived
"Converged Result" tables for the LN2 microchannel and serpentine cases, is:

1. **`f`'s formula omits ρ from the denominator** — true.
2. **BUT, for the LN2 cases, `DeltaP_Pa` in `Nu_f_report.txt` is *not* in true
   pascals.** `buoyantBoussinesqSimpleFoam` (and the underlying `rhoConst`
   Boussinesq formulation) carries pressure as a **kinematic** quantity
   (`p_rgh`, units m²/s² = Pa/ρ_ref). The post-processing script subtracts
   `p_in − p_out` directly from this kinematic field and labels the result
   `DeltaP_Pa` without re-multiplying by ρ. So in fact
   `DeltaP_Pa(reported) = ΔP_true / ρ`.
3. **The two errors exactly cancel for `f` itself**:
   ```
   f_reported = 2 · ΔP_reported · D_h / (U_mean² · L)
              = 2 · (ΔP_true/ρ) · D_h / (U_mean² · L)
              = 2 · ΔP_true · D_h / (ρ · U_mean² · L)
              = f_Darcy (true, standard definition)
   ```
   **`f_reported` already IS the standard dimensionless Darcy friction
   factor — for He-4 (ρ=1, no kinematic/true distinction) AND for LN2. No
   ρ-correction of any kind is needed for `f`, `Nu_over_f`, `j_over_f`, or
   `PF = Nu/f^(1/3)`** — all four are directly cross-fluid-comparable as
   reported.
4. **Empirical confirmation** (the smoking gun): the hand-derived "Converged
   Result" Darcy-f values, computed independently from the raw simulation
   fields with explicit ρ-scaling, match `Nu_f_report.txt`'s `f` to <0.1%:
   - `stage1_microchannel_LN2_77K`: hand-derived Darcy f = **0.07956** vs.
     `Nu_f_report.txt` f = **0.0795583** (Δ ≈ 0.005%).
   - `stage1_serpentine_LN2_77K`: hand-derived Darcy f = **0.1066** vs.
     `Nu_f_report.txt` f = **0.106635** (Δ ≈ 0.03%).
   If the old "/807" guidance were correct, these pairs would differ by a
   factor of ~807, not <0.1%.
5. **A *different* ρ-correction IS needed — for `DeltaP_Pa`, `Wp_W`, and
   `Convec_Bejan` (§13) in the LN2 cases**, because (unlike `f`, `Nu_over_f`,
   `j_over_f`, `PF`, which are dimensionless ratios where the missing-ρ and
   kinematic-ΔP errors cancel) these three quantities carry units that do
   *not* benefit from that cancellation:
   ```
   DeltaP_Pa(true) = DeltaP_Pa(reported) × ρ        [Pa]
   Wp_W(true)      = Wp_W(reported)      × ρ        [W]   (Wp = ΔP·Q_vol)
   Convec_Bejan(true) = Convec_Bejan(reported) × ρ        [-]  (Be = ΔP·L²/(μα))
   ```
   For He-4 (ρ = 1.0 kg/m³ exactly) this correction is a no-op — kinematic
   and true pressure are numerically identical, so `DeltaP_Pa`, `Wp_W`, `f`,
   and `Convec_Bejan` are all already correct as reported. **For LN2
   (ρ = 807 kg/m³), multiply `DeltaP_Pa`, `Wp_W`, and `Convec_Bejan` by 807**;
   leave `f`, `Nu_over_f`, `j_over_f`, `PF` unchanged.
6. **Empirical confirmation for `Wp_W`**: `stage1_microchannel_LN2_77K`'s
   `Nu_f_report.txt` gives `Wp_W = 5.76484e-8`; × 807 = **46.5 µW**, exactly
   matching that case's hand-derived "Converged Result" pumping power. Same
   for `stage1_serpentine_LN2_77K`: `Wp_W = 8.13894e-8 × 807 = 65.7 µW`,
   exact match.

**Net effect on the two completed LN2-manifold READMEs**
(`stage1_manifold_LN2_77K`, `stage1_manifold_LN2_77K_Re2300`): their §8.4
sections, written under the old (incorrect) guidance, divided the reported
`f` by 807 and concluded `f_Darcy ≈ 7.4×10⁻⁵` (≈185× *below* `f_theory`).
Under the corrected rule, `f_reported` (0.0599177 / 0.060439) **is itself**
`f_Darcy`, giving `f/f_theory ≈ 4.36 / 4.41` — in line with the other
LN2 and He-4 cases' `f/f_theory ≈ 2–5`. Conversely, those READMEs' `DeltaP_Pa`
and `Wp_W` values (`0.00510941 Pa` / `2.11005e-7 W` and `0.0051795 Pa` /
`2.14431e-7 W`) need × 807, giving true `ΔP ≈ 4.12 / 4.18 Pa` and
`Wp ≈ 170.3 / 173.0 µW`.

---

## 6. Merit ratios — Nu/f and PF = Nu/f^(1/3)

```
Nu/f   — heat transfer gained per unit hydraulic penalty
PF = Nu / f^(1/3)   — "performance factor", the standard heat-exchanger figure
                        of merit for constant-pumping-power comparisons
```

**Meaning**: a channel that doubles Nu but quadruples f is a poor trade; Nu/f
and PF normalise heat-transfer benefit against hydraulic cost so that
Manifold/Microchannel/Serpentine — three geometries with very different f —
can be ranked on a single axis. Higher is better for both.

---

## 7. Stanton number St and Colburn j-factor

```
St = Nu / (Re · Pr)            Stanton number
j  = St · Pr^(2/3)             Colburn j-factor
j/f                             heat-transfer/friction analogy ratio
```

**Meaning**: St is Nu non-dimensionalised by the flow's thermal capacity flux
— it directly compares heat actually transferred to the maximum possible
(ρ·U·cp·ΔT). The Colburn j-factor extends the Reynolds analogy (heat transfer
~ momentum transfer) to fluids with Pr ≠ 1 via the Pr^(2/3) Chilton-Colburn
correction. `j/f` close to 0.5 indicates the Reynolds analogy holds (heat and
momentum transport equally efficient); `j/f` << 0.5 indicates the geometry
incurs friction penalties disproportionate to its heat-transfer benefit
(typical of bends/headers).

---

## 8. Prandtl number Pr

```
Pr = ν/α = μ·cp/k    (fluid property input, not solved for)
```

**Meaning**: ratio of momentum diffusivity to thermal diffusivity — how fast
velocity disturbances diffuse relative to temperature disturbances. He-4 at
50 K: Pr ≈ 0.766 (momentum and heat diffuse at comparable rates, typical of
gases). LN2 at 77 K: Pr ≈ 2.36 (thermal boundary layer thinner than momentum
boundary layer, typical of liquids). Note: several `transportProperties`
files use Pr as an *input* to the Boussinesq solver's thermal diffusivity,
not a measured output.

---

## 9. Mouromtseff number — Mo

```
Mo = k^0.6 · ρ^0.8 · cp^0.4 · μ^(-0.4)
```

**Meaning**: a fluid figure-of-merit (Mouromtseff 1942) for single-phase
forced-convection cooling, independent of geometry — it ranks coolants by how
much heat transfer (h) they deliver per unit pumping power for a *fixed*
channel. He-4 (50 K): Mo ≈ 470. LN2 (77 K): Mo ≈ 45 000, **≈ 96× higher** —
LN2 is an intrinsically far more effective convective coolant than helium gas
at these conditions, which is the core "why LN2 for the 77 K stage"
argument. (Geometry-dependent effects — Re regime, entrance length — still
modulate the realised Nu, so Mo is a *ranking* indicator, not a direct Nu
predictor.)

---

## 10. Grashof number Gr, Gr/Re² and Rayleigh Ra — natural vs. forced convection

```
Gr    = g·β·ΔT·L³ / ν²              Grashof number
Gr/Re²                               buoyancy-to-inertia ratio
Ra    = Gr·Pr                        Rayleigh number (pure natural convection)
```

**Meaning**: Gr is the buoyancy analogue of Re — ratio of buoyancy to viscous
forces. `Gr/Re²` determines the convection regime:

- `Gr/Re² >> 1` → **natural-convection dominated**: buoyancy-driven
  recirculation dominates the imposed flow. This is the regime found for the
  *base-flow* (low Re) He-4 cases (Gr/Re² ~ 10⁴–10⁶), where buoyant plumes from
  the heated wall recirculate against the imposed throughflow, inflating the
  apparent friction factor and stalling SIMPLE-algorithm convergence.
- `Gr/Re² << 1` → **forced-convection dominated**: the imposed flow
  overwhelms buoyancy. This is the design intent of the **Re = 2300**
  matched-flow condition (Gr/Re² ~ 0.02–0.2 for all six Re2300 cases).
- `Gr/Re² ~ O(1)` → mixed convection (neither dominates).

---

## 11. Boussinesq validity — β·ΔT

`buoyantBoussinesqSimpleFoam` linearises density as
`ρ = ρ_ref·(1 − β(T − T_ref))`. This linearisation is only accurate for small
relative temperature excursions:

```
β·ΔT << 1     (commonly: β·ΔT < ~0.3 "acceptable", > ~1 "invalid")
```

- He-4, β = 0.02 K⁻¹: at the base-flow condition ΔT ~ 100 K → β·ΔT ≈ 2,
  **violates** the Boussinesq assumption — rankings between topologies remain
  *qualitatively* valid (same linearisation error applies to all three), but
  absolute Nu/f/h values carry ~10–20% uncertainty. At the Re=2300 matched
  condition ΔT ~ 5–8 K → β·ΔT ≈ 0.1–0.2, comfortably valid.
- LN2, β = 0.0057 K⁻¹: even the largest ΔT (~5–6 K, wall-to-bulk) gives
  β·ΔT ≈ 0.03, well within validity for every LN2 case.

---

## 12. Carnot COP

```
COP_Carnot = T_cold / (T_room − T_cold),   T_room = 293 K (CarnotCOP in metricConstants
                                             is computed at T_room=300K in some cases)
```

**Meaning**: the theoretical best-case coefficient of performance for a
refrigerator rejecting to room temperature and absorbing at `T_cold` — the
thermodynamic ceiling against which the *real* cryocooler's input power
(W/W) for the heat load `Q_wall` would be judged. He-4 (50 K):
COP_Carnot ≈ 0.21–0.206. LN2 (77 K): COP_Carnot ≈ 0.345–0.356. The higher
COP_Carnot at 77 K is the thermodynamic reason every Watt of heat intercepted
at the LN2-cooled 77 K stage is "cheaper" (in cryocooler input power) than the
same Watt intercepted at 50 K — independent of which channel topology is used.

---

## 13. Second-law (entropy generation / exergy) terms

For the six **base-condition** directories (not the `_Re2300` variants —
see §14), `Nu_f_report.txt` additionally reports:

```
Irrev_sT  = ∫ κ|∇T|²/T² dV   [W/K]   thermal (conduction) entropy generation rate
Irrev_sV  = ∫ 2μ(S:S)/T dV   [W/K]   viscous entropy generation rate (S = strain-rate tensor)
Irrev_Bejan = Irrev_sT / (Irrev_sT + Irrev_sV)     thermal fraction, ∈[0,1]
W_exergy  = T₀ · (Irrev_sT + Irrev_sV),  T₀ = 300 K     exergy destruction rate [W]
Convec_Bejan (= Be) = ΔP·L² / (μ·α),  α = k/(ρ·cp)      Bejan (entropy-generation) number
```

**Meaning**: this is a second-law (entropy/exergy) view of the same flow.
`Irrev_Bejan ≈ 0.99999...` in every base case means entropy generation is
**almost entirely from thermal gradients** (axial/radial conduction across
the ΔT between wall and bulk), with viscous dissipation contributing a
negligible fraction — expected at these very low Re and ΔP. `W_exergy`
converts that entropy generation into an equivalent rate of "lost work" at a
300 K reference — i.e. how much room-temperature shaft work is destroyed by
the temperature gradients sustaining the heat transfer, a quantity that scales
roughly with `Q_wall` and `ΔT_wall-bulk` and is therefore largest for the
worst-performing (highest ΔT) topology. The separate `Convec_Bejan` (=Be) is
the classic Bejan number relating pumping-driven pressure drop to thermal
diffusion time-scale; very large Convec_Bejan (10⁷–10¹¹ across this suite)
reflects how slow thermal diffusion is relative to the imposed pressure
forces at these flow rates — i.e. that heat transport here is
advection-dominated, not diffusion-dominated, consistent with Pe = Re·Pr >> 1
in every case.

**⚠ LN2 correction**: `Convec_Bejan = ΔP·L²/(μ·α)` is computed from the same
`DeltaP_Pa` field discussed in §5. For the LN2 cases, `DeltaP_Pa(reported)`
is the *kinematic* pressure drop (`ΔP_true/ρ`), so
`Convec_Bejan(reported) = Convec_Bejan(true)/ρ`. **Multiply the reported
`Convec_Bejan` by ρ = 807 for LN2 cases** to get the true Bejan number (no
correction for He-4, ρ=1). This does not change the qualitative conclusion
(Convec_Bejan remains enormous either way — advection-dominated heat
transport), only its absolute magnitude.

---

## 14. ⚠ Second known data issue — `_Re2300` report template

For the six base-condition directories
(`Buoyancy_50K_{Manifold,Microchannel,Serpentine}`,
`stage1_{manifold,microchannel,serpentine}_LN2_77K`), `Nu_f_report.txt`
contains valid `Irrev_sT_WperK`, `Irrev_sV_WperK`, `Irrev_Bejan` and
`W_exergy_W` values (§13).

For the six `_Re2300` directories, the report template was regenerated with
renamed-but-unpopulated fields: `Irrev_Be_thermal_WperK:`,
`Irrev_Be_viscous_WperK:` and `Irrev_Bejan:` are **blank**, and
`W_exergy_loss_W:` is **mis-populated with the `CarnotCOP` value** (a
field-alignment bug in the later script version). Per-case READMEs for the
`_Re2300` directories should state that second-law entropy/exergy data is
**not available** for that run, rather than report the spurious
`W_exergy_loss_W = CarnotCOP` figure as an exergy value.

---

## 15. Summary formula sheet

| Symbol | Formula | Source |
|---|---|---|
| Re | ρ U D_h / μ | `postProcess_dimensionless.sh` |
| Nu | h D_h / k, h = Q/(A_heated(T_w−T_b)) | ″ |
| f (Darcy) | 2ΔP D_h /(ρ U² L) — **reported value is correct as-is, no ρ correction (§5)** | ″ |
| Nu/f, PF | Nu/f, Nu/f^(1/3) — correct as reported | ″ / hand reports |
| St | Nu/(Re·Pr) | ″ |
| j (Colburn) | St·Pr^(2/3) | ″ |
| j/f | j/f — correct as reported | ″ |
| Mo | k^0.6 ρ^0.8 cp^0.4 μ^-0.4 | ″ |
| Gr | gβΔT L³/ν² | hand reports / derived |
| Gr/Re² | — | hand reports / derived |
| Ra | Gr·Pr | derived |
| β·ΔT | Boussinesq validity | hand reports |
| COP_Carnot | T_cold/(T_room−T_cold) | `metricConstants` |
| Be (Convec_Bejan) | ΔP L²/(μα), α=k/(ρcp) — **× ρ=807 for LN2 cases (§5/§13)** | `postProcess_dimensionless.sh` |
| Irrev_sT, Irrev_sV, Irrev_Bejan, W_exergy | §13 | ″ (base cases only) |
| DeltaP_Pa, Wp_W | — | **× ρ=807 for LN2 cases to get true Pa/W (§5)** |

---

## 16. Reference correlations

- **Shah, R.K. & London, A.L. (1978)**, *Laminar Flow Forced Convection in
  Ducts* — square duct, one wall heated, fully developed: **Nu∞ ≈ 3.61**,
  **f·Re ≈ 56.9**.
- **Mouromtseff, I.E. (1942)** — coolant figure of merit, §9.
- **Bejan, A.** — entropy generation minimisation / Bejan number, §13.
