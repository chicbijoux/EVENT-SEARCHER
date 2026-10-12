# Leo & Bibo — AI Cartoon Channel

A faceless kids' 3D cartoon channel built on the *AI Cartoon Channel System*
(Claude writes the Shorts → Wan2GP animates them locally for free → CapCut → YouTube Shorts).

**The idea:** Leo, a 4-year-old boy, has a little red toy bus called **Bibo**. When Leo honks
Bibo's horn three times — *"Bip, bip, BIG!"* — Bibo grows into a real bus, and Leo, his puppy
**Tofu** and a new set of animal friends ride off on a tiny adventure with one simple lesson and
one catchy sing-along line.

- **Niche:** nursery rhymes & learning songs (counting, colors, shapes, opposites, animal sounds)
- **Format:** vertical 9:16 Shorts, ~30 s, a 3 s hook and then 5 s scenes
- **Cast (forever):** Leo, Bibo, Tofu. Same look and same colors in every Short.

## What's in here

| File | What it is |
|---|---|
| [`SETUP.md`](SETUP.md) | Checklist for setting up the free video studio on your PC, plus the YouTube channel |
| [`channel-bible.md`](channel-bible.md) | Channel rules: world, recurring ritual, style lock, negative prompt, render settings |
| [`characters.md`](characters.md) | Locked character descriptions and character-sheet image prompts |
| [`claude-prompts.md`](claude-prompts.md) | Copy-paste Claude prompts for writing a week of Shorts, copying what wins, and fixing scenes |
| [`episodes/001-bip-bip-counting-bus/script.md`](episodes/001-bip-bip-counting-bus/script.md) | **Episode 1:** story, shot list, song lyrics, edit notes, title and thumbnail |
| [`episodes/001-bip-bip-counting-bus/scene-prompts.md`](episodes/001-bip-bip-counting-bus/scene-prompts.md) | **Episode 1:** start-frame image prompt and LTX-2.5 video prompt for each scene |
| [`episodes/_TEMPLATE.md`](episodes/_TEMPLATE.md) | Blank template for the next episodes |
| [`episodes/ideas.md`](episodes/ideas.md) | Backlog of the next Short ideas |

## The pipeline (once per Short)

1. **Characters**: done once. Generate the sheets in `characters.md` and save the best images. Don't regenerate them after that.
2. **Script**: Claude writes it with `claude-prompts.md` → save it to `episodes/NNN-name/script.md`.
3. **Start frames**: one image per scene (Flux / Qwen Image in Wan2GP), using the character sheets.
4. **Clips**: Wan2GP → LTX-2.5 (or Wan 2.2) → image-to-video, 9:16, ~5 s, one prompt per scene. Queue them all and let them run overnight.
5. **Song**: generate the full song once as a single track. Don't let every clip make its own music.
6. **Edit**: CapCut → clips + song + sound effects → trim any slow first second.
7. **Upload**: title, **Made for kids = Yes**, schedule.

## Weekly schedule

| When | Do |
|---|---|
| Monday | Claude writes 10 Shorts (`claude-prompts.md` → prompt 1). ~15 min |
| Monday night | Queue every scene in Wan2GP and let the PC work overnight |
| Tuesday | Redo the weak scenes, then stitch and title the Shorts in CapCut |
| Wednesday | Schedule the whole week in YouTube Studio (1–3 Shorts a day, same times) |
| Friday | Check which Shorts did best and ask Claude for the next 10 in that direction (prompt 4) |
| Every other week | Stitch the 20 best Shorts into one 30–60 min compilation |

## Status

- [x] Channel concept, cast and style lock
- [x] Character-sheet prompts
- [x] Claude prompt pack, adapted to this channel
- [x] Episode 1: script, song, shot list, scene prompts
- [ ] Install Wan2GP on your PC (`SETUP.md`). It needs your own GPU, so it can't be done from here
- [ ] Generate and lock the character sheets
- [ ] Make Episode 1 and upload it
