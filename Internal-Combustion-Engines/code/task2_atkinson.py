"""
Task 2 - Ideal Atkinson cycle analysis.

Uses the same compression ratio as the other cycles (r = 14.57),
but the expansion ratio is larger (e = 17), which is the whole point
of the Atkinson cycle — expand further than you compressed.

Heat rejection happens at constant pressure (4->1), which lets us
derive state 3 from the condition P4 = P1 working backwards.
"""

import numpy as np

k  = 1.4
cp = 1.005   # kJ/kg.K
cv = 0.718
R  = cp - cv

P1, T1 = 100.0, 300.0  # kPa, K
r = 14.5726  # compression ratio (same as task 1)
e = 17.0     # expansion ratio (v4/v3) - larger than r, hence "over-expansion"

# state 1 and 2
v1 = R * T1 / P1
v2 = v1 / r
T2 = T1 * r**(k - 1)
P2 = P1 * r**k

# v3 = v2 (constant-volume heat addition), v4 = e * v3
v3 = v2
v4 = e * v3

# work backwards from 4->1 being constant pressure:
# P4 = P1, and 3->4 is isentropic => P3 * v3^k = P4 * v4^k => P3 = P1*(v4/v3)^k
P3 = P1 * e**k
T3 = P3 * v3 / R

P4 = P1
T4 = P4 * v4 / R

# energy balance
q_in  = cv * (T3 - T2)   # heat added at constant volume
q_out = cp * (T4 - T1)   # heat rejected at constant pressure
w_net = q_in - q_out
eta   = w_net / q_in

print("Atkinson cycle  (r=14.57, expansion ratio e=17)")
print(f"  v1={v1:.4f}  v2={v2:.4f}  v3={v3:.4f}  v4={v4:.4f}")
print(f"  T1={T1:.2f}  T2={T2:.2f}  T3={T3:.2f}  T4={T4:.2f}")
print(f"  P1={P1:.2f}  P2={P2:.2f}  P3={P3:.2f}  P4={P4:.2f}")
print(f"  q_in ={q_in:.2f} kJ/kg")
print(f"  q_out={q_out:.2f} kJ/kg")
print(f"  w_net={w_net:.2f} kJ/kg")
print(f"  eta  ={eta:.4f}")
