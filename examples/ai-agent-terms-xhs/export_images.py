#!/usr/bin/env python3
from pathlib import Path
import textwrap

W, H = 810, 1080
OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

slides = [
    ("AI Agent skills 常用术语解释", "用生活案例，5 分钟看懂 AI Agent 的 10 个高频词。"),
    ("01 Agent（智能体）", "像会自己比价+下单+催发货的网购助理：能拆步骤、会调用工具、还会复查结果。"),
    ("02 Skill（技能包）", "像菜谱 + 厨房 SOP：把规则、模板、工具调用写清楚，让每次输出稳定可复用。"),
    ("03 Prompt ≠ Skill", "Prompt 是一次口头指令；Skill 是可复制的流程系统。一次性和可沉淀，差很多。"),
    ("04 Workflow（工作流）", "像外卖流程：接单 → 备餐 → 配送。顺序明确，才能规模化执行。"),
    ("05 Tool Call（工具调用）", "Agent 要借助地图、搜索、表格、邮件 API 才能做完整任务。"),
    ("06 Context（上下文）", "上下文就是背景包：历史对话、文档、角色、约束。太少会空泛，太乱会跑偏。"),
    ("07 Memory（记忆）", "短期记住当前会话，长期记住你偏好。像常去咖啡店，店员记得你少糖。"),
    ("08 Planner（计划器）", "先把复杂任务拆成 5~10 步再执行。像搬家先列清单，减少返工。"),
    ("09 Guardrails（护栏）", "像汽车安全带：平时无感，关键时刻防止越界和事故。"),
    ("10 Eval（评测）", "持续测准确率、稳定性、速度和成本，避免“这周好用下周翻车”。"),
    ("一页总结", "Agent 会做事，Skill 定标准，Workflow 管流程，Tool 给能力，Guardrails 保安全，Eval 保质量。"),
]


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

for i, (title, body) in enumerate(slides, start=1):
    lines = textwrap.wrap(body, width=20)
    body_svg = "\n".join(
        f'<text x="72" y="{360 + idx*58}" font-size="42" fill="#6f4a3e" font-family="Inter,Noto Sans SC,sans-serif">{esc(line)}</text>'
        for idx, line in enumerate(lines)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff7f3"/>
      <stop offset="100%" stop-color="#ffeedd"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="36" fill="url(#bg)"/>
  <rect x="50" y="46" width="180" height="44" rx="22" fill="#3a1f18"/>
  <text x="72" y="76" font-size="24" fill="#fff" font-family="Inter,Noto Sans SC,sans-serif" font-weight="700">AI Agent 术语</text>
  <rect x="620" y="46" width="140" height="44" rx="22" fill="#3a1f18"/>
  <text x="653" y="76" font-size="24" fill="#fff" font-family="JetBrains Mono,monospace" font-weight="700">{i:02d}/12</text>
  <text x="72" y="190" font-size="66" fill="#3a1f18" font-family="Inter,Noto Sans SC,sans-serif" font-weight="900">{esc(title)}</text>
  <line x1="72" y1="230" x2="738" y2="230" stroke="#3a1f18" stroke-width="4" opacity="0.2"/>
  {body_svg}
  <rect x="72" y="930" width="666" height="96" rx="20" fill="#fff" stroke="#3a1f18" stroke-width="3"/>
  <text x="96" y="989" font-size="36" fill="#3a1f18" font-family="Inter,Noto Sans SC,sans-serif" font-weight="700">可直接下载图片使用（SVG 高清）</text>
</svg>'''
    (OUT / f"slide-{i:02d}.svg").write_text(svg, encoding="utf-8")

index = [
    "<!doctype html><meta charset='utf-8'><title>AI Agent术语图文下载</title>",
    "<style>body{font-family:Inter,Noto Sans SC,sans-serif;background:#faf7f5;padding:24px} .g{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px} .c{background:#fff;border:1px solid #eee;border-radius:12px;padding:12px} img{width:100%;border-radius:8px}</style>",
    "<h1>AI Agent 术语图文（SVG 下载）</h1><div class='g'>",
]
for i in range(1, 13):
    fn = f"slide-{i:02d}.svg"
    index.append(f"<div class='c'><img src='{fn}'><p><a href='{fn}' download='{fn}'>下载 {fn}</a></p></div>")
index.append("</div>")
(OUT / "index.html").write_text("\n".join(index), encoding="utf-8")
print(f"generated {len(slides)} SVG slides to {OUT}")
