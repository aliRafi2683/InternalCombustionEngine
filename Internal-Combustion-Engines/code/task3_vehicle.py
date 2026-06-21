"""
Task 3 - Toyota 2NZ-FE: air mass flow and vehicle speed per gear.

Engine specs: 1.298 L displacement, 4-cylinder, 5-speed manual gearbox.
Tyre size: 175/65 R14.
"""

import numpy as np

# ambient air density at intake conditions
P_atm = 100.0e3  # Pa
T_atm = 300.0    # K
R_air = 287.0    # J/kg.K
rho_a = P_atm / (R_air * T_atm)

Vd    = 1.298e-3  # total displacement in m^3
eta_v = 0.9       # volumetric efficiency

def mdot_air(N_rpm):
    # 4-stroke engine: one intake stroke every 2 revolutions
    Vdot = Vd * (N_rpm / 60.0) / 2.0
    return eta_v * rho_a * Vdot

print(f"rho_a = {rho_a:.4f} kg/m^3")
for N in [750, 3000, 6000]:
    m = mdot_air(N)
    print(f"  N={N:>4} rpm -> mdot_air = {m*1000:.2f} g/s = {m:.4f} kg/s")
print()

# tyre geometry: 175/65 R14
# section width = 175 mm, aspect ratio = 65% => sidewall height = 0.65 * 175
sidewall = 0.65 * 175.0        # mm
D        = 14 * 25.4 + 2 * sidewall  # overall diameter in mm
D_m      = D / 1000.0
C_t      = np.pi * D_m        # rolling circumference in m

print(f"Tyre diameter D = {D_m:.4f} m, circumference C_t = {C_t:.4f} m")

# gearbox ratios (C50 5-speed) and final drive
gears = {1: 3.545, 2: 1.904, 3: 1.233, 4: 0.918, 5: 0.732}
i_f   = 4.312

def vehicle_speed(N_rpm, ig):
    n_wheel = N_rpm / (ig * i_f)   # wheel speed in rev/min
    v_mps   = n_wheel * C_t / 60.0
    return v_mps * 3.6              # convert to km/h

N = 3000
print(f"\nVehicle speed at {N} rpm:")
print(f"{'gear':>5}{'ratio':>8}{'V(km/h)':>10}")
for g, ig in gears.items():
    print(f"{g:>5}{ig:>8.3f}{vehicle_speed(N, ig):>10.2f}")
