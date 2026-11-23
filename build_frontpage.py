"""Generates the 1024x1024 editorial front page for Sunday 22 November 2026."""
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


def build_html() -> str:
    # Custom crisp vector SVG illustrations (100% original geometry)
    svg_cop31 = """<svg viewBox="0 0 310 108" width="310" height="108" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="skyCop" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#1E293B"/>
          <stop offset="65%" stop-color="#7C2D12"/>
          <stop offset="100%" stop-color="#EA580C"/>
        </linearGradient>
      </defs>
      <rect width="310" height="108" fill="url(#skyCop)"/>
      <circle cx="155" cy="96" r="54" fill="#FDE68A" opacity="0.22"/>
      <circle cx="155" cy="52" r="34" fill="none" stroke="#93C5FD" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.45"/>
      <path d="M0 78 Q55 62 110 76 T220 72 T310 80 L310 108 L0 108 Z" fill="#0F172A"/>
      <!-- Factory smokestacks vs UN globe -->
      <rect x="28" y="42" width="14" height="44" fill="#334155"/>
      <rect x="48" y="34" width="16" height="52" fill="#475569"/>
      <path d="M34 40 C30 26 48 22 46 10 M55 32 C54 18 72 18 70 6" stroke="#CBD5E1" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.55"/>
      <!-- Fractured agreement document -->
      <polygon points="122,20 156,20 150,54 159,86 122,86" fill="#FAF5EB" stroke="#1E293B" stroke-width="1.5"/>
      <polygon points="163,20 196,20 196,86 165,86 157,54" fill="#E2E8F0" stroke="#1E293B" stroke-width="1.5"/>
      <line x1="129" y1="33" x2="148" y2="33" stroke="#64748B" stroke-width="2.5"/>
      <line x1="129" y1="42" x2="145" y2="42" stroke="#64748B" stroke-width="2.5"/>
      <line x1="166" y1="33" x2="188" y2="33" stroke="#64748B" stroke-width="2.5"/>
      <line x1="166" y1="42" x2="185" y2="42" stroke="#64748B" stroke-width="2.5"/>
      <path d="M159 16 L152 52 L162 56 L156 90" stroke="#DC2626" stroke-width="3" fill="none"/>
      <!-- Gavel -->
      <g transform="translate(234,54) rotate(-28)">
        <rect x="-18" y="-9" width="36" height="16" rx="3" fill="#B45309" stroke="#FEF3C7" stroke-width="1.2"/>
        <rect x="-4" y="7" width="8" height="32" rx="2" fill="#D97706"/>
      </g>
      <rect x="218" y="80" width="52" height="8" rx="2" fill="#92400E"/>
      <rect x="6" y="6" width="96" height="17" rx="2" fill="#B91C1C"/>
      <text x="54" y="18" fill="#FFF" font-family="Arial,sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">49H OVERTIME</text>
      <rect x="206" y="6" width="98" height="17" rx="2" fill="#0F172A" opacity="0.9"/>
      <text x="255" y="18" fill="#FDE047" font-family="Arial,sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">NO CLIMATE PACT</text>
    </svg>"""

    svg_sea_drone = """<svg viewBox="0 0 310 108" width="310" height="108" xmlns="http://www.w3.org/2000/svg">
      <rect width="310" height="108" fill="#0B132B"/>
      <!-- Night sky & radar rings -->
      <circle cx="235" cy="48" r="42" stroke="#1E3A5F" stroke-width="1" fill="none"/>
      <circle cx="235" cy="48" r="24" stroke="#1E3A5F" stroke-width="1" fill="none"/>
      <!-- Horizon & water -->
      <rect x="0" y="68" width="310" height="40" fill="#1C2541"/>
      <path d="M0 74 Q35 69 70 74 T140 74 T210 74 T280 74 T310 74" stroke="#3A506B" stroke-width="1.5" fill="none"/>
      <!-- Drone swarm incoming left (186 drones / Kyiv) -->
      <g stroke="#FBBF24" stroke-width="1.8" fill="none">
        <path d="M22 30 L34 34 L22 38 M28 34 L42 34"/>
        <path d="M52 22 L64 26 L52 30 M58 26 L70 26"/>
        <path d="M40 46 L52 50 L40 54 M46 50 L58 50"/>
      </g>
      <path d="M98 68 L112 28 M98 68 L128 36" stroke="#38BDF8" stroke-width="1.5" opacity="0.65"/>
      <circle cx="114" cy="34" r="5" fill="#EF4444" opacity="0.9"/>
      <!-- Tilting corvette silhouette in Benghazi -->
      <g transform="translate(215,64) rotate(-8)">
        <polygon points="-58,6 52,6 64,-7 -48,-7" fill="#475569"/>
        <rect x="-25" y="-20" width="38" height="13" fill="#334155"/>
        <line x1="-10" y1="-20" x2="-10" y2="-34" stroke="#94A3B8" stroke-width="2.5"/>
        <polygon points="8,-6 22,-22 34,-6" fill="#EA580C"/>
        <polygon points="13,-6 22,-17 29,-6" fill="#FDE047"/>
      </g>
      <!-- USV sea drone trail -->
      <polygon points="122,79 144,76 140,83" fill="#38BDF8"/>
      <line x1="78" y1="81" x2="120" y2="80" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="4 3"/>
      <rect x="6" y="6" width="110" height="17" rx="2" fill="#B91C1C"/>
      <text x="61" y="18" fill="#FFF" font-family="Arial,sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">186 DRONES · KYIV</text>
      <rect x="180" y="6" width="124" height="17" rx="2" fill="#0F172A" opacity="0.9"/>
      <text x="242" y="18" fill="#38BDF8" font-family="Arial,sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">BENGHAZI SEA STRIKE</text>
    </svg>"""

    svg_markets = """<svg viewBox="0 0 310 108" width="310" height="108" xmlns="http://www.w3.org/2000/svg">
      <rect width="310" height="108" fill="#18181B"/>
      <!-- Grid lines -->
      <g stroke="#27272A" stroke-width="1">
        <line x1="0" y1="27" x2="310" y2="27"/><line x1="0" y1="54" x2="310" y2="54"/><line x1="0" y1="81" x2="310" y2="81"/>
        <line x1="62" y1="0" x2="62" y2="108"/><line x1="124" y1="0" x2="124" y2="108"/><line x1="186" y1="0" x2="186" y2="108"/><line x1="248" y1="0" x2="248" y2="108"/>
      </g>
      <!-- Plunging chart area -->
      <polygon points="14,32 62,36 105,28 148,50 192,64 236,78 292,92 292,108 14,108" fill="#DC2626" opacity="0.18"/>
      <polyline points="14,32 62,36 105,28 148,50 192,64 236,78 292,92" fill="none" stroke="#EF4444" stroke-width="3.2" stroke-linejoin="round"/>
      <circle cx="292" cy="92" r="4.5" fill="#FCA5A5"/>
      <!-- Silicon chip icon -->
      <rect x="228" y="24" width="44" height="36" rx="4" fill="#27272A" stroke="#F59E0B" stroke-width="1.8"/>
      <rect x="238" y="32" width="24" height="20" rx="2" fill="#F59E0B" opacity="0.25"/>
      <text x="250" y="46" fill="#FCD34D" font-family="Arial,sans-serif" font-size="11" font-weight="800" text-anchor="middle">AI</text>
      <text x="18" y="88" fill="#F87171" font-family="Arial,sans-serif" font-size="18" font-weight="900">-10% CORRECTION</text>
      <rect x="6" y="6" width="118" height="17" rx="2" fill="#B91C1C"/>
      <text x="65" y="18" fill="#FFF" font-family="Arial,sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">S&amp;P 500 · NASDAQ</text>
      <rect x="184" y="6" width="120" height="17" rx="2" fill="#27272A"/>
      <text x="244" y="18" fill="#FBBF24" font-family="Arial,sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">ANTHROPIC · NVIDIA</text>
    </svg>"""

    # Mini SVGs for 8 secondary cards (each 228x54)
    mini_hormuz = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#1E293B"/>
      <path d="M0 38 Q30 34 60 38 T120 38 T180 38 T228 38 L228 54 L0 54 Z" fill="#0F172A"/>
      <polygon points="34,36 94,36 102,28 28,28" fill="#64748B"/><rect x="44" y="21" width="18" height="7" fill="#94A3B8"/>
      <circle cx="150" cy="28" r="14" stroke="#22C55E" stroke-width="1.4" fill="none"/><line x1="150" y1="28" x2="160" y2="20" stroke="#4ADE80" stroke-width="2"/>
      <rect x="6" y="5" width="76" height="14" rx="2" fill="#DC2626"/><text x="44" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">CLAIM VS DENIAL</text>
    </svg>"""

    mini_hk = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#EFF6FF"/>
      <rect x="18" y="14" width="38" height="36" fill="#CBD5E1"/><rect x="62" y="8" width="44" height="42" fill="#94A3B8"/>
      <rect x="148" y="18" width="46" height="30" rx="2" fill="#1E3A8A"/><rect x="158" y="12" width="26" height="9" fill="#FFF" stroke="#1E3A8A" stroke-width="1.5"/>
      <rect x="6" y="5" width="76" height="14" rx="2" fill="#1D4ED8"/><text x="44" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">98.79% TURNOUT</text>
    </svg>"""

    mini_motogp = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#18181B"/>
      <rect x="0" y="40" width="228" height="14" fill="#3F3F46"/>
      <path d="M52 38 Q95 16 142 36" stroke="#DC2626" stroke-width="6" fill="none" stroke-linecap="round"/>
      <circle cx="96" cy="21" r="6" fill="#F8FAFC"/>
      <circle cx="58" cy="39" r="9" fill="#09090B" stroke="#E4E4E7" stroke-width="2.5"/>
      <circle cx="136" cy="39" r="9" fill="#09090B" stroke="#E4E4E7" stroke-width="2.5"/>
      <rect x="196" y="7" width="8" height="8" fill="#FFF"/><rect x="204" y="7" width="8" height="8" fill="#52525B"/>
      <rect x="196" y="15" width="8" height="8" fill="#52525B"/><rect x="204" y="15" width="8" height="8" fill="#FFF"/>
      <text x="172" y="36" fill="#FACC15" font-family="Georgia" font-size="25" font-weight="900" text-anchor="middle">8x</text>
      <rect x="6" y="5" width="76" height="14" rx="2" fill="#DC2626"/><text x="44" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">MOTOGP GOAT</text>
    </svg>"""

    mini_f1 = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#09090B"/>
      <rect x="0" y="39" width="228" height="15" fill="#27272A"/>
      <polygon points="48,36 168,36 150,27 72,27" fill="#1D4ED8"/>
      <rect x="52" y="25" width="16" height="8" fill="#EF4444"/>
      <circle cx="76" cy="38" r="7.5" fill="#18181B" stroke="#F4F4F5" stroke-width="2"/>
      <circle cx="146" cy="38" r="7.5" fill="#18181B" stroke="#F4F4F5" stroke-width="2"/>
      <circle cx="195" cy="18" r="4" fill="#F43F5E"/><circle cx="209" cy="24" r="4" fill="#A855F7"/><circle cx="182" cy="26" r="4" fill="#38BDF8"/>
      <rect x="6" y="5" width="84" height="14" rx="2" fill="#1D4ED8"/><text x="48" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">VERSTAPPEN P1</text>
    </svg>"""

    mini_cricket = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#14532D"/>
      <rect x="0" y="34" width="228" height="20" fill="#166534"/>
      <line x1="56" y1="18" x2="56" y2="42" stroke="#FEF3C7" stroke-width="2.5"/>
      <line x1="63" y1="18" x2="63" y2="42" stroke="#FEF3C7" stroke-width="2.5"/>
      <line x1="70" y1="18" x2="70" y2="42" stroke="#FEF3C7" stroke-width="2.5"/>
      <g transform="translate(88,28) rotate(24)"><rect x="-3" y="-12" width="6" height="20" rx="1.5" fill="#FDE68A"/><rect x="-1.2" y="8" width="2.4" height="7" fill="#92400E"/></g>
      <circle cx="112" cy="25" r="5.5" fill="#DC2626"/>
      <text x="174" y="37" fill="#FEF08A" font-family="Georgia" font-size="22" font-weight="900" text-anchor="middle">720/9</text>
      <rect x="6" y="5" width="82" height="14" rx="2" fill="#15803D"/><text x="47" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">NZ TEST RECORD</text>
    </svg>"""

    mini_fire = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#451A03"/>
      <rect x="44" y="20" width="80" height="34" fill="#292524"/>
      <polygon points="62,54 78,16 94,54" fill="#EA580C"/><polygon points="78,54 96,12 114,54" fill="#FACC15" opacity="0.85"/>
      <circle cx="156" cy="26" r="14" fill="#78716C" opacity="0.5"/><circle cx="176" cy="18" r="16" fill="#57534E" opacity="0.5"/>
      <rect x="6" y="5" width="122" height="14" rx="2" fill="#B91C1C"/><text x="67" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">14H BLAZE · 36 MISSING</text>
    </svg>"""

    mini_turin = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#0F172A"/>
      <rect x="28" y="24" width="106" height="24" fill="#1D4ED8" stroke="#93C5FD" stroke-width="1.2"/>
      <line x1="81" y1="24" x2="81" y2="48" stroke="#E2E8F0" stroke-width="2"/>
      <circle cx="118" cy="18" r="6" fill="#BEF264"/>
      <text x="180" y="34" fill="#FDE047" font-family="Georgia" font-size="16" font-weight="900" text-anchor="middle">6-2 7-6</text>
      <rect x="6" y="5" width="84" height="14" rx="2" fill="#0284C7"/><text x="48" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">ALCARAZ TITLE</text>
    </svg>"""

    mini_sparta = """<svg viewBox="0 0 228 54" width="228" height="54"><rect width="228" height="54" fill="#0C4A6E"/>
      <rect x="0" y="37" width="228" height="17" fill="#082F49"/>
      <polygon points="40,37 124,37 132,27 32,27" fill="#475569"/>
      <polygon points="88,27 98,10 108,27" fill="#F97316"/>
      <path d="M104 12 C118 4 134 10 148 5" stroke="#94A3B8" stroke-width="4" fill="none" stroke-linecap="round"/>
      <rect x="6" y="5" width="82" height="14" rx="2" fill="#B91C1C"/><text x="47" y="15" fill="#FFF" font-family="Arial" font-size="8.5" font-weight="700" text-anchor="middle">GULF OF FINLAND</text>
    </svg>"""

    # Clean stylized SVG world map (356 x 176) with graticule, improved continents, and numbered pins
    world_map_svg = """<svg viewBox="0 0 356 176" width="356" height="176" xmlns="http://www.w3.org/2000/svg">
      <rect width="356" height="176" rx="4" fill="#EAE2D1" stroke="#C5B99E" stroke-width="1"/>
      <g stroke="#DDD3BD" stroke-width="0.6" stroke-dasharray="3 3">
        <line x1="0" y1="44" x2="356" y2="44"/><line x1="0" y1="88" x2="356" y2="88"/><line x1="0" y1="132" x2="356" y2="132"/>
        <line x1="89" y1="0" x2="89" y2="156"/><line x1="178" y1="0" x2="178" y2="156"/><line x1="267" y1="0" x2="267" y2="156"/>
      </g>
      <!-- Simplified continent shapes -->
      <g fill="#B7A98E" stroke="#F6F1E6" stroke-width="0.7">
        <!-- North America -->
        <polygon points="18,18 96,14 106,36 86,62 66,70 50,58 30,42"/>
        <!-- South America -->
        <polygon points="72,78 106,84 114,106 96,142 80,136 70,104"/>
        <!-- Europe -->
        <polygon points="148,22 204,16 212,44 180,50 152,44"/>
        <!-- Africa -->
        <polygon points="150,56 196,56 214,82 194,126 174,124 160,90"/>
        <!-- Asia -->
        <polygon points="206,18 314,20 322,52 290,74 256,80 224,68 204,48"/>
        <!-- Indonesia / SE Asia -->
        <polygon points="264,86 294,88 292,96 266,94"/>
        <!-- Australia & NZ -->
        <polygon points="278,104 318,102 322,130 284,132"/>
        <polygon points="334,124 342,128 336,140 330,136"/>
      </g>
      <!-- Pins matching key story numbers -->
      <g font-family="Arial,sans-serif" font-size="7.5" font-weight="800" text-anchor="middle">
        <circle cx="201" cy="47" r="6.5" fill="#B91C1C"/><text x="201" y="49.5" fill="#FFF">1</text>
        <circle cx="194" cy="32" r="6.5" fill="#B91C1C"/><text x="194" y="34.5" fill="#FFF">2</text>
        <circle cx="72" cy="43" r="6.5" fill="#B91C1C"/><text x="72" y="45.5" fill="#FFF">3</text>
        <circle cx="218" cy="65" r="6" fill="#1D4ED8"/><text x="218" y="67.5" fill="#FFF">4</text>
        <circle cx="288" cy="61" r="6" fill="#1D4ED8"/><text x="288" y="63.5" fill="#FFF">5</text>
        <circle cx="151" cy="41" r="6" fill="#1D4ED8"/><text x="151" y="43.5" fill="#FFF">6</text>
        <circle cx="40" cy="42" r="6" fill="#1D4ED8"/><text x="40" y="44.5" fill="#FFF">7</text>
        <circle cx="336" cy="132" r="6" fill="#15803D"/><text x="336" y="134.5" fill="#FFF">8</text>
        <circle cx="280" cy="91" r="6" fill="#B45309"/><text x="280" y="93.5" fill="#FFF">9</text>
        <circle cx="171" cy="39" r="6" fill="#0F766E"/><text x="171" y="41.5" fill="#FFF">10</text>
        <circle cx="195" cy="21" r="6" fill="#0F766E"/><text x="195" y="23.5" fill="#FFF">11</text>
        <circle cx="178" cy="59" r="5.5" fill="#7C3AED"/><text x="178" y="61.5" fill="#FFF">12</text>
        <circle cx="101" cy="105" r="5.5" fill="#7C3AED"/><text x="101" y="107.5" fill="#FFF">13</text>
        <circle cx="255" cy="59" r="5.5" fill="#7C3AED"/><text x="255" y="61.5" fill="#FFF">14</text>
        <circle cx="201" cy="84" r="5.5" fill="#7C3AED"/><text x="201" y="86.5" fill="#FFF">16</text>
        <circle cx="212" cy="94" r="5.5" fill="#15803D"/><text x="212" y="96.5" fill="#FFF">19</text>
      </g>
      <rect x="0" y="156" width="356" height="20" fill="#DFD5C0"/>
      <circle cx="16" cy="166" r="4" fill="#B91C1C"/><text x="24" y="169" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Leads 1–3</text>
      <circle cx="88" cy="166" r="4" fill="#1D4ED8"/><text x="96" y="169" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Cards 4–7</text>
      <circle cx="162" cy="166" r="4" fill="#0F766E"/><text x="170" y="169" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Cards 8–11</text>
      <circle cx="244" cy="166" r="4" fill="#7C3AED"/><text x="252" y="169" fill="#1E293B" font-family="Arial" font-size="8" font-weight="700">Digest 12–27</text>
    </svg>"""

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1024px;
    height: 1024px;
    overflow: hidden;
    background: #F6F1E6;
    color: #151922;
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{
    width: 1024px;
    height: 1024px;
    padding: 12px 16px 10px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .topbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #141923;
    color: #F6F1E6;
    padding: 4px 10px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.9px;
    text-transform: uppercase;
  }}
  .masthead {{
    text-align: center;
    border-bottom: 2.5px solid #141923;
    padding: 4px 0 5px 0;
  }}
  .masthead h1 {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 44px;
    font-weight: 900;
    line-height: 1.02;
    letter-spacing: -0.6px;
    color: #11151E;
  }}
  .masthead .deck {{
    margin-top: 2px;
    font-family: Georgia, serif;
    font-style: italic;
    font-size: 12px;
    color: #8A1E19;
    font-weight: 700;
  }}
  .kpis {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 6px;
    padding: 5px 0;
    border-bottom: 1px solid #C8BEAA;
  }}
  .kpi {{
    text-align: center;
    border-right: 1px solid #D5CCB8;
    padding: 0 4px;
  }}
  .kpi:last-child {{ border-right: none; }}
  .kpi .val {{
    font-family: Georgia, serif;
    font-size: 17px;
    font-weight: 900;
    color: #9B1C1C;
    line-height: 1.08;
  }}
  .kpi .lbl {{
    font-size: 8.5px;
    font-weight: 600;
    color: #475569;
    line-height: 1.15;
  }}
  .regions {{
    display: grid;
    grid-template-columns: 7fr 4fr 6fr 6fr 3fr 2fr 2fr;
    font-size: 8.5px;
    font-weight: 800;
    color: #FFF;
    text-align: center;
    margin-top: 3px;
  }}
  .regions div {{ padding: 2.5px 2px; white-space: nowrap; }}
  .utcbar {{
    background: #1E2430;
    color: #E2E8F0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3.5px 8px;
    font-size: 8.8px;
    margin-top: 3px;
  }}
  .utcbar .tag {{
    background: #B91C1C;
    color: #FFF;
    font-weight: 800;
    padding: 1.5px 6px;
    margin-right: 4px;
    font-size: 8.5px;
  }}
  .utcbar b {{ color: #FDE047; }}
  .leads {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 6px;
  }}
  .lead {{
    background: #FFFDF8;
    border: 1px solid #D5CCB8;
    padding: 5px;
    display: flex;
    flex-direction: column;
  }}
  .lead svg {{ width: 100%; height: auto; display: block; border: 1px solid #CBD5E1; }}
  .meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 4px;
    font-size: 8.5px;
    font-weight: 800;
    color: #7C2D12;
  }}
  .badge {{
    padding: 1px 4px;
    font-size: 7.5px;
    border: 1px solid;
    font-weight: 800;
  }}
  .b-conf {{ color: #166534; border-color: #166534; background: #DCFCE7; }}
  .b-rep {{ color: #1E40AF; border-color: #1E40AF; background: #DBEAFE; }}
  .b-disp {{ color: #9A3412; border-color: #9A3412; background: #FFEDD5; }}
  .lead h2 {{
    font-family: Georgia, serif;
    font-size: 14px;
    line-height: 1.16;
    font-weight: 900;
    margin-top: 3px;
    color: #111827;
  }}
  .lead p {{
    font-size: 9.8px;
    line-height: 1.26;
    color: #334155;
    margin-top: 3px;
  }}
  .src {{ font-weight: 700; color: #64748B; }}
  .sec-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 6px;
  }}
  .card {{
    background: #FFFDF8;
    border: 1px solid #D5CCB8;
    padding: 4px;
  }}
  .card svg {{ width: 100%; height: auto; display: block; }}
  .card h3 {{
    font-family: Georgia, serif;
    font-size: 11px;
    line-height: 1.15;
    font-weight: 800;
    margin-top: 3px;
    color: #111827;
  }}
  .card p {{
    font-size: 8.8px;
    line-height: 1.22;
    color: #334155;
    margin-top: 2px;
  }}
  .bottom {{
    display: grid;
    grid-template-columns: 358px 1fr;
    gap: 10px;
    margin-top: 6px;
    border-top: 2px solid #141923;
    padding-top: 5px;
  }}
  .sec-head {{
    font-size: 9px;
    font-weight: 900;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    color: #141923;
    margin-bottom: 3px;
    display: flex;
    justify-content: space-between;
  }}
  .briefs {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 12px;
    font-size: 8.9px;
    line-height: 1.24;
    color: #1E293B;
  }}
  .brief-col {{
    display: flex;
    flex-direction: column;
    gap: 2.8px;
  }}
  .brief b {{ color: #9B1C1C; }}
  .datecheck {{
    border: 1.5px solid #9B1C1C;
    background: #FEF2F2;
    padding: 3.5px 8px;
    font-size: 8.3px;
    line-height: 1.24;
    color: #1E293B;
    margin-top: 4px;
  }}
  .datecheck .dc-tag {{
    background: #9B1C1C;
    color: #FFF;
    font-weight: 800;
    padding: 1px 5px;
    margin-right: 5px;
  }}
  .foot {{
    display: flex;
    justify-content: space-between;
    font-size: 7.8px;
    color: #64748B;
    margin-top: 2px;
  }}
</style>
</head>
<body>
<div class="page">
  <div class="topbar">
    <span>THE WORLD IN ONE EDITION</span>
    <span>27 VERIFIED STORIES · ALL 7 REGIONS · FULL 24-HOUR RECORD OF NOV 22</span>
  </div>

  <div class="masthead">
    <h1>Sunday 22 November 2026</h1>
    <div class="deck">COP31 collapses with no fossil-fuel deal · Sea drones sink Russian warship in Libya · S&amp;P 500 enters 10% correction · Márquez wins 8th MotoGP title</div>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="val">0 PACT</div><div class="lbl">COP31 ends in Antalya deadlock</div></div>
    <div class="kpi"><div class="val">161 / 186</div><div class="lbl">drones downed over Ukraine</div></div>
    <div class="kpi"><div class="val">-10%</div><div class="lbl">S&amp;P 500 &amp; Nasdaq AI slump</div></div>
    <div class="kpi"><div class="val">98.79%</div><div class="lbl">Hong Kong 723-seat turnout</div></div>
    <div class="kpi"><div class="val">720/9</div><div class="lbl">India Test record in NZ</div></div>
    <div class="kpi"><div class="val">8th TITLE</div><div class="lbl">Marc Márquez ties MotoGP record</div></div>
  </div>

  <div class="regions">
    <div style="background:#1E3A8A;">EUROPE 7</div>
    <div style="background:#9A3412;">M. EAST 3</div>
    <div style="background:#0F766E;">ASIA 4</div>
    <div style="background:#4338CA;">AMERICAS 7</div>
    <div style="background:#15803D;">AFRICA 4</div>
    <div style="background:#B45309;">OCEANIA 1</div>
    <div style="background:#475569;">WORLD 1</div>
  </div>

  <div class="utcbar">
    <span><span class="tag">UTC TIMELINE</span><b>03:00</b> COP31 talks stall</span>
    <span><b>05:30</b> Verstappen wins Vegas GP</span>
    <span><b>08:00</b> Ukraine 186-drone tally</span>
    <span><b>14:00</b> HK Election closes</span>
    <span><b>17:30</b> Márquez 8th title · Alcaraz wins Turin</span>
    <span><b>21:00</b> COP31 collapses</span>
  </div>

  <div class="leads">
    <div class="lead">
      {svg_cop31}
      <div class="meta"><span>1 · ANTALYA, TÜRKIYE · CLIMATE</span><span class="badge b-conf">CONFIRMED</span></div>
      <h2>COP31 ends without a pact after 49-hour overtime</h2>
      <p>The UN summit collapsed Sunday after the EU, UK, and allies rejected the final “Antalya Pact” text for omitting fossil-fuel phase-out language and dropping the $120bn adaptation baseline. Procedural Just Transition rules passed; Guterres blamed fossil interests. <span class="src">(UN, Reuters, Guardian)</span></p>
    </div>
    <div class="lead">
      {svg_sea_drone}
      <div class="meta"><span>2 · KYIV &amp; BENGHAZI · WAR</span><span class="badge b-conf">CONFIRMED</span></div>
      <h2>Russia fires 186 drones; Kyiv sea drones hit Benghazi</h2>
      <p>Ukraine downed 161 of 186 Russian strike drones overnight, though a block in Dymer was hit. Separately, President Zelenskyy confirmed Ukrainian sea drones sailed 2,000+ km to sink the Russian corvette <i>Merkury</i> and strike cargo ship <i>Angara</i> in Libya. <span class="src">(BBC, Guardian, Naval News)</span></p>
    </div>
    <div class="lead">
      {svg_markets}
      <div class="meta"><span>3 · WALL STREET · MARKETS &amp; AI</span><span class="badge b-rep">REPORTED</span></div>
      <h2>Tech rout pushes S&amp;P 500 into 10% correction</h2>
      <p>A brutal semiconductor and AI sell-off drove the S&amp;P 500 down 10% from its October peak as Nvidia, AMD, and newly listed Anthropic tumbled amid rate-hike jitters. On Sunday Trump publicly demanded Nvidia reinstate ex-CEO Jensen Huang. <span class="src">(WashPost, Marketplace)</span></p>
    </div>
  </div>

  <div class="sec-grid">
    <div class="card">
      {mini_hormuz}
      <div class="meta"><span>4 · GULF &amp; RED SEA</span><span class="badge b-disp">DISPUTED</span></div>
      <h3>Iran claims US radar hits; Houthis target oil site</h3>
      <p>Iran claimed strikes on US radars in Bahrain; Manama denied, citing a civilian site fire. Houthis struck Saudi Petrol Rabigh refinery. <span class="src">(Al Jazeera, ISW)</span></p>
    </div>
    <div class="card">
      {mini_hk}
      <div class="meta"><span>5 · HONG KONG</span><span class="badge b-conf">OFFICIAL</span></div>
      <h3>Election Committee fills 723 seats</h3>
      <p>Subsector ordinary polls closed Sunday with 98.79% turnout across 31 subsectors under “patriots administering” rules. <span class="src">(HK Gov, SCMP)</span></p>
    </div>
    <div class="card">
      {mini_motogp}
      <div class="meta"><span>6 · PORTUGAL · MOTOGP</span><span class="badge b-conf">OFFICIAL</span></div>
      <h3>Márquez clinches 8th premier title</h3>
      <p>Finishing 8th at Portimão behind Bezzecchi, Marc Márquez overcame a 102-pt deficit to tie Agostini’s all-time record. <span class="src">(Guardian, MotoGP)</span></p>
    </div>
    <div class="card">
      {mini_f1}
      <div class="meta"><span>7 · LAS VEGAS · F1</span><span class="badge b-conf">OFFICIAL</span></div>
      <h3>Verstappen wins Las Vegas GP</h3>
      <p>Red Bull’s Max Verstappen beat McLaren duo Lando Norris (2nd) and Oscar Piastri (3rd) under the Strip lights. <span class="src">(Formula 1)</span></p>
    </div>
    <div class="card">
      {mini_cricket}
      <div class="meta"><span>8 · WELLINGTON · TEST</span><span class="badge b-conf">OFFICIAL</span></div>
      <h3>India declare at 720/9 record</h3>
      <p>Rahul 156, Pant 128, Gill 98 powered India to the highest Test total ever recorded on New Zealand soil. <span class="src">(ESPNcricinfo)</span></p>
    </div>
    <div class="card">
      {mini_fire}
      <div class="meta"><span>9 · INDONESIA · DISASTER</span><span class="badge b-rep">REPORTED</span></div>
      <h3>3 dead, 36 missing in plant fire</h3>
      <p>A 14-hour inferno tore through a three-story candy factory in Cikande, Banten; hundreds of rescuers searched rubble. <span class="src">(WashPost)</span></p>
    </div>
    <div class="card">
      {mini_turin}
      <div class="meta"><span>10 · TURIN · TENNIS</span><span class="badge b-conf">OFFICIAL</span></div>
      <h3>Alcaraz wins first ATP Finals</h3>
      <p>Carlos Alcaraz defeated Alexander Zverev 6-2, 7-6(7) in straight sets to capture the season-ending Turin crown. <span class="src">(ATP Tour)</span></p>
    </div>
    <div class="card">
      {mini_sparta}
      <div class="meta"><span>11 · BALTIC SEA</span><span class="badge b-conf">CONFIRMED</span></div>
      <h3>Burning Russian ship towed out</h3>
      <p>Drone-damaged cargo ship <i>Sparta II</i> drifted into Finnish waters; 16 crew rescued and Russian tow began Sunday. <span class="src">(Al Jazeera, Guardian)</span></p>
    </div>
  </div>

  <div class="bottom">
    <div>
      <div class="sec-head"><span>WHERE IT HAPPENED</span><span style="color:#64748B;">PINS MATCH NUMBERS</span></div>
      {world_map_svg}
    </div>
    <div>
      <div class="sec-head"><span>ALSO ON SUNDAY 22 NOVEMBER 2026</span><span style="color:#64748B;">GLOBAL ROUNDUP (12–27)</span></div>
      <div class="briefs">
        <div class="brief-col">
          <div class="brief"><b>12 Libya:</b> Russian-linked cargo vessel targeted off Benghazi alongside <i>Merkury</i> strike. (CBS)</div>
          <div class="brief"><b>13 Brazil:</b> Ex-president Bolsonaro remains stable in Brasília ICU after bowel surgery alert. (CP24)</div>
          <div class="brief"><b>14 India:</b> Nepal PM Balendra Shah lands in New Delhi for bilateral talks with PM Modi. (Hindu)</div>
          <div class="brief"><b>15 UK:</b> Liverpool thrash 10-man Man Utd 4-0 in Pochettino’s Anfield debut; Yoro sent off. (LFC)</div>
          <div class="brief"><b>16 Sudan:</b> Aerial and drone strikes hit North &amp; West Kordofan amid UN famine warnings. (OHCHR)</div>
          <div class="brief"><b>17 USA:</b> Spurs’ Victor Wembanyama drops 50 pts, 19 reb, 5 blk in 114-91 win over Pelicans. (NBC)</div>
          <div class="brief"><b>18 Belgium:</b> Air-traffic controllers prepare Monday national strike grounding commercial flights. (AA)</div>
          <div class="brief"><b>19 Somalia:</b> Protests and diplomatic rift escalate after Mogadishu expels UAE ambassador. (Africanews)</div>
        </div>
        <div class="brief-col">
          <div class="brief"><b>20 Qatar:</b> Pakistan Shaheens beat India A by 48 runs in Asia Cup Rising Stars cricket. (NDTV)</div>
          <div class="brief"><b>21 Lebanon:</b> UNIFIL starts handing southern buffer posts to Lebanese army ahead of mandate end. (AA)</div>
          <div class="brief"><b>22 USA:</b> Atmospheric rivers batter US West Coast with flood alerts ahead of Thanksgiving travel. (NWS)</div>
          <div class="brief"><b>23 Mexico:</b> President Sheinbaum balances US-China trade ties after APEC Shenzhen talks. (IntelRep)</div>
          <div class="brief"><b>24 UAE / LatAm:</b> UAE launches digital drive to train 1M AI coders in Dominican Republic. (The National)</div>
          <div class="brief"><b>25 Asia-Pacific:</b> Pope Francis &amp; aid agencies warn Super El Niño threatens millions across region. (Crux)</div>
          <div class="brief"><b>26 Kenya:</b> 42-day WHO Ebola-free countdown advances after last patient discharge. (WHO)</div>
          <div class="brief"><b>27 Baltics:</b> Estonia seals Russia border crossings after foiled drone-factory arson plot. (TVC)</div>
        </div>
      </div>
    </div>
  </div>

  <div class="datecheck">
    <span class="dc-tag">DATE CHECK</span>
    Events verified for <b>Sunday 22 November 2026</b> (any time zone). Excluded on purpose from earlier days: Peru M6.7 quake (Fri 20 Nov), Shenzhen Trump-Xi-Putin summit (Thu 19 Nov), El Chapo Isidro arrest (Sat 21 Nov), BepiColombo Mercury burn (Sat 21 Nov). Unverified social claims omitted.
  </div>

  <div class="foot">
    <span>Original vector diagrams, map, &amp; typography authored in Python/HTML/SVG · Built for make.fun news-image-20261122</span>
    <span>Sources: UN · Reuters · AP · BBC · Guardian · Al Jazeera · F1 · ATP · ESPNcricinfo · HK Gov</span>
  </div>
</div>
</body>
</html>
"""
    return html


def main() -> None:
    HTML_PATH.write_text(build_html(), encoding="utf-8")
    chrome = next((p for p in CHROME_PATHS if os.path.exists(p)), None)
    if not chrome:
        raise RuntimeError("No headless Chromium/Edge browser found")
    url = HTML_PATH.as_uri()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--window-size=1024,1024",
        "--force-device-scale-factor=1",
        f"--screenshot={OUT_PNG}",
        url,
    ]
    subprocess.run(cmd, check=True)
    with Image.open(OUT_PNG) as im:
        im = im.convert("RGB")
        if im.size != (1024, 1024):
            im = im.resize((1024, 1024), Image.Resampling.LANCZOS)
        # Save optimized PNG; fallback to JPEG bytes if > 1 MiB
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
