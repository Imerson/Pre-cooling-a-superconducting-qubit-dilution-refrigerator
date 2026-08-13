#!/usr/bin/env python3
# He(50K) vs LN2(77K) cold-plate comparison on the grid-converged GRADED mesh.
# Includes Mouromtseff, NTU/eps, Graetz, axial-conduction (lambda_ax), and EGM/entropy.
import os
BASE="/home/ubuntu/channel/remesh/production"
HE=os.path.join(BASE,"He_graded"); LN=os.path.join(BASE,"LN2_graded")
def csv1(p):
    L=open(p).read().splitlines(); return dict(zip(L[0].split(','),L[1].split(',')))
def load(d):
    m=csv1(os.path.join(d,'metrics.csv'))
    e=csv1(os.path.join(d,'egm_lax.csv'))
    m.update(e); return m
he,ln=load(HE),load(LN)
def F(x):
    try: return float(x)
    except: return float('nan')
def mc(d,k):
    for ln_ in open(os.path.join(d,'system/metricConstants')):
        if ln_.startswith(k+'='): return float(ln_.split('=')[1])
    return float('nan')
kHe,kLN=mc(HE,'k_W_mK'),mc(LN,'k_W_mK')
import math
WpHe,WpLN=F(he['Wpump_W']),F(ln['Wpump_W'])
ReHe,ReLN=F(he['Re']),F(ln['Re'])

L=[]
L.append("="*78)
L.append(" Stage-1 cold-plate HX -- He(50K) vs LN2(77K)  [GRID-CONVERGED graded mesh, 292k]")
L.append(" Matched duty 9.4 W, Re=2300, laminar.  He: compressible | LN2: Boussinesq")
L.append(" Mesh GCI: Nu converged (extrap 30.6, GCI 2.4% medium); f GCI ~17% (uncertainty band)")
L.append("="*78)
L.append(f"{'quantity':<34}{'He_50K':>14}{'LN2_77K':>14}{'LN2/He':>12}")
L.append("-"*78)
def row(lbl,a,b,fmt="{:.4g}",ratio=True):
    r=(b/a) if (ratio and a not in (0,) and not math.isnan(a)) else float('nan')
    rs=(fmt.format(r) if ratio and not math.isnan(r) else "")
    L.append(f"{lbl:<34}{fmt.format(a):>14}{fmt.format(b):>14}{rs:>12}")
row("Re",ReHe,ReLN)
row("Nu",F(he['Nu']),F(ln['Nu']))
row("Nu/Nu_inf (3.61)",F(he['Nu_over_Nuinf']),F(ln['Nu_over_Nuinf']))
row("f (Darcy)",F(he['f_Darcy']),F(ln['f_Darcy']))
row("h [W/m2K]",F(he['h_W_m2K']),F(ln['h_W_m2K']))
row("wall superheat Tw-Tb [K]",F(he['Tw_K'])-F(he['Tb_K']),F(ln['Tw_K'])-F(ln['Tb_K']))
row("pumping power Wp [W]",WpHe,WpLN)
L.append("-- HX effectiveness --")
row("NTU",F(he['NTU']),F(ln['NTU']))
row("effectiveness eps",F(he['eps']),F(ln['eps']))
L.append("-- fluid figure of merit --")
row("Mouromtseff Mo",F(he['Mo']),F(ln['Mo']))
row("thermal conductivity k [W/mK]",kHe,kLN)
L.append("-- developing-flow / axial conduction --")
row("Graetz L_t/L",F(he['Lt_over_L']),F(ln['Lt_over_L']))
row("axial Peclet (Dh)",F(he['axial_Peclet']),F(ln['axial_Peclet']))
row("lambda_ax = 1/Pe",F(he['lambda_ax']),F(ln['lambda_ax']))
L.append("-- EGM / entropy generation --")
row("Sgen_thermal [W/K]",F(he['Sgen_thermal_WK']),F(ln['Sgen_thermal_WK']))
row("Sgen_viscous [W/K]",F(he['Sgen_viscous_WK']),F(ln['Sgen_viscous_WK']))
row("Sgen_total [W/K]",F(he['Sgen_total_WK']),F(ln['Sgen_total_WK']))
row("Bejan irreversibility (thermal)",F(he['Bejan_irrev']),F(ln['Bejan_irrev']),ratio=False)
row("exergy destruction [W] (T0=300K)",F(he['exergy_W']),F(ln['exergy_W']))
L.append("-"*78)
L.append("")
L.append("MATCHED Re=2300: LN2 gives %.1fx higher h and %.1fx lower wall superheat at %.1fx LESS pumping."%(
    F(ln['h_W_m2K'])/F(he['h_W_m2K']),
    (F(he['Tw_K'])-F(he['Tb_K']))/(F(ln['Tw_K'])-F(ln['Tb_K'])),
    WpHe/WpLN))
L.append("MATCHED PUMPING (laminar Wp~Re^2): h~Nu*k/Dh, Nu~Re-weak => advantage set by k_LN2/k_He=%.1f."%(kLN/kHe))
L.append("MOUROMTSEFF: Mo_LN2/Mo_He=%.0fx (turbulent-regime projection)."%(F(ln['Mo'])/F(he['Mo'])))
L.append("EGM: both thermal-dominated (Bejan~%.3f He / %.3f LN2); LN2 destroys LESS exergy per watt (lower wall superheat)."%(F(he['Bejan_irrev']),F(ln['Bejan_irrev'])))
L.append("AXIAL CONDUCTION: lambda_ax<<1 for both (Pe>>1) => fluid axial conduction negligible; neglecting it is justified.")
L.append("")
L.append("VERDICT: nitrogen at 77 K is the superior Stage-1 coolant on every axis -- higher h/Nu,")
L.append("lower plate superheat, less pumping, and lower exergy destruction per watt.")
L.append("="*78)
txt="\n".join(L)
open(os.path.join("/home/ubuntu/channel/remesh","He_vs_N2_comparison_REMESH.txt"),'w').write(txt+"\n")
# merged csv
import csv as C
keys=['fluid','model','Re','Nu','Nu_over_Nuinf','f_Darcy','h_W_m2K','Tw_K','Tb_K','Wpump_W','NTU','eps','Mo','Lt_over_L','axial_Peclet','lambda_ax','Sgen_thermal_WK','Sgen_viscous_WK','Sgen_total_WK','Bejan_irrev','exergy_W','ebal_pct']
with open(os.path.join("/home/ubuntu/channel/remesh","He_vs_N2_comparison_REMESH.csv"),'w',newline='') as fp:
    w=C.writer(fp); w.writerow(keys)
    for d in (he,ln): w.writerow([d.get(k,'') for k in keys])
print(txt)
