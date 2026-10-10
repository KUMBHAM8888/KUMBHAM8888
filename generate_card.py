#!/usr/bin/env python3
"""
Generates profile-card.svg: an animated terminal-style card with an ASCII
portrait on the left and a "system info" panel on the right.

Usage:
    pip install pillow
    python generate_card.py --photo me.jpg      # ASCII portrait from your photo
    python generate_card.py                     # placeholder silhouette

Edit the CONFIG block below, re-run, commit profile-card.svg.
"""
import argparse
import html
from PIL import Image, ImageDraw, ImageFilter, ImageOps

# ───────────────────────── EDIT ME ─────────────────────────
CONFIG = {
    "handle": "saiteja@devops",
    "prompt": "saiteja@devops ~ % ./profile.sh --live",
    "sections": [
        ("", [
            ("Subject",   "Sai Teja Kumbham"),
            ("Cert",      "AWS Certified Developer – Associate"),
            ("Role",      "DevOps • SRE • Platform • Cloud"),
            ("Status",    "Building • Learning • Shipping"),
            ("ToolChain", "VS Code, Git, Docker, Postman"),
        ]),
        ("", [
            ("Core.Cloud",  "AWS (EC2, S3, Lambda, IAM)"),
            ("Core.CI/CD",  "GitHub Actions, Jenkins"),
            ("Core.Infra",  "Docker, Kubernetes, Terraform"),
            ("Core.Lang",   "Python, Bash, YAML, SQL"),
            ("Core.AI",     "MCP (Model Context Protocol)"),
        ]),
        ("Contact", [
            ("Grid.Portfolio", "kumbham8888.github.io"),
            ("Grid.LinkedIn",  "in/saitejagoudk"),
            ("Grid.Github",    "KUMBHAM8888"),
        ]),
    ],
    "footer": "See live GitHub stats below in README ↓",
}
# ───────────────────────────────────────────────────────────

W, H = 860, 450
ASCII_COLS, ASCII_ROWS = 64, 44
RAMP = " .:-=+*#%@"


def placeholder_portrait():
    """Head-and-shoulders silhouette so the card works before you add a photo."""
    img = Image.new("L", (320, 360), 0)
    d = ImageDraw.Draw(img)
    d.ellipse((60, 250, 260, 460), fill=150)          # shoulders
    d.rectangle((135, 200, 185, 270), fill=170)        # neck
    d.ellipse((100, 60, 220, 220), fill=215)           # head
    d.ellipse((92, 45, 228, 140), fill=120)            # hair
    for x in (132, 172):
        d.ellipse((x, 125, x + 16, 137), fill=70)      # eyes
    return img.filter(ImageFilter.GaussianBlur(4))


def photo_to_ascii(path):
    if path:
        img = ImageOps.exif_transpose(Image.open(path)).convert("L")
        img = ImageOps.autocontrast(ImageOps.fit(img, (360, 360)))
    else:
        img = placeholder_portrait()
    # characters are ~2x taller than wide → squash rows
    img = img.resize((ASCII_COLS, ASCII_ROWS))
    px = img.load()
    rows = []
    for y in range(ASCII_ROWS):
        rows.append("".join(RAMP[min(len(RAMP) - 1, px[x, y] * len(RAMP) // 256)]
                            for x in range(ASCII_COLS)))
    return rows


def dotted(key, val, width=44):
    dots = "." * max(3, width - len(key) - len(val))
    return key, dots, val


def build_svg(ascii_rows):
    e = html.escape
    out = []
    out.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#7c3aed"/><stop offset="0.5" stop-color="#22d3ee"/><stop offset="1" stop-color="#10b981"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" x2="1">
    <stop offset="0" stop-color="#22d3ee" stop-opacity="0"/><stop offset="0.5" stop-color="#22d3ee" stop-opacity=".55"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="win"><rect x="10" y="10" width="{W-20}" height="{H-20}" rx="12"/></clipPath>
</defs>
<style>
  text{{font-family:'JetBrains Mono','Fira Code',Consolas,monospace}}
  .k{{fill:#22d3ee}} .d{{fill:#3b4a5e}} .v{{fill:#e2e8f0}} .h{{fill:#10b981}}
  .lbl{{fill:#22d3ee;font-size:9px;letter-spacing:2px;opacity:.7}}
  .ascii{{fill:#60a5fa;font-size:7.4px;white-space:pre}}
  .row{{opacity:0;animation:in .4s ease forwards}}
  @keyframes in{{to{{opacity:1}}}}
  .blink{{animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}
  .pulse{{animation:pu 1.6s ease-in-out infinite}} @keyframes pu{{50%{{opacity:.25}}}}
</style>
<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="12" fill="#0b1220" stroke="url(#border)" stroke-width="1.6"/>
<g clip-path="url(#win)">
  <circle cx="30" cy="30" r="5" fill="#ef4444"/><circle cx="46" cy="30" r="5" fill="#f59e0b"/><circle cx="62" cy="30" r="5" fill="#10b981"/>
  <text x="{W/2}" y="34" text-anchor="middle" font-size="10" fill="#64748b">{e(CONFIG["prompt"])}</text>
  <circle class="pulse" cx="{W-82}" cy="30" r="3.5" fill="#ef4444"/>
  <text x="{W-74}" y="34" font-size="9" fill="#ef4444" letter-spacing="1">SCANNING</text>

  <rect x="24" y="52" width="370" height="372" rx="8" fill="#0d1628" stroke="#1e3a5f"/>
  <text x="34" y="66" class="lbl">VISUAL.MAP</text>
  <text class="ascii" x="38" y="82">''')
    for i, r in enumerate(ascii_rows):
        out.append(f'<tspan x="38" dy="{0 if i == 0 else 7.6}" xml:space="preserve">{e(r)}</tspan>')
    out.append('</text>')

    # right panel
    px, py = 408, 52
    out.append(f'<rect x="{px}" y="{py}" width="{W-24-px}" height="372" rx="8" fill="#0d1628" stroke="#1e3a5f"/>')
    out.append(f'<text x="{px+12}" y="{py+14}" class="lbl">SYSTEM.INFO</text>')
    out.append(f'<text x="{px+12}" y="{py+32}" font-size="13" fill="#a78bfa" font-weight="700">{e(CONFIG["handle"])}'
               f'<tspan fill="#3b4a5e" font-weight="400"> ──────────────────────</tspan></text>')
    y = py + 52
    delay = 0.2
    for title, rows in CONFIG["sections"]:
        if title:
            out.append(f'<text class="row h" style="animation-delay:{delay:.2f}s" x="{px+12}" y="{y}" font-size="11">─ {e(title)} <tspan class="d">──────────────────────────────</tspan></text>')
            y += 17; delay += 0.12
        for k, v in rows:
            k, dots, v = dotted(k, v)
            out.append(f'<text class="row" style="animation-delay:{delay:.2f}s" x="{px+12}" y="{y}" font-size="11" xml:space="preserve">'
                       f'<tspan class="d">. </tspan><tspan class="k">{e(k)}</tspan><tspan class="d">: {dots} </tspan><tspan class="v">{e(v)}</tspan></text>')
            y += 16; delay += 0.12
        y += 8
    out.append(f'<text class="row" style="animation-delay:{delay:.2f}s" x="{px+12}" y="{min(y+4, 412)}" font-size="11">'
               f'<tspan class="blink" fill="#22d3ee">█</tspan><tspan class="v"> {e(CONFIG["footer"])}</tspan></text>')

    # scan line sweeping the whole window
    out.append(f'''<rect x="10" y="0" width="{W-20}" height="2" fill="url(#scan)">
    <animate attributeName="y" values="50;425;50" dur="6s" repeatCount="indefinite"/></rect>
</g>
</svg>''')
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", help="path to a front-facing photo (jpg/png)")
    ap.add_argument("--out", default="profile-card.svg")
    a = ap.parse_args()
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(build_svg(photo_to_ascii(a.photo)))
    print(f"wrote {a.out}")
