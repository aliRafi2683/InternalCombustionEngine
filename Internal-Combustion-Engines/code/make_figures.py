"""
Generate all figures for the report.
Outputs PNGs into ../figures/
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'figures')
os.makedirs(OUT, exist_ok=True)

K, cp, cv = 1.4, 1.005, 0.718
R = cp - cv
P1, T1 = 100.0, 300.0
r = 14.5726
alpha = 1.7
cutoff = 0.05

# ---------- shared dual states ----------
v1 = R*T1/P1; v2 = v1/r
T2 = T1*r**(K-1); P2 = P1*r**K
v3 = v2; P3 = alpha*P2; T3 = T2*alpha
v4 = v3 + cutoff*(v1-v2); P4 = P3; T4 = T3*(v4/v3)
v5 = v1; T5 = T4*(v4/v5)**(K-1); P5 = P4*(v4/v5)**K
q_in = cv*(T3-T2) + cp*(T4-T3)

def isentrope(va, vb, Pa, n=120):
    vs = np.linspace(va, vb, n)
    Ps = Pa*(va/vs)**K
    return vs, Ps

# ============ FIG 1: P-V dual/otto/diesel ============
fig, ax = plt.subplots(figsize=(8,5.5))
# dual
vc, Pc = isentrope(v1, v2, P1)
ax.plot(vc, Pc, 'b')
ax.plot([v2,v3],[P2,P3],'b')
ax.plot([v3,v4],[P3,P4],'b')
ve, Pe = isentrope(v4, v5, P4)
ax.plot(ve, Pe, 'b', label='Dual')
ax.plot([v5,v1],[P5,P1],'b')

# otto same q_in
T3o = T2 + q_in/cv; P3o = P2*(T3o/T2)
T4o = T3o*(1/r)**(K-1); P4o = P3o*(1/r)**K
vc,Pc = isentrope(v1,v2,P1); ax.plot(vc,Pc,'r--')
ax.plot([v2,v2],[P2,P3o],'r--')
ve,Pe = isentrope(v2,v1,P3o); ax.plot(ve,Pe,'r--',label='Otto')
ax.plot([v1,v1],[P4o,P1],'r--')

# diesel same q_in
T3d = T2 + q_in/cp; rc = T3d/T2; v3d = v2*rc; P3d = P2
T4d = T3d*(v3d/v1)**(K-1); P4d = P3d*(v3d/v1)**K
vc,Pc = isentrope(v1,v2,P1); ax.plot(vc,Pc,'g-.')
ax.plot([v2,v3d],[P2,P3d],'g-.')
ve,Pe = isentrope(v3d,v1,P3d); ax.plot(ve,Pe,'g-.',label='Diesel')
ax.plot([v1,v1],[P4d,P1],'g-.')

ax.set_xlabel('Specific Volume  v (m$^3$/kg)')
ax.set_ylabel('Pressure  P (kPa)')
ax.set_title('Comparative P-V Diagram: Dual, Otto, Diesel  (r = 14.57)')
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/fig1_pv_three.png', dpi=150); plt.close()

# ============ FIG 2: Atkinson P-V ============
e = 17.0
v3a = v2; v4a = e*v3a
P3a = P1*e**K; T3a = P3a*v3a/R
P4a = P1; T4a = P4a*v4a/R
fig, ax = plt.subplots(figsize=(8,5.5))
vc,Pc = isentrope(v1,v2,P1); ax.plot(vc,Pc,label='1-2 isentropic compression')
ax.plot([v2,v3a],[P2,P3a],label='2-3 const-v heat addition')
ve,Pe = isentrope(v3a,v4a,P3a); ax.plot(ve,Pe,label='3-4 isentropic expansion')
ax.plot([v4a,v1],[P4a,P1],label='4-1 const-p heat rejection')
ax.set_xlabel('Specific Volume  v (m$^3$/kg)')
ax.set_ylabel('Pressure  P (kPa)')
ax.set_title('Ideal Atkinson Cycle P-V Diagram')
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/fig2_atkinson_pv.png', dpi=150); plt.close()

# ============ FIG 3: mass flow vs rpm ============
Vd=1.298e-3; eta_v=0.9; rho_a=100e3/(287*300)
N = np.linspace(750,6500,200)
mdot = eta_v*rho_a*Vd*(N/60)/2*1000
fig, ax = plt.subplots(figsize=(8,4.8))
ax.plot(N,mdot,lw=2)
ax.fill_between(N,mdot,alpha=0.15)
ax.set_xlabel('Engine Speed  (rpm)'); ax.set_ylabel('Mass Flow Rate  (g/s)')
ax.set_title('(a) Intake Air Mass Flow Rate vs Engine Speed')
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/fig3_mdot_rpm.png', dpi=150); plt.close()

# ============ FIG 4: vehicle speed vs rpm per gear ============
gears={1:3.545,2:1.904,3:1.233,4:0.918,5:0.732}; i_f=4.312
D=(14*25.4+2*0.65*175)/1000; Ct=np.pi*D
fig, ax = plt.subplots(figsize=(8,4.8))
for g,ig in gears.items():
    V = (N/(ig*i_f))*Ct/60*3.6
    ax.plot(N,V,label=f'Gear {g} (i={ig})')
ax.axvline(6000,ls='--',color='grey',label='Redline (6000 rpm)')
ax.set_xlabel('Engine Speed  (rpm)'); ax.set_ylabel('Vehicle Speed  (km/h)')
ax.set_title('(b) Vehicle Speed vs Engine Speed per Gear')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/fig4_speed_gear.png', dpi=150); plt.close()

# ============ FIG 5: valve lift ============
Lmax=8.0
IVO,IVC=345,585; EVO,EVC=130,375
th=np.linspace(0,720,1441)
def lift(t,o,c):
    L=np.zeros_like(t); m=(t>=o)&(t<=c)
    L[m]=Lmax*np.sin(np.pi*(t[m]-o)/(c-o)); return L
Li=lift(th,IVO,IVC); Le=lift(th,EVO,EVC)
fig, ax = plt.subplots(figsize=(9,4.8))
ax.plot(th,Li,label='Intake Valve Lift')
ax.plot(th,Le,label='Exhaust Valve Lift')
ax.axvspan(IVO,EVC,alpha=0.2,color='green',label='Valve Overlap')
for x,t in [(EVO,'EVO'),(IVO,'IVO'),(EVC,'EVC'),(IVC,'IVC')]:
    ax.axvline(x,ls='--',alpha=0.5)
ax.set_xlabel('Crankshaft Angle (degree)'); ax.set_ylabel('Valve Lift (mm)')
ax.set_title('Intake and Exhaust Valve Lift vs Crankshaft Angle')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/fig5_valve_lift.png', dpi=150); plt.close()

# ============ FIG 6 & 7: Vt and mdot vs Pu ============
Kc,Rc,cpc=1.4,287.0,1005.0
Pt=105e3; Tu=300.0
crit=((Kc+1)/2)**(Kc/(Kc-1)); Pu_crit=Pt*crit
Tt_s=2*Tu/(Kc+1); Vt_s=np.sqrt(Kc*Rc*Tt_s)
At=3e-4
Pu=np.linspace(106e3,400e3,400)
Vt=np.where(Pu<=Pu_crit, np.sqrt(2*cpc*Tu*(1-(Pt/np.clip(Pu,Pt+1,None))**((Kc-1)/Kc))), Vt_s)
def md(Pu):
    out=np.empty_like(Pu)
    for i,p in enumerate(Pu):
        if p<=Pu_crit:
            pr=Pt/p
            out[i]=At*p*np.sqrt((2/(Rc*Tu))*pr**(2/Kc)*(Kc/(Kc-1))*(1-pr**((Kc-1)/Kc)))
        else:
            out[i]=At*p*np.sqrt((Kc/(Rc*Tu))*(2/(Kc+1))**((Kc+1)/(Kc-1)))
    return out
mdot2=md(Pu)

fig, ax = plt.subplots(figsize=(8.5,5))
ax.plot(Pu/1000,Vt,'r',lw=2,label='Throat Velocity $V_t$')
ax.axvline(Pu_crit/1000,ls='--',color='k',label=f'Critical Pressure = {Pu_crit/1000:.1f} kPa')
ax.axvspan(Pu[0]/1000,Pu_crit/1000,alpha=0.15,color='green',label='Subsonic Region')
ax.axvspan(Pu_crit/1000,Pu[-1]/1000,alpha=0.15,color='red',label='Sonic / Choked Region')
ax.set_xlabel('Upstream Pressure $P_u$ (kPa)'); ax.set_ylabel('Throat Velocity $V_t$ (m/s)')
ax.set_title('Throat Velocity vs Upstream Pressure ($P_t$=105 kPa, $T_u$=300 K)')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/fig6_Vt_Pu.png', dpi=150); plt.close()

fig, ax = plt.subplots(figsize=(8.5,5))
ax.plot(Pu/1000,mdot2,color='purple',lw=2,label='Mass Flow Rate $\\dot m$')
ax.axvline(Pu_crit/1000,ls='--',color='k',label=f'Critical Pressure = {Pu_crit/1000:.1f} kPa')
ax.axvspan(Pu[0]/1000,Pu_crit/1000,alpha=0.15,color='green',label='Subsonic Region')
ax.axvspan(Pu_crit/1000,Pu[-1]/1000,alpha=0.15,color='red',label='Sonic Region')
ax.set_xlabel('Upstream Pressure $P_u$ (kPa)'); ax.set_ylabel('Mass Flow Rate $\\dot m$ (kg/s)')
ax.set_title('Mass Flow Rate vs Upstream Pressure')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/fig7_mdot_Pu.png', dpi=150); plt.close()

# ============ FIG 8: NOx bar ============
names=['Otto','Dual','Diesel','Atkinson']
nox=[7945.05,180.61,23.28,1e-6]
fig, ax = plt.subplots(figsize=(7.5,5))
ax.bar(names,nox,color=['#1f77b4','#ff7f0e','#2ca02c','#d62728'])
ax.set_yscale('log'); ax.set_ylabel('NOx (ppm, log scale)')
ax.set_title('Thermal NOx by Cycle (Zeldovich initial-rate estimate)')
for i,v in enumerate(nox):
    ax.text(i, v*1.3, f'{v:.1f}' if v>1e-3 else '~0', ha='center', fontsize=9)
ax.grid(alpha=0.3, axis='y')
fig.tight_layout(); fig.savefig(f'{OUT}/fig8_nox.png', dpi=150); plt.close()

print("All figures generated:")
for f in sorted(os.listdir(OUT)):
    print("  ", f)
