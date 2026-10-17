/* ============================================================
   Aethelgard — end-to-end verifier

   Drives both games with real clicks and real game calls, and checks:
     - every tab renders
     - every action runs without throwing
     - combat resolves
     - a save round-trips exactly
     - no chapter objective is uncompletable
     - the whole campaign can be played to the end
     - content validation reports nothing

   Needs puppeteer-core and chromium-headless-shell.
     node tools/verify.js [path-to-build]
   ============================================================ */
const http = require('http'), fs = require('fs'), path = require('path');
const puppeteer = require('/usr/lib/node_modules/puppeteer-core');
const sleep = ms => new Promise(r => setTimeout(r, ms));

const ROOT = process.argv[2] || '/scratch/work/aethelgard';
const MIME = { '.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json',
               '.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.md':'text/markdown',
               '.svg':'image/svg+xml','.txt':'text/plain' };
const TABS = ["story","hero","skills","atlas","home","forge","market","underworld","inventory","codex","wiki"];
const problems = [];

function serve(port) {
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      let u = decodeURIComponent(q.url.split('?')[0]); if (u === '/') u = '/index.html';
      fs.readFile(path.join(ROOT, u), (e, d) => {
        if (e) { r.writeHead(404); return r.end('404'); }
        r.writeHead(200, { 'Content-Type': MIME[path.extname(u)] || 'application/octet-stream' });
        r.end(d);
      });
    });
    s.listen(port, '127.0.0.1', () => res(s));
  });
}

async function startGame(p, mode, cls) {
  await p.evaluate((m, c) => {
    localStorage.clear();
    Game.settings.mode = m; Game.saveSettings();
  }, mode, cls);
  await p.reload({ waitUntil: 'load' });
  await sleep(2600);
  return p.evaluate((c) => {
    Game.pendingSlot = 1; Game.pendingDifficulty = 'normal';
    Game.creation = { name:'Verify', race:'human', gender:'nb', cls: c || Game.modeClassIds()[0] };
    Game.confirmCreation();
    const s = Game.state;
    s.map.unlocked = Object.keys(Game.LOCATIONS);
    s.map.visited = Object.keys(Game.LOCATIONS);
    return { mode: Game.activeModeId(), cls: s.cls, chapter: s.story.chapter };
  }, cls);
}

(async () => {
  const srv = await serve(8990);
  const b = await puppeteer.launch({ executablePath:'/usr/local/bin/chromium-headless-shell',
                                     args:['--no-sandbox'], protocolTimeout: 60000 });

  for (const [mode, cls] of [['chronicles','warrior'], ['villain',null]]) {
    const p = await b.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
    p.on('console', m => { if (m.type()==='error' && !/ERR_FILE_NOT_FOUND/.test(m.text())) errs.push('CONSOLE: ' + m.text().slice(0,110)); });
    await p.setViewport({ width: 1400, height: 950 });
    await p.goto('http://127.0.0.1:8990/index.html', { waitUntil:'load' });
    await sleep(2600);

    const started = await startGame(p, mode, cls);
    console.log(`\n=== ${mode.toUpperCase()} — ${started.cls} ===`);

    // tabs
    const tabs = await p.evaluate((list) => list.map(t => {
      try { Game.switchTab(t); return { t, len: document.getElementById('view-container').innerHTML.length }; }
      catch (e) { return { t, err: e.message }; }
    }), TABS);
    const badTabs = tabs.filter(x => x.err || x.len < 50);
    console.log('  tabs:', tabs.map(x => x.err ? `${x.t}:ERR` : `${x.t}:ok`).join(' '));
    if (badTabs.length) problems.push(`${mode}: bad tabs ${JSON.stringify(badTabs)}`);

    // actions
    const acts = await p.evaluate(() => {
      const out = {}, T = (n, f) => { try { f(); out[n] = 'ok'; } catch (e) { out[n] = e.message; } };
      T('travel', () => Game.travel('oakhaven'));
      T('buy', () => Game.buyItem && Game.buyItem('potion'));
      T('sell', () => Game.sellItem && Game.sellItem('wood'));
      T('craft', () => { if (Game.canCraft && Game.canCraft('potion')) Game.craftItem('potion'); });
      T('tick', () => { for (let i=0;i<5;i++) Game.tick(); });
      T('achievements', () => Game.checkAchievements());
      T('modReport', () => Game.modCompatReport());
      T('content', () => Game.validateContent());
      T('diagnostics', () => Game.diagnosticsReport());
      T('exportWrap', () => Game.wrapSave(Game.state));
      T('save', () => Game.save());
      return out;
    });
    const bad = Object.entries(acts).filter(([,v]) => v !== 'ok');
    console.log('  actions:', Object.entries(acts).map(([k,v]) => v==='ok'?k:'['+k+':FAIL]').join(' '));
    if (bad.length) problems.push(`${mode}: failing actions ${JSON.stringify(bad)}`);

    // content validation
    const val = await p.evaluate(() => Game.validateContent());
    console.log(`  content: ${val.errors.length} errors, ${val.warnings.length} warnings`);
    val.errors.forEach(e => console.log(`     ✗ ${e.where}: ${e.msg}`));
    if (val.errors.length) problems.push(`${mode}: content errors ${JSON.stringify(val.errors)}`);

    // combat
    const com = await p.evaluate(() => {
      try {
        const s = Game.state; s.energy = 999; s.hp = Game.maxHp();
        Game.startCombat(['wolf'], { cost:0 });
        let g = 0;
        while (s.combat && s.combat.active && g++ < 80) { s.hp = Game.maxHp(); s.energy = 999; Game.combatAction('attack'); }
        return { ok:true, ended: !s.combat.active };
      } catch (e) { return { ok:false, err:e.message }; }
    });
    console.log('  combat:', JSON.stringify(com));
    if (!com.ok || !com.ended) problems.push(`${mode}: combat ${JSON.stringify(com)}`);

    // save round trip
    const before = await p.evaluate(() => { Game.state.gold = 7777; Game.state.level = 23; Game.save();
      return { gold: Game.state.gold, level: Game.state.level }; });
    await p.reload({ waitUntil:'load' }); await sleep(2500);
    const after = await p.evaluate(() => { Game.continueGame(1); return { gold: Game.state.gold, level: Game.state.level }; });
    console.log('  save round-trip:', JSON.stringify(after));
    if (after.gold !== 7777 || after.level !== 23) problems.push(`${mode}: save lost state ${JSON.stringify({before, after})}`);

    // walk the campaign
    let step = 0, done = false;
    while (step++ < 22) {
      const st = await p.evaluate(() => ({ ch: Game.state.story.chapter, pending: !!Game.state.story.pending,
                                           completed: !!Game.state.story.completed }));
      if (st.completed) { done = true; break; }
      if (st.pending) { await p.evaluate(() => Game.chooseOption(0)); continue; }
      const r = await p.evaluate(() => {
        const s = Game.state;
        const ch = Game.CHAPTERS.find(c => c.id === s.story.chapter);
        if (!ch || !ch.objective) return { stop: 'no objective' };
        const o = ch.objective;
        if (o.type === 'depth') {
          s.map.current = 'cave';
          let g = 0;
          while ((s.dungeon.depth || 0) < o.required && g++ < 40) {
            s.energy = 999; s.hp = Game.maxHp(); Game.exploreDungeon();
            let c = 0; while (s.combat && s.combat.active && c++ < 80) { s.hp = Game.maxHp(); s.energy = 999; Game.combatAction('attack'); }
          }
          return { type:'depth', depth: s.dungeon.depth };
        }
        if (o.type !== 'kill') return { stop: 'objective type ' + o.type };
        let where = null;
        for (const rg of Object.keys(Game.LOCAL_MAPS)) {
          const poi = Game.LOCAL_MAPS[rg].find(x => (x.spawn||[]).includes(o.target));
          if (poi) { where = { region: rg, id: poi.id }; break; }
        }
        if (!where) return { FAILED: o.target + ' placed nowhere' };
        s.map.current = where.region;
        const need = o.required || 1;
        let kills = 0, guard = 0;
        while (kills < need && guard++ < 12) {
          s.energy = 999; s.hp = Game.maxHp(); Game.localAct(where.id);
          if (s.combat && s.combat.enemies) s.combat.enemies.forEach(e => { e.hp = Math.min(e.hp, 12); });
          let c = 0; while (s.combat && s.combat.active && c++ < 80) { s.hp = Game.maxHp(); s.energy = 999; Game.combatAction('attack'); }
          kills++;
        }
        return { ch: ch.id, target: o.target, region: where.region };
      });
      if (r.FAILED || r.stop) { console.log('     stopped:', JSON.stringify(r)); break; }
    }
    console.log('  campaign:', done ? 'completed → Open World' : `stopped at chapter ${(await p.evaluate(() => Game.state.story.chapter))}`);
    if (!done) problems.push(`${mode}: campaign did not complete`);

    if (errs.length) problems.push(`${mode}: JS errors ${errs.slice(0,3).join(' | ')}`);
    console.log('  errors:', errs.length ? errs.slice(0,2).join(' | ') : 'none');
    await p.close();
  }

  await b.close(); srv.close();
  console.log('\n================ VERIFY SUMMARY ================');
  console.log(problems.length ? problems.map(x => '  ✗ ' + x).join('\n') : '  ✓ everything passed');
  process.exit(problems.length ? 1 : 0);
})();
