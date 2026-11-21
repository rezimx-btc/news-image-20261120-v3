"""THE WORLD TODAY - Friday, 20 November 2026. Front-page newspaper, 1024x1024.

Pure Python 3.13 standard library only (os, struct, zlib). No network, no
fonts, no image libraries: text is drawn with an embedded 5x7 bitmap font
and the PNG is encoded by hand. Deterministic: identical bytes every run.
Output goes ONLY to os.environ["MAKEFUN_OUTPUT_DIR"] + "/entry.png".
"""

import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (250, 247, 238)
INK = (12, 12, 12)
RED = (178, 34, 34)
BLUE = (18, 52, 120)
GREY = (110, 110, 108)
LIGHT = (232, 228, 218)
SEA = (168, 196, 214)
LAND = (214, 196, 150)
LAND2 = (198, 210, 170)
GOLD = (176, 132, 30)

# ------------------------------------------------------- 5x7 bitmap font
# Each glyph: 7 rows of 5 bits, "1" = ink. Uppercase only; text is uppercased.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}

# ---------------------------------------------------------------- canvas
PIX = bytearray(W * H * 3)


def _set(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        PIX[i] = color[0]
        PIX[i + 1] = color[1]
        PIX[i + 2] = color[2]


def fill_rect(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            PIX[i] = color[0]
            PIX[i + 1] = color[1]
            PIX[i + 2] = color[2]


def rect(x, y, w, h, color, t=1):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def hline(x, y, w, color, t=1):
    fill_rect(x, y, w, t, color)


def vline(x, y, h, color, t=1):
    fill_rect(x, y, t, h, color)


def line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        _set(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def fill_circle(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                _set(xx, yy, color)


def circle(cx, cy, r, color):
    for a in range(360):
        import math
        x = cx + int(r * math.cos(a * 3.14159265 / 180.0))
        y = cy + int(r * math.sin(a * 3.14159265 / 180.0))
        _set(x, y, color)


def fill_poly(points, color):
    # Scanline fill for a simple polygon.
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(points)
        for k in range(n):
            x0, y0 = points[k]
            x1, y1 = points[(k + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                _set(x, y, color)


# ------------------------------------------------------------------- text
def text_w(s, scale=1):
    return len(s) * 6 * scale


def draw_text(x, y, s, scale=1, color=INK, bold=False):
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch)
        if g is None:
            cx += 6 * scale
            continue
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "1":
                    fill_rect(cx + col * scale, y + row * scale,
                              scale, scale, color)
                    if bold:
                        fill_rect(cx + col * scale + 1, y + row * scale,
                                  scale, scale, color)
        cx += 6 * scale
    return cx


def draw_centered(y, s, scale=1, color=INK, bold=False):
    draw_text((W - text_w(s, scale)) // 2, y, s, scale, color, bold)


def wrap(s, max_chars):
    words = s.split(" ")
    lines = []
    cur = ""
    for wd in words:
        if cur == "":
            cur = wd
        elif len(cur) + 1 + len(wd) <= max_chars:
            cur = cur + " " + wd
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# -------------------------------------------------------------- PNG write
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def save_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(PIX[y * W * 3:(y + 1) * W * 3])
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

# ------------------------------------------------------------- the stories
# (region, headline, body) - every figure attributed to its source.
STORIES = [
    # EUROPE
    ("EUROPE", "KYIV BRIDGES HIT IN MASS BARRAGE",
     "Russia fired 100+ missiles and 400 drones overnight, Kyiv mayor says; 3 killed, 15 hurt; 3 Dnipro bridges closed. (Kyiv Post)"),
    ("EUROPE", "POLAND: MISSILES CROSS BORDER",
     "2 cruise missiles and 1 drone fell in SE Poland at 03:30; no injuries; NATO jets scrambled. (Polish Defence Ministry)"),
    ("EUROPE", "UK-EU RESET DEAL SEALED",
     "Food checks scrapped from Mar 2028; carbon markets linked Jan 2028; youth mobility up to 100,000 a year. (Reuters)"),
    ("EUROPE", "EU-UK SUMMIT: AI PARTNERSHIP",
     "Leaders in Brussels pledge a Digital Partnership in early 2027 covering AI safety, quantum and connectivity. (Joint statement)"),
    ("EUROPE", "COST-OF-LIVING STRIKES SPREAD",
     "Young people in 25+ countries join a general strike over housing costs and military spending. (Global Map News)"),
    ("EUROPE", "NATIONS LEAGUE DRAW MADE",
     "Spain face France, England meet Norway in quarter-finals; first legs due late Mar 2027. (UEFA)"),
    ("EUROPE", "KANE OUT FOR MONTHS",
     "Bayern lose Harry Kane to an ankle syndesmosis tear in a 1-1 draw with Cologne; Olise also hurt. (Pollar)"),
    # ASIA-PACIFIC
    ("ASIA-PACIFIC", "CYCLONE AKVAN HITS ODISHA",
     "Landfall near Gopalpur with winds over 90 km/h; 300,000+ evacuated, 28 trains cancelled. (Odisha govt)"),
    ("ASIA-PACIFIC", "NIKKEI SINKS 5% IN AI ROUT",
     "Tokyo -5.1%, Seoul Kospi -5.5%, Taipei Taiex -6.2%; SoftBank -14.5%, Samsung -7%. (Reuters)"),
    ("ASIA-PACIFIC", "ICJ: MYANMAR COMMITTED GENOCIDE",
     "Court rules 9-6, first state genocide verdict; 10,000 Rohingya killed in 2017, 400 villages razed. (ICJ)"),
    ("ASIA-PACIFIC", "XI MEETS ALBANESE IN SHENZHEN",
     "China and Australia leaders meet at APEC; Albanese tells Putin to stop the war 'now'. (China MFA)"),
    ("ASIA-PACIFIC", "JAKARTA MINIMUM WAGE UP 7.1%",
     "2027 wage set at Rp 6.136 million, up 7.1%, the Jakarta government announces. (Jakarta govt)"),
    ("ASIA-PACIFIC", "BARTY INTO HALL OF FAME",
     "Ash Barty, 3-time Grand Slam champion, elected to the International Tennis Hall of Fame, Class of 2027. (AP)"),
    ("ASIA-PACIFIC", "NZ 243/5 AFTER NICHOLLS TON",
     "Henry Nicholls 113 not out, Glenn Phillips 94; NZ recover from 70/5 v India in Wellington. (Jagran Josh)"),
    # MIDDLE EAST
    ("MIDDLE EAST", "HOUTHIS HIT RIYADH TOWER",
     "Missiles strike the PIF Tower in Riyadh; Saudi-led coalition intercepts 1 missile and 3 drones. (BriefWire)"),
    ("MIDDLE EAST", "TANKERS BURN IN HORMUZ",
     "Iran's Revolutionary Guards say 2 tankers are burning in the Strait of Hormuz; 14 tankers mass at Kharg. (BriefWire)"),
    ("MIDDLE EAST", "SAUDI STRIKES POUND YEMEN",
     "Saudi-led strikes hit Hodeidah, Sanaa, Saada and Taiz; unverified claims of 41 dead, 11 children. (Daily Brief)"),
    ("MIDDLE EAST", "IRAQ MOVES ON JURF AL-SAKHAR",
     "Security forces enter the Kataib Hezbollah stronghold south of Baghdad after a 2-hour delay under a deal. (Global Map News)"),
    ("MIDDLE EAST", "TRUMP DEFERS IRAN STRIKE CALL",
     "Trump defers strike decisions on Iran until after the New Year as 14 tankers mass at Kharg Island. (Daily Brief)"),
    # NORTH AMERICA
    ("NORTH AMERICA", "WALL ST IN CORRECTION",
     "S and P 500 -3.7%, 7th straight loss, 10% below its record; Nasdaq -5.3%, wiping out 2026 gains. (RelaxNews)"),
    ("NORTH AMERICA", "NVIDIA DIVES 14%",
     "Nvidia -14% as the SEC examines accounting; Anthropic -9% to $88.30; AMD -13%. (RelaxNews)"),
    ("NORTH AMERICA", "TRUMP: TAX ON OVERSEAS DATA CENTRES",
     "US firms building AI data centres abroad face a 'tremendous tax', Trump warns; not yet policy. (Daily Brief)"),
    ("NORTH AMERICA", "SENATE BLOCKS IRAN WAR LIMITS",
     "Senate votes 51-48 to block a War Powers resolution limiting Trump's Iran war powers; decision pushed to Jan 2027. (1-min Brief)"),
    ("NORTH AMERICA", "CALIFORNIA QUAKE M5.0",
     "Magnitude 5.0 quake near Pinnacles National Park, strongest in a swarm felt Salinas to San Jose; no injuries. (BriefWire)"),
    ("NORTH AMERICA", "GTA 6 SALES TOP $2.3BN",
     "GTA 6 drives a download spike; estimated sales top $2.3bn, reports say. (Budget Report)"),
    # LATIN AMERICA
    ("LATIN AMERICA", "COLOMBIA TEEN WINS PEACE PRIZE",
     "Francisco Javier Vera Manzanares, 17, receives the International Children's Peace Prize. (Archynewsy)"),
    ("LATIN AMERICA", "ARGENTINA THRASH COSTA RICA 7-0",
     "Nico Paz scores twice in a friendly rout in Buenos Aires. (One Turn)"),
    ("LATIN AMERICA", "SPORTING LIFT FUTSAL CUP",
     "Sporting beat Palma 5-4 in Pato Branco, Brazil, to win the Intercontinental Cup. (Sport TV)"),
    ("LATIN AMERICA", "HAITI: FRAUD IN INDICTMENT",
     "Pandemic relief fraud runs through the indictment in the assassination of Haiti's president. (Today News Africa)"),
    # AFRICA
    ("AFRICA", "S AFRICA MOURNS MLAMBO-NGCUKA",
     "Ex-deputy president Phumzile Mlambo-Ngcuka dies at 71; the first woman in the post. (SA Presidency)"),
    ("AFRICA", "EGYPT IMF DEAL: $2.3BN",
     "Egypt and the IMF agree the final review of the $8bn programme; $2.3bn rides on a board vote before 15 Dec. (Today News Africa)"),
    ("AFRICA", "NIGERIA BOAT TOLL: 4 DEAD",
     "4 dead, 24 rescued in a Bayelsa boat accident, police say. (Punch)"),
    ("AFRICA", "LITTON DAS SETS TEST RECORD",
     "8 dismissals in one innings v South Africa in Johannesburg: 6 catches, 2 stumpings. (One Turn)"),
    # OCEANIA AND SPORT
    ("OCEANIA + SPORT", "ALCARAZ STAYS UNBEATEN",
     "Alcaraz beats Cobolli 6-4, 6-1 at the ATP Finals in Turin; faces Shelton in the semis. (One Turn)"),
    ("OCEANIA + SPORT", "A LIM KIM ACES 16TH",
     "Hole-in-one at the CME Group Tour Championship in Florida; leads by 3 after round 2. (One Turn)"),
    ("OCEANIA + SPORT", "WALLABIES FACE WALES",
     "Australia captain Harry Wilson confident before the Cardiff clash; Wales made 325 tackles v NZ. (RugbyPass)"),
    ("OCEANIA + SPORT", "PRICE UNDISPUTED CHAMPION",
     "Lauren Price beats Michaela Kotaskova to take the undisputed welterweight title in Wales. (One Turn)"),
    ("OCEANIA + SPORT", "MEDVEDEV INTO TURIN SEMIS",
     "Medvedev beats Tiafoe 6-3, 6-4, and faces Zverev on Sat 21 Nov at 20:30 local. (Pollar)"),
]

# Column plan: (region, count) per column, in story order.
COLUMNS = [
    ["EUROPE", "AFRICA"],
    ["ASIA-PACIFIC", "MIDDLE EAST"],
    ["NORTH AMERICA", "LATIN AMERICA", "OCEANIA + SPORT"],
]

# -------------------------------------------------------------- world map
# Rough continent outlines as (lon, lat) points; projected into map box.
CONTINENTS = [
    ("NA", [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
            (-80, 73), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
            (-80, 32), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
            (-125, 40), (-125, 48), (-140, 60), (-165, 60)], LAND),
    ("SA", [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-40, -5), (-35, -10),
            (-40, -20), (-48, -28), (-58, -35), (-65, -45), (-70, -55),
            (-75, -40), (-75, -20), (-80, -5)], LAND2),
    ("EU", [(-10, 36), (-9, 43), (0, 44), (-2, 49), (5, 53), (8, 57), (10, 59),
            (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 55),
            (35, 50), (30, 45), (23, 40), (19, 42), (12, 44), (8, 44), (3, 42),
            (-2, 37)], LAND),
    ("AF", [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
            (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -28),
            (25, -34), (18, -35), (15, -25), (12, -10), (9, 4), (-8, 5),
            (-15, 10)], LAND2),
    ("AS", [(40, 68), (60, 70), (80, 73), (100, 76), (120, 73), (140, 72),
            (160, 70), (178, 66), (170, 60), (162, 55), (158, 50), (142, 45),
            (140, 40), (130, 35), (127, 35), (122, 30), (120, 25), (110, 20),
            (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15),
            (75, 10), (72, 20), (66, 25), (60, 25), (55, 26), (50, 29),
            (48, 30), (45, 35), (42, 40), (40, 45), (38, 50)], LAND),
    ("OC", [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (137, -35),
            (140, -38), (147, -39), (150, -37), (153, -32), (153, -27), (150, -23),
            (146, -19), (142, -15), (142, -11), (136, -12), (132, -12), (126, -14),
            (122, -17), (118, -20)], LAND2),
]

# (number, lon, lat, label, label_dx, label_dy) - key stories on the map.
MARKERS = [
    (1, 30.5, 50.5, "KYIV", 10, 8), (2, 19.0, 52.0, "POLAND", -52, -12),
    (3, -0.1, 51.5, "LONDON", -52, 8), (4, 85.0, 19.8, "GOPALPUR", 10, -12),
    (5, 139.7, 35.7, "TOKYO", 10, 8), (6, 46.7, 24.6, "RIYADH", 10, 10),
    (7, 56.0, 26.5, "HORMUZ", 10, -12), (8, 30.7, 36.9, "ANTALYA", -58, 10),
    (9, -121.0, 36.6, "CALIFORNIA", 10, 8), (10, -74.0, 40.7, "NEW YORK", 10, -12),
    (11, 28.0, -26.2, "JOBURG", 10, 8), (12, 151.2, -33.9, "SYDNEY", -58, 8),
]

MAP_X, MAP_Y, MAP_W, MAP_H = 16, 196, 992, 158


def project(lon, lat):
    x = MAP_X + int((lon + 170.0) / 360.0 * MAP_W)
    y = MAP_Y + int((90.0 - lat) / 180.0 * MAP_H)
    return x, y


def draw_map():
    fill_rect(MAP_X, MAP_Y, MAP_W, MAP_H, SEA)
    rect(MAP_X, MAP_Y, MAP_W, MAP_H, INK, 2)
    for _name, pts, color in CONTINENTS:
        fill_poly([project(lo, la) for lo, la in pts], color)
    draw_text(MAP_X + 6, MAP_Y + 6, "THE WORLD AT A GLANCE - 12 FLASHPOINTS",
              1, BLUE, bold=True)
    for num, lon, lat, label, ldx, ldy in MARKERS:
        x, y = project(lon, lat)
        fill_circle(x, y, 8, RED)
        circle(x, y, 8, INK)
        draw_text(x - 3, y - 3, str(num), 1, (255, 255, 255), bold=True)
        draw_text(x + ldx, y + ldy, label, 1, INK, bold=True)


# ------------------------------------------------------------------ layout
def draw_story_column(x, width, regions, y_top, y_bottom):
    y = y_top
    for region in regions:
        fill_rect(x, y, width, 13, INK)
        draw_text(x + 4, y + 3, region, 1, (255, 255, 255), bold=True)
        y += 17
        for reg, title, body in STORIES:
            if reg != region:
                continue
            draw_text(x, y, title, 1, RED, bold=True)
            y += 9
            for ln in wrap(body, 52):
                draw_text(x, y, ln, 1, INK)
                y += 8
            y += 4
            hline(x, y - 2, width, LIGHT, 1)
        y += 2
    return y


def main():
    fill_rect(0, 0, W, H, PAPER)
    # Masthead
    draw_centered(14, "THE WORLD TODAY", 5, INK, bold=True)
    hline(16, 62, 992, INK, 3)
    draw_centered(70, "FRIDAY, 20 NOVEMBER 2026", 3, RED, bold=True)
    draw_centered(100, "38 STORIES  -  7 REGIONS  -  EVERY FIGURE SOURCED",
              1, INK, bold=True)
    hline(16, 122, 992, INK, 2)
    # Main headline
    draw_text(16, 132, "KYIV BRIDGES HIT AS 100+ MISSILES RAIN DOWN", 2, INK, bold=True)
    draw_text(16, 156, "THREE DNIPRO CROSSINGS CLOSED; 3 KILLED, 15 HURT - MAYOR",
              1, INK, bold=True)
    draw_text(16, 170, "CYCLONE AKVAN LANDFALL: 300,000 FLEE - AI ROUT SINKS ASIA - UK-EU DEAL SEALED - COP31 DEADLOCK",
              1, BLUE, bold=True)
    hline(16, 188, 992, INK, 2)
    # Map
    draw_map()
    # Columns
    col_x = [16, 350, 684]
    col_w = 324
    for cx, regions in zip(col_x, COLUMNS):
        draw_story_column(cx, col_w, regions, 366, 922)
    hline(16, 928, 992, INK, 2)
    # Market ticker
    fill_rect(16, 936, 992, 22, INK)
    draw_text(22, 942,
              "NIKKEI -5.1%  |  KOSPI -5.5%  |  TAIEX -6.2%  |  S+P 500 -3.7%  |  "
              "NASDAQ -5.3%  |  NVIDIA -14%  |  ANTHROPIC -9%  |  SOFTBANK -14.5%",
              1, (255, 255, 255), bold=True)
    # Footer: sources
    draw_text(16, 968,
              "SOURCES: REUTERS, KYIV POST, AP, ICJ, COP31 PRESIDENCY, POLISH DEFENCE MINISTRY,",
              1, GREY)
    draw_text(16, 980,
              "ODISHA GOVT, BRIEFWIRE, GLOBAL MAP NEWS, RELAXNEWS, POLLAR, ONE TURN, TODAY NEWS AFRICA, PUNCH, SPORT TV.",
              1, GREY)
    draw_text(16, 992,
              "ALL FIGURES ATTRIBUTED IN TEXT. DRAWN FRIDAY 20 NOVEMBER 2026. 38 STORIES, 7 REGIONS.",
              1, GREY, bold=True)
    out = os.path.join(os.environ["MAKEFUN_OUTPUT_DIR"], "entry.png")
    save_png(out)


if __name__ == "__main__":
    main()
