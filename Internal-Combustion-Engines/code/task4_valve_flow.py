"""
Task 4 - Valve lift profile and compressible flow through the intake throat.

Part A: sinusoidal model for intake and exhaust valve lift vs crank angle.
Part B: throat velocity and mass flow rate as upstream pressure increases,
        with a clear transition from subsonic to choked (sonic) flow.
"""

import numpy as np

# ---- Part A: valve timing ----
# all angles in degrees of crank rotation (0-720 = one full 4-stroke cycle)
IVO = 345.0  # intake valve opens  (15 deg BTDC)
IVC = 585.0  # intake valve closes (45 deg ABDC)
EVO = 130.0  # exhaust valve opens (50 deg BBDC)
EVC = 375.0  # exhaust valve closes (15 deg ATDC)

overlap = EVC - IVO
print(f"Valve overlap = {overlap:.0f} deg")
print(f"Intake max lift at {(IVO+IVC)/2:.1f} deg, exhaust max lift at {(EVO+EVC)/2:.1f} deg")

# ---- Part B: compressible flow through a fixed throat ----
k   = 1.4
R   = 287.0   # J/kg.K
cp  = 1005.0  # J/kg.K

Pt  = 105e3   # throat static pressure (Pa)
Tu  = 300.0   # upstream stagnation temperature (K)
At  = 3e-4    # throat area (m^2)

# critical upstream pressure at which flow chokes
crit_ratio = ((k + 1) / 2)**(k / (k - 1))
Pu_crit    = Pt * crit_ratio
print(f"\nCritical pressure ratio (Pu/Pt) = {crit_ratio:.4f}")
print(f"Critical upstream pressure Pu   = {Pu_crit/1000:.2f} kPa")

# sonic conditions at the throat
Tt_sonic = 2 * Tu / (k + 1)
Vt_sonic = np.sqrt(k * R * Tt_sonic)
print(f"Choked throat static temp = {Tt_sonic:.2f} K")
print(f"Choked throat velocity Vt = {Vt_sonic:.2f} m/s")


def Vt_of(Pu):
    if Pu <= Pu_crit:
        return np.sqrt(2 * cp * Tu * (1 - (Pt / Pu)**((k - 1) / k)))
    return Vt_sonic   # choked — velocity can't increase further


def mdot_of(Pu):
    if Pu <= Pu_crit:
        pr   = Pt / Pu
        term = (2.0 / (R * Tu)) * pr**(2.0 / k) * (k / (k - 1)) * (1 - pr**((k - 1) / k))
        return At * Pu * np.sqrt(term)
    else:
        # choked: mdot grows linearly with Pu once sonic
        return At * Pu * np.sqrt((k / (R * Tu)) * (2 / (k + 1))**((k + 1) / (k - 1)))


for Pu_k in [110, 150, 198.75, 250, 400]:
    Pu = Pu_k * 1000
    print(f"  Pu={Pu_k:>7.2f} kPa -> Vt={Vt_of(Pu):7.2f} m/s, mdot={mdot_of(Pu):.4f} kg/s")
