# Troubleshooting

## The game shows a screen saying "The game files did not load"

The `js/` folder is missing. This almost always means `index.html` was opened
from **inside** a zip viewer — most tools unpack only the single file you
double-clicked.

**Fix:** right-click the zip → *Extract All* (Windows) or *Extract Here* (Mac),
then open `index.html` from inside the extracted folder. You should see
`index.html` next to folders named `js`, `mods` and `icons`.

## It loads but nothing happens when I click

Two things to check:

1. **Give it a second.** The title screen appears before the save slots are
   ready. Empty slots read *Loading saves…* until they are.
2. **Do a hard refresh** — `Ctrl+F5`, or `Cmd+Shift+R` on Mac. An older version
   can be served from the offline cache; the hard refresh clears it.

If it still does nothing, open **Settings → Diagnostics** and copy the report.

## It is stuck on an old version

The service worker caches the app shell. A new version takes over on your next
visit, and if an update is ready the game shows a small **Update ready — reload**
chip in the corner. Press it, or hard-refresh once.

## My progress disappeared

Saves are written to your browser's `localStorage`, which is per-browser and
per-profile. Progress will not follow you between browsers or devices, and it is
cleared if you clear site data, or if you play in a private window.

Use **Export slot** on the title screen to keep a real file you can move around.

## "Could not save — browser storage is full or blocked"

`localStorage` is full or disabled. Private/incognito windows often block it.
Free some space, or leave private browsing, then reload.

## A mod broke the game

Turn on **Safe mode** in **Settings → Mods**, which loads the game with no mods
at all. Then re-enable them one at a time to find the culprit.

The Mods panel already tells you which mods work together and which clash, and
it will refuse to load a mod that conflicts with another.

## Something else

Open **Settings → Diagnostics**. It lists the version, the mode, how many mods
are loaded, the storage state, your viewport and any errors captured this
session — each with a plain-English explanation of what it means and what to do.

Press **Copy report** and include it in a bug report. That single block answers
most of the questions anyone would otherwise have to ask you.
