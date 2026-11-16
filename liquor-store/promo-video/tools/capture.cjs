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
    const tops = q => [...document.querySelectorAll(q)].map(e => Math.round(e.getBoundingClientRect().top + scrollY));
    return { pourTop: pe.offsetTop, span: pe.offsetHeight - innerHeight, boxes: top('#boxes'), cards: tops('#grid .card'), services: top('#services'), svcList: top('#svc'), rows: tops('#svc .svc-row'), events: top('#events'), calc: top('.calc'), max: document.documentElement.scrollHeight - innerHeight }; });
  console.log(JSON.stringify(L));
  const P = q => L.pourTop + L.span * q;
  const click = sel => [sel, new Function(`document.querySelector(${JSON.stringify(sel)}).click()`)];
  // K: scroll keyframes [seconds, y, 'ease'|'lin'] · T: taps [seconds, selector, action] · DRAG: slider [start s, end s, from, to]
  let K = [[0, 0, 'ease']], T = [], DRAG, endAt, t = 0;
  const hold = d => { t += d; K.push([t, K[K.length - 1][1], 'ease']); };
  const go = (y, d, mode = 'ease') => { t += d; K.push([t, Math.min(y, L.max), mode]); };
  const tap = (sel, dt = 0) => T.push([t + dt, ...click(sel)]);
  if (process.env.PLAN === 'long') {
    // Reading pace: every heading, card and price is held long enough to read.
    tap('#gate-yes', 1.8); hold(6.6);                                   // age gate, then the hero
    go(P(0), 0.6);
    go(P(.12), 1.6, 'lin'); go(P(.30), 2.2, 'lin');                     // ring opens
    go(P(.375), 3.4, 'lin');                                            // "Twelve years in oak."
    go(P(.56), 3.0, 'lin');
    go(P(.645), 4.2, 'lin');                                            // "Poured slow. Savoured longer."
    go(P(.775), 2.2, 'lin'); go(P(.83), 4.2, 'lin');                    // the three labels
    go(P(.9), 1.4, 'lin'); go(P(1), 2.2, 'lin'); hold(1.8);             // circle opens on the collection title
    go(L.boxes + 30, 0.9); hold(3.6);                                   // collection heading and intro
    [3.4, 2.5, 3.4, 2.3, 2.3, 2.5].forEach((h, i) => { go(L.cards[i] - 84, 0.9); if (i === 0 || i === 2) tap(`#grid .card:nth-child(${i + 1}) [data-add]`, 1.7); hold(h); });
    go(L.services - 60, 1.0); hold(3.2);                                // services photo and heading
    go(L.rows[0] - 96, 0.9); tap('#svc .svc-row:nth-child(2) [data-add]', 1.9); hold(3.8);
    go(L.rows[3] - 96, 0.9); hold(3.8);
    go(L.events + 36, 1.0); hold(4.4);                                  // event bar heading and promises
    go(L.calc - 150, 0.9); hold(1.3);
    DRAG = [t, t + 2.6, 80, 200]; hold(2.6); hold(2.3);
    tap('#types button:nth-child(2)'); hold(2.5);
    tap('#types button:nth-child(3)'); hold(2.4);
    tap('#cart-btn'); hold(4.8);                                        // the box with three items
    endAt = t;
  } else if (process.env.PLAN === 'mid') {
    // 45-second cut: the same stops as the long plan, held just long enough to take in.
    tap('#gate-yes', 1.2); hold(4.8);
    go(P(0), 0.5);
    go(P(.12), 1.0, 'lin'); go(P(.30), 1.3, 'lin'); go(P(.375), 2.0, 'lin'); go(P(.56), 1.8, 'lin');
    go(P(.645), 2.4, 'lin'); go(P(.775), 1.3, 'lin'); go(P(.83), 2.0, 'lin'); go(P(.9), 0.8, 'lin'); go(P(1), 1.2, 'lin'); hold(0.4);
    go(L.boxes + 30, 0.7); hold(1.6);
    go(L.cards[0] - 84, 0.6); tap('#grid .card:nth-child(1) [data-add]', 0.9); hold(1.8);
    go(L.cards[1] - 84, 0.6); hold(1.0);
    go(L.cards[2] - 84, 0.6); tap('#grid .card:nth-child(3) [data-add]', 0.9); hold(1.8);
    go(L.cards[5] - 84, 1.9, 'lin'); hold(0.5);                          // boxes four to six in one pass
    go(L.services - 60, 0.7); hold(1.2);
    go(L.rows[0] - 96, 0.6); tap('#svc .svc-row:nth-child(2) [data-add]', 0.9); hold(2.0);
    go(L.events + 36, 0.7); hold(1.3);
    go(L.calc - 150, 0.7); hold(0.5);
    DRAG = [t, t + 1.6, 80, 200]; hold(1.6); hold(1.2);
    tap('#types button:nth-child(2)'); hold(1.4);
    tap('#cart-btn'); hold(Math.max(2.6, 45 - t));                      // pad the cart so the cut lands on 45 s
    endAt = t;
  } else {
    T = []; K = [[0, 0], [3.5, 0], [3.95, P(0)], [5.4, P(.19), 'lin'], [7.5, P(.42), 'lin'], [10.2, P(.71), 'lin'], [12.1, P(.875), 'lin'], [13.0, P(1), 'lin'], [13.75, L.boxes + 40], [14.55, L.cards[0] - 96], [15.5, L.cards[0] - 96], [17.1, L.cards[2] - 96], [17.7, L.cards[2] - 96],
         [18.45, L.services - 70], [18.8, L.services - 70], [20.5, L.svcList + 250], [21.25, L.calc - 170], [END, L.calc - 170]];
    T = [[0.85, ...click('#gate-yes')], [15.0, ...click('#grid .card:nth-child(1) [data-add]')], [17.35, ...click('#grid .card:nth-child(3) [data-add]')], [24.0, ...click('#types button:nth-child(2)')], [25.2, ...click('#cart-btn')]];
    DRAG = [21.8, 23.4, 80, 200]; endAt = END;
  }
  const yAt = s => { for (let i = 1; i < K.length; i++) if (s <= K[i][0]) { const [t0, y0] = K[i-1], [t1, y1, mode] = K[i]; const u = (s - t0) / (t1 - t0); return lerp(y0, y1, mode === 'lin' ? u : ease(u)); } return K[K.length-1][1]; };
  console.log('length', endAt.toFixed(1), 's');
  const total = Math.min(MAXF, Math.round(endAt * FPS));
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
