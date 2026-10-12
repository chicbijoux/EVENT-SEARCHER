# Claude prompt pack

These are the guide's prompts, adapted to Leo & Bibo. **Before every prompt, paste
[`channel-bible.md`](channel-bible.md) and [`characters.md`](characters.md) into the chat**
(or put them in a Claude Project once, so every chat already knows them).

---

## 1. Monday: write a week of Shorts

```
You are the head writer of "Leo & Bibo", a kids' 3D cartoon channel (nursery rhymes & learning songs). The channel bible and the locked character descriptions are above. Follow them exactly.

Write 10 new YouTube Shorts. Each one is about 30 seconds: Leo, Bibo and Tofu, bright colors, ONE simple lesson (counting, colors, shapes, opposites, animal sounds, sharing, washing, bedtime...), and a catchy repeated sing-along line kids can sing. Every Short follows the ritual: 3-second hook → "Bip, bip, BIG!" → three stops → the ride → "Bip, bip, small!" ending that loops back to the hook. Don't repeat a lesson or a sing-along line from these past episodes: [LIST PAST TITLES].

For every Short give me:
1. Title (searchable: lesson + "Leo & Bibo" + "Nursery Rhymes for Kids") and a thumbnail idea
2. The 3-second hook scene: it must open on motion and a face
3. The scene-by-scene shot list (5-second scenes) with the lyric line for each scene
4. For each scene, a START-FRAME image prompt that uses the full character blocks word for word and ends with the style lock
5. For each scene, one LTX-2.5 image-to-video prompt: a single present-tense paragraph with the shot, setting, characters (short tags word for word), action, camera move, style, then "Audio:" with sound effects only and ending "no music, no speech", then "Final frame:"
6. The full song lyrics with timings, and a music-model prompt for the song
7. A YouTube description with 5 hashtags

Make each Short a real little story with its own new song. Never use famous characters, songs or brands.
```

**Tip:** ask for 3 at a time if the answer gets cut off ("Shorts 1–3 now, then I'll say next").

---

## 2. Copy what already wins

Search YouTube for *nursery rhymes* or *kids cartoon* → open a big channel → **Shorts** →
**Popular** → screenshot the page with view counts → attach it here:

```
Here is a screenshot of the most popular Shorts on a big kids' channel. Find the patterns: topics, hooks, colors, length, what the characters do, how the songs repeat.
Then write 5 ORIGINAL Shorts in the same spirit using MY characters (Leo, Bibo, Tofu) and the Leo & Bibo ritual, with new stories and new songs. Do not copy their characters, titles, lyrics or melodies.
Give me the same 7 parts per Short as in my weekly prompt, including the start-frame and LTX-2.5 prompt for each scene.
```

> **Take the pattern, never the content.** Close copies get channels demonetized or removed.

---

## 3. Fix a weak scene

```
This scene came out wrong in LTX-2.5 image-to-video. Here's the prompt I used:
[PASTE PROMPT]
What went wrong: [e.g. "Bibo grew a face", "the frogs don't move", "Leo has 6 fingers", "the clip is frozen"].
Rewrite the prompt to fix it. Keep the character tags word for word, put the main motion first, keep it under 180 words, and keep the Audio and Final frame lines.
```

---

## 4. Friday: review and steer

```
Here are this week's Leo & Bibo Shorts with their views, average % viewed and likes:
[PASTE TABLE: title | views | avg % viewed | likes]
What do the winners have in common (lesson, hook, animals, song, length)? What should we drop?
Then write the next 10 Shorts leaning into what works, in the same format as my weekly prompt.
```

---

## 5. Every other week: compilation

```
Here are my 20 best Leo & Bibo Shorts with view counts: [LIST].
Put them in an order for a 30–60 minute compilation that keeps toddlers watching: open with the strongest, mix lessons, and put calmer ones near the end. Then give me a title, a description with chapters (timestamps from these lengths: [LENGTHS]) and a thumbnail idea.
```
