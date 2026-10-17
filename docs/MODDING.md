# Modding

The full guide lives next to the mods themselves, because that is where you will
be working:

**→ [`mods/README.md`](../mods/README.md)**

It covers the mod format, the folder layout, every field a mod can set, the
compatibility system, how to declare a game mode, how to ship art, and how to
test what you wrote.

## The short version

A mod is one JavaScript file that pushes an object onto `window.AETHELGARD_MODS`:

```js
window.AETHELGARD_MODS = window.AETHELGARD_MODS || [];

window.AETHELGARD_MODS.push({
  id: "my-mod",
  name: "My Mod",
  version: "1.0.0",
  author: "You",
  description: "What it does.",
  impact: "additive",            // additive | story | overhaul

  ENEMIES: { ... },
  ITEMS:   { ... },
});
```

Drop the file in `mods/`, reload, and it is discovered automatically.

## Impact tiers

| tier | applies |
|---|---|
| `additive` | immediately — new content alongside the existing game |
| `story` | on restart — changes the narrative |
| `overhaul` | on restart — changes the game itself |

Story and overhaul mods never apply mid-session, so they cannot corrupt a run
you are in the middle of.

## What a mod can replace

Tables merge by key, so a mod can **add** to the game or **replace** an existing
entry by using the same key. That covers both minor upgrades and full overhauls.

## Nine worked examples ship with the game

`example-mod.js`, `example-addon.js`, `example-class.js`, `story-expansion.js`,
`villain-arc.js`, `example-graphics/`, `overhaul-vector/` and the two art packs.
Read those before writing your own — between them they demonstrate every
feature of the format.
