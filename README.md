<div align="center">

# ⚔️ Aethelgard: Chronicles of Fate

**A deep, single-player, text-based fantasy RPG for the browser.**

Classes, races, a branching story, crafting, settlement building, an underworld of crime, and a wiki you can hover.
Built entirely with vanilla HTML, CSS and JavaScript — **no server, no build step, no dependencies, fully offline.**

[![Play Now](https://img.shields.io/badge/▶_PLAY_NOW-aethelgardplay.netlify.app-8B5CF6?style=for-the-badge&logo=netlify&logoColor=white)](https://aethelgardplay.netlify.app/)

[![Version](https://img.shields.io/badge/version-game%20v7%20·%20changelog%201.0.4-blue?style=flat-square)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/code-MIT-green?style=flat-square)](LICENSE)
[![Art License](https://img.shields.io/badge/art-©_reserved-orange?style=flat-square)](LICENSE-ASSETS.md)
[![JavaScript](https://img.shields.io/badge/JavaScript-vanilla_ES5--ish-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](#the-files-are-deliberately-kept-separate)
[![No Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen?style=flat-square)](#play-it)
[![No Build Step](https://img.shields.io/badge/build_step-none-informational?style=flat-square)](#play-it)
[![PWA Ready](https://img.shields.io/badge/PWA-installable%20%2B%20offline-blueviolet?style=flat-square&logo=pwa&logoColor=white)](#install-as-an-app-optional)
[![Languages Shipped](https://img.shields.io/badge/interface-English-red?style=flat-square)](#languages)
[![Mods Supported](https://img.shields.io/badge/mods-drop--in%20JS%20files-yellow?style=flat-square)](mods/README.md)
[![Offline First](https://img.shields.io/badge/offline-first-success?style=flat-square)](#play-it)
[![Mobile Friendly](https://img.shields.io/badge/mobile-responsive-lightgrey?style=flat-square)](#play-it)

*Created by [Dr. Sohil Momin](#credits).*

</div>

---

## 🎮 Table of contents

- [Play it](#-play-it) · [Game modes](#-game-modes) · [Story mods](#-two-extra-games-ship-as-mods) · [Languages](#-languages)
- [What's in this repo](#-whats-in-this-repo) · [File map](#-the-files-are-deliberately-kept-separate)
- [Features](#-features) · [Modding](#-adding-content-mods) · [Documentation](#-documentation) · [Development & testing](#-development--testing) · [Credits](#-credits)

---

## ▶️ Play it

**Live game → https://aethelgardplay.netlify.app/**

Or run it locally:

1. **Extract the whole folder first**, then open `index.html` from inside it — do **not**
   open `index.html` from inside a zip viewer, or the `js/` folder will be missing and the
   game cannot start. Full steps are at the top of [`HOW_TO_PLAY.md`](HOW_TO_PLAY.md).
2. Open `index.html` in any modern browser (Chrome, Edge, Firefox, Safari — desktop or mobile).
3. Choose a save slot, then create your hero.

### 📱 Install as an app (optional)
When served over `http://` or `https://` (any static host, or `python3 -m http.server`), the game registers a service worker and installs to your home screen with its own icon and full offline support.

---

## 🕹️ Game modes

The title screen has a **Game** row. **Chronicles** is the original campaign.
A mod can declare a second mode — **The Crown's Shadow** (the villain arc) is
one — and then the two play as genuinely separate games:

- the hero classes are **hidden** in villain mode; only the five villains are offered
- the villain campaign **replaces** chapters 1–5, so the storyline is different throughout
- **saves are kept apart**: slot 1 in Chronicles and slot 1 in the villain game are different characters, and neither game can load the other's
- switching mode reloads the page, because different content is loaded

Add a third game by writing a mod that declares a `MODE` — see [`mods/README.md`](mods/README.md).

## 🧩 Two extra games ship as mods

- **`story-expansion.js` — The Hollow Crown.** Three chapters continuing the campaign after Chapter V, two new regions, three new foes and a four-part side chain. If you have already finished the story it picks you up **exactly where you left off**, with your hero, level, gear and gold intact.
- **`villain-arc.js` — The Crown's Shadow.** A complete reversal: you play as one of the five bosses (Coven Leader, Iron Warden, Bandit Warlord, Spider Queen, Bog Horror), the eight hero classes become your enemies, and a five-chapter campaign is told from the other side. Same art, other side of the blade.

Both are toggled in Settings or on the title screen and apply on restart. Each ships its own art, in `mods/story-expansion/sprites/` and `mods/villain-arc/sprites/`. The villain arc adds the separate **game mode** described above.

## 🌐 Languages

The interface ships in **English**. The translation mechanism is deliberately generic: every table carries stable keys, and a mod can add another language by shipping an `I18N` table and calling `Game.setLang()` — see [`mods/README.md`](mods/README.md).

---

## 📦 What's in this repo

| Folder | Contents |
|---|---|
| 🖼️ **`screenshots/`** | twenty-four captures of the finished game (title, creation, story, all tabs, combat, settings, diagnostics, villain mode and mobile). |
| 📣 **`posters/`** | seventeen Instagram-ready 1080×1350 posters built from the character art, generated by `tools/make-instagram-posters.py`. |
| 🎨 **`mods/ai-art/`** | the illustrated art pack (142 sprites), selectable at the start of a new game. |
| 📝 **`AI_ART_PROMPTS.md`** | copy-paste prompts for the creatures, classes, items and gear. |
| 📝 **`MOD_ART_PROMPTS.md`** | prompts for the art the two story mods use. |
| 📝 **`ICON_PROMPTS_*.md`** | six sheets of icon prompts, one per group: skills, statuses, buildings, gear sets, points of interest, achievements. |
| 📚 **`docs/`** | architecture, modding, save format, troubleshooting and the engine audit report. |
| 🔍 **`AUDIT_REPORT.md`** | the latest full repository audit: findings, evidence and suggested fixes. |

---

## 🗂️ The files are deliberately kept separate

The engine is split into small modules so it loads fast, is easy to debug, and can be extended with addons and mods. There is **no single-file bundle**.

```
index.html            App shell, icons, layout, all modals
style.css             All styling, responsive layout, themes, animation
manifest.json         PWA manifest
sw.js                 Service worker (offline cache)
icons/                App icons

js/data/              Pure data — safe to edit or extend
  gamedata.js           elements, statuses, rarities, affixes, difficulty, items, buildings, locations
  races.js              8 playable races + genders
  classes.js            8 classes, their skills, and their mission lines
  enemies.js            the bestiary — 20 core enemies and world bosses (mods add more)
  gear.js               weapons, armour, offhand, rings, amulets + recipes
  quests.js             the 5 branching story chapters, 16 side quests, bounties
  events.js             travel events + spontaneous in-game events
  activities.js         non-combat activities, arena waves, tavern rumours
  achievements.js       39 achievements
  companions.js         recruitable allies
  gems.js / music.js / reactions.js   gem upgrades, soundtrack data, combat quips
  wiki.js               80+ hand-written wiki entries, extended automatically from the data above
  i18n.js               English interface strings (mod-extensible key table)

js/                   Logic
  core.js               state, saves, tick, day/night, stats, audio, effects, notifications, settings
  combat.js             statuses, enemy abilities, class skills, multi-enemy, loot
  world.js              travel, local maps, economy, crafting, settlement, underworld, activities, events
  quests.js             quest engine, chapters, choices, unlocks, failure help
  maps.js               world map + local region maps
  wiki.js               hover tooltips + the wiki tab
  ui.js                 all tabs, character creation, inventory, codex, settings
  graphics.js           the single sprite-drawing function every art pack hooks into
  music.js              procedural soundtrack
  mods.js               mod discovery, toggling, compatibility checks
  companions.js         companion recruitment and follow logic
  late-game.js          endless dungeon, ascension, raids
  validate.js / diagnostics.js   content validator + in-game diagnostics
  boot.js               startup

js/views/             One file per tab (story, hero, skills, atlas, home, forge, market,
                      underworld, inventory, codex)

mods/                 Drop-in content — see mods/README.md
docs/                 Architecture · Modding · Save format · Troubleshooting · Audit
tools/                Static audit, end-to-end verifier, twelve simulations, art importers
```

### ➕ Adding content (mods)
- New enemy: add an entry to `js/data/enemies.js` and a spawn point in `js/world.js`.
- New class: add to `js/data/classes.js` (perks + skills + missions).
- New quest: add to `js/data/quests.js`; unlocks are declarative (`chapter`, `flag`, `level`, `cls`).
- New wiki entry: add to `js/data/wiki.js`, then use `data-wiki="your_key"` anywhere.
- Or drop a `.js` file in `mods/` — nothing in `js/` needs to change. See **[mods/README.md](mods/README.md)**.

---

## ✨ Features

### 🧙 Character
- **8 races** (Human, Elf, Dwarf, Orc, Halfling, Tiefling, Beastkin, Revenant) each with real perks.
- **8 classes** (Berserker, Warrior, Defender, Archer, Thief, Swordmaster, Duel Wielder, Mage) with unique skills and their own mission lines.
- Three genders, a name, and a class chosen at the very start.

### ⚔️ Combat
- Turn-based, one *or several* enemies, tap to target.
- Four attributes; crits, defence, lifesteal, double strikes.
- Six elements, and a bestiary of 20 core enemies and world bosses with resistances and weaknesses.
- Status effects: bleed, poison, burn, stun, weaken, ward, rage, regen, focus, mark.
- Telegraphed enemy attacks, so Defend matters.
- Active skills across the classes, with cooldowns and energy costs.
- Multiple world bosses plus the five arc bosses of villain mode.

### 📜 Story & quests
- A 5-chapter main storyline that ends with a **choice in every chapter** — different choices unlock different side quests, reputation and outcomes, so the game plays differently each run.
- **16 side quests** unlocked as the story progresses, plus class missions and endless bounties.
- Every quest shows its **objectives, rewards and what it unlocks**.
- **Failure help**: after you fail a mission, a note explains how to prepare for the next attempt.

### 🗺️ World
- A visual **world map** and per-region **local maps** with clickable points of interest.
- **7 regions**, random travel events, and **spontaneous in-game events** with big rewards.
- A day/night cycle that changes enemies and prices.
- Faction reputation with Oakhaven, the Coven and the Bandits.

### 🎣 Beyond fighting
- Fishing, foraging, farming, cooking, gambling, the Arena, tavern rumours, mining, prospecting and woodcutting.
- A live market, a black market, and a settlement you grow with 7 building types and settlers.

### 🕵️ The Underworld
- Nerve-powered crime: pickpocketing, lockpicking, heists, guild jobs, a Heat system, and a fence.

### 🔌 Mods
- Drop a `.js` file in `mods/` and the game finds it automatically. Toggle each mod on or off in Settings or on the new-game screen.
- Content mods apply instantly; **story and overhaul mods only load on a fresh start**, so a running save is never reshaped underneath you.
- **Safe mode** (Settings, or `?safe=1`) runs the game with no mods at all.
- **Graphics packs**: the whole game draws its art through one function, so an art overhaul is drop-in. Two packs ship — **Flat Icons** (59 PNG pictograms) and **Chronicles Vector** (102 illustrated SVG models) — pick one in **Settings → Graphics pack**. Anything a pack doesn't cover keeps its emoji, so partial packs work.
- **Compatibility checking**: the Mods panel tells you which mods work together (✓), which merely overlap (⚠), and which cannot load (✗, with the reason) — and blocks only the broken ones.
- See **[mods/README.md](mods/README.md)** for the full format and worked examples.

### 🏆 Meta
- **Notifications** for events, quests, unlocks, upgrades and achievements, with a bell and a history panel.
- **Hover tooltips** on nearly everything, and a searchable **Wiki** tab with 80+ hand-written entries plus auto-generated pages for every enemy, item and skill (both toggleable).
- **39 achievements**, a statistics page, and Ascension (New Game+).
- 3 save slots, export/import, and autosave.
- A contextual **Hints** panel that reads your situation and tells you what to do next.
- Keyboard shortcuts: **Esc** closes any overlay, **1–9** switch tabs.
- Settings: theme (4), difficulty (4), text size, sound + volume, music + volume, mods, tooltips, notifications, damage numbers, screen shake, autosave, auto-battle, reduced motion, compact layout, colourblind mode, dyslexia-friendly font and high-contrast colours.

---

## 📚 Documentation

| Document | Read it when… |
|---|---|
| [HOW_TO_PLAY.md](HOW_TO_PLAY.md) | you just downloaded the game. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | you want to understand how the engine fits together. |
| [docs/MODDING.md](docs/MODDING.md) → [mods/README.md](mods/README.md) | you want to write a mod. |
| [docs/SAVE-FORMAT.md](docs/SAVE-FORMAT.md) | you want to inspect or migrate saves. |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | something looks broken. |
| [docs/AUDIT.md](docs/AUDIT.md) | you want the deep engine test results. |
| [AUDIT_REPORT.md](AUDIT_REPORT.md) | you want the current repo-wide audit and suggested fixes. |
| [CHANGELOG.md](CHANGELOG.md) | you want to know what changed lately. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | you want to help. |

## 🧪 Development & testing

Everything runs with plain Node/Python — there is nothing to install:

```bash
node --check js/core.js            # any single file
node test6.js && node test7.js && node test8.js   # unit suites
node tools/verify.js               # end-to-end: tabs, actions, combat, save, both campaigns
node tools/sims.js 1 12            # the twelve gameplay simulations
node js/validate.js                # content validator — or in-game: Settings → Diagnostics → Run content check
python3 tools/static-audit.py .    # functions, dead code, duplicates, wiring (note the dot!)
```

Content validation is also in-game: **Settings → Diagnostics → Run content check**.

CI (`.github/workflows/ci.yml`) runs the syntax check, JSON validation and the three test suites on every push and pull request.

---

## 🙏 Credits

Designed and developed by **Dr. Sohil Momin**.

Built with vanilla JavaScript. Core art is emoji and inline SVG — no external assets, so it works fully offline. Illustrated packs ship as optional mods ([art licence](LICENSE-ASSETS.md)); the engine is [MIT](LICENSE).

<div align="center">

*If Aethelgard entertains you, star the repo ⭐ — it helps other adventurers find it.*

</div>
