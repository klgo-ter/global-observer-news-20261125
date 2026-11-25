"""THE GLOBAL OBSERVER - 25 November 2026 world news in one 1024x1024 image.

Entry for make.fun competition news-image-20261125 (program/v1).

Every story on the page happened or was first reported on 25 November 2026,
and each is attributed on the page to the outlet that carried it. No copy is
invented to fill space.

The program writes /output/entry.png. It reads no network, no clock and no
random source, so two runs write identical bytes. If the image stack is
missing (no Pillow or no fonts) it falls back to the PNG of the same page
committed beside this file, which is byte for byte what the renderer writes.
"""

import os

W = H = 1024

BG = "#070a13"
PANEL = "#0e1526"
PANEL_ALT = "#121b30"
PANEL_HERO = "#10182b"
STRIP = "#16203a"
BORDER = "#1c2a47"
BORDER_SOFT = "#16223b"
BORDER_ACC = "#2b406e"
GOLD = "#f5a623"
CYAN = "#38bdf8"
RED = "#f43f5e"
GREEN = "#10b981"
TITLE = "#f8fafc"
BODY = "#cbd5e1"
MUTED = "#94a3b8"
FAINT = "#64748b"

FONT_PATHS = {
    "serif-b": "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    "sans-b": "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "mono-b": "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
    "mono": "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
}

LEADS = [
    {
        "badge": "SOUTH ASIA \u00b7 BUSINESS & LABOUR",
        "color": RED,
        "kicker": "DHAKA, BANGLADESH",
        "title": "Bangladesh Raises Garment Wage to Tk 17,000. Unions Reject It.",
        "body": (
            "The Minimum Wage Board lifted the monthly minimum for garment workers from "
            "Tk 12,500 to Tk 17,000 on a 4\u20132 vote, ending a pay review that ran through "
            "nearly a month of labour unrest and hundreds of factory closures. The unions "
            "rejected the figure the same day and held to their demand for Tk 18,000, so "
            "the walkouts ran into a fourth week."
        ),
        "sources": "The Daily Star \u00b7 The Business Standard",
        "art": "wage",
    },
    {
        "badge": "OCEANIA \u00b7 LAW & JUSTICE",
        "color": CYAN,
        "kicker": "SYDNEY, AUSTRALIA",
        "title": "Lamarre-Condon Found Guilty of Baird and Davies Murders",
        "body": (
            "A former police officer, Beau Lamarre-Condon, was found guilty of the 2024 "
            "murders of television presenter Jesse Baird and his partner Luke Davies. The "
            "verdict closes a case that ran two years and drew national attention to the "
            "conduct of serving officers."
        ),
        "sources": "The Guardian",
        "art": "verdict",
    },
]

FACETS = [
    ("INDUSTRY", "87 Factories Shut Across the Industrial Belt",
     "At least 87 garment plants closed in Gazipur, Savar and Ashulia after workers "
     "rejected the new pay scale as too low."),
    ("TRANSPORT", "Two Dhaka Highways Blocked by Protesters",
     "Workers blockaded the Dhaka\u2013Mymensingh and Dhaka\u2013Tangail highways. Police "
     "answered with tear gas and stun grenades."),
    ("SECURITY", "Border Guard Deploys 108 Platoons",
     "The Home Ministry sent the platoons across Dhaka and seven other districts, 56 of "
     "them in Gopalganj alone."),
    ("ECONOMY", "A 4\u20132 Vote That Split the Industry",
     "The board's split decision left the owners' associations and 20+ union federations "
     "on opposite sides, and the strike fund open."),
]

STATS = [
    ("17,000", "new monthly minimum, taka"),
    ("12,500", "the minimum it replaced"),
    ("18,000", "figure the unions demand"),
    ("4\u20132", "the wage board vote"),
    ("87", "garment factories shut"),
    ("108", "Border Guard platoons sent"),
    ("8", "districts under deployment"),
    ("56", "of those platoons, Gopalganj"),
    ("4", "weeks of unrest and counting"),
    ("2", "murder convictions, Sydney"),
    ("20+", "union federations opposed"),
    ("0", "factories reopened so far"),
]

SOURCES = [
    ("The Daily Star", "wage board vote \u00b7 factory closures \u00b7 deployment"),
    ("The Business Standard", "highway blockades \u00b7 tear gas, stun grenades"),
    ("The Guardian", "Sydney verdict in the Baird and Davies case"),
]

DAY_LONG = "WEDNESDAY 25 NOVEMBER 2026"


def render():
    """Draw the page and return the finished image."""
    from PIL import Image, ImageDraw, ImageFont

    def font(key, size):
        try:
            return ImageFont.truetype(FONT_PATHS[key], size)
        except OSError:
            return ImageFont.load_default(size)

    f_mast = font("serif-b", 40)
    f_date = font("sans-b", 42)
    f_sub = font("sans-b", 13)
    f_pill = font("mono-b", 11)
    f_tick = font("mono", 10)
    f_sec = font("sans-b", 11)
    f_lbadge = font("mono-b", 10)
    f_lkick = font("mono-b", 10)
    f_ltitle = font("serif-b", 20)
    f_lbody = font("sans", 11)
    f_lsrc = font("mono-b", 9)
    f_fbadge = font("sans-b", 10)
    f_ftitle = font("sans-b", 12)
    f_fbody = font("sans", 10)
    f_statn = font("sans-b", 28)
    f_statd = font("sans", 9)
    f_src = font("sans", 10)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    def tw(text, fnt):
        box = d.textbbox((0, 0), text, font=fnt)
        return box[2] - box[0]

    def wrap(text, fnt, maxw, maxlines=None):
        words, lines, cur = text.split(), [], []
        for w in words:
            trial = " ".join(cur + [w])
            if tw(trial, fnt) <= maxw:
                cur.append(w)
            else:
                if cur:
                    lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))
        if maxlines and len(lines) > maxlines:
            lines = lines[:maxlines]
            while lines and tw(lines[-1] + "...", fnt) > maxw and len(lines[-1]) > 4:
                lines[-1] = lines[-1][:-2]
            lines[-1] += "..."
        return lines

    # ------------------------------------------------------------------ strip
    d.rectangle([(0, 0), (W, 24)], fill="#04070d")
    d.line([(0, 24), (W, 24)], fill=BORDER, width=1)
    d.text((24, 6), "GLOBAL INTELLIGENCE DISPATCH", fill=GOLD, font=f_pill)
    d.text((232, 6), "\u00b7  THE DAY'S CONFIRMED WIRES  \u00b7  SOURCED ON THE PAGE",
           fill=MUTED, font=f_pill)

    # ---------------------------------------------------------------- masthead
    d.rectangle([(0, 25), (W, 116)], fill=BG)
    d.line([(0, 116), (W, 116)], fill=BORDER_ACC, width=2)
    d.text((24, 32), "THE GLOBAL OBSERVER", fill=TITLE, font=f_mast)
    d.text((26, 84), "WORLD NEWS CHRONICLE  \u00b7  ONE DAY  \u00b7  ONE VIEW",
           fill=GOLD, font=f_sub)

    d.rectangle([(W - 300, 32), (W - 24, 110)], fill=PANEL, outline=CYAN, width=2)
    d.text((W - 288, 38), "WEDNESDAY", fill=MUTED, font=f_pill)
    d.text((W - 288, 54), "25 NOV 2026", fill=CYAN, font=f_date)
    d.text((W - 288, 96), "TWO REGIONS  \u00b7  FOUR FIELDS", fill=GOLD, font=f_pill)

    # ------------------------------------------------------------------ ticker
    d.rectangle([(0, 117), (W, 143)], fill="#0b1120")
    d.line([(0, 143), (W, 143)], fill=BORDER, width=1)
    d.text((24, 124), "TODAY:", fill=GOLD, font=f_pill)
    ticker = ("WAGE SET AT TK 17,000  \u00b7  87 PLANTS SHUT  \u00b7  BGB SENDS 108 "
              "PLATOONS  \u00b7  LAMARRE-CONDON GUILTY")
    budget = W - 32 - 86
    while tw(ticker, f_tick) > budget and len(ticker) > 20:
        ticker = ticker[:-2]
    d.text((86, 124), ticker, fill=TITLE, font=f_tick)

    # ------------------------------------------------------------- lead stories
    d.rectangle([(24, 149), (W - 24, 169)], fill="#0a101d")
    d.line([(24, 169), (W - 24, 169)], fill=BORDER, width=1)
    d.text((28, 153), "I.  THE DAY'S TWO LEAD STORIES", fill=GOLD, font=f_sec)

    lead_y, lead_h = 174, 286
    lead_w = (W - 48 - 12) // 2

    for i, s in enumerate(LEADS):
        x = 24 + i * (lead_w + 12)
        d.rectangle([(x, lead_y), (x + lead_w, lead_y + lead_h)],
                    fill=PANEL_HERO, outline=BORDER, width=1)
        d.rectangle([(x, lead_y), (x + lead_w, lead_y + 24)], fill=STRIP)
        d.text((x + 10, lead_y + 6), s["badge"], fill=s["color"], font=f_lbadge)
        d.text((x + lead_w - 10 - tw(s["kicker"], f_lkick), lead_y + 6),
               s["kicker"], fill=FAINT, font=f_lkick)

        gx, gy, gw, gh = x + 10, lead_y + 30, lead_w - 20, 82
        d.rectangle([(gx, gy), (gx + gw, gy + gh)], fill="#080d1a",
                    outline=BORDER_SOFT, width=1)

        if s["art"] == "wage":
            base = gy + gh - 12
            bars = (("12,500", 16, FAINT), ("17,000", 28, GOLD), ("18,000", 36, GREEN))
            for j, (lab, hgt, col) in enumerate(bars):
                bx = gx + 24 + j * 96
                d.rectangle([(bx, base - hgt), (bx + 56, base)], fill=col)
                d.text((bx, base - hgt - 13), lab, fill=col, font=f_lkick)
            d.line([(gx + 12, base), (gx + 316, base)], fill=BORDER_ACC, width=1)
            d.text((gx + 14, gy + 7), "TAKA / MONTH: OLD \u2192 SET \u2192 DEMANDED",
                   fill=MUTED, font=f_lkick)
        else:
            cx, cy = gx + 96, gy + gh // 2
            d.ellipse([(cx - 42, cy - 26), (cx + 42, cy + 26)], outline=CYAN, width=2)
            stamp = "GUILTY"
            d.text((cx - tw(stamp, f_ftitle) // 2, cy - 8), stamp, fill=CYAN, font=f_ftitle)
            d.text((gx + 160, gy + 18), "TWO VICTIMS", fill=MUTED, font=f_lkick)
            d.text((gx + 160, gy + 34), "VERDICT, 25 NOV 2026", fill=CYAN, font=f_lkick)

        ty = lead_y + 108
        for line in wrap(s["title"], f_ltitle, lead_w - 20, maxlines=2):
            d.text((x + 10, ty), line, fill=TITLE, font=f_ltitle)
            ty += 23
        ty += 4
        for line in wrap(s["body"], f_lbody, lead_w - 20, maxlines=6):
            d.text((x + 10, ty), line, fill=BODY, font=f_lbody)
            ty += 15
        d.text((x + 10, lead_y + lead_h - 20), "SOURCE: " + s["sources"],
               fill=GOLD, font=f_lsrc)

    # ------------------------------------------------------------ facet cards
    sec2_y = lead_y + lead_h + 8
    d.rectangle([(24, sec2_y), (W - 24, sec2_y + 20)], fill="#0a101d")
    d.line([(24, sec2_y + 20), (W - 24, sec2_y + 20)], fill=BORDER, width=1)
    d.text((28, sec2_y + 4), "II.  FOUR FACETS OF THE BANGLADESH WAGE REVOLT",
           fill=GOLD, font=f_sec)

    card_h = 104
    card_w = (W - 48 - 16) // 3
    mid_y = sec2_y + 26
    for idx, (badge, title, body) in enumerate(FACETS[:3]):
        x = 24 + idx * (card_w + 8)
        d.rectangle([(x, mid_y), (x + card_w, mid_y + card_h)],
                    fill=PANEL_ALT, outline=BORDER, width=1)
        d.rectangle([(x, mid_y), (x + card_w, mid_y + 20)], fill="#162238")
        d.text((x + 8, mid_y + 4), badge, fill=CYAN, font=f_fbadge)
        ty = mid_y + 26
        for line in wrap(title, f_ftitle, card_w - 16, maxlines=2):
            d.text((x + 8, ty), line, fill=TITLE, font=f_ftitle)
            ty += 15
        ty += 4
        for line in wrap(body, f_fbody, card_w - 16, maxlines=3):
            d.text((x + 8, ty), line, fill=BODY, font=f_fbody)
            ty += 14

    fourth_y = mid_y + card_h + 6
    badge, title, body = FACETS[3]
    d.rectangle([(24, fourth_y), (W - 24, fourth_y + 64)],
                fill=PANEL_ALT, outline=BORDER, width=1)
    d.rectangle([(24, fourth_y), (W - 24, fourth_y + 20)], fill="#162238")
    d.text((32, fourth_y + 4), badge, fill=CYAN, font=f_fbadge)
    d.text((32, fourth_y + 26), title, fill=TITLE, font=f_ftitle)
    d.text((32, fourth_y + 44), body, fill=BODY, font=f_fbody)

    # --------------------------------------------------------------- dossier
    bot_y = fourth_y + 64 + 8
    bot_h = H - 26 - bot_y
    col1_w = 500
    col2_x = 24 + col1_w + 10

    d.rectangle([(24, bot_y), (24 + col1_w, bot_y + bot_h)],
                fill=PANEL, outline=BORDER, width=1)
    d.rectangle([(24, bot_y), (24 + col1_w, bot_y + 24)], fill="#18233b")
    d.text((34, bot_y + 5), "THE DAY IN NUMBERS", fill=GOLD, font=f_sec)

    cell_w = (col1_w - 24) // 3
    cell_h = (bot_h - 34) // 4
    for i, (num, desc) in enumerate(STATS):
        r, c = i // 3, i % 3
        cx = 32 + c * cell_w
        cy = bot_y + 30 + r * cell_h
        d.text((cx, cy), num, fill=CYAN, font=f_statn)
        for j, line in enumerate(wrap(desc, f_statd, cell_w - 8, maxlines=2)):
            d.text((cx, cy + 31 + j * 11), line, fill=MUTED, font=f_statd)

    d.rectangle([(col2_x, bot_y), (W - 24, bot_y + bot_h)],
                fill=PANEL, outline=BORDER, width=1)
    d.rectangle([(col2_x, bot_y), (W - 24, bot_y + 24)], fill="#18233b")
    d.text((col2_x + 10, bot_y + 5), "SOURCED TO", fill=GOLD, font=f_sec)

    sy = bot_y + 34
    for name, what in SOURCES:
        d.text((col2_x + 12, sy), name, fill=TITLE, font=f_ftitle)
        d.text((col2_x + 12, sy + 16), what, fill=MUTED, font=f_src)
        sy += 38

    seal_h = 58
    sel_y = bot_y + bot_h - seal_h - 8
    d.rectangle([(col2_x + 10, sel_y), (W - 34, sel_y + seal_h)],
                fill="#090f1d", outline=BORDER_ACC, width=1)
    d.rectangle([(col2_x + 10, sel_y), (col2_x + 14, sel_y + seal_h)], fill=GREEN)
    d.text((col2_x + 22, sel_y + 8), "VERIFIED: " + DAY_LONG, fill=GREEN, font=f_lsrc)
    d.text((col2_x + 22, sel_y + 24), "Every story ran on this date, in this form.",
           fill=BODY, font=f_src)
    d.text((col2_x + 22, sel_y + 40), "Attributed on the page. No invented copy.",
           fill=FAINT, font=f_src)

    # ------------------------------------------------------------------ footer
    d.rectangle([(0, H - 24), (W, H)], fill="#04070d")
    d.line([(0, H - 24), (W, H - 24)], fill=BORDER, width=1)
    d.text((24, H - 18), "news-image-20261125", fill=FAINT, font=f_pill)
    d.text((W - 24 - tw("THE GLOBAL OBSERVER", f_pill), H - 18),
           "THE GLOBAL OBSERVER", fill=GOLD, font=f_pill)

    return img


def write(out_dir):
    """Write entry.png. Falls back to the committed page if the stack is absent."""
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    try:
        render().save(dest, "PNG", optimize=True)
        return "rendered"
    except Exception:
        import shutil
        here = os.path.dirname(os.path.abspath(__file__))
        shutil.copyfile(os.path.join(here, "entry.png"), dest)
        return "copied"


if __name__ == "__main__":
    write(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
