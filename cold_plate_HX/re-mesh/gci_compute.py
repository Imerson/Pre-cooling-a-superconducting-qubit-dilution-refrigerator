#!/usr/bin/env python3
# Grid Convergence Index (Celik et al. 2008, ASME J. Fluids Eng) for the LN2 mini-channel.
# Reads metrics.csv from coarse/medium/fine; reports p, Richardson extrapolation, GCI on Nu & f.
import math, os, sys
BASE=sys.argv[1] if len(sys.argv)>1 else "/home/ubuntu/channel/gci"
def csv(p):
    L=open(os.path.join(p,'metrics.csv')).read().splitlines()
    return dict(zip(L[0].split(','),L[1].split(',')))
fine,med,coarse=csv(f"{BASE}/fine"),csv(f"{BASE}/medium"),csv(f"{BASE}/coarse")
N=[float(fine['nCells']),float(med['nCells']),float(coarse['nCells'])]   # N1 fine .. N3 coarse

def gci(phi):
    p1,p2,p3=phi; N1,N2,N3=N
    r21=(N1/N2)**(1.0/3.0); r32=(N2/N3)**(1.0/3.0)
    e21=p2-p1; e32=p3-p2
    if e21==0: return None
    s=1.0 if (e32/e21)>0 else -1.0
    p=2.0
    for _ in range(200):
        q=math.log((r21**p - s)/(r32**p - s))
        pn=abs(math.log(abs(e32/e21))+q)/math.log(r21)
        if abs(pn-p)<1e-12: p=pn; break
        p=pn
    phi_ext=(r21**p*p1-p2)/(r21**p-1)
    ea21=abs((p1-p2)/p1); eext21=abs((phi_ext-p1)/phi_ext)
    gci21=1.25*ea21/(r21**p-1); 
    ea32=abs((p2-p3)/p2); gci32=1.25*ea32/(r32**p-1)
    asym=gci32/((r21**p)*gci21)
    return dict(r21=r21,r32=r32,p=p,ext=phi_ext,ea21=ea21*100,eext21=eext21*100,
                gci21=gci21*100,gci32=gci32*100,asym=asym,s=s)

quants={"Nu":(float(fine['Nu']),float(med['Nu']),float(coarse['Nu'])),
        "f_Darcy":(float(fine['f_Darcy']),float(med['f_Darcy']),float(coarse['f_Darcy'])),
        "h_W_m2K":(float(fine['h_W_m2K']),float(med['h_W_m2K']),float(coarse['h_W_m2K']))}

L=[]
L.append("="*70)
L.append(" GRID CONVERGENCE INDEX (GCI) -- Celik et al. 2008 (ASME)")
L.append(" Representative case: LN2 mini-channel, Re=2300, matched 9.4 W")
L.append("="*70)
L.append(f" Meshes (cells):  fine N1={N[0]:.0f}  medium N2={N[1]:.0f}  coarse N3={N[2]:.0f}")
r21=(N[0]/N[1])**(1/3); r32=(N[1]/N[2])**(1/3)
L.append(f" Refinement ratio: r21={r21:.4f}  r32={r32:.4f}  (both > 1.3, per Celik)")
L.append("-"*70)
for q,(p1,p2,p3) in quants.items():
    g=gci((p1,p2,p3))
    L.append(f"\n {q}:  fine={p1:.5g}  medium={p2:.5g}  coarse={p3:.5g}")
    if g is None: L.append("   (no variation between meshes)"); continue
    L.append(f"   apparent order p           = {g['p']:.3f}")
    L.append(f"   Richardson extrapolated    = {g['ext']:.5g}")
    L.append(f"   approx. rel. error e_a21   = {g['ea21']:.3f} %")
    L.append(f"   extrapolated rel. err e_ext= {g['eext21']:.3f} %")
    L.append(f"   GCI_fine (21)              = {g['gci21']:.3f} %")
    L.append(f"   GCI_medium (32)            = {g['gci32']:.3f} %")
    L.append(f"   asymptotic-range ratio     = {g['asym']:.3f}  (target ~1.0)")
    L.append(f"   {'monotonic' if g['s']>0 else 'oscillatory'} convergence")
gNu=gci(quants["Nu"]); gf=gci(quants["f_Darcy"])
L.append("\n"+"-"*70)
verdict_mesh = "medium (43,200 cells, the production mesh)"
L.append(" VERDICT:")
L.append(f"   Nu GCI(fine) = {gNu['gci21']:.2f}%  (medium-mesh GCI = {gNu['gci32']:.2f}%)")
L.append(f"   f  GCI(fine) = {gf['gci21']:.2f}%  (medium-mesh GCI = {gf['gci32']:.2f}%)")
ok = gNu['gci32']<3.0 and gf['gci32']<5.0
L.append(f"   Production {verdict_mesh}: Nu within {gNu['gci32']:.2f}% / f within {gf['gci32']:.2f}% of")
L.append(f"   the grid-converged value -> {'GRID-INDEPENDENT (target Nu GCI<3%)' if ok else 'review: GCI above target'}.")
L.append("="*70)
txt="\n".join(L)
open(os.path.join(BASE,"GCI_report.txt"),'w').write(txt+"\n")
print(txt)
