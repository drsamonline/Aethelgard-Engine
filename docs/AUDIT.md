# Audit report

A full pass over the engine and the content, run against the shipped build.

## 1. Static analysis

| | |
|---|---|
| JS files | **50** |
| Lines of engine + mod code | **7,254** |
| Functions defined | **447** |
| Duplicate definitions | **0** |
| Missing script files | **0** |
| Files that fail to parse | **0** |

Two functions are reported as unreferenced and both are deliberate:
`setLang` is the hook a mod uses to add a language, and
`reportContentValidation` is a console helper. Everything else is reachable.

The four apparent duplicates are local `const`s that share a name in separate
IIFEs (`list`, `row`, `s`, `activeMode`) — not real collisions.

## 2. API surface

Every one of the **383** functions on `window.Game` was called and classified:

| outcome | count |
|---|---|
| called cleanly | 303 |
| wanted an argument (expected) | 33 |
| skipped by design (navigate / prompt / wipe) | 38 |
| threw | 0 |
| hung | 0 |

An early run reported five throws and four hangs. Both turned out to be
artefacts of the harness, not defects — but one was worth fixing anyway:

- The five "throws" were volume setters called with no argument. A `NaN` volume
  flows into a Web Audio `AudioParam`, which rejects it. **Fixed**: volume is now
  clamped to 0–1 at both the setter and the audio layer, so no value can break it.
- The four "hangs" were one blocked native `confirm()` in `ascend()`. With a
  dialog handler all four return in under 3 ms. No real hang.

## 3. Twelve simulations

| # | simulation | result |
|---|---|---|
| 1 | Chronicles campaign, start to Open World | **PASS** — reached chapter 9 |
| 2 | Villain campaign, start to Open World | **PASS** — reached chapter 5 |
| 3 | Mode isolation | **PASS** — villain loads 0 hero enemies; hero campaign gets 0 villain chapters |
| 4 | Endless dungeon | **PASS** — descended, no errors |
| 5 | Economy: gather → sell → buy | **PASS** — gold and items move correctly |
| 6 | Settlement + underworld | **PASS** — 7 structures, crime and heist resolve |
| 7 | Companions | **PASS** — 5 recruited, dismissed cleanly |
| 8 | Achievements | **PASS** — unlocked and persisted |
| 9 | Save / export / import | **PASS** — round-trips exactly |
| 10 | Mod toggling | **PASS** — dependency cascade correct; story mods refuse mid-session |
| 11 | Ascension | **PASS** — permanent bonuses applied, run resets |
| 12 | Mobile + 120-tick soak | **PASS** — 11/11 tabs, no DOM leak, no overflow |

## 4. Bugs found and fixed

| bug | fix |
|---|---|
| Volume setter threw on a `NaN` or out-of-range value | clamped to 0–1 at both layers |
| `unlockAchievement` only took an object; an id produced a toast reading "undefined" | accepts either |

Everything else that looked like a fault was the harness being wrong, and in each
case the game was behaving correctly:

- companions correctly refuse to join without the declared reputation or flags
- disabling a mod correctly removes the mods that `requiresMods` it
- a `story`-impact mod correctly refuses to change the game mid-session
- `confirm()` in a headless browser blocks until a dialog handler is attached

## 5. Reproducing this

```bash
node tools/verify.js          # end-to-end: tabs, actions, combat, save, both campaigns
node tools/sims.js 1 12       # the twelve simulations
python3 tools/static-audit.py # functions, dead code, duplicates, wiring
node test6.js && node test7.js && node test8.js
```

Content validation is also in-game: **Settings → Diagnostics → Run content check**.
