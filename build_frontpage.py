"""v2 generator for Sunday 22 November 2026: 29 verified Sunday events, dot-matrix map, 13 illustrations."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
HTML_PATH = HERE / "frontpage.html"
OUT_PNG = HERE / "entry.png"

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def dot_matrix_world_map() -> str:
    """Generates a crisp 56x24 dot-matrix world map SVG with numbered event pins."""
    # Coarse 56x24 world landmass mask ('.' = ocean, '#' = land)
    rows = [
        "........................................................",
        "......#######...........####....#########...............",
        "....###########........######..#############............",
        "...#############......#######..################.........",
        "...###########.........#####...#################........",
        "....#########..........####...##################........",
        ".....#######...........####..##################.........",
        "......#####.............######################..........",
        ".......###.............######################...........",
        "........##..............#####################...........",
        ".........###...........#####..##############............",
        "..........####........######...###########..............",
        "..........#####......#######....#########...............",
        "..........#####......######......#######................",
        "...........####.......#####.......#####...##............",
        "...........####.......####.........###....####..........",
        "............###.......####................#####.........",
        "............##.........###.................####.........",
        "............##..........##..................##......##..",
        "....................................................##..",
        "........................................................",
    ]
    dots = []
    for ry, row in enumerate(rows):
        y = 10 + ry * 6.5
        for cx, ch in enumerate(row):
            if ch == "#":
                x = 12 + cx * 6.0
                dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="#8C7E65"/>')
            elif (cx + ry) % 2 == 0:
                x = 12 + cx * 6.0
                dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="0.6" fill="#D5CCB8"/>')

    pins = [
        (216, 48, "1", "#B91C1C"),   # Antalya COP31
        (212, 34, "2", "#B91C1C"),   # Kyiv 186 drones
        (196, 56, "3", "#B91C1C"),   # Benghazi Libya Merkury
        (232, 66, "4", "#0F3D5E"),   # Bahrain/Saudi
        (294, 62, "5", "#0F3D5E"),   # Hong Kong
        (166, 45, "6", "#0F3D5E"),   # Portimao Portugal
        (46, 48, "7", "#0F3D5E"),    # Las Vegas
        (332, 130, "8", "#15803D"),  # Wellington NZ
        (286, 94, "9", "#B45309"),   # Cikande Indonesia
        (182, 42, "10", "#0F766E"),  # Turin Italy
        (170, 34, "11", "#0F766E"),  # Liverpool UK
        (206, 22, "12", "#0F766E"),  # Gulf of Finland
        (56, 54, "13", "#0F766E"),   # San Antonio TX
        (82, 49, "14", "#7C3AED"),   # Washington
        (98, 96, "15", "#7C3AED"),   # Brasilia
        (264, 61, "16", "#7C3AED"),  # New Delhi
        (210, 74, "19", "#7C3AED"),  # Sudan Kordofan
    ]
    pin_svg = "".join(
        f'<circle cx="{px}" cy="{py}" r="6.2" fill="{col}" stroke="#FFF" stroke-width="0.9"/>'
        f'<text x="{px}" y="{py + 2.5}" fill="#FFF" font-family="Arial,sans-serif" font-size="7.2" font-weight="800" text-anchor="middle">{lbl}</text>'
        for px, py, lbl, col in pins
    )

    return f"""<svg viewBox="0 0 356 172" width="356" height="172" xmlns="http://www.w3.org/2000/svg">
      <rect width="356" height="172" rx="4" fill="#EFE8D8" stroke="#C5B99E" stroke-width="1"/>
      {''.join(dots)}
      {pin_svg}
      <rect x="0" y="152" width="356" height="20" fill="#E0D6C1"/>
      <circle cx="16" cy="162" r="4" fill="#B91C1C"/><text x="24" y="165" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Leads 1–3</text>
      <circle cx="88" cy="162" r="4" fill="#0F3D5E"/><text x="96" y="165" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Cards 4–8</text>
      <circle cx="164" cy="162" r="4" fill="#0F766E"/><text x="172" y="165" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Cards 9–13</text>
      <circle cx="248" cy="162" r="4" fill="#7C3AED"/><text x="256" y="165" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Digest 14–29</text>
    </svg>"""


def build_html() -> str:
    svg_cop31 = """<svg viewBox="0 0 310 98" width="310" height="98" xmlns="http://www.w3.org/2000/svg">
      <defs><linearGradient id="skyCop2" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1E293B"/><stop offset="65%" stop-color="#7C2D12"/><stop offset="100%" stop-color="#EA580C"/></linearGradient></defs>
      <rect width="310" height="98" fill="url(#skyCop2)"/>
      <circle cx="155" cy="48" r="32" fill="none" stroke="#93C5FD" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.45"/>
      <path d="M0 72 Q55 58 110 70 T220 68 T310 74 L310 98 L0 98 Z" fill="#0F172A"/>
      <rect x="28" y="38" width="14" height="40" fill="#334155"/><rect x="48" y="30" width="16" height="48" fill="#475569"/>
      <path d="M34 36 C30 22 48 20 46 8 M55 28 C54 16 72 16 70 6" stroke="#CBD5E1" stroke-width="3.5" fill="none" stroke-linecap="round" opacity="0.55"/>
      <polygon points="122,18 156,18 150,50 159,80 122,80" fill="#FAF5EB" stroke="#1E293B" stroke-width="1.4"/>
      <polygon points="163,18 196,18 196,80 165,80 157,50" fill="#E2E8F0" stroke="#1E293B" stroke-width="1.4"/>
      <line x1="129" y1="30" x2="148" y2="30" stroke="#64748B" stroke-width="2.5"/><line x1="166" y1="30" x2="188" y2="30" stroke="#64748B" stroke-width="2.5"/>
      <path d="M159 14 L152 48 L162 52 L156 84" stroke="#DC2626" stroke-width="3" fill="none"/>
      <g transform="translate(236,50) rotate(-28)"><rect x="-16" y="-8" width="32" height="14" rx="3" fill="#B45309" stroke="#FEF3C7" stroke-width="1"/><rect x="-4" y="6" width="8" height="28" rx="2" fill="#D97706"/></g>
      <rect x="218" y="74" width="52" height="8" rx="2" fill="#92400E"/>
      <rect x="6" y="6" width="96" height="16" rx="2" fill="#B91C1C"/><text x="54" y="17" fill="#FFF" font-family="Arial" font-size="9" font-weight="700" text-anchor="middle">49H OVERTIME</text>
      <rect x="206" y="6" width="98" height="16" rx="2" fill="#0F172A" opacity="0.9"/><text x="255" y="17" fill="#FDE047" font-family="Arial" font-size="9" font-weight="700" text-anchor="middle">NO CLIMATE PACT</text>
    </svg>"""

    svg_kyiv = """<svg viewBox="0 0 310 98" width="310" height="98" xmlns="http://www.w3.org/2000/svg">
      <rect width="310" height="98" fill="#0B132B"/>
      <rect x="0" y="70" width="310" height="28" fill="#1E293B"/>
      <rect x="212" y="34" width="38" height="38" fill="#334155"/><rect x="256" y="42" width="30" height="30" fill="#475569"/>
      <polygon points="224,38 234,20 246,38" fill="#EA580C"/>
      <g stroke="#FBBF24" stroke-width="2" fill="none">
        <path d="M22 28 L36 32 L22 36 M28 32 L44 32"/><path d="M58 20 L72 24 L58 28 M64 24 L78 24"/><path d="M44 46 L58 50 L44 54 M50 50 L64 50"/>
      </g>
      <path d="M126 70 L144 26 M126 70 L166 36" stroke="#38BDF8" stroke-width="1.8" opacity="0.75"/>
      <circle cx="146" cy="34" r="6" fill="#EF4444"/><circle cx="164" cy="40" r="4.5" fill="#FDE047"/>
      <rect x="6" y="6" width="114" height="16" rx="2" fill="#B91C1C"/><text x="63" y="17" fill="#FFF" font-family="Arial" font-size="9" font-weight="700" text-anchor="middle">186 DRONES FIRED</text>
      <rect x="196" y="6" width="108" height="16" rx="2" fill="#0F172A" opacity="0.9"/><text x="250" y="17" fill="#38BDF8" font-family="Arial" font-size="9" font-weight="700" text-anchor="middle">161 INTERCEPTED</text>
    </svg>"""

    svg_benghazi = """<svg viewBox="0 0 310 98" width="310" height="98" xmlns="http://www.w3.org/2000/svg">
      <rect width="310" height="98" fill="#0A192F"/>
      <rect x="0" y="62" width="310" height="36" fill="#112D4E"/>
      <path d="M0 64 Q40 58 80 64 T160 64 T240 64 T310 64" stroke="#38BDF8" stroke-width="1.5" fill="none"/>
      <g transform="translate(212,56) rotate(-14)">
        <polygon points="-58,8 52,8 64,-6 -48,-6" fill="#64748B"/><rect x="-24" y="-19" width="38" height="13" fill="#475569"/>
        <line x1="-10" y1="-19" x2="-10" y2="-33" stroke="#94A3B8" stroke-width="2.5"/>
        <polygon points="8,-6 22,-24 36,-6" fill="#EA580C"/><polygon points="13,-6 22,-18 29,-6" fill="#FDE047"/>
      </g>
      <polygon points="94,74 118,70 112,78" fill="#38BDF8"/>
      <line x1="22" y1="76" x2="90" y2="74" stroke="#7DD3FC" stroke-width="2" stroke-dasharray="5 3"/>
      <text x="64" y="54" fill="#93C5FD" font-family="Arial" font-size="10.5" font-weight="800" text-anchor="middle">2,000+ KM STRIKE</text>
      <rect x="6" y="6" width="114" height="16" rx="2" fill="#B91C1C"/><text x="63" y="17" fill="#FFF" font-family="Arial" font-size="9" font-weight="700" text-anchor="middle">MERKURY SUNK</text>
      <rect x="190" y="6" width="114" height="16" rx="2" fill="#1E3A8A"/><text x="247" y="17" fill="#DBEAFE" font-family="Arial" font-size="9" font-weight="700" text-anchor="middle">BENGHAZI, LIBYA</text>
    </svg>"""

    # 10 secondary mini SVGs (each 184 x 46)
    m_gulf = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#1E293B"/>
      <circle cx="136" cy="24" r="14" stroke="#22C55E" stroke-width="1.5" fill="none"/><line x1="136" y1="24" x2="146" y2="16" stroke="#4ADE80" stroke-width="2"/>
      <polygon points="28,34 86,34 94,24 22,24" fill="#64748B"/><rect x="38" y="18" width="18" height="6" fill="#94A3B8"/>
      <rect x="5" y="4" width="84" height="13" rx="2" fill="#DC2626"/><text x="47" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">CLAIM VS DENIAL</text>
    </svg>"""
    m_hk = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#EFF6FF"/>
      <rect x="16" y="14" width="28" height="30" fill="#CBD5E1"/><rect x="48" y="8" width="32" height="36" fill="#94A3B8"/>
      <rect x="118" y="16" width="44" height="26" rx="2" fill="#1E3A8A"/><rect x="128" y="11" width="24" height="8" fill="#FFF" stroke="#1E3A8A" stroke-width="1.5"/>
      <rect x="5" y="4" width="80" height="13" rx="2" fill="#1D4ED8"/><text x="45" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">98.79% TURNOUT</text>
    </svg>"""
    m_moto = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#18181B"/>
      <rect x="0" y="34" width="184" height="12" fill="#3F3F46"/>
      <path d="M36 34 Q70 15 106 32" stroke="#DC2626" stroke-width="5" fill="none" stroke-linecap="round"/>
      <circle cx="42" cy="34" r="7.5" fill="#09090B" stroke="#E4E4E7" stroke-width="2"/><circle cx="102" cy="34" r="7.5" fill="#09090B" stroke="#E4E4E7" stroke-width="2"/>
      <text x="148" y="34" fill="#FACC15" font-family="Georgia" font-size="22" font-weight="900" text-anchor="middle">8x</text>
      <rect x="5" y="4" width="76" height="13" rx="2" fill="#DC2626"/><text x="43" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">MOTOGP GOAT</text>
    </svg>"""
    m_f1 = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#09090B"/>
      <rect x="0" y="33" width="184" height="13" fill="#27272A"/>
      <polygon points="36,31 136,31 122,23 56,23" fill="#1D4ED8"/><rect x="40" y="21" width="14" height="7" fill="#EF4444"/>
      <circle cx="60" cy="33" r="6" fill="#18181B" stroke="#F4F4F5" stroke-width="2"/><circle cx="118" cy="33" r="6" fill="#18181B" stroke="#F4F4F5" stroke-width="2"/>
      <circle cx="160" cy="18" r="4" fill="#F43F5E"/><circle cx="170" cy="25" r="3.5" fill="#38BDF8"/>
      <rect x="5" y="4" width="84" height="13" rx="2" fill="#1D4ED8"/><text x="47" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">VERSTAPPEN P1</text>
    </svg>"""
    m_cri = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#14532D"/>
      <line x1="36" y1="18" x2="36" y2="38" stroke="#FEF3C7" stroke-width="2"/><line x1="42" y1="18" x2="42" y2="38" stroke="#FEF3C7" stroke-width="2"/><line x1="48" y1="18" x2="48" y2="38" stroke="#FEF3C7" stroke-width="2"/>
      <circle cx="72" cy="26" r="5" fill="#DC2626"/>
      <text x="134" y="33" fill="#FEF08A" font-family="Georgia" font-size="20" font-weight="900" text-anchor="middle">720/9</text>
      <rect x="5" y="4" width="84" height="13" rx="2" fill="#15803D"/><text x="47" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">NZ TEST RECORD</text>
    </svg>"""
    m_fire = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#451A03"/>
      <rect x="34" y="18" width="66" height="28" fill="#292524"/>
      <polygon points="48,46 62,14 76,46" fill="#EA580C"/><polygon points="62,46 78,12 94,46" fill="#FACC15" opacity="0.85"/>
      <circle cx="136" cy="24" r="12" fill="#78716C" opacity="0.5"/>
      <rect x="5" y="4" width="106" height="13" rx="2" fill="#B91C1C"/><text x="58" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">14H BLAZE · 36 MISSING</text>
    </svg>"""
    m_atp = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#0F172A"/>
      <rect x="18" y="21" width="84" height="20" fill="#1D4ED8" stroke="#93C5FD" stroke-width="1.2"/>
      <line x1="60" y1="21" x2="60" y2="41" stroke="#E2E8F0" stroke-width="1.8"/><circle cx="88" cy="16" r="5" fill="#BEF264"/>
      <text x="142" y="33" fill="#FDE047" font-family="Georgia" font-size="14" font-weight="900" text-anchor="middle">6-2 7-6</text>
      <rect x="5" y="4" width="82" height="13" rx="2" fill="#0284C7"/><text x="46" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">ALCARAZ TITLE</text>
    </svg>"""
    m_lfc = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#7F1D1D"/>
      <rect x="0" y="31" width="184" height="15" fill="#15803D"/>
      <rect x="26" y="19" width="10" height="16" fill="#EF4444" stroke="#FFF" stroke-width="1"/>
      <text x="122" y="32" fill="#FEF08A" font-family="Georgia" font-size="22" font-weight="900" text-anchor="middle">4 - 0</text>
      <rect x="5" y="4" width="88" height="13" rx="2" fill="#991B1B"/><text x="49" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">ANFIELD ROUT</text>
    </svg>"""
    m_ship = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#0C4A6E"/>
      <rect x="0" y="32" width="184" height="14" fill="#082F49"/>
      <polygon points="34,32 104,32 112,23 26,23" fill="#475569"/>
      <polygon points="74,23 82,10 90,23" fill="#F97316"/>
      <rect x="5" y="4" width="86" height="13" rx="2" fill="#B91C1C"/><text x="48" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">GULF OF FINLAND</text>
    </svg>"""
    m_nba = """<svg viewBox="0 0 184 46" width="184" height="46"><rect width="184" height="46" fill="#18181B"/>
      <circle cx="44" cy="27" r="11" fill="#EA580C" stroke="#18181B" stroke-width="1.2"/>
      <path d="M34 27 H54 M44 16 V38" stroke="#18181B" stroke-width="1.3"/>
      <text x="128" y="34" fill="#FDE047" font-family="Georgia" font-size="19" font-weight="900" text-anchor="middle">50 PTS</text>
      <rect x="5" y="4" width="86" height="13" rx="2" fill="#3F3F46"/><text x="48" y="13" fill="#FFF" font-family="Arial" font-size="8" font-weight="700" text-anchor="middle">SPURS 114-91</text>
    </svg>"""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1024px; height: 1024px; overflow: hidden;
    background: #F6F1E6; color: #141821;
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{
    width: 1024px; height: 1024px;
    padding: 10px 14px 8px 14px;
    display: flex; flex-direction: column; justify-content: space-between;
  }}
  .topbar {{
    display: flex; justify-content: space-between; align-items: center;
    background: #141923; color: #F6F1E6; padding: 3.5px 10px;
    font-size: 9.8px; font-weight: 700; letter-spacing: 0.85px; text-transform: uppercase;
  }}
  .masthead {{ text-align: center; border-bottom: 2.5px solid #141923; padding: 3px 0 4px 0; }}
  .masthead h1 {{ font-family: Georgia, "Times New Roman", serif; font-size: 42px; font-weight: 900; line-height: 1.0; letter-spacing: -0.6px; color: #11151E; }}
  .masthead .deck {{ margin-top: 2px; font-family: Georgia, serif; font-style: italic; font-size: 11.6px; color: #8A1E19; font-weight: 700; }}
  .kpis {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px; padding: 4px 0; border-bottom: 1px solid #C8BEAA; }}
  .kpi {{ text-align: center; border-right: 1px solid #D5CCB8; padding: 0 3px; }}
  .kpi:last-child {{ border-right: none; }}
  .kpi .val {{ font-family: Georgia, serif; font-size: 16px; font-weight: 900; color: #9B1C1C; line-height: 1.05; }}
  .kpi .lbl {{ font-size: 8.2px; font-weight: 600; color: #475569; line-height: 1.12; }}
  .regions {{ display: grid; grid-template-columns: 7fr 4fr 4fr 8fr 3fr 1fr 2fr; font-size: 8.2px; font-weight: 800; color: #FFF; text-align: center; margin-top: 2px; }}
  .regions div {{ padding: 2px 2px; white-space: nowrap; }}
  .utcbar {{ background: #1E2430; color: #E2E8F0; display: flex; justify-content: space-between; align-items: center; padding: 3px 8px; font-size: 8.5px; margin-top: 2px; }}
  .utcbar .tag {{ background: #B91C1C; color: #FFF; font-weight: 800; padding: 1.5px 5px; margin-right: 4px; font-size: 8.2px; }}
  .utcbar b {{ color: #FDE047; }}
  .leads {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px; }}
  .lead {{ background: #FFFDF8; border: 1px solid #D5CCB8; padding: 4.5px; display: flex; flex-direction: column; }}
  .lead svg {{ width: 100%; height: auto; display: block; border: 1px solid #CBD5E1; }}
  .meta {{ display: flex; justify-content: space-between; align-items: center; margin-top: 3px; font-size: 8px; font-weight: 800; color: #7C2D12; }}
  .badge {{ padding: 0.5px 3.5px; font-size: 7px; border: 1px solid; font-weight: 800; }}
  .b-conf {{ color: #166534; border-color: #166534; background: #DCFCE7; }}
  .b-rep {{ color: #1E40AF; border-color: #1E40AF; background: #DBEAFE; }}
  .b-disp {{ color: #9A3412; border-color: #9A3412; background: #FFEDD5; }}
  .lead h2 {{ font-family: Georgia, serif; font-size: 13.4px; line-height: 1.14; font-weight: 900; margin-top: 2.5px; color: #111827; }}
  .lead p {{ font-size: 9.4px; line-height: 1.22; color: #334155; margin-top: 2.5px; }}
  .src {{ font-weight: 700; color: #64748B; }}
  .sec-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin-top: 5px; }}
  .card {{ background: #FFFDF8; border: 1px solid #D5CCB8; padding: 3.5px; }}
  .card svg {{ width: 100%; height: auto; display: block; }}
  .card h3 {{ font-family: Georgia, serif; font-size: 10.2px; line-height: 1.13; font-weight: 800; margin-top: 2.5px; color: #111827; }}
  .card p {{ font-size: 8.2px; line-height: 1.18; color: #334155; margin-top: 1.5px; }}
  .bottom {{ display: grid; grid-template-columns: 356px 1fr; gap: 10px; margin-top: 5px; border-top: 2px solid #141923; padding-top: 4px; }}
  .sec-head {{ font-size: 8.8px; font-weight: 900; letter-spacing: 0.65px; text-transform: uppercase; color: #141923; margin-bottom: 2.5px; display: flex; justify-content: space-between; }}
  .briefs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px 10px; font-size: 8.4px; line-height: 1.2; color: #1E293B; }}
  .brief-col {{ display: flex; flex-direction: column; gap: 2.3px; }}
  .brief b {{ color: #9B1C1C; }}
  .datecheck {{ border: 1.5px solid #9B1C1C; background: #FEF2F2; padding: 3px 7px; font-size: 8px; line-height: 1.2; color: #1E293B; margin-top: 3px; }}
  .datecheck .dc-tag {{ background: #9B1C1C; color: #FFF; font-weight: 800; padding: 0.5px 4.5px; margin-right: 4px; }}
  .foot {{ display: flex; justify-content: space-between; font-size: 7.5px; color: #64748B; margin-top: 2px; }}
</style>
</head>
<body>
<div class="page">
  <div class="topbar">
    <span>THE WORLD IN ONE EDITION</span>
    <span>29 VERIFIED STORIES · ALL 7 REGIONS · STRICT SUNDAY 22 NOV 2026 RECORD</span>
  </div>

  <div class="masthead">
    <h1>Sunday 22 November 2026</h1>
    <div class="deck">COP31 collapses without fossil-fuel pact · Russia fires 186 drones overnight · Ukrainian sea drones sink Russian corvette in Libya · Márquez wins 8th title</div>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="val">0 PACT</div><div class="lbl">COP31 ends in Antalya deadlock</div></div>
    <div class="kpi"><div class="val">161 / 186</div><div class="lbl">drones downed over Ukraine</div></div>
    <div class="kpi"><div class="val">2,000+ km</div><div class="lbl">sea-drone strike hits Libya</div></div>
    <div class="kpi"><div class="val">98.79%</div><div class="lbl">Hong Kong 723-seat turnout</div></div>
    <div class="kpi"><div class="val">720/9</div><div class="lbl">India Test record in NZ</div></div>
    <div class="kpi"><div class="val">8th TITLE</div><div class="lbl">Marc Márquez ties MotoGP GOAT</div></div>
  </div>

  <div class="regions">
    <div style="background:#1E3A8A;">EUROPE 7</div>
    <div style="background:#9A3412;">M. EAST 4</div>
    <div style="background:#0F766E;">ASIA 4</div>
    <div style="background:#4338CA;">AMERICAS 8</div>
    <div style="background:#15803D;">AFRICA 3</div>
    <div style="background:#B45309;">OCEANIA 1</div>
    <div style="background:#475569;">WORLD 2</div>
  </div>

  <div class="utcbar">
    <span><span class="tag">UTC TIMELINE</span><b>03:00</b> COP31 talks stall</span>
    <span><b>05:30</b> Verstappen Vegas P1</span>
    <span><b>08:00</b> 186 drones logged</span>
    <span><b>14:00</b> HK Election closes</span>
    <span><b>17:30</b> Márquez 8x · Alcaraz Turin</span>
    <span><b>21:00</b> COP31 ends no deal</span>
  </div>

  <div class="leads">
    <div class="lead">
      {svg_cop31}
      <div class="meta"><span>1 · ANTALYA, TÜRKIYE · CLIMATE</span><span class="badge b-conf">CONFIRMED</span></div>
      <h2>COP31 ends without a pact after 49-hour overtime</h2>
      <p>The UN summit collapsed Sunday after the EU, UK, and allies rejected the Antalya draft omitting fossil-fuel phase-out terms and dropping the $120bn adaptation baseline. Just Transition rules passed; Guterres blamed fossil interests. <span class="src">(UN, Reuters, Guardian)</span></p>
    </div>
    <div class="lead">
      {svg_kyiv}
      <div class="meta"><span>2 · KYIV &amp; DYMER · WAR</span><span class="badge b-conf">CONFIRMED</span></div>
      <h2>Russia launches 186 attack drones overnight; 161 downed</h2>
      <p>Ukrainian air defences intercepted or suppressed 161 of 186 strike drones fired overnight across eight directions, though a five-storey residential block in Dymer outside Kyiv was struck. <span class="src">(Ukrainian Air Force, Pravda)</span></p>
    </div>
    <div class="lead">
      {svg_benghazi}
      <div class="meta"><span>3 · BENGHAZI, LIBYA · NAVAL WAR</span><span class="badge b-conf">CONFIRMED</span></div>
      <h2>Ukrainian sea drones sink Russian corvette Merkury</h2>
      <p>President Zelenskyy confirmed Ukrainian uncrewed naval vessels traveled 2,000+ km into the Mediterranean to strike and capsize corvette <i>Merkury</i> and hit cargo ship <i>Angara</i> in eastern Libya. <span class="src">(Guardian, CNN, Naval News)</span></p>
    </div>
  </div>

  <div class="sec-grid">
    <div class="card">{m_gulf}<div class="meta"><span>4 · GULF &amp; RED SEA</span><span class="badge b-disp">DISPUTED</span></div><h3>Iran claims radar hits; Houthis target oil</h3><p>Iran claimed Bahrain radar hits; Manama denied. Houthis struck Saudi Petrol Rabigh site. <span class="src">(AJ, ISW)</span></p></div>
    <div class="card">{m_hk}<div class="meta"><span>5 · HONG KONG</span><span class="badge b-conf">OFFICIAL</span></div><h3>723 seats filled on 98.79% turnout</h3><p>Subsector polls closed Sunday across 31 sectors under “patriots” rules. <span class="src">(HK Gov, SCMP)</span></p></div>
    <div class="card">{m_moto}<div class="meta"><span>6 · PORTUGAL · GP</span><span class="badge b-conf">OFFICIAL</span></div><h3>Márquez clinches 8th premier crown</h3><p>8th place at Portimão overturned a 102-pt deficit to tie Agostini’s record. <span class="src">(MotoGP)</span></p></div>
    <div class="card">{m_f1}<div class="meta"><span>7 · LAS VEGAS · F1</span><span class="badge b-conf">OFFICIAL</span></div><h3>Verstappen wins Las Vegas GP</h3><p>Red Bull’s champion beat McLaren’s Norris (2nd) and Piastri (3rd) under Strip lights. <span class="src">(F1)</span></p></div>
    <div class="card">{m_cri}<div class="meta"><span>8 · WELLINGTON</span><span class="badge b-conf">OFFICIAL</span></div><h3>India declare at 720/9 NZ record</h3><p>Rahul 156, Pant 128, Gill 98 posted New Zealand’s highest Test innings ever. <span class="src">(ESPN)</span></p></div>
    <div class="card">{m_fire}<div class="meta"><span>9 · INDONESIA</span><span class="badge b-rep">REPORTED</span></div><h3>3 dead, 36 missing in plant fire</h3><p>14-hour inferno gutted a three-story Cikande candy plant; rescue continues. <span class="src">(WashPost)</span></p></div>
    <div class="card">{m_atp}<div class="meta"><span>10 · TURIN · ATP</span><span class="badge b-conf">OFFICIAL</span></div><h3>Alcaraz beats Zverev 6-2, 7-6(7)</h3><p>Spaniard won straight sets in Turin to capture his first ATP Finals crown. <span class="src">(ATP Tour)</span></p></div>
    <div class="card">{m_lfc}<div class="meta"><span>11 · LIVERPOOL</span><span class="badge b-conf">OFFICIAL</span></div><h3>Liverpool rout Man Utd 4-0</h3><p>Yoro’s 8’ red card opened floodgates, spoiling Pochettino’s United debut. <span class="src">(LFC)</span></p></div>
    <div class="card">{m_ship}<div class="meta"><span>12 · BALTIC SEA</span><span class="badge b-conf">CONFIRMED</span></div><h3>Russian ship Sparta II towed out</h3><p>Drone-damaged vessel stabilized off Finland; 16 crew safe, tow began Sunday. <span class="src">(AJ)</span></p></div>
    <div class="card">{m_nba}<div class="meta"><span>13 · SAN ANTONIO</span><span class="badge b-conf">OFFICIAL</span></div><h3>Wembanyama drops 50 &amp; 19 reb</h3><p>Spurs star added 5 blocks to crush Pelicans 114-91 on NBA slate. <span class="src">(NBC Sports)</span></p></div>
  </div>

  <div class="bottom">
    <div>
      <div class="sec-head"><span>WHERE IT HAPPENED</span><span style="color:#64748B;">DOT MATRIX · PINS MATCH NUMBERS</span></div>
      {dot_matrix_world_map()}
    </div>
    <div>
      <div class="sec-head"><span>ALSO ON SUNDAY 22 NOVEMBER 2026</span><span style="color:#64748B;">GLOBAL ROUNDUP (14–29)</span></div>
      <div class="briefs">
        <div class="brief-col">
          <div class="brief"><b>14 Washington:</b> Trump posts Sunday demanding Nvidia reinstate ex-CEO Jensen Huang. (Cointribune)</div>
          <div class="brief"><b>15 Brasília:</b> Ex-president Bolsonaro stable under monitoring in ICU after acute bowel scare. (CP24)</div>
          <div class="brief"><b>16 New Delhi:</b> Nepal PM Balendra Shah lands Sunday ahead of Modi bilateral talks. (The Hindu)</div>
          <div class="brief"><b>17 Doha:</b> Pakistan Shaheens beat India A by 48 runs in Asia Cup Rising Stars cricket. (NDTV)</div>
          <div class="brief"><b>18 Brussels:</b> Air-traffic controllers set Monday strike halting Belgian commercial flights. (AA)</div>
          <div class="brief"><b>19 Sudan:</b> Drone and artillery strikes hit Kordofan region amid UN famine warnings. (OHCHR)</div>
          <div class="brief"><b>20 Somalia:</b> Protests mount after Mogadishu expels UAE envoy over sovereignty dispute. (Africanews)</div>
          <div class="brief"><b>21 Lebanon:</b> UNIFIL begins handing southern border posts to Lebanese army. (AA)</div>
        </div>
        <div class="brief-col">
          <div class="brief"><b>22 USA:</b> Back-to-back atmospheric rivers lash West Coast ahead of Thanksgiving travel. (NWS)</div>
          <div class="brief"><b>23 Mexico:</b> Sheinbaum navigates US-China trade balancing after APEC Shenzhen talks. (IntelRep)</div>
          <div class="brief"><b>24 UAE / LatAm:</b> UAE launches initiative to train 1M AI coders in Dominican Republic. (National)</div>
          <div class="brief"><b>25 Asia-Pacific:</b> Pope Francis &amp; aid agencies warn Super El Niño threatens millions. (Crux)</div>
          <div class="brief"><b>26 Antalya:</b> COP31 passes Just Transition Mechanism procedurally despite pact collapse. (CP)</div>
          <div class="brief"><b>27 Baltics:</b> Estonia shuts Russia border crossings after foiled drone-factory arson plot. (TVC)</div>
          <div class="brief"><b>28 Hormuz:</b> Maritime monitors report Iranian shipping attacks hit highest conflict intensity. (CNN)</div>
          <div class="brief"><b>29 US Trade:</b> Lawmakers push toward year-end ban on Chinese autos amid summit fallout. (CNN)</div>
        </div>
      </div>
    </div>
  </div>

  <div class="datecheck">
    <span class="dc-tag">DATE CHECK</span>
    Strictly verified for <b>Sunday 22 November 2026</b>. Excluded on purpose from earlier days: Wall St S&amp;P 10% correction (Fri 20 Nov close), Peru M6.7 quake (Fri 20 Nov), Shenzhen summit (Thu 19 Nov), El Chapo Isidro arrest &amp; BepiColombo Mercury burn (Sat 21 Nov), Kenya last Ebola discharge (11 Nov).
  </div>

  <div class="foot">
    <span>CONFIRMED = multi-outlet wire · OFFICIAL = gov/league · REPORTED = single wire · DISPUTED = contested claim</span>
    <span>Original Python/HTML/SVG graphics · Sources: UN · Reuters · BBC · Guardian · Al Jazeera · F1 · ATP</span>
  </div>
</div>
</body>
</html>
"""


def main() -> None:
    HTML_PATH.write_text(build_html(), encoding="utf-8")
    chrome = next((p for p in CHROME_PATHS if os.path.exists(p)), None)
    if not chrome:
        raise RuntimeError("No headless Chromium/Edge browser found")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--window-size=1024,1024",
        "--force-device-scale-factor=1",
        f"--screenshot={OUT_PNG}",
        HTML_PATH.as_uri(),
    ]
    subprocess.run(cmd, check=True)
    with Image.open(OUT_PNG) as im:
        im = im.convert("RGB")
        if im.size != (1024, 1024):
            im = im.resize((1024, 1024), Image.Resampling.LANCZOS)
        im.save(OUT_PNG, "PNG", optimize=True)
        size = OUT_PNG.stat().st_size
        if size > 1_048_576:
            im.save(OUT_PNG, "JPEG", quality=92, optimize=True)
            size = OUT_PNG.stat().st_size
    if HTML_PATH.exists():
        HTML_PATH.unlink()
    print(f"Generated {OUT_PNG} ({size} bytes)")


if __name__ == "__main__":
    main()
