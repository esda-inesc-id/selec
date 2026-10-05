"""RE3 - stability of a series-parallel (voltage-voltage) feedback amplifier, h-parameters.

A (no RL): h11 = Rid, h12 = 0, h21 = -A1*Rid/Ro, h22 = 1/Ro.
beta:      h11 = R1//R2, h12 = R2/(R1+R2), h21 = -R2/(R1+R2), h22 = 1/(R1+R2).
H = hA + hB (sum of the two-port matrices).
"""
import numpy as np
from scipy.optimize import brentq

A1 = 8000.0
Rid, Ro = 10e3, 5e3
R1, R2 = 40e3, 10e3
RL = 100e3                      # not included in A, as requested
fp1, fp2 = 1e6, 10e6            # Hz
A0_dB = 134.0                   # stated open-loop gain of the amplifier (not used in the h-model)

# --- b) matrices --------------------------------------------------------------
hA = np.array([[Rid, 0.0], [-A1 * Rid / Ro, 1 / Ro]])
hB = np.array([[R1 * R2 / (R1 + R2), R2 / (R1 + R2)], [-R2 / (R1 + R2), 1 / (R1 + R2)]])
H = hA + hB
H11, H12, H21, H22 = H[0, 0], H[0, 1], H[1, 0], H[1, 1]
detH = np.linalg.det(H)

# --- c) blocks A' and beta' ---------------------------------------------------
Ap = -H21 / (H11 * H22)         # loaded amplifier, A' = -h21/(h11 h22) with H = hA + hB
Bp = H12                        # beta' = h12

# --- d) feedback results -------------------------------------------------------
Af = -H21 / detH                # Vo/Vi
Zi = detH / H22                 # input impedance, output open
Zo = H11 / detH                 # output impedance, input shorted

# --- e) dominant pole from fp2/(A' beta') -------------------------------------
fp1_e = fp2 / (Ap * Bp)
T_loop = lambda f, fa: (Ap * Bp) / ((1 + 1j * f / fa) * (1 + 1j * f / fp2))
f = np.logspace(0, 9, 900001)


def margins(fa):
    t = T_loop(f, fa)
    mag = np.abs(t)
    ph = np.degrees(np.unwrap(np.angle(t)))
    idx = np.where(np.diff(np.sign(mag - 1)) != 0)[0]
    fu = f[idx[-1]] if len(idx) else np.nan
    pm = 180 + np.interp(np.log10(fu), np.log10(f), ph) if len(idx) else np.nan
    return fu, pm


def pm_at(fa):
    return margins(fa)[1]


fu_e, pm_e = margins(fp1_e)
fp1_45 = brentq(lambda x: pm_at(x) - 45, 1e0, 1e6)   # PM = 45 deg exactly
fu_45, pm_45 = margins(fp1_45)
gm_45 = -20 * np.log10(abs(T_loop(np.array([100e6]), fp1_45)[0]))   # two poles: read at 100 MHz

if __name__ == "__main__":
    print("H =\n", H)
    print(f"det H = {detH:.2f}")
    print(f"A' = {Ap:.1f}, B' = beta' = {Bp:.3f}, A'B' = {Ap*Bp:.1f} ({20*np.log10(Ap*Bp):.1f} dB)")
    print(f"Af = Vo/Vi = {Af:.4f}  (1/beta' = {1/Bp:.2f})")
    print(f"Zi = detH/h22 = {Zi/1e6:.2f} Mohm")
    print(f"Zo = h11/detH = {Zo:.2f} ohm")
    print(f"e) fp1' = fp2/(A'B') = {fp1_e/1e3:.2f} kHz: fu = {fu_e/1e6:.2f} MHz, PM = {pm_e:.1f} deg")
    print(f"   PM = 45 deg: fp1' = {fp1_45/1e3:.2f} kHz, fu = {fu_45/1e6:.2f} MHz, GM at 100 MHz = {gm_45:.1f} dB")
