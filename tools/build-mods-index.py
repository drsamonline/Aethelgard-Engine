#!/usr/bin/env python3
"""
Aethelgard mod manifest builder.

Scans the mods/ folder and regenerates BOTH:
  mods/index.js   (used when the game is opened from disk, file://)
  mods/mods.json  (used when the game is served over http/https)

Run it from the game's root folder:

    python3 tools/build-mods-index.py

Any *.js file in mods/ is treated as a mod, except index.js itself.
Load order follows the filename sort, so prefix files with numbers
(10-base.js, 20-addon.js) if order matters.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODS = ROOT / "mods"

if not MODS.is_dir():
    sys.exit(f"No mods/ folder found at {MODS}")

# a mod is either mods/<name>.js or a folder with mods/<name>/mod.js
files = [p.name for p in MODS.glob("*.js") if p.name != "index.js"]
files += [f"{p.parent.name}/mod.js" for p in MODS.glob("*/mod.js")]
files = sorted(files)

index_js = (
    "/* ============================================================\n"
    "   Aethelgard - MOD MANIFEST (auto-generated)\n"
    "   Regenerate with:  python3 tools/build-mods-index.py\n"
    "   ============================================================ */\n"
    "window.AETHELGARD_MOD_FILES = [\n"
    + "".join(f'  "{f}",\n' for f in files)
    + "];\n"
)
(MODS / "index.js").write_text(index_js, encoding="utf-8")
(MODS / "mods.json").write_text(json.dumps(files, indent=2) + "\n", encoding="utf-8")

print(f"Found {len(files)} mod(s):")
for f in files:
    print(f"  - {f}")
print("Wrote mods/index.js and mods/mods.json")
