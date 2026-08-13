#!/usr/bin/env python3
"""Figures for the Cryogenics pre-cooling paper, from model data."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 10, 'font.family': 'DejaVu Serif',
                     'axes.grid': True, 'grid.alpha': 0.3, 'figure.dpi': 300,
                     'savefig.bbox': 'tight'})
OUT = ("/Users/imerson/Library/CloudStorage/OneDrive-Personal/Documents/Education Hub/"
       "15-Energy Systems/4-Year 3/4-Dissertation/8-Publlication/1-Pre-cooling paper")
HX = ("/Users/imerson/Library/CloudStorage/OneDrive-Personal/Documents/Education Hub/"
      "15-Energy Systems/4-Year 3/4-Dissertation/2-Model/2-Stage 1 Heat exchanger")
C_HE, C_N2 = '#B85042', '#50708E'   # helium route / nitrogen route
C_RAD, C_CON = '#E8A87C', '#1E2761'

# ---------------- Fig 2: cascade heat loads (production values) ----------------
cases = ['S1: 300$\\to$50 K\n(He)', 'S1: 300$\\to$77 K\n(LN$_2$)',
         'S2: 50$\\to$4 K\n(He)', 'S2: 77$\\to$4 K\n(LN$_2$)']
rad  = np.array([8.411, 8.383, 0.003443, 0.01935])
cond = np.array([1.029, 0.962, 0.070294, 0.16210])
x = np.arange(4)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.bar(x, rad, 0.55, color=C_RAD, label='Radiation')
ax.bar(x, cond, 0.55, bottom=rad, color=C_CON, label='Conduction')
for xi, (r, c) in enumerate(zip(rad, cond)):
    t = r + c
    lab = f'{t:.2f} W' if t > 1 else f'{t*1e3:.0f} mW'
    ax.text(xi, t*1.25, lab, ha='center', fontsize=9)
ax.set_yscale('log'); ax.set_ylim(1e-3, 60)
ax.set_xticks(x); ax.set_xticklabels(cases, fontsize=8.5)
ax.set_ylabel('Stage heat load [W]')
ax.legend(fontsize=9, loc='upper right')
ax.text(0.5, 20, 'radiation-dominated', ha='center', fontsize=8, color='#B06A3B')
ax.text(2.5, 0.45, 'conduction-dominated', ha='center', fontsize=8, color=C_CON)
fig.savefig(f"{OUT}/fig2_cascade_loads.png"); plt.close(fig)

# ---------------- Fig 3: view-factor agglomeration sweep vs analytic anchor ----------------
lvl = [60, 250, 500]
s1 = [9.455681, 8.411264, 3.575180]; anchor1 = 7.073
fig, ax = plt.subplots(figsize=(5.8, 3.5))
ax.plot(lvl, s1, 'o-', color=C_CON, lw=1.5, ms=6)
ax.axhline(anchor1, ls='--', color=C_HE, lw=1.3)
ax.text(70, anchor1-0.55, 'analytic grey-body anchor: 7.07 W', fontsize=8.5, color=C_HE)
labs = ['coarse\n(over-predicts)', 'production\n(+19%, retained)', 'over-agglomerated\n(closure lost, discarded)']
offs = [(8, 4), (8, 4), (-10, 8)]
for x_, y_, lab, off in zip(lvl, s1, labs, offs):
    ax.annotate(lab, (x_, y_), textcoords='offset points', xytext=off, fontsize=7.5,
                ha='left' if off[0] > 0 else 'right')
ax.set_xlabel('View-factor agglomeration level [coarsest patch faces]')
ax.set_ylabel('Stage-1 radiative load [W]')
ax.set_xlim(20, 590); ax.set_ylim(2.8, 10.5)
fig.savefig(f"{OUT}/fig3_radiation_sweep.png"); plt.close(fig)

# ---------------- Fig 4: cold-plate GCI (Nu and f) ----------------
g = pd.read_csv(f"{HX}/re-mesh/GCI_study/gci_convergence.csv")
g = g[g['mesh'].isin(['coarse', 'medium', 'fine'])]
cells = g.nCells.values; Nu = g.Nu.values; f = g.f_Darcy.values
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.4), gridspec_kw={'wspace': 0.35})
h = cells**(-1/3)*1e2
a1.plot(h, Nu, 'o-', color=C_N2, lw=1.5)
a1.axhline(30.64, ls='--', color=C_HE, lw=1.2)
a1.text(2.28, 30.72, 'Richardson extrapolate 30.6', fontsize=8, color=C_HE, va='bottom')
for x_, y_, lab in zip(h, Nu, ['coarse (86k)', 'medium (292k, production)', 'fine (984k)']):
    a1.annotate(lab, (x_, y_), textcoords='offset points', xytext=(6, 5), fontsize=7.5)
a1.set_xlabel(r'Cell size $h\propto N^{-1/3}$ [$\times10^{-2}$]'); a1.set_ylabel(r'$\mathrm{Nu}$')
a1.set_title('(a) Nusselt number: $p=1.63$, GCI$_{32}$ = 2.4%', fontsize=9)
a1.set_ylim(30.4, 33.9); a1.invert_xaxis()
a2.plot(h, f, 's-', color=C_N2, lw=1.5)
a2.axhline(0.1374, ls='--', color=C_HE, lw=1.2)
a2.text(2.28, 0.1360, 'Richardson extrapolate 0.137', fontsize=8, color=C_HE, va='top')
a2.set_xlabel(r'Cell size $h\propto N^{-1/3}$ [$\times10^{-2}$]'); a2.set_ylabel(r'$f$ (Darcy)')
a2.set_title('(b) Friction factor: $p=0.56$, GCI $\\approx$ 17%', fontsize=9)
a2.set_ylim(0.108, 0.142); a2.invert_xaxis()
fig.savefig(f"{OUT}/fig4_hx_gci.png"); plt.close(fig)

# ---------------- Fig 5: He vs LN2 ratio chart ----------------
d = pd.read_csv(f"{HX}/He_vs_N2_comparison_REMESH.csv")
he, n2 = d.iloc[0], d.iloc[1]
metrics = [
    (r'Mouromtseff $\mathrm{Mo}$',            n2.Mo/he.Mo,                       'ln2'),
    (r'Heat-transfer coeff. $h$',             n2.h_W_m2K/he.h_W_m2K,             'ln2'),
    (r'Nusselt $\mathrm{Nu}$',                n2.Nu/he.Nu,                       'ln2'),
    (r'Friction factor $f$',                  n2.f_Darcy/he.f_Darcy,             'he'),
    (r'NTU',                                  n2.NTU/he.NTU,                     'amb'),
    (r'Effectiveness $\varepsilon$',          n2.eps/he.eps,                     'amb'),
    (r'Pumping power $\dot W_\mathrm{p}$',    n2.Wpump_W/he.Wpump_W,             'ln2'),
    (r'Wall superheat $T_\mathrm{w}-T_\mathrm{b}$', (n2.Tw_K-n2.Tb_K)/(he.Tw_K-he.Tb_K), 'ln2'),
    (r'Entropy generation $\dot S_\mathrm{gen}$',   n2.Sgen_total_WK/he.Sgen_total_WK,   'ln2'),
    (r'Exergy destruction',                   n2.exergy_W/he.exergy_W,           'ln2'),
]
cols = {'ln2': C_N2, 'he': C_HE, 'amb': '#9AA5B1'}
fig, ax = plt.subplots(figsize=(6.6, 4.0))
y = np.arange(len(metrics))[::-1]
for yi, (lab, r, fav) in zip(y, metrics):
    ax.barh(yi, r, 0.6, color=cols[fav])
    ax.text(r*1.25 if r > 1 else r/1.35, yi, f'{r:.3g}', va='center', fontsize=8,
            ha='left' if r > 1 else 'right')
ax.axvline(1, color='k', lw=1)
ax.set_xscale('log'); ax.set_xlim(8e-3, 4e2)
ax.set_yticks(y); ax.set_yticklabels([m[0] for m in metrics], fontsize=8.5)
ax.set_xlabel(r'LN$_2$/He ratio at matched duty and $Re$  (log scale)')
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=C_N2, label='favours LN$_2$'), Patch(fc=C_HE, label='favours He'),
                   Patch(fc='#9AA5B1', label='capacity-rate artefact (see text)')],
          fontsize=8, loc='lower right')
fig.savefig(f"{OUT}/fig5_ln2_he_ratios.png"); plt.close(fig)

# ---------------- Fig 6: ideal wall-power ledger ----------------
s1 = {'He': 9.44*5.0, 'LN2': 9.345*2.9}
s2 = {'He': 0.0737*74, 'LN2': 0.1815*74}
analytic = {'He': 8.1*5.0 + 0.0737*74, 'LN2': 8.0*2.9 + 0.1815*74}
fig, ax = plt.subplots(figsize=(5.2, 3.6))
x = [0, 1]
for xi, k in zip(x, ['He', 'LN2']):
    c = C_HE if k == 'He' else C_N2
    ax.bar(xi, s1[k], 0.5, color=c, alpha=0.95)
    ax.bar(xi, s2[k], 0.5, bottom=s1[k], color=c, alpha=0.55)
    tot = s1[k]+s2[k]
    ax.plot([xi-0.25, xi+0.25], [analytic[k]]*2, 'k--', lw=1)
    ax.text(xi, tot+1.2, f'{tot:.0f} W', ha='center', fontsize=10, fontweight='bold')
    ax.text(xi, s1[k]/2, f'Stage 1\n{s1[k]:.1f} W', ha='center', va='center', color='w', fontsize=8.5)
    ax.text(xi, s1[k]+s2[k]/2+0.3, f'Stage 2: {s2[k]:.1f} W', ha='center', fontsize=8)
ax.text(0.5, analytic['He']-3.4, 'dashed: analytic-anchored\nbest estimate', ha='center', fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels(['He route\n(50 K shield)', 'LN$_2$ route\n(77 K shield)'])
ax.set_ylabel(r'Ideal wall power $\sum_i \dot Q_i\,(T_0-T_i)/T_i$  [W]')
ax.set_ylim(0, 60)
fig.savefig(f"{OUT}/fig6_cop_ledger.png"); plt.close(fig)
print("all figures written")
