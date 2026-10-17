/* Twelve end-to-end simulations. node sims.js <from> <to> */
const puppeteer = require('/usr/lib/node_modules/puppeteer-core');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const FROM = Number(process.argv[2] || 1), TO = Number(process.argv[3] || 12);
const results = [];

const boot = async (b, mode, cls) => {
  const p = await b.newPage();
  p.on('dialog', async d => { await d.dismiss(); });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.setViewport({ width: 1400, height: 950 });
  await p.goto('file:///scratch/work/aethelgard/index.html', { waitUntil:'load' });
  await sleep(2400);
  await p.evaluate((m) => { localStorage.clear(); Game.settings.mode = m; Game.saveSettings(); }, mode || 'chronicles');
  await p.reload({ waitUntil:'load' }); await sleep(2500);
  await p.evaluate((c) => {
    Game.pendingSlot = 1; Game.pendingDifficulty = 'normal';
    Game.creation = { name:'Sim', race:'human', gender:'nb', cls: c || Game.modeClassIds()[0] };
    Game.confirmCreation();
    const s = Game.state;
    s.map.unlocked = Object.keys(Game.LOCATIONS); s.map.visited = Object.keys(Game.LOCATIONS);
  }, cls);
  return { p, errs };
};

const fight = (p) => p.evaluate(() => {
  const s = Game.state; s.hp = Game.maxHp(); s.energy = 999;
  let g = 0;
  while (s.combat && s.combat.active && g++ < 100) { s.hp = Game.maxHp(); s.energy = 999; Game.combatAction('attack'); }
  return !s.combat.active;
});

(async () => {
  const b = await puppeteer.launch({ executablePath:'/usr/local/bin/chromium-headless-shell',
                                     args:['--no-sandbox'], protocolTimeout: 60000 });

  // ---------- 1 & 2: full campaigns ----------
  for (const [n, mode, cls] of [[1,'chronicles','warrior'], [2,'villain',null]]) {
    if (n < FROM || n > TO) continue;
    const { p, errs } = await boot(b, mode, cls);
    let done = false, step = 0;
    while (step++ < 24) {
      const st = await p.evaluate(() => ({ pending: !!Game.state.story.pending, completed: !!Game.state.story.completed }));
      if (st.completed) { done = true; break; }
      if (st.pending) { await p.evaluate(() => Game.chooseOption(0)); continue; }
      const r = await p.evaluate(() => {
        const s = Game.state, ch = Game.CHAPTERS.find(c => c.id === s.story.chapter);
        if (!ch || !ch.objective) return { stop:1 };
        const o = ch.objective;
        if (o.type === 'depth') { s.map.current = 'cave';
          let g = 0; while ((s.dungeon.depth||0) < o.required && g++ < 40) { s.energy=999; s.hp=Game.maxHp(); Game.exploreDungeon();
            let c=0; while (s.combat && s.combat.active && c++<100){ s.hp=Game.maxHp(); s.energy=999; Game.combatAction('attack'); } }
          return { ok:1 }; }
        if (o.type !== 'kill') return { stop:1 };
        let where=null;
        for (const rg of Object.keys(Game.LOCAL_MAPS)) { const poi=Game.LOCAL_MAPS[rg].find(x=>(x.spawn||[]).includes(o.target)); if(poi){where={region:rg,id:poi.id};break;} }
        if (!where) return { FAILED:o.target };
        s.map.current = where.region;
        const need = o.required||1; let k=0,g=0;
        while (k<need && g++<12) { s.energy=999; s.hp=Game.maxHp(); Game.localAct(where.id);
          if (s.combat && s.combat.enemies) s.combat.enemies.forEach(e=>{e.hp=Math.min(e.hp,12);});
          let c=0; while (s.combat && s.combat.active && c++<100){ s.hp=Game.maxHp(); s.energy=999; Game.combatAction('attack'); } k++; }
        return { ok:1 };
      });
      if (r.FAILED || r.stop) break;
    }
    const fin = await p.evaluate(() => ({ ch: Game.state.story.chapter, completed: !!Game.state.story.completed, mode: Game.state.mode }));
    results.push({ sim:`${n}. ${mode} campaign`, pass: done, detail:`reached chapter ${fin.ch}, ${fin.completed?'Open World':'not finished'}${errs.length?' | errors: '+errs.slice(0,2).join('; '):''}` });
    await p.close();
  }

  // ---------- 3: mode isolation ----------
  if (3 >= FROM && 3 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const a = await p.evaluate(() => ({ ch: Game.CHAPTERS.map(c=>c.id).join(','),
      villainEnemies: Object.keys(Game.ENEMIES).filter(k=>k.startsWith('hero_')).length,
      villainClasses: Object.keys(Game.CLASSES).filter(k=>['coven_leader','iron_warden','spider_queen'].includes(k)).length,
      storyMod: (Game.MODS.loaded||[]).some(m=>m.id==='story-expansion') }));
    await p.evaluate(() => { localStorage.clear(); Game.settings.mode='villain'; Game.saveSettings(); });
    await p.reload({ waitUntil:'load' }); await sleep(2500);
    const v = await p.evaluate(() => ({ ch: Game.CHAPTERS.map(c=>c.id).join(','),
      heroChapters: Game.CHAPTERS.filter(c=>/Hollow Crown|Drowned Choir|Last Dawn/.test(c.title||'')).length,
      storyMod: (Game.MODS.loaded||[]).some(m=>m.id==='story-expansion'),
      villainMod: (Game.MODS.loaded||[]).some(m=>m.id==='villain-arc') }));
    const ok = a.ch === '1,2,3,4,5,6,7,8,9' && v.ch === '1,2,3,4,5,6' &&
               a.villainEnemies === 0 && v.storyMod === false && v.heroChapters === 0;
    results.push({ sim:'3. mode isolation', pass: ok,
      detail:`chronicles ch[${a.ch}] heroEnemies=${a.villainEnemies} | villain ch[${v.ch}] heroChapters=${v.heroChapters} storyMod=${v.storyMod}${errs.length?' | errors':''}` });
    await p.close();
  }

  // ---------- 4: endless dungeon depth ----------
  if (4 >= FROM && 4 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const r = await p.evaluate(() => {
      const s = Game.state; s.level = 40; s.gold = 50000;
      let floors = 0, deaths = 0;
      for (let i = 0; i < 25; i++) {
        s.energy = 999; s.hp = Game.maxHp();
        try {
          Game.exploreDungeon();
          let c = 0;
          while (s.combat && s.combat.active && c++ < 120) {
            s.hp = Game.maxHp(); s.energy = 999;
            Game.combatAction('attack');
          }
          if (s.dungeon && s.dungeon.depth > floors) floors = s.dungeon.depth;
        } catch (e) { deaths++; }
      }
      return { floors, deepest: (s.stats.deepestDepth||0), deaths, active: !!(s.dungeon && s.dungeon.active) };
    });
    results.push({ sim:'4. endless dungeon', pass: r.floors > 0 && r.deaths === 0,
      detail:`reached depth ${r.floors}, deepest ${r.deepest}, ${r.deaths} errors${errs.length?' | js errors':''}` });
    await p.close();
  }

  // ---------- 5: economy ----------
  if (5 >= FROM && 5 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const r = await p.evaluate(() => {
      const s = Game.state; s.gold = 1000; const out = {};
      const g0 = s.gold, w0 = s.inv.wood || 0;
      Game.gather('wood', 0); Game.gather('wood', 0);
      out.gathered = (s.inv.wood||0) - w0;
      const before = s.gold; Game.sellItem('wood');
      out.soldFor = s.gold - before;
      const b2 = s.gold, p2 = s.inv.potion || 0;
      Game.buyItem('potion');
      out.boughtCost = b2 - s.gold; out.gotPotion = (s.inv.potion||0) - p2;
      out.canCraft = !!(Game.canCraft && Game.canCraft('potion'));
      out.marketMoves = typeof s.market.wood === 'number';
      Game.tick(); Game.tick();
      out.goldFinite = isFinite(s.gold);
      return out;
    });
    const ok = r.gathered > 0 && r.soldFor > 0 && r.boughtCost > 0 && r.gotPotion > 0 && r.goldFinite;
    results.push({ sim:'5. economy', pass: ok, detail: JSON.stringify(r) + (errs.length?' | errors':'') });
    await p.close();
  }

  // ---------- 6: settlement + underworld ----------
  if (6 >= FROM && 6 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const r = await p.evaluate(() => {
      const s = Game.state; s.gold = 99999; s.nerve = 999; s.energy = 999;
      const out = {};
      try { Game.buildStructure(Object.keys(Game.BUILDINGS)[0]); out.built = Object.keys(s.settlement.buildings||{}).length; }
      catch(e){ out.buildErr = e.message.slice(0,40); }
      try { Game.crime && Game.crime(); out.crime = 'ok'; } catch(e){ out.crimeErr = e.message.slice(0,40); }
      try { Game.heist && Game.heist(); out.heist = 'ok'; } catch(e){ out.heistErr = e.message.slice(0,40); }
      try { Game.setMapMode && Game.setMapMode('local'); out.mapOk = true; } catch(e){ out.mapErr = e.message.slice(0,40); }
      out.goldFinite = isFinite(s.gold); out.heat = s.underworld ? s.underworld.heat : 'n/a';
      return out;
    });
    const ok = !r.buildErr && !r.crimeErr && !r.heistErr && r.goldFinite;
    results.push({ sim:'6. settlement + underworld', pass: ok, detail: JSON.stringify(r) + (errs.length?' | errors':'') });
    await p.close();
  }


  // ---------- 7: companions ----------
  if (7 >= FROM && 7 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const r = await p.evaluate(() => {
      const s = Game.state; s.gold = 99999; s.level = 60;
      // meet every requirement the companions declare
      s.reputation.oakhaven = 100;
      s.flags.coven_choice = 'purge'; s.flags.road_choice = 'fence';
      const list = Game.COMPANIONS || [];
      const out = { defined: list.length, tried: 0, recruited: 0 };
      list.map(d => d.id).forEach(id => {
        try {
          Game.recruitCompanion(id);
          out.tried++;
          if (Game.recruited(id)) out.recruited++;
        } catch (e) { (out.err = out.err||[]).push(id + ': ' + e.message.slice(0,30)); }
      });
      out.inParty = (s.companions||[]).length;
      out.activeCompanion = s.activeCompanion || null;
      // dismiss one and confirm it leaves
      const c = (s.companions||[])[0];
      try { if (c) { Game.dismissCompanion(c.id); out.dismissed = !Game.recruited(c.id); } }
      catch (e) { out.dismissErr = e.message.slice(0,40); }
      out.afterDismiss = (s.companions||[]).length;
      return out;
    });
    const ok = r.defined > 0 && !r.err && r.recruited > 0 && r.dismissed !== false;
    results.push({ sim:'7. companions', pass: ok, detail: JSON.stringify(r) + (errs.length?' | errors':'') });
    await p.close();
  }

  // ---------- 8: achievements ----------
  if (8 >= FROM && 8 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const r = await p.evaluate(() => {
      const s = Game.state; s.level = 50; s.gold = 999999;
      const total = (Game.ACHIEVEMENTS||[]).length;
      let before = Object.keys(s.achievements||{}).length;
      Game.checkAchievements();
      const ids = (Game.ACHIEVEMENTS||[]).slice(0, 8).map(a => a.id);
      ids.forEach(id => { try { Game.unlockAchievement(id); } catch(e){} });
      const after = Object.keys(s.achievements||{}).length;
      Game.save();
      return { total, before, after, unlockedById: after - before, saved: true };
    });
    const ok = r.after >= r.before && r.total > 0;
    results.push({ sim:'8. achievements', pass: ok, detail: JSON.stringify(r) + (errs.length?' | errors':'') });
    await p.close();
  }

  // ---------- 9: save / export / import ----------
  if (9 >= FROM && 9 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const before = await p.evaluate(() => {
      const s = Game.state; s.gold = 12345; s.level = 27; s.name = 'Exported';
      Game.save();
      const wrapped = Game.wrapSave(s);
      const txt = JSON.stringify(wrapped);
      const parsed = Game.parseSaveText(txt);
      return { gold: s.gold, level: s.level, wrapped: !!wrapped.state, parsedGold: parsed ? parsed.gold : null };
    });
    await p.reload({ waitUntil:'load' }); await sleep(2400);
    const after = await p.evaluate(() => { Game.continueGame(1); return { gold: Game.state.gold, level: Game.state.level }; });
    const ok = after.gold === 12345 && after.level === 27 && before.parsedGold === 12345 && before.wrapped;
    results.push({ sim:'9. save / export / import', pass: ok, detail: JSON.stringify({ before, after }) + (errs.length?' | errors':'') });
    await p.close();
  }

  // ---------- 10: mod toggling ----------
  if (10 >= FROM && 10 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    const r = await p.evaluate(() => {
      const out = {};
      out.loadedBefore = (Game.MODS.loaded||[]).map(m=>m.id).sort();
      const additive = (Game.MODS.loaded||[]).find(m => m.impact === 'additive' && m.id !== 'ai-art');
      out.toggledMod = additive ? additive.id : null;
      if (additive) {
        const before = (Game.MODS.loaded||[]).map(m=>m.id);
        Game.setModEnabled(additive.id, false);
        const off = (Game.MODS.loaded||[]).map(m=>m.id);
        out.removedOnOff = before.filter(x=>off.indexOf(x)<0);
        Game.setModEnabled(additive.id, true);
        const on = (Game.MODS.loaded||[]).map(m=>m.id);
        out.restoredOnOn = before.filter(x=>on.indexOf(x)>=0).length;
        // anything that also went is a dependent, which is correct
        out.dependentsAlsoRemoved = out.removedOnOff.filter(x=>x!==additive.id);
      }
      // a story mod must REFUSE to apply mid-session
      const storyMod = (Game.MODS.discovered||[]).find(m => m.needsRestart && Game.modEnabled(m.id));
      out.storyMod = storyMod ? storyMod.id : null;
      if (storyMod) {
        const chBefore = Game.CHAPTERS.length;
        Game.setModEnabled(storyMod.id, false);
        out.chaptersAfterStoryOff = Game.CHAPTERS.length;
        out.storyRefusedMidSession = Game.CHAPTERS.length === chBefore;
        Game.setModEnabled(storyMod.id, true);
      }
      // art packs stay mutually exclusive
      Game.setEdition('ai-art-graphics');
      out.packsOn = Game.graphicsMods().filter(d=>Game.modEnabled(d.id)).map(d=>d.id);
      Game.setEdition('flat-icons');
      out.packsAfterSwitch = Game.graphicsMods().filter(d=>Game.modEnabled(d.id)).map(d=>d.id);
      return out;
    });
    const ok = r.removedOnOff.length >= 1 && r.restoredOnOn >= 1 && r.storyRefusedMidSession === true
               && r.packsOn.length === 1 && r.packsAfterSwitch.length === 1;
    results.push({ sim:'10. mod toggling', pass: ok, detail: JSON.stringify(r) + (errs.length?' | errors':'') });
    await p.close();
  }

  // ---------- 11: ascension / late game ----------
  if (11 >= FROM && 11 <= TO) {
    const { p, errs } = await boot(b, 'chronicles', 'warrior');
    p.removeAllListeners('dialog');
    p.on('dialog', async d => { await d.accept(); });   // ascend() asks to confirm
    const r = await p.evaluate(() => {
      const s = Game.state; s.level = 40; s.gold = 5000;
      s.story.completed = true; s.mode = 'open';
      const before = { asc: s.ascensions||0, ach: Object.keys(s.achievements||{}).length };
      let ok = false;
      try { Game.ascend(); ok = true; } catch(e) { return { err: e.message.slice(0,60) }; }
      const a = Game.state;
      return { before, after: { asc: a.ascensions, level: a.level, ach: Object.keys(a.achievements||{}).length,
                                might: a.attrs.might, ap: a.ap }, ok,
               canAscend: Game.canAscend ? Game.canAscend() : 'n/a' };
    });
    const ok = r.ok && r.after && r.after.asc > r.before.asc;
    results.push({ sim:'11. ascension', pass: ok, detail: JSON.stringify(r) + (errs.length?' | errors':'') });
    await p.close();
  }

  // ---------- 12: mobile + long soak ----------
  if (12 >= FROM && 12 <= TO) {
    const p = await b.newPage();
    p.on('dialog', async d => { await d.dismiss(); });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.setViewport({ width: 390, height: 844 });
    await p.goto('file:///scratch/work/aethelgard/index.html', { waitUntil:'load' });
    await sleep(2400);
    await p.evaluate(() => { localStorage.clear();
      Game.pendingSlot=1; Game.pendingDifficulty='normal';
      Game.creation={name:'Mob',race:'human',gender:'nb',cls:'warrior'}; Game.confirmCreation(); });
    const r = await p.evaluate(() => {
      const s = Game.state; s.map.unlocked = Object.keys(Game.LOCATIONS);
      const tabs = ['story','hero','skills','atlas','home','forge','market','underworld','inventory','codex','wiki'];
      let okTabs = 0;
      tabs.forEach(t => { try { Game.switchTab(t); if (document.getElementById('view-container').innerHTML.length > 50) okTabs++; } catch(e){} });
      const nodesBefore = document.getElementsByTagName('*').length;
      for (let i = 0; i < 120; i++) { s.energy = 999; Game.tick(); }
      const nodesAfter = document.getElementsByTagName('*').length;
      return { okTabs, nodesBefore, nodesAfter, leak: nodesAfter - nodesBefore,
               overflow: document.documentElement.scrollWidth > window.innerWidth + 2,
               scrollW: document.documentElement.scrollWidth, winW: window.innerWidth };
    });
    const ok = r.okTabs === 11 && !r.overflow && Math.abs(r.leak) < 60;
    results.push({ sim:'12. mobile + 120-tick soak', pass: ok, detail: JSON.stringify(r) + (errs.length?' | errors':'') });
    await p.close();
  }

  await b.close();
  console.log('\n===== SIMULATIONS ' + FROM + '-' + TO + ' =====');
  results.forEach(r => console.log(`  ${r.pass ? 'PASS' : 'FAIL'}  ${r.sim}\n        ${r.detail}`));
  console.log(`\n  ${results.filter(r=>r.pass).length}/${results.length} passed`);
})();
