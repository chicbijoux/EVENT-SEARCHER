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

> Checked against the Wan2GP repo on 12 Oct 2026 (WanGP **v18.00**).

**Before you start (NVIDIA cards):** update your graphics driver to the latest version (GeForce
Experience / NVIDIA App, or nvidia.com/drivers). Some of Wan2GP's speed-up kernels need driver
**R580 or newer**.

**Easiest way: Pinokio (no typing)**

- [ ] Download and install Pinokio from **pinokio.computer**
- [ ] Open Pinokio → **Discover** → search `wan2gp`. Pick the community script by **Morpheus**, or `wan2gp-amd` for AMD cards
- [ ] Click **Install** and wait. The first install downloads several GB
- [ ] Click **Start**. The studio opens in your browser

**Alternative: the one-click script**

- [ ] Install Git from **git-scm.com** (all default options are fine)
- [ ] Open a terminal (Windows: press Start, type `cmd`, press Enter) and run:
  ```bash
  git clone https://github.com/deepbeepmeep/Wan2GP.git
  cd Wan2GP
  ```
- [ ] **Windows:** double-click `scripts\install.bat`. If it says Python 3.11+ is missing, answer **y** and it installs it for you. In the menu, type **1** (*Automatic Install (1-Click)*). It picks the right setup for your card
- [ ] **Linux:** run `scripts/install.sh` in the terminal and choose Auto Install
- [ ] Start the studio: double-click `scripts\run.bat` (Linux: `scripts/run.sh`) and open **http://localhost:7860** in your browser
- [ ] *Optional:* create a file `scripts\args.txt` containing `--open-browser`, so the browser opens by itself on every start
- [ ] *Later:* `scripts\update.bat` (Linux: `scripts/update.sh`) gets the newest version. Wan2GP updates often

## 3. Pick your model and test it

- [ ] In the studio's **top-left model menu**, pick a model. It downloads the first time you use it:
  - **12 GB+:** **LTX 2.5 Distilled**. It makes video and sound together, needs only 8 steps, and is the recommended starting point
  - **6–8 GB:** **Wan 2.2** (the 5B model, or **Wan 2.2 I2V**). It has no sound
- [ ] Use **image-to-video**: upload the scene's start frame as the **Start Image**
- [ ] Set **vertical 9:16** and about **5 seconds**. At 24 fps that's ≈ 121 frames, and ≈ 73 frames for the 3 s hook
- [ ] Paste the negative prompt from `channel-bible.md`
- [ ] **Test run:** generate Scene 0 from Episode 1 (`episodes/001-bip-bip-counting-bus/scene-prompts.md`)
- [ ] Create a **Workspace** called *Leo & Bibo*, so every clip of the channel lands in its own folder (see *Config / Outputs*)

**The other tools you'll use, all in the same menu:**

| Job | Model in Wan2GP | Tip |
|---|---|---|
| Character sheets and start frames | **Qwen Image 2.1** (or Flux 2 / Krea 2) | Qwen Image 2.1 can also **edit**: give it your character sheets as reference images. It writes text well, so the "1 2 3" bus-stop numbers come out right |
| Keeping characters identical | **LTX 2.5 MSR** | Takes 1–4 reference images (Leo, Bibo, Tofu sheets) plus the prompt. Try it if image-to-video drifts away from the characters |
| The song with vocals | **YuE2** (lyrics + style → full song) or **Ace Step** | Paste the lyrics and the music prompt from the episode's `script.md` |
| Voices / narration | **Qwen3 TTS**, **Chatterbox**, **Index TTS2** | |
| Continuity between scenes | Video Gallery → *add current frame to Image Gallery* | Use a clip's last frame as the next scene's start image |
| Overnight batches | **Generation queue** | Add all 7 scenes, then leave the PC running |

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
