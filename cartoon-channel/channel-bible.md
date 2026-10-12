# Channel bible: Leo & Bibo

The rules every Short follows. Paste this whole file into Claude whenever you ask for new episodes.

## Identity

- **Channel name:** Leo & Bibo
- **Tagline:** Bip-bip! Learning songs on the magic bus
- **Audience:** kids aged 2–6 (and the parents who press play)
- **Niche:** nursery rhymes & learning songs: counting, colors, shapes, opposites, animal sounds, simple habits (sharing, washing, bedtime)
- **Language:** English, kept very simple. The stories work without words, and the animal sounds and the horn carry them in any country.

## The cast (never changes)

| Character | Role | Signature |
|---|---|---|
| **Leo** (boy, 4) | The hero. Curious, cheerful, counts everything on his fingers | Holds up fingers to count; the catchphrase *"Bip-bip, here we go!"* |
| **Bibo** (toy bus) | Leo's magic toy bus. No face: he "talks" by blinking his headlights, bouncing on his wheels and honking | The horn: *"bip-bip!"* |
| **Tofu** (puppy) | Leo's puppy and the comic relief. Always rides at the front window | Ears flapping in the wind; one "Woof!" at every stop |

Exact visual descriptions are in [`characters.md`](characters.md). Paste them word for word.

> **Why Bibo has no face:** most cartoon buses and cars have eyes on the windshield.
> Keeping Bibo faceless (headlights that blink) makes him ours, and he's also much easier for
> the video model to keep consistent.

## The world

- **Leo's backyard:** sunny lawn, grey stone path with a chalk-drawn road, white picket fence, round green bushes, and a white garden gate that opens onto the road. Every episode starts and ends here.
- **Lollipop Hills:** a winding road through rolling green hills with round, lollipop-shaped trees, a blue pond, a lily pond, a sunflower field and puffy white clouds.
- **Bus stops:** round sky-blue signs, each showing one big white number, shape or color. They're perfect for the lesson of the day.

## The ritual (in every episode)

1. **Hook (0–3 s):** motion plus a face. Bibo zooms at the camera, the horn honks, Leo laughs.
2. **"Bip, bip, BIG!"** Leo honks three times, golden sparkles swirl, and Bibo grows into a real bus.
3. **Three stops, one lesson.** Each stop adds one thing (a passenger, a color, a shape), and each stop repeats the **sing-along line**.
4. **The ride.** Everyone waves out of the windows, and the lesson gets one recap line.
5. **"Bip, bip, small!"** Back in the backyard, Bibo shrinks into Leo's hands and the Short ends on a close-up of toy Bibo, just like the hook opens, so it loops.

## Style lock

Paste this at the end of **every image prompt**. Video prompts carry a short version of it.

```
Bright 3D animated kids' cartoon, soft rounded shapes, smooth matte clay-like textures, big expressive eyes, warm soft sunlight, gentle shadows, saturated candy colors, clean simple background, cheerful and safe mood.
```

**Palette:** cherry red (Bibo), sky blue (Leo's shirt, bus-stop signs, Bibo's seats), sunny yellow (headlights, steering wheel), grass green, cream white (Tofu).

## Negative prompt

Use it in Wan2GP's negative prompt field for every clip and image.

```
blurry, low quality, flicker, distorted face, extra fingers, extra limbs, deformed hands, extra wheels, melted wheels, face on the bus, eyes on the windshield, mouth on the bus, watermark, logo, subtitles, random text, realistic photo, dark, scary, sad
```

## Render settings

| Setting | Value |
|---|---|
| Mode | Image-to-video (start frame plus prompt) |
| Aspect | 9:16 vertical (720p if your GPU allows it, otherwise 480p) |
| Scene length | 5 s (≈ 121 frames at 24 fps); the hook is 3 s (≈ 73 frames) |
| Clip audio | Sound effects only. The song is one separate track added in CapCut |
| Total length | 28–35 s |

## Rules to stay monetizable

- Every Short gets a **real little story, a new song or lesson, and our own characters.**
- **Never** use Disney, Pixar or any other famous characters, songs, names or styles in prompts, and never reupload anyone else's videos.
- **Take the pattern, never the content.** When copying what wins (prompt 2 in `claude-prompts.md`), new stories and new songs only.
- Mark every upload as **Made for kids**.
