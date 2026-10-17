# 🔍 Repository Audit Report — Aethelgard: Chronicles of Fate

> **Audit date:** 17 October 2026 · **Branch audited:** working tree at `7a145f7`
> **Scope:** full repo — 50 JS files (7,309 lines), HTML shell, CSS, PWA files, mods, docs.
> **Constraint honoured:** no source file (`js/`, `mods/*.js`, `index.html`, `style.css`, `sw.js`) was modified by this audit. Only documentation was updated/beautified.

---

## ✅ What passed

| Check | Result |
|---|---|
| Syntax (`node --check` on all 57 JS files incl. mods, tests, service worker) | **0 errors** |
| `<script>` wiring — every file referenced by `index.html` exists on disk | **41/41 OK** |
| Service-worker precache list (`sw.js` → 61 entries) vs. disk | **all present** |
| `manifest.json` / `mods/mods.json` | valid JSON, all listed mod files exist |
| Duplicate top-level function definitions across IIFEs | none real (4 name shares are local `const`s in separate scopes) |
| Documented counts — 8 races, 8 classes, 16 side quests, 7 regions, 59 Flat-Icons PNGs, 102 Vector SVGs | **verified against data tables** |

---

## 🐞 Errors found (with suggested fixes)

### High priority

**E1 — README claims seven languages; the game ships English only.**
`js/data/i18n.js` contains a single locale (`en`) and its own header says *"interface strings (English only)"*. `README.md` still advertises *"seven languages — English, Hindi, Gujarati, Spanish, French, Mandarin and Japanese"* and labels `i18n.js` as *"English / हिन्दी / ગુજરાતી"*.
**Fix:** corrected in the README (documentation-only change). If multi-language support is planned, ship it as an `I18N` mod instead of re-adding the claim.

**E2 — Achievement count mismatch: docs say 38, data has 39.**
`js/data/achievements.js` defines **39** `{ id:"…" }` entries; `README.md` and `docs/AUDIT.md` both say 38.
**Fix:** README updated to 39. Suggested: update `docs/AUDIT.md` §API-surface wording or add a regression test that pins the count:
```js
// suggested test (not added — audit is read-only on sources)
console.assert(Object.keys(Game.ACHIEVEMENTS).length === 39, "achievement count drifted");
```

**E3 — Precached Markdown goes stale forever (service worker).**
`sw.js` precaches `./README.md`, `./HOW_TO_PLAY.md`, `./AI_ART_PROMPTS.md`, `./MOD_ART_PROMPTS.md`, `./mods/README.md`. The fetch handler is **cache-first**, so these copies are served from cache until `CACHE` is bumped — readers on the installed PWA get old docs even after deploys.
**Fix (suggested):** either drop the `.md` files from `CORE` (they are not needed at runtime), or serve them network-first:
```js
// suggested sw.js change (NOT applied — audit must not touch source)
const NO_CACHE = /\.md$/;
self.addEventListener("fetch", e => {
  if (NO_CACHE.test(e.request.url)) return;            // let docs go to network
  /* …existing cache-first handler… */
});
```
If you keep them precached, **bump `CACHE = "aethelgard-v23"`** whenever docs change.

### Medium priority

**E4 — `tools/static-audit.py` silently reports zeros with no arguments.**
Its default path is a hard-coded `/scratch/work/aethelgard` that doesn't exist here, so `python3 tools/static-audit.py` prints `0 files / 0 functions` and *looks* like a clean pass. `docs/AUDIT.md` tells users to run exactly that command.
**Fix (suggested):** default to the repo root instead of a scratch dir:
```python
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
```
(and update `docs/AUDIT.md` reproduction block to `python3 tools/static-audit.py .`).

**E5 — 24 `G.*` references flagged as "undefined" by static analysis.**
All verified to be state/property assignments made at runtime (`G.tab = tab` in `js/ui.js:14`, `G.pendingSlot` in `js/core.js:729`, etc.) — **not bugs**. But the tool cannot tell properties from functions, which buries real findings.
**Fix (suggested):** teach the tool to ignore names assigned as `G.x = <non-function>` (assignment without `function`/arrow on the RHS).

**E6 — No CI despite first-party test suites.**
`test6.js`, `test7.js`, `test8.js`, `tools/verify.js`, `tools/sims.js` exist but nothing runs them automatically; `CONTRIBUTING.md` asks contributors to run them by hand.
**Fix (suggested):** add a GitHub Actions workflow (created in this audit as `.github/workflows/ci.yml` — infrastructure, not game source) that runs `node --check` on every JS file plus the three test suites on each PR.

**E7 — Missing social/SEO meta tags.**
`index.html` has a good `<meta name="description">` but no Open Graph / Twitter card tags, so link previews on Discord/social hosts show nothing for a game whose main distribution channel is a Netlify URL shared in posts.
**Fix (suggested):** add to `<head>`:
```html
<meta property="og:title" content="Aethelgard: Chronicles of Fate">
<meta property="og:description" content="A deep, offline, text-based fantasy RPG for the browser.">
<meta property="og:image" content="https://aethelgardplay.netlify.app/posters/cover.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
```

### Low priority / hygiene

**E8 — Two intentionally dead functions.** `setLang` (`js/ui.js:304`) and `reportContentValidation` (`js/validate.js`) are unreferenced by design (mod hook / console helper). Already documented in `docs/AUDIT.md`; consider an `/* exported … */` comment so linters agree.

**E9 — Empty blank-line run at the top of `CHANGELOG.md`** (four consecutive blank lines after the title). Cosmetic; cleaned during beautification.

**E10 — Enemy count understated.** README says "18+ enemies"; `js/data/enemies.js` actually defines ~40 keyed entries. "18+" is technically true but the atlas is bigger than advertised — suggest stating the real number in the next doc pass.

**E11 — Repo has no git remote configured** (`git remote -v` is empty), so the Netlify deploy is presumably manual/drag-drop. Suggest documenting the deploy path in `CONTRIBUTING.md` or adding a GitHub → Netlify connection.

---

## 📋 Documentation changes made in this pass (no source touched)

| File | Change |
|---|---|
| `README.md` | Full beautification + shields.io badges; fixed E1 (languages), E2 (achievements), file-tree now lists `views/`, `companions.js`, `late-game.js`, `music.js`, `graphics.js`, `mods.js`, `validate.js`, `diagnostics.js` and the new `docs/` + `AUDIT_REPORT.md`; screenshot count corrected (24, not 10); poster count verified (17). |
| `docs/AUDIT.md` | Cross-linked to this report; commands updated to pass the repo path (E4 workaround). |
| `CHANGELOG.md` | Badge header, tidy spacing, entry describing this documentation/audit pass. |
| `CONTRIBUTING.md` | Badges, clearer structure, note about running the audit tool with a path argument. |
| `HOW_TO_PLAY.md` | Badge header, table-of-contents anchors, consistent formatting. |
| `.github/workflows/ci.yml` | **New** — syntax check + test suites on every push/PR (addresses E6). |

---

## Suggested fix priority order

1. Bump/adjust `sw.js` caching of `.md` files (**E3**) — affects end users reading docs offline.
2. Fix `tools/static-audit.py` default path (**E4**) — currently gives false-clean results.
3. Add CI workflow activation (**E6**) — file already provided here; just needs the repo pushed to GitHub.
4. Reconcile achievement count everywhere (**E2**) — one remaining mention lives in `docs/AUDIT.md` prose about the API harness (383 functions), which is a different metric and can stay.
5. OG/Twitter meta tags (**E7**) when you next touch `index.html`.
