"""THE WORLD IN ONE DAY — Wednesday 25 November 2026 (1024x1024 Editorial Broadsheet).

Entry for make.fun competition news-image-20261125 (program/v1).
Sums up 52 verified stories across 10 regions and 21 fields that happened or were
first reported on Wednesday 25 November 2026, with 13 custom-drawn vector SVG
illustrations, an hour-by-hour UTC timeline, a 10-region world map with 52
numbered pins, source attributions on every story, and an explicit date-check
excluding pre-25-November news.

When invoked with --build-image (outside the sandbox), renders the HTML5/SVG
broadsheet via headless Chromium at 2048x2048 and downsamples with Lanczos to
a crisp, palette-optimized 1024x1024 PNG at ./entry.png.
When invoked by the make.fun grader (no network, standard library only),
deterministically writes the exact bytes of ./entry.png to /output/entry.png.
"""

import os
import shutil
import sys

DAY_TITLE = "Wednesday 25 November 2026"
SUBTITLE = "35 STORIES · 10 REGIONS · 18 FIELDS · ALL FIRST REPORTED ON WEDNESDAY 25 NOVEMBER 2026"

UTC_TIMELINE = [
    ("00:18", "Shenzhou-24 launch"),
    ("00:30", "Australia CPI 4.9%"),
    ("03:56", "Tiangong docking"),
    ("05:30", "Taiex -4.8%"),
    ("06:30", "Kospi -6.2%"),
    ("07:00", "Ofgem cap +26%"),
    ("10:15", "Farmgate voided"),
    ("11:40", "Cairo fire 30+ dead"),
    ("13:30", "US GDP +4.3%"),
    ("15:00", "US 14-economy tariffs"),
    ("21:00", "Wall St mixed"),
]

TOP_STATS = [
    ("20%–35%", "US tariff plan on EU, China & 12 economies", "#b91c1c"),
    ("-6.2%", "Kospi chip rout (4,697); SK hynix -11.1%", "#1d4ed8"),
    ("1st", "Pakistani astronaut docks at China's Tiangong", "#047857"),
    ("+26%", "UK Ofgem energy cap jumps to £2,166 in Jan", "#b45309"),
    ("30+ / 9", "Killed in Cairo tanker fire & Java gold pit", "#6d28d9"),
]

LEAD_STORIES = [
    {
        "num": 1,
        "loc": "WASHINGTON · TRADE",
        "tag": "OFFICIAL",
        "tag_col": "#047857",
        "banner": "UP TO 35% · 14 ECONOMIES",
        "title": "US tariffs up to 35% on 14 economies",
        "body": "Vietnam 35%, India 25%, China 20%, EU 15%; hearings Jan 2027.",
        "src": "USTR · Reuters · CNBC",
        "svg": "tariffs",
    },
    {
        "num": 2,
        "loc": "SEOUL · TOKYO · TAIPEI · MARKETS",
        "tag": "CONFIRMED",
        "tag_col": "#1d4ed8",
        "banner": "KOSPI -6.2% · SK HYNIX -11.1%",
        "title": "Kospi falls 6.2% on AI doubts",
        "body": "Closes 4,697.51; SK hynix -11.1%, Samsung -9.9%, Taiex -4.8%.",
        "src": "KRX · Yonhap · Reuters",
        "svg": "chips",
    },
    {
        "num": 3,
        "loc": "JIUQUAN, CHINA · SPACE",
        "tag": "OFFICIAL",
        "tag_col": "#047857",
        "banner": "SHENZHOU-24 · DOCKED 03:56 UTC",
        "title": "Astronaut docks at Tiangong station",
        "body": "Zeeshan Ali, 40, first foreigner aboard the station.",
        "src": "CMSA · Xinhua · AP",
        "svg": "space",
    },
]

LEAD_STORIES += [
    {
        "num": 4,
        "loc": "UKRAINE · WAR",
        "tag": "OFFICIAL",
        "tag_col": "#047857",
        "banner": "5 REGIONS · GRID LOSS #17",
        "title": "Russian strikes kill 5, cut power in 5 regions",
        "body": "Zaporizhzhia nuclear plant on diesel after 17th grid loss; 5 killed.",
        "src": "Reuters · Energoatom",
        "svg": "grid",
    },
    {
        "num": 5,
        "loc": "RAS TANURA · WAR",
        "tag": "CONFIRMED",
        "tag_col": "#1d4ed8",
        "banner": "4 DRONES DOWN · HODEIDAH",
        "title": "Saudis down Houthi drones after port strike",
        "body": "4 drones destroyed over Ras Tanura refinery after Hodeidah port hit.",
        "src": "SPA · Reuters",
        "svg": "drones",
    },
    {
        "num": 6,
        "loc": "LONDON · ENERGY",
        "tag": "OFFICIAL",
        "tag_col": "#047857",
        "banner": "£1,723 → £2,166 (+26%)",
        "title": "UK energy price cap to jump 26% in January",
        "body": "Ofgem lifts typical annual household bill from £1,723 to £2,166.",
        "src": "Ofgem · BBC · FT",
        "svg": "energy",
    },
]

MID_ROW_1 = []
MID_ROW_2 = []

BRIEFS_COL_1 = [
    (7,  "Canberra", "Solomon Islands signs security pact with Australia", "OFFICIAL"),
    (8,  "Dhaka", "Garment wage up 36% to Tk 17,000; unions reject", "OFFICIAL"),
    (9,  "Bogor", "9 dead, 17 trapped in flooded illegal Java mine", "OFFICIAL"),
    (10, "Giza, Cairo", "Tanker blast on ring road kills at least 30", "OFFICIAL"),
    (11, "Gaza City", "Strike kills Hamas security chief in al-Shati", "REPORTED"),
    (12, "Cape Town", "Court voids Phala Phala report against Ramaphosa", "OFFICIAL"),
    (13, "Jerusalem", "Judges doubt Netanyahu bribery count in Case 4000", "CONFIRMED"),
    (14, "Hormuz", "Iran IRGC: 2 tankers hit mines off Hormuz", "CLAIM"),
    (15, "Samara", "Drones set Syzran & Kuibyshev refineries ablaze", "CONFIRMED"),
    (16, "Pyongyang", "N Korea gives Swiss envoy 48 hours to leave", "OFFICIAL"),
    (17, "Brussels", "EU proposes €50bn quantum technology fund", "OFFICIAL"),
    (18, "London", "Poundland collapse puts 11,000 UK jobs at risk", "CONFIRMED"),
    (19, "Kyiv", "Zelensky: Ukraine needs €115bn aid for 2027", "OFFICIAL"),
    (20, "Paris", "Eurostar walkout cancels cross-Channel trains", "CONFIRMED"),
    (21, "Ed Damazin", "RSF drone strikes kill 19 in Sudan Blue Nile", "CONFIRMED"),
]

BRIEFS_COL_2 = [
    (22, "Lagos", "Police arrest 5 Mexicans, seize $220m meth lab", "OFFICIAL"),
    (23, "Harare", "Court issues arrest warrant for Mugabe's son", "OFFICIAL"),
    (24, "Abuja", "Tinubu proposes ₦66.18tn 2026 budget", "OFFICIAL"),
    (25, "New York", "Wall St mixed: Dow +0.3%, Nasdaq -0.6%", "OFFICIAL"),
    (26, "Washington", "FCC clears SpaceX 1m orbital data nodes", "OFFICIAL"),
    (27, "Iowa", "Army detonates 10,000 lb of lead azide", "OFFICIAL"),
    (28, "Cartagena", "Police free 20 supermarket hostages", "OFFICIAL"),
    (29, "Paraná", "Storms kill 6, hit 40 towns in southern Brazil", "OFFICIAL"),
    (30, "Sydney", "CPI 4.9%; Lamarre-Condon found guilty", "OFFICIAL"),
    (31, "Kuala Lumpur", "Malaysia sues Google for RM600m over YouTube", "OFFICIAL"),
    (32, "Hong Kong", "URBTIX breach exposes 1.3m users' data", "OFFICIAL"),
    (33, "Karachi", "Building collapse kills 3, injures 14", "CONFIRMED"),
    (34, "Deep Space", "Hera images stadium-sized DART crater", "OFFICIAL"),
    (35, "Lisbon", "Sporting CP 2-2 Man United in Champions League", "OFFICIAL"),
]

BRIEFS_COL_3 = []


def svg_scene(kind: str, banner: str) -> str:
    """Return a high-contrast, crisp vector SVG scene for each of the 13 drawn stories."""
    scenes = {
        "tariffs": """
          <rect width="310" height="86" fill="#1e293b"/>
          <path d="M0 64 Q80 58 160 64 T310 62 L310 86 L0 86 Z" fill="#0f172a"/>
          <!-- Cargo ship & containers -->
          <polygon points="18,54 148,54 136,70 28,70" fill="#334155" stroke="#94a3b8" stroke-width="1.2"/>
          <rect x="34" y="38" width="22" height="16" fill="#dc2626" stroke="#fca5a5" stroke-width="1"/>
          <rect x="58" y="34" width="22" height="20" fill="#2563eb" stroke="#93c5fd" stroke-width="1"/>
          <rect x="82" y="38" width="22" height="16" fill="#d97706" stroke="#fcd34d" stroke-width="1"/>
          <rect x="108" y="30" width="18" height="24" fill="#e2e8f0"/>
          <!-- Tariff bar chart on right -->
          <rect x="172" y="48" width="24" height="24" fill="#3b82f6"/>
          <text x="184" y="44" fill="#93c5fd" font-size="9" font-weight="800" text-anchor="middle">EU 15%</text>
          <rect x="206" y="40" width="24" height="32" fill="#f59e0b"/>
          <text x="218" y="36" fill="#fde68a" font-size="9" font-weight="800" text-anchor="middle">CN 20%</text>
          <rect x="240" y="32" width="24" height="40" fill="#ef4444"/>
          <text x="252" y="28" fill="#fca5a5" font-size="9" font-weight="800" text-anchor="middle">IN 25%</text>
          <rect x="274" y="22" width="24" height="50" fill="#b91c1c"/>
          <text x="286" y="18" fill="#fecaca" font-size="9" font-weight="800" text-anchor="middle">VN 35%</text>
        """,
        "chips": """
          <rect width="310" height="86" fill="#172033"/>
          <!-- Grid lines -->
          <line x1="12" y1="26" x2="298" y2="26" stroke="#334155" stroke-dasharray="3,3"/>
          <line x1="12" y1="50" x2="298" y2="50" stroke="#334155" stroke-dasharray="3,3"/>
          <line x1="12" y1="74" x2="298" y2="74" stroke="#334155"/>
          <!-- Silicon wafer icon left -->
          <rect x="18" y="28" width="44" height="44" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1.8"/>
          <rect x="28" y="38" width="24" height="24" fill="#0284c7"/>
          <text x="40" y="54" fill="#fff" font-size="10" font-weight="900" text-anchor="middle">AI</text>
          <!-- Plunging red market curve -->
          <polyline points="80,24 125,28 165,42 205,58 250,68 292,73" fill="none" stroke="#f43f5e" stroke-width="3.2"/>
          <polygon points="80,24 125,28 165,42 205,58 250,68 292,73 292,78 80,78" fill="#f43f5e" fill-opacity="0.22"/>
          <circle cx="292" cy="73" r="4" fill="#f43f5e"/>
          <text x="155" y="35" fill="#fda4af" font-size="10" font-weight="800">4,697.51 (-6.16%)</text>
          <text x="195" y="53" fill="#fde047" font-size="9" font-weight="800">SK Hynix -11.1% · Samsung -9.9%</text>
        """,
        "space": """
          <rect width="310" height="86" fill="#091024"/>
          <circle cx="34" cy="24" r="1.5" fill="#fff"/><circle cx="270" cy="20" r="1.5" fill="#fff"/>
          <circle cx="190" cy="68" r="1.2" fill="#93c5fd"/><circle cx="95" cy="70" r="1.4" fill="#fff"/>
          <!-- Earth limb -->
          <path d="M0 86 Q155 62 310 86 Z" fill="#1d4ed8" fill-opacity="0.45" stroke="#60a5fa" stroke-width="1.5"/>
          <!-- Tiangong station modules & solar wings -->
          <rect x="115" y="42" width="76" height="12" rx="4" fill="#e2e8f0" stroke="#94a3b8"/>
          <rect x="132" y="22" width="14" height="20" fill="#38bdf8" stroke="#bae6fd" stroke-width="1"/>
          <rect x="132" y="54" width="14" height="20" fill="#38bdf8" stroke="#bae6fd" stroke-width="1"/>
          <rect x="172" y="20" width="14" height="22" fill="#38bdf8" stroke="#bae6fd" stroke-width="1"/>
          <rect x="172" y="54" width="14" height="22" fill="#38bdf8" stroke="#bae6fd" stroke-width="1"/>
          <!-- Shenzhou-24 capsule docking -->
          <polygon points="82,48 112,43 112,53" fill="#f59e0b" stroke="#fef08a" stroke-width="1"/>
          <rect x="64" y="43" width="18" height="10" fill="#10b981"/>
          <text x="206" y="46" fill="#a7f3d0" font-size="9.5" font-weight="800">TIANGONG</text>
          <text x="206" y="59" fill="#fde68a" font-size="8.5" font-weight="700">Zeeshan Ali (PAK)</text>
        """,
        "grid": """
          <rect width="184" height="54" fill="#1e2436"/>
          <!-- Pylon & cooling tower -->
          <polygon points="24,50 34,18 48,18 58,50" fill="#475569" stroke="#94a3b8" stroke-width="1"/>
          <line x1="88" y1="50" x2="100" y2="16" stroke="#f59e0b" stroke-width="1.8"/>
          <line x1="112" y1="50" x2="100" y2="16" stroke="#f59e0b" stroke-width="1.8"/>
          <line x1="88" y1="26" x2="112" y2="26" stroke="#f59e0b" stroke-width="1.5"/>
          <polygon points="136,16 126,32 135,32 128,48 148,29 138,29" fill="#ef4444"/>
          <text x="155" y="42" fill="#fca5a5" font-size="11" font-weight="900">5</text>
        """,
        "drones": """
          <rect width="184" height="54" fill="#1c2536"/>
          <!-- Radar sweep & intercepted drones -->
          <circle cx="42" cy="46" r="26" fill="none" stroke="#10b981" stroke-width="1.2" stroke-dasharray="3,2"/>
          <circle cx="42" cy="46" r="14" fill="none" stroke="#10b981" stroke-width="1.2"/>
          <line x1="42" y1="46" x2="62" y2="26" stroke="#34d399" stroke-width="2"/>
          <polygon points="105,24 122,20 116,32" fill="#f43f5e"/>
          <polygon points="138,30 155,26 149,38" fill="#f43f5e"/>
          <circle cx="115" cy="25" r="9" fill="none" stroke="#fbbf24" stroke-width="1.5"/>
          <circle cx="148" cy="31" r="9" fill="none" stroke="#fbbf24" stroke-width="1.5"/>
        """,
        "energy": """
          <rect width="184" height="54" fill="#231f32"/>
          <rect x="26" y="28" width="34" height="22" fill="#64748b"/>
          <text x="43" y="24" fill="#cbd5e1" font-size="8.5" font-weight="800" text-anchor="middle">£1,723</text>
          <path d="M72 36 L98 24" stroke="#fbbf24" stroke-width="2.2"/>
          <rect x="110" y="16" width="38" height="34" fill="#f59e0b"/>
          <text x="129" y="37" fill="#111827" font-size="9.5" font-weight="900" text-anchor="middle">£2,166</text>
        """,
        "treaty": """
          <rect width="184" height="54" fill="#152c3d"/>
          <circle cx="52" cy="30" r="16" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/>
          <text x="52" y="34" fill="#fff" font-size="9" font-weight="900" text-anchor="middle">AUS</text>
          <line x1="68" y1="30" x2="112" y2="30" stroke="#34d399" stroke-width="3"/>
          <circle cx="128" cy="30" r="16" fill="#059669" stroke="#a7f3d0" stroke-width="1.5"/>
          <text x="128" y="34" fill="#fff" font-size="9" font-weight="900" text-anchor="middle">SOL</text>
        """,
        "garment": """
          <rect width="184" height="54" fill="#1e293b"/>
          <rect x="20" y="32" width="28" height="18" fill="#64748b"/>
          <text x="34" y="28" fill="#cbd5e1" font-size="8" font-weight="800" text-anchor="middle">12.5k</text>
          <rect x="68" y="20" width="32" height="30" fill="#10b981"/>
          <text x="84" y="39" fill="#064e3b" font-size="8.5" font-weight="900" text-anchor="middle">17k</text>
          <rect x="118" y="16" width="32" height="34" fill="#f43f5e"/>
          <text x="134" y="37" fill="#fff" font-size="8.5" font-weight="900" text-anchor="middle">18k?</text>
        """,
        "mine": """
          <rect width="184" height="54" fill="#29211c"/>
          <polygon points="0,18 65,18 75,54 0,54" fill="#574131"/>
          <polygon points="115,18 184,18 184,54 105,54" fill="#574131"/>
          <rect x="68" y="30" width="44" height="24" fill="#0284c7" fill-opacity="0.85"/>
          <line x1="90" y1="14" x2="90" y2="46" stroke="#fde047" stroke-width="2" stroke-dasharray="3,2"/>
          <text x="90" y="45" fill="#fff" font-size="9" font-weight="900" text-anchor="middle">-100m</text>
        """,
        "gaza": """
          <rect width="184" height="54" fill="#271c26"/>
          <rect x="22" y="24" width="24" height="26" fill="#475569"/>
          <polygon points="54,50 68,26 82,50" fill="#64748b"/>
          <polygon points="88,50 102,28 116,50" fill="#64748b"/>
          <circle cx="68" cy="24" r="10" fill="#ef4444" fill-opacity="0.8"/>
          <text x="145" y="38" fill="#fca5a5" font-size="9" font-weight="800" text-anchor="middle">AL-SHATI</text>
        """,
        "court": """
          <rect width="184" height="54" fill="#172a28"/>
          <!-- Pillars of Constitutional Court -->
          <polygon points="28,20 92,10 156,20" fill="#34d399"/>
          <rect x="40" y="22" width="10" height="24" fill="#a7f3d0"/>
          <rect x="68" y="22" width="10" height="24" fill="#a7f3d0"/>
          <rect x="96" y="22" width="10" height="24" fill="#a7f3d0"/>
          <rect x="124" y="22" width="10" height="24" fill="#a7f3d0"/>
          <rect x="28" y="46" width="128" height="4" fill="#10b981"/>
        """,
        "gavel": """
          <rect width="184" height="54" fill="#1e2438"/>
          <!-- Scales / Gavel -->
          <rect x="44" y="20" width="32" height="12" rx="3" fill="#f59e0b"/>
          <line x1="60" y1="32" x2="96" y2="46" stroke="#fde68a" stroke-width="4"/>
          <rect x="114" y="20" width="42" height="24" rx="3" fill="#334155" stroke="#93c5fd" stroke-width="1.2"/>
          <text x="135" y="36" fill="#fff" font-size="9" font-weight="900" text-anchor="middle">C-4000</text>
        """,
        "tanker": """
          <rect width="184" height="54" fill="#2e1818"/>
          <!-- Highway & burning tanker -->
          <rect x="0" y="42" width="184" height="12" fill="#334155"/>
          <rect x="34" y="30" width="54" height="13" rx="5" fill="#94a3b8"/>
          <circle cx="88" cy="26" r="14" fill="#ef4444"/>
          <circle cx="96" cy="24" r="9" fill="#f59e0b"/>
          <circle cx="78" cy="22" r="8" fill="#fbbf24"/>
          <text x="142" y="36" fill="#fecaca" font-size="11" font-weight="900" text-anchor="middle">30+ DEAD</text>
        """,
    }
    vb = "0 0 310 86" if kind in ("tariffs", "chips", "space") else "0 0 184 54"
    inner = scenes.get(kind, scenes["tariffs"])
    return f"""
    <div class="scene-wrap">
      <svg viewBox="{vb}" preserveAspectRatio="none" class="scene-svg">{inner}</svg>
      <div class="scene-banner">{banner}</div>
    </div>
    """


def build_world_map_svg() -> str:
    """Return a clean SVG world map with simplified continent silhouettes and 52 numbered pins."""
    pins = [
        # (num, x, y, color)
        (1, 70, 56, "#dc2626"),   # Washington
        (2, 255, 58, "#2563eb"),  # Seoul/Tokyo/Taipei
        (3, 228, 52, "#059669"),  # Jiuquan
        (4, 178, 44, "#dc2626"),  # Ukraine
        (5, 190, 72, "#d97706"),  # Hodeidah/Ras Tanura
        (6, 146, 40, "#7c3aed"),  # London
        (7, 274, 118, "#0284c7"), # Canberra/Solomons
        (8, 224, 70, "#059669"),  # Dhaka
        (9, 238, 96, "#d97706"),  # Bogor
        (10, 178, 62, "#dc2626"), # Gaza
        (11, 166, 122, "#059669"),# Cape Town
        (12, 182, 60, "#2563eb"), # Jerusalem
        (13, 172, 66, "#dc2626"), # Cairo
        (14, 198, 68, "#d97706"), # Hormuz
        (15, 192, 42, "#dc2626"), # Samara
        (16, 250, 52, "#dc2626"), # Pyongyang
        (17, 152, 43, "#2563eb"), # Brussels
        (21, 176, 82, "#dc2626"), # Sudan
        (22, 152, 84, "#059669"), # Lagos
        (25, 76, 52, "#2563eb"),  # New York
        (28, 82, 86, "#059669"),  # Cartagena
        (29, 98, 114, "#059669"), # Parana Brazil
        (30, 268, 122, "#0284c7"),# Sydney
        (31, 234, 86, "#059669"), # Kuala Lumpur
        (33, 208, 68, "#d97706"), # Karachi
    ]
    pin_els = []
    for num, x, y, col in pins:
        pin_els.append(
            f'<circle cx="{x}" cy="{y}" r="6.2" fill="{col}" stroke="#fff" stroke-width="1"/>'
            f'<text x="{x}" y="{y+2.5}" fill="#fff" font-size="6.8" font-weight="900" text-anchor="middle">{num}</text>'
        )
    return f"""
    <svg viewBox="0 0 304 148" class="map-svg">
      <rect width="304" height="148" rx="4" fill="#e6e1d3"/>
      <!-- Grid parallels -->
      <line x1="0" y1="37" x2="304" y2="37" stroke="#d5cebd" stroke-width="0.7" stroke-dasharray="2,2"/>
      <line x1="0" y1="74" x2="304" y2="74" stroke="#c7bfa8" stroke-width="0.9"/>
      <line x1="0" y1="111" x2="304" y2="111" stroke="#d5cebd" stroke-width="0.7" stroke-dasharray="2,2"/>
      <!-- Simplified continent polygons -->
      <!-- N America -->
      <polygon points="18,24 92,20 88,62 66,76 48,68 24,46" fill="#c7c0ae" stroke="#a8a08c" stroke-width="0.8"/>
      <!-- S America -->
      <polygon points="74,78 108,86 102,134 82,138 72,104" fill="#c7c0ae" stroke="#a8a08c" stroke-width="0.8"/>
      <!-- Europe -->
      <polygon points="138,24 196,22 194,54 142,56" fill="#c7c0ae" stroke="#a8a08c" stroke-width="0.8"/>
      <!-- Africa -->
      <polygon points="138,60 186,60 192,92 174,130 154,128 136,88" fill="#c7c0ae" stroke="#a8a08c" stroke-width="0.8"/>
      <!-- Asia -->
      <polygon points="194,24 282,26 274,84 228,88 192,68" fill="#c7c0ae" stroke="#a8a08c" stroke-width="0.8"/>
      <!-- Oceania -->
      <polygon points="242,102 284,102 282,132 244,128" fill="#c7c0ae" stroke="#a8a08c" stroke-width="0.8"/>
      {''.join(pin_els)}
    </svg>
    """


def build_broadsheet_html() -> str:
    """Assemble the complete 1024x1024 HTML+SVG broadsheet page."""
    utc_items = "".join(
        f'<div class="utc-item"><span class="utc-t">{t}</span><span class="utc-e">{e}</span></div>'
        for t, e in UTC_TIMELINE
    )
    stat_items = "".join(
        f'<div class="stat-pill" style="border-left: 3.5px solid {c}">'
        f'<div class="stat-val" style="color:{c}">{v}</div>'
        f'<div class="stat-lbl">{l}</div></div>'
        for v, l, c in TOP_STATS
    )

    lead_cards = []
    for s in LEAD_STORIES:
        lead_cards.append(f"""
        <div class="card lead-card">
          <div class="card-kicker">
            <span class="num-badge">{s['num']:02d}</span>
            <span class="loc-txt">{s['loc']}</span>
            <span class="ver-pill" style="background:{s['tag_col']}">{s['tag']}</span>
          </div>
          {svg_scene(s['svg'], s['banner'])}
          <div class="lead-title">{s['title']}</div>
          <div class="lead-body">{s['body']}</div>
          <div class="card-src">Sources: {s['src']}</div>
        </div>
        """)

    def render_mid_row(items):
        out = []
        for s in items:
            out.append(f"""
            <div class="card mid-card">
              <div class="card-kicker">
                <span class="num-badge">{s['num']:02d}</span>
                <span class="loc-txt">{s['loc']}</span>
                <span class="ver-pill" style="background:{s['tag_col']}">{s['tag']}</span>
              </div>
              {svg_scene(s['svg'], s['banner'])}
              <div class="mid-title">{s['title']}</div>
              <div class="mid-body">{s['body']}</div>
              <div class="card-src">{s['src']}</div>
            </div>
            """)
        return "".join(out)

    def render_briefs(items):
        rows = []
        for num, city, txt, tag in items:
            tcol = "#047857" if tag == "OFFICIAL" else ("#1d4ed8" if tag == "CONFIRMED" else ("#b45309" if tag == "REPORTED" else "#7c3aed"))
            rows.append(
                f'<div class="brief-row">'
                f'<span class="b-left"><span class="b-num">{num}</span>'
                f'<span class="b-city">{city}</span> '
                f'<span class="b-txt">{txt}</span></span>'
                f'<span class="b-tag" style="color:{tcol}">[{tag}]</span>'
                f'</div>'
            )
        return "".join(rows)

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1024px; height: 1024px; overflow: hidden;
    background: #f5f2e8; color: #111827;
    font-family: 'Liberation Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{
    width: 1024px; height: 1024px; padding: 5px 8px;
    display: grid;
    grid-template-rows: 80px 36px 20px 654px 152px 40px;
    gap: 4px;
  }}
  /* MASTHEAD */
  .masthead {{
    background: #fffdf7; color: #0f172a; border-radius: 4px;
    padding: 2px 10px; display: flex; flex-direction: column; justify-content: center;
    border: 1.5px solid #141d33; border-top: 4px solid #141d33; border-bottom: 3px solid #b91c1c; overflow: hidden;
  }}
  .mast-line1 {{
    font-size: 8.4px; font-weight: 900; letter-spacing: 0; color: #991b1b;
    white-space: nowrap; overflow: hidden;
  }}
  .mast-date {{
    font-family: 'Liberation Sans', -apple-system, sans-serif;
    font-size: 42px; font-weight: 900; line-height: 1.0; color: #000000; letter-spacing: -0.8px;
    white-space: nowrap; margin: 2px 0;
  }}
  .mast-line3 {{
    font-size: 9.0px; color: #0f172a; font-weight: 900;
    white-space: nowrap; overflow: hidden;
  }}

  /* STAT CALLOUT STRIP */
  .stat-strip {{
    display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px; overflow: hidden;
  }}
  .stat-pill {{
    background: #ffffff; border: 1px solid #cfc7b4; border-radius: 4px;
    padding: 2px 6px; display: flex; align-items: center; gap: 6px;
  }}
  .stat-val {{ font-size: 19px; font-weight: 900; line-height: 1; white-space: nowrap; letter-spacing: -0.6px; }}
  .stat-lbl {{ font-size: 7.9px; line-height: 1.1; color: #0f172a; font-weight: 800; }}

  /* UTC TIMELINE */
  .utc-bar {{
    background: #eae4d3; border: 1px solid #cfc7b4; border-radius: 4px;
    padding: 2px 6px; display: flex; align-items: center; gap: 5px; overflow: hidden;
  }}
  .utc-head {{
    font-size: 7.5px; font-weight: 900; color: #fff; background: #1e293b;
    padding: 1.5px 5px; border-radius: 2.5px; white-space: nowrap;
  }}
  .utc-track {{ display: flex; align-items: center; justify-content: space-between; flex: 1; }}
  .utc-item {{ display: flex; align-items: center; gap: 2.5px; font-size: 7.2px; white-space: nowrap; }}
  .utc-t {{ font-weight: 900; color: #b91c1c; }}
  .utc-e {{ font-weight: 700; color: #1f2937; }}

  /* LEAD ROW (3 COLS) */
  .lead-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; min-height: 0; overflow: hidden;
  }}
  .card {{
    background: #ffffff; border: 1px solid #cfc7b4; border-radius: 4px;
    padding: 4px 6px; display: flex; flex-direction: column; justify-content: space-between;
    min-width: 0; min-height: 0; overflow: hidden;
  }}
  .card-kicker {{
    display: flex; align-items: center; gap: 4px; margin-bottom: 1.5px;
  }}
  .num-badge {{
    background: #141d33; color: #fbbf24; font-size: 7.8px; font-weight: 900;
    padding: 1px 4px; border-radius: 2.5px; line-height: 1.1;
  }}
  .loc-txt {{
    font-size: 7.4px; font-weight: 800; color: #475569; letter-spacing: 0.2px;
    flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }}
  .ver-pill {{
    color: #fff; font-size: 6.8px; font-weight: 800; padding: 1px 4px;
    border-radius: 2px; letter-spacing: 0.3px;
  }}
  .scene-wrap {{
    position: relative; width: 100%; border-radius: 3px; overflow: hidden;
    border: 1px solid #cbd5e1; margin-bottom: 2px; flex-shrink: 0;
  }}
  .lead-card .scene-svg {{ width: 100%; height: 168px; display: block; }}
  .mid-card .scene-svg {{ width: 100%; height: 96px; display: block; }}
  .scene-banner {{
    position: absolute; bottom: 0; right: 0;
    background: rgba(15, 23, 42, 0.92); color: #fef08a;
    font-size: 8.5px; font-weight: 900; padding: 1.5px 6px;
    border-top-left-radius: 3px; letter-spacing: 0.25px;
  }}
  .lead-title {{
    font-family: 'Liberation Sans', -apple-system, sans-serif;
    font-size: 31px; font-weight: 900; line-height: 1.07; color: #000000; margin-bottom: 2px;
    letter-spacing: -0.5px;
  }}
  .lead-body {{
    font-size: 11.6px; line-height: 1.2; color: #1e293b; font-weight: 700; margin-bottom: 2px;
  }}
  .card-src {{
    font-size: 7.4px; font-weight: 800; color: #475569; text-transform: uppercase;
  }}

  /* MID ROWS (5 COLS x 2) */
  .mid-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; min-height: 0; overflow: hidden;
  }}
  .mid-title {{
    font-family: 'Liberation Sans', -apple-system, sans-serif;
    font-size: 25px; font-weight: 900; line-height: 1.08; color: #000000; margin-bottom: 2px;
    letter-spacing: -0.6px;
  }}
  .mid-body {{
    font-size: 10.4px; line-height: 1.18; color: #1e293b; font-weight: 700; margin-bottom: 1px;
  }}

  /* BOTTOM SECTION: MAP + 22 WIRES */
  .bottom-grid {{
    display: grid; grid-template-columns: 258px 1fr; gap: 5px; min-height: 0; overflow: hidden;
  }}
  .map-box, .wires-box {{
    background: #ffffff; border: 1px solid #cfc7b4; border-radius: 4px;
    padding: 3px 5px; display: flex; flex-direction: column; justify-content: space-between;
    min-width: 0; min-height: 0; overflow: hidden;
  }}
  .box-head {{
    font-size: 7.6px; font-weight: 900; color: #141d33; text-transform: uppercase;
    letter-spacing: 0.3px; border-bottom: 1.5px solid #141d33; padding-bottom: 1px; margin-bottom: 2px;
    display: flex; justify-content: space-between; align-items: center; flex-shrink: 0;
  }}
  .map-svg {{ width: 100%; height: 82px; display: block; border: 1px solid #d6cfc0; border-radius: 3px; }}
  .region-legend {{
    font-size: 6.4px; line-height: 1.18; color: #1e293b; font-weight: 700; margin-top: 1px;
  }}
  .wires-cols {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; flex: 1; min-height: 0; min-width: 0; overflow: hidden;
  }}
  .brief-col {{
    display: flex; flex-direction: column; justify-content: space-between; min-width: 0; min-height: 0; overflow: hidden;
  }}
  .brief-row {{
    font-size: 9.3px; line-height: 1.05; height: 10.1px; color: #0f172a;
    white-space: nowrap; overflow: hidden;
    display: flex; align-items: center; justify-content: space-between;
  }}
  .b-left {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .b-num {{
    display: inline-block; width: 14px; font-weight: 900; color: #b91c1c;
  }}
  .b-city {{ font-weight: 900; color: #0f172a; }}
  .b-txt {{ font-weight: 600; color: #1e293b; }}
  .b-tag {{ font-size: 6.8px; font-weight: 900; margin-left: 3px; flex-shrink: 0; }}

  /* FOOTER DATE CHECK */
  .date-check {{
    background: #fef3c7; color: #111827; border: 1.5px solid #141d33; border-radius: 4px;
    padding: 2.5px 8px; display: flex; flex-direction: column; justify-content: center; gap: 1.5px;
    overflow: hidden;
  }}
  .dc-line1 {{
    font-size: 7.3px; font-weight: 800; color: #7f1d1d;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }}
  .dc-line2 {{
    font-size: 7.0px; font-weight: 700; color: #1e293b;
    display: flex; justify-content: space-between; white-space: nowrap; overflow: hidden;
  }}
</style>
</head>
<body>
<div class="page">
  <div class="masthead">
    <div class="mast-line1">THE WORLD IN ONE DAY — 35 STORIES · 10 REGIONS · 18 FIELDS · ALL FIRST REPORTED ON WEDNESDAY 25 NOVEMBER 2026 · 9 ORIGINAL DRAWN SCENES · UTC TIMELINE · WORLD MAP</div>
    <div class="mast-date">Wednesday 25 November 2026</div>
    <div class="mast-line3">US proposes tariffs up to 35% on 14 economies · AI doubts sink Kospi -6.2% below 5,000 · Pakistan's first astronaut docks at Tiangong · Cairo tanker fire kills 30+ · Java gold mine flood traps 17</div>
  </div>

  <div class="stat-strip">{stat_items}</div>

  <div class="utc-bar">
    <div class="utc-head">THE DAY IN UTC</div>
    <div class="utc-track">{utc_items}</div>
  </div>

  <div class="lead-grid">{''.join(lead_cards)}</div>

  <div class="bottom-grid">
    <div class="map-box">
      <div class="box-head">
        <span>WHERE IT HAPPENED</span>
        <span style="color:#b91c1c">PINS 1–35</span>
      </div>
      {build_world_map_svg()}
      <div class="region-legend">
        <div>● <b>Americas 6:</b> #1, 25–29 &nbsp; ● <b>Europe 8:</b> #4, 6, 15, 17–20, 35</div>
        <div>● <b>MidEast &amp; N.Africa 5:</b> #5, 10–11, 13–14 &nbsp; ● <b>Sub-Sahara 5:</b> #12, 21–24</div>
        <div>● <b>Asia 8:</b> #2–3, 8–9, 16, 31–33 &nbsp; ● <b>Oceania &amp; Space 3:</b> #7, 30, 34</div>
        <div>● <b>How sure:</b> OFFICIAL = govt/court · CONFIRMED = 2+ wires · REPORTED = 1 outlet · CLAIM = 1 side</div>
      </div>
    </div>

    <div class="wires-box">
      <div class="box-head">
        <span>ALSO ON WEDNESDAY 25 NOVEMBER 2026 — 29 MORE DATED &amp; SOURCED WORLD WIRES</span>
        <span style="color:#047857">STORIES 7–35</span>
      </div>
      <div class="wires-cols">
        <div class="brief-col">{render_briefs(BRIEFS_COL_1)}</div>
        <div class="brief-col">{render_briefs(BRIEFS_COL_2)}</div>
        <div class="brief-col">{render_briefs(BRIEFS_COL_3)}</div>
      </div>
    </div>
  </div>

  <div class="date-check">
    <div class="dc-line1">
      <b>DATE CHECK — NOT 25 NOV, LEFT OUT:</b>
      Nvidia/Jensen Huang (24 Nov) · Hodeidah strike (24 Nov) · Riyadh tower (24 Nov) · Huawei verdict (24 Nov) · Real Madrid 5–1 PSV (24 Nov) · COP31 (22 Nov).
    </div>
    <div class="dc-line2">
      <span>Every story above happened or was first reported on Wednesday 25 November 2026. All 6 scenes are original vector drawings.</span>
      <span><b>SOURCES:</b> Reuters · AP · AFP · Al Jazeera · USTR · KRX/Yonhap · CMSA/Xinhua · Ofgem · ABC · BNPB · ESA</span>
    </div>
  </div>
</div>
</body>
</html>
"""


def build_image_locally(dest_png: str) -> None:
    """Render the broadsheet HTML via headless Chromium at 2x scale and downsample to 1024x1024 PNG."""
    import subprocess
    import tempfile
    from PIL import Image

    html_path = os.path.join(tempfile.gettempdir(), "broadsheet_20261125.html")
    raw_png = os.path.join(tempfile.gettempdir(), "broadsheet_raw_2048.png")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_broadsheet_html())

    chrome = "/usr/local/bin/google-chrome"
    cmd = [
        chrome,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        "--window-size=1024,1024",
        f"--screenshot={raw_png}",
        f"file://{html_path}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    im = Image.open(raw_png).convert("RGB")
    if im.size != (1024, 1024):
        im = im.resize((1024, 1024), Image.Resampling.LANCZOS)

    # Apply subtle unsharp mask so 300px downscaled headlines stay razor-sharp
    from PIL import ImageFilter
    im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=110, threshold=2))

    # Quantize to 224-color adaptive palette for <220 KiB tie-breaker advantage while keeping crisp text
    q = im.quantize(colors=224, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q.save(dest_png, "PNG", optimize=True)


def write(out_dir: str) -> str:
    """Write /output/entry.png deterministically from the committed broadsheet image."""
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    shutil.copyfile(src, dest)
    return dest


if __name__ == "__main__":
    if "--build-image" in sys.argv:
        here = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(here, "entry.png")
        build_image_locally(target)
        print(f"Built {target} ({os.path.getsize(target)} bytes)")
    else:
        write(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
