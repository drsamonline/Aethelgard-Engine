#!/usr/bin/env python3
"""
Builds Instagram-ready posters from the game's character art.

    python3 tools/make-instagram-posters.py

Reads the high-resolution cut-outs in mods/poster-hi/sprites/ and the region
backdrops in mods/ai-art/sprites/, and writes 1080x1350 (4:5) posters to
posters/. Text is deliberately minimal — a name, a role, and a wordmark.

Regenerate the high-res cut-outs first if they are missing:

    python3 tools/import-ai-art.py <folder-of-originals> \
        --pack-id poster-hi --name hi --size 1024
"""
import pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
ART = ROOT / "mods" / "ai-art" / "sprites"
HI = ROOT / "mods" / "poster-hi" / "sprites"
OUT = ROOT / "posters"
OUT.mkdir(exist_ok=True)

W, H = 1080, 1350
GOLD = (224, 179, 77)
PALE = (238, 233, 245)
MUTED = (168, 160, 186)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
]


def font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = pathlib.Path(d) / n
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), size)
                except Exception:
                    pass
    return ImageFont.load_default()


def F_DISPLAY(sz):   # big names
    return font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf", "DejaVuSans-Bold.ttf"], sz)


def F_UI(sz):        # small labels
    return font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"], sz)


def F_UI_B(sz):
    return font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"], sz)


def spaced(draw, cx, y, text, fnt, fill, tracking=8, anchor="mm"):
    """Draw text with letter-spacing, centred on cx."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="lm")
        x += w + tracking


# ---------------------------------------------------------------- poster list
# name, role line, sprite key, backdrop
POSTERS = [
    ("Warrior",     "The Bulwark of Oakhaven", "class.warrior",     "bg.banditcamp"),
    ("Berserker",   "Fury Given Form",         "class.berserker",   "bg.mountains"),
    ("Mage",        "Keeper of the Arcane",    "class.mage",        "bg.temple"),
    ("Archer",      "Eyes of the Woodland",    "class.archer",      "bg.mire"),
    ("Thief",       "Shadow Between Torches",  "class.thief",       "bg.ruins"),
    ("Defender",    "The Line That Holds",     "class.defender",    "bg.oakhaven"),
    ("Swordmaster", "One Blade, One Cut",      "class.swordmaster", "bg.temple"),
    ("Duelist",     "Steel at Full Speed",     "class.duelist",     "bg.oakhaven"),
    ("Coven Leader",     "The Dark Comes Calling", "enemy.coven",        "bg.depths"),
    ("Iron Warden",      "Guardian of the Deep",   "enemy.warden",       "bg.cave"),
    ("Bandit Warlord",   "Master of the Badlands", "enemy.warlord",      "bg.banditcamp"),
    ("Spider Queen",     "Weaver of the Dark",     "enemy.spider_queen", "bg.cave"),
    ("Orc",         "Strength Unbroken",       "race.orc",          "bg.banditcamp"),
    ("Elf",         "Older Than the Road",     "race.elf",          "bg.mire"),
    ("Dwarf",       "Stone and Stubbornness",  "race.dwarf",        "bg.mountains"),
    ("Tiefling",    "Born of a Darker Fire",   "race.tiefling",     "bg.depths"),
]


def backdrop(key):
    for ext in (".webp", ".png", ".jpg"):
        p = ART / (key.replace(".", "_") + ext)
        if p.exists():
            im = Image.open(p).convert("RGB")
            # cover-crop to the poster canvas
            s = max(W / im.width, H / im.height)
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
            l, t = (im.width - W) // 2, (im.height - H) // 2
            return im.crop((l, t, l + W, t + H))
    return Image.new("RGB", (W, H), (18, 15, 26))


def build(name, role, sprite_key, bg_key, path, cover=False):
    bg = backdrop(bg_key).filter(ImageFilter.GaussianBlur(5))
    # darken, heavier at the bottom so the type reads
    veil = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(veil)
    for y in range(H):
        vd.line([(0, y), (W, y)], fill=int(140 + 95 * (y / H)))
    bg = Image.composite(Image.new("RGB", (W, H), (8, 6, 14)), bg, veil)

    poster = bg.convert("RGBA")

    # warm glow behind the subject
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W * 0.16, H * 0.20, W * 0.84, H * 0.80], fill=(224, 179, 77, 46))
    poster = Image.alpha_composite(poster, glow.filter(ImageFilter.GaussianBlur(90)))

    # the character
    sp = None
    for d in (HI, ART):
        p = d / (sprite_key.replace(".", "_") + ".png")
        if p.exists():
            sp = Image.open(p).convert("RGBA")
            break
    if sp:
        target_h = int(H * 0.64)
        s = target_h / sp.height
        sp = sp.resize((max(1, int(sp.width * s)), target_h), Image.LANCZOS)
        if sp.width > W - 120:
            s2 = (W - 120) / sp.width
            sp = sp.resize((W - 120, max(1, int(sp.height * s2))), Image.LANCZOS)
        # soft contact shadow
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([W / 2 - sp.width * 0.42, 1010, W / 2 + sp.width * 0.42, 1080],
                                   fill=(0, 0, 0, 150))
        poster = Image.alpha_composite(poster, sh.filter(ImageFilter.GaussianBlur(22)))
        poster.alpha_composite(sp, (int(W / 2 - sp.width / 2), 1010 - sp.height))

    d = ImageDraw.Draw(poster)

    # wordmark, top (skipped on the cover, which already carries the title)
    if not cover:
        spaced(d, W / 2, 74, "AETHELGARD", F_UI_B(26), GOLD, tracking=13)

    # name
    spaced(d, W / 2, 1092, name.upper(), F_DISPLAY(74), PALE, tracking=5)
    # rule
    d.line([(W / 2 - 90, 1140), (W / 2 + 90, 1140)], fill=GOLD, width=3)
    # role
    spaced(d, W / 2, 1180, role.upper(), F_UI(22), MUTED, tracking=4)

    # footer
    d.text((72, 1296), "" if cover else "CHRONICLES OF FATE", font=F_UI_B(19), fill=(150, 142, 170), anchor="lm")
    d.text((W - 72, 1296), "by Dr. Sohil Momin", font=F_UI(19), fill=(150, 142, 170), anchor="rm")

    poster.convert("RGB").save(path, "JPEG", quality=90, optimize=True)
    return path


n = 0
for name, role, sprite, bg in POSTERS:
    fn = name.lower().replace(" ", "-") + ".jpg"
    build(name, role, sprite, bg, OUT / fn)
    n += 1
    print(f"  {fn}")

# a square hero card for the grid
build("Aethelgard", "Chronicles of Fate", "class.warrior", "bg.title", OUT / "cover.jpg", cover=True)
print(f"\nWrote {n + 1} posters to {OUT}")
