"""
Task 1 - Comparing Dual, Otto, and Diesel air-standard cycles.

The idea is to fix the dual cycle parameters (pressure ratio, cut-off fraction, CR),
then run Otto and Diesel with the same compression ratio and same total heat input
to compare efficiencies fairly.
"""

import numpy as np

# air properties - cold air standard, constant specific heats
k  = 1.4
cp = 1.005   # kJ/kg.K
cv = 0.718
R  = cp - cv  # 0.287 kJ/kg.K

# initial conditions
P1 = 100.0  # kPa
T1 = 300.0  # K

# dual cycle parameters
alpha  = 1.7   # pressure ratio at constant-volume step (P3/P2)
cutoff = 0.05  # fraction of stroke where constant-pressure heat addition ends
T_limit = 2500.0  # max allowed temperature (K)


def dual_cycle(r):
    # state 1
    v1 = R * T1 / P1
    v2 = v1 / r

    # isentropic compression 1->2
    T2 = T1 * r**(k - 1)
    P2 = P1 * r**k

    # constant-volume heat addition 2->3
    v3 = v2
    P3 = alpha * P2
    T3 = T2 * alpha

    # constant-pressure heat addition 3->4 (cut-off 5% of stroke)
    v4 = v3 + cutoff * (v1 - v2)
    P4 = P3
    T4 = T3 * (v4 / v3)

    # isentropic expansion back to v1
    v5 = v1
    T5 = T4 * (v4 / v5)**(k - 1)
    P5 = P4 * (v4 / v5)**k

    q_in  = cv * (T3 - T2) + cp * (T4 - T3)
    q_out = cv * (T5 - T1)
    w_net = q_in - q_out
    eta   = w_net / q_in

    return dict(v1=v1, v2=v2, v3=v3, v4=v4, v5=v5,
                P1=P1, P2=P2, P3=P3, P4=P4, P5=P5,
                T1=T1, T2=T2, T3=T3, T4=T4, T5=T5,
                q23=cv*(T3-T2), q34=cp*(T4-T3),
                q_in=q_in, q_out=q_out, w_net=w_net, eta=eta, Tmax=T4)


# sweep CR from 12 to 18 and find the highest one that keeps Tmax under 2500 K
rs = np.linspace(12, 18, 60001)
best_r, best_gap = None, 1e9

for r in rs:
    s = dual_cycle(r)
    if s['Tmax'] <= T_limit:
        gap = T_limit - s['Tmax']
        if gap < best_gap:
            best_gap = gap
            best_r = r

st = dual_cycle(best_r)

print(f"Optimal CR (dual)         : {best_r:.4f}")
print(f"Max dual-cycle temp T4    : {st['Tmax']:.2f} K")
print(f"Total heat input q_in     : {st['q_in']:.2f} kJ/kg")
print(f"Dual net work             : {st['w_net']:.2f} kJ/kg")
print(f"Dual thermal efficiency   : {st['eta']:.4f}")
print()

print("Dual cycle state table at optimal CR:")
print(f"{'state':>5} {'P(kPa)':>10} {'T(K)':>10} {'v(m3/kg)':>10}")
for i in [1, 2, 3, 4, 5]:
    print(f"{i:>5} {st['P'+str(i)]:>10.2f} {st['T'+str(i)]:>10.2f} {st['v'+str(i)]:>10.4f}")
print()

# reuse some computed values
r  = best_r
v1 = R * T1 / P1
v2 = v1 / r
T2 = T1 * r**(k - 1)
P2 = P1 * r**k
q_in = st['q_in']

# --- Otto cycle at same CR and same total q_in ---
# all heat goes in at constant volume
eta_otto = 1 - 1 / r**(k - 1)
T3o = T2 + q_in / cv
P3o = P2 * (T3o / T2)
T4o = T3o * (1 / r)**(k - 1)
P4o = P3o * (1 / r)**k

print(f"Otto efficiency 1-1/r^(k-1): {eta_otto:.4f}")
print(f"Otto Tmax (T3)            : {T3o:.2f} K")
print(f"Otto Pmax (P3)            : {P3o:.2f} kPa")
print()

# --- Diesel cycle at same CR and same total q_in ---
# all heat goes in at constant pressure
T3d = T2 + q_in / cp
rc  = T3d / T2   # cut-off ratio
eta_diesel = 1 - (1 / r**(k - 1)) * ((rc**k - 1) / (k * (rc - 1)))
v3d = v2 * rc
T4d = T3d * (v3d / v1)**(k - 1)
P4d = P2 * (v3d / v1)**k  # P3d = P2 for diesel

print(f"Diesel cut-off ratio rc   : {rc:.4f}")
print(f"Diesel efficiency         : {eta_diesel:.4f}")
print(f"Diesel Tmax (T3)          : {T3d:.2f} K")
print(f"Diesel Pmax               : {P2:.2f} kPa")
print()

print("Summary efficiencies:")
print(f"  Otto   : {eta_otto:.4f}")
print(f"  Dual   : {st['eta']:.4f}")
print(f"  Diesel : {eta_diesel:.4f}")
