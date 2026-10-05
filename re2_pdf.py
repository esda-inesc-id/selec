"""Generate alt_R2.pdf: numerical solution of RE2 (stability), with the errors of RE2.pdf."""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph

import re2_solution as r

ss = getSampleStyleSheet()
H = ParagraphStyle("H", parent=ss["Heading2"], spaceBefore=10)
T = ss["BodyText"]


def p(txt, st=T):
    return Paragraph(txt, st)


pm_1k = r.pm_at([1e3, r.fp2])          # PM with the printed fp1' = 1 kHz
pm_10 = r.pm_at([10.0, r.fp1, r.fp2])  # PM with the printed fp'' = 10 Hz

el = [
    p("RE2 - Stability of a feedback amplifier: numerical solution", ss["Title"]),
    p("Data: A<sub>0</sub> = 10<super>6</super> (120 dB), f<sub>p1</sub> = 100 kHz, f<sub>p2</sub> = 10 MHz, "
      "R<sub>1</sub> = 1 k&Omega;, R<sub>2</sub> = 100 k&Omega;, R<sub>L</sub> irrelevant (zero R<sub>o</sub>)."),

    p("a) Feedback gain A(s)&beta;", H),
    p("A(s) = A<sub>0</sub> / [(1+s/&omega;<sub>p1</sub>)(1+s/&omega;<sub>p2</sub>)], "
      "&beta; = R<sub>1</sub>/(R<sub>1</sub>+R<sub>2</sub>) = %.5f = %.2f dB."
      % (r.beta, 20 * math.log10(r.beta))),
    p("A&beta; mid-band = %.0f = %.2f dB. Uncompensated: f<sub>u</sub> = %.2f MHz, PM = %.1f&deg;, "
      "gain at 100 MHz = %.1f dB." % (r.Lmid, 20 * math.log10(r.Lmid), r.fu_a / 1e6, r.pm_a, r.gm_a100)),

    p("f<sub>u</sub> is the unity-gain crossover frequency, where |A&beta;| = 1 (0 dB). The phase margin is measured "
      "there: PM = 180&deg; + &angle;A&beta;(f<sub>u</sub>). The gain margin is read at the phase crossover, "
      "where &angle;A&beta; = -180&deg;."),

    p("b) Displacement of the first pole (PM = 45&deg;)", H),
    p("Solving numerically for PM = 45&deg; with f<sub>p2</sub> fixed: "
      "<b>f<sub>p1</sub>' = %.0f Hz</b>, f<sub>u</sub> = %.2f MHz, PM = %.1f&deg;."
      % (r.fp1_b, r.fu_b / 1e6, r.pm_b)),
    p("Gain margin: the loop has two poles, so the phase only reaches -180&deg; at infinity (no finite phase crossover). "
      "Reading the gain at 100 MHz gives GM = <b>%.1f dB</b>." % r.gm_b100),

    p("c) Insertion of an additional pole (PM = 45&deg;)", H),
    p("Solving numerically for PM = 45&deg; with f<sub>p1</sub>, f<sub>p2</sub> kept: "
      "<b>f<sub>x</sub> = %.1f Hz</b>, f<sub>u</sub> = %.1f kHz, PM = %.1f&deg;."
      % (r.fpx_c, r.fu_c / 1e3, r.pm_c)),
    p("Phase reaches -180&deg; at %.2f MHz, where <b>GM = %.1f dB</b>."
      % (r.fpc_c / 1e6, r.gm_c)),

    p("Asymptotic + numerical resolution", H),
    p("<b>Displaced first pole (b):</b> asymptotic estimate f<sub>p1</sub>' = f<sub>p2</sub>/(A<sub>0</sub>&beta;) = "
      "%.0f Hz, assuming f<sub>u</sub> = f<sub>p2</sub> and PM = 180&deg; - 90&deg; - 45&deg; = 45&deg;. "
      "The asymptote ignores the -3 dB of the second pole at f<sub>p2</sub>, so the exact condition "
      "|A&beta;(f<sub>p2</sub>)| = 1 gives f<sub>p1</sub>' = f<sub>p2</sub>/&radic;((A<sub>0</sub>&beta;)<super>2</super>/2 - 1) = "
      "<b>%.0f Hz</b>. The numerical solution is %.0f Hz (PM = %.2f&deg;)."
      % (r.fp1_b_asym, r.fp1_b_ref, r.fp1_b, r.pm_b)),
    p("<b>Added pole (c):</b> asymptotic estimate f<sub>x</sub> = f<sub>p1</sub>/(A<sub>0</sub>&beta;) = %.1f Hz, "
      "assuming f<sub>u</sub> = f<sub>p1</sub> with the second pole negligible. The numerical solution, which includes "
      "the second pole, is <b>%.1f Hz</b> (PM = %.1f&deg;)."
      % (r.fpx_c_asym, r.fpx_c_ref, r.pm_c)),
    p("The asymptotic values are the ones in RE2.pdf. The numerical solution includes the magnitude and phase of "
      "the second pole, so it is the value that meets PM = 45&deg; exactly."),

    p("d) Comparison", H),
    p("Added pole: simple to implement (one RC network), but the crossover falls to about %.0f kHz, "
      "so the bandwidth is lower. Displaced first pole: crossover at %.0f MHz, i.e. a much larger bandwidth, "
      "but it needs a dominant-pole network that is harder to build. The gain margin is 37 dB for the added pole "
      "and is not finite for the displaced pole." % (r.fu_c / 1e3, r.fu_b / 1e6)),

    p("Errors found in the original resolution (RE2.pdf)", H),
    p("- <b>&beta; = 0.1</b> is printed, but R<sub>1</sub>/(R<sub>1</sub>+R<sub>2</sub>) = 1/101 = <b>0.0099</b>. "
      "The printed -40 dB is correct, the value 0.1 (-20 dB) is not."),
    p("- <b>Gain margin 40 dB at 100 MHz</b> is not a true margin: the phase is not -180&deg; there "
      "(it is about -174&deg; for the displaced pole). The gain at 100 MHz is %.1f dB for the displaced pole. "
      "Only the added-pole case has a finite phase crossover, at %.2f MHz, with GM = %.1f dB."
      % (r.gm_b100, r.fpc_c / 1e6, r.gm_c)),
]

SimpleDocTemplate("alt_R2.pdf", pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=2 * cm,
                  title="RE2 numerical solution").build(el)
print("wrote alt_R2.pdf")
