#!/usr/bin/env python3
"""The Stew Rescue Card. The lead magnet behind the email capture on the recipe page.

One page, printable, every fault a pot of Nigerian stew can develop and how to fix it.
Built from the troubleshooting the free page already publishes, so it gives away nothing
the book is selling.

  python3 card.py   ->  Stew_Rescue_Card.pdf

Chrome headless needs --allow-file-access-from-files or the webfonts silently fall back
to Helvetica. Never use text-shadow here, Chrome print-to-pdf stamps it once per layer.
"""
import subprocess, re
from pathlib import Path

HERE = Path(__file__).parent
SITE = HERE.parent
FONTCSS = (SITE / "fonts.css").read_text(encoding="utf-8")
PDF = HERE / "Stew_Rescue_Card.pdf"

FAULTS = [
 ("Sour or sharp", "Tomato. Either too much of it in the base, or it has not fried long "
  "enough to lose its raw edge. Keep frying before you add anything else."),
 ("Watery", "Keep cooking uncovered until it reduces. Do not add more stock to fix a "
  "texture problem."),
 ("Bitter", "The peppers want more cooking, or something has caught and over charred. Fry "
  "gently and taste again. Seasoning will not bury bitterness."),
 ("Too spicy", "More mild pepper and tomato base, more cooked protein, then simmer. Salt "
  "does not help."),
 ("Too salty", "Dilute with more unsalted pepper base, not water. Water thins the stew "
  "without fixing the balance."),
 ("Flat", "Give it time before you give it seasoning. Let it reduce and fry longer, then "
  "adjust salt, stock seasoning, soy sauce or acidity one at a time."),
 ("Pale", "More long red pepper, or simply more reduction. Pepper colour varies, so do not "
  "chase colour at the expense of flavour."),
 ("Sticking", "Lower the heat and stir up from the bottom. A heavy pot helps, and a "
  "reducing stew should not be left alone."),
]

CSS = """
@page { size: 8.5in 11in; margin: 0; }
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"Karla","Helvetica Neue",Arial,sans-serif;color:#2b211d}
.page{width:8.5in;height:11in;position:relative;background:#fdf9f5;overflow:hidden}
.hd{background:#7a2a20;color:#fff;padding:.54in .85in .46in}
.kick{font-size:8pt;letter-spacing:.22em;text-transform:uppercase;color:#e8c9a8;margin-bottom:12pt}
h1{font-family:"Fraunces",Georgia,serif;font-weight:600;font-size:33pt;line-height:1.05;
  letter-spacing:-.01em;margin-bottom:9pt}
.hd p{font-family:"Fraunces",Georgia,serif;font-size:11.5pt;color:#f3ddcc;max-width:5.2in;
  line-height:1.5}
.body{padding:.38in .85in 0}
.row{display:flex;gap:16pt;padding:8.5pt 0;border-bottom:.6pt solid #e8ded5}
.row:last-child{border-bottom:0}
.q{font-family:"Fraunces",Georgia,serif;font-size:13pt;color:#7a2a20;width:1.5in;flex:none;
  line-height:1.25;padding-top:1pt}
.a{font-size:10.2pt;line-height:1.6;color:#3b2f29}
.rule{border-top:2.4pt solid #c08a3e;width:64pt;margin:0 0 15pt}
.note{margin:17pt 0 0;background:#fff;border:.6pt solid #eeddcb;border-left:2.4pt solid #a63a2c;
  padding:15pt 18pt}
.note b{color:#7a2a20}
.note p{font-size:10.2pt;line-height:1.62}
.ft{position:absolute;left:.85in;right:.85in;bottom:.5in;display:flex;
  justify-content:space-between;border-top:.6pt solid #e3d3c6;padding-top:8pt;
  font-size:7.6pt;letter-spacing:.11em;text-transform:uppercase;color:#a2958b}
"""

ROWS = "".join(f'<div class="row"><div class="q">{q}</div><div class="a">{a}</div></div>'
               for q, a in FAULTS)

HTML = f"""<!doctype html><html><head><meta charset="utf-8">
<title>The Stew Rescue Card</title>
<style>{FONTCSS}</style><style>{CSS}</style></head><body>
<div class="page">
  <div class="hd">
    <div class="kick">MaamiMade &middot; keep this near the hob</div>
    <h1>The Stew Rescue Card</h1>
    <p>Eight things that go wrong in a pot of Nigerian stew, and what to do about each one
    before you reach for more seasoning.</p>
  </div>
  <div class="body">
    <div class="rule"></div>
    {ROWS}
    <div class="note">
      <p><b>The rule underneath all eight.</b> Taste before you add. Almost every fault on
      this card is time rather than seasoning, and almost every rescue starts by letting the
      pot cook a little longer than feels reasonable.</p>
    </div>
  </div>
  <div class="ft"><span>Ob&eacute; T&oacute; D&ugrave;n &middot; the full method</span>
  <span>maamimade</span></div>
</div></body></html>"""

html_file = HERE / "_card.html"
html_file.write_text(HTML, encoding="utf-8")
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--headless", "--disable-gpu", "--no-pdf-header-footer",
                "--allow-file-access-from-files", "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=30000", f"--print-to-pdf={PDF}",
                f"file://{html_file}"], capture_output=True, timeout=300)
html_file.unlink()

prose = re.sub(r"<[^>]+>", " ", HTML)
print("em dash in prose :", prose.count("—"))
print("en dash in prose :", prose.count("–"))
print("wrote            :", PDF, f"{PDF.stat().st_size // 1024} KB" if PDF.exists() else "FAILED")
