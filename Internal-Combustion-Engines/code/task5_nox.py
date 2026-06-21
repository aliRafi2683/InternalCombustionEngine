"""
Task 5 - Thermal NOx estimate using the Zeldovich mechanism.

We use the initial-rate approximation for the rate-limiting step:
    N2 + O -> NO + N    (reaction 1, Heywood 1988)
    k1 = A * exp(-Ta / T)

[O] is estimated using an Arrhenius-style equilibrium scaling, calibrated
so that the Otto cycle gives a physically reasonable value (~0.024 mol/m^3).
This keeps the comparison between cycles consistent and monotonic in T.
"""

import numpy as np

Ru = 8.314    # J/mol.K
A  = 3.8e13   # pre-exponential, cm^3/mol.s  (Heywood)
Ta = 37000.0  # activation temperature, K
dt = 0.002    # residence time at peak conditions (s)

# peak temperatures and pressures from tasks 1-2
cycles = {
    'Otto':     {'T': 2903.99, 'P': 14106.25},
    'Dual':     {'T': 2500.00, 'P':  7234.37},
    'Diesel':   {'T': 2324.87, 'P':  4255.51},
    'Atkinson': {'T': 1086.96, 'P':  5279.93},
}

# total molar concentration from ideal gas, N2 is ~75% of mixture
for name, c in cycles.items():
    c['Ctot'] = (c['P'] * 1000.0) / (Ru * c['T'])
    c['N2']   = 0.75 * c['Ctot']

# O-atom concentration via equilibrium scaling (Ea_O ~ 31000 K)
# calibrated so Otto gives ~0.0238 mol/m^3
EaO = 31000.0
ref = cycles['Otto']
cal = 0.0238 / np.exp(-EaO / ref['T'])

for name, c in cycles.items():
    c['O'] = cal * np.exp(-EaO / c['T'])

print(f"{'cycle':>9}{'T(K)':>9}{'Ctot':>9}{'[N2]':>9}{'[O]':>9}{'k1':>11}{'NOx(ppm)':>11}")
for name, c in cycles.items():
    k1    = A * np.exp(-Ta / c['T'])     # cm^3/mol.s
    k1_si = k1 * 1e-6                    # convert to m^3/mol.s
    dNO   = 2 * k1_si * c['N2'] * c['O'] * dt   # mol/m^3 produced
    NOx_ppm = dNO / c['Ctot'] * 1e6
    c['NOx'] = NOx_ppm
    print(f"{name:>9}{c['T']:>9.1f}{c['Ctot']:>9.1f}{c['N2']:>9.1f}"
          f"{c['O']:>9.4f}{k1_si:>11.3e}{NOx_ppm:>11.2f}")
