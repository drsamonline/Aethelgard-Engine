/* ============================================================
   RPG Engine — DATA: sample story chapters and side quests
   A small generic sample. Replace with your own game's story.
   ============================================================ */
"use strict";
window.Game = window.Game || {};

/* Each chapter: an objective, then a CHOICE that shapes the story.
   Choices set flags, change rewards/reputation, and unlock side quests. */
const CHAPTERS = [
  { id:1, title:"Chapter I — First Steps",
    text:"You arrive in Town with nothing. Beasts have been seen on the edge of the Wilds.",
    objective:{ type:"kill", target:"beast", required:1, label:"Defeat a Beast" },
    rewards:{ gold:60, xp:80 }, unlocks:["The Wilds explored"],
    prepare:["Equip your starting weapon","Buy a potion if you can"],
    choices:[
      { label:"Drive them back", outcome:"You clear the road. The town takes note.", effects:{ flags:{ ch1_choice:"push" }, rep:{ town:8 }, xp:20, unlockSide:["sq_hunt"] } },
      { label:"Study them first", outcome:"You learn their habits before you strike.", effects:{ flags:{ ch1_choice:"study" }, rep:{ town:3 }, gold:20 } },
    ] },
  { id:2, title:"Chapter II — Into the Caves",
    text:"Something is stirring below. Descend into the Caves and see how deep it goes.",
    objective:{ type:"depth", target:"caves", required:3, label:"Reach Depth 3 of the Caves" },
    rewards:{ gold:130, xp:200 }, unlocks:["The Peaks revealed","Sunken Ruins rumoured"],
    prepare:["Bring energy for the descent","Bats drain life — kill them fast"],
    choices:[
      { label:"Seal the deep tunnels", outcome:"Safer roads, fewer riches.", effects:{ flags:{ ch2_choice:"seal" }, rep:{ town:10 }, unlockSide:["sq_deep"] } },
      { label:"Leave them open", outcome:"The dark promises treasure and danger alike.", effects:{ flags:{ ch2_choice:"open" }, xp:40 } },
    ] },
  { id:3, title:"Chapter III — The Guardian",
    text:"An old guardian wakes beneath the Ruins. End it, and the land is free.",
    objective:{ type:"kill", target:"warden", required:1, label:"Defeat the Guardian" },
    rewards:{ gold:400, xp:600 }, unlocks:["Open World","Endless bounties"],
    prepare:["It resists Physical — bring Ice","Full HP and potions before you go"],
    choices:[
      { label:"Claim its power", outcome:"Its strength flows into you — and a burden with it.", effects:{ flags:{ ch3_choice:"claim" }, xp:200 } },
      { label:"Shatter it and walk away", outcome:"You break the seal forever. The land breathes.", effects:{ flags:{ ch3_choice:"free" }, rep:{ town:30 }, gold:200 } },
    ] },
  { id:4, title:"Open World",
    text:"The land is quiet again. Roam freely: take bounties, grow your settlement, and write your own legend.",
    objective:null, rewards:null, unlocks:[], prepare:[] },
];

const SIDE_QUESTS = [
  { id:"sq_hunt", name:"Pest Control", desc:"The town wants the beasts thinned: defeat 4 beasts.", objective:{ type:"kill", target:"beast", required:4 }, rewards:{ gold:90, xp:100 }, unlocks:["Hunter's standing"], unlock:{ chapter:2 }, prepare:["Hunt them from the Atlas","Carry a potion"] },
  { id:"sq_deep", name:"Deeper Still", desc:"Reach Depth 5 of the Caves.", objective:{ type:"depth", target:"caves", required:5 }, rewards:{ gold:200, xp:220, items:{ ruby:1 } }, unlocks:["Deep loot tier"], unlock:{ chapter:2 }, prepare:["Each descent costs energy","Bank depth by leaving and re-entering"] },
];

const BOUNTY_POOL = ["beast","imp","spider","brigand","ogre","mage","wraith","harpy","ghoul"];

Object.assign(window.Game, { CHAPTERS, SIDE_QUESTS, BOUNTY_POOL });
