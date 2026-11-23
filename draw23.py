#!/usr/bin/env python3
"""Draw the 23 November 2026 front page. Fresh code, Pillow + stdlib only.
All text is hardcoded from verified reporting; no network use.
Output: entry.png, 1024x1024, next to this script."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W, H = 1024, 1024

FDIR = "/usr/share/fonts/truetype/liberation/"
SERIF = FDIR + "LiberationSerif-Regular.ttf"
SERIF_B = FDIR + "LiberationSerif-Bold.ttf"
SERIF_I = FDIR + "LiberationSerif-Italic.ttf"
SANS = FDIR + "LiberationSans-Regular.ttf"
SANS_B = FDIR + "LiberationSans-Bold.ttf"

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (179, 32, 44)
BLUE = (18, 52, 86)
SKY = (214, 230, 240)
SEA = (203, 224, 235)
LAND = (232, 222, 196)
GREY = (90, 88, 82)
RULE = (120, 116, 108)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, fnt, fill=INK, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centre(d, y, s, fnt, fill=INK):
    d.text((W // 2, y), s, font=fnt, fill=fill, anchor="ma")


def hline(d, y, x0=28, x1=996, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- top bar + eyebrow ----------
d.rectangle([0, 0, W, 6], fill=INK)
y = 12
text(d, (28, y), "THE WORLD IN ONE DAY", font(SANS_B, 13), fill=RED)
text(d, (996, y), "MONDAY'S NEWS  ·  ONE PAGE  ·  35 STORIES  ·  6 CONTINENTS",
     font(SANS_B, 13), anchor="ra")
y = 30
hline(d, y, width=2)

# ---------- masthead ----------
y = 36
centre(d, y, "Monday 23 November 2026", font(SERIF_B, 50))
y = 90
centre(d, y, "COP31 collapses  ·  a Kyiv block falls  ·  a Russian warship sinks off Libya",
       font(SERIF_I, 17), fill=(60, 58, 52))
y = 112
hline(d, y, width=2)

# ---------- key numbers strip ----------
NUMS = [
    ("14", "MISSING IN DYMER", "Zelenskiy"),
    ("24", "BODY BAGS, CIKANDE FIRE", "Monday toll"),
    ("258", "DEMOCRAT HOUSE SEATS", "biggest since 1992"),
    ("$120bn", "ADAPTATION TARGET CUT", "from COP31 text"),
    ("0.639s", "VERSTAPPEN'S VEGAS MARGIN", "over Norris"),
    ("6", "INJURED IN HOUTHI STRIKES", "Saudi refinery, radar"),
]
y0 = 120
cell = (996 - 28) // 6
for i, (num, lab, sub) in enumerate(NUMS):
    cx = 28 + i * cell + cell // 2
    d.text((cx, y0), num, font=font(SERIF_B, 27), fill=RED, anchor="ma")
    d.text((cx, y0 + 30), lab, font=font(SANS_B, 9), fill=INK, anchor="ma")
    d.text((cx, y0 + 41), sub, font=font(SANS, 9), fill=GREY, anchor="ma")
    if i:
        d.line([(28 + i * cell, y0 + 4), (28 + i * cell, y0 + 50)], fill=RULE, width=1)
y = y0 + 52
hline(d, y)

# ---------- region counts ----------
y += 5
centre(d, y, "EUROPE 6   ·   AMERICAS 3   ·   ASIA-PACIFIC 1   ·   MIDEAST 1   ·   AFRICA 1   ·   OCEANIA 1   ·   13 DRAWN STORIES",
       font(SANS_B, 12))
y += 16
hline(d, y, width=2)

# ---------- lead cards ----------
LEADS = [
    ("01", "ANTALYA, TURKEY  ·  CLIMATE", "COP31 collapses as the EU rejects a fossil-free pact",
     "After the longest COP ever, the EU and UK refuse a deal with no mention of fossil fuels. (CNN)",
     "globe"),
    ("02", "DYMER, UKRAINE  ·  WAR", "Drone flattens a tower block; 14 people missing",
     "A Russian drone collapses a five-storey block in Dymer; 14 unaccounted for, two dead. (Reuters)",
     "skyline"),
    ("03", "BENGHAZI, LIBYA  ·  WAR AT SEA", "Sea drones sink a Russian warship off Libya",
     "Suspected Ukrainian sea drones hit the corvette Merkury; it capsizes, 10 hurt. (AP)",
     "ship"),
]
y += 6
lead_y = y
lead_w, lead_h, gap = 312, 156, 12
for i, (num, tag, head, summ, art) in enumerate(LEADS):
    x = 28 + i * (lead_w + gap)
    d.rectangle([x, lead_y, x + lead_w, lead_y + lead_h], outline=INK, width=1)
    # illustration band
    d.rectangle([x + 1, lead_y + 1, x + lead_w - 1, lead_y + 62], fill=SKY)
    if art == "globe":
        cx, cy = x + 52, lead_y + 32
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(70, 130, 90), outline=INK, width=2)
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(255, 255, 255), width=1)
        d.line([(cx - 24, cy), (cx + 24, cy)], fill=(255, 255, 255), width=1)
        d.ellipse([cx - 9, cy - 24, cx + 9, cy + 24], outline=(255, 255, 255), width=1)
        # thermometer
        tx = x + 110
        d.rectangle([tx, lead_y + 12, tx + 12, lead_y + 48], outline=INK, width=2, fill=(255, 255, 255))
        d.rectangle([tx + 2, lead_y + 30, tx + 10, lead_y + 46], fill=RED)
        d.ellipse([tx - 3, lead_y + 44, tx + 15, lead_y + 60], fill=RED, outline=INK, width=1)
        d.text((x + 150, lead_y + 16), "NO", font=font(SERIF_B, 22), fill=RED)
        d.text((x + 150, lead_y + 38), "DEAL", font=font(SERIF_B, 22), fill=RED)
    elif art == "skyline":
        base = lead_y + 62
        d.rectangle([x + 1, lead_y + 1, x + lead_w - 1, base], fill=(30, 44, 66))
        for bx, bw, bh in [(x + 14, 46, 34), (x + 66, 40, 44), (x + 112, 52, 26),
                           (x + 170, 44, 40), (x + 220, 48, 32), (x + 272, 30, 22)]:
            d.rectangle([bx, base - bh, bx + bw, base], fill=(70, 84, 104), outline=INK, width=1)
            for wy in range(base - bh + 5, base - 4, 8):
                for wx in range(bx + 5, bx + bw - 4, 10):
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 214, 90))
        # collapsed block (tilted rubble)
        d.polygon([(x + 112, base), (x + 130, base - 26), (x + 164, base - 8), (x + 164, base)],
                  fill=(150, 60, 50), outline=INK)
        # drone trail
        pts = [(x + 20, lead_y + 14), (x + 90, lead_y + 8), (x + 160, lead_y + 16), (x + 230, lead_y + 10)]
        d.line(pts, fill=(255, 255, 255), width=2)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=(255, 255, 255))
    else:  # ship
        base = lead_y + 62
        d.rectangle([x + 1, lead_y + 1, x + lead_w - 1, base], fill=(24, 58, 86))
        d.rectangle([x + 1, base - 14, x + lead_w - 1, base], fill=(40, 110, 150))
        for wx in range(x + 8, x + lead_w - 8, 22):
            d.arc([wx, base - 12, wx + 16, base - 2], 0, 180, fill=(255, 255, 255), width=1)
        # capsized warship
        d.polygon([(x + 90, base - 16), (x + 210, base - 16), (x + 225, base - 26), (x + 105, base - 26)],
                  fill=(60, 60, 64), outline=INK)
        d.rectangle([x + 150, base - 40, x + 158, base - 26], fill=(60, 60, 64), outline=INK)
        d.line([(x + 154, base - 52), (x + 154, base - 40)], fill=INK, width=2)
        # explosion
        ex, ey = x + 240, lead_y + 20
        for dx, dy in [(0, -12), (9, -9), (12, 0), (9, 9), (0, 12), (-9, 9), (-12, 0), (-9, -9)]:
            d.line([(ex, ey), (ex + dx, ey + dy)], fill=(255, 180, 40), width=3)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 220, 90), outline=RED, width=1)
        # drone boat
        d.ellipse([x + 30, base - 22, x + 62, base - 14], fill=(200, 40, 40), outline=INK)
    # text
    ty = lead_y + 66
    d.text((x + 10, ty), num, font=font(SERIF_B, 15), fill=RED)
    d.text((x + 38, ty + 2), tag, font=font(SANS_B, 10), fill=GREY)
    ty += 18
    for ln in wrap(d, head, font(SERIF_B, 16), lead_w - 20):
        d.text((x + 10, ty), ln, font=font(SERIF_B, 16), fill=INK)
        ty += 19
    ty += 1
    for ln in wrap(d, summ, font(SANS, 11), lead_w - 20):
        d.text((x + 10, ty), ln, font=font(SANS, 11), fill=(40, 38, 34))
        ty += 13
y = lead_y + lead_h + 8
hline(d, y)

# ---------- feature cards ----------
FEATS = [
    ("04", "CIKANDE, INDONESIA", "Factory fire: 24 body bags, dozens missing",
     "Candy factory fire; 300 inside. Toll 24 on Monday. (Reuters)", "flame"),
    ("05", "LAS VEGAS, USA", "Verstappen wins Vegas thriller",
     "Beats Norris by 0.639s; 35 lead changes. His 75th win. (F1)", "flag"),
    ("06", "LIVERPOOL, ENGLAND", "Liverpool 4-0 United in Pochettino debut",
     "Yoro off in the 8th minute; United 19th after 11 games. (Reuters)", "ball"),
    ("07", "ZURICH, SWITZERLAND", "UK to host 2035 Women's World Cup",
     "FIFA ratifies sole UK bid Monday: 48 teams, 104 games. (BBC)", "trophy"),
    ("08", "TURIN, ITALY", "Alcaraz wins first ATP Finals title",
     "Beats world No. 1 Zverev 6-2, 7-6(7) in Turin. (Reuters)", "tennis"),
    ("09", "WELLINGTON, NZ", "India close in on day five in Wellington",
     "NZ 157-4 at lunch, 206-5 at tea; India need five. (Reuters)", "cricket"),
    ("10", "SEATTLE, USA", "ICE seizes father, daughter on jet bridge",
     "Pair flew to a family baptism; protests at airport. (AP)", "plane"),
    ("11", "RABIGH, SAUDI ARABIA", "Houthis claim refinery strike",
     "Group claims a direct hit on Rabigh; Saudis silent. (Reuters)", "oil"),
    ("12", "NAPLES, USA", "Thitikul's third straight $4m win",
     "Beats Iwai by two; passes Sorenstam as money leader. (AP)", "golf"),
    ("13", "WOLVERHAMPTON, ENGLAND", "Price ends four-year major wait",
     "Beats van Veen 16-11 in the Grand Slam final. (PDC)", "darts"),
]
fw, fh, fgap = 190, 118, 4
fy0 = y + 5
for row in range(2):
    for col in range(5):
        i = row * 5 + col
        num, tag, head, summ, art = FEATS[i]
        x = 28 + col * (fw + fgap)
        yy = fy0 + row * (fh + 6)
        d.rectangle([x, yy, x + fw, yy + fh], outline=INK, width=1)
        # mini illustration
        ix, iy = x + 6, yy + 6
        d.rectangle([x + 1, yy + 1, x + fw - 1, yy + 34], fill=SKY)
        if art == "flame":
            d.polygon([(ix + 14, iy + 26), (ix + 6, iy + 12), (ix + 12, iy + 8), (ix + 16, iy + 2),
                       (ix + 22, iy + 10), (ix + 28, iy + 14), (ix + 24, iy + 26)],
                      fill=(230, 90, 30), outline=INK)
            d.ellipse([ix + 11, iy + 16, ix + 21, iy + 26], fill=(255, 200, 40))
        elif art == "flag":
            d.line([(ix + 8, iy + 2), (ix + 8, iy + 28)], fill=INK, width=2)
            for r in range(2):
                for c in range(4):
                    if (r + c) % 2 == 0:
                        d.rectangle([ix + 10 + c * 5, iy + 3 + r * 6, ix + 14 + c * 5, iy + 8 + r * 6],
                                    fill=INK)
        elif art == "ball":
            d.ellipse([ix + 6, iy + 4, ix + 30, iy + 28], outline=INK, width=2, fill=(255, 255, 255))
            d.polygon([(ix + 18, iy + 10), (ix + 24, iy + 15), (ix + 21, iy + 22), (ix + 15, iy + 22),
                       (ix + 12, iy + 15)], fill=INK)
        elif art == "trophy":
            d.polygon([(ix + 8, iy + 4), (ix + 28, iy + 4), (ix + 25, iy + 18), (ix + 11, iy + 18)],
                      fill=(220, 170, 40), outline=INK)
            d.line([(ix + 18, iy + 18), (ix + 18, iy + 24)], fill=INK, width=2)
            d.rectangle([ix + 12, iy + 24, ix + 24, iy + 28], fill=(220, 170, 40), outline=INK)
        elif art == "tennis":
            d.ellipse([ix + 6, iy + 4, ix + 30, iy + 28], fill=(190, 220, 60), outline=INK, width=2)
            d.arc([ix + 8, iy + 4, ix + 20, iy + 28], 270, 90, fill=(255, 255, 255), width=2)
            d.arc([ix + 16, iy + 4, ix + 28, iy + 28], 90, 270, fill=(255, 255, 255), width=2)
        elif art == "cricket":
            d.line([(ix + 8, iy + 26), (ix + 26, iy + 8)], fill=(150, 100, 40), width=5)
            d.ellipse([ix + 24, iy + 4, ix + 32, iy + 12], fill=RED, outline=INK)
        elif art == "plane":
            d.polygon([(ix + 4, iy + 16), (ix + 30, iy + 12), (ix + 30, iy + 18), (ix + 4, iy + 20)],
                      fill=(60, 90, 130), outline=INK)
            d.polygon([(ix + 14, iy + 6), (ix + 20, iy + 6), (ix + 18, iy + 14)], fill=(60, 90, 130), outline=INK)
        elif art == "oil":
            d.line([(ix + 10, iy + 28), (ix + 10, iy + 8)], fill=INK, width=3)
            d.line([(ix + 10, iy + 8), (ix + 24, iy + 20)], fill=INK, width=3)
            d.line([(ix + 24, iy + 20), (ix + 24, iy + 28)], fill=INK, width=3)
            d.ellipse([ix + 26, iy + 14, ix + 32, iy + 22], fill=(230, 90, 30))
        elif art == "golf":
            d.line([(ix + 14, iy + 4), (ix + 14, iy + 28)], fill=INK, width=2)
            d.polygon([(ix + 14, iy + 4), (ix + 30, iy + 9), (ix + 14, iy + 14)], fill=RED, outline=INK)
            d.ellipse([ix + 8, iy + 26, ix + 14, iy + 30], fill=(255, 255, 255), outline=INK)
        else:  # darts
            d.ellipse([ix + 6, iy + 4, ix + 30, iy + 28], fill=(40, 40, 40), outline=INK, width=2)
            d.ellipse([ix + 11, iy + 9, ix + 25, iy + 23], fill=(240, 240, 240), outline=INK)
            d.ellipse([ix + 15, iy + 13, ix + 21, iy + 19], fill=RED)
        d.text((x + 40, yy + 8), num, font=font(SERIF_B, 20), fill=RED)
        ty = yy + 38
        d.text((x + 6, ty), tag, font=font(SANS_B, 8), fill=GREY)
        ty += 11
        for ln in wrap(d, head, font(SERIF_B, 12), fw - 12):
            d.text((x + 6, ty), ln, font=font(SERIF_B, 12), fill=INK)
            ty += 14
        for ln in wrap(d, summ, font(SANS, 10), fw - 12):
            d.text((x + 6, ty), ln, font=font(SANS, 10), fill=(40, 38, 34))
            ty += 12
y = fy0 + 2 * fh + 6 + 4
hline(d, y)

# ---------- world map ----------
y += 4
d.text((28, y), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
d.text((996, y), "Pins 1-13 match the numbered stories above", font=font(SANS, 10), fill=GREY, anchor="ra")
map_y = y + 14
map_x, map_w, map_h = 28, 968, 140
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA, outline=INK, width=1)


def proj(lon, lat):
    # equirectangular, latitude stretched x2.2 so continents read at this band height
    return (map_x + (lon + 180) / 360 * map_w,
            map_y + (84 - lat) / 142 * map_h)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-95, 80), (-80, 73), (-75, 62), (-55, 52), (-60, 45),
     (-75, 35), (-80, 25), (-90, 20), (-105, 20), (-115, 30), (-125, 40), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 10), (-50, 0), (-35, -8), (-40, -20), (-50, -30), (-60, -40), (-70, -55),
     (-75, -40), (-80, -20), (-80, 0)],
    [(-10, 36), (0, 44), (-2, 48), (5, 58), (10, 58), (18, 56), (28, 60), (30, 70), (40, 68),
     (45, 60), (35, 50), (28, 45), (20, 40), (10, 38), (0, 36), (-10, 37)],
    [(-17, 15), (-10, 30), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11), (40, -5),
     (35, -20), (20, -35), (12, -18), (9, 0), (9, 4), (-8, 5), (-17, 15)],
    [(40, 70), (60, 70), (70, 72), (90, 75), (110, 76), (130, 72), (160, 70), (180, 66), (162, 60),
     (158, 52), (142, 45), (140, 40), (130, 35), (122, 30), (120, 22), (108, 10), (105, 2), (100, 8),
     (95, 15), (90, 22), (80, 8), (77, 8), (72, 20), (66, 25), (60, 25), (55, 26), (50, 29),
     (48, 30), (44, 29), (40, 32), (38, 36), (35, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35), (140, -38), (147, -39),
     (150, -37), (153, -27), (153, -22), (146, -19), (142, -11), (136, -12), (132, -12), (126, -14),
     (122, -17), (113, -22)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=(120, 110, 88))

PINS = [
    (1, 30.7, 36.9, 0, 0), (2, 30.3, 50.8, 0, -10), (3, 20.1, 32.1, 0, 0),
    (4, 106.3, -6.3, 0, 0), (5, -115.1, 36.2, 0, 0), (6, -3.0, 53.4, -12, -2),
    (7, -0.1, 51.5, 12, -8), (8, 7.7, 45.1, 2, 10), (9, 174.8, -41.3, 0, 0),
    (10, -122.3, 47.6, 0, 0), (11, 39.0, 22.8, 0, 0), (12, -81.8, 26.1, 0, 0),
    (13, -2.1, 52.6, 14, 8),
]
for n, lon, lat, dx, dy in PINS:
    px, py = proj(lon, lat)
    px += dx
    py += dy
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py), str(n), font=font(SANS_B, 9), fill=(255, 255, 255), anchor="mm")
y = map_y + map_h + 6
hline(d, y)

# ---------- also on Monday ----------
ALSO = [
    "14  Democrats reach 258 House seats - biggest majority since 1992. (Reuters)",
    "15  Trump reposts a Democrat's gold 'TrumpCare' card - with no comment. (Fox)",
    "16  Israel coalition talks end with no deal; Eisenkot has until 6 Dec. (Al Jazeera)",
    "17  Modi meets Nepal PM Shah in Delhi; joint vision document expected. (PTI)",
    "18  Russian cargo ship Sparta II towed out of Finnish waters, still smouldering. (Reuters)",
    "19  Camara stays at Haas for final two races, giving up F2 title shot. (Reuters)",
    "20  M4.0 quake shakes Chitral, Pakistan, at 02:19 on Monday. (VolcanoDiscovery)",
    "21  Strong El Nino may bring heavy snow, floods to the Himalayas. (PTI)",
    "22  Book claims William will strip Harry and Meghan of titles as king. (Page Six)",
    "23  US spy chief confirms probe into Nvidia chip flows to China. (Bloomberg)",
    "24  India, China end 10-day border talks in Arunachal before winter. (Indian Express)",
    "25  Chess: Sindarov draws white for Game 1 vs Gukesh on Tuesday. (Chess.com)",
    "26  Atalanta earn dramatic late draw with Inter in Serie A. (AFP)",
    "27  COP31's $120bn adaptation-finance target was cut from the text. (Business Day)",
    "28  Finland still probes Russian helicopter incursion off Loviisa. (Reuters)",
    "29  Zverev ends the year as world No. 1 despite losing the final. (The Times)",
    "30  Houthis also claim a strike on a Saudi radar site. (ISW)",
    "31  Four US House races still uncalled; Louisiana run-offs on 12 Dec. (Reuters)",
    "32  Seattle airport protests after ICE video; mayor calls tactics 'un-American'. (Guardian)",
    "33  Wider Russian assault hit 18 sites in Ukraine overnight; 30 hurt. (IBT)",
    "34  Nvidia chief Jensen Huang to face Congress on 1 Dec. (Bloomberg)",
    "35  US Army to detonate toxic lead azide in Iowa by Tuesday, defying court pause. (Reuters)",
]
y += 4
d.text((28, y), "ALSO ON MONDAY 23 NOVEMBER  —  22 MORE STORIES", font=font(SANS_B, 12), fill=RED)
ay = y + 14
col_w = 478
for i, line in enumerate(ALSO):
    col = i // 11
    row = i % 11
    lx = 28 + col * (col_w + 12)
    ly = ay + row * 11
    d.text((lx, ly), line, font=font(SANS, 10), fill=INK)
y = ay + 11 * 11 + 4
hline(d, y)

# ---------- date check ----------
y += 4
d.text((28, y), "DATE CHECK  —  NOT SHOWN, BECAUSE THEY ARE NOT 23 NOVEMBER",
       font=font(SANS_B, 11), fill=RED)
dy = y + 15
CHECKS = [
    "Lisbon march - Sat 21 Nov (Reuters)  ·  Myanmar ASEAN rebuke - Sat 21 Nov (Reuters)  ·  Pant's 128 - Sun 22 Nov (AP)",
    "Amazon man found - 20 Nov (AFP)  ·  FIDE Game 1 - Tue 24 Nov (FIDE)  ·  Verstappen on pole - Fri qualifying (F1)",
]
for ln in CHECKS:
    d.text((28, dy), ln, font=font(SANS, 10), fill=GREY)
    dy += 12
y = dy + 2
hline(d, y)

# ---------- footer ----------
y += 5
for ln in wrap(d, "Every story here happened, or was first reported, on Monday 23 November 2026 in at least one "
                  "time zone. Claims are attributed, not stated as fact. "
                  "Sources: Reuters, AP, AFP, BBC, CNN, F1, ATP, PDC, Chess.com, PTI. Original vector drawings.",
               font(SANS, 10), 968):
    d.text((28, y), ln, font=font(SANS, 10), fill=GREY)
    y += 12
d.text((28, y + 2), "THE WORLD IN ONE DAY  ·  MONDAY 23 NOVEMBER 2026",
       font=font(SANS_B, 9), fill=GREY)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes; footer ends at y =", y + 14)
