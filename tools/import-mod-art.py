#!/usr/bin/env python3
"""
Imports the art generated for the two story mods.

    python3 tools/import-mod-art.py <stripped-source-folder>

Expects the magenta-background PNGs already caption-stripped (see
strip_caption in this file), and routes each file to the mod that owns it:

    mods/story-expansion/sprites/   The Hollow Crown  (foes, regions, POIs)
    mods/villain-arc/sprites/       The Crown's Shadow (villains, heroes)

Characters are cut out, trimmed, squared and saved at 256x256 WebP.
Backdrops are saved at 1600px wide, aspect preserved (the game cover-fits).
"""
import pathlib
import sys
from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
CELL = 256
BG_WIDTH = 1600

STORY = ROOT / "mods" / "story-expansion" / "sprites"
VILLAIN = ROOT / "mods" / "villain-arc" / "sprites"


def owner(stem):
    """which mod does this file belong to?"""
    if stem.startswith(("enemy_frost_revenant", "enemy_hollow_knight", "enemy_choir_wretch",
                        "bg_hollowmere", "bg_drownedchoir", "loc_hollowmere", "loc_drownedchoir",
                        "poi_hollowmere", "poi_drownedchoir")):
        return STORY
    return VILLAIN


# ------------------------------------------------------------------ cutout
def remove_flat_bg(im, tol=64):
    """Flood-fill from the border, treating near-magenta as background."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()

    def is_bg(c):
        r, g, b = c[0], c[1], c[2]
        # magenta field, plus the near-white frame some exports carry
        magenta = r > 150 and b > 130 and g < 130 and (r - g) > 60 and (b - g) > 50
        whiteish = r > 232 and g > 232 and b > 232
        return magenta or whiteish

    seen = bytearray(w * h)
    stack = []
    for x in range(w):
        stack.append((x, 0)); stack.append((x, h - 1))
    for y in range(h):
        stack.append((0, y)); stack.append((w - 1, y))
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h: continue
        i = y * w + x
        if seen[i]: continue
        c = px[x, y]
        if not is_bg(c): continue
        seen[i] = 1
        px[x, y] = (0, 0, 0, 0)
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    # the flood fill cannot reach magenta trapped between limbs, so sweep the
    # whole image for the chroma-key colour afterwards. True magenta is never a
    # natural art colour, so this is safe.
    for y in range(h):
        for x in range(w):
            c = px[x, y]
            if c[3] and c[0] > 150 and c[2] > 130 and c[1] < 130 and (c[0]-c[1]) > 60 and (c[2]-c[1]) > 50:
                px[x, y] = (0, 0, 0, 0)
    return im


def drop_sparse_edges(im, min_frac=0.03):
    """Some exports leave a 1-2px line down the edge. Clear any column or row
    that is almost entirely transparent."""
    im = im.convert("RGBA"); w, h = im.size
    px = im.load()
    for x in range(w):
        op = sum(1 for y in range(h) if px[x, y][3] > 24)
        if op < h * min_frac:
            for y in range(h): px[x, y] = (0, 0, 0, 0)
    for y in range(h):
        op = sum(1 for x in range(w) if px[x, y][3] > 24)
        if op < w * min_frac:
            for x in range(w): px[x, y] = (0, 0, 0, 0)
    return im


def trim(im, pad_frac=0.06):
    bbox = im.getbbox()
    if bbox: im = im.crop(bbox)
    w, h = im.size
    side = int(max(w, h) * (1 + pad_frac * 2))
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.paste(im, ((side - w) // 2, (side - h) // 2), im)
    return out


def main():
    src = pathlib.Path(sys.argv[1])
    STORY.mkdir(parents=True, exist_ok=True)
    VILLAIN.mkdir(parents=True, exist_ok=True)
    for p in sorted(src.rglob("*.png")):
        stem = p.stem
        dest = owner(stem)
        im = Image.open(p)
        if stem.startswith("bg_"):
            w, h = im.size
            im = im.convert("RGB").resize((BG_WIDTH, max(1, round(h * BG_WIDTH / w))), Image.LANCZOS)
            out = dest / (stem + ".webp")
            im.save(out, "WEBP", quality=88, method=6)
            print(f"  backdrop  {stem:34} {im.size}  {out.stat().st_size//1024} KB  -> {dest.parent.name}")
        else:
            im = remove_flat_bg(im)
            im = drop_sparse_edges(im)
            im = trim(im).resize((CELL, CELL), Image.LANCZOS)
            out = dest / (stem + ".webp")
            im.save(out, "WEBP", quality=90, method=6)
            print(f"  sprite    {stem:34} {im.size}  {out.stat().st_size//1024} KB  -> {dest.parent.name}")


if __name__ == "__main__":
    main()
