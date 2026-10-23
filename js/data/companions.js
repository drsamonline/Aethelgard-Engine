/* ============================================================
   RPG Engine — DATA: sample companions, NPCs, endless dungeon, endings
   A small generic sample. Replace with your own game's cast and story.
   ============================================================ */
"use strict";
window.Game = window.Game || {};

const COMPANIONS = [
  { id:"guard", name:"The Guard", emoji:"🛡️", role:"Guardian",
    desc:"A stoic ex-soldier who never left a comrade behind.",
    perk:"Intercepts blows and shields you each round.",
    atk:0.65, hpMult:1.5, def:8, behaviour:"guard", recruit:{ rep:{ town:15 } }, cost:{ gold:0 }, quip:"Stand behind me." },
  { id:"ranger", name:"The Ranger", emoji:"🏹", role:"Ranger",
    desc:"A scout who speaks more to beasts than to people.",
    perk:"Strikes a random enemy every round and marks it.",
    atk:1.0, hpMult:0.9, crit:0.15, behaviour:"strike", recruit:{ level:6 }, cost:{ gold:120 }, quip:"The wilds are watching." },
  { id:"healer", name:"The Healer", emoji:"✨", role:"Cleric",
    desc:"A wandering healer who follows the wounded wherever they go.",
    perk:"Heals you when you fall below half health.",
    atk:0.4, hpMult:1.1, behaviour:"heal", recruit:{ rep:{ town:40 } }, cost:{ gold:150 }, quip:"Hold still. This will sting." },
];

const NPCS = {
  town: [
    { id:"captain", name:"The Captain", emoji:"💂", lines:[
      "Keep your blade sharp. The wilds breed monsters.",
      "We need people like you." ],
      options:[ {label:"Ask for a rumour", action:"npcRumour"}, {label:"Ask for work", action:"npcBounty"}, {label:"Leave", action:"npcNone"} ] },
    { id:"smith", name:"The Smith", emoji:"🔨", lines:[
      "Bring me iron and I'll bring you steel.",
      "A weapon is only as good as the hand that swings it." ],
      options:[ {label:"Open the Forge", action:"npcForge"}, {label:"Enchant my gear", action:"npcEnchant"}, {label:"Leave", action:"npcNone"} ] },
    { id:"innkeep", name:"The Innkeep", emoji:"🍺", lines:[
      "Ale's warm, beds are warmer, and rumours are cheapest of all." ],
      options:[ {label:"Rest (25g)", action:"npcRest"}, {label:"Buy a rumour (15g)", action:"npcRumour"}, {label:"Leave", action:"npcNone"} ] },
  ],
  shrine: [
    { id:"priest", name:"The Priest", emoji:"🙏", lines:[
      "The light mends what steel cannot." ],
      options:[ {label:"Pray (40g)", action:"npcPray"}, {label:"Leave", action:"npcNone"} ] },
  ],
  wilds: [
    { id:"hermit", name:"The Hermit", emoji:"🧙", lines:[
      "I know the wilds' secrets. They cost herbs, not gold." ],
      options:[ {label:"Trade herbs for a secret", action:"npcHermit"}, {label:"Leave", action:"npcNone"} ] },
  ],
  camp: [
    { id:"fence", name:"The Fence", emoji:"🎭", lines:[
      "No names, no questions, no refunds." ],
      options:[ {label:"Trade contraband", action:"npcBlack"}, {label:"Leave", action:"npcNone"} ] },
  ],
};

const ENDLESS_MODS = {
  enraged:  { name:"Enraged",  emoji:"🔺", desc:"Enemies deal +25% damage.", atk:1.25 },
  armored:  { name:"Armoured", emoji:"🛡", desc:"Enemies have +40% defence.", def:1.4 },
  swarm:    { name:"Swarm",    emoji:"🐝", desc:"Extra enemies in every fight.", extra:1 },
  venomous: { name:"Venomous", emoji:"☠️", desc:"Every enemy hit can poison you.", onHit:"poison" },
  fog:      { name:"Choking Fog", emoji:"🌫️", desc:"Healing is halved.", healMult:0.5 },
  greedy:   { name:"Greedy",   emoji:"💰", desc:"Double gold, but tougher foes.", gold:2.0, atk:1.1 },
  cursed:   { name:"Cursed",   emoji:"⛓️", desc:"You cannot flee.", noFlee:true },
  elite:    { name:"Elite Ranks", emoji:"⭐", desc:"All enemies are elite.", allElite:true },
};
const ENDLESS_FLOOR_POOL = ["bat","spider","ghoul","harpy","wraith","golem","brigand","ogre","mage","wyvern","assassin"];

const ENDINGS = [
  { id:"warden_free",  name:"The Land Breathes", emoji:"🌅", when:{ flag:"ch3_choice=free" },
    text:"You shattered the Guardian's seal and walked away from its power. The town's bells ring for a hero who wanted nothing in return." },
  { id:"warden_claim", name:"The New Colossus",  emoji:"🗿", when:{ flag:"ch3_choice=claim" },
    text:"You took the Guardian's strength into yourself. The land is safe — but something ancient now looks out through your eyes." },
  { id:"legend",       name:"A Story of Your Own", emoji:"⭐", when:{},
    text:"You were nothing when you arrived. Now the bards argue over which of your deeds to sing first. The land is yours, and so is the story." },
];

Object.assign(window.Game, { COMPANIONS, NPCS, ENDLESS_MODS, ENDLESS_FLOOR_POOL, ENDINGS });
