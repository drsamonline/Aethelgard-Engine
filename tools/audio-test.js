// Measures real audio output: attaches an analyser to the master gain and
// checks that each sound and the music actually produce a signal.
const puppeteer = require('/usr/lib/node_modules/puppeteer-core');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const b = await puppeteer.launch({ executablePath:'/usr/local/bin/chromium-headless-shell',
                                     args:['--no-sandbox'], protocolTimeout: 60000 });
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('file:///scratch/work/aethelgard/index.html', { waitUntil:'load' });
  await sleep(2600);

  // a real gesture, which is what unlocks audio in a browser
  await p.click('body');
  await sleep(400);

  const r = await p.evaluate(async () => {
    const out = {};
    const S = Game.Sound;
    out.ctxStateBefore = S.ctx ? S.ctx.state : 'no ctx';
    if (!S.ctx) return { fatal: 'no AudioContext after a gesture' };
    if (S.ctx.state === 'suspended') { try { await S.ctx.resume(); } catch(e){} }
    out.ctxStateAfter = S.ctx.state;

    // tap the master output
    const an = S.ctx.createAnalyser();
    an.fftSize = 2048;
    S.master.connect(an);
    const buf = new Float32Array(an.fftSize);
    const peak = () => { an.getFloatTimeDomainData(buf); let m = 0; for (let i=0;i<buf.length;i++) m = Math.max(m, Math.abs(buf[i])); return m; };
    const listen = async (ms) => {
      let m = 0; const t0 = performance.now();
      while (performance.now() - t0 < ms) { m = Math.max(m, peak()); await new Promise(r=>setTimeout(r,16)); }
      return m;
    };

    out.settings = { sound: Game.settings.sound, music: Game.settings.music,
                     volume: Game.settings.volume, musicVolume: Game.settings.musicVolume };
    out.masterGain = S.master.gain.value;
    out.musicGain = Game.Music.gain ? Game.Music.gain.gain.value : null;

    // silence baseline
    out.silence = await listen(150);

    // each sound effect
    const sounds = ["ui","sword","hit","crit","spell","heal","coin","craft","levelup","victory","death","error","pickup","boss","notify"];
    out.effects = {};
    for (const s of sounds) {
      S.play(s);
      out.effects[s] = +(await listen(220)).toFixed(4);
    }

    // music
    Game.Music.update();
    out.musicPlaying = Game.Music.playing;
    out.musicSignal = +(await listen(1400)).toFixed(4);
    return out;
  });

  console.log(JSON.stringify(r, null, 1));
  await b.close();
  console.log(errs.length ? 'page errors: ' + errs.slice(0,2).join(' | ') : 'no page errors');
})();
