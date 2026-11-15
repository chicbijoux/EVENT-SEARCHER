# Media for the Amber Orbit page

Everything the page shows lives in `liquor-store/media/`. Work is on branch
`ccr-6d995c3c-l9pr03` of `chicbijoux/EVENT-SEARCHER`.

## What is in place

| File | Used for | Source |
| --- | --- | --- |
| `hero.webp` | Hero photo | Generated in ChatGPT |
| `box-spritz.webp`, `box-espresso.webp`, `box-flight.webp`, `box-agave.webp`, `box-zero.webp`, `box-rtd.webp` | The six collection cards | Generated in ChatGPT |
| `gift.webp` | Services section | Generated in ChatGPT |
| `events.webp` | Event bar background | Generated in ChatGPT |
| `og.jpg` | Link preview image | From the hero photo |
| `pour/d_0001.webp` … `d_0150.webp` | Scroll film, desktop (1600 × 900) | RunningHub, Seedance 2.5, 12 s clip |
| `pour/m_0001.webp` … `m_0120.webp` | Scroll film, portrait phones (608 × 1080 centre crop) | Same clip |
| `media.json` | Tells the page the film exists | Hand-written |

The photos are referenced directly in `index.html` (the `PACKS` list and the hero, services
and events `<img>` tags). The film is switched on by `media.json`:

```json
{"pour":{"count":150,"ext":"webp","prefix":"d_","mobile":{"count":120,"prefix":"m_"}}}
```

Set `media.json` to `{}` to turn the film off; the page then shows a drawn liquid effect instead.
The page must be served over http(s). Opened as a local file, browsers block `media.json`
and the film does not load.

## Replacing a photo

Convert to WebP and keep the same file name:

```bash
ffmpeg -i new.png -vf "scale=1200:-2" -c:v libwebp -quality 84 media/box-spritz.webp
```

Photo style used for every image: ultra-photorealistic luxury advertising photography, pure
black studio background, polished black stone surface, warm amber rim light, labels reading
"AMBER ORBIT" in fine serif lettering, no people, no other text. Landscape 3:2.

## Replacing the pour film

Source clip: 16:9, 1080p, about 12 seconds, one continuous shot with the glass centred:
pour into a tumbler with one large ice cube on slate, slow push-in over the rim, then a dive
into the amber liquid ending dark.

```bash
cd liquor-store/media && rm -f pour/*.webp
ffmpeg -i clip.mp4 -vf "fps=12.5,scale=1600:900:flags=lanczos" -c:v libwebp -quality 80 pour/d_%04d.webp
ffmpeg -i clip.mp4 -vf "fps=10,crop=608:1080" -c:v libwebp -quality 76 pour/m_%04d.webp
ls pour/d_* | wc -l   # desktop "count"
ls pour/m_* | wc -l   # mobile "count"
```

Then update the two counts in `media.json`.

RunningHub call used for the clip (needs an Enterprise-Shared API key and wallet balance;
the 12 s clip at upscaled 1080p cost $4.03):

- `POST https://www.runninghub.ai/openapi/v2/bytedance/seedance-2.5-token/text-to-video`
  with `resolution: "1080p"`, `duration: "12"`, `ratio: "16:9"`, `generateAudio: false`.
- Poll `POST /openapi/v2/query` with the `taskId` until `status` is `SUCCESS`.
- The result is hosted on `rh-hk-images-1252422369.cos.ap-hongkong.myqcloud.com`, which the
  cloud environment's network rules block; download it in a browser and upload it.
