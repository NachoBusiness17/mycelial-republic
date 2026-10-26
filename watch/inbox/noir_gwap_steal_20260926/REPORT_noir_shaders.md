# REPORT: illustrated-noir shaders + style (verbatim agent bank)

Provenance: background Explore agent "Research noir shader stacks", 2026-09-26, 31 tool uses / ~11 min, banked at the 17-minute clause. Verbatim capture; the agent's own punctuation preserved. Headline catch: Nighthawks' public-domain status is CONTESTED (AIC's own API says not PD, Wikipedia asserts PD); the Hopper style is free, literal reproduction is not; "Memo's Dreamscapes" footage must never be reused regardless.

---

# SHADERS + STYLE — Illustrated-Noir Render Pipeline Research (banked ~17 min)

## 1. Games that prove the illustrated-noir look
- **Disco Elysium** — Wikipedia: art "drawn mostly in a painterly style, was led by Aleksander Rostov," described as an oil painter; Unity engine, isometric. The look is **authored painted assets + painterly 3D rendering**, not a post filter. https://en.wikipedia.org/wiki/Disco_Elysium
- **Grim Fandango** — verified: "first adventure game by LucasArts to use 3D computer graphics overlaid on pre-rendered static backgrounds," GrimE engine/Lua, "combines elements of the Aztec afterlife with film noir style," characters from Day-of-the-Dead calacas. https://en.wikipedia.org/wiki/Grim_Fandango
- **The Wolf Among Us** — verified: 3D game on Telltale Tool "based on Bill Willingham's Fables comic book series"; Wikipedia does *not* use the term cel-shaded — the cel-noir look is comic-derived 3D with inked outlines (outline detail unfetched). https://en.wikipedia.org/wiki/The_Wolf_Among_Us
- **Backbone** — verified: "noir role-playing indie video game," anthropomorphic Vancouver, **Unreal Engine 4** (pixel look is authored assets + low-res rasterization, technique detail unfetched). https://en.wikipedia.org/wiki/Backbone_(video_game)
- **Sable** — verified: "art style was inspired by the sci-fi works of Jean Giraud (Mœbius)," Unity, "each of the game's environments are hand-crafted," categorized cel-shaded. https://en.wikipedia.org/wiki/Sable_(video_game)
- **Twelve Minutes** — verified: top-down single-apartment loop; cover "created to reflect the influences of Alfred Hitchcock, Stanley Kubrick, and David Fincher." Hopper is press/community framing, not in the article. https://en.wikipedia.org/wiki/Twelve_Minutes
- **Norco / Citizen Sleeper** — pixel-noir Louisiana / hand-drawn Guillaume Singelin art (from general knowledge; pages not fetched): https://en.wikipedia.org/wiki/Norco_(video_game) , https://en.wikipedia.org/wiki/Citizen_Sleeper

## 2. Creative-shader canon (what to steal)
- **Return of the Obra Dinn** — verified: "'1-bit' monochromatic graphical style inspired by early Macintosh," custom Unity rendering routines, dithering modified into motion-blur equivalents; CRT filter considered and rejected. Steal: dithering as the *only* shading info carrier + history-aware trails. https://en.wikipedia.org/wiki/Return_of_the_Obra_Dinn
- **Downwell** — 3-color palette quantization where palette shifts = combo/game state. Steal: the palette IS the HUD. https://en.wikipedia.org/wiki/Downwell
- **Sable** — steal: flat 2-tone light bands + outline from shader on 3D (Moebius banding). https://en.wikipedia.org/wiki/Sable_(video_game)
- **Hi-Fi Rush** — steal: lock global shader params (outline width pulse, rim flash) to the music clock. https://en.wikipedia.org/wiki/Hi-Fi_Rush
- **BPM: Bullets Per Minute** — steal: world pulse/beat = combat timing channel. https://en.wikipedia.org/wiki/BPM:_Bullets_Per_Minute
- **Superhot** — time-moves-when-you-move is one global scalar driving all rendering. Steal: one master uniform as the identity. https://superhotgame.com
- **Viewfinder** — photographs rewrite geometry; perception-as-mechanic. https://en.wikipedia.org/wiki/Viewfinder_(video_game)
- **Minit + CRT filters** — 64-second timer as global constraint; CRT scanline/phosphor shaders as retro identity: https://github.com/libretro/slang-shaders (verified repo exists, 469★; folder contents not listed)

## 3. Adoptable shader assets (all verified fetched — GitHub API / godotshaders.com)
- **Halftone/print:** daniel-ilett/shaders-halftone (Unity URP Shader Graph, MIT) https://github.com/daniel-ilett/shaders-halftone ; G4ND44/UnityHalftone (compute-shader postprocess, MIT) https://github.com/G4ND44/UnityHalftone ; patrickmatte/color-halftone-filter (canvas/WebGL, no license) https://github.com/patrickmatte/color-halftone-filter
- **Risograph:** Robpayot/risograph-grain-shader (80★, WebGL) https://github.com/Robpayot/risograph-grain-shader + template repo https://github.com/Robpayot/risograph-grain-shader-template ; hugomgris/RisoShader (Godot) https://github.com/hugomgris/RisoShader
- **Kuwahara painterly:** TxN/UnityURP_Kuwahara ("oil painting" URP render feature, MIT) https://github.com/TxN/UnityURP_Kuwahara ; alicepm800/Kuwahara-Filter-Plugin (UE HLSL global shader) https://github.com/alicepm800/Kuwahara-Filter-Plugin ; strangewarp/LoveAnisotropicKuwahara (anisotropic variant) https://github.com/strangewarp/LoveAnisotropicKuwahara
- **Toon stacks Godot:** https://github.com/EXPWorlds/Godot-Cel-Shader (245★) ; https://github.com/CaptainProton42/FlexibleToonShaderGD (201★) ; https://github.com/nekotogd/Godot_BoTW_Toon_Shader (166★) ; https://github.com/EMBYRDEV/godot-toon-outline (113★)
- **Toon UE5:** https://github.com/chrisloop/Unreal5_ToonShader (272★) ; https://github.com/lexULL/UE5_ToonShader (killer7-style cel + Kuwahara) ; https://github.com/Eragon-Brisingr/ToonShader (87★) ; https://github.com/shjh3117/UE_CelLit
- **Palette quantization / dither (GodotShaders, fetched):** PixelDither quantizer https://godotshaders.com/shader/pixeldither-color-quantizer-with-palette-support/ ; Snap Colors to Palette https://godotshaders.com/shader/snap-screen-colors-to-palette-posterize/ ; Arbitrary Color Reduction + Ordered Dither https://godotshaders.com/shader/arbitrary-color-reduction-ordered-dithering/ ; 1-bit multi-dithering (Obra-Dinn-style, Godot) https://godotshaders.com/shader/1-bit-spatial-multi-dithering-shader-with-1-bit-color-palette/
- **Noir / hard-shadow:** Noir XR/VR shader https://godotshaders.com/shader/noir-xr-vr-shader/ ; Moebius hatching outlines https://godotshaders.com/shader/mobius-outline-hatching/ + https://godotshaders.com/shader/moebius-shader/
- **CMYK offset-print:** no dedicated CMYK repo surfaced in halftone search (56 matches, none CMYK-specific) — build from the halftone repos with per-channel screen-angle rotation (analysis, not a citation).

## 4. Style transfer in-engine (2026 practicality)
- Unity's official `Unity-Technologies/unity-style-transfer` repo **404s** (dead). Verified live examples are proof-of-concept tier: ParkHaeChan/RealtimeStyleTransferwithUnityBarracuda (AdaIN ONNX in Unity Barracuda) https://github.com/ParkHaeChan/RealtimeStyleTransferwithUnityBarracuda ; huailiang/nnStyle (22★) https://github.com/huailiang/nnStyle
- **Memo Akten, Learning to See (2017)** — verified: custom pix2pix-style networks reinterpreting a live camera feed "in real time," exhibited Barbican/Grand Palais. The art-real-time-GAN lineage exists. https://memo.tv/works/learning-to-see/
- **Genie 3 (DeepMind, Aug 5 2025)** — verified: real-time 24fps 720p generated interactive worlds, consistent only "for a few minutes," limited research preview, explicitly struggles with multi-agent simulation. https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/
- **Verdict (analysis):** streamed diffusion passes per-frame remain impractical for a stylized *multiplayer* game in 2026 — latency, cross-client visual consistency, cost, and Genie-3-style consistency limits. Small deterministic CNN passes (AdaIN-class at low res + upscale) are the only viable in-frame option; practical uses today are offline asset paint-over, marketing art, async replays. A hand-tuned halftone/Kuwahara/palette stack is cheaper, deterministic, and hackable — build the noir look there.

## 5. Nighthawks public-domain check — the premise is WRONG (contested, not clean PD)
- **AIC holds it** (bought May 13, 1942, acc. 1942.51): https://en.wikipedia.org/wiki/Nighthawks_(painting)
- **AIC's own API says NOT public domain:** fetched JSON for id 111628 returns `"is_public_domain":false`, credit "Friends of American Art Collection" — https://api.artic.edu/api/v1/artworks/111628 and https://www.artic.edu/artworks/111628/nighthawks
- **Wikipedia asserts the opposite:** file https://en.wikipedia.org/wiki/File:Nighthawks_by_Edward_Hopper_1942.jpg carries `LicenseShortName: "Public domain"`, `License: "pd"` (fetched via Wikipedia extmetadata API). So: Wikipedia treats the 1942 painting as PD-US; the holding museum's rights metadata does not.
- **Meaning (analysis, not legal advice):** Hopper's *style* — hard light, diner geometry, nocturne palette — is not copyrightable; channel it freely. Literal reproduction of the composition/figures carries risk under the AIC/estate position and none under the Wikipedia PD position → tiered approach: original Hopper-inspired art is safe; shipping a recreated Nighthawks scene needs counsel sign-off. Photographs: under Bridgeman v. Corel, faithful photos of a genuinely-PD 2D work get no US copyright — but that shield only applies if the painting is PD, which is exactly what's contested; AIC's IIIF image (image_id 831a05de-d3f6-f4fa-a460-23008dd58dda) is served for research while the record stays non-PD.
- **"Memo's Dreamscapes":** **could not verify this artist exists** — search hit 429/1302 rate-limit storms on every attempt; zero usable results (sources attempted: en.wikipedia.org/wiki/Nighthawks_(Hopper), learn.oreateai.com/learn/how-imaginae-studios-and-fremantle-are-redefining-ainative-storytelling-for-television). Conditional logic: anyone may animate a PD painting, but *their* animated video is a new copyrighted work regardless of watermark — never reuse their footage; make your own animated Nighthawk.

## DEBT (listed, not done)
- Shadertoy direct shader links: site is JS-rendered, unfetchable this session — GitHub/GodotShaders equivalents substituted.
- Unfetched canon details: Downwell palette mechanics, Hi-Fi Rush beat-synced rendering, BPM, Superhot, Viewfinder, Backbone pixelation technique, Norco backgrounds, Citizen Sleeper artist.
- Disco Elysium environment pipeline (3D + paint-over) and Wolf Among Us cel-shading wording uncited.
- Games explicitly channeling Hopper (e.g., the Cobbett "Nighthawks" RPG) unverified.
- Bridgeman v. Corel cited from case-law common knowledge, page not fetched.
- Memo's Dreamscapes identity: unverified due to search rate-limiting — assign a follow-up when search recovers.
