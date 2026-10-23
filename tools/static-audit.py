#!/usr/bin/env python3
"""Static audit: every function, every reference, dead code, duplicates."""
import re, pathlib, collections, json, sys

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
JS = sorted(list(ROOT.glob("js/**/*.js")) + list(ROOT.glob("mods/**/*.js")))
HTML = (ROOT / "index.html").read_text() if (ROOT / "index.html").exists() else ""

print("=" * 74)
print("STATIC AUDIT")
print("=" * 74)

src = {}
for p in JS:
    try:
        src[str(p.relative_to(ROOT))] = p.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  !! cannot read {p}: {e}")

total_lines = sum(s.count("\n") + 1 for s in src.values())
print(f"\n[1] FILES  {len(src)} JS files, {total_lines} lines")

# ---- 2. every function defined -------------------------------------------
defs = {}          # name -> [files]
for f, s in src.items():
    for m in re.finditer(r'^\s*G\.([A-Za-z_$][\w$]*)\s*=\s*(?:async\s+)?function', s, re.M):
        defs.setdefault(m.group(1), []).append(f)
    for m in re.finditer(r'^\s*function\s+([A-Za-z_$][\w$]*)\s*\(', s, re.M):
        defs.setdefault(m.group(1), []).append(f)
    for m in re.finditer(r'^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function|\()', s, re.M):
        defs.setdefault(m.group(1), []).append(f)

print(f"\n[2] FUNCTIONS  {len(defs)} defined")
dupes = {n: f for n, f in defs.items() if len(f) > 1}
if dupes:
    print(f"  !! {len(dupes)} defined more than once:")
    for n, f in sorted(dupes.items())[:20]:
        print(f"       {n}: {', '.join(f)}")
else:
    print("  no duplicate definitions")

# ---- 3. unreferenced (dead) functions ------------------------------------
allsrc = "\n".join(src.values()) + HTML
dead = []
for n, files in defs.items():
    # count uses outside its own definition line
    uses = len(re.findall(r'\b' + re.escape(n) + r'\b', allsrc))
    if uses <= len(files):
        dead.append((n, files[0]))
print(f"\n[3] DEAD CODE  {len(dead)} unreferenced function(s)")
for n, f in sorted(dead, key=lambda x: x[1]):
    print(f"       {n}  ({f})")

# ---- 4. G.xxx referenced but never defined -------------------------------
called = set(re.findall(r'\bG\.([A-Za-z_$][\w$]*)', allsrc))
builtin_ok = {"t","fmt","rnd","sprite","clog","log","notify","state","settings","store"}
undef = sorted(c for c in called if c not in defs and c not in builtin_ok)
# filter out data-table references (they are objects, not functions)
tables = set()
for s in src.values():
    for m in re.finditer(r'^\s*([A-Z][A-Z_0-9]{2,})\s*[:=]', s, re.M):
        tables.add(m.group(1))
tables |= set(re.findall(r'Object\.assign\(window\.Game,\s*\{([^}]*)\}', allsrc)[0].split(",")) if re.findall(r'Object\.assign\(window\.Game,\s*\{([^}]*)\}', allsrc) else set()
undef_fn = [u for u in undef if u not in tables and not u[0].isupper()]
print(f"\n[4] UNDEFINED REFERENCES  {len(undef_fn)} lowercase G.x used but never defined")
for u in undef_fn[:25]:
    print(f"       G.{u}")

# ---- 5. script tags vs files --------------------------------------------
refs = re.findall(r'<script src="([^"]+)"', HTML)
missing = [r for r in refs if not (ROOT / r).exists()]
on_disk = {str(p.relative_to(ROOT)) for p in JS}
not_loaded = sorted(on_disk - set(refs))
print(f"\n[5] SCRIPT WIRING  {len(refs)} tags in index.html")
print(f"  missing files: {missing or 'none'}")
print(f"  never loaded:  {not_loaded or 'none'}")

# ---- 6. data tables ------------------------------------------------------
print(f"\n[6] DATA TABLES")
for name in ["RACES","CLASSES","ENEMIES","GEAR","ITEMS","ACTIVE_SKILLS","BUILDINGS","COMPANIONS",
             "NPCS","GEMS","GEAR_SETS","STATUS","ELEMENTS","ACHIEVEMENTS","SIDE_QUESTS",
             "CLASS_MISSIONS","LOCATIONS","CHAPTERS","ARENA_WAVES","CONSUMABLE_RECIPES"]:
    n = len(re.findall(r'"' + name + r'"\s*:', allsrc))
    print(f"       {name:22} referenced {n}x")

print()
print("=" * 74)
print(f"SUMMARY: {len(defs)} functions | {len(dead)} dead | {len(dupes)} duplicated | "
      f"{len(undef_fn)} undefined refs | {len(missing)} missing files")
print("=" * 74)
