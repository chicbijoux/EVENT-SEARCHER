// Deterministic full-frame phone recording of the Shionagi page.
// JavaScript time is faked and CSS animations are stepped by hand, so every run gives the same frames.
// Usage: node omakase/tools/capture.cjs <frames-dir> [url]   (serve omakase/ first, e.g. python3 -m http.server 8770)
// Env: VW, VH (CSS viewport), DSF (pixel density). Defaults record 432x768 at 2.5x = 1080x1920.
const { chromium } = require('playwright');
const VW = +(process.env.VW || 432), VH = +(process.env.VH || 768), DSF = +(process.env.DSF || 2.5);
const FPS = 30, OUT = process.argv[2], URL = process.argv[3] || 'http://localhost:8770/index.html';
const ONLY = process.env.ONLY ? process.env.ONLY.split(',').map(Number) : null;
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const lerp = (a, b, t) => a + (b - a) * t;

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: DSF, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  await p.clock.install({ time: new Date('2026-11-17T12:00:00') });
  await p.addInitScript(() => { try { sessionStorage.setItem('sn-intro', '1'); } catch (e) {} });
  await p.goto(URL, { waitUntil: 'networkidle' });
  await p.waitForTimeout(4000);                                   // let photos and film frames load (real time)
  // Freeze time, then replay the opening curtain from the start under our control.
  const now = await p.evaluate(() => Date.now());
  await p.clock.pauseAt(new Date(now + 1000));
  await p.addStyleTag({ content: `html{scroll-behavior:auto!important} ::-webkit-scrollbar{display:none}
    #__tap{position:fixed;left:0;top:0;width:54px;height:54px;margin:-27px 0 0 -27px;border-radius:50%;background:rgba(255,255,255,.3);border:1.5px solid rgba(255,255,255,.8);box-shadow:0 4px 18px rgba(0,0,0,.35);z-index:9999;opacity:0;pointer-events:none}` });
  await p.evaluate(() => {
    const t = document.createElement('div'); t.id = '__tap'; document.body.appendChild(t);
    const held = new WeakSet();
    window.__step = dt => { for (const a of document.getAnimations()) { if (!held.has(a)) { a.pause(); held.add(a); } else { a.currentTime = (a.currentTime || 0) + dt; } } };
    window.__tap = (x, y, o, s) => { t.style.transform = `translate(${x}px,${y}px) scale(${s})`; t.style.opacity = o; };
    window.__scroll = y => { window.scrollTo(0, y); window.dispatchEvent(new Event('scroll')); };
    window.__c = sel => { const r = document.querySelector(sel).getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };
    window.__top = sel => Math.round(document.querySelector(sel).getBoundingClientRect().top + scrollY);
    window.__max = () => document.documentElement.scrollHeight - innerHeight;
    // replay the intro
    window.__scroll(0);
    const html = document.documentElement, noren = document.getElementById('noren');
    document.body.classList.remove('ready'); noren.classList.remove('open'); html.classList.add('intro');
    setTimeout(() => { noren.classList.add('open'); document.body.classList.add('ready'); }, 1250);
    setTimeout(() => html.classList.remove('intro'), 2700);
  });

  // ---------- the plan: K = scroll keyframes [t, target, 'ease'|'lin'], T = taps [t, selector, action] ----------
  const film = await p.evaluate(() => { const f = document.getElementById('film-sec'); return { top: f.offsetTop, span: f.offsetHeight - innerHeight }; });
  const P = q => film.top + film.span * q, A = .03, Q = (.97 - .03) / 4;
  const K = [[0, 0]]; const T = []; let t = 0;
  const hold = d => { t += d; K.push([t, null]); };                 // null = stay where we are
  const go = (y, d, mode) => { t += d; K.push([t, y, mode]); };     // y: number or a function evaluated when the move starts
  const tap = (sel, fn, dt = 0) => T.push([t + dt, sel, fn]);
  const at = (sel, off = 0) => async () => (await p.evaluate(s => window.__top(s), sel)) + off;

  hold(4.1);                                                        // curtain parts, hero settles
  go(at('#arrival', -64), 1.0); hold(2.2);                          // 18:40 arrival in the rain
  go(at('.film-intro', -40), 1.0); hold(1.1);                        // 19:00 one piece, in four movements
  go(P(0), .7);
  for (let i = 0; i < 4; i++) { go(P(A + Q * (i + .62)), 2.0, 'lin'); hold(.5); }   // catch, knife, rice, serve
  go(P(1), 1.0, 'lin');
  go(at('#courses', -40), .9); hold(1.0);                          // fifteen courses
  go(at('.course', -150), .7);
  go(async () => p.evaluate(() => { const c = [...document.querySelectorAll('.course')].pop(); return c.getBoundingClientRect().top + scrollY - 150; }), 5.8, 'lin'); hold(.4);   // the clock runs through the evening
  go(at('#reserve', -50), 1.0); hold(.7);                           // choose your seat
  go(at('#dates', -170), .7);
  tap('#dates .date:nth-child(3)', 'click', .3); hold(1.0);
  go(at('.counter', -90), .8);
  tap('__seat', 'seat', .3); hold(1.1);                              // a centre seat, the view appears
  go(at('#seat-view', -150), .8); hold(1.0);
  go(at('#pairs', -260), .7);
  tap('#pairs .opt:nth-child(2)', 'click', .2); hold(.6);
  tap('#f-name', 'fill', 0); go(at('#summary', -80), 1.0);
  tap('#hold', 'click', .3); hold(1.3);                              // seats held
  go(async () => { const c = await p.evaluate(() => { const e = document.getElementById('closing'); return { top: e.offsetTop, h: e.offsetHeight }; }); return c.top + (c.h - VH) * .97; }, 1.9);
  hold(Math.max(.8, 45 - t));                                        // the curtain closes; pad to 45 s
  const END = 45;

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
      return lerp(y0, y1, mode === 'lin' ? u : ease(u));
    }
    return resolved.get(K.length - 1) ?? lastY;
  }
  // pick a free seat in the middle of the counter once the evening is chosen
  const seatSel = async () => { const s = await p.evaluate(() => { const f = [...document.querySelectorAll('.counter .v .seat:not(.taken)')].map(g => +g.dataset.s); return f.find(n => n >= 4 && n <= 7) || f[0]; }); return `.counter .v .seat[data-s="${s}"]`; };

  const total = Math.round(END * FPS), done = new Set(), sel = {};
  for (let f = 0; f < total; f++) {
    const s = f / FPS;
    lastY = await yAt(s);
    await p.evaluate(y => window.__scroll(y), lastY);
    let ind = null;
    for (const [ts, key, fn] of T) {
      if (s < ts - .45 || s > ts + .3) continue;
      if (!sel[key]) sel[key] = key === '__seat' ? await seatSel() : key;
      const [x, y] = await p.evaluate(q => window.__c(q), sel[key]);
      const u = (s - (ts - .45)) / .45;
      ind = [x, y, s < ts ? Math.min(1, u * 2.2) : Math.max(0, 1 - (s - ts) / .3), s < ts ? 1.25 - .25 * Math.min(1, u * 1.4) : 1 - .22 * Math.sin(Math.min(1, (s - ts) / .2) * Math.PI)];
      if (s >= ts && !done.has(ts)) {
        done.add(ts);
        if (fn === 'fill') await p.evaluate(() => { document.getElementById('f-name').value = 'Ana Popescu'; document.getElementById('f-email').value = 'ana@example.com'; });
        else await p.evaluate(q => { const el = document.querySelector(q); el.dispatchEvent(new MouseEvent('click', { bubbles: true })); }, sel[key]);
      }
    }
    await p.evaluate(i => i ? window.__tap(i[0], i[1], i[2], i[3]) : window.__tap(0, 0, 0, 1), ind);
    await p.clock.runFor(1000 / FPS);
    await p.evaluate(dt => window.__step(dt), 1000 / FPS);
    await p.waitForTimeout(8);
    if (!ONLY || ONLY.includes(f)) await p.screenshot({ path: `${OUT}/f_${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 93 });
    if (f % 150 === 0) console.log('frame', f, '/', total, 't', s.toFixed(1));
  }
  console.log('plan length', t.toFixed(1), 's');
  await b.close();
})();
