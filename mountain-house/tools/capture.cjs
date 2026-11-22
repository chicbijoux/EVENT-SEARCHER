// Deterministic full-frame phone recording of the Casa Măgura page.
// JavaScript time is faked and CSS animations are stepped by hand, so every run gives the same frames.
// Usage: node mountain-house/tools/capture.cjs <frames-dir> [url]   (serve mountain-house/ first, e.g. python3 -m http.server 8773)
// Env: VW, VH (CSS viewport), DSF (pixel density). Defaults record 432x768 at 2.5x = 1080x1920.
const { chromium } = require('playwright');
const VW = +(process.env.VW || 432), VH = +(process.env.VH || 768), DSF = +(process.env.DSF || 2.5);
const FPS = 30, OUT = process.argv[2], URL = process.argv[3] || 'http://localhost:8773/index.html';
const ONLY = process.env.ONLY ? process.env.ONLY.split(',').map(Number) : null;
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const soft = t => t * t * (3 - 2 * t);
const lerp = (a, b, t) => a + (b - a) * t;

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: DSF, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  await p.clock.install({ time: new Date('2026-11-22T12:00:00') });
  await p.goto(URL, { waitUntil: 'networkidle' });
  // wait (real time) until every walk frame and photo has loaded
  for (let i = 0; i < 60; i++) {
    const ok = await p.evaluate(() => film.on && film.imgs.length === film.n && film.imgs.every(o => o && o.ok) && [...document.images].every(im => im.complete));
    if (ok) break;
    await p.waitForTimeout(500);
  }
  await p.evaluate(() => [...document.images].forEach(im => { im.loading = 'eager'; }));
  await p.waitForTimeout(1500);
  const now = await p.evaluate(() => Date.now());
  await p.clock.pauseAt(new Date(now + 1000));
  await p.addStyleTag({ content: `html{scroll-behavior:auto!important} ::-webkit-scrollbar{display:none} #rail{scroll-snap-type:none!important}
    #__tap{position:fixed;left:0;top:0;width:54px;height:54px;margin:-27px 0 0 -27px;border-radius:50%;background:rgba(255,255,255,.3);border:1.5px solid rgba(255,255,255,.85);box-shadow:0 4px 18px rgba(0,0,0,.35);z-index:9999;opacity:0;pointer-events:none}` });
  await p.evaluate(() => {
    const t = document.createElement('div'); t.id = '__tap'; document.body.appendChild(t);
    const held = new WeakSet();
    window.__step = dt => { for (const a of document.getAnimations()) { if (!held.has(a)) { a.pause(); held.add(a); } else { a.currentTime = (a.currentTime || 0) + dt; } } };
    window.__tap = (x, y, o, s) => { t.style.transform = `translate(${x}px,${y}px) scale(${s})`; t.style.opacity = o; };
    window.__scroll = y => { window.scrollTo(0, y); window.dispatchEvent(new Event('scroll')); };
    window.__c = sel => { const r = document.querySelector(sel).getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };
    window.__top = sel => Math.round(document.querySelector(sel).getBoundingClientRect().top + scrollY);
    window.__max = () => document.documentElement.scrollHeight - innerHeight;
    // replay the hero entrance from the start
    window.__scroll(0);
    for (const a of document.getAnimations()) { a.currentTime = 0; a.pause(); held.add(a); }
  });

  // ---------- the plan: K = scroll keyframes [t, target, 'ease'|'lin'|'soft'], T = taps [t, selector, action] ----------
  const walk = await p.evaluate(() => { const w = document.getElementById('walk'); return { top: w.offsetTop, span: w.offsetHeight - innerHeight }; });
  const W = q => walk.top + walk.span * q;
  const K = [[0, 0]]; const T = []; let t = 0;
  const hold = d => { t += d; K.push([t, null]); };
  const go = (y, d, mode) => { t += d; K.push([t, y, mode]); };
  const tap = (sel, fn, dt = 0) => T.push([t + dt, sel, fn]);
  const at = (sel, off = 0) => async () => (await p.evaluate(s => window.__top(s), sel)) + off;

  hold(2.3);                                           // the name rises over the pond
  go(W(0), .9);                                        // into the walk: the first frame is the hero photo
  // the walk: pond, porch, hearth, long window, study, then the laptop opens (about 12.5 s)
  go(W(.30), 3.2, 'soft');                             // over the pond to the porch
  go(W(.52), 2.4, 'soft');                             // through the door to the fire
  go(W(.70), 2.2, 'soft');                             // the glass gable and the ridge
  go(W(.84), 1.9, 'soft');                             // into the study, to the laptop
  hold(.35);
  go(W(1), 2.2, 'soft');                               // the screen opens into the case study
  go(at('#house'), .7); hold(1.3);                    // CASA MĂGURA
  go(at('#analysis', 40), 1.0); hold(.9);              // the site
  go(at('#idea', 30), .9); hold(.8);                   // the idea
  go(at('#function', 20), 1.0);
  tap('.floor[data-f="roof"]', 'click', .4); hold(1.3);    // three floors: tap the roof
  go(at('#interior', 30), 1.0);
  tap('#rail', 'swipe', .3); hold(1.2);                // inside: swipe the rooms
  go(at('#stay', 0), 1.1);
  go(at('#book', -120), .7);
  tap('#email', 'fill', .2); tap('#book .btn', 'click', 1.0); hold(1.6);   // request dates
  hold(Math.max(.4, 30 - t));
  const END = 30;
  console.log('plan length', t.toFixed(2));

  const resolved = new Map();
  let lastY = 0;
  async function yAt(s){
    for (let i = 1; i < K.length; i++) {
      if (s > K[i][0]) continue;
      const [t0] = K[i - 1], [t1, tgt, mode] = K[i];
      if (!resolved.has(i)) {
        const y0 = resolved.has(i - 1) ? resolved.get(i - 1) : lastY;
        let y1 = tgt == null ? y0 : typeof tgt === 'function' ? await tgt() : tgt;
        y1 = Math.max(0, Math.min(y1, await p.evaluate(() => window.__max())));
        if (!resolved.has(i - 1)) resolved.set(i - 1, y0);
        resolved.set(i, y1);
      }
      const y0 = resolved.get(i - 1), y1 = resolved.get(i), u = (s - t0) / (t1 - t0);
      return lerp(y0, y1, mode === 'lin' ? u : mode === 'soft' ? soft(u) : ease(u));
    }
    return resolved.get(K.length - 1) ?? lastY;
  }

  const total = Math.round(END * FPS), done = new Set();
  for (let f = 0; f < total; f++) {
    const s = f / FPS;
    lastY = await yAt(s);
    await p.evaluate(y => window.__scroll(y), lastY);
    let ind = null;
    for (const [ts, sel, fn] of T) {
      if (s < ts - .45 || s > ts + .35) continue;
      let [x, y] = await p.evaluate(q => window.__c(q), sel);
      if (fn === 'swipe') { const k = clamp01((s - (ts - .2)) / .55); x = lerp(VW * .78, VW * .2, ease(k)); await p.evaluate(k => { const r = document.getElementById('rail'); r.scrollLeft = k * (document.querySelector('#rail figure').getBoundingClientRect().width + 16); }, ease(k)); }
      const u = (s - (ts - .45)) / .45;
      ind = [x, y, s < ts ? Math.min(1, u * 2.2) : Math.max(0, 1 - (s - ts) / .35), s < ts ? 1.25 - .25 * Math.min(1, u * 1.4) : 1 - .22 * Math.sin(Math.min(1, (s - ts) / .2) * Math.PI)];
      if (s >= ts && !done.has(ts)) {
        done.add(ts);
        if (fn === 'fill') await p.evaluate(() => { document.getElementById('email').value = 'ana@example.com'; });
        else if (fn === 'swipe') {}
        else await p.evaluate(q => document.querySelector(q).dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })), sel);
      }
    }
    await p.evaluate(i => i ? window.__tap(i[0], i[1], i[2], i[3]) : window.__tap(0, 0, 0, 1), ind);
    await p.clock.runFor(1000 / FPS);
    await p.evaluate(dt => window.__step(dt), 1000 / FPS);
    await p.waitForTimeout(8);
    if (!ONLY || ONLY.includes(f)) await p.screenshot({ path: `${OUT}/f_${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 93 });
    if (f % 150 === 0) console.log('frame', f, '/', total, 't', s.toFixed(1));
  }
  await b.close();
})();
function clamp01(v){ return Math.min(1, Math.max(0, v)); }
