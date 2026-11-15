# Real photos and footage for the Amber Orbit page

`index.html` shows drawn illustrations until real media exists. Put generated files in
`liquor-store/media/`, list them in `media/media.json`, and the page switches to them
automatically. Nothing else in the page needs editing.

Work lives on branch `ccr-6d995c3c-l9pr03` of `chicbijoux/EVENT-SEARCHER`.

## Rules for every shot

- Photoreal studio product photography, pure black background, warm amber rim light,
  soft reflection on a dark surface, shallow depth of field.
- Fictional brand only: label text "AMBER ORBIT" in a bold serif. No real brand names or logos.
- No people, no hands, no extra text or watermarks.

## 1. Hero photo → `media/hero.jpg` (16:9, at least 2048 × 1152)

> Three premium spirit bottles on a pure black background, studio product photography.
> Centre: a tall matte black bottle with a copper cap and a dark label reading "AMBER ORBIT",
> the largest of the three, its base in the lower middle of the frame. Left: a clear glass
> bottle of amber whisky with a cream label reading "AMBER ORBIT", next to a crystal rocks
> glass of whisky with one large clear ice cube. Right: a cream ceramic bottle with a dark
> label reading "AMBER ORBIT", next to a coupe glass holding an orange cocktail. Warm amber
> rim light, faint golden glow on the surface behind the bottles, floating ice cubes and a
> curl of orange peel in the air. Wide empty black margins on all sides. Photoreal, 85mm lens.

## 2. Box photos → `media/box-<id>.jpg` (16:10, at least 1600 × 1000)

Start every prompt with: *"Photoreal studio product photo on a pure black background, warm
amber rim light, gift box contents arranged in a row on a dark reflective surface, labels
reading "AMBER ORBIT":"*

| File | Add to the prompt |
| --- | --- |
| `box-spritz.jpg` | a bottle of bright orange aperitivo, a green bottle of prosecco with gold foil, a small bottle of soda, two balloon wine glasses filled with orange spritz, ice and an orange slice |
| `box-espresso.jpg` | a clear bottle of vodka, a dark bottle of coffee liqueur, a small bottle of cold-brew coffee, a steel cocktail shaker, a coupe glass with an espresso martini topped with foam and three coffee beans |
| `box-flight.jpg` | five identical 50 ml miniature whisky bottles in a row, liquid going from pale gold to deep mahogany, with small printed tasting cards in front |
| `box-agave.jpg` | three small matching bottles: clear tequila blanco, golden reposado, smoky grey mezcal, with a dish of chilli salt and a cut lime |
| `box-zero.jpg` | a pale green bottle of alcohol-free botanical spirit, a coral bottle of alcohol-free aperitivo, a cream can of sparkling tea, a rocks glass with a pink drink and ice, a small "0%" tag |
| `box-rtd.jpg` | three small flat flask bottles of pre-mixed cocktails in deep red, amber and dark ruby, next to a rocks glass with a red negroni, a large ice cube and orange peel |

## 3. Pour footage (16:9, 1080p, two clips of 5 to 8 seconds)

First generate the opening still, then use it as the start frame of clip A.

**Start frame → `media/src/pour-start.jpg`**

> An empty crystal whisky tumbler with one large clear ice cube, standing on a dark slate
> stone plinth, pure black background, warm amber rim light. The glass sits slightly right
> of centre (about 62% across the frame) and is vertically centred. Photoreal, 16:9.

**Clip A → `media/src/pour-a.mp4`** (image-to-video from the start frame)

> A thin, smooth stream of amber whisky pours from above the frame into the tumbler and
> fills it to about two thirds. The ice cube lifts and turns. The camera pushes in slowly
> and steadily toward the glass until the liquid surface fills the frame. Slow motion,
> no cuts, no hands, no bottle visible.

**Clip B → `media/src/pour-b.mp4`** (start from the last frame of clip A)

> Extreme macro, looking down at amber whisky swirling in a slow spiral around an ice cube,
> glossy highlights on the surface. The camera sinks through the surface into the liquid:
> golden light caustics ripple across the frame and small bubbles rise. Ends in deep, dark
> amber. Slow motion, no cuts.

Turn the two clips into the scroll sequence:

```bash
cd liquor-store/media
printf "file 'src/pour-a.mp4'\nfile 'src/pour-b.mp4'\n" > src/list.txt
mkdir -p pour
ffmpeg -f concat -safe 0 -i src/list.txt -vf "fps=15,scale=1280:-2" -q:v 5 pour/f_%04d.jpg
ls pour | wc -l    # this number is "count" below
```

## 4. Tell the page what exists → `media/media.json`

Only list files that are really there. An empty `{}` keeps the illustrations.

```json
{
  "hero": "hero.jpg",
  "boxes": {
    "spritz": "box-spritz.jpg", "espresso": "box-espresso.jpg", "flight": "box-flight.jpg",
    "agave": "box-agave.jpg", "zero": "box-zero.jpg", "rtd": "box-rtd.jpg"
  },
  "pour": { "count": 150, "ext": "jpg" }
}
```

## What the page does with them

- **Hero photo:** fills the hero and hides the drawn bottles. The glowing orbit arcs,
  floating ice and the button stay on top. The arc position will need a small adjustment
  once the real photo is in.
- **Box photos:** replace the drawn art on each card.
- **Pour frames:** play forward and backward as the visitor scrolls. The ring opening, the
  headline, the angled labels and the closing circle are still drawn by the page on top.
- The page must be opened from a web server (any host, or `python3 -m http.server`).
  Opened as a local file, browsers block the media list and the illustrations stay.

## Generating with RunningHub (runninghub.ai)

Chosen route: GPT Image 2 for the photos, Seedance 2.5 for the pour clips. Needs an
**Enterprise-Shared** API key from the RunningHub API Key page (the other key types cannot
call these models). Never put the key in this repo or in chat.

- Auth: `Authorization: Bearer <key>`, host `www.runninghub.ai`.
- Photos: `POST /openapi/v2/rhart-image-g-2-official/text-to-image` with
  `{"prompt": "...", "aspectRatio": "16:9", "resolution": "2k", "quality": "high"}`.
- Pour clips: `POST /openapi/v2/bytedance/seedance-2.5-token/image-to-video` with
  `{"prompt": "...", "firstFrameUrl": "<photo result url>", "lastFrameUrl": "<optional>",
  "resolution": "1080p", "duration": "8", "ratio": "adaptive", "generateAudio": false,
  "watermark": false}`.
- Each call returns a `taskId`. Poll `POST /openapi/v2/query` with `{"taskId": "..."}` until
  `status` is `SUCCESS`, then download `results[].url`. `usage.consumeMoney` is the cost.
- Prices are not listed in the API docs; check the first task's `usage` before running the rest.
- Alternatives if Seedance disappoints: `rhart-video-v3.1-pro-official/image-to-video`
  (Veo 3.1 Pro) or `kling-v3-4k/image-to-video`.
