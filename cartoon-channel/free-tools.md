# Free online tools (no GPU needed)

Researched on **12 Oct 2026** for Leo & Bibo: a monetized "Made for kids" channel, made from Romania
(EU) on a PC without a graphics card.

> **How solid is this?** 4 researchers and 4 independent fact-checkers ran, but many vendor
> websites were blocked from the research environment, and the shared search budget ran out
> before the fact-checkers could search. So most free-credit numbers come from search snippets
> and 2026 reviews, not from the vendors' own pages. Model licenses and Hugging Face/Kaggle
> facts were checked against official GitHub sources. **Before you rely on a tool, open it from
> Romania and check three things: the credit counter, whether there's a watermark, and the
> commercial-use line in its plan page.** The checklist at the bottom takes about 10 minutes.

## The short answer

1. **No free tool gives all three:** good quality, no watermark, and a license to use the clips on a monetized channel.
2. **The free Chinese video sites are for testing only.** Free clips from **Kling, Hailuo, Vidu and PixVerse** carry a watermark, and their own plans or terms say free output is **non-commercial**. Dreamina doesn't say clearly either way. Use their free credits to test prompts, never for clips you upload.
3. **Google is the best free option from Romania.** **Flow** (Veo video, free daily credits) and **Gemini** (Nano Banana images) work here, and Google doesn't claim ownership of what you make. But see the warning about child characters below.
4. **Kaggle + WanGP is the only free route with no watermark and a clean license**, using open models (Wan 2.2). It's slower and lower quality than Kling or Veo, but it costs nothing.
5. **YouTube's own AI tools for Shorts are not available in Romania.** That covers the Veo and Omni clip generation in the Shorts camera and YouTube Create. Its official help page excludes the EEA.

## ⚠️ Warning: Leo is a child, and Google blocks child characters in the EU

In the EU, Google limits Veo image-to-video when the picture shows children. Developers report
**Pixar-style cartoon children being refused** (support code 17301594). This may block every
scene with Leo in Flow, Vids and Gemini video. Scenes with only Bibo and Tofu should pass.
**Test a Leo start frame in Flow before planning around Google.** If it's blocked, use Kaggle +
WanGP (open models have no such filter) or a paid Kling or Dreamina plan for Leo's scenes.

## Recommended free setup

| Job | Tool | Free amount (unverified unless noted) | Watermark | OK for monetized? |
|---|---|---|---|---|
| Character sheets and start frames | **Gemini app → Nano Banana 2** (also inside Google Flow) | Up to about 20 images/day (no Google figure since May 2026); image generation in Flow reportedly costs 0 credits | Small visible sparkle on Gemini-app images, so leave the bottom-right corner empty and crop it | Probably. Google claims no ownership; not stated explicitly |
| Start frames, no watermark | **Qwen-Image-Edit-2511** on Hugging Face (free Space) | **5 GPU-minutes/day** with a free account (confirmed in HF docs) | None | **Yes**, Apache-2.0 weights |
| Start frames, alternative | **Gemini API, Nano Banana 2 Lite** (in AI Studio) | Google's own cookbook says it "includes a free tier"; quota and EU eligibility unknown | None (invisible SynthID only) | Probably |
| Video clips | **Google Flow** (labs.google/flow) | 50 credits/day reported: ~5 Veo 3.1 Lite clips (720p, up to 8 s) or ~2 Veo 3.1 Fast clips a day. Romania is on Google's official list | Maybe a small "Veo" mark, so check | Probably. Not stated explicitly |
| Video clips (few) | **Google Vids** (vids.new) | About 6–10 clips/month with Gemini Omni (Flash or Flash Lite) | No visible mark | Probably |
| Video clips (unlimited, slower) | **Kaggle Notebooks + WanGP** (Wan 2.2 5B) | About 30 GPU-hours/week on T4 GPUs (the P100 was retired in Sep 2026, confirmed) | None | **Yes**: Wan 2.2 is Apache-2.0, LTX-2.x is free under $10M revenue |
| Sing-along song | **ACE-Step 1.5**: free Hugging Face Space, or inside WanGP | Unlimited if you run it yourself; the Space uses your ZeroGPU minutes | None | **Yes**, MIT license (check the model card) |
| Song, more polished | **Gemini app music** (Lyria 3.5) | Free songs of about 1–3 min; you must be 18+ | Inaudible SynthID | **Unclear**: Google lists "commercial use rights" for its music tools as a *paid* benefit. Moderate risk |
| Sound effects | **YouTube Audio Library** (filter "attribution not required"), **Pixabay**, **Mixkit**, **Freesound** (filter CC0) | Unlimited | None | Yes |
| Voices (if needed) | **Kokoro** (Apache-2.0, runs on a normal PC) or **Chatterbox** (MIT) | Unlimited | Chatterbox adds an inaudible mark | Yes |
| Editing | **CapCut** free, or **Clipchamp** (free 1080p, no watermark, comes with Windows 11), or **Kdenlive** (offline) | Unlimited | None | Yes, with your own audio only |

## Video tools compared

| Tool | Quality for 3D cartoon | Free tier | Free output usable on the channel? | Notes |
|---|---|---|---|---|
| **Kling 3.0 / Omni** | ★★★★★ best character consistency (Elements: one per character) | Unclear in 2026: 66 credits/day historically; a 5 s 720p silent clip costs ~30 | ❌ watermark + "not for commercial use" | **Best paid pick**: Standard ~$6.99 first month, ~22 clips. Kling 4.0 is due this month |
| **Dreamina / Seedance 2.x** (ByteDance) | ★★★★★ up to 12 tagged references | ~120 credits/day reported (US accounts); a clip costs 34–60 | ❌ watermark; commercial use unclear | EU added Apr 2026, but access depends on the account |
| **Hailuo H3** (MiniMax) | ★★★★ lively motion | One-time trial credits only | ❌ watermark; commercial rights only on paid plans | Paid ~$8.40–10.50/mo |
| **Vidu Q3 / Q4** | ★★★★ up to 15 references | ~40–80 credits/month | ❌ watermark + non-commercial | Paid ~$8/mo |
| **PixVerse V6** | ★★★ | ~30–60 credits/day, ~1 clip | ❌ ToS: free = non-commercial | |
| **Google Flow (Veo 3.1)** | ★★★★ | ~50 credits/day | ✅ probably (check watermark) | ⚠️ child-character limit in the EU |
| **Google Vids (Omni)** | ★★★★ | ~6–10 clips/month | ✅ probably, no visible mark | ⚠️ same limit |
| **Runway** | ★★★★ | 125 credits **once** (~5 clips) | Terms allow commercial use, but clips are watermarked | Test only |
| **Kaggle + WanGP (Wan 2.2)** | ★★★ | ~30 GPU-h/week | ✅ yes | Slow; no sound |
| **Hugging Face Wan 2.2 Spaces** | ★★★ | 5 GPU-min/day | ✅ yes | A few clips a day at most |
| **YouTube Shorts / Create AI clips** | ★★★★ | Free | — | ❌ **Not available in the EEA (Romania)** |
| Gemini app video | ★★★★ | ❌ paid only (the free promo ended Aug 2026) | — | |
| Sora | — | — | — | Shut down (app Apr 2026, API Sep 2026) |
| Grok Imagine | — | Free video dropped Mar 2026 | — | |
| Luma, Pika, LTX Studio | ★★★ | Small | ❌ watermark + non-commercial | |
| Tencent Hunyuan | — | — | ❌ license **excludes the EU** | Don't use, including the Hunyuan models inside WanGP |

## Music: what *not* to use for free

- **Suno free:** non-commercial, Suno owns the songs, and upgrading later does **not** license songs you already made. If you pay (Pro ~$10/mo), make the final song *after* subscribing.
- **ElevenLabs free** (music, SFX, voices): non-commercial and attribution required.
- **Mureka free:** Mureka owns the output.
- **Udio:** downloads have been disabled since Oct 2025.
- **MMAudio** (inside WanGP): non-commercial license (CC-BY-NC).
- **YuE2** (inside WanGP): its license wasn't checked. Prefer ACE-Step until you have checked it.

## Rule for every tool: rights depend on when you made the clip

Several tools (e.g. Hailuo, Suno) give commercial rights only to things **made while you're on a
paid plan**. Clips made on free credits stay non-commercial even after you upgrade. **Use free
credits to test; make the final clips after you pay.**

## Cheapest paid upgrades (if free isn't enough)

| Option | Price | What you get |
|---|---|---|
| **Google AI Plus** | 26.99 lei/month in Romania (13.99 lei for the first 2 months) | +200 Flow credits/month and Omni with reference images ("ingredients"), much better Leo/Bibo/Tofu consistency. Same child-character caveat |
| **Kling Standard** | ~$6.99 first month, then ~$8.80/month | ~22 clips of 5 s at 720p (silent), Elements for consistency, commercial use, no watermark |
| **Suno Pro** | ~$10/month | Commercially licensed songs (made while subscribed) |

## 10-minute test from Romania (do this first)

1. **Google Flow:** sign in at labs.google/flow and note the credit counter. Upload a Leo start frame and try one image-to-video clip.
   - Did it refuse Leo?
   - Does the clip have a visible "Veo" mark?
   - Then try a Bibo-only scene.
2. **Gemini app:** generate Leo's character sheet (prompt in `characters.md`). Note the sparkle mark and how many images you get before it stops.
3. **Hugging Face:** open the Qwen-Image-Edit-2511 Space, give it your Leo, Bibo and Tofu sheets, and ask for the Scene 2 start frame.
4. **ACE-Step Space:** paste the Bip-Bip Bus lyrics and the music prompt from `episodes/001-bip-bip-counting-bus/script.md`.
5. **Kling** (optional): check whether free credits show up, and read the plan page's commercial-use line.

## Sources (main ones)

- Google Flow countries: support.google.com/flow/answer/16353544 · credits: support.google.com/flow/answer/16526234
- YouTube Shorts AI features (EEA exclusions): support.google.com/youtube/answer/15260303
- Veo child-safety refusals in the EU: discuss.ai.google.dev/t/veo-3-1-image-to-video-blocks-wholesome-commercial-storyboard-child-safety-false-positive/131917
- Google Vids free Omni: blog.google/products-and-platforms/products/workspace/gemini-omni-in-google-vids/
- Nano Banana 2: blog.google/innovation-and-ai/technology/ai/nano-banana-2/ · free-tier note: github.com/google-gemini/cookbook (Get_Started_Nano_Banana)
- Kling plans: kling.ai/blog/kling-video-3-0-credit-cost-guide · Hailuo terms: hailuoai.video/doc/terms-of-service.html · PixVerse ToS: pixverse.ai/en/terms-of-service · Vidu: vidu.com/pricing
- Runway usage rights: help.runwayml.com/hc/en-us/articles/18927776141715-Usage-rights
- Hugging Face ZeroGPU quota: github.com/huggingface/hub-docs (spaces-zerogpu.md) · Kaggle P100 retirement: github.com/Kaggle/kaggle-cli/pull/1192
- ACE-Step 1.5: github.com/ace-step/ACE-Step-1.5 · Suno terms: suno.com/blog/suno-updates-tos · MMAudio license: github.com/hkchengrex/MMAudio
- Model licenses: github.com/Wan-Video/Wan2.2 (Apache-2.0) · github.com/Lightricks/LTX-2 (LICENSE-2_x) · github.com/QwenLM/Qwen-Image
