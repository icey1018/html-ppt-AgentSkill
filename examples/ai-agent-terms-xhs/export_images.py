#!/usr/bin/env python3
"""Export per-slide SVG files that preserve original HTML slide content/styles 1:1.

This script extracts each `<section class="slide">...</section>` from
`examples/ai-agent-terms-xhs/index.html` and wraps it in an SVG `<foreignObject>`.
The embedded XHTML imports the same CSS files as the source deck so visual output
matches the original slide style/content without simplification.
"""

from pathlib import Path
import re

ROOT = Path(__file__).parent
SOURCE = ROOT / "index.html"
OUT_DIR = ROOT / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 810, 1080

html = SOURCE.read_text(encoding="utf-8")
sections = re.findall(r'(<section class="slide"[\s\S]*?</section>)', html)
if len(sections) != 12:
    raise SystemExit(f"expected 12 slides, got {len(sections)}")

css_links = "\n".join(
    [
        '<link rel="stylesheet" href="../../../assets/fonts.css"/>',
        '<link rel="stylesheet" href="../../../assets/base.css"/>',
        '<link rel="stylesheet" href="../../../assets/themes/xiaohongshu-white.css"/>',
        '<link rel="stylesheet" href="../../../assets/animations/animations.css"/>',
        '<link rel="stylesheet" href="../style.css"/>',
    ]
)

for idx, section in enumerate(sections, start=1):
    section = section.replace('class="slide"', 'class="slide is-active"', 1)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <foreignObject x="0" y="0" width="{WIDTH}" height="{HEIGHT}">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN">
      <head>
        <meta charset="utf-8"/>
        {css_links}
        <style>
          html, body {{ margin:0; padding:0; width:{WIDTH}px; height:{HEIGHT}px; overflow:hidden; background:transparent; }}
          body.tpl-xhs-post {{ min-height:{HEIGHT}px; background:transparent; display:block; }}
          body.tpl-xhs-post .deck {{ width:{WIDTH}px; height:{HEIGHT}px; }}
          body.tpl-xhs-post .slide {{ position:relative; inset:auto; width:{WIDTH}px; height:{HEIGHT}px; opacity:1; pointer-events:auto; }}
        </style>
      </head>
      <body class="tpl-xhs-post">
        <div class="deck">
          {section}
        </div>
      </body>
    </html>
  </foreignObject>
</svg>
'''
    (OUT_DIR / f"slide-{idx:02d}.svg").write_text(svg, encoding="utf-8")

cards = []
for i in range(1, len(sections) + 1):
    fn = f"slide-{i:02d}.svg"
    cards.append(
        f"<div class='c'><img src='{fn}' alt='slide {i:02d}'/><p><a href='{fn}' download='{fn}'>下载 {fn}</a></p></div>"
    )

index_html = """<!doctype html>
<meta charset='utf-8'>
<title>AI Agent术语图文下载（与原 HTML 一致）</title>
<style>
body{font-family:Inter,Noto Sans SC,sans-serif;background:#faf7f5;padding:24px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.c{background:#fff;border:1px solid #eee;border-radius:12px;padding:12px}
img{width:100%;border-radius:8px;display:block}
a{color:#7c3aed;text-decoration:none;font-weight:700}
</style>
<h1>AI Agent 术语图文（SVG 下载）</h1>
<p>以下图片直接复用原始 HTML Slide 内容与样式，不做简化、不改样式。</p>
<div class='g'>
""" + "\n".join(cards) + "\n</div>\n"

(OUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
print(f"generated {len(sections)} svg slides to {OUT_DIR}")
