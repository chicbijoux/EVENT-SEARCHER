# Media for the Shionagi page

`index.html` shows a labelled placeholder wherever a photo is missing, and a drawn brush
circle in place of the scroll film. Drop the files below into `omakase/media/` with these
exact names and the page picks them up. Convert to WebP first (see the end).

Work lives on branch `ccr-6d995c3c-l9pr03` of `chicbijoux/EVENT-SEARCHER`.

## Photos (ChatGPT, landscape 3:2)

Paste this first, in one chat:

```
I'm going to ask for a series of photos for one premium Japanese omakase restaurant. Use this style for every image in this chat: ultra-photorealistic fine-dining photography, medium-format camera, 85mm lens, soft warm low-key light, pale hinoki wood counter, dark charcoal background, shallow depth of field, calm and precise. Landscape format, 3:2. No people's faces, no text, no lettering, no logos, no watermark. Reply "ready" and wait for my first request.
```

| File | Where it appears | Prompt |
| --- | --- | --- |
| `hero.webp` | Hero | An empty ten-seat omakase counter of pale hinoki wood in a quiet, dimly lit room. A single piece of tuna nigiri on a small matte black plate in the foreground. Soft pools of warm light fall from above onto each seat. Dark charcoal walls, a white linen curtain far in the background. Wide composition with generous empty space above. |
| `door.webp` | 18:40 Arrival | The entrance of a small Japanese restaurant at dusk: a sliding wooden door with a plain white linen noren curtain in the doorway, warm light glowing from inside, a stone path wet from rain, a small paper lantern beside the door. No signs, no lettering. |
| `hands.webp` | 21:05 The last word | Close-up of a sushi chef's hands at the hinoki counter, seen from the chest down in a white chef's jacket, placing a piece of nigiri onto a small black ceramic plate. No face visible. |
| `otoro.webp` | Course 07 | A single piece of otoro (fatty bluefin tuna) nigiri on a matte black ceramic plate on pale hinoki wood, glossy marbling catching the light, a small dab of fresh wasabi beside it. |
| `uni.webp` | Course 09 | A hand roll of crisp seaweed filled with golden sea urchin (uni) over rice, resting in a small wooden holder on the hinoki counter. |
| `wagyu.webp` | Course 11 | A piece of seared wagyu beef nigiri with a light torched crust and a few flakes of sea salt, a thin wisp of smoke rising, on a matte black plate. |
| `yuzu.webp` | Course 15 | A small dessert: a smooth quenelle of pale yellow yuzu sorbet in a hand-thrown grey ceramic bowl, a thin curl of yuzu zest on top. |
| `sake.webp` | Pairing | Three sake bottles of plain unlabelled glass and two small ceramic sake cups on the hinoki counter, clear sake being poured into one cup. |
| `private.webp` | Private counter | A private omakase room: a short hinoki counter with six seats, set with black plates and chopsticks on stone rests, warm light, a low window with a view of a small moss garden at night. |

## Scroll film (RunningHub, about $4)

Seedance 2.5, text to video, 16:9, 1080p, 12 seconds, audio off. The page splits the clip
into four equal chapters (0–3 s The Catch, 3–6 s The Knife, 6–9 s The Rice, 9–12 s The Serve),
so keep the timestamps.

```
Photoreal cinematic food film for a high-end omakase sushi counter, slow motion, warm low-key light, pale hinoki wood counter, dark charcoal background, shallow depth of field, macro lens. [00:00-00:03] A glistening block of deep red bluefin tuna rests on crushed ice beside a leaf of green shiso, cold mist drifting across the ice, the camera glides slowly along it. [00:03-00:06] A long single-bevel sushi knife draws through the tuna in one smooth stroke and a perfect slice peels away, light catching the marbling. [00:06-00:09] A chef's hands press a small mound of glossy vinegared rice, then lay the tuna slice over it and shape the nigiri with two fingers. [00:09-00:12] The finished nigiri is set down on a matte black ceramic plate on the hinoki counter, a small brush paints a thin gloss of soy across the top, the camera settles in a slow push-in and holds. Style: Japanese fine-dining commercial, calm and precise, realistic textures. Avoid: faces, text, logos, watermarks, extra fingers, deformed hands, camera shake, flicker.
```

Turn the clip into frames and switch the film on:

```bash
cd omakase/media && mkdir -p film
ffmpeg -i clip.mp4 -vf "fps=12.5,scale=1600:900:flags=lanczos" -c:v libwebp -quality 80 film/d_%04d.webp
ffmpeg -i clip.mp4 -vf "fps=10,crop=608:1080" -c:v libwebp -quality 76 film/m_%04d.webp
ls film/d_* | wc -l; ls film/m_* | wc -l     # the two counts below
echo '{"film":{"count":150,"ext":"webp","prefix":"d_","mobile":{"count":120,"prefix":"m_"}}}' > media.json
```

The film only loads when the page is served over http(s), not opened as a local file.

## Converting photos

```bash
ffmpeg -i photo.png -vf "scale=1536:-2" -c:v libwebp -quality 84 omakase/media/hero.webp
```

## What to edit in the page

At the top of the script in `index.html`: price per guest (`OMAKASE`), seats (`SEATS`), the
online party limit (`MAX_ONLINE`) and the fifteen courses with their times. `takenFor()` stands
in for a real booking system; replace it with availability from yours.
