#!/usr/bin/env python3
"""
Builds AI_ART_PROMPTS.md — a copy-paste prompt sheet for every sprite key
the game asks for that the AI art pack does not already cover.

    python3 tools/make-prompt-sheet.py

Each prompt is complete: subject + style line, ready to paste straight into
an image model. Save the result under the filename shown.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "AI_ART_PROMPTS.md"

SPRITE_STYLE = ("fantasy game sprite, bold stylized illustration with thick dark outlines, "
                "dramatic rim lighting, full body, centered, high contrast, standing on a "
                "completely plain flat solid magenta background, no text")

ICON_STYLE = ("fantasy game inventory icon, bold stylized illustration with thick dark outlines, "
              "dramatic rim lighting, centered, high contrast, on a completely plain flat solid "
              "magenta background, no text")

# ---- everything still to generate (subject text only; style is appended) ----
ENEMIES = {
    "rat":        "a giant diseased rat with matted grey fur, a bare tail and glowing red eyes",
    "bat":        "a giant cave bat with wide leathery spread wings and glowing yellow eyes",
    "boar":       "a ferocious wild boar with long tusks, bristled dark hide and a scarred snout",
    "bandit":     "a scarred human bandit in a dark hood and studded leather straps, holding a curved dagger",
    "harpy":      "a harpy with broad feathered wings, sharp talons and wild tangled hair",
    "ghoul":      "a gaunt flesh eating ghoul with grey mottled skin, long claws and hollow glowing eyes",
    "rogue_mage": "a renegade rogue mage in a tattered blue robe with crackling lightning in his hands",
    "golem":      "a hulking stone golem built from cracked boulders with glowing blue runes",
    "wyvern":     "a red wyvern, a two legged winged dragon with a spiked tail",
    "assassin":   "a masked nightblade assassin in black leathers holding two curved blades",
}
CLASSES = {
    "defender":     "a stout armoured defender in heavy plate carrying a tall tower shield",
    "thief":        "a stealthy hooded thief in dark leathers holding two daggers, crouched low",
    "swordmaster":  "an elegant swordmaster in ornate light armour holding a single longsword, flowing cape",
    "duelist":      "a nimble duel wielder in a feathered hat and buckled coat, a rapier in each hand",
}
RACES = {
    "human":    "a determined human adventurer in simple travelling leathers with a short sword",
    "elf":      "a graceful elf ranger in green woodland leathers drawing a longbow",
    "dwarf":    "a stout dwarf warrior with a braided beard, heavy armour and a war hammer",
    "orc":      "a powerful orc warrior with tusks, scarred green skin and a broad battle axe",
    "halfling": "a cheerful small halfling adventurer in a waistcoat with a short sword",
    "tiefling": "a tiefling with curved horns, crimson skin and a long tail, in dark robes",
    "beastkin": "a beastkin with feline ears, tawny fur and clawed hands, in tribal leathers",
    "revenant": "an undead revenant warrior with a pale skeletal face and tattered armour",
}
COMPANIONS = {
    "bryn":         "a loyal shieldmaiden companion in chainmail with a round shield and sword",
    "sylva":        "a young elf scout companion in green leathers with a shortbow",
    "mordecai":     "a brooding hooded sorcerer companion with a staff and glowing runes",
    "pip":          "a small cheerful halfling companion with a sling and a heavy pack",
    "sister_maeve": "a serene priestess companion in white and gold robes holding a staff",
}
ITEMS = {
    "wood":     "a bundle of cut wooden logs",
    "iron":     "a chunk of raw iron ore",
    "leather":  "a folded piece of tanned leather hide",
    "ruby":     "a cut red ruby gemstone",
    "food":     "a loaf of crusty bread",
    "fish":     "a fresh silver fish",
    "herb":     "a bundle of green healing herbs",
    "ore":      "a lump of deep glowing ore",
    "relic":    "a stolen golden relic idol",
    "potion":   "a glass flask of glowing red health potion",
    "ether":    "a glass flask of glowing blue energy draught",
    "antidote": "a glass flask of glowing green antidote",
    "elixir":   "a glass flask of golden elixir",
    "lockpick": "a set of metal lockpicks",
    "meal":     "a hearty plated meal of roast meat and vegetables",
    "artifact": "an ancient glowing magical artifact",
}
GEAR = {
    "dagger":         "a rusty iron dagger",
    "hand_axe":       "a small hand axe with a wooden haft",
    "hunting_bow":    "a simple wooden hunting bow",
    "apprentice_staff": "a plain wooden apprentice staff",
    "mace":           "an iron mace with a flanged head",
    "katana":         "a folded steel katana",
    "steel_sword":    "a polished steel longsword",
    "twin_dagger":    "a matched pair of twin daggers",
    "runic_blade":    "a sword etched with glowing blue runes",
    "arcane_staff":   "an arcane staff topped with a glowing crystal",
    "dragonfang":     "a curved blade carved from a dragon fang",
    "dagger2":        "a slim parrying dagger with a crossguard",
    "tower_shield":   "a tall wooden tower shield with iron banding",
    "buckler":        "a small round metal buckler",
    "spell_tome":     "a heavy leather bound spell tome with a glowing clasp",
    "clothes":        "a set of tattered cloth garments",
    "leather_armor":  "a leather armour chestpiece",
    "iron_plate":     "an iron plate armour chestpiece",
    "dragonscale":    "a dragonscale armour chestpiece of overlapping scales",
    "robe":           "an arcane robe embroidered with silver thread",
    "iron_helm":      "an iron helmet with a visor",
    "hood":           "a dark shadow hood",
    "circlet":        "an arcane circlet set with a blue gem",
    "swift_boots":    "a pair of light swift leather boots",
    "plated_boots":   "a pair of heavy plated boots",
    "ruby_ring":      "a gold ring set with a ruby",
    "signet":         "a heavy warlord's signet ring",
    "arcane_amulet":  "an arcane amulet on a silver chain",
    "guardian_amulet": "a guardian amulet with a blue stone",
}
GEMS = {
    "ruby": "red ruby", "sapphire": "deep blue sapphire", "emerald": "green emerald",
    "topaz": "golden topaz", "amethyst": "violet amethyst", "diamond": "clear white diamond",
    "onyx": "black onyx",
}


def block(fullkey, subject, style, note=None):
    fn = fullkey.replace(".", "_")
    ext = ".webp" if fullkey.startswith("bg.") else ".png"
    out = [f"### `{fn}{ext}`", ""]
    if note:
        out.append(f"_{note}_")
        out.append("")
    out.append("```")
    out.append(f"{subject}, {style}")
    out.append("```")
    out.append("")
    return "\n".join(out)


def section(title, intro, table, style, prefix, ratio="1:1", note=None):
    out = [f"## {title}", ""]
    if intro:
        out.append(intro)
        out.append("")
    out.append(f"**Generate at {ratio}.**")
    out.append("")
    for k, v in table.items():
        out.append(block(f"{prefix}.{k}", v, style, note))
    return "\n".join(out)


parts = []
parts.append("""# Aethelgard — AI art prompt sheet

Every prompt below is **complete and ready to copy-paste** — the subject and the
style line are already combined. Paste one into your image model, then save the
result under the filename shown in the heading (e.g. `enemy_rat.png`).

You do not have to do them all. **Anything you skip simply keeps its emoji**, so
send them in any batch size and I will import whatever arrives.

## The one rule that matters

**Characters and items** must sit on a completely plain flat **magenta**
background — that is what lets me cut them out. No floor, no shadow, no scenery,
no second colour. Generate these at **1:1**.

**Backdrops** are the opposite: a full scene, no magenta, generated at **16:9**.
All backdrops are already done, so there are none left in this sheet.

## Already generated (do not repeat)

Creatures: wolf, goblin, spider, ogre, wraith, assassin-adjacent bosses, coven,
warden, warlord, spider queen, bog horror.
Classes: warrior, mage, archer, berserker.
Backdrops: all eight regions, the title screen, the world map, the battlefield.

---

""")

parts.append(section("1. Enemies", "The rest of the bestiary. **Highest priority** — these appear in every fight.",
                     ENEMIES, SPRITE_STYLE, "enemy"))
parts.append(section("2. Classes", "The four classes still missing a portrait. The character-creation screen shows all eight.",
                     CLASSES, SPRITE_STYLE, "class"))
parts.append(section("3. Races", "These fill the race picker on the character-creation screen.",
                     RACES, SPRITE_STYLE, "race"))
parts.append(section("4. Companions", "Optional — allies who join you.",
                     COMPANIONS, SPRITE_STYLE, "companion"))
parts.append(section("5. Items", "Small inventory icons. Optional — the game ships vector icons for these already.",
                     ITEMS, ICON_STYLE, "item"))
parts.append(section("6. Equipment", "Small inventory icons. Optional, and the largest batch.",
                     GEAR, ICON_STYLE, "gear"))
parts.append(section("7. Gems", "Small socket icons. Optional.",
                     {k: f"a cut {v} gemstone" for k, v in GEMS.items()}, ICON_STYLE, "gem"))

parts.append("""---

## Tips

- **Avoid the word "goblin"** — it trips the moderation filter. "Cave imp" or
  "small green creature" gets through fine (that is how yours was made).
- Keep the magenta **flat and unbroken**. If the model adds a gradient, a
  vignette or a second panel behind the character, send it anyway — I have a
  flag that keys out a second colour.
- If a character comes out with its feet cut off or off-centre, regenerate it;
  "full body, centered" in the prompt usually fixes it.
- Anything you generate that I have not asked for is still welcome — send it
  with a note about what it is and I will find a key for it.
""")

OUT.write_text("\n".join(parts), encoding="utf-8")
n = sum(len(t) for t in (ENEMIES, CLASSES, RACES, COMPANIONS, ITEMS, GEAR, GEMS))
print(f"Wrote {OUT} with {n} prompts")
