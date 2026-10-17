/* Mod compatibility suite: dependencies, conflicts, key collisions, load order. */
const fs = require("fs"), path = require("path");
const store = {};
global.localStorage = { getItem:k=>(k in store?store[k]:null), setItem:(k,v)=>{store[k]=String(v);}, removeItem:k=>{delete store[k];} };
function styleStub(){ const o={}; o.setProperty=(k,v)=>{o[k]=v;}; o.removeProperty=(k)=>{delete o[k];}; return o; }
function makeEl(id){ const el={ id,_html:"",style:styleStub(),scrollTop:0,offsetWidth:120,offsetHeight:60,dataset:{},className:"",value:"",children:[],firstChild:null,tagName:"DIV",src:"",
  classList:{_s:new Set(),add(...c){c.forEach(x=>this._s.add(x));},remove(...c){c.forEach(x=>this._s.delete(x));},toggle(c,f){if(f===undefined)f=!this._s.has(c);f?this._s.add(c):this._s.delete(c);return f;},contains(c){return this._s.has(c);}},
  appendChild(){},removeChild(){},remove(){},replaceWith(){},closest(){return null;},getAttribute(){return null;},setAttribute(){},removeAttribute(){},focus(){},offsetParent:null,contains(){return false;},
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

const mods = ["data/gamedata","data/races","data/classes","data/enemies","data/gear","data/quests","data/events","data/activities","data/achievements","data/i18n","data/music","data/reactions","data/gems","data/companions","data/wiki","graphics","core","combat","world","quests","maps","wiki","music","mods","companions","late-game","ui","boot"];
mods.forEach(m => eval(fs.readFileSync(path.join(__dirname,"js",m+".js"),"utf8")));
const G = global.Game;
G.render=()=>{}; G.Sound.init=()=>true; G.Sound.play=()=>{}; G.Music.init=()=>true; G.Music.start=()=>{}; G.Music.stop=()=>{};
const realWarn = console.warn; console.warn = () => {};

let pass=0, fail=0;
const ok=(c,l)=>{ if(c){pass++;console.log("  ✓ "+l);} else {fail++;console.log("  ✗ FAIL: "+l);} };
function hero(){ G.pendingSlot=1; G.pendingDifficulty="normal"; G.creation={name:"T",race:"human",gender:"nb",cls:"warrior"}; G.confirmCreation(); }
function reset(mods){ window.AETHELGARD_MODS = mods; G.MODS.discovered=[]; G.MODS.errors=[]; G.MODS.bootSet={}; G.modPrefs={enabled:{},safe:false}; G.snapshotData(); G.registerMods(); }
const E = (id, extra) => Object.assign({ id, name:id, version:"1.0", impact:"additive" }, extra||{});

hero();

console.log("\n[1] A clean set reports everything compatible");
reset([
  E("base", { provides:["core"], ENEMIES:{ a:{ name:"A", emoji:"a", hp:1, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } } }),
  E("extra", { ENEMIES:{ b:{ name:"B", emoji:"b", hp:1, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } } }),
]);
let r = G.modCompatReport();
ok(r.errors.length===0, "no errors");
ok(r.warnings.length===0, "no warnings");
ok(r.ok.length===2, "both mods OK");
ok(G.modStatus("base", r).state==="ok", "base status ok");

console.log("\n[2] Missing / disabled dependencies");
reset([ E("solo", { requiresMods:["absent"] }) ]);
r = G.modCompatReport();
ok(r.errors.some(e=>e.type==="missing-mod"), "missing dependency flagged");
ok(G.modStatus("solo", r).state==="error", "status is error");
reset([ E("base"), E("needs", { requiresMods:["base"] }) ]);
G.setModEnabled("base", false);
r = G.modCompatReport();
ok(r.errors.some(e=>e.type==="disabled-dep"), "disabled dependency flagged");
G.setModEnabled("base", true);
r = G.modCompatReport();
ok(r.errors.length===0, "re-enabling the dependency clears the error");

console.log("\n[3] Declared conflicts");
reset([ E("a", { conflicts:["b"] }), E("b") ]);
r = G.modCompatReport();
ok(r.conflicts.length===1, "conflict recorded");
ok(r.errors.some(e=>e.type==="conflict"), "conflict is an error");
ok(r.ok.length===0, "neither mod loads");
G.setModEnabled("b", false);
r = G.modCompatReport();
ok(r.errors.length===0 && r.ok.length===1, "disabling the other side resolves it");

console.log("\n[4] Key collisions");
reset([
  E("one", { ENEMIES:{ wolf:{ name:"W1", emoji:"w", hp:1, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } } }),
  E("two", { ENEMIES:{ wolf:{ name:"W2", emoji:"w", hp:1, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } } }),
]);
r = G.modCompatReport();
ok(r.collisions.length===1, "collision detected on ENEMIES.wolf");
ok(r.warnings.some(w=>w.type==="override"), "plain overlap is a warning, not an error");
ok(r.ok.length===2, "both still load (last wins)");
reset([
  E("owner", { exclusive:["ENEMIES.wolf"], ENEMIES:{ wolf:{ name:"W1", emoji:"w", hp:1, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } } }),
  E("other", { ENEMIES:{ wolf:{ name:"W2", emoji:"w", hp:1, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } } }),
]);
r = G.modCompatReport();
ok(r.errors.some(e=>e.type==="exclusive-key"), "an exclusive claim turns it into an error");

console.log("\n[5] Load order");
reset([
  E("later", { loadAfter:["first"] }),
  E("first"),
]);
r = G.modCompatReport();
ok(r.order[0]==="first" && r.order[1]==="later", "loadAfter respected ("+r.order.join(" → ")+")");
reset([ E("x", { loadAfter:["y"] }), E("y", { loadAfter:["x"] }) ]);
r = G.modCompatReport();
ok(r.warnings.some(w=>/circular/.test(w.msg)), "circular dependency warned, not fatal");

console.log("\n[6] Capability tokens");
reset([ E("art", { provides:["art:vector"] }), E("needs-art", { requiresProvides:["art:vector"] }) ]);
r = G.modCompatReport();
ok(r.errors.length===0, "capability satisfied");
reset([ E("needs-art", { requiresProvides:["art:vector"] }) ]);
r = G.modCompatReport();
ok(r.errors.some(e=>e.type==="missing-capability"), "unmet capability flagged");

console.log("\n[7] Broken mods are skipped, the rest still load");
reset([
  E("good", { ENEMIES:{ ok:{ name:"OK", emoji:"o", hp:1, atk:1, def:0, xp:1, gold:1, tier:1, element:"physical" } } }),
  E("bad",  { requiresMods:["nope"] }),
]);
G.rebuildMods();
ok(!!G.ENEMIES.ok, "the working mod applied");
ok(G.MODS.blocked.length===1 && G.MODS.blocked[0].id==="bad", "the broken mod was blocked");
ok(G.MODS.blocked[0].reasons.length>0, "with a reason recorded");
ok(G.MODS.loaded.length===1, "only one mod reported loaded");

console.log("\n[8] Missing data table requirement");
reset([ E("t", { requires:["NOT_A_TABLE"] }) ]);
r = G.modCompatReport();
ok(r.errors.some(e=>e.type==="missing-table"), "missing data table flagged");

console.log("\n[9] Real shipped mods are mutually compatible");
window.AETHELGARD_MODS = [];
["example-mod.js","example-addon.js","example-overhaul.js","example-graphics/mod.js","overhaul-vector/mod.js"].forEach(f => {
  try { eval(fs.readFileSync(path.join(__dirname,"mods",f),"utf8")); } catch(e){ console.log("   load skip", f, e.message); }
});
G.MODS.discovered=[]; G.MODS.errors=[]; G.modPrefs={enabled:{},safe:false};
G.registerMods();
r = G.modCompatReport();
ok(G.MODS.discovered.length>=5, "all shipped mods registered ("+G.MODS.discovered.length+")");
ok(r.errors.length===0, "no compatibility errors among shipped mods");
ok(r.order.indexOf("marsh-lurker") < r.order.indexOf("lurker-hunt"), "add-on loads after its base mod");
G.setModEnabled("marsh-lurker", false);
r = G.modCompatReport();
ok(r.errors.some(e=>e.id==="lurker-hunt"), "add-on reports broken when its base is off");
G.setModEnabled("marsh-lurker", true);
r = G.modCompatReport();
ok(r.errors.length===0, "turning the base back on fixes the add-on");

console.log("\n[10] The panel renders the report");
G.MODS.discovered=[]; G.modPrefs={enabled:{},safe:false}; reset([ E("p1",{ provides:["x"] }), E("p2",{ requiresMods:["nope"] }) ]);
const html = G.modSettingsHTML();
ok(html.indexOf("work together")>=0 || html.indexOf("problem")>=0, "summary line rendered");
ok(html.indexOf("mc-status")>=0, "per-mod status badge rendered");
ok(html.indexOf("Load order")>=0 || html.indexOf("requires")>=0, "detail rendered");

console.log(`\n==== ${pass} passed, ${fail} failed ====`);
console.warn = realWarn;
process.exit(fail?1:0);
