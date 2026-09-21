"""Generate alt_R0_R1.pdf: alternative resolution of RE1 using S = A + B,
following the order of the questions a) to e)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

import re1_solution as r

S, det = r.S, r.det
ss = getSampleStyleSheet()
H = ParagraphStyle("H", parent=ss["Heading2"], spaceBefore=10)
T = ss["BodyText"]


def p(txt, st=T):
    return Paragraph(txt, st)


def matrix(rows):
    t = Table([[Paragraph(c, T) for c in row] for row in rows], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 1, colors.black),
                           ("LINEAFTER", (-1, 0), (-1, -1), 1, colors.black)]))
    return t


Ap_b = r.Ap / (1 + r.Ap * r.bp)
el = [
    p("RE1 - Alternative resolution: closed loop with S = A + B", ss["Title"]),
    p("Data: I<sub>C</sub> = %.2f mA, g<sub>m</sub> = %.0f mS, r<sub>&pi;</sub> = %.1f &Omega;, "
      "R<sub>f</sub> = 50 k&Omega;, R<sub>C</sub> = 300 &Omega;, R<sub>g</sub> = 1 k&Omega;, "
      "r<sub>o</sub> = &infin;." % (r.Ic * 1e3, r.gm * 1e3, r.rpi)),

    p("a) Topology and models of A and &beta;", H),
    p("A senses the output voltage and subtracts input currents: <b>parallel-parallel</b> "
      "(current-voltage, transimpedance amplifier). Common variables v<sub>1</sub>, v<sub>2</sub>, "
      "so both blocks are represented by the admittance matrix."),
    p("A ="), matrix([["1/r<sub>&pi;</sub>", "0"], ["g<sub>m</sub>", "1/R<sub>C</sub>"]]),
    p("&beta; (shunt R<sub>f</sub>) ="),
    matrix([["1/R<sub>f</sub>", "-1/R<sub>f</sub>"], ["-1/R<sub>f</sub>", "1/R<sub>f</sub>"]]),

    p("b) Gains A' and &beta;'", H),
    p("Loading A with R<sub>g</sub> and &beta; (S = A + B, S<sub>11g</sub> = S<sub>11</sub> + 1/R<sub>g</sub>):"),
    p("A' = -S<sub>21</sub> / (S<sub>11g</sub> S<sub>22</sub>) = "
      "-(g<sub>m</sub> - 1/R<sub>f</sub>) / [(1/r<sub>&pi;</sub>+1/R<sub>f</sub>+1/R<sub>g</sub>)(1/R<sub>C</sub>+1/R<sub>f</sub>)]"
      " = <b>%.1f k&Omega;</b>" % (r.Ap / 1e3)),
    p("&beta;' = S<sub>12</sub> = -1/R<sub>f</sub> = <b>-20 &mu;S</b>"),
    p("Consistency: A'/(1+A'&beta;') = -S<sub>21</sub> / (S<sub>11g</sub>S<sub>22</sub> - S<sub>12</sub>S<sub>21</sub>) "
      "= -S<sub>21</sub>/det S<sub>g</sub>."),
    p("1 + A'&beta;' = %.3f" % r.D),

    p("c) V<sub>o</sub>/V<sub>s</sub>", H),
    p("Feedback theory: A<sub>f</sub> = A'/(1+A'&beta;') = %.2f k&Omega;, "
      "K<sub>v</sub> = A<sub>f</sub>/R<sub>g</sub> = <b>%.2f</b>." % (Ap_b / 1e3, Ap_b / r.Rg)),
    p("Same result with S = A + B, R<sub>g</sub> and R<sub>l</sub> excluded (ideal Norton source):"),
    matrix([["1/r<sub>&pi;</sub> + 1/R<sub>f</sub>", "-1/R<sub>f</sub>"],
            ["g<sub>m</sub> - 1/R<sub>f</sub>", "1/R<sub>C</sub> + 1/R<sub>f</sub>"]]),
    Spacer(1, 4),
    p("det S = S<sub>11</sub>S<sub>22</sub> - S<sub>12</sub>S<sub>21</sub> = %.4e S<super>2</super>" % det),
    p("v<sub>2</sub>/i<sub>1</sub> = -S<sub>21</sub>/det S = %.2f k&Omega; "
      "(magnitude S<sub>21</sub>/det S, minus sign = inversion)" % (r.T / 1e3)),
    p("K<sub>v</sub> = (v<sub>2</sub>/i<sub>1</sub>)/(R<sub>g</sub> + Z<sub>i</sub>) = "
      "%.2f k&Omega; / (1 k&Omega; + %.1f &Omega;) = <b>%.2f</b>" % (r.T / 1e3, r.Zi, r.Kv)),
    p("Check with R<sub>g</sub> included in S<sub>11</sub> from the start: K<sub>v</sub> = %.2f." % r.Kv_check),

    p("d) Z<sub>i</sub> and Z<sub>o</sub>", H),
    p("Z<sub>i</sub> = S<sub>22</sub>/det S (R<sub>g</sub> excluded) = <b>%.1f &Omega;</b> " % r.Zi),
    p("Z<sub>o</sub> = S<sub>11g</sub>/det S<sub>g</sub> with R<sub>g</sub> included, R<sub>l</sub> = &infin; = "
      "<b>%.1f &Omega;</b>" % r.Zo),

    p("e) Frequency responses", H),
    p("Basic amplifier: f<sub>L</sub> = 500 Hz, f<sub>H</sub> = 400 kHz, mid-band |A'<sub>0</sub>| = "
      "%.1f k&Omega;. With feedback the mid-band gain drops to %.2f k&Omega; and"
      % (abs(r.Ap) / 1e3, abs(Ap_b) / 1e3)),
    p("f<sub>Lf</sub> = f<sub>L</sub>/(1+A'<sub>0</sub>&beta;') = <b>%.0f Hz</b>, "
      "f<sub>Hf</sub> = f<sub>H</sub>(1+A'<sub>0</sub>&beta;') = <b>%.0f kHz</b>."
      % (r.fLf, r.fHf / 1e3)),
    p("Bandwidth: %.1f kHz without feedback, %.1f kHz with feedback."
      % ((r.fH - r.fL) / 1e3, (r.fHf - r.fLf) / 1e3)),

    p("Errors found in the original resolution (R1.pdf)", H),
    p("- g<sub>m</sub> = I<sub>C</sub>/V<sub>T</sub> = 14.26 mA / 25 mV = <b>570.6 mS</b>, not 584 mS as printed "
      "(584 mS would need I<sub>C</sub> = 14.6 mA)."),
    p("- R<sub>&pi;</sub> = &beta;<sub>0</sub>/g<sub>m</sub> = 200/0.5706 = <b>350.5 &Omega;</b>, not 542.5 &Omega; "
      "as printed. The later numbers in R1.pdf (e.g. Z<sub>iA'</sub> = 253.8 &Omega;) were obtained with "
      "342.5 &Omega; (= 200/0.584), so they follow neither the printed r<sub>&pi;</sub> nor the correct one."),
    p("- Because of the wrong g<sub>m</sub>/r<sub>&pi;</sub>, R1.pdf gives A' = 44.7 k&Omega; (correct: %.1f k&Omega;), "
      "A<sub>f</sub> = K<sub>v</sub> = -23.6 (correct: %.2f), Z<sub>i</sub> = 154.8 &Omega; (correct: %.1f &Omega;), "
      "Z<sub>o</sub> = 157.5 &Omega; (correct: %.1f &Omega;)." % (abs(r.Ap)/1e3, r.Kv, r.Zi, r.Zo)),
    p("- f<sub>Hf</sub> = 1364 kHz in R1.pdf is wrong: f<sub>H</sub>(1+A'<sub>0</sub>&beta;') = 400 kHz x %.3f = "
      "<b>%.0f kHz</b> (even with its own 1 + A'<sub>0</sub>&beta;' = 1.894 the result would be 757.6 kHz)." % (r.D, r.fHf/1e3)),
]

SimpleDocTemplate("alt_R0_R1.pdf", pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=2 * cm,
                  title="RE1 alternative resolution").build(el)
print("wrote alt_R0_R1.pdf")
