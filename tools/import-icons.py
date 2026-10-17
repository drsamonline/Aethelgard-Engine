#!/usr/bin/env python3
"""
Imports the base-game icon sheets (skills, statuses, buildings, gear sets,
points of interest, achievements).

    python3 tools/import-icons.py <folder-of-pngs>

Each source PNG is a crop from a contact sheet, so it usually carries a sliver
of its neighbour along one edge. This cuts out the magenta, keeps only the
LARGEST connected blob (the real icon) and throws the slivers away, then trims,
squares and saves a 256x256 WebP.

Icons land in mods/ai-art/sprites/ as individual files, and are listed in the
art pack's mod.js so they ride along with whichever pack is selected.
"""
import pathlib
import sys
from PIL import Image, ImageDraw
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "mods" / "ai-art" / "sprites"
CELL = 256
KNOWN = ("skill", "status", "bld", "set", "poi", "ach")


def is_bg(c):
    """the magenta field, plus the near-white frame some exports carry"""
    r, g, b = c[0], c[1], c[2]
    magenta = r > 140 and b > 120 and g < 135 and (r - g) > 55 and (b - g) > 45
    whiteish = r > 236 and g > 236 and b > 236
    return magenta or whiteish


def cut(im, trim_edge=2):
    """Cut the magenta field out, vectorised."""
    im = im.convert("RGBA")
    w, h = im.size
    if trim_edge and w > trim_edge * 4 and h > trim_edge * 4:
        im = im.crop((trim_edge, trim_edge, w - trim_edge, h - trim_edge))
        w, h = im.size
    # Only MAGENTA is removed, so white highlights inside an icon survive.
    # No flood fill is needed: the vectorised sweep below is far faster and the
    # sliver is separated from the icon by a magenta gap, which keep_main_region
    # uses to tell them apart.
    a = np.array(im)
    r, g, b, al = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int), a[..., 3]
    mag = (r > 140) & (b > 120) & (g < 135) & ((r - g) > 55) & ((b - g) > 45)
    a[..., 3] = np.where(mag, 0, al)
    return Image.fromarray(a)


def keep_main_region(im):
    """Keep only the main icon. These files are crops from a contact sheet, so
    they carry a sliver of the neighbouring icon along an edge — separated from
    the real icon by a strip of magenta. The widest run of non-empty columns
    (and rows) is the icon; everything outside it is dropped."""
    a = np.array(im.convert("RGBA"))
    mask = a[..., 3] > 24
    if not mask.any():
        return im
    def runs(profile):
        out, start = [], None
        for i, v in enumerate(profile):
            if v and start is None: start = i
            elif not v and start is not None: out.append((start, i)); start = None
        if start is not None: out.append((start, len(profile)))
        return out
    # Each crop holds its own icon on the LEFT with the next icon bleeding in on
    # the right, so the leftmost run wide enough to be a real icon is the one we
    # want — not the widest, which can be the neighbour.
    cols = runs(mask.sum(axis=0) > 0)
    minw = mask.shape[1] * 0.18
    pick = next((r for r in cols if r[1] - r[0] >= minw), cols[0] if cols else (0, mask.shape[1]))
    c0, c1 = pick
    band = mask[:, c0:c1]
    rows = runs(band.sum(axis=1) > 0)
    minh = mask.shape[0] * 0.18
    rp = next((r for r in rows if r[1] - r[0] >= minh), rows[0] if rows else (0, mask.shape[0]))
    r0, r1 = rp
    if c1 - c0 < 4 or r1 - r0 < 4:
        return im
    return im.crop((c0, r0, c1, r1))


def trim_square(im, pad=0.06):
    bbox = im.getbbox()
    if bbox: im = im.crop(bbox)
    w, h = im.size
    side = int(max(w, h) * (1 + pad * 2))
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.paste(im, ((side - w) // 2, (side - h) // 2), im)
    return out


def key_from(stem):
    for k in KNOWN:
        if stem.startswith(k + "_"):
            rest = stem[len(k) + 1:]
            if k == "poi":
                parts = rest.split("_")
                if len(parts) >= 2:
                    return "poi." + parts[0] + "." + "_".join(parts[1:])
            return k + "." + rest
    return None


def main():
    src = pathlib.Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for p in sorted(src.rglob("*.png")):
        key = key_from(p.stem)
        if not key:
            print(f"  skipped (unknown prefix): {p.name}"); continue
        im = Image.open(p)
        before = im.size
        im = cut(im)
        im = keep_main_region(im)
        im = trim_square(im).resize((CELL, CELL), Image.LANCZOS)
        dest = OUT / (p.stem + ".webp")
        im.save(dest, "WEBP", quality=90, method=4)
        made.append((key, p.stem + ".webp"))
        print(f"  {p.stem:28} {str(before):12} -> {key:28} {dest.stat().st_size//1024} KB")
    print(f"\n{len(made)} icons written to {OUT.relative_to(ROOT)}")
    pathlib.Path("/scratch/work/icon_keys.json").write_text(
        __import__("json").dumps(made, indent=1))


if __name__ == "__main__":
    main()
