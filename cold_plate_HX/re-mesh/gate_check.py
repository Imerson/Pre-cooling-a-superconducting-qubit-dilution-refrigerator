#!/usr/bin/env python3
# Gate-check / sanity QA for the Stage-1 cold-plate HX cases.
# Usage: gate_check.py <case_dir>
import sys, os, re, glob, math
case=sys.argv[1].rstrip('/')
name=os.path.basename(case)

def read_csv(p):
    L=open(p).read().splitlines()
    h=L[0].split(','); v=L[1].split(',')
    return dict(zip(h,v))
m=read_csv(os.path.join(case,'metrics.csv'))
def f(k):
    try: return float(m[k])
    except: return float('nan')

# steadiness from TWall FO history (last 10 samples)
tw=glob.glob(os.path.join(case,'postProcessing/TWall/*/surfaceFieldValue.dat'))
steady_metric=float('nan')
if tw:
    rows=[ln.split() for ln in open(tw[0]) if ln.strip() and not ln.startswith('#')]
    vals=[float(r[-1]) for r in rows[-10:]]
    if vals: steady_metric=(max(vals)-min(vals))/(sum(vals)/len(vals))

# log check
logp=os.path.join(case,'log.rerun_9p4')
log=open(logp).read() if os.path.exists(logp) else ''
ended = log.rstrip().endswith('End')
fatal = ('FOAM FATAL' in log)

model=m.get('model','?')
gates=[]
def G(nm, ok, detail): gates.append((nm, bool(ok), detail))

G('solver_completed', ended and not fatal, f"log ends 'End'={ended}, FATAL={fatal}")
G('duty_correct_9p4W', abs(f('Q_W')-9.4)<1e-6, f"Q_wall={m.get('Q_W')} W")
G('energy_balance_<6pct', abs(f('ebal_pct'))<6.0, f"err={f('ebal_pct'):.2f}% (Qrem={m.get('Qrem_W')} W)")
G('Re_on_target_2300', abs(f('Re')-2300)/2300<0.05, f"Re={f('Re'):.1f}")
G('steady_state_<0.1pct', steady_metric<1e-3, f"TWall range/mean over last10={steady_metric:.2e}")
if model=='boussinesq':
    G('model_appropriate', f('beta_dT_wall')<0.10, f"Boussinesq: beta*dT_wall={f('beta_dT_wall'):.3f} (<0.1 valid)")
else:
    G('model_appropriate', model=='compressible', f"compressible variable-density (rho_ratio={m.get('rho_ratio')}); Boussinesq limit N/A")
G('validation_Nu>=Nuinf', f('Nu_over_Nuinf')>=1.0, f"Nu/Nu_inf={f('Nu_over_Nuinf'):.2f} (developing => >1)")
G('validation_fRe_band', 1.0<=f('fRe_over_56p9')<=6.0, f"fRe/56.9={f('fRe_over_56p9'):.2f} (1-6 developing duct, resolved)")
phys = (f('Tw_K')>f('Tb_K')) and (0<f('eps')<1) and (f('h_W_m2K')>0) and (f('f_Darcy')>0)
G('physicality', phys, f"Tw>Tb={f('Tw_K')>f('Tb_K')}, 0<eps<1={0<f('eps')<1}, h>0,f>0")
G('mesh_present', f('nCells')>0, f"nCells={m.get('nCells')} (GCI mesh-independence: PENDING, see caveats)")

npass=sum(1 for _,ok,_ in gates if ok); n=len(gates)
out=[f"GATE CHECK (QA / sanity): {name}",
     f"  model={model}  Re={f('Re'):.0f}  Nu={f('Nu'):.2f}  h={f('h_W_m2K'):.1f} W/m2K  Q={m.get('Q_W')} W",
     "="*70]
for nm,ok,det in gates:
    out.append(f"  [{'PASS' if ok else 'FAIL'}] {nm:<26} {det}")
out.append("-"*70)
out.append(f"  {npass}/{n} gates passed")
txt="\n".join(out)
open(os.path.join(case,'GATE_CHECK.txt'),'w').write(txt+"\n")
print(txt)
sys.exit(0 if npass==n else 1)
