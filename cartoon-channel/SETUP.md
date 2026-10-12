# Setup checklist

You do this once on your own computer. The video models run locally on your graphics card, so
each video costs nothing after setup.

## 1. Check your computer

- [ ] **Graphics card:** on Windows press **Ctrl + Shift + Esc** → **Performance** tab → **GPU**. Note the card name and the **Dedicated GPU memory**.
- [ ] **Disk:** about **100 GB free** for the app and the models.

| Your GPU memory | Use this model | Notes |
|---|---|---|
| **12 GB or more** (NVIDIA RTX) | **LTX-2.5** | Best quality. Makes video and sound together |
| **6–8 GB** | **Wan 2.2 (5B)** | Lightest good model. No sound, so add all audio in CapCut |
| **No GPU / too small** | **Kling** (klingai.com) | Use the free daily credits to test the idea first. The same prompts work |

## 2. Install the free video studio (Wan2GP)

**Easiest way: Pinokio (no typing)**

- [ ] Download and install Pinokio from **pinokio.computer**
- [ ] Open Pinokio → **Discover** → search `wan2gp`. Pick the community script by **Morpheus**, or `wan2gp-amd` for AMD cards
- [ ] Click **Install** and wait. The first install downloads several GB
- [ ] Click **Start**. The studio opens in your browser

**Alternative: the one-click script (Windows)**

```bash
git clone https://github.com/deepbeepmeep/Wan2GP.git
cd Wan2GP
```

- [ ] Double-click `scripts\install.bat` and choose **Auto Install**
- [ ] Double-click `scripts\run.bat` and open the address it prints in your browser

> On Linux, follow the install section of the Wan2GP README at github.com/deepbeepmeep/Wan2GP.

## 3. Pick your model and test it

- [ ] In the studio's **top-left model menu**, pick **LTX-2.5** (or **Wan 2.2 5B**). It downloads the first time you use it
- [ ] Choose **image-to-video** mode
- [ ] Set **vertical 9:16** and about **5 seconds**. At 24 fps that's ≈ 121 frames, and ≈ 73 frames for the 3 s hook
- [ ] **Test run:** generate Scene 0 from Episode 1 (`episodes/001-bip-bip-counting-bus/scene-prompts.md`)
- [ ] Find the image models (**Flux** / **Qwen Image**) in the same menu. You'll use them for the character sheets and start frames

## 4. Lock your characters

- [ ] Generate every sheet in [`characters.md`](characters.md). Make 4–8 tries each and keep the best
- [ ] Save them in a `characters/` folder on your PC (`leo.png`, `bibo-toy.png`, `bibo-big.png`, `tofu.png`, `group.png`)
- [ ] **Never regenerate them once you start posting.** Kids come back for characters who always look the same

## 5. Editing and channel

- [ ] Install **CapCut** (capcut.com, free)
- [ ] Create the YouTube channel **Leo & Bibo**. Use the avatar and banner prompts in `characters.md`
- [ ] In **YouTube Studio → Settings → Channel → Advanced settings**, set the audience to **"Yes, set this channel as made for kids"**. This is required by law (COPPA) for kids' content
- [ ] Bookmark the rules: Shorts monetization (support.google.com/youtube/answer/12504220), Partner Program (…/72851), Made for kids (…/9528076)

## 6. Folder layout on your PC

```
LeoAndBibo/
  characters/          locked sheets (never change)
  episodes/
    001-bip-bip-counting-bus/
      frames/          start-frame images, one per scene
      clips/           generated video clips
      audio/           song + sound effects
      final/           exported Short + thumbnail frame
```

## Troubleshooting

- **The clip barely moves or freezes.** LTX image-to-video sometimes stalls on cartoon images. Put the motion first in the prompt and make it bigger ("races", "jumps", "spins"). If your build has an *image strength* setting, lower it a little. Otherwise try Wan 2.2 for that one scene.
- **The character looks different from the sheet.** Make a better start frame. The start image controls the look much more than the text does.
- **Random music or voices in the clip.** Every scene prompt ends with "no music, no speech". Keep that line, and mute the clip audio in CapCut if it still slips in.
- **Out of memory.** Use a lower resolution (480p) or switch to Wan 2.2 5B.
