# accuracy lens: stupid-model comics lane, 2026-10-07

Lens: falsifier-hunt. Every claim below was checked against bytes or executed this
sitting (2026-10-07, ~14:30-15:10Z). Instruments named inline. No em-dashes per law.
Probe artifacts live in this directory: probe_panel_spec.py, probe_panel_spec_results.json.

## Estate claims re-verified (instrument + moment each)

1. M1 grammar bench: watch/inbox/48h_synth/m1_bench.json (read this sitting) reads
   model gemma:2b, 30 prompts, unconstrained_valid 0/30, format_schema_valid 30/30,
   verdict "M1 CONFIRMED: schema arm wins". The ask's M1 cite is byte-true.
2. Free seats: tools/free_lane_fleet.py:115-137, PROVIDERS table read directly:
   nvidia-1/nvidia-2 = meta/llama-3.2-11b-vision-instruct on integrate.api.nvidia.com,
   ollama-local = qwen2.5:7b, plus 4 more free providers (openrouter x2, mistral,
   cohere). First measured register watch/inbox/GAUNTLET_FREE_LANDED_20261006.md:30-41:
   11 trials at $0.00, dice 2/2 PASS (llama-3.2-11b + qwen2.5:7b both suspended to the
   deterministic tool), beat grid held to 8 counts and broke at 12. "A stupid model is
   already on the payroll" is TRUE and measured.
3. Census spot-rerun (quantifier law): `git grep -li <term> -- mag tools corpus watch`
   on THIS tree at this moment reads xkcd 26 / stickfigure 0 / mermaid 84 / voxel 83 /
   comic 75 / electron 283, vs the ask's 23/3/65/69/67/241. Direction holds (prior art
   deep); the deltas are tree drift plus term shape: "comics" alone reads 16, "comic"
   reads 75 (the ask's 67 matches the "comic" substring family), and the 2 stickfigure
   hits in the whole repo are shadertoy shader files (memory/corpus/shadertoy21k/),
   outside the ask's scope. Absence claim scoped: stickfigure appears in ZERO files
   under mag+tools+corpus+watch by git grep -li at this moment.
4. Discord wiring point: mag/phone_relay.py read this sitting. REST base discord.com
   (:34-36, api.discord.com DNS dead 09-24), token from the hermes env DISCORD_BOT_TOKEN
   (:64-73), DM-only + DISCORD_ALLOWED_USERS fail-closed + 12 asks/hour cap (:54).
   Function census (:41-218): ask/test/_api are TEXT-message only; there is no
   attachment, embed, or file-upload path in the file today. The comics lane extends
   this file or sits beside it; it does not start from zero.
5. Light-maze frame: ROLL_SHAPE_TURING_CASTLE_20261007.md (read, 6993 bytes) carries
   "light maze" 4x and ZERO hits for comic/imaging/7318df04/346. The zknot session
   file memory/zknot/2026-10-06_sess_7318df04-6115-449d-b554-2f93d5ee2a6e.md (7883
   bytes, read) carries "10-07 09:33 this is our light maze." and NO msg-346 marker.
   The ask's exact phrasing "the light maze IMAGES walkers by their paths" appears in
   NO file I grepped (memory/watch/corpus, git grep -in "images walkers": zero rows).
   Verdict: the naming moment is byte-verified; the imaging-turing quote's wording is
   the ractor's paraphrase and is OWED a source, not asserted.

## THE PROBE (executed, not proposed)

Script probe_panel_spec.py (this dir), fired 2026-10-07 ~14:5xZ against local
ollama (daemon live, /api/tags read): 8 session-summary prompts x 3 free seats with
format:"json" (the M1 door) + 8 gemma:2b prompts unconstrained = 32 calls, $0, all
local. Schema scored mechanically: parses (JSON), spec_valid (title str, 3-4 panels,
each panel caption str non-empty + characters list[str] + bubbles list of
{who,text} non-empty, <=2 bubbles/panel).

- qwen2.5:3b-instruct format:json: 8/8 parses, 7/8 spec_valid, mean 6.8s. WINNER.
- gemma:2b format:json: as-run 7/8 parses 5/8 spec_valid, BUT 1 row was MY scorer's
  defect (unguarded bubbles iteration crashed on a null field and banked as error).
  Cell rerun with fixed scorer: parses True, spec_valid True (4 panels). Corrected:
  8/8 parses, 6/8 spec_valid, mean 5.8s. The instrument bug is reported, not buried;
  full raw text was not persisted (only 90-char heads), so the correction rests on
  the rerun cell, noted honestly.
- gemma:2b UNCONSTRAINED: 8/8 parses, 6/8 spec_valid, mean 11.9s (fences ```json on
  row 5, still extractable).
- deepseek-r1:1.5b format:json: 6/8 parses, 1/8 spec_valid. Wrong seat: it
  over-produces (5-panel comics, 2 bubbles) regardless of the door.

## Findings

F1 (the lane's falsifier PASSES on a free seat; CONVERGENT with the gauntlet dice
result). A 1.9GB local model already writes spec-valid xkcd-shape panel specs at
87.5% through the format door at comic-per-7-seconds, $0. Evidence: probe rows this
sitting (probe_panel_spec_results.json). Falsifier: 8 prompts/seat is small-n and
temperature-0.3-only; a 50-prompt run or the renderer's final schema (typed enums,
fixed character roster) could regress 87.5% materially. Move (60-90 min): freeze the
spec schema NOW from the probe's shape, wire the PIL renderer to it, then rerun the
probe at n=50 as the lane's admission gate, exactly the gauntlet register pattern.

F2 (ACCURACY CORRECTION to the ask's framing). "The comic spec is the same shape" as
the M1 0/30 to 30/30 flip is half wrong: on THIS schema gemma:2b parsed 8/8 and
spec'd 6/8 even UNCONSTRAINED. The M1 flip is task/prompt-specific (my probe's
instruction says "Output ONLY a JSON object", which alone rescues parse rate). The
door's measured value on this task is latency (11.9s to 5.8s mean) and variance
control, not a 0-to-1 rescue. Evidence: unconstrained arm rows this sitting vs
watch/inbox/48h_synth/m1_bench.json. Falsifier: drop the "Output ONLY JSON"
sentence and rerun; if unconstrained gemma:2b collapses toward 0/8, the M1 transfer
claim revives. Move (30 min): that exact rerun; until then cite this probe, not M1,
as the comic lane's format-door evidence.

F3 (the operator's model identified + priced by the estate's own instrument).
"New model from google that runs on nothing" = Gemma 4 26B-A4B: 26B total, ~4B
active per token (MoE), Apache-2.0, multimodal, per ai.google.dev/gemma/docs/core
and huggingface.co/google/gemma-4-26B-A4B (web, this sitting). The estate's own
endpoint-news instrument already banked it: watch/inbox/endpoint_news/
snapshot_openrouter.json (mtime 2026-10-07T13:01Z) lists google/gemma-4-26b-a4b-it
at prompt_price 0.00000009 USD/token ($0.09/M) AND google/gemma-4-26b-a4b-it:free
at free=true, plus gemma-4-31b-it:free. Two openrouter-free providers are already
wired (tools/free_lane_fleet.py:116-121), so the stupid seat joins with a config
row, not a new account. Falsifier: the :free variant is a point-in-time snapshot; it
may be rate-capped or withdrawn; also the local ollama tag gemma4:latest (9.6GB,
/api/tags this sitting) is UNVERIFIED as gemma-4-26b-a4b (naming ambiguity, OWED).
Move (15 min + one cycle): add gemma-4-26b-a4b-it:free as a gauntlet seat on an
existing openrouter provider row; let the 30-min fleet clock drain 5 trials and the
register scores it mechanically.

F4 (CARRIER CORRECTION, no sacred cows). "Deterministic SVG renderer, discord relay
posts it" fails at the last hop on two measured facts: (a) Discord does NOT render
SVG inline, PNG/JPEG/GIF/WEBP only (discord-api-docs issue #25935 "Could not process
image"; long-standing support feature request; web this sitting) [STRUCK:
issue #25935 is a phantom, see ERRATUM below, 2026-10-07]; (b) this venv has
no SVG rasterizer (checked: cairosvg False, svglib False, resvg not on PATH) while
PIL is present. Right shape: ONE panel spec, TWO deterministic renderers: PIL
ImageDraw to PNG for the discord face (zero new deps, stick figures are lines +
ellipses + text, resolution-locked), SVG emitter for the dashboard/estate_walk face
(browser renders SVG fine). Falsifier: a Discord changelog admitting SVG inline
rendering, or installing resvg/cairosvg, revives the single-SVG carrier. Move (90
min): PIL stick-figure renderer + phone_relay attachment extension (multipart post,
the file's first non-JSON body) posting to the DM lane.

F5 (external prior-art verdict: composition, not invention). The exact combo
(session -> cheap model -> panel spec -> deterministic renderer -> discord) surfaced
NO product in my searches; every piece has verified prior art: darwin/cmx.js
(GitHub API this sitting: 798 stars, JavaScript, "[prototype] A library/markup for
building xkcd-style comic strips", pushed 2013-04-22, license NOASSERTION, homepage
cmx.io) is the deterministic xkcd renderer, 13 years old and prototype-dead: steal
the panel/character/bubble vocabulary, not the code; SVGBob (ivanceras/svgbob,
Rust; pypi vye-svgbob) proves the text-to-SVG instrument class; pellmellism/xkcd
LoRA on Replicate and Flux xkcd LoRAs are the PAID raster route this lane rejects
(nondeterministic, per-image cost); discord summarizers (tldrbot, Discord native
in-channel summaries, daily-discord-summarizer) are text-only, and the one comic
discord bot found is a 2016 pre-LLM reddit toy. The estate's actual novelty is the
falsifier-scoring register (mechanical admission gates per seat), not the comic.
Falsifier: a targeted top.gg / Discord App Directory sweep (not run, named below)
could surface a live comic-summarizer product and demote this from open lane to
steal-target. Move (20 min, decision only): adopt cmx-style field names in the
frozen schema so the spec reads like 2013 prior art, not a novel format.

## Blind spots

- Probe is n=8/seat, one temperature, no typed-enum schema, and one scorer bug
  (found, fixed, one cell rerun); a 50-prompt power run is OWED.
- I fired ZERO live calls through openrouter/nvidia keys (spending live provider
  calls sat outside this ask); gemma-4 :free availability is snapshot-only.
- Discord app-store depth (top.gg directory pages) not exhaustively crawled.
- Local gemma4:latest identity unverified; it may or may not be the Gemma 4 MoE.
- The ask's census numbers cannot be re-derived at its original moment (another
  seat's sitting); my rerun names instrument, scope, and moment instead.
- The imaging-turing frame's source (sess_7318df04 msg 346) was not found in any
  byte store I can read; zknot summarizes sessions and msg-level indexes may live
  elsewhere. OWED, not asserted.
- PART A organs (mag_dance beat grid, estate_walk, voxel) were verified by file
  census and the gauntlet receipt, not by executing them this sitting.


## CORRECTION (hostile second pass, 2026-10-07; every byte below re-checked by this seat)

F3 as originally filed is corrected on three counts, all re-verified this sitting:

1. REACHABILITY (was: reachable through the two already-wired providers). FALSE
   today. memory/runs/free_lane_fleet/health.json (read this sitting):
   openrouter-free-1 consecutive_fails 6 (last_fail 2026-10-05T14:33:10Z),
   openrouter-free-2 fails 5 (last_ok 2026-10-05T07:00:27Z). The cycle loop
   SKIPS providers at fails >= 5 (tools/free_lane_fleet.py:306-308, comment:
   "dead provider; re-provision at the console, then reset health"). Ledger
   memory/runs/free_lane_fleet/ledger.jsonl last openrouter rows: HTTP 429 +
   empty completions 2026-10-05T14:33Z, zero rows since. The openrouter free
   lane has been silently dark for 2 days behind its own fence; the stale
   ALIVE-sweep 7/7 comment at tools/free_lane_fleet.py:114 is contradicted by
   its own health file. The 15-min move as written would silently never fire.
2. IDENTITY (was: the operator model IS Gemma 4 26B-A4B). Downgraded to ranked
   inference. The same snapshot also lists google/gemma-4-31b-it:free, so the
   estate instrument does not uniquely pick 26B-A4B; 26B-A4B ranks first only
   because the MoE ~4B-active shape matches "runs on nothing" (31B dense is
   not a runs-on-nothing claim). Operator referent confirmation OWED. What IS
   verified by my own HF API call this sitting: google/gemma-4-26B-A4B exists,
   license apache-2.0, createdAt 2026-03-12, downloads 44822, safetensors
   total 26544131376 (~26.5B, BF16), model_type gemma4. The active-params
   ~3.8B figure stays secondhand (web-search summary + second-pass page read;
   the HF API fields I pulled do not carry it).
3. LOCAL TAG RESOLVED (was: gemma4:latest identity unverified). My own
   /api/show this sitting: gemma4:latest = family gemma4, parameter_size
   8.0B, Q4_K_M. NOT the 26B-A4B. The local garden holds an 8B gemma-4;
   the exact runs-on-nothing model is openrouter-only among wired providers
   (nvidia removed google/gemma-4-31b-it on 2026-09-19 per
   watch/inbox/endpoint_news/endpoint_news.jsonl model_removed row).
   ai.google.dev/gemma/docs/core: NOT direct-fetched by this seat (search
   summary only); direct fetch stays OWED.

Corrected move: (a) one live curl against openrouter on
google/gemma-4-26b-a4b-it:free with the estate key; (b) on 200, reset the two
health counters (the code-documented cure at :308) and add the seat row; on
429/4xx the finding banks as PATH-DARK with the silent-fence receipt and the
move becomes console re-provision. Tightened falsifier: the curl outcome
itself, a fresh /models pull showing the :free variant gone (kills the /usr/bin/bash
clause, leaves /usr/bin/bash.09/M), or operator word that the referent is not the A4B.

## ERRATUM (2026-10-07, comics L1 landing seat; amend-never-rewrite)

F4(a) cites "discord-api-docs issue #25935". That issue number is a PHANTOM:
the fold's hostile pass checked the GitHub API for discord/discord-api-docs
and issue #25935 returned Not Found (SYNTHESIS.md, correction 2, this
directory). The number is struck inline above; the load-bearing fact F4
rests on SURVIVES on its own corroboration: Discord does not render SVG
inline, and the upload/embed whitelist is PNG/JPEG/GIF/WEBP per
docs.discord.com/developers/reference (web fetch, this fold). The
two-renderer carrier verdict is unchanged: it never rested on the issue
number alone. Erratum landed by the comics L1 lane; receipt:
LAND_L1_schema_door.md (this directory).
