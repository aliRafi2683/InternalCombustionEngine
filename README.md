# Internal Combustion Engines — Comparative Analysis of Dual, Otto, Diesel, and Atkinson Cycles

Course project for **Internal Combustion Engines** (AmirKabir University of Technology / Tehran Polytechnic), Spring 2026.

This repository contains an independent thermodynamic analysis of four ideal air-standard
engine cycles plus supporting engine-performance studies, all implemented in Python.

## Problem
Dual cycle with pressure ratio α = 1.7, cut-off at 5% of stroke, inlet 100 kPa / 300 K,
compression-ratio range 12–18, and a max-temperature constraint of 2500 K.

## Tasks
1. **Task 1** — Optimal compression ratio for the Dual cycle; performance of Otto and Diesel at the same CR and heat input; comparative P–V diagram.
2. **Task 2** — Atkinson cycle (CR = 14.57, expansion ratio = 17): work, efficiency, heat input, P–V diagram, comparison, and practical applications.
3. **Task 3** — Toyota 2NZ-FE: intake-air mass flow rate (η_v = 0.9) and vehicle speed across gears.
4. **Task 4** — Valve-lift profiles (intake/exhaust) and compressible flow: throat velocity and mass flow rate vs upstream pressure, with sonic/subsonic regions.
5. **Task 5** — NOx emissions via the Zeldovich mechanism for all four cycles.

## Key results
| Cycle | Efficiency η | Peak T (K) | Peak P (kPa) | NOx (ppm) |
|-------|------:|------:|------:|------:|
| Otto | 0.658 | 2904 | 14106 | ~7945 |
| Dual | 0.629 | 2500 | 7234 | ~181 |
| Diesel | 0.568 | 2325 | 4256 | ~23 |
| Atkinson | 0.668 | 1087 | 5280 | ~0 |

Optimal Dual-cycle compression ratio: **r = 14.57** (peak T = 2500 K, Q_in ≈ 1456 kJ/kg).

## Repository layout
```
code/        Python source for each task + figure generator
figures/     Generated PNG figures
report/      Final report (Persian, .docx and .pdf)
README.md
requirements.txt
```

## Running
```bash
pip install -r requirements.txt
python code/task1_cycles.py
python code/task2_atkinson.py
python code/task3_vehicle.py
python code/task4_valve_flow.py
python code/task5_nox.py
python code/make_figures.py      # writes all figures into figures/
```

## Notes on method
- Air-standard, cold-air assumptions with constant specific heats (k = 1.4).
- "Same heat input" is enforced across Otto/Dual/Diesel, so the Diesel cut-off ratio (and hence its efficiency) follows from the shared Q_in rather than from the Dual-cycle geometry.
- The choked throat velocity is evaluated at the throat **static** temperature (T_t = 250 K → 316.9 m/s), not the upstream stagnation temperature.

All code was written and verified independently.
