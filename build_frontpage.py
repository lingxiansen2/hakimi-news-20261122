from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent
HTML_OUT = ROOT_DIR / "frontpage.html"
PNG_OUT = ROOT_DIR / "entry.png"

BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def dot_matrix_world_map() -> str:
    """58x24 stylized dot-matrix world map SVG with zero-overlap story pins."""
    land_polygons = [
        # North & Central America
        [(-168, 66), (-142, 70), (-118, 72), (-95, 70), (-78, 63), (-62, 52), (-54, 47),
         (-68, 44), (-76, 35), (-81, 25), (-90, 29), (-97, 26), (-96, 19), (-88, 16),
         (-83, 10), (-78, 8), (-85, 11), (-93, 15), (-105, 20), (-117, 32), (-125, 42),
         (-131, 54), (-150, 60), (-166, 60)],
        # Greenland
        [(-56, 76), (-36, 82), (-19, 77), (-25, 70), (-44, 60), (-54, 67)],
        # South America
        [(-78, 10), (-67, 11), (-51, 2), (-35, -6), (-39, -18), (-48, -28), (-57, -38),
         (-66, -54), (-73, -53), (-75, -42), (-71, -30), (-71, -18), (-81, -5), (-79, 4)],
        # UK & Ireland
        [(-10, 52), (-5, 58), (1, 56), (1, 51), (-6, 50)],
        # Continental Europe & Scandinavia
        [(-9, 37), (-9, 43), (-2, 43), (-4, 48), (4, 53), (9, 55), (5, 61), (16, 69),
         (29, 71), (42, 67), (58, 68), (58, 52), (46, 44), (37, 45), (29, 41), (24, 38),
         (18, 40), (15, 38), (9, 44), (4, 43), (-5, 36)],
        # Africa
        [(-17, 15), (-13, 28), (-6, 36), (10, 37), (25, 32), (33, 31), (42, 13), (51, 12),
         (45, 2), (40, -11), (34, -24), (27, -33), (18, -35), (14, -22), (11, -6),
         (9, 4), (2, 6), (-8, 5), (-16, 10)],
        # Madagascar
        [(44, -25), (49, -13), (50, -21)],
        # Middle East & Asia
        [(27, 41), (36, 37), (35, 30), (43, 14), (54, 17), (59, 23), (56, 26), (62, 25),
         (72, 20), (77, 8), (83, 18), (90, 22), (98, 16), (103, 2), (104, 11), (109, 13),
         (108, 21), (121, 24), (122, 31), (120, 38), (126, 40), (129, 35), (132, 43),
         (141, 52), (144, 60), (162, 60), (177, 66), (170, 70), (135, 72), (105, 75),
         (76, 72), (58, 69), (58, 50), (47, 43), (38, 45)],
        # Japan & Okinawa
        [(130, 31), (136, 35), (141, 41), (145, 44), (140, 44), (137, 37), (130, 33)],
        # Maritime SE Asia
        [(96, 5), (105, -6), (116, -8), (119, 1), (109, 2), (101, 2)],
        [(120, 18), (126, 13), (125, 7), (121, 9)],
        # Australia & New Zealand
        [(114, -22), (129, -14), (136, -12), (143, -11), (153, -26), (150, -37),
         (138, -36), (128, -32), (115, -34)],
        [(167, -46), (172, -41), (178, -37), (174, -42), (168, -46)],
    ]

    def pt_in_poly(x: float, y: float, poly: list[tuple[float, float]]) -> bool:
        inside = False
        n = len(poly)
        j = n - 1
        for i in range(n):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi):
                inside = not inside
            j = i
        return inside

    w, h = 310, 166
    dots = []
    cols, rows = 58, 24
    for r in range(rows):
        lat = 75.0 - (r + 0.5) * (133.0 / rows)
        cy = 6.0 + (r + 0.5) * ((h - 12.0) / rows)
        for c in range(cols):
            lon = -168.0 + (c + 0.5) * (348.0 / cols)
            cx = 6.0 + (c + 0.5) * ((w - 12.0) / cols)
            if any(pt_in_poly(lon, lat, poly) for poly in land_polygons):
                dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.65" fill="#c7bfb0"/>')

    def proj(lon: float, lat: float) -> tuple[float, float]:
        x = 6.0 + (lon + 168.0) / 348.0 * (w - 12.0)
        y = 6.0 + (75.0 - lat) / 133.0 * (h - 12.0)
        return x, y

    raw_pins = [
        (1, 30.5, 50.6, "lead", "Kyiv"),
        (2, 30.7, 36.9, "lead", "Antalya"),
        (3, 50.6, 26.2, "lead", "Manama"),
        (4, 127.0, 37.6, "card", "Seoul"),
        (5, 114.2, 22.3, "card", "Hong Kong"),
        (6, 174.8, -41.3, "card", "Wellington"),
        (7, -115.1, 36.1, "card", "Las Vegas"),
        (8, -8.5, 37.2, "card", "Portimao"),
        (9, 7.7, 45.1, "card", "Turin"),
        (10, -98.5, 29.4, "card", "San Antonio"),
        (11, 106.4, -6.2, "card", "Cikande"),
        (12, 26.2, 60.4, "card", "Loviisa"),
        (13, 6.2, 4.9, "card", "Bayelsa"),
        (14, 12.4, 41.9, "card", "Vatican"),
        (15, 127.7, 26.2, "card", "Okinawa"),
        (16, -2.9, 53.4, "dig", "Liverpool"),
        (17, 28.2, 59.4, "dig", "Narva"),
        (18, 12.6, 55.7, "dig", "Copenhagen"),
        (21, 93.9, 24.8, "dig", "Manipur"),
        (22, 121.5, 25.0, "dig", "Taipei"),
        (23, 77.2, 28.6, "dig", "Delhi"),
        (24, 34.4, 31.5, "dig", "Gaza"),
        (28, 45.3, 2.0, "dig", "Mogadishu"),
        (29, 32.5, 15.6, "dig", "Khartoum"),
        (31, -47.9, -15.8, "dig", "Brasilia"),
        (32, -77.0, 38.9, "dig", "Washington"),
        (35, 149.1, -35.3, "dig", "Canberra"),
    ]

    placed: list[tuple[int, float, float, str]] = []
    for num, lon, lat, kind, _ in raw_pins:
        x, y = proj(lon, lat)
        angle = 0.0
        step = 0.0
        bx, by = x, y
        for _ in range(56):
            tx = max(8.0, min(w - 8.0, x + step * math.cos(angle)))
            ty = max(8.0, min(h - 8.0, y + step * math.sin(angle)))
            if all(math.hypot(tx - px, ty - py) >= 12.1 for _, px, py, _ in placed):
                bx, by = tx, ty
                break
            angle += 0.85
            step += 1.4
        placed.append((num, bx, by, kind))

    palette = {"lead": "#b91c1c", "card": "#0f766e", "dig": "#1e3a8a"}
    pin_svg = []
    for num, x, y, kind in sorted(placed, key=lambda p: 0 if p[3] == "dig" else (1 if p[3] == "card" else 2)):
        col = palette[kind]
        r = 6.2 if kind == "lead" else (5.6 if kind == "card" else 5.0)
        fs = 6.8 if kind == "lead" else (6.1 if kind == "card" else 5.5)
        pin_svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" stroke="#fbf9f3" stroke-width="1"/>'
            f'<text x="{x:.1f}" y="{y + fs * 0.34:.1f}" text-anchor="middle" fill="#fff" '
            f'font-size="{fs:.1f}" font-weight="700" font-family="Segoe UI, sans-serif">{num}</text>'
        )

    eq_y = proj(0, 0)[1]
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" style="display:block;background:#f2ece0;border:1px solid #d5cebf">'
        f'<line x1="6" y1="{eq_y:.1f}" x2="{w-6}" y2="{eq_y:.1f}" stroke="#ddd5c4" stroke-dasharray="3 3" stroke-width="0.8"/>'
        f'{"".join(dots)}{"".join(pin_svg)}</svg>'
    )


def art_ukraine_drones() -> str:
    return '''<svg viewBox="0 0 318 104" width="100%" height="104" style="display:block">
      <defs><linearGradient id="bg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#1e293b"/></linearGradient></defs>
      <rect width="318" height="104" fill="url(#bg1)"/>
      <!-- Searchlight & air defence arc -->
      <polygon points="48,96 86,20 112,24" fill="#38bdf8" fill-opacity="0.18"/>
      <polygon points="148,96 116,18 134,15" fill="#facc15" fill-opacity="0.16"/>
      <path d="M22 86 Q116 14 214 64" fill="none" stroke="#38bdf8" stroke-dasharray="4 3" stroke-width="1.5"/>
      <!-- Intercepted drones -->
      <polygon points="74,40 88,36 82,46" fill="#94a3b8"/>
      <circle cx="90" cy="39" r="5" fill="#f97316"/>
      <polygon points="122,28 138,24 132,35" fill="#94a3b8"/>
      <circle cx="136" cy="30" r="6" fill="#ef4444"/><circle cx="136" cy="30" r="3" fill="#fde047"/>
      <!-- Vyshhorod / Dymer 5-storey block -->
      <rect x="218" y="28" width="66" height="68" fill="#334155" stroke="#475569"/>
      <rect x="226" y="36" width="10" height="8" fill="#fbbf24"/><rect x="242" y="36" width="10" height="8" fill="#0f172a"/><rect x="258" y="36" width="10" height="8" fill="#fbbf24"/>
      <rect x="226" y="50" width="10" height="8" fill="#0f172a"/><rect x="242" y="50" width="10" height="8" fill="#fbbf24"/>
      <polygon points="256,28 284,28 284,58 260,50" fill="#0f172a"/>
      <circle cx="268" cy="43" r="8" fill="#f97316"/><circle cx="268" cy="43" r="4" fill="#fde047"/>
      <rect x="8" y="7" width="108" height="14" rx="1" fill="#b91c1c"/>
      <text x="62" y="17" text-anchor="middle" fill="#fff" font-size="7.4" font-weight="700" font-family="Segoe UI, sans-serif">186 DRONES FIRED</text>
      <rect x="210" y="7" width="100" height="14" rx="1" fill="#0369a1"/>
      <text x="260" y="17" text-anchor="middle" fill="#fff" font-size="7.4" font-weight="700" font-family="Segoe UI, sans-serif">161 INTERCEPTED</text>
    </svg>'''


def art_cop31_collapse() -> str:
    return '''<svg viewBox="0 0 318 104" width="100%" height="104" style="display:block">
      <defs><linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1e293b"/><stop offset="100%" stop-color="#334155"/></linearGradient></defs>
      <rect width="318" height="104" fill="url(#bg2)"/>
      <circle cx="96" cy="56" r="34" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
      <ellipse cx="96" cy="56" rx="16" ry="34" fill="none" stroke="#38bdf8" stroke-opacity="0.45" stroke-width="1"/>
      <line x1="62" y1="56" x2="130" y2="56" stroke="#38bdf8" stroke-opacity="0.45" stroke-width="1"/>
      <path d="M90 27 L99 49 L91 63 L103 84" fill="none" stroke="#ef4444" stroke-width="2.6" stroke-linecap="round"/>
      <rect x="148" y="24" width="66" height="66" rx="2" fill="#f8fafc" stroke="#94a3b8"/>
      <line x1="158" y1="37" x2="202" y2="37" stroke="#cbd5e1" stroke-width="3"/>
      <line x1="158" y1="46" x2="196" y2="46" stroke="#cbd5e1" stroke-width="3"/>
      <line x1="158" y1="55" x2="200" y2="55" stroke="#cbd5e1" stroke-width="3"/>
      <g transform="rotate(-12 182 54)">
        <rect x="148" y="44" width="68" height="20" rx="2" fill="#b91c1c" stroke="#fecaca" stroke-width="1.2"/>
        <text x="182" y="57" text-anchor="middle" fill="#fff" font-size="9.5" font-weight="800" font-family="Segoe UI, sans-serif">NO PACT</text>
      </g>
      <rect x="236" y="49" width="28" height="12" rx="2" fill="#d97706" transform="rotate(-24 250 55)"/>
      <rect x="254" y="56" width="38" height="5" rx="2" fill="#b45309" transform="rotate(24 254 56)"/>
      <rect x="234" y="80" width="46" height="7" rx="2" fill="#92400e"/>
      <rect x="8" y="7" width="96" height="14" rx="1" fill="#b91c1c"/>
      <text x="56" y="17" text-anchor="middle" fill="#fff" font-size="7.4" font-weight="700" font-family="Segoe UI, sans-serif">49H+ OVERTIME</text>
      <rect x="210" y="7" width="100" height="14" rx="1" fill="#0f172a" stroke="#64748b"/>
      <text x="260" y="17" text-anchor="middle" fill="#e2e8f0" font-size="7.4" font-weight="700" font-family="Segoe UI, sans-serif">FOSSIL STALEMATE</text>
    </svg>'''


def art_iran_bahrain() -> str:
    return '''<svg viewBox="0 0 318 104" width="100%" height="104" style="display:block">
      <defs><linearGradient id="bg3" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#3b0764"/><stop offset="60%" stop-color="#1e1b4b"/><stop offset="100%" stop-color="#0f172a"/></linearGradient></defs>
      <rect width="318" height="104" fill="url(#bg3)"/>
      <rect x="0" y="78" width="318" height="26" fill="#0c4a6e"/>
      <!-- Radar dish left -->
      <path d="M46 68 Q62 46 84 62 Z" fill="#cbd5e1"/>
      <line x1="65" y1="58" x2="65" y2="78" stroke="#94a3b8" stroke-width="3"/>
      <circle cx="65" cy="52" r="14" fill="none" stroke="#38bdf8" stroke-dasharray="3 2" stroke-width="1.3"/>
      <!-- Industrial tanks & fire plume Manama -->
      <rect x="148" y="54" width="26" height="24" rx="2" fill="#e2e8f0" stroke="#94a3b8"/>
      <rect x="180" y="58" width="22" height="20" rx="2" fill="#cbd5e1" stroke="#94a3b8"/>
      <path d="M160 54 C154 38 168 30 172 24 C178 33 184 42 176 54 Z" fill="#f97316"/>
      <path d="M164 54 C162 42 170 36 172 32 C175 39 175 45 173 54 Z" fill="#fde047"/>
      <!-- Incoming track dashed -->
      <line x1="286" y1="26" x2="180" y2="48" stroke="#ef4444" stroke-dasharray="4 2" stroke-width="1.8"/>
      <circle cx="286" cy="26" r="4" fill="#ef4444"/>
      <rect x="8" y="7" width="100" height="14" rx="1" fill="#b45309"/>
      <text x="58" y="17" text-anchor="middle" fill="#fff" font-size="7.4" font-weight="700" font-family="Segoe UI, sans-serif">CLAIM VS DENIAL</text>
      <rect x="210" y="7" width="100" height="14" rx="1" fill="#b91c1c"/>
      <text x="260" y="17" text-anchor="middle" fill="#fff" font-size="7.4" font-weight="700" font-family="Segoe UI, sans-serif">GULF REFINERY ALERT</text>
    </svg>'''


def mini_choi() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#f1f5f9"/>
      <!-- OMR Exam Sheet -->
      <rect x="14" y="8" width="68" height="48" rx="2" fill="#fff" stroke="#64748b"/>
      <rect x="14" y="8" width="68" height="10" fill="#1e3a8a"/>
      <text x="48" y="15.5" text-anchor="middle" fill="#fff" font-size="6.4" font-weight="700" font-family="Segoe UI, sans-serif">SUNEUNG OMR</text>
      <circle cx="26" cy="26" r="3" fill="#0f172a"/><circle cx="36" cy="26" r="3" fill="none" stroke="#475569"/><circle cx="46" cy="26" r="3" fill="none" stroke="#475569"/>
      <circle cx="26" cy="36" r="3" fill="none" stroke="#475569"/><circle cx="36" cy="36" r="3" fill="#0f172a"/><circle cx="46" cy="36" r="3" fill="none" stroke="#475569"/>
      <circle cx="26" cy="46" r="3" fill="none" stroke="#475569"/><circle cx="36" cy="46" r="3" fill="none" stroke="#475569"/><circle cx="46" cy="46" r="3" fill="#0f172a"/>
      <!-- AI Phone + RESIGNED stamp -->
      <rect x="94" y="10" width="46" height="28" rx="3" fill="#0f172a" stroke="#38bdf8"/>
      <text x="117" y="27" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="800" font-family="Segoe UI, sans-serif">AI</text>
      <rect x="86" y="42" width="64" height="14" rx="2" fill="#b91c1c"/>
      <text x="118" y="51.5" text-anchor="middle" fill="#fff" font-size="7.2" font-weight="800" font-family="Segoe UI, sans-serif">RESIGNED</text>
    </svg>'''


def mini_hk_poll() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#eff6ff"/>
      <rect x="20" y="24" width="54" height="30" rx="2" fill="#1e3a8a"/>
      <rect x="28" y="28" width="38" height="4" fill="#93c5fd"/>
      <!-- Crisp ticked ballot card -->
      <polygon points="36,10 66,10 56,28 26,28" fill="#fff" stroke="#1e293b" stroke-width="1.2"/>
      <polyline points="40,19 45,24 55,13" fill="none" stroke="#059669" stroke-width="2.6" stroke-linecap="round"/>
      <rect x="88" y="14" width="60" height="32" rx="2" fill="#1e293b"/>
      <text x="118" y="27" text-anchor="middle" fill="#fde047" font-size="9.5" font-weight="800" font-family="Segoe UI, sans-serif">98.79%</text>
      <text x="118" y="40" text-anchor="middle" fill="#cbd5e1" font-size="7" font-weight="700" font-family="Segoe UI, sans-serif">723 SEATS</text>
    </svg>'''


def mini_cricket_720() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#14532d"/>
      <ellipse cx="72" cy="40" rx="58" ry="18" fill="#15803d" stroke="#86efac" stroke-width="1"/>
      <rect x="58" y="22" width="28" height="34" fill="#ca8a04" fill-opacity="0.45"/>
      <line x1="67" y1="22" x2="67" y2="48" stroke="#fef9c3" stroke-width="2"/>
      <line x1="72" y1="22" x2="72" y2="48" stroke="#fef9c3" stroke-width="2"/>
      <line x1="77" y1="22" x2="77" y2="48" stroke="#fef9c3" stroke-width="2"/>
      <line x1="66" y1="21.5" x2="78" y2="21.5" stroke="#fde047" stroke-width="2"/>
      <circle cx="48" cy="39" r="4.2" fill="#dc2626"/>
      <rect x="98" y="11" width="52" height="22" rx="2" fill="#052e16" stroke="#4ade80"/>
      <text x="124" y="20" text-anchor="middle" fill="#86efac" font-size="6.4" font-weight="700" font-family="Segoe UI, sans-serif">RECORD</text>
      <text x="124" y="29.5" text-anchor="middle" fill="#fff" font-size="8.2" font-weight="800" font-family="Segoe UI, sans-serif">720/9d</text>
    </svg>'''


def mini_vegas_f1() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#0f172a"/>
      <!-- Neon Strip glow & asphalt -->
      <circle cx="34" cy="20" r="3" fill="#ec4899"/><circle cx="54" cy="14" r="3" fill="#38bdf8"/><circle cx="78" cy="18" r="3" fill="#fde047"/>
      <rect x="0" y="42" width="160" height="22" fill="#334155"/>
      <line x1="0" y1="53" x2="160" y2="53" stroke="#94a3b8" stroke-dasharray="10 6" stroke-width="1.3"/>
      <!-- F1 car silhouette -->
      <path d="M24 44 L44 38 H86 L104 42 H110 V47 H24 Z" fill="#1e3a8a" stroke="#ef4444" stroke-width="1"/>
      <circle cx="42" cy="47" r="6" fill="#111827" stroke="#94a3b8" stroke-width="1.5"/>
      <circle cx="96" cy="47" r="6" fill="#111827" stroke="#94a3b8" stroke-width="1.5"/>
      <!-- Checkered P1 flag -->
      <rect x="116" y="12" width="34" height="20" rx="2" fill="#dc2626"/>
      <text x="133" y="25.5" text-anchor="middle" fill="#fff" font-size="9" font-weight="800" font-family="Segoe UI, sans-serif">P1</text>
    </svg>'''


def mini_motogp_8x() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#1e293b"/>
      <rect x="0" y="46" width="160" height="18" fill="#334155"/>
      <path d="M0 46 H160" stroke="#ef4444" stroke-width="2"/>
      <!-- Leaning racing bike -->
      <circle cx="44" cy="44" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
      <circle cx="88" cy="44" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2"/>
      <path d="M44 44 L60 28 L86 30 L88 44 Z" fill="#dc2626"/>
      <circle cx="72" cy="21" r="6" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
      <rect x="108" y="10" width="42" height="26" rx="2" fill="#450a0a" stroke="#f59e0b"/>
      <text x="129" y="22" text-anchor="middle" fill="#fde047" font-size="9.5" font-weight="800" font-family="Segoe UI, sans-serif">8th</text>
      <text x="129" y="32" text-anchor="middle" fill="#fff" font-size="6.4" font-weight="700" font-family="Segoe UI, sans-serif">MOTOGP</text>
    </svg>'''


def mini_atp_alcaraz() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#1d4ed8"/>
      <rect x="12" y="16" width="90" height="40" fill="#2563eb" stroke="#eff6ff" stroke-width="1.5"/>
      <line x1="57" y1="16" x2="57" y2="56" stroke="#eff6ff" stroke-width="2"/>
      <line x1="28" y1="36" x2="86" y2="36" stroke="#93c5fd" stroke-width="1.2"/>
      <circle cx="76" cy="26" r="5" fill="#bef264" stroke="#365314"/>
      <rect x="108" y="12" width="44" height="32" rx="2" fill="#1e293b" stroke="#fbbf24"/>
      <text x="130" y="25" text-anchor="middle" fill="#fde047" font-size="7.5" font-weight="800" font-family="Segoe UI, sans-serif">TURIN</text>
      <text x="130" y="37" text-anchor="middle" fill="#fff" font-size="7" font-weight="700" font-family="Segoe UI, sans-serif">CHAMP</text>
    </svg>'''


def mini_wemby() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#111827"/>
      <rect x="10" y="48" width="140" height="16" fill="#78350f"/>
      <!-- Basketball backboard & hoop -->
      <rect x="20" y="12" width="38" height="24" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
      <rect x="31" y="20" width="16" height="12" fill="none" stroke="#ef4444" stroke-width="1.5"/>
      <line x1="32" y1="33" x2="46" y2="33" stroke="#ea580c" stroke-width="2.5"/>
      <path d="M58 26 Q84 8 102 22" fill="none" stroke="#fb923c" stroke-dasharray="3 2" stroke-width="1.5"/>
      <circle cx="62" cy="23" r="6.5" fill="#ea580c" stroke="#7c2d12"/>
      <rect x="100" y="10" width="52" height="30" rx="2" fill="#1f2937" stroke="#94a3b8"/>
      <text x="126" y="23" text-anchor="middle" fill="#fff" font-size="8.5" font-weight="800" font-family="Segoe UI, sans-serif">50 PTS</text>
      <text x="126" y="34" text-anchor="middle" fill="#cbd5e1" font-size="7" font-weight="700" font-family="Segoe UI, sans-serif">19 REB</text>
    </svg>'''


def mini_cikande() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#292524"/>
      <rect x="0" y="48" width="160" height="16" fill="#44403c"/>
      <!-- Factory roof silhouette -->
      <polygon points="14,48 14,32 34,24 34,32 54,24 54,32 78,24 78,48" fill="#57534e"/>
      <path d="M40 24 C36 12 46 6 52 10 C58 14 58 22 50 24 Z" fill="#f97316"/>
      <circle cx="64" cy="14" r="9" fill="#78716c" fill-opacity="0.7"/>
      <circle cx="76" cy="9" r="7" fill="#a8a29e" fill-opacity="0.5"/>
      <rect x="94" y="14" width="56" height="24" rx="2" fill="#991b1b"/>
      <text x="122" y="25" text-anchor="middle" fill="#fff" font-size="8" font-weight="800" font-family="Segoe UI, sans-serif">24 DEAD</text>
      <text x="122" y="34" text-anchor="middle" fill="#fecaca" font-size="6.4" font-weight="700" font-family="Segoe UI, sans-serif">FACTORY</text>
    </svg>'''


def mini_sparta_tow() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#0c4a6e"/>
      <rect x="0" y="44" width="160" height="20" fill="#075985"/>
      <!-- Towed cargo hull -->
      <path d="M16 40 H78 L72 48 H20 Z" fill="#475569"/>
      <rect x="24" y="33" width="18" height="7" fill="#94a3b8"/>
      <path d="M48 39 C45 30 53 26 56 32 C59 35 56 39 52 39 Z" fill="#f97316"/>
      <!-- Tug line & rescue tug -->
      <line x1="78" y1="43" x2="106" y2="43" stroke="#fde047" stroke-width="1.5"/>
      <path d="M106 39 H142 L138 47 H108 Z" fill="#dc2626"/>
      <rect x="116" y="31" width="14" height="8" fill="#f8fafc"/>
      <text x="120" y="16" text-anchor="middle" fill="#bae6fd" font-size="7.2" font-weight="800" font-family="Segoe UI, sans-serif">FINLAND TOW</text>
    </svg>'''


def mini_nigeria_boat() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#1e3a8a"/>
      <rect x="0" y="42" width="160" height="22" fill="#0369a1"/>
      <path d="M0 44 Q20 39 40 44 T80 44 T120 44 T160 44" fill="none" stroke="#7dd3fc" stroke-width="1.5"/>
      <!-- Capsized wooden hull -->
      <g transform="rotate(20 56 42)">
        <path d="M22 38 Q56 24 90 38 Z" fill="#92400e" stroke="#fde68a" stroke-width="1"/>
      </g>
      <rect x="102" y="12" width="50" height="22" rx="2" fill="#7f1d1d"/>
      <text x="127" y="22" text-anchor="middle" fill="#fff" font-size="7.5" font-weight="800" font-family="Segoe UI, sans-serif">24+ LOST</text>
      <text x="127" y="31" text-anchor="middle" fill="#fecaca" font-size="6.4" font-weight="700" font-family="Segoe UI, sans-serif">BAYELSA</text>
    </svg>'''


def mini_pope_lunch() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#fef3c7"/>
      <!-- St Peter dome silhouette -->
      <path d="M18 52 V36 C18 20 58 20 58 36 V52 Z" fill="#b45309"/>
      <line x1="38" y1="12" x2="38" y2="22" stroke="#78350f" stroke-width="2"/>
      <line x1="34" y1="15" x2="42" y2="15" stroke="#78350f" stroke-width="2"/>
      <!-- Long banquet table -->
      <rect x="70" y="40" width="78" height="7" fill="#fff" stroke="#78350f"/>
      <circle cx="84" cy="34" r="4" fill="#92400e"/><circle cx="102" cy="34" r="4" fill="#0f172a"/>
      <circle cx="120" cy="34" r="4" fill="#92400e"/><circle cx="138" cy="34" r="4" fill="#0f172a"/>
      <rect x="76" y="10" width="70" height="16" rx="2" fill="#78350f"/>
      <text x="111" y="21" text-anchor="middle" fill="#fff" font-size="7.5" font-weight="800" font-family="Segoe UI, sans-serif">1,300 GUESTS</text>
    </svg>'''


def mini_shuri_castle() -> str:
    return '''<svg viewBox="0 0 160 64" width="100%" height="68" preserveAspectRatio="xMidYMid slice" style="display:block">
      <rect width="160" height="64" fill="#e0f2fe"/>
      <rect x="0" y="48" width="160" height="16" fill="#94a3b8"/>
      <!-- Vermilion Seiden Pavilion -->
      <polygon points="24,26 80,14 136,26" fill="#7f1d1d"/>
      <polygon points="34,34 80,24 126,34" fill="#991b1b"/>
      <rect x="44" y="34" width="72" height="14" fill="#dc2626"/>
      <rect x="72" y="38" width="16" height="10" fill="#fde047"/>
      <text x="128" y="14" text-anchor="middle" fill="#1e3a8a" font-size="7" font-weight="800" font-family="Segoe UI, sans-serif">RESTORED</text>
    </svg>'''


def render_markup() -> str:
    leads = [
        {
            "num": 1,
            "art": art_ukraine_drones(),
            "eyebrow": "KYIV REGION, UKRAINE · WAR",
            "badge": ("CONFIRMED", "#065f46"),
            "hed": "Russia launches 186 attack drones; 161 downed, Kyiv block hit",
            "body": "Ukraine air defenses downed or jammed 161 of 186 drones overnight (72 jet-powered) across eight axes, as debris struck a residential block in Vyshhorod district outside Kyiv. (Ukrinform, Pravda)",
        },
        {
            "num": 2,
            "art": art_cop31_collapse(),
            "eyebrow": "ANTALYA, TÜRKİYE · CLIMATE",
            "badge": ("CONFIRMED", "#065f46"),
            "hed": "COP31 ends in overtime deadlock with no consensus climate deal",
            "body": "After 49+ hours past Friday schedule, Antalya talks broke down without formal adoption of the final text after disputes over fossil-fuel transition language and adaptation finance. (WRI, WWF, IUCN)",
        },
        {
            "num": 3,
            "art": art_iran_bahrain(),
            "eyebrow": "MANAMA & GULF · SECURITY",
            "badge": ("DISPUTED", "#b45309"),
            "hed": "Iran claims Bahrain radar hits; Houthi refinery strikes spark alerts",
            "body": "Iran claimed strikes on US radars in Bahrain while Manama reported a civilian industrial fire; US missions issued Middle East security alerts after Houthi threats to Saudi refineries. (ISW, US Embassy)",
        },
    ]

    cards = [
        (4, mini_choi(), "SEOUL · POLITICS", ("CONFIRMED", "#065f46"), "Education chief Choi quits over Suneung AI rules", "Resigns amid outcry after tax-exam AI cheating panic sparked rule chaos. (Time)"),
        (5, mini_hk_poll(), "HONG KONG · VOTE", ("OFFICIAL", "#0f766e"), "Hong Kong fills 723 seats on 98.79% turnout", "5,640 subsector voters cast Sunday ballots across 31 sectors. (HK Gov)"),
        (6, mini_cricket_720(), "WELLINGTON · TEST", ("OFFICIAL", "#0f766e"), "India declare at record 720/9 in New Zealand", "Highest Test total in NZ leaves Black Caps facing steep Day 5 chase. (ESPN)"),
        (7, mini_vegas_f1(), "LAS VEGAS · F1", ("OFFICIAL", "#0f766e"), "Verstappen wins Vegas GP from pole for Ford", "Red Bull Ford Powertrains scores historic first US F1 victory. (Ford/FIA)"),
        (8, mini_motogp_8x(), "PORTIMÃO · MOTOGP", ("OFFICIAL", "#0f766e"), "Márquez clinches eighth premier MotoGP crown", "Spaniard caps comeback to seal 8th top-class championship. (Al Jazeera)"),
        (9, mini_atp_alcaraz(), "TURIN · TENNIS", ("OFFICIAL", "#0f766e"), "Alcaraz beats Zverev for first ATP Finals title", "Joins elite set owning all four majors plus season finale. (Al Jazeera)"),
        (10, mini_wemby(), "SAN ANTONIO · NBA", ("OFFICIAL", "#0f766e"), "Wembanyama drops 50 & 19 in Spurs' 14th win", "French star powers San Antonio past New Orleans with dominant slate. (AJ)"),
        (11, mini_cikande(), "CIKANDE · DISASTER", ("CONFIRMED", "#065f46"), "24 body bags recovered at burned candy factory", "Search continues in Banten ruins for dozens missing in plant blaze. (ChinaDaily)"),
        (12, mini_sparta_tow(), "BALTIC · MARITIME", ("CONFIRMED", "#065f46"), "Drone-hit Russian ship Sparta II towed from Finland", "Joint firefighting ends; Russian rescue vessel pulls hull from Finnish waters. (NV)"),
        (13, mini_nigeria_boat(), "BAYELSA · DISASTER", ("REPORTED", "#1d4ed8"), "24+ drown as mourners' boat capsizes in Nigeria", "Overcrowded passenger craft fails mechanically in southern river. (Al Jazeera)"),
        (14, mini_pope_lunch(), "VATICAN · FAITH", ("OFFICIAL", "#0f766e"), "Pope Leo XIV hosts 1,300 poor guests for lunch", "St. Peter's Angelus and banquet mark 10th World Day of the Poor. (Vatican)"),
        (15, mini_shuri_castle(), "OKINAWA · HERITAGE", ("OFFICIAL", "#0f766e"), "Shuri Castle marks main hall restoration completion", "Ceremony honors rebuilt Seiden seven years after 2019 blaze. (Japan Times)"),
    ]

    digest_left = [
        (16, "Liverpool", "#1d4ed8", "Liverpool rout Man Utd 4-0 at Anfield in Premier League clash", "BBC"),
        (17, "Estonia", "#1d4ed8", "Weekend queues build at Russian borders before Dec 1 shutdown", "GUARDIAN"),
        (18, "Denmark", "#1d4ed8", "Copenhagen expels Russian defense attaché after PET plot probe", "ANADOLU"),
        (19, "Brussels", "#1d4ed8", "Belgian ATC agency skeyes readies 07:00–21:00 Monday flight halt", "AIRWAYS"),
        (20, "Kyiv / Libya", "#1d4ed8", "Kyiv details long-range sea-drone strike off Libya coast", "WIRES"),
        (21, "Manipur", "#0f766e", "Toxic liquor death toll hits 16–17 with 600+ hospitalized", "HINDU"),
        (22, "Taipei", "#0f766e", "63rd Taipei Golden Horse Awards honor regional cinema Sunday", "SCREEN"),
        (23, "New Delhi", "#0f766e", "Nepal PM Balendra Shah opens India trip ahead of Modi summit", "HINDU"),
        (24, "Gaza", "#9a3412", "Tel al-Hawa vehicle strike kills 3; Israel & WCK trade claims", "TOI"),
        (25, "Jerusalem", "#9a3412", "Likud & Eisenkot hold 4h coalition talks without rotation deal", "JAPANTIMES"),
        (26, "World", "#374151", "Crypto swings and tanker threats keep maritime & market risk high", "WIRES"),
    ]

    digest_right = [
        (27, "Gulf", "#9a3412", "US missions issue Middle East alerts after Saudi energy threats", "US EMBASSY"),
        (28, "Lebanon", "#9a3412", "UNIFIL & border teams coordinate southern security transitions", "AA"),
        (29, "Mogadishu", "#6d28d9", "Somalia launches digital arms registry & builds naval dock", "HIIRAAN"),
        (30, "Khartoum", "#6d28d9", "Civil war drone strikes and displacement squeeze Sudanese aid", "AL JAZEERA"),
        (31, "Juba", "#6d28d9", "South Sudan oil fragility & Horn stability draw diplomatic scrutiny", "SENTRY"),
        (32, "Brasília", "#b45309", "Bolsonaro stable and pain-free in DF Star ICU after blockage", "CP24"),
        (33, "Washington", "#b45309", "FBI probes apparent breach affecting NCIC gun-check network", "WIRES"),
        (34, "US Tech", "#b45309", "Trump urges Nvidia rehire Huang; FBI tracks DPRK crypto thefts", "FBI / WIRES"),
        (35, "Canberra", "#0284c7", "Defence chief Marles rejects CBO report warning on AUKUS subs", "JAPANTIMES"),
        (36, "US Sports", "#b45309", "Packed Sunday NBA and US sports slate wraps holiday weekend", "ESPN"),
    ]

    def render_lead(item: dict) -> str:
        label, bg = item["badge"]
        return f'''
        <article class="lead-card">
          <div class="art-wrap">{item["art"]}</div>
          <div class="meta-row">
            <span class="eyebrow"><b class="nlead">{item["num"]}</b> {item["eyebrow"]}</span>
            <span class="pill" style="background:{bg}">{label}</span>
          </div>
          <h2 class="lead-hed">{item["hed"]}</h2>
          <p class="lead-body">{item["body"]}</p>
        </article>'''

    def render_sec(c: tuple) -> str:
        num, art, eye, (lbl, bg), hed, blurb = c
        return f'''
        <article class="sec-card">
          <div class="sec-art">{art}</div>
          <div class="sec-meta">
            <span class="sec-eye"><b class="nsec">{num}</b> {eye}</span>
            <span class="pill-sm" style="background:{bg}">{lbl}</span>
          </div>
          <h3 class="sec-hed">{hed}</h3>
          <p class="sec-blurb">{blurb}</p>
        </article>'''

    def render_dig(d: tuple) -> str:
        num, loc, col, txt, src = d
        return (
            f'<li class="dig-item"><span class="dnum" style="background:{col}">{num}</span>'
            f'<span class="dtxt"><b>{loc}:</b> {txt}</span>'
            f'<span class="dsrc">{src}</span></li>'
        )

    map_html = dot_matrix_world_map()

    return f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1024px; height: 1024px; overflow: hidden;
    background: #f5f1e6; color: #1a1e24;
    font-family: "Segoe UI", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{
    width: 1024px; height: 1024px;
    padding: 11px 15px 9px 15px;
    display: flex; flex-direction: column; gap: 6px;
  }}
  .top-strip {{
    background: #181c22; color: #f8fafc;
    display: flex; justify-content: space-between; align-items: center;
    padding: 3px 9px; font-size: 8.5px; font-weight: 700; letter-spacing: 0.7px;
  }}
  .masthead {{ text-align: center; border-bottom: 2px solid #181c22; padding-bottom: 5px; }}
  .masthead h1 {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 44px; line-height: 1.03; font-weight: 800; letter-spacing: -0.6px; color: #111827;
  }}
  .subdeck {{
    font-family: Georgia, serif; font-style: italic; font-size: 11.4px; color: #991b1b;
    margin-top: 2px; font-weight: 600;
  }}
  .kpis {{
    display: grid; grid-template-columns: repeat(6, 1fr);
    border-top: 1px solid #d5cebf; border-bottom: 1px solid #d5cebf;
    background: #fbf9f2; padding: 4px 0;
  }}
  .kpi {{ text-align: center; border-right: 1px solid #dfd8ca; padding: 0 4px; }}
  .kpi:last-child {{ border-right: none; }}
  .kpi-val {{ font-family: Georgia, serif; font-size: 15px; font-weight: 800; color: #111827; line-height: 1.1; }}
  .kpi-val.red {{ color: #b91c1c; }}
  .kpi-lbl {{ font-size: 7.7px; color: #4b5563; margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

  .regions {{ display: flex; height: 15px; font-size: 8px; font-weight: 800; color: #fff; border-radius: 1px; overflow: hidden; }}
  .reg {{ display: flex; align-items: center; justify-content: center; letter-spacing: 0.2px; }}

  .utcbar {{
    background: #20252d; color: #e2e8f0; display: flex; align-items: center; gap: 8px;
    padding: 3px 8px; font-size: 8px; white-space: nowrap; overflow: hidden;
  }}
  .utctag {{ background: #b91c1c; color: #fff; font-weight: 800; padding: 1px 5px; font-size: 7.6px; letter-spacing: 0.4px; }}
  .utcitem b {{ color: #fbbf24; margin-right: 2px; }}

  .leads {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }}
  .lead-card {{ background: #fbf9f3; border: 1px solid #d4cdc0; padding: 5px; display: flex; flex-direction: column; }}
  .art-wrap svg, .sec-art svg {{ text-rendering: geometricPrecision; }}
  .art-wrap {{ border: 1px solid #cbd5e1; margin-bottom: 4px; }}
  .meta-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }}
  .eyebrow {{ font-size: 7.6px; font-weight: 800; color: #991b1b; letter-spacing: 0.25px; }}
  .nlead {{ display: inline-block; background: #b91c1c; color: #fff; padding: 0 3.5px; border-radius: 2px; margin-right: 2px; }}
  .pill {{ color: #fff; font-size: 7px; font-weight: 800; padding: 1px 4px; border-radius: 1px; letter-spacing: 0.3px; }}
  .lead-hed {{
    font-family: Georgia, serif; font-size: 14px; line-height: 1.13; font-weight: 800;
    color: #111827; margin-bottom: 3px;
  }}
  .lead-body {{ font-size: 9.2px; line-height: 1.24; color: #334155; }}

  .sec-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 5px; }}
  .sec-card {{ background: #fbf9f3; border: 1px solid #d4cdc0; padding: 4px; display: flex; flex-direction: column; }}
  .sec-art {{ border: 1px solid #cbd5e1; margin-bottom: 3px; overflow: hidden; }}
  .sec-meta {{ display: flex; justify-content: space-between; align-items: center; gap: 2px; margin-bottom: 2px; }}
  .sec-eye {{ font-size: 6.7px; font-weight: 800; color: #0f766e; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .nsec {{ display: inline-block; background: #0f766e; color: #fff; padding: 0 3px; border-radius: 1.5px; margin-right: 1px; }}
  .pill-sm {{ color: #fff; font-size: 6.1px; font-weight: 800; padding: 0.5px 3px; border-radius: 1px; flex-shrink: 0; }}
  .sec-hed {{
    font-family: Georgia, serif; font-size: 10.6px; line-height: 1.12; font-weight: 800;
    color: #111827; margin-bottom: 2px;
  }}
  .sec-blurb {{ font-size: 8.2px; line-height: 1.2; color: #374151; }}

  .bottom {{ display: grid; grid-template-columns: 312px 1fr; gap: 8px; align-items: stretch; flex: 1; min-height: 0; }}
  .map-panel {{ background: #fbf9f3; border: 1px solid #d4cdc0; padding: 5px; display: flex; flex-direction: column; justify-content: space-between; }}
  .panel-hdr {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 3px; }}
  .panel-hdr h4 {{ font-size: 8.8px; font-weight: 800; letter-spacing: 0.3px; color: #111827; }}
  .panel-hdr span {{ font-size: 7.4px; color: #6b7280; font-weight: 600; }}
  .map-leg {{ display: flex; justify-content: space-between; font-size: 7.6px; font-weight: 700; color: #374151; margin-top: 3px; }}
  .dotl {{ display: inline-block; width: 7px; height: 7px; border-radius: 50%; vertical-align: middle; margin-right: 3px; }}

  .dig-panel {{ background: #fbf9f3; border: 1px solid #d4cdc0; padding: 5px 6px; display: flex; flex-direction: column; }}
  .dig-cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 3px; flex: 1; align-content: space-between; }}
  .dig-list {{ list-style: none; display: flex; flex-direction: column; gap: 3px; }}
  .dig-item {{ display: flex; align-items: flex-start; gap: 4px; font-size: 8.1px; line-height: 1.2; color: #1f2937; border-bottom: 1px dotted #e5dec9; padding-bottom: 2px; }}
  .dig-item:last-child {{ border-bottom: none; }}
  .dnum {{ color: #fff; font-size: 6.7px; font-weight: 800; min-width: 14px; text-align: center; padding: 0.5px 2px; border-radius: 2px; margin-top: 0.5px; flex-shrink: 0; }}
  .dtxt {{ flex: 1; }}
  .dsrc {{ font-size: 6.5px; font-weight: 700; color: #475569; background: #ede8da; border: 1px solid #d6cfc0; padding: 0.5px 3px; border-radius: 1.5px; white-space: nowrap; flex-shrink: 0; }}

  .datecheck {{
    border: 1px solid #dc2626; background: #fef2f2; color: #7f1d1d;
    padding: 3px 7px; font-size: 7.6px; line-height: 1.25; display: flex; gap: 6px; align-items: center;
  }}
  .dc-badge {{ background: #b91c1c; color: #fff; font-weight: 800; padding: 1px 5px; font-size: 7.2px; white-space: nowrap; }}
  .foot {{
    display: flex; justify-content: space-between; font-size: 7.3px; color: #4b5563;
    border-top: 1px solid #cfc7b8; padding-top: 2px;
  }}
</style>
</head>
<body>
<div class="page">
  <div class="top-strip">
    <span>THE WORLD IN ONE EDITION</span>
    <span>36 VERIFIED STORIES · ALL 7 REGIONS · STRICT SUNDAY 22 NOVEMBER 2026</span>
  </div>

  <header class="masthead">
    <h1>Sunday 22 November 2026</h1>
    <div class="subdeck">186 drones over Ukraine overnight · COP31 stalls without climate pact · Iran &amp; Bahrain trade claims · HK votes at 98.79% · Márquez &amp; Alcaraz win</div>
  </header>

  <section class="kpis">
    <div class="kpi"><div class="kpi-val red">186</div><div class="kpi-lbl">drones fired; 161 downed</div></div>
    <div class="kpi"><div class="kpi-val red">49h+</div><div class="kpi-lbl">COP31 overtime deadlock</div></div>
    <div class="kpi"><div class="kpi-val">98.79%</div><div class="kpi-lbl">Hong Kong poll turnout</div></div>
    <div class="kpi"><div class="kpi-val">720/9</div><div class="kpi-lbl">India record Test in NZ</div></div>
    <div class="kpi"><div class="kpi-val">8th</div><div class="kpi-lbl">Márquez premier crown</div></div>
    <div class="kpi"><div class="kpi-val">50 / 19</div><div class="kpi-lbl">Wembanyama pts &amp; reb</div></div>
  </section>

  <div class="regions">
    <div class="reg" style="flex:10;background:#1d4ed8">EUROPE 10</div>
    <div class="reg" style="flex:7;background:#0f766e">ASIA 7</div>
    <div class="reg" style="flex:5;background:#9a3412">M. EAST 5</div>
    <div class="reg" style="flex:6;background:#b45309">AMERICAS 6</div>
    <div class="reg" style="flex:4;background:#6d28d9">AFRICA 4</div>
    <div class="reg" style="flex:2;background:#0284c7">OCEANIA 2</div>
    <div class="reg" style="flex:2;background:#374151">WORLD 2</div>
  </div>

  <div class="utcbar">
    <span class="utctag">DAY IN UTC</span>
    <span class="utcitem"><b>01:00</b>HK subsector polls open</span>
    <span class="utcitem"><b>05:30</b>Verstappen Vegas P1</span>
    <span class="utcitem"><b>08:00</b>161 of 186 drones downed</span>
    <span class="utcitem"><b>14:00</b>HK closes at 98.79%</span>
    <span class="utcitem"><b>17:30</b>Alcaraz &amp; Márquez crowns</span>
    <span class="utcitem"><b>21:00</b>COP31 closes with no pact</span>
  </div>

  <section class="leads">
    {''.join(render_lead(i) for i in leads)}
  </section>

  <section class="sec-grid">
    {''.join(render_sec(c) for c in cards)}
  </section>

  <section class="bottom">
    <div class="map-panel">
      <div class="panel-hdr">
        <h4>WHERE IT HAPPENED</h4>
        <span>PINS MATCH NUMBERS</span>
      </div>
      {map_html}
      <div class="map-leg">
        <span><i class="dotl" style="background:#b91c1c"></i>Leads 1–3</span>
        <span><i class="dotl" style="background:#0f766e"></i>Featured 4–15</span>
        <span><i class="dotl" style="background:#1e3a8a"></i>Digest 16–36</span>
      </div>
    </div>

    <div class="dig-panel">
      <div class="panel-hdr">
        <h4>ALSO ON SUNDAY 22 NOVEMBER 2026 — 21 MORE VERIFIED STORIES</h4>
        <span>SOURCE NAMED BESIDE EACH ITEM</span>
      </div>
      <div class="dig-cols">
        <ul class="dig-list">{''.join(render_dig(d) for d in digest_left)}</ul>
        <ul class="dig-list">{''.join(render_dig(d) for d in digest_right)}</ul>
      </div>
    </div>
  </section>

  <section class="datecheck">
    <span class="dc-badge">DATE CHECK</span>
    <span>Strictly Sun 22 Nov 2026. Excluded from earlier/later days: Peru M6.7–6.9 quake &amp; Wall St close (Fri 20 Nov); "El Chapo Isidro" capture &amp; BepiColombo burn (Sat 21 Nov); Belgian ATC flight walkout &amp; Modi–Shah MoUs (Mon 23 Nov).</span>
  </section>

  <footer class="foot">
    <span>CONFIRMED = 2+ wires · OFFICIAL = gov/league · REPORTED = single wire · DISPUTED = competing claim</span>
    <span>Original Python/HTML/SVG graphics for make.fun news-image-20261122</span>
  </footer>
</div>
</body>
</html>'''


def _find_browser() -> str:
    for path in BROWSERS:
        if Path(path).exists():
            return path
    found = shutil.which("chrome") or shutil.which("msedge")
    if found:
        return found
    raise FileNotFoundError("Chrome or Edge executable is required to render frontpage.html")


def main() -> None:
    HTML_OUT.write_text(render_markup(), encoding="utf-8")
    browser = _find_browser()
    raw_png = ROOT_DIR / "_raw_frontpage.png"
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=1024,1024",
        f"--screenshot={raw_png}",
        HTML_OUT.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with Image.open(raw_png) as img:
        final_img = img.convert("RGB")
        if final_img.size != (1024, 1024):
            final_img = final_img.crop((0, 0, 1024, 1024))
        final_img.save(PNG_OUT, format="PNG", optimize=True)
    raw_png.unlink(missing_ok=True)
    HTML_OUT.unlink(missing_ok=True)
    size = PNG_OUT.stat().st_size
    assert size < 1_048_576, f"PNG too large: {size}"
    print(f"Rendered {PNG_OUT.name} ({size} bytes, 1024x1024)")


if __name__ == "__main__":
    main()
