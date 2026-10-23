/* ============================================================
   Aethelgard — DATA: non-combat activities
   Created by Dr. Sohil Momin
   ============================================================ */
"use strict";
window.Game = window.Game || {};

const ACTIVITIES = {
  fishing:  { name:"Fishing",      emoji:"🎣", zone:"wilds",       cost:{ energy:8 },  desc:"Cast a line in the shallows for fish." },
  foraging: { name:"Foraging",     emoji:"🌿", zone:"wilds",       cost:{ energy:6 },  desc:"Search the undergrowth for herbs." },
  farming:  { name:"Farming",      emoji:"🌾", zone:"town",   cost:{ energy:5 },  desc:"Tend your fields for food and coin." },
  gambling: { name:"Dice Den",     emoji:"🎲", zone:"town",   cost:{ gold:20 },   desc:"Wager gold on a roll of the bones." },
  arena:    { name:"The Arena",    emoji:"🏟️", zone:"town",   cost:{ energy:15 }, desc:"Fight waves of foes for glory and gold." },
  cooking:  { name:"Cooking",      emoji:"🍳", zone:"town",   cost:{ energy:4 },  desc:"Turn fish and food into hearty meals." },
  tavern:   { name:"Tavern Rumours",emoji:"🍺",zone:"town",   cost:{ gold:15 },   desc:"Buy a round and learn something useful." },
  bounty:   { name:"Bounty Board", emoji:"📜", zone:"town",   cost:{},            desc:"Take on paid bounties for coin and renown." },
  mining:   { name:"Mining",       emoji:"⛏️", zone:"peaks",  cost:{ energy:8 },  desc:"Break ore from the The Peaks." },
  prospect: { name:"Prospecting",  emoji:"💠", zone:"peaks",  cost:{ energy:12 }, desc:"Search for gems in the deep seams." },
  woodcut:  { name:"Woodcutting",  emoji:"🪵", zone:"wilds",       cost:{ energy:5 },  desc:"Fell timber for building and crafting." },
  pray:     { name:"Pray",         emoji:"🙏", zone:"shrine",     cost:{ gold:40 },   desc:"Offer gold for a full restoration." },
};

const ARENA_WAVES = [
  { name:"Novice Bracket",  enemies:["rat","rat"],           reward:{ gold:40, xp:40 } },
  { name:"Soldier Bracket", enemies:["imp","beast"],       reward:{ gold:70, xp:70 } },
  { name:"Veteran Bracket", enemies:["brigand","spider"],     reward:{ gold:110, xp:120 } },
  { name:"Champion Bracket",enemies:["ogre","harpy"],        reward:{ gold:180, xp:200 } },
  { name:"Grand Champion",  enemies:["wyvern","assassin"],   reward:{ gold:300, xp:350 } },
];

const TAVERN_RUMOURS = [
  "They say the Cult Leader fears fire above all else.",
  "A merchant near the Ruins sells relics cheap if you know the password.",
  "The the Guardian's plates crack under ice — a mage's trick.",
  "Spider venom can be cured with a simple antidote of herb and leather.",
  "Brigands never attack anyone with a full purse and an empty head — carry less.",
  "The Arena pays double if you never flee a wave.",
  "There's a hidden strongbox beneath the old shrine in the Wilds.",
  "Night makes monsters bolder — and loot richer.",
  "Ogres telegraph their crushing blow. Guard, then strike.",
  "The fence in the Underworld buys relics for a hundred and more.",
];

Object.assign(window.Game, { ACTIVITIES, ARENA_WAVES, TAVERN_RUMOURS });
