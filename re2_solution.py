"""RE2 - stability of an inverting OPAMP feedback amplifier, solved numerically.

A(s) = A0 / ((1 + s/wp1)(1 + s/wp2)), beta = R1/(R1+R2).
Ideal OPAMP (infinite Ri, zero Ro): RL does not load the loop, so it is not used.
"""
import numpy as np
from scipy.optimize import brentq

A0 = 1e6
fp1 = 1e5             # Hz  (wp1 = 2*pi*1e5 rad/s)
fp2 = 1e7             # Hz  (wp2 = 2*pi*1e7 rad/s)
R1, R2 = 1e3, 100e3
beta = R1 / (R1 + R2)            # 0.0099 (RE2.pdf prints 0.1)
Lmid = A0 * beta                 # mid-band loop gain, 79.9 dB

f = np.logspace(-2, 9, 2_000_001)


def T(f, poles):
    """Loop gain Lmid / prod(1 + j f/fk) for the list of pole frequencies."""
    out = np.full(f.shape, Lmid, dtype=complex)
    for fk in poles:
        out /= (1 + 1j * f / fk)
    return out


def phase_deg(f, poles):
    return np.degrees(np.unwrap(np.angle(T(f, poles))))


def margins(poles):
    """Crossover fu (last |T| = 1 crossing), phase margin, first phase crossover fpc, gain margin."""
    t = T(f, poles)
    mag = np.abs(t)
    ph = np.degrees(np.unwrap(np.angle(t)))
    idx = np.where(np.diff(np.sign(mag - 1)) != 0)[0]
    fu = f[idx[-1]] if len(idx) else np.nan
    pm = 180 + np.interp(np.log10(fu), np.log10(f), ph) if len(idx) else np.nan
    jdx = np.where(ph <= -180)[0]
    if len(jdx):
        fpc = f[jdx[0]]
        gm = -20 * np.log10(np.interp(np.log10(fpc), np.log10(f), mag))
    else:
        fpc, gm = np.nan, np.inf      # two poles: phase reaches -180 only at infinity
    return fu, pm, fpc, gm


def pm_at(poles):
    return margins(poles)[1]


# --- a) uncompensated -------------------------------------------------------
fu_a, pm_a, fpc_a, gm_a = margins([fp1, fp2])
gm_a100 = -20 * np.log10(abs(T(np.array([100e6]), [fp1, fp2]))[0])

# --- b) displacement of the first pole, PM = 45 deg -------------------------
# solve for the dominant pole fp1' such that PM = 45 deg (a pole-1 shift alone)
fp1_b = brentq(lambda x: pm_at([x, fp2]) - 45, 1e2, 1e5)
fu_b, pm_b, fpc_b, gm_b = margins([fp1_b, fp2])
gm_b100 = -20 * np.log10(abs(T(np.array([100e6]), [fp1_b, fp2]))[0])

# --- c) insertion of an additional pole, PM = 45 deg ------------------------
# keep fp1 and fp2, insert a new pole fpx below them, solve for PM = 45 deg
fpx_c = brentq(lambda x: pm_at([x, fp1, fp2]) - 45, 1e-1, 1e4)
fu_c, pm_c, fpc_c, gm_c = margins([fpx_c, fp1, fp2])
gm_c100 = -20 * np.log10(abs(T(np.array([100e6]), [fpx_c, fp1, fp2]))[0])

if __name__ == "__main__":
    print(f"beta = {beta:.5f} ({20*np.log10(beta):.2f} dB), A0*beta = {Lmid:.0f} ({20*np.log10(Lmid):.2f} dB)")
    print(f"a) uncompensated: fu = {fu_a/1e6:.2f} MHz, PM = {pm_a:.1f} deg, GM at 100 MHz = {gm_a100:.1f} dB")
    print(f"b) fp1' = {fp1_b:.1f} Hz (PM = 45 deg): fu = {fu_b/1e6:.2f} MHz, PM = {pm_b:.1f} deg, "
          f"GM at 100 MHz = {gm_b100:.1f} dB, finite phase crossover: {'none' if np.isnan(fpc_b) else f'{fpc_b/1e6:.2f} MHz'}")
    print(f"c) fpx = {fpx_c:.2f} Hz (PM = 45 deg): fu = {fu_c/1e3:.1f} kHz, PM = {pm_c:.1f} deg, "
          f"GM at 100 MHz = {gm_c100:.1f} dB, finite phase crossover: {'none' if np.isnan(fpc_c) else f'{fpc_c/1e6:.2f} MHz, GM = {gm_c:.1f} dB'}")

# --- asymptotic (straight-line Bode) estimates, then numerical refinement ----
# b) crossover assumed at fp2: the -20 dB/dec line of fp1' meets 0 dB at fp2
fp1_b_asym = fp2 / Lmid                         # 1.01 kHz
pm_b_asym = 180 - 90 - 45                       # pole1 -90 deg, pole2 -45 deg at fu = fp2 -> 45 deg
# the asymptotic value ignores the -3 dB of pole2 at fu = fp2; refine with the exact |Aβ| = 1 condition
fu_b_ref = fp2
fp1_b_ref = fp2 / np.sqrt(Lmid**2 / 2 - 1)     # exact |T(fp2)| = 1 with pole2 magnitude 1/sqrt(2)
# c) crossover assumed at fp1 (pole2 negligible): the -20 dB/dec line of fpx meets 0 dB at fp1
fpx_c_asym = fp1 / Lmid                         # 10.1 Hz
pm_c_asym = 180 - 90 - 45                       # pole1 at fu = fp1 -> 45 deg, pole2 negligible
fpx_c_ref = fpx_c                               # numerical solution (PM = 45 deg exactly)
