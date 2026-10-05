"""Generate alt_R3.pdf: h-parameter solution of RE3 (RL not included in A)."""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph

import re3_solution as r

ss = getSampleStyleSheet()
H = ParagraphStyle("H", parent=ss["Heading2"], spaceBefore=10)
T = ss["BodyText"]


def p(txt, st=T):
    return Paragraph(txt, st)


el = [
    p("RE3 - Stability of a differential amplifier with feedback: h-parameter solution", ss["Title"]),
    p("Data: A<sub>1</sub> = 8000, R<sub>id</sub> = 10 k&Omega;, R<sub>o</sub> = 5 k&Omega;, R<sub>1</sub> = 40 k&Omega;, "
      "R<sub>2</sub> = 10 k&Omega;. R<sub>L</sub> = 100 k&Omega; is <b>not</b> included in A."),

    p("a) Topology", H),
    p("Series-parallel (voltage-voltage) feedback. The output voltage is sampled and the input voltages are compared; "
      "the stabilized parameter is the voltage gain."),

    p("b) Matrices of A and &beta;", H),
    p("H<sub>A</sub> = [[R<sub>id</sub>, 0], [-A<sub>1</sub>R<sub>id</sub>/R<sub>o</sub>, 1/R<sub>o</sub>]] = "
      "[[10 k&Omega;, 0], [-16000, 2&times;10<super>-4</super> S]]"),
    p("H<sub>&beta;</sub> = [[R<sub>1</sub>//R<sub>2</sub>, R<sub>2</sub>/(R<sub>1</sub>+R<sub>2</sub>)], "
      "[-R<sub>2</sub>/(R<sub>1</sub>+R<sub>2</sub>), 1/(R<sub>1</sub>+R<sub>2</sub>)]] = "
      "[[8 k&Omega;, 0.2], [-0.2, 2&times;10<super>-5</super> S]]"),
    p("H = H<sub>A</sub> + H<sub>&beta;</sub> = [[%.0f &Omega;, %.2f], [%.1f, %.3g S]], det H = %.2f"
      % (r.H11, r.H12, r.H21, r.H22, r.detH)),

    p("c) Blocks A' and &beta;'", H),
    p("A' = -h<sub>21</sub>/(h<sub>11</sub>h<sub>22</sub>) (with H) = -(%.1f)/(%.0f &times; %.3g) = <b>%.1f</b>"
      % (r.H21, r.H11, r.H22, r.Ap)),
    p("&beta;' = h<sub>12</sub> = <b>%.2f</b>" % r.Bp),
    p("A'&beta;' = %.1f (%.1f dB)" % (r.Ap * r.Bp, 20 * math.log10(r.Ap * r.Bp))),

    p("d) Voltage gain and output impedance", H),
    p("A<sub>f</sub> = V<sub>o</sub>/V<sub>i</sub> = -h<sub>21</sub>/det H = <b>%.4f</b> (about 1/&beta;' = %.2f)"
      % (r.Af, 1 / r.Bp)),
    p("Z<sub>i</sub> = det H/h<sub>22</sub> = <b>%.2f M&Omega;</b>" % (r.Zi / 1e6)),
    p("Z<sub>o</sub> = h<sub>11</sub>/det H = <b>%.2f &Omega;</b> (PDF: 5.6 &Omega;)" % r.Zo),

    p("e) Dominant pole and phase margin", H),
    p("Pole from f<sub>p2</sub>/(A'&beta;') = 10 MHz / %.1f = <b>%.2f kHz</b>. With this pole the crossover is "
      "%.2f MHz and PM = %.1f&deg;." % (r.Ap * r.Bp, r.fp1_e / 1e3, r.fu_e / 1e6, r.pm_e)),
    p("Numerical solution for PM = 45&deg;: f<sub>p1</sub>' = <b>%.2f kHz</b>, crossover %.2f MHz. "
      "The loop has two poles, so the phase reaches -180&deg; only at infinity. The gain at 100 MHz gives "
      "GM = <b>%.1f dB</b>." % (r.fp1_45 / 1e3, r.fu_45 / 1e6, r.gm_45)),

    p("Notes", H),
    p("- Including R<sub>L</sub> in A (h<sub>22A</sub> = 1/R<sub>o</sub> + 1/R<sub>L</sub> = 2.1&times;10<super>-4</super> S) "
      "gives H<sub>22</sub> = 2.3&times;10<super>-4</super> S and <b>A' = 3865</b>, the value in RE3.pdf. "
      "The PDF's A' therefore includes R<sub>L</sub> in A, which explains the difference from the 4040 found here "
      "with R<sub>L</sub> excluded. RL is not added to h<sub>22A</sub>: the load is applied afterwards as a divider, "
      "V<sub>o</sub>/V<sub>i</sub> (with R<sub>L</sub>) = A<sub>f</sub> &middot; R<sub>L</sub>/(R<sub>L</sub>+Z<sub>o</sub>) = "
      "%.4f &times; %.5f = %.4f." % (r.Af, r.RL/(r.RL+r.Zo), r.Af*r.RL/(r.RL+r.Zo))),
    p("- The 134 dB gain quoted in e) is not consistent with A<sub>1</sub> = 8000 (78 dB). With the requested formula "
      "f<sub>p2</sub>/(A'&beta;') and A' = 4040, the loop gain is 808 (58.1 dB)."),
]

SimpleDocTemplate("alt_R3.pdf", pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=2 * cm,
                  title="RE3 h-parameter solution").build(el)
print("wrote alt_R3.pdf")
