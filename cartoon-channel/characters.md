# Characters

Three characters, locked forever. Paste the descriptions **word for word** every time. Changing a
single word ("red" to "crimson") is enough to make the model drift.

- **Full block:** use it in image prompts (character sheets and start frames).
- **Short tag:** use it in video prompts. The start frame already carries the look, so the video prompt only needs enough detail to keep the model on track.

---

## Leo: the boy

4 years old. Curious, cheerful and a little impatient. Counts everything on his fingers,
steers an imaginary wheel with both hands, laughs with his whole body.
**Catchphrase:** *"Bip-bip, here we go!"*

**Full block**
```
Leo, a 4-year-old boy with a round face, big warm brown eyes, rosy cheeks and messy curly chestnut-brown hair with one curl sticking up at the front, wearing a sky-blue t-shirt, orange shorts and white sneakers with red laces
```

**Short tag**
```
Leo, a 4-year-old boy with messy curly chestnut-brown hair, a sky-blue t-shirt and orange shorts
```

---

## Bibo: the magic toy bus

Leo's favorite toy. **No face:** he shows feelings by blinking his headlights (happy = two quick
blinks), bouncing on his wheels (excited) and honking (*"bip-bip!"*).

- **Toy size:** fits in Leo's two hands.
- **Big size:** a real bus, after Leo honks three times, *"Bip, bip, BIG!"*. Inside are soft sky-blue seats and a big yellow steering wheel. *"Bip, bip, small!"* shrinks him back.

**Full block, toy**
```
Bibo, a chubby, rounded cherry-red toy bus with a white roof, four round windows on each side, two big round yellow headlights, a small silver horn on the front bumper, chunky black wheels with yellow hubcaps and a gold number 1 on each side
```

**Full block, big**
```
Bibo, a full-size chubby, rounded cherry-red bus with a white roof, four big round windows on each side, two big round yellow headlights, a silver horn on the front bumper, chunky black wheels with yellow hubcaps, a gold number 1 on each side, soft sky-blue seats and a big yellow steering wheel inside
```

**Short tags**
```
Bibo, a chubby cherry-red toy bus with a white roof, round windows and big yellow headlights
```
```
Bibo, the full-size chubby cherry-red bus with a white roof, round windows and big yellow headlights
```

---

## Tofu: the puppy

Leo's puppy (she). The comic relief: always tries to be first, sniffs every new passenger,
rides with her head out of the front window and her ears flapping. One happy "Woof!" at every stop.

**Full block**
```
Tofu, a small fluffy cream-white puppy with one floppy caramel-brown ear, a black button nose and a red collar with a tiny gold bell
```

**Short tag**
```
Tofu, a small fluffy cream-white puppy with one caramel-brown ear and a red collar
```

---

## Character-sheet prompts (Flux / Qwen Image in Wan2GP)

Generate 4–8 of each, keep the best and save it in your `characters/` folder. Set the image to
**square or 16:9** (sheets need width) and use the negative prompt from `channel-bible.md`.

### 1. Leo (`leo.png`)
```
Character turnaround sheet for a kids' 3D cartoon channel. Leo, a 4-year-old boy with a round face, big warm brown eyes, rosy cheeks and messy curly chestnut-brown hair with one curl sticking up at the front, wearing a sky-blue t-shirt, orange shorts and white sneakers with red laces. Full-body front view, side view and back view standing in a row, plus three head close-ups: a happy grin, a surprised open "O" mouth, and giggling with eyes closed. Plain white background, even soft studio lighting, identical proportions in every view. Bright 3D animated kids' cartoon, soft rounded shapes, smooth matte clay-like textures, big expressive eyes, saturated candy colors, cheerful and safe mood.
```

### 2. Bibo, toy (`bibo-toy.png`)
```
Product-style turnaround sheet of a toy for a kids' 3D cartoon channel. Bibo, a chubby, rounded cherry-red toy bus with a white roof, four round windows on each side, two big round yellow headlights, a small silver horn on the front bumper, chunky black wheels with yellow hubcaps and a gold number 1 on each side. Front view, side view, three-quarter view and back view in a row. The bus has no face, no eyes and no mouth; the headlights are simple glowing yellow circles. Plain white background, even soft studio lighting. Bright 3D animated kids' cartoon, soft rounded shapes, smooth matte clay-like textures, saturated candy colors.
```

### 3. Bibo, big (`bibo-big.png`)
```
Three-quarter view of Bibo, a full-size chubby, rounded cherry-red bus with a white roof, four big round windows on each side, two big round yellow headlights, a silver horn on the front bumper, chunky black wheels with yellow hubcaps and a gold number 1 on the side, parked on green grass with its front door open, showing soft sky-blue seats and a big yellow steering wheel inside. Leo, a 4-year-old boy with messy curly chestnut-brown hair, a sky-blue t-shirt and orange shorts, stands next to the front wheel for scale, looking up and smiling. The bus has no face, no eyes and no mouth. Plain soft white background. Bright 3D animated kids' cartoon, soft rounded shapes, smooth matte clay-like textures, warm soft sunlight, saturated candy colors.
```

### 4. Tofu (`tofu.png`)
```
Character turnaround sheet for a kids' 3D cartoon channel. Tofu, a small fluffy cream-white puppy with one floppy caramel-brown ear, a black button nose and a red collar with a tiny gold bell. Front view sitting, side view standing, running with ears flying, plus three head close-ups: happy with tongue out, head tilted curiously, and a happy bark. Plain white background, even soft studio lighting, identical proportions in every view. Bright 3D animated kids' cartoon, soft rounded shapes, fluffy soft fur, big expressive eyes, saturated candy colors, cheerful and safe mood.
```

### 5. Group hero shot (`group.png`)
Use it as a channel visual and as a fallback start frame.
```
Leo, a 4-year-old boy with a round face, big warm brown eyes, rosy cheeks and messy curly chestnut-brown hair with one curl sticking up at the front, wearing a sky-blue t-shirt, orange shorts and white sneakers with red laces, sits cross-legged on a sunny backyard lawn hugging Bibo, a chubby, rounded cherry-red toy bus with a white roof, four round windows on each side, two big round yellow headlights, a small silver horn on the front bumper, chunky black wheels with yellow hubcaps and a gold number 1 on each side. Beside him sits Tofu, a small fluffy cream-white puppy with one floppy caramel-brown ear, a black button nose and a red collar with a tiny gold bell, with her tongue out. All three face the viewer, Leo grinning. White picket fence and round green bushes softly blurred behind. Bright 3D animated kids' cartoon, soft rounded shapes, smooth matte clay-like textures, big expressive eyes, warm soft sunlight, gentle shadows, saturated candy colors, cheerful and safe mood.
```

---

## Channel art

### Avatar (square, readable at tiny size)
```
Close-up of a chubby, rounded cherry-red toy bus with a white roof and two big round glowing yellow headlights, facing the viewer, with a 4-year-old boy with messy curly chestnut-brown hair peeking over the roof and grinning. Simple sky-blue circular background. The bus has no face. Bright 3D animated kids' cartoon, soft rounded shapes, smooth matte clay-like textures, saturated candy colors.
```

### Banner (wide 16:9, keep the middle clear for the channel name)
```
Wide panoramic view of Lollipop Hills: a winding road through rolling green hills with round lollipop-shaped trees, a blue pond and puffy white clouds. On the right, a full-size chubby cherry-red bus with a white roof and big yellow headlights drives along the road, with a 4-year-old boy with curly chestnut-brown hair at the wheel and a fluffy cream-white puppy with one caramel-brown ear leaning out of the front window. Lots of clear sky in the center. Bright 3D animated kids' cartoon, soft rounded shapes, warm soft sunlight, saturated candy colors.
```
