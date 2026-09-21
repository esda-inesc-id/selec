"""RE1 - shunt-shunt feedback amplifier, solved with S = A + B (y-parameters).

Rg and Rl are excluded from S (ideal Norton source Is, open output).
Feedback network: shunt Rf (y21_beta = -1/Rf).
"""
import numpy as np

# --- circuit data -----------------------------------------------------------
VCC, VBEon, beta = 10.0, 0.7, 200.0
Rc, Rf, Re, Rg = 300.0, 50e3, 100.0, 1e3
VT = 25e-3

# bias: (Ic + Ic/b) Rc + (Ic/b) Rf + Re (b+1)/b Ic + VBEon = VCC
Ic = (VCC - VBEon) / ((1 + 1 / beta) * Rc + Rf / beta + Re * (beta + 1) / beta)
gm = Ic / VT     # 570.6 mS (the PDF prints 584 mS)
rpi = beta / gm  # 350.5 ohm (the PDF prints 542.5 ohm)

# --- two-port y matrices ----------------------------------------------------
A = np.array([[1 / rpi, 0.0],
              [gm, 1 / Rc]])
B = np.array([[1 / Rf, -1 / Rf],
              [-1 / Rf, 1 / Rf]])
S = A + B
det = np.linalg.det(S)

# --- results without Rg, Rl -------------------------------------------------
T = -S[1, 0] / det      # v2/i1 : closed-loop transimpedance (S21/det, sign = inversion)
Zi = S[1, 1] / det      # input impedance seen by the source branch
Kv = T / (Rg + Zi)      # Vl/Vs

# --- cross-check: Rg included from the start --------------------------------
Sg = S + np.array([[1 / Rg, 0.0], [0.0, 0.0]])
Af = -Sg[1, 0] / np.linalg.det(Sg)      # v2/Is, Is = Vs/Rg
Kv_check = Af / Rg

Zo = Sg[0, 0] / np.linalg.det(Sg)      # output impedance (source off, Rg in, Rl = inf)

# --- feedback-theory cross-check (exact A', beta') --------------------------
Ap = -S[1, 0] / (Sg[0, 0] * S[1, 1])   # -S21 / ((S11 + 1/Rg) S22)
bp = S[0, 1]                            # S12
D = 1 + Ap * bp                  # 1 + A'beta'
fL, fH = 500.0, 400e3
fLf, fHf = fL / D, fH * D

if __name__ == "__main__":
    print(f"Ic  = {Ic*1e3:.2f} mA   gm = {gm*1e3:.1f} mS   rpi = {rpi:.1f} ohm")
    print("S =\n", S, f"\ndet S = {det:.4e}")
    print(f"T  = v2/i1 (no Rg) = {T/1e3:.2f} kohm")
    print(f"Zi (no Rg)         = {Zi:.1f} ohm")
    print(f"Vl/Vs              = {Kv:.2f}")
    print(f"check, Rg included : Af = {Af/1e3:.2f} kohm, Kv = {Kv_check:.2f}")
    print(f"A' = {Ap/1e3:.2f} kohm, beta' = {bp*1e6:.0f} uS, "
          f"A/(1+A beta) = {Ap/(1+Ap*bp)/1e3:.2f} kohm")
    print(f"Zo = {Zo:.1f} ohm, 1+A'b' = {D:.3f}, fLf = {fLf:.0f} Hz, fHf = {fHf/1e3:.0f} kHz")
