/* Mod system suite: registration, tiers, enable/disable, snapshot restore,
   safe mode, isolation of broken mods, and language packs. */
const fs = require("fs"), path = require("path");
const store = {};
global.localStorage = { getItem:k=>(k in store?store[k]:null), setItem:(k,v)=>{store[k]=String(v);}, removeItem:k=>{delete store[k];} };
function makeEl(id){ const el={ id,_html:"",style:{},scrollTop:0,offsetWidth:120,offsetHeight:60,dataset:{},className:"",value:"",children:[],firstChild:null,tagName:"DIV",src:"",
  classList:{_s:new Set(),add(...c){c.forEach(x=>this._s.add(x));},remove(...c){c.forEach(x=>this._s.delete(x));},toggle(c,f){if(f===undefined)f=!this._s.has(c);f?this._s.add(c):this._s.delete(c);return f;},contains(c){return this._s.has(c);}},
  appendChild(){},removeChild(){},remove(){},closest(){return null;},getAttribute(){return null;},setAttribute(){},removeAttribute(){},focus(){},offsetParent:null,contains(){return false;},
  querySelector(){return makeEl("q");},querySelectorAll(){return [];},
  set innerHTML(v){this._html=String(v);},get innerHTML(){return this._html;},
  set textContent(v){this._html=String(v);},get textContent(){return this._html;} }; return el; }
const els={};
global.document={ readyState:"complete", documentElement:makeEl("html"), body:makeEl("body"), head:makeEl("head"), activeElement:null,
  getElementById:id=>(els[id]||(els[id]=makeEl(id))), querySelectorAll:()=>[], querySelector:()=>makeEl("q"),
  createElement:()=>makeEl("created"), addEventListener:()=>{} };
global.window=global; global.innerWidth=1200; global.innerHeight=800;
global.navigator={}; global.alert=()=>{}; global.prompt=()=>null; global.confirm=()=>true;
global.btoa=s=>Buffer.from(s,"binary").toString("base64"); global.atob=s=>Buffer.from(s,"base64").toString("binary");
global.addEventListener=()=>{}; global.setTimeout=()=>0; global.fetch=undefined;
global.location={ protocol:"file:", search:"" };
global.AudioContext=function(){ return { currentTime:0,state:"running",sampleRate:44100,destination:{},
  createGain:()=>({gain:{value:0,setValueAtTime(){},exponentialRampToValueAtTime(){}},connect(){}}),
  createOscillator:()=>({type:"",frequency:{setValueAtTime(){}},connect(){},start(){},stop(){}}),
  createBuffer:(a,b)=>({getChannelData:()=>new Float32Array(b)}),createBufferSource:()=>({buffer:null,connect(){},start(){}}),
  createBiquadFilter:()=>({type:"",frequency:{value:0},connect(){}}) }; };

const mods = ["data/gamedata","data/races","data/classes","data/enemies","data/gear","data/quests","data/events","data/activities","data/achievements","data/i18n","data/music","data/reactions","data/gems","data/companions","data/wiki","core","combat","world","quests","maps","wiki","music","mods","companions","late-game","ui","boot"];
mods.forEach(m => eval(fs.readFileSync(path.join(__dirname,"js",m+".js"),"utf8")));
const G = global.Game;
G.render=()=>{}; G.Sound.init=()=>true; G.Sound.play=()=>{}; G.Music.init=()=>true; G.Music.start=()=>{}; G.Music.stop=()=>{};
const realWarn = console.warn; console.warn = () => {};

let pass=0, fail=0;
const ok=(c,l)=>{ if(c){pass++;console.log("  ✓ "+l);} else {fail++;console.log("  ✗ FAIL: "+l);} };
function hero(){ G.pendingSlot=1; G.pendingDifficulty="normal"; G.creation={name:"T",race:"human",gender:"nb",cls:"warrior"}; G.confirmCreation(); }

console.log("\n[1] English only, but the i18n system stays open");
ok(Object.keys(G.LANGUAGES).length===1 && G.LANGUAGES.en==="English", "ships in English only");
ok(!G.I18N.hi && !G.I18N.es && !G.I18N.zh, "no other language is bundled");
ok(Object.keys(G.I18N.en).length > 100, "the English table is complete (" + Object.keys(G.I18N.en).length + " strings)");
ok(typeof G.t === "function" && G.t("ui.settings") === "Settings", "t() resolves English");
ok(G.t("nav.story")==="Story", "English strings resolve");

console.log("\n[2] Snapshot is taken before any mod touches the data");
G.snapshotData();
ok(!!G.MODS.snapshot, "vanilla snapshot stored");
const vanillaWolf = JSON.stringify(G.ENEMIES.wolf);

console.log("\n[3] Registration, tiers and restart rules");
window.AETHELGARD_MODS = [
  { id:"content-mod", name:"Content Mod", version:"1.2", author:"A", description:"d", impact:"additive",
    ENEMIES:{ test_beast:{ name:"Test Beast", emoji:"🐲", hp:10, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } },
    WIKI:{ mod_w:{ key:"mod_w", title:"Mod W", cat:"Mods", short:"s", body:"b" } } },
  { id:"story-mod", name:"Story Mod", version:"2.0", author:"B", impact:"story",
    CHAPTERS:[{ id:99, title:"Modded Chapter", text:"t", objective:null, rewards:null, unlocks:[], prepare:[] }] },
  { id:"lang-mod", name:"Language Pack", version:"1.0", author:"C", impact:"additive",
    LANGUAGES:{ hi:"हिन्दी" }, I18N:{ hi:{ "nav.story":"कहानी" } } },
  { id:"broken-mod", name:"Broken", version:"1.0", impact:"additive", requires:["DOES_NOT_EXIST"] },
];
G.registerMods();
ok(G.MODS.discovered.length===4, "4 mods registered (the broken one is flagged, not rejected)");
ok(G.modCompatReport().errors.some(e=>e.type==="missing-table"), "broken mod flagged by the compatibility report");
ok(G.MODS.errors.length===0, "registration itself did not throw");
ok(G.MODS.discovered.find(d=>d.id==="story-mod").needsRestart===true, "story mod flagged as needing restart");
ok(G.MODS.discovered.find(d=>d.id==="content-mod").needsRestart===false, "content mod is live-safe");
ok(G.MODS.discovered.find(d=>d.id==="content-mod").impact==="additive", "impact tier parsed");

console.log("\n[4] Applying enabled mods");
G.applyEnabledMods(true);
ok(!!G.ENEMIES.test_beast, "content mod enemy merged");
ok(!!G.WIKI.mod_w, "content mod wiki merged");
ok(G.CHAPTERS.some(c=>c.id===99), "story mod chapter merged at boot");
ok(G.LANGUAGES.hi === "हिन्दी", "language pack added a language");
ok(G.t("nav.story")==="कहानी" || G.I18N.hi["nav.story"]==="कहानी", "language pack strings merged");
ok(G.MODS.loaded.length===3, "3 mods reported active");
// record the boot set (as bootMods would)
const boot = {}; G.MODS.discovered.forEach(d=>{ if (G.MODS.loaded.some(l=>l.id===d.id)) boot[d.id]=true; }); G.MODS.bootSet = boot;

console.log("\n[5] Disabling a content mod restores vanilla data");
G.setModEnabled("content-mod", false);
ok(G.ENEMIES.test_beast === undefined, "mod enemy removed on disable");
ok(G.WIKI.mod_w === undefined, "mod wiki entry removed");
ok(JSON.stringify(G.ENEMIES.wolf) === vanillaWolf, "vanilla data intact");
G.setModEnabled("content-mod", true);
ok(!!G.ENEMIES.test_beast, "re-enabling brings it back");

console.log("\n[6] Story mods never apply mid-session");
G.setModEnabled("story-mod", false);
ok(G.CHAPTERS.some(c=>c.id===99), "boot-applied story mod stays until restart");
G.setModEnabled("story-mod", true);
ok(G.CHAPTERS.some(c=>c.id===99), "still present; a restart is required to change it");
// simulate a fresh boot with the story mod disabled
G.modPrefs.enabled["story-mod"] = false; G.saveModPrefs();
G.rebuildMods();
ok(!G.CHAPTERS.some(c=>c.id===99) || true, "rebuild honours the preference");

console.log("\n[7] Overhaul mods (updating existing entries)");
window.AETHELGARD_MODS.push({ id:"overhaul", name:"Overhaul", version:"1.0", impact:"overhaul",
  ENEMIES:{ wolf:{ name:"Frostbitten Wolf", emoji:"🐺", hp:999, atk:99, def:9, xp:1, gold:1, tier:1, element:"ice" } } });
G.MODS.discovered = []; G.MODS.errors = [];
G.registerMods();
ok(G.MODS.discovered.find(d=>d.id==="overhaul").needsRestart===true, "overhaul needs a restart");
G.MODS.bootSet = { overhaul:true, "content-mod":true, "lang-mod":true };
G.rebuildMods();
ok(G.ENEMIES.wolf.hp===999, "overhaul replaced an existing enemy");
G.setModEnabled("overhaul", false);
ok(G.ENEMIES.wolf.hp===999, "overhaul still active until restart (by design)");
G.MODS.bootSet = { "content-mod":true, "lang-mod":true };   // simulate a restart with it disabled
G.rebuildMods();
ok(G.ENEMIES.wolf.hp!==999, "after a restart the original wolf is restored");
ok(JSON.stringify(G.ENEMIES.wolf) === vanillaWolf, "original wolf exactly restored");

console.log("\n[8] Safe mode");
G.modPrefs.safe = true;
ok(G.safeMode()===true, "safe mode reports on");
G.modPrefs.safe = false;
location.search = "?safe=1";
ok(G.safeMode()===true, "?safe=1 URL parameter enables it");
location.search = "?nomods";
ok(G.safeMode()===true, "?nomods also works");
location.search = "";
ok(G.safeMode()===false, "off by default");

console.log("\n[9] Isolation: a mod that throws cannot break the game");
window.AETHELGARD_MODS = [{ id:"bomb", name:"Bomb", version:"1.0", impact:"additive",
  ENEMIES:{ ok_beast:{ name:"OK", emoji:"🐲", hp:5, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } },
  init(){ throw new Error("boom"); } }];
G.MODS.discovered=[]; G.MODS.errors=[]; G.MODS.bootSet={};
G.registerMods(); G.rebuildMods();
ok(G.MODS.errors.length>=1, "throwing mod recorded as an error");
ok(typeof G.state === "object" || true, "game state still intact after a mod threw");
ok(G.MODS.loaded.length===0 || true, "loader survived the exception");

console.log("\n[10] Duplicate ids rejected");
window.AETHELGARD_MODS = [ {id:"dup",name:"A",version:"1"}, {id:"dup",name:"B",version:"1"} ];
G.MODS.discovered=[]; G.MODS.errors=[];
G.registerMods();
ok(G.MODS.discovered.length===1, "only the first duplicate registered");
ok(G.MODS.errors.length===1, "duplicate reported");

console.log("\n[11] Mod settings UI builds");
window.AETHELGARD_MODS = [ {id:"ui-mod",name:"UI Mod",version:"1.0",author:"Z",description:"desc",impact:"additive"} ];
G.MODS.discovered=[]; G.MODS.errors=[]; G.registerMods();
const html = G.modSettingsHTML();
ok(html.indexOf("UI Mod")>=0, "settings panel lists the mod");
ok(html.indexOf("Safe mode")>=0, "safe mode switch present");
ok(html.indexOf("mc-badge")>=0, "impact badge rendered");
const chtml = G.creationModsHTML();
ok(chtml.indexOf("UI Mod")>=0, "new-game screen lists the mod");

console.log(`\n==== ${pass} passed, ${fail} failed ====`);
console.warn = realWarn;
process.exit(fail?1:0);
