#!/usr/bin/env python3
"""MaamiMade Pinterest creatives. 1000 x 1500 (2:3), the ratio Pinterest favours.

Built the same way as the book cover: Chrome headless screenshots so the type matches
the book exactly, then a JPEG compression loop.

  python3 pins.py     ->  pins/pin_hero.jpg   keyword pin, clean
                          pins/pin_sour.jpg   objection hook
                          pins/pin_fix.jpg    listicle
                          pins/pin_steps.jpg  process collage

Formats chosen from live Pinterest research, see ../pinterest/2026-09-12-winning-pins.md
"""
import subprocess
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "pins"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTCSS = (HERE / "fonts.css").read_text(encoding="utf-8")
W, H = 1000, 1500

BASE = """
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact}
body{font-family:"Karla","Helvetica Neue",Arial,sans-serif;background:#7a2a20}
.c{position:relative;width:%dpx;height:%dpx;overflow:hidden;background:#7a2a20}
.ph{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.tag{position:absolute;bottom:44px;left:0;right:0;text-align:center;font-size:22px;
  letter-spacing:.26em;text-transform:uppercase;color:#f0dcc6;z-index:4}
h1{font-family:"Fraunces",Georgia,serif;font-weight:600;line-height:1.03;
  letter-spacing:-.01em;color:#fff}
.kick{font-size:22px;letter-spacing:.28em;text-transform:uppercase;color:#e0b978}
.hair{width:110px;border-top:3px solid #c08a3e}
""" % (W, H)


def doc(body, css=""):
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>{FONTCSS}</style><style>{BASE}{css}</style></head>'
            f'<body>{body}</body></html>')


HERO = doc("""
<div class="c">
  <img class="ph" src="../build/img/plated_rice.jpg">
  <div class="sc"></div>
  <div class="band">
    <div class="kick">Nigerian &middot; Serves 6</div>
    <h1>Nigerian<br>Stew</h1>
    <div class="hair"></div>
    <div class="sl">The pepper led base my mother has cooked for forty years,
      and every way a pot of it can go wrong</div>
  </div>
  <div class="tag">maamimade &middot; the full method</div>
</div>""", """
.sc{position:absolute;inset:0;background:linear-gradient(180deg,
  rgba(70,20,13,.06) 0%, rgba(70,20,13,.14) 38%, rgba(70,20,13,.82) 62%,
  rgba(70,20,13,.94) 100%)}
.band{position:absolute;left:80px;right:80px;bottom:130px;z-index:3}
.band h1{font-size:108px;margin:26px 0 30px}
.hair{margin:0 0 30px}
.sl{font-family:"Fraunces",Georgia,serif;font-size:30px;line-height:1.42;color:#f6e6d8;
  max-width:760px}
""")

SOUR = doc("""
<div class="c">
  <img class="ph" src="../build/img/fry_stage.jpg">
  <div class="sc"></div>
  <div class="top">
    <div class="kick">Nigerian stew</div>
    <h1>Stop making<br>sour stew</h1>
  </div>
  <div class="bot">
    <div class="hair"></div>
    <div class="sl">It is almost always the tomato, and it is almost always fixable.
      The one rule that changes the whole pot.</div>
  </div>
  <div class="tag">maamimade</div>
</div>""", """
.sc{position:absolute;inset:0;background:linear-gradient(180deg,
  rgba(70,20,13,.90) 0%, rgba(70,20,13,.52) 32%, rgba(70,20,13,.04) 54%,
  rgba(70,20,13,.74) 80%, rgba(70,20,13,.95) 100%)}
.top{position:absolute;top:96px;left:80px;right:80px;z-index:3}
.top h1{font-size:104px;margin-top:30px}
.bot{position:absolute;left:80px;right:80px;bottom:132px;z-index:3}
.hair{margin:0 0 28px}
.sl{font-family:"Fraunces",Georgia,serif;font-size:31px;line-height:1.42;color:#f6e6d8}
""")

FAULTS = ["It tastes sour", "It tastes watery", "It tastes bitter", "It tastes flat",
          "It is too spicy", "It looks pale", "It is sticking", "It is too salty"]

FIX = doc("""
<div class="c">
  <div class="hd">
    <div class="kick">Nigerian stew</div>
    <h1>8 ways your<br>stew goes wrong</h1>
  </div>
  <img class="strip" src="../build/img/orishirishi.jpg">
  <div class="list">""" + "".join(f"<div>{f}</div>" for f in FAULTS) + """</div>
  <div class="cta">and how to fix every one</div>
  <div class="tag">maamimade</div>
</div>""", """
.c{background:#7a2a20}
.hd{position:absolute;top:80px;left:80px;right:80px;z-index:3}
.hd h1{font-size:82px;margin-top:24px}
.strip{position:absolute;top:390px;left:0;width:100%;height:430px;object-fit:cover}
.list{position:absolute;top:900px;left:80px;right:80px;z-index:3;
  display:grid;grid-template-columns:1fr 1fr;gap:22px 26px}
.list div{font-size:29px;color:#f6e6d8;padding-left:26px;position:relative;line-height:1.35}
.list div:before{content:"";position:absolute;left:0;top:14px;width:10px;height:10px;
  background:#c08a3e;border-radius:50%}
.cta{position:absolute;left:80px;right:80px;bottom:150px;z-index:3;
  font-family:"Fraunces",Georgia,serif;font-style:italic;font-size:36px;color:#fff}
""")

STEPS = doc("""
<div class="c">
  <div class="hd">
    <div class="kick">Step by step</div>
    <h1>How to make<br>Nigerian stew</h1>
  </div>
  <div class="grid">
    <figure><img src="../build/img/step_peppers_can.jpg"><figcaption>01 &nbsp; Pepper leads, tomato follows</figcaption></figure>
    <figure><img src="../build/img/step_blended.jpg"><figcaption>02 &nbsp; Blend it with your stock, never water</figcaption></figure>
    <figure><img src="../build/img/fry_stage.jpg"><figcaption>03 &nbsp; Fry it far longer than you think</figcaption></figure>
  </div>
  <div class="tag">maamimade &middot; the full method</div>
</div>""", """
.c{background:#7a2a20}
.hd{position:absolute;top:76px;left:80px;right:80px;z-index:3}
.hd h1{font-size:76px;margin-top:22px}
.grid{position:absolute;top:320px;left:80px;right:80px;display:grid;gap:26px}
.grid figure{position:relative}
.grid img{width:100%;height:296px;object-fit:cover;display:block}
.grid figcaption{margin-top:12px;font-size:25px;color:#f0dcc6;letter-spacing:.04em}
""")

JOBS = [("_hero.html", HERO, "pin_hero"), ("_sour.html", SOUR, "pin_sour"),
        ("_fix.html", FIX, "pin_fix"), ("_steps.html", STEPS, "pin_steps")]

OUT.mkdir(exist_ok=True)
for name, html, stem in JOBS:
    (HERE / name).write_text(html, encoding="utf-8")
    png = OUT / f"{stem}.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--virtual-time-budget=20000",
                    f"--window-size={W},{H}", f"--screenshot={png}",
                    f"file://{HERE / name}"], capture_output=True, timeout=300)
    if not png.exists():
        print(f"{stem} FAILED")
        continue
    jpg = png.with_suffix(".jpg")
    q = 92
    while q >= 60:
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=q, optimize=True, progressive=True)
        if jpg.stat().st_size < 1_000_000:
            break
        q -= 6
    png.unlink()
    (HERE / name).unlink()
    print(f"{stem:12} {jpg.stat().st_size // 1024:>4} KB  q{q}")
