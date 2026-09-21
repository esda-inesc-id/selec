# select2627

Alternative resolutions of feedback-amplifier exercises (Feedback and stability),
solved with the two-port sum S = A + B (feedforward + feedback y-matrices).

## Method

- Closed-loop gain: `v2/i1 = -S21/det(S)` (Rg and Rl excluded at first).
- Input impedance: `Zi = S22/det(S)`; output impedance: `Zo = S11g/det(S_g)` (Rg included, Rl = inf).
- Voltage gain: `Vl/Vs = (v2/i1) / (Rg + Zi)`.
- With `S11g = S11 + 1/Rg` (`S_g` = S with S11g), the one-way gains are:
  `A' = -S21/(S11g*S22)`, `beta' = S12`.

## Files

| File | Purpose |
|---|---|
| `R0.pdf`, `R1.pdf` | Original exercises and resolutions |
| `re1_solution.py` | RE1 (BJT shunt-shunt feedback amplifier) calculation; prints the results |
| `re1_pdf.py` | Builds `alt_R0_R1.pdf` from `re1_solution.py`, following questions a) to e) |
| `alt_R0_R1.pdf` | Generated alternative resolution |

New exercises: add `reN_solution.py` and `reN_pdf.py` next to these.

## Usage

    python3 re1_solution.py   # print results
    python3 re1_pdf.py        # write alt_R0_R1.pdf (needs reportlab, numpy)

## RE1 results (gm = Ic/VT = 570.6 mS, rpi = 350.5 ohm)

| Quantity | Value |
|---|---|
| A' / beta' | -43.9 kohm / -20 uS |
| Vo/Vs | -23.39 |
| Zi / Zo | 159.3 ohm / 158.7 ohm |
| fLf / fHf | 266 Hz / 751 kHz |

## Errors in the original R1.pdf

- gm is printed as 584 mS; 14.26 mA / 25 mV = 570.6 mS.
- Rpi is printed as 542.5 ohm; beta0/gm = 350.5 ohm (later numbers use 342.5 ohm).
- Hence A' = 44.7 kohm, Af = Kv = -23.6, Zi = 154.8 ohm, Zo = 157.5 ohm are slightly off.
- fHf = 1364 kHz is wrong: fH(1 + A'0 beta') = 751 kHz.
