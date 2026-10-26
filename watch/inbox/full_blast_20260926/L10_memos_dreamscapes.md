# L10: Memo's Dreamscapes identity + local animated-painting pipeline (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore L10) · **Class:** RECEIPT / steal
**Closes debt:** #7 from the noir shader pack (Memo's Dreamscapes identity unverified).

## Identity result

"Memo's Dreamscapes" is a real but obscure INDEPENDENT YouTube channel (youtube.com/@memosdreamscapes, fetched) and is almost certainly NOT Memo Akten: Akten's memo.tv branding never uses "Dreamscapes", his handles are @memoakten/@memo_akten, and his style (abstract neural re-interpretation, Learning to See 2017) differs from photoreal painting animation. Exact-phrase search returned zero other indexed matches. A definitive X/Instagram link remains unresolvable with the storm-limited search (debt stays partially open, low stakes).

## The genre pipeline (all repos verified)

Commercial tier (what most living-painting X posts use): Runway Gen-4 / Kling / Veo image-to-video with first-frame + last-frame conditioning (end-frame = same painting makes true loops trivial).
Open-source tier on a 24GB card, verified:
- **LTX-Video** (Lightricks, DiT 13B/2B + FP8, distilled near-real-time, 1216x704@30fps, up to ~60s via forward/backward video extension, commercial OK under OpenRail-M): BEST fit for long ambient loops.
- **DynamiCrafter** (Doubiiu): explicit i2v with dedicated LOOPING and frame-interpolation variants; 576x1024, 16 frames/clip, ~18.3GB VRAM.
- **SVD-XT**: 25 frames (~4s), too short for 30s loops.
- **Practical-RIFE** (MIT, models 4.24+ recommended by its own README for diffusion output): 2x/4x interpolation to 60fps, minutes per 900 frames.

## Concrete plan for our OWN animated Nighthawks (fleet-generated, no third-party footage)

1. High-res Nighthawks scan (Wikimedia/AIC) to ~1216x704 crop.
2. LTX-Video 13B FP8 i2v, prompt: steady rain, flickering neon, drifting cigarette smoke, subtle camera parallax; 121-257 frame clips, 1-2 min each on RTX 3090/4090 class.
3. Loop via LTX forward+backward extension chaining or last-to-first crossfade (DynamiCrafter loop variant as fallback).
4. RIFE x2/x4 to 60fps.
5. Budget: ~10-15 chained clips + interpolation + encode = 1-2.5 hours total for 30s @ 1080p60.

## Rights recap (sharpened)

Hopper died 1967: likely protected through 2037 in life+70 jurisdictions; AIC's own API marks is_public_domain false (id 111628), Wikipedia asserts PD-US. Contested. Independent of that: the dropped video is separately copyrighted by its maker; generating our OWN animation infringes neither their recording nor their watermark. Ship our own.

## Agent debts

Channel subscriber count/description not loaded (YouTube JS wall); X/IG presence of "Memo's Dreamscapes" unresolved; Kling/Veo loop specifics from general knowledge, pages not fetched.
