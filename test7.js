/* Graphics/sprite pipeline suite. */
const fs = require("fs"), path = require("path");
const store = {};
global.localStorage = { getItem:k=>(k in store?store[k]:null), setItem:(k,v)=>{store[k]=String(v);}, removeItem:k=>{delete store[k];} };
function styleStub(){ const o={}; o.setProperty=(k,v)=>{o[k]=v;}; o.removeProperty=(k)=>{delete o[k];}; o.setProperty._=0; return o; }
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

console.log("\n[1] No pack → emoji, exactly as before");
hero();
ok(G.sprite("enemy.wolf","🐺")==="🐺", "unmapped key returns the emoji");
ok(G.sprite("anything")==="•", "missing fallback is safe");
ok(G.sprite(null,"X")==="X", "null key is safe");
ok(Object.keys(G.SPRITES).length===0, "no sprites registered by default");

console.log("\n[2] Registering and activating a pack");
G.registerGraphicsPack({
  id:"test-pack", name:"Test Pack", base:"mods/test-pack/art/", scale:1.5, pixel:true,
  palette:{ "--gold":"#f0c060" },
  sprites:{
    "enemy.wolf":"wolf.png",
    "class.mage":{ src:"heroes.png", sheet:{x:32,y:0,w:32,h:32}, cols:4, rows:1, scale:2 },
    "player.mage":{ src:"heroes.png", sheet:{x:0,y:0,w:32,h:32}, cols:4, rows:1, frames:4, fps:8 },
  },
});
ok(G.graphicsPackList().length===1, "pack listed");
G.applyGraphicsPack("test-pack");
ok(Object.keys(G.SPRITES).length===3, "3 sprites resolved");
ok(G.SPRITES["enemy.wolf"].src==="mods/test-pack/art/wolf.png", "base path applied");
ok(G.SPRITES["enemy.wolf"].scale===1.5, "pack scale inherited");
ok(G.SPRITES["enemy.wolf"].pixel===true, "pack pixel flag inherited");
ok(document.documentElement.style["--gold"]==="#f0c060", "palette applied");

console.log("\n[3] Rendering");
const img = G.sprite("enemy.wolf","🐺");
ok(img.indexOf("<img")===0 && img.indexOf('class="spr')>0, "simple sprite renders an <img class=spr>");
ok(img.indexOf("spr-pixel")>0, "pixel class applied");
ok(img.indexOf("width:1.5em")>0, "scale applied inline");
ok(img.indexOf("data-fb=\"🐺\"")>0, "fallback emoji stored for onerror");
const sheet = G.sprite("class.mage","🧙");
ok(sheet.indexOf("spr-crop")>0, "sheet cell renders a crop");
ok(sheet.indexOf("background-position")>0, "sheet cell uses a background offset");
ok(sheet.indexOf("background-size:400%")>0, "sheet is scaled so one cell fills the box");
const anim = G.sprite("player.mage","🧙");
ok(anim.indexOf("animation:sprSheet")>0, "animated sprite gets the sheet animation");
ok(anim.indexOf("--frames:4")>0 && anim.indexOf("--cols:4")>0, "--frames/--cols set");
ok(anim.indexOf("0.500s steps(4)")>0, "animation duration computed (4 frames / 8 fps)");
ok(G.sprite("enemy.goblin","👺")==="👺", "uncovered key still falls back to emoji");

console.log("\n[4] Turning the pack off restores emoji");
G.applyGraphicsPack(null);
ok(Object.keys(G.SPRITES).length===0, "sprites cleared");
ok(G.sprite("enemy.wolf","🐺")==="🐺", "back to emoji");
ok(document.documentElement.style["--gold"]===undefined, "palette removed");

console.log("\n[5] A graphics pack arriving as a mod");
G.snapshotData();
window.AETHELGARD_MODS = [{
  id:"art-mod", name:"Art Mod", version:"1.0", impact:"additive",
  GRAPHICS:{ id:"art", name:"Art Pack", base:"mods/art/", sprites:{ "item.potion":"p.png" } },
}];
G.MODS.discovered=[]; G.MODS.errors=[]; G.MODS.bootSet={};
G.registerMods(); G.rebuildMods();
ok(!!G.GRAPHICS_PACKS.art, "pack registered from the mod");
G.applyGraphicsPack("art");
ok(!!G.SPRITES["item.potion"], "mod sprite active");
G.setModEnabled("art-mod", false);
ok(!G.GRAPHICS_PACKS.art, "disabling the mod removes its pack");
ok(!G.SPRITES["item.potion"], "its sprites are gone too");

console.log("\n[6] Fallback handler swaps a broken image for its emoji");
let swapped = null;
G.spriteFallback({ getAttribute:()=>"🐲", closest:()=>null, replaceWith:(n)=>{ swapped = n; } });
ok(swapped && swapped.textContent==="🐲", "broken image replaced by the emoji");

console.log("\n[7] Settings exposes the picker");
G.registerGraphicsPack({ id:"p1", name:"Pack One", sprites:{} });
const html = G.graphicsSettingsHTML();
ok(html.indexOf("Graphics pack")>=0, "section present");
ok(html.indexOf("Pack One")>=0, "pack listed");
ok(html.indexOf("Default (emoji)")>=0, "default option present");
ok(html.indexOf("Game.setGraphicsPack")>=0, "switch wired");

console.log(`\n==== ${pass} passed, ${fail} failed ====`);
console.warn = realWarn;
process.exit(fail?1:0);
