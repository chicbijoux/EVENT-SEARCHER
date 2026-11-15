# Amber Orbit promo video

A 31-second vertical (1080 × 1920) social video that walks through the Amber Orbit page on a
phone: age gate and hero, the scroll-driven pour film, the collection with add-to-box,
services, the event calculator, the cart, and a closing brand card. Silent by design, so a
trending sound can be added in the social app.

Final file: `renders/amber-orbit-promo.mp4`.

## How it is made

1. `tools/capture.js` records the live page at phone size, frame by frame, with scripted
   scrolling and taps. JavaScript time is faked and CSS animations are stepped by hand, so
   the recording is identical on every run.
2. `index.html` is a HyperFrames composition that places that recording in a phone frame
   and adds the captions, section progress bars and closing card.

## Re-rendering

`assets/screen.mp4` is not in git (20 MB). Rebuild it, then render:

```bash
# serve the page (from liquor-store/)
python3 -m http.server 8765 &

# record the phone session (needs Playwright with Chromium)
mkdir -p /tmp/ao-frames && node promo-video/tools/capture.js /tmp/ao-frames
ffmpeg -framerate 30 -i /tmp/ao-frames/f_%04d.jpg -c:v libx264 -preset slow -crf 14 \
  -pix_fmt yuv420p -g 15 promo-video/assets/screen.mp4

# check and render
cd promo-video && npm run check && npx hyperframes render --output renders/amber-orbit-promo.mp4 --crf 17
```

Captions and timings are at the bottom of `index.html`. If the page's layout changes, adjust
the scroll keyframes (`K`) and taps (`T`) in `tools/capture.js`.
