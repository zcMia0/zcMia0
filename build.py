# -*- coding: utf-8 -*-
"""
zcMia0 · profile README builder  (软萌日系 Q 版治愈风)

用法（在本文件所在目录执行）：
    python build.py                      # 重新生成全部 SVG 资产 + README.md + preview.html
    python build.py --shiba              # 把顶部横幅换成柴犬版（覆盖 assets/banner.svg）
    python build.py --cat                # 换回橘猫版
    python build.py --mascot my.png      # 用自己生成的小动物图重建横幅（内嵌为 base64，离线可用）
    python build.py --url https://...    # 直接抓一张网络图片来重建横幅

说明：SVG 必须完全自包含（GitHub 的 <img> 不会加载外部字体/图片），
     所以所有字体都用系统字体栈，自定义图用 data URI 内嵌。
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import mimetypes
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

# 界面文案的唯一数据源（基于 github.com/zcMia0 的真实公开资料）
# 改完 profile.json 后重跑 `python build.py` 即可全量重建
PROFILE = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))


def esc(s: str) -> str:
    """写进 HTML/SVG 前的最小转义。"""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- palette
CREAM = "#FFF8F0"
PAPER = "#FFFDF9"
PINK = "#FFD6E0"
PINK_DEEP = "#F2AFC2"
MINT = "#C8E6D4"
MINT_DEEP = "#9FD2B6"
YELLOW = "#FFE9A8"
YELLOW_DEEP = "#EBC46E"
INK = "#6B5A4F"
MUTED = "#A9988A"
ROSE = "#B5838D"
GREEN = "#6F9C81"
BROWN = "#5B4636"

# 圆润字体感：系统圆体优先 + 同色描边 (paint-order) 把笔画末端磨圆
FONT = ("'Varela Round','Quicksand','Nunito','Arial Rounded MT Bold',"
        "'Avenir Next Rounded','Chalkboard SE','Trebuchet MS','Segoe UI',"
        "'Microsoft YaHei','Segoe UI Emoji','Apple Color Emoji','Noto Color Emoji',sans-serif")


# ---------------------------------------------------------------- helpers
def svg(w: int, h: int, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{title}">\n'
        f'  <title>{title}</title>\n{body}\n</svg>\n'
    )


def T(x, y, s, size=20, fill=INK, weight=600, anchor="start", soft=True, opacity=None):
    st = (f' stroke="{fill}" stroke-width="0.95" stroke-linejoin="round" '
          'paint-order="stroke"') if soft else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
            f'{st}{op}>{s}</text>')


def flower(cx, cy, r, color, core=YELLOW_DEEP):
    out = []
    for i in range(5):
        a = i * 2 * math.pi / 5 - math.pi / 2
        out.append(f'<circle cx="{cx + r*0.78*math.cos(a):.2f}" '
                   f'cy="{cy + r*0.78*math.sin(a):.2f}" r="{r*0.60:.2f}" fill="{color}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.40:.2f}" fill="{core}"/>')
    return "".join(out)


def sparkle(cx, cy, r, color):
    return (f'<path d="M{cx} {cy-r} Q{cx} {cy} {cx+r} {cy} Q{cx} {cy} {cx} {cy+r} '
            f'Q{cx} {cy} {cx-r} {cy} Q{cx} {cy} {cx} {cy-r} Z" fill="{color}"/>')


def heart(cx, cy, r, color):
    return (f'<circle cx="{cx-r*0.45:.2f}" cy="{cy-r*0.25:.2f}" r="{r*0.50:.2f}" fill="{color}"/>'
            f'<circle cx="{cx+r*0.45:.2f}" cy="{cy-r*0.25:.2f}" r="{r*0.50:.2f}" fill="{color}"/>'
            f'<path d="M{cx-r*0.87:.2f} {cy-r*0.10:.2f} L{cx} {cy+r*0.95:.2f} '
            f'L{cx+r*0.87:.2f} {cy-r*0.10:.2f} Z" fill="{color}"/>')


# ---------------------------------------------------------------- mascot
def mascot(kind: str) -> str:
    """返回 200x200 局部坐标的 Q 版小动物（静态，挥手）。"""
    if kind == "shiba":
        fur, dark, cream, inner = "#E9A97A", "#D68F60", "#FFF6E8", "#F6C6AE"
        ears = (
            f'<path d="M48 62 Q42 10 84 38 Q90 45 88 62 Z" fill="{fur}"/>'
            f'<path d="M152 62 Q158 10 116 38 Q110 45 112 62 Z" fill="{fur}"/>'
            f'<path d="M57 56 Q55 28 79 44 Z" fill="{inner}"/>'
            f'<path d="M143 56 Q145 28 121 44 Z" fill="{inner}"/>'
        )
        marks = (f'<ellipse cx="82" cy="72" rx="6" ry="4" fill="{cream}" opacity="0.9"/>'
                 f'<ellipse cx="118" cy="72" rx="6" ry="4" fill="{cream}" opacity="0.9"/>')
        tail = (f'<path d="M148 150 C 184 150 188 110 166 102 C 152 97 148 116 162 122" '
                f'fill="none" stroke="{fur}" stroke-width="16" stroke-linecap="round"/>'
                f'<circle cx="166" cy="102" r="8" fill="{cream}"/>')
        eyes = (f'<ellipse cx="80" cy="91" rx="5.5" ry="7.5" fill="{BROWN}"/>'
                f'<ellipse cx="120" cy="91" rx="5.5" ry="7.5" fill="{BROWN}"/>'
                f'<circle cx="82" cy="88" r="2" fill="#FFFFFF"/>'
                f'<circle cx="122" cy="88" r="2" fill="#FFFFFF"/>')
    else:  # 橘猫
        fur, dark, cream, inner = "#F7B267", "#E8944A", "#FFF3E0", "#FFC9D4"
        ears = (
            f'<path d="M46 60 Q40 14 76 36 Q86 43 88 58 Z" fill="{fur}"/>'
            f'<path d="M154 60 Q160 14 124 36 Q114 43 112 58 Z" fill="{fur}"/>'
            f'<path d="M54 53 Q52 30 74 42 Z" fill="{inner}"/>'
            f'<path d="M146 53 Q148 30 126 42 Z" fill="{inner}"/>'
        )
        marks = (f'<rect x="88" y="34" width="7" height="15" rx="3.5" fill="{dark}"/>'
                 f'<rect x="100" y="30" width="7" height="19" rx="3.5" fill="{dark}"/>'
                 f'<rect x="112" y="34" width="7" height="15" rx="3.5" fill="{dark}"/>')
        tail = (f'<path d="M148 152 C 182 156 190 120 172 106" fill="none" '
                f'stroke="{fur}" stroke-width="17" stroke-linecap="round"/>'
                f'<circle cx="172" cy="106" r="9" fill="{cream}"/>')
        eyes = (f'<ellipse cx="78" cy="90" rx="6" ry="8" fill="{BROWN}"/>'
                f'<ellipse cx="122" cy="90" rx="6" ry="8" fill="{BROWN}"/>'
                f'<circle cx="80" cy="87" r="2" fill="#FFFFFF"/>'
                f'<circle cx="124" cy="87" r="2" fill="#FFFFFF"/>')

    return f'''\n    <ellipse cx="100" cy="186" rx="60" ry="8" fill="#E7D6C2" opacity="0.55"/>
    {tail}
    <ellipse cx="100" cy="150" rx="55" ry="44" fill="{fur}"/>
    <ellipse cx="100" cy="154" rx="36" ry="31" fill="{cream}"/>
    <ellipse cx="72" cy="182" rx="18" ry="10" fill="{cream}"/>
    <ellipse cx="128" cy="182" rx="18" ry="10" fill="{cream}"/>
    {ears}
    <circle cx="100" cy="90" r="60" fill="{fur}"/>
    {marks}
    <ellipse cx="100" cy="106" rx="30" ry="19" fill="{cream}"/>
    {eyes}
    <ellipse cx="62" cy="105" rx="10" ry="6" fill="#FFB3C1" opacity="0.85"/>
    <ellipse cx="138" cy="105" rx="10" ry="6" fill="#FFB3C1" opacity="0.85"/>
    <path d="M95 100 Q100 95 105 100 Q100 106 95 100 Z" fill="#E08C9B"/>
    <path d="M100 105 Q93 114 86 107 M100 105 Q107 114 114 107" fill="none"
          stroke="{BROWN}" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M60 104 L40 100 M60 110 L42 113 M140 104 L160 100 M140 110 L158 113"
          stroke="{BROWN}" stroke-width="1.6" stroke-linecap="round" opacity="0.45"/>
    <path d="M142 138 C 164 132 172 108 166 92" fill="none"
          stroke="{fur}" stroke-width="21" stroke-linecap="round"/>
    <circle cx="166" cy="86" r="15" fill="{cream}"/>
    <circle cx="161" cy="81" r="2.4" fill="{fur}"/>
    <circle cx="168" cy="79" r="2.4" fill="{fur}"/>
    <circle cx="174" cy="82" r="2.4" fill="{fur}"/>
    <path d="M184 60 q9 -7 17 -1 M188 74 q8 -5 14 0" fill="none"
          stroke="{PINK_DEEP}" stroke-width="3" stroke-linecap="round"/>
    {heart(38, 34, 10, "#FFB3C1")}
'''


# ---------------------------------------------------------------- banner
def banner(kind="cat", name=None, embedded=None) -> str:
    name = name or PROFILE["name"]
    W, H = 860, 250
    deco = f'''\n  <defs><clipPath id="round"><rect x="6" y="6" width="848" height="238" rx="34"/></clipPath></defs>
  <rect x="6" y="6" width="848" height="238" rx="34" fill="{CREAM}" stroke="{PINK}" stroke-width="2.5"/>
  <g clip-path="url(#round)">
    <circle cx="806" cy="6" r="122" fill="{YELLOW}" opacity="0.40"/>
    <circle cx="26" cy="248" r="122" fill="{MINT}" opacity="0.38"/>
    <circle cx="726" cy="230" r="68" fill="{PINK}" opacity="0.55"/>
    <circle cx="372" cy="2" r="52" fill="{PINK}" opacity="0.28"/>
    <circle cx="646" cy="52" r="8" fill="{PINK_DEEP}" opacity="0.55"/>
    <circle cx="668" cy="34" r="5" fill="{MINT_DEEP}" opacity="0.75"/>
    <circle cx="812" cy="176" r="7" fill="{YELLOW_DEEP}" opacity="0.6"/>
    <circle cx="290" cy="36" r="5" fill="{MINT_DEEP}" opacity="0.7"/>
    {sparkle(760, 62, 8, YELLOW_DEEP)}
    {sparkle(300, 210, 7, PINK_DEEP)}
    {flower(794, 200, 9, "#FFFFFF", YELLOW_DEEP)}
  </g>
  <circle cx="170" cy="130" r="100" fill="none" stroke="{MINT_DEEP}"
          stroke-width="2" stroke-dasharray="3 10" stroke-linecap="round" opacity="0.85"/>
  <circle cx="170" cy="130" r="92" fill="#FFE7EE" stroke="#FFFFFF" stroke-width="6"/>
'''
    if embedded is not None:
        mime, b64 = embedded
        mascot_group = (f'  <image x="82" y="42" width="176" height="176" '
                        f'href="data:{mime};base64,{b64}" preserveAspectRatio="xMidYMid meet"/>')
    else:
        mascot_group = f'  <g transform="translate(78,38) scale(0.92)">{mascot(kind)}  </g>'

    text = f'''\n  <rect x="298" y="46" width="176" height="32" rx="16" fill="{PAPER}" stroke="{MINT_DEEP}" stroke-width="1.6"/>
  {flower(316, 62, 7, PINK_DEEP, YELLOW_DEEP)}
  {T(330, 68, "welcome in ~", 15, GREEN, 600)}
  {T(300, 122, f"Hi, I'm {name} 👋", 34, ROSE, 600)}
  {T(302, 162, "nice to meet you!", 23, INK, 500)}
  <rect x="300" y="182" width="204" height="34" rx="17" fill="{PAPER}" stroke="{YELLOW_DEEP}" stroke-width="1.6"/>
  {T(322, 205, "a tiny cozy corner", 15, MUTED, 500)}
  {heart(486, 199, 8, PINK_DEEP)}
  <circle cx="540" cy="199" r="3.5" fill="{MINT_DEEP}"/>
  <circle cx="552" cy="199" r="3.5" fill="{YELLOW_DEEP}"/>
  <circle cx="564" cy="199" r="3.5" fill="{PINK_DEEP}"/>
'''
    body = (deco + "  <!-- ===== MASCOT START · 换图只需替换这一组 ===== -->\n"
            + mascot_group + "\n  <!-- ===== MASCOT END ===== -->" + text)
    return svg(W, H, body, f"Hi, I'm {name}, nice to meet you")


# ---------------------------------------------------------------- divider
def divider() -> str:
    W, H = 860, 30
    body = f'''\n  <path d="M46 15 H356" fill="none" stroke="{PINK_DEEP}" stroke-width="3.2"
        stroke-dasharray="9 13" stroke-linecap="round"/>
  <path d="M504 15 H814" fill="none" stroke="{PINK_DEEP}" stroke-width="3.2"
        stroke-dasharray="9 13" stroke-linecap="round"/>
  <circle cx="34" cy="15" r="4" fill="{MINT_DEEP}"/>
  <circle cx="826" cy="15" r="4" fill="{YELLOW_DEEP}"/>
  {flower(430, 15, 12, PINK, YELLOW_DEEP)}
  <circle cx="386" cy="15" r="3" fill="{MINT_DEEP}" opacity="0.8"/>
  <circle cx="474" cy="15" r="3" fill="{PINK_DEEP}" opacity="0.8"/>
'''
    return svg(W, H, body, "dotted divider")


# ---------------------------------------------------------------- titles
def title_svg(text: str, accent: str, deep: str, icon: str, label: str) -> str:
    W, H = 440, 72
    icon_color = ROSE if accent == PINK else (GREEN if accent == MINT else "#B48A3E")
    if icon == "bubble":
        glyph = (f'<rect x="3" y="4" width="26" height="19" rx="9.5" fill="{icon_color}"/>'
                 f'<path d="M11 22 L9 29 L18 22 Z" fill="{icon_color}"/>'
                 '<circle cx="10" cy="13.5" r="2" fill="#FFFFFF"/>'
                 '<circle cx="16" cy="13.5" r="2" fill="#FFFFFF"/>'
                 '<circle cx="22" cy="13.5" r="2" fill="#FFFFFF"/>')
    elif icon == "paw":
        glyph = (f'<circle cx="16" cy="20" r="7.5" fill="{icon_color}"/>'
                 f'<circle cx="8" cy="10" r="3.2" fill="{icon_color}"/>'
                 f'<circle cx="16" cy="7.5" r="3.2" fill="{icon_color}"/>'
                 f'<circle cx="24" cy="10" r="3.2" fill="{icon_color}"/>')
    elif icon == "gift":
        glyph = (f'<rect x="3" y="11" width="26" height="18" rx="5" fill="{icon_color}"/>'
                 f'<rect x="2" y="8" width="28" height="6" rx="3" fill="{icon_color}"/>'
                 '<path d="M16 8 V29" stroke="#FFFFFF" stroke-width="2.4"/>'
                 '<path d="M16 8 C10 2 6 8 16 9 C26 8 22 2 16 8 Z" fill="#FFFFFF"/>')
    else:  # dango
        glyph = (f'<rect x="15" y="4" width="2.6" height="26" rx="1.3" fill="{icon_color}"/>'
                 f'<circle cx="16" cy="8" r="5.5" fill="{PINK_DEEP}"/>'
                 f'<circle cx="16" cy="17" r="5.5" fill="#FFFFFF" stroke="{icon_color}" stroke-width="1.2"/>'
                 f'<circle cx="16" cy="26" r="5.5" fill="{MINT_DEEP}"/>')
    body = f'''\n  <rect x="4" y="8" width="432" height="56" rx="28" fill="{accent}" opacity="0.62"
        stroke="{deep}" stroke-width="2"/>
  <circle cx="42" cy="36" r="21" fill="{PAPER}"/>
  <g transform="translate(26,20)">{glyph}</g>
  {T(76, 45, text, 26, INK, 600)}
  <circle cx="396" cy="30" r="3.2" fill="{deep}"/>
  <circle cx="408" cy="36" r="3.2" fill="{deep}"/>
  <circle cx="396" cy="42" r="3.2" fill="{deep}"/>
  {sparkle(370, 20, 5, deep)}
'''
    return svg(W, H, body, label)


# ---------------------------------------------------------------- bubble
def bubble() -> str:
    W, H = 760, 212
    outline = (
        "M 48 14 H 712 Q 746 14 746 48 V 138 Q 746 172 712 172 H 110 "
        "L 62 202 Q 56 204 58 194 L 66 172 H 48 Q 14 172 14 138 V 48 Q 14 14 48 14 Z"
    )
    lines = PROFILE["about_lines"]
    body = f'''\n  <path d="{outline}" fill="{PAPER}" stroke="{PINK}" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="60" cy="52" r="22" fill="{PINK}"/>
  {T(60, 61, "💬", 24, INK, 400, "middle", soft=False)}
  {T(100, 74, esc(lines[0]), 18, INK, 500)}
  {T(100, 112, esc(lines[1]), 18, INK, 500)}
  {T(100, 150, esc(lines[2]), 18, INK, 500)}
  <circle cx="690" cy="150" r="4" fill="{PINK_DEEP}"/>
  <circle cx="706" cy="150" r="4" fill="{MINT_DEEP}"/>
  <circle cx="722" cy="150" r="4" fill="{YELLOW_DEEP}"/>
  {flower(716, 40, 8, PINK, YELLOW_DEEP)}
'''
    return svg(W, H, body, "a little note from me")


# ---------------------------------------------------------------- tiny dots
def dot(color: str) -> str:
    body = f'''\n  <circle cx="12" cy="12" r="11" fill="{color}"/>
  <circle cx="12" cy="15" r="4.3" fill="#FFFFFF" opacity="0.95"/>
  <circle cx="7.2" cy="8.6" r="1.9" fill="#FFFFFF" opacity="0.95"/>
  <circle cx="12" cy="7" r="1.9" fill="#FFFFFF" opacity="0.95"/>
  <circle cx="16.8" cy="8.6" r="1.9" fill="#FFFFFF" opacity="0.95"/>
'''
    return svg(24, 24, body, "round paw dot")


# ---------------------------------------------------------------- socials
GITHUB_PATH = ("M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
               "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 "
               "3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 "
               "1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 "
               "0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 "
               "1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 "
               "2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 "
               "2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297"
               "c0-6.627-5.373-12-12-12")
X_PATH = ("M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 "
          "1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z")
MAIL_GLYPH = ('<rect x="2.5" y="5.5" width="19" height="13" rx="3.2" fill="none" stroke="#FFFFFF" stroke-width="2"/>'
              '<path d="M3.6 7.2 L12 13.4 L20.4 7.2" fill="none" stroke="#FFFFFF" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round"/>')
BLOG_GLYPH = ('<circle cx="12" cy="12" r="9" fill="none" stroke="#FFFFFF" stroke-width="2"/>'
              '<ellipse cx="12" cy="12" rx="4.2" ry="9" fill="none" stroke="#FFFFFF" stroke-width="1.8"/>'
              '<path d="M3 12 H21" stroke="#FFFFFF" stroke-width="1.8"/>')


def social(color: str, glyph: str, label: str) -> str:
    body = f'''\n  <circle cx="22" cy="22" r="20.5" fill="{color}" stroke="#FFFFFF" stroke-width="2"/>
  <g transform="translate(10,10)">{glyph}</g>
'''
    return svg(44, 44, body, label)


# ---------------------------------------------------------------- stats links
USER = "zcMia0"
CREAM_THEME = dict(
    bg_color="FFF8F0", title_color="B5838D", text_color="6B5A4F",
    icon_color="D98FA3", border_color="FFD6E0",
)
STATS_URL = (
    "https://github-readme-stats.vercel.app/api?username=zcMia0"
    "&show_icons=true&hide_border=false&border_radius=24&include_all_commits=true"
    "&disable_animations=true&locale=en&custom_title=my%20little%20stats"
    "&title_color=B5838D&text_color=6B5A4F&icon_color=D98FA3"
    "&bg_color=FFF8F0&border_color=FFD6E0"
)
LANGS_URL = (
    "https://github-readme-stats.vercel.app/api/top-langs/?username=zcMia0"
    "&layout=compact&langs_count=6&card_width=320&hide_border=false&border_radius=24"
    "&disable_animations=true&locale=en&custom_title=things%20i%20speak"
    "&title_color=B5838D&text_color=6B5A4F&bg_color=FFF8F0&border_color=FFD6E0"
)
STREAK_URL = (
    "https://streak-stats.demolab.com/?user=zcMia0"
    "&hide_border=true&border_radius=24&background=FFF8F0&border=FFD6E0"
    "&stroke=F3E4D2&ring=FFD6E0&fire=E8A0B4"
    "&currStreakNum=B5838D&sideNums=6B5A4F&currStreakLabel=B5838D"
    "&sideLabels=6B5A4F&dates=A9988A"
    "&disable_animations=true&mode=daily&type=svg"
)

DIV = '<p align="center"><img src="./assets/divider.svg" alt="┄" width="860"></p>'


def readme_body() -> str:
    p = PROFILE
    lang_rows = "<br>\n".join(
        f'        <img src="./assets/dot-{c}.svg" width="16" align="absmiddle" alt=""> &nbsp; {esc(v)}'
        for c, v in zip(["pink", "mint", "yellow", "pink"], p["languages"])
    )
    tool_rows = "<br>\n".join(
        f'        <img src="./assets/dot-{c}.svg" width="16" align="absmiddle" alt=""> &nbsp; {esc(v)}'
        for c, v in zip(["mint", "yellow", "pink", "mint"], p["tools"])
    )
    projects = "<br>\n".join(
        f'  {sq} &nbsp; <a href="{pr["url"]}"><b>{esc(pr["name"])}</b></a>'
        f' &nbsp;—&nbsp; {esc(pr["desc"])}'
        for sq, pr in zip(["🟧", "🟩", "🟨", "🟪"], p["projects"])
    )
    social_icons = "\n  &nbsp;&nbsp;\n".join(
        f'  <a href="{s["url"]}" title="{esc(s["title"])}">'
        f'<img src="./assets/{s["icon"]}" width="36" alt="{esc(s["title"])}"></a>'
        for s in p["social"]
    )
    now = p["now"]
    return f'''
<p align="center">
  <img src="./assets/banner.svg" alt="Hi, I'm {esc(p["name"])} 👋 nice to meet you!" width="860">
</p>

{DIV}

<!-- ① 关于我 · 聊天气泡 -->
<p align="center"><img src="./assets/title-about.svg" alt="about me" width="440"></p>
<p align="center"><img src="./assets/bubble.svg" alt="a little note from me 💬" width="760"></p>

{DIV}

<!-- ② 我在用的东西 · 两列 · 圆圆小图标 + 文字（不用徽章墙） -->
<p align="center"><img src="./assets/title-stack.svg" alt="things i use" width="440"></p>

<table align="center" width="100%" cellpadding="10">
  <tr>
    <td align="center" width="50%">
      <p align="center"><b>🐾 &nbsp; languages</b></p>
      <p align="center">
{lang_rows}
      </p>
    </td>
    <td align="center" width="50%">
      <p align="center"><b>🧸 &nbsp; tools</b></p>
      <p align="center">
{tool_rows}
      </p>
    </td>
  </tr>
</table>

{DIV}

<!-- ③ 我做过的小东西 -->
<p align="center"><img src="./assets/title-projects.svg" alt="little things i made" width="440"></p>

<p align="center">
{projects}
</p>

{DIV}

<!-- ④ 现在在干嘛 -->
<p align="center"><img src="./assets/title-now.svg" alt="right now" width="440"></p>

<p align="center">🍡 &nbsp; currently eating <b>{esc(now["eating"])}</b> &nbsp;·&nbsp; learning <b>{esc(now["learning"])}</b> &nbsp;·&nbsp; building <b>{esc(now["building"])}</b></p>

{DIV}

<!-- ⑤ 奶油色统计卡片（可选小尾巴，删掉这一整段也不影响结构） -->
<p align="center"><sub>tiny numbers, big feelings</sub></p>

<table align="center" cellpadding="6">
  <tr>
    <td align="center"><img src="{STATS_URL}" alt="GitHub stats for zcMia0" width="280"></td>
    <td align="center"><img src="{LANGS_URL}" alt="Top languages of zcMia0" width="280"></td>
    <td align="center"><img src="{STREAK_URL}" alt="Contribution streak of zcMia0" width="280"></td>
  </tr>
</table>

{DIV}

<!-- ⑥ 底部 -->
<p align="center">
{social_icons}
</p>

<p align="center"><sub>thanks for stopping by 💛</sub></p>
'''


README_COMMENT = '''<!-- ============================================================
     🌸 zcMia0 · GitHub profile README · 软萌日系 Q 版治愈风

     调色：奶油白 #FFF8F0 / 淡粉 #FFD6E0 / 薄荷绿 #C8E6D4 / 鹅黄 #FFE9A8
     全部资产在 ./assets/ ，为自包含静态 SVG（无 GIF、无打字机动画、无外链字体）。

     ── 内容已按真实资料填好，不再是占位符 ──────────────────────
     数据源：github.com/zcMia0 的公开 API 与仓库文件（采集于 2026-11-04）。
     界面文案集中在 profile.json，改完执行 python build.py 即可重建
     README.md、assets/*.svg 与 preview.html。逐条依据见 PROFILE_INFO.md。

     ── 想换主角？────────────────────────────────────────────
     1) 橘猫 ↔ 柴犬：python build.py --shiba / --cat
     2) 换成自己生成的图：python build.py --mascot assets/mascot.png
        （图片会被内嵌成 data URI，GitHub 上照样显示，无需外链）
     3) 改「关于我」三句话：编辑 profile.json 的 about_lines

     ── 统计卡片 ──────────────────────────────────────────────
     3 张卡片按 username=zcMia0 生成，用 bg_color=FFF8F0 等参数
     调成奶油色（不是默认紫），关掉动画、加了 24px 圆角。
     公共实例偶尔限流；若加载不出来可自托管。

     ── 分隔线：assets/divider.svg 是圆头虚线，未使用 Markdown 水平线 ─
     ============================================================ -->'''


def stats_fallback() -> str:
    body = f'''\n  <rect x="4" y="4" width="272" height="162" rx="24" fill="{CREAM}" stroke="{PINK}" stroke-width="2.5"/>
  <circle cx="140" cy="62" r="24" fill="{PINK}" opacity="0.7"/>
  {flower(140, 62, 12, PAPER, YELLOW_DEEP)}
  {T(140, 116, "stats card", 20, ROSE, 600, "middle")}
  {T(140, 140, "connect to load", 13, MUTED, 500, "middle")}
  <circle cx="52" cy="146" r="4" fill="{MINT_DEEP}"/>
  <circle cx="228" cy="146" r="4" fill="{YELLOW_DEEP}"/>
'''
    return svg(280, 170, body, "stats card placeholder")


def preview_html(body: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>zcMia0 · profile README 预览</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:28px 16px 60px; background:#F3EEE7;
         font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif; color:#6B5A4F; }}
  .note {{ max-width:900px; margin:0 auto 18px; padding:14px 18px; border-radius:18px;
          background:#FFF8F0; border:2px dashed #FFD6E0; font-size:13px; line-height:1.8; }}
  .note b {{ color:#B5838D; }}
  .sheet {{ max-width:900px; margin:0 auto; padding:34px 26px 44px; border-radius:28px;
           background:#FFFFFF; box-shadow:0 10px 34px rgba(107,90,79,.13); }}
  .sheet img {{ max-width:100%; height:auto; }}
  .sheet table {{ border-collapse:collapse; }}
  .sheet sub {{ font-size:14px; color:#A9988A; letter-spacing:.4px; }}
  .sheet b {{ color:#6B5A4F; }}
  .sheet a {{ color:#B5838D; text-decoration:none; }}
  .sheet a:hover {{ text-decoration:underline; }}
</style>
</head>
<body>
<div class="note">
  <b>🌸 预览说明</b> · 这是 README.md 在本机渲染的样子（与 GitHub 基本一致）。
  界面文案已按 <b>zcMia0 的真实公开资料</b> 填好，依据见 profile.json / PROFILE_INFO.md；
  三张统计卡片需要联网才能加载。所有装饰都是本地静态 SVG，没有 GIF、没有打字机动画。<br>
  灰白色底是为了模拟 GitHub 浅色主题；深底下这些奶油色 SVG 会像贴纸一样浮起来。
</div>
<div class="sheet">
{body}
</div>
<script>
  // 离线预览时，用同款奶油色占位卡片兜底（README.md 本身不需要这段）
  document.querySelectorAll('img[src^="http"]').forEach(function (im) {{
    var fallback = function () {{ im.onerror = null; im.src = './assets/stats-fallback.svg'; }};
    im.addEventListener('error', fallback);
    if (im.complete && im.naturalWidth === 0) fallback();
  }});
</script>
</body>
</html>
'''


# ---------------------------------------------------------------- write
def write(name: str, content: str):
    (ASSETS / name).write_text(content, encoding="utf-8")


def build_assets():
    write("banner.svg", banner("cat"))
    write("banner-shiba.svg", banner("shiba"))
    write("divider.svg", divider())
    write("title-about.svg", title_svg("about me", PINK, PINK_DEEP, "bubble", "about me"))
    write("title-stack.svg", title_svg("things i use", MINT, MINT_DEEP, "paw", "things i use"))
    write("title-projects.svg", title_svg("little things i made", YELLOW, YELLOW_DEEP, "gift", "little things i made"))
    write("title-now.svg", title_svg("right now", MINT, MINT_DEEP, "dango", "right now"))
    write("bubble.svg", bubble())
    write("dot-pink.svg", dot(PINK_DEEP))
    write("dot-mint.svg", dot(MINT_DEEP))
    write("dot-yellow.svg", dot(YELLOW_DEEP))
    write("ico-github.svg", social(PINK_DEEP, f'<path d="{GITHUB_PATH}" fill="#FFFFFF"/>', "GitHub"))
    write("ico-x.svg", social(MINT_DEEP, f'<path d="{X_PATH}" fill="#FFFFFF"/>', "X"))
    write("ico-mail.svg", social(YELLOW_DEEP, MAIL_GLYPH, "Email"))
    write("ico-blog.svg", social(PINK, BLOG_GLYPH, "Blog"))
    write("stats-fallback.svg", stats_fallback())


def build_docs():
    body = readme_body()
    (ROOT / "README.md").write_text(README_COMMENT + body, encoding="utf-8")
    (ROOT / "preview.html").write_text(preview_html(body), encoding="utf-8")


def embed(path: Path = None, url: str = None):
    if url:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=30).read()
        mime = mimetypes.guess_type(url.split("?")[0])[0] or "image/png"
    else:
        raw = path.read_bytes()
        mime = mimetypes.guess_type(str(path))[0] or "image/png"
        if mime == "image/svg+xml":
            mime = "image/svg+xml"
    b64 = base64.b64encode(raw).decode("ascii")
    (ASSETS / "banner.svg").write_text(
        banner("cat", embedded=(mime, b64)), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="生成软萌日系 GitHub profile README 资产")
    ap.add_argument("--shiba", action="store_true", help="横幅换成柴犬版")
    ap.add_argument("--cat", action="store_true", help="横幅换回橘猫版")
    ap.add_argument("--mascot", type=str, help="用本地图片重建横幅")
    ap.add_argument("--url", type=str, help="用网络图片重建横幅")
    ap.add_argument("--name", type=str, default=None, help="横幅里的名字（默认取 profile.json）")
    a = ap.parse_args()

    build_assets()
    build_docs()
    print("✓ assets/*.svg + README.md + preview.html 已生成")

    if a.shiba or a.cat:
        (ASSETS / "banner.svg").write_text(banner("shiba" if a.shiba else "cat", a.name), encoding="utf-8")
        print(f"✓ 横幅已切换为 {'柴犬' if a.shiba else '橘猫'}")
    if a.mascot or a.url:
        embed(Path(a.mascot) if a.mascot else None, a.url)
        print("✓ 横幅已用自定义小动物图重建（data URI 内嵌）")
    print(f"✓ 目录：{ROOT}")


if __name__ == "__main__":
    main()
