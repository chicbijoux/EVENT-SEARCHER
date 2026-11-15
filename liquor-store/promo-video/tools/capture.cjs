// Deterministic phone-screen capture of the Amber Orbit page: JS time is faked, CSS animations are stepped by hand.
const { chromium } = require('playwright');
const fs = require('fs');
// Optional env: VW, VH (CSS viewport), DSF (pixel density), END (seconds). Defaults record a 390x844 phone at 2x for 27.6 s.
const VW = +(process.env.VW || 390), VH = +(process.env.VH || 844), DSF = +(process.env.DSF || 2), END = +(process.env.END || 27.6);
const FPS = 30, OUT = process.argv[2], MAXF = +(process.argv[3] || 1e9), ONLY = process.argv[4] ? process.argv[4].split(',').map(Number) : null;
const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
const lerp = (a, b, t) => a + (b - a) * t;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: DSF });
  const p = await ctx.newPage();
  await p.clock.install({ time: new Date('2026-11-15T12:00:00') });
  await p.addInitScript(() => { try { localStorage.removeItem('ao-age'); } catch (e) {} });
  await p.goto('http://localhost:8765/index.html', { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: `html{scroll-behavior:auto!important} ::-webkit-scrollbar{display:none}
    #__tap{position:fixed;left:0;top:0;width:54px;height:54px;margin:-27px 0 0 -27px;border-radius:50%;background:rgba(255,255,255,.28);border:1.5px solid rgba(255,255,255,.75);box-shadow:0 4px 18px rgba(0,0,0,.35);z-index:9999;opacity:0;pointer-events:none}` });
  await p.evaluate(() => {
    const t = document.createElement('div'); t.id = '__tap'; document.body.appendChild(t);
    const held = new WeakSet();
    window.__step = dt => { for (const a of document.getAnimations()) { if (!held.has(a)) { a.pause(); held.add(a); } else { a.currentTime = (a.currentTime || 0) + dt; } } };
    window.__tap = (x, y, o, s) => { t.style.transform = `translate(${x}px,${y}px) scale(${s})`; t.style.opacity = o; };
    window.__scroll = y => { window.scrollTo(0, y); window.dispatchEvent(new Event('scroll')); };
    window.__c = sel => { const r = document.querySelector(sel).getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };
  });
  await p.waitForTimeout(2500);                       // let every film frame and photo finish loading (real time)
  const L = await p.evaluate(() => { const top = s => Math.round(document.querySelector(s).getBoundingClientRect().top + scrollY); const pe = document.querySelector('#pour');
    return { pourTop: pe.offsetTop, span: pe.offsetHeight - innerHeight, boxes: top('#boxes'), card1: top('#grid .card:nth-child(1)'), card3: top('#grid .card:nth-child(3)'), services: top('#services'), svcList: top('#svc'), calc: top('.calc'), max: document.documentElement.scrollHeight - innerHeight }; });
  console.log(JSON.stringify(L));
  const P = q => L.pourTop + L.span * q;
  // scroll keyframes: [seconds, y]
  const K = [[0, 0], [3.5, 0], [3.95, P(0)], [5.4, P(.19)], [7.5, P(.42)], [10.2, P(.71)], [12.1, P(.875)], [13.0, P(1)], [13.75, L.boxes + 40], [14.55, L.card1 - 96], [15.5, L.card1 - 96], [17.1, L.card3 - 96], [17.7, L.card3 - 96],
             [18.45, L.services - 70], [18.8, L.services - 70], [20.5, L.svcList + 250], [21.25, L.calc - 170], [END, L.calc - 170]];
  const yAt = s => { for (let i = 1; i < K.length; i++) if (s <= K[i][0]) { const [t0, y0] = K[i-1], [t1, y1] = K[i]; const u = (s - t0) / (t1 - t0); const lin = i >= 3 && i <= 7; return lerp(y0, y1, lin ? u : ease(u)); } return K[K.length-1][1]; };
  // taps: [seconds, selector, action]
  const T = [[0.85, '#gate-yes', () => document.getElementById('gate-yes').click()],
             [15.0, '#grid .card:nth-child(1) [data-add]', () => document.querySelector('#grid .card:nth-child(1) [data-add]').click()],
             [17.35, '#grid .card:nth-child(3) [data-add]', () => document.querySelector('#grid .card:nth-child(3) [data-add]').click()],
             [24.0, '#types button:nth-child(2)', () => document.querySelector('#types button:nth-child(2)').click()],
             [25.2, '#cart-btn', () => document.getElementById('cart-btn').click()]];
  const DRAG = [21.8, 23.4, 80, 200];                 // slider drag: start s, end s, from, to
  const total = Math.min(MAXF, Math.round(END * FPS));
  const done = new Set();
  for (let f = 0; f < total; f++) {
    const s = f / FPS;
    await p.evaluate(y => window.__scroll(y), yAt(s));
    // tap indicator
    let tap = null;
    for (const [ts, sel, fn] of T) {
      if (s >= ts - .45 && s <= ts + .3) { const [x, y] = await p.evaluate(q => window.__c(q), sel); const u = (s - (ts - .45)) / .45; tap = [x, y, s < ts ? Math.min(1, u * 2.2) : Math.max(0, 1 - (s - ts) / .3), s < ts ? 1.25 - .25 * Math.min(1, u * 1.4) : 1 - .22 * Math.sin(Math.min(1, (s - ts) / .2) * Math.PI)]; }
      if (s >= ts && !done.has(ts)) { done.add(ts); await p.evaluate(fn); }
    }
    if (s >= DRAG[0] - .4 && s <= DRAG[1] + .3) {
      const u = ease(Math.min(1, Math.max(0, (s - DRAG[0]) / (DRAG[1] - DRAG[0])))); const v = Math.round(lerp(DRAG[2], DRAG[3], u) / 5) * 5;
      const pos = await p.evaluate(v => { const el = document.getElementById('guests'); if (+el.value !== v) { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); } const r = el.getBoundingClientRect(); const k = (v - el.min) / (el.max - el.min); return [r.left + 9 + k * (r.width - 18), r.top + r.height / 2]; }, v);
      tap = [pos[0], pos[1], s < DRAG[0] ? Math.min(1, (s - (DRAG[0] - .4)) / .25) : s > DRAG[1] ? Math.max(0, 1 - (s - DRAG[1]) / .3) : 1, s >= DRAG[0] && s <= DRAG[1] ? .85 : 1];
    }
    await p.evaluate(t => t ? window.__tap(t[0], t[1], t[2], t[3]) : window.__tap(0, 0, 0, 1), tap);
    await p.clock.runFor(1000 / FPS);
    await p.evaluate(dt => window.__step(dt), 1000 / FPS);
    await p.waitForTimeout(8);
    if (!ONLY || ONLY.includes(f)) await p.screenshot({ path: `${OUT}/f_${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 93 });
    if (f % 90 === 0) console.log('frame', f, '/', total);
  }
  await b.close();
})();
