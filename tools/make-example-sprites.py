#!/usr/bin/env python3
"""
Generates the sprite images for the bundled example graphics pack
(mods/example-graphics/). Pure PIL — no external art needed.

    python3 tools/make-example-sprites.py

These are deliberately simple flat pictograms: they exist to prove the
sprite pipeline works end to end, and to show pack authors the expected
file layout. Replace them with real art and nothing else changes.
"""
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "mods" / "example-graphics" / "sprites"
OUT.mkdir(parents=True, exist_ok=True)

S = 64
BG = (24, 20, 36, 255)


def canvas(border):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([2, 2, S - 3, S - 3], radius=12, fill=BG, outline=border, width=3)
    return img, d


def save(img, name):
    img.save(OUT / name)
    return name


# ---------- pictograms ----------
def person(c, accent=(230, 179, 77, 255)):
    img, d = canvas(accent)
    d.ellipse([24, 14, 40, 30], fill=accent)                       # head
    d.polygon([(32, 32), (16, 54), (48, 54)], fill=accent)         # shoulders
    return img

def beast(c, accent=(150, 160, 190, 255)):
    img, d = canvas(accent)
    d.polygon([(12, 22), (20, 10), (26, 22)], fill=accent)         # ears
    d.polygon([(38, 22), (44, 10), (52, 22)], fill=accent)
    d.ellipse([16, 20, 48, 46], fill=accent)                       # head
    d.polygon([(24, 46), (32, 58), (40, 46)], fill=accent)         # snout
    return img

def monster(c, accent=(120, 190, 120, 255)):
    img, d = canvas(accent)
    d.ellipse([14, 18, 50, 50], fill=accent)
    d.polygon([(20, 18), (26, 6), (32, 18)], fill=accent)          # horns
    d.polygon([(32, 18), (38, 6), (44, 18)], fill=accent)
    d.rectangle([24, 32, 29, 38], fill=BG)                         # eyes
    d.rectangle([35, 32, 40, 38], fill=BG)
    return img

def boss(c, accent=(230, 90, 70, 255)):
    img, d = canvas(accent)
    d.polygon([(32, 8), (52, 22), (46, 52), (18, 52), (12, 22)], fill=accent)
    d.polygon([(24, 26), (32, 20), (40, 26), (32, 36)], fill=BG)   # eye slit
    return img

def sword(c, accent=(200, 210, 235, 255)):
    img, d = canvas(accent)
    d.polygon([(32, 8), (39, 20), (36, 42), (28, 42), (25, 20)], fill=accent)
    d.rectangle([20, 44, 44, 49], fill=(140, 110, 70, 255))        # guard
    d.rectangle([30, 49, 34, 58], fill=(140, 110, 70, 255))        # grip
    return img

def shield(c, accent=(110, 160, 220, 255)):
    img, d = canvas(accent)
    d.polygon([(32, 8), (52, 16), (48, 40), (32, 56), (16, 40), (12, 16)], fill=accent)
    d.line([(32, 16), (32, 48)], fill=BG, width=4)
    return img

def bow(c, accent=(150, 200, 130, 255)):
    img, d = canvas(accent)
    d.arc([12, 10, 60, 54], start=290, end=70, fill=accent, width=5)
    d.line([(40, 12), (40, 52)], fill=(220, 220, 220, 255), width=2)
    d.polygon([(36, 32), (56, 28), (56, 36)], fill=accent)
    return img

def flask(c, accent=(220, 110, 190, 255)):
    img, d = canvas(accent)
    d.rectangle([27, 10, 37, 24], fill=(200, 200, 210, 255))
    d.polygon([(27, 24), (37, 24), (50, 52), (14, 52)], fill=accent)
    return img

def gem(c, accent=(90, 200, 230, 255)):
    img, d = canvas(accent)
    d.polygon([(32, 10), (50, 26), (32, 54), (14, 26)], fill=accent)
    d.line([(14, 26), (50, 26)], fill=BG, width=3)
    return img

def coin(c, accent=(235, 195, 70, 255)):
    img, d = canvas(accent)
    d.ellipse([14, 14, 50, 50], fill=accent)
    d.ellipse([22, 22, 42, 42], outline=BG, width=4)
    return img

def wood(c, accent=(160, 120, 80, 255)):
    img, d = canvas(accent)
    d.rounded_rectangle([14, 18, 50, 46], radius=8, fill=accent)
    d.ellipse([44, 24, 54, 40], fill=(120, 88, 56, 255))
    return img

def ore(c, accent=(150, 150, 165, 255)):
    img, d = canvas(accent)
    d.polygon([(14, 46), (24, 20), (40, 18), (52, 40), (44, 50), (20, 50)], fill=accent)
    d.polygon([(28, 30), (36, 26), (40, 38), (30, 40)], fill=(235, 235, 245, 255))
    return img

def house(c, accent=(200, 160, 100, 255)):
    img, d = canvas(accent)
    d.polygon([(32, 10), (54, 30), (10, 30)], fill=(180, 90, 70, 255))
    d.rectangle([16, 30, 48, 52], fill=accent)
    d.rectangle([27, 38, 37, 52], fill=BG)
    return img

def tree(c, accent=(110, 180, 110, 255)):
    img, d = canvas(accent)
    d.rectangle([28, 38, 36, 54], fill=(120, 88, 56, 255))
    d.ellipse([12, 12, 52, 44], fill=accent)
    return img

def mountain(c, accent=(170, 175, 200, 255)):
    img, d = canvas(accent)
    d.polygon([(8, 52), (26, 18), (40, 52)], fill=accent)
    d.polygon([(30, 52), (46, 26), (58, 52)], fill=(140, 145, 175, 255))
    return img

def cave(c, accent=(140, 130, 170, 255)):
    img, d = canvas(accent)
    d.rounded_rectangle([10, 14, 54, 54], radius=10, fill=accent)
    d.ellipse([20, 28, 44, 56], fill=BG)
    return img

def temple(c, accent=(225, 215, 180, 255)):
    img, d = canvas(accent)
    d.polygon([(32, 10), (52, 26), (12, 26)], fill=accent)
    d.rectangle([16, 26, 48, 32], fill=accent)
    for x in (18, 27, 36, 45):
        d.rectangle([x, 32, x + 4, 50], fill=accent)
    d.rectangle([12, 50, 52, 55], fill=accent)
    return img

def skull(c, accent=(220, 220, 210, 255)):
    img, d = canvas(accent)
    d.ellipse([16, 12, 48, 44], fill=accent)
    d.rectangle([24, 42, 40, 54], fill=accent)
    d.ellipse([23, 24, 31, 34], fill=BG)
    d.ellipse([33, 24, 41, 34], fill=BG)
    return img

def tower(c, accent=(160, 130, 200, 255)):
    img, d = canvas(accent)
    d.rectangle([20, 20, 44, 54], fill=accent)
    d.polygon([(16, 20), (48, 20), (44, 10), (20, 10)], fill=accent)
    d.rectangle([28, 34, 36, 44], fill=BG)
    return img


PICTOGRAMS = {
    "person": person, "beast": beast, "monster": monster, "boss": boss, "sword": sword,
    "shield": shield, "bow": bow, "flask": flask, "gem": gem, "coin": coin, "wood": wood,
    "ore": ore, "house": house, "tree": tree, "mountain": mountain, "cave": cave,
    "temple": temple, "skull": skull, "tower": tower,
}

# entity key -> pictogram, with an optional accent colour
SPRITES = {
    "enemy.rat":          ("beast",    (170, 160, 150, 255)),
    "enemy.wolf":         ("beast",    (150, 160, 190, 255)),
    "enemy.goblin":       ("monster",  (120, 190, 120, 255)),
    "enemy.spider":       ("monster",  (170, 120, 190, 255)),
    "enemy.boar":         ("beast",    (170, 140, 110, 255)),
    "enemy.bandit":       ("person",   (200, 140, 110, 255)),
    "enemy.rogue_mage":   ("person",   (150, 120, 220, 255)),
    "enemy.assassin":     ("person",   (140, 140, 160, 255)),
    "enemy.ogre":         ("monster",  (200, 150, 90, 255)),
    "enemy.bat":          ("beast",    (130, 120, 160, 255)),
    "enemy.golem":        ("monster",  (150, 150, 165, 255)),
    "enemy.wraith":       ("skull",    (150, 190, 210, 255)),
    "enemy.harpy":        ("beast",    (200, 170, 120, 255)),
    "enemy.wyvern":       ("beast",    (200, 110, 90, 255)),
    "enemy.coven":        ("boss",     (200, 90, 150, 255)),
    "enemy.warden":       ("boss",     (220, 120, 70, 255)),
    "enemy.warlord":      ("boss",     (210, 100, 90, 255)),
    "enemy.spider_queen": ("boss",     (170, 110, 200, 255)),
    "enemy.bog_horror":   ("boss",     (110, 170, 130, 255)),
    "class.warrior":      ("sword",    (200, 90, 80, 255)),
    "class.berserker":    ("sword",    (230, 90, 70, 255)),
    "class.defender":     ("shield",   (110, 160, 220, 255)),
    "class.archer":       ("bow",      (150, 200, 130, 255)),
    "class.thief":        ("person",   (150, 150, 170, 255)),
    "class.swordmaster":  ("sword",    (210, 200, 160, 255)),
    "class.duelist":      ("sword",    (190, 190, 220, 255)),
    "class.mage":         ("person",   (150, 120, 220, 255)),
    "item.potion":        ("flask",    (220, 110, 190, 255)),
    "item.ether":         ("flask",    (110, 180, 220, 255)),
    "item.antidote":      ("flask",    (130, 200, 150, 255)),
    "item.wood":          ("wood",     (160, 120, 80, 255)),
    "item.iron":          ("ore",      (150, 150, 165, 255)),
    "item.ore":           ("ore",      (120, 130, 150, 255)),
    "item.leather":       ("wood",     (170, 120, 90, 255)),
    "item.ruby":          ("gem",      (230, 90, 110, 255)),
    "item.herb":          ("tree",     (130, 200, 140, 255)),
    "item.food":          ("wood",     (210, 180, 120, 255)),
    "item.fish":          ("beast",    (140, 190, 210, 255)),
    "loc.oakhaven":       ("house",    (200, 160, 100, 255)),
    "loc.mire":           ("tree",     (120, 170, 130, 255)),
    "loc.cave":           ("cave",     (140, 130, 170, 255)),
    "loc.mountains":      ("mountain", (170, 175, 200, 255)),
    "loc.temple":         ("temple",   (225, 215, 180, 255)),
    "loc.ruins":          ("tower",    (160, 130, 200, 255)),
    "loc.banditcamp":     ("tower",    (200, 140, 100, 255)),
    "loc.depths":         ("skull",    (180, 120, 200, 255)),
    "race.human":         ("person",   (210, 180, 140, 255)),
    "race.elf":           ("bow",      (150, 210, 160, 255)),
    "race.dwarf":         ("ore",      (190, 150, 110, 255)),
    "race.orc":           ("monster",  (140, 190, 120, 255)),
    "race.halfling":      ("person",   (200, 190, 140, 255)),
    "race.tiefling":      ("monster",  (200, 110, 140, 255)),
    "race.beastkin":      ("beast",    (200, 170, 120, 255)),
    "race.revenant":      ("skull",    (150, 190, 210, 255)),
    "companion.bryn":     ("shield",   (110, 160, 220, 255)),
    "companion.sylva":    ("bow",      (150, 200, 130, 255)),
    "companion.mordecai": ("person",   (150, 120, 220, 255)),
    "companion.pip":      ("person",   (200, 170, 120, 255)),
    "companion.sister_maeve": ("temple", (235, 225, 190, 255)),
}

count = 0
for key, (pict, accent) in SPRITES.items():
    fn = key.replace(".", "_") + ".png"
    save(PICTOGRAMS[pict](None, accent), fn)
    count += 1

# ---- also emit the pack mod file so keys and files can never drift ----
lines = []
for key in SPRITES:
    lines.append(f'    "{key}": "{key.replace(".", "_")}.png",')
mod = """/* ============================================================
   EXAMPLE GRAPHICS PACK — generated by tools/make-example-sprites.py
   A drop-in art pack. It registers images for the game's sprite
   keys; anything it does not cover keeps its emoji fallback.
   Pick it in Settings -> Graphics pack.
   ============================================================ */
window.AETHELGARD_MODS = window.AETHELGARD_MODS || [];

window.AETHELGARD_MODS.push({
  id: "example-graphics",
  name: "Flat Icon Pack (example)",
  version: "1.0.0",
  author: "Dr. Sohil Momin",
  description: "A simple flat sprite set that replaces the emoji art. Demonstrates the graphics-pack format.",
  impact: "additive",

  GRAPHICS: {
    id: "flat-icons",
    name: "Flat Icons",
    base: "mods/example-graphics/sprites/",   // every src below is relative to this
    pixel: true,                              // crisp scaling for pixel art
    scale: 1.15,                              // default size in em
    sprites: {
""" + "\n".join(lines) + """
    },
  },
});
"""
(OUT.parent / "mod.js").write_text(mod, encoding="utf-8")
print(f"Wrote {count} sprites to {OUT}")
print("Wrote", OUT.parent / "mod.js")
