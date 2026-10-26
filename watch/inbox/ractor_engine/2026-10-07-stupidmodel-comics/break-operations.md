# BREAK-OPERATIONS pass: stupid-model comics lane (operations lens)

Hostile second pass, 2026-10-07. Seat: break-operations. Every cite below was
read or run this sitting on this box. No em-dashes. No file was edited in the
estate; the only write is this receipt.

Instrument note (what this pass ran):
- Read whole or in part: tools/gauntlet_feed.py, tools/gauntlet_grade.py,
  tools/free_lane_fleet.py (lines 1-175, 230-345), tools/m1_grammar_bench.py,
  watch/inbox/48h_synth/m1_bench.json, logs/gauntlet_free.log (whole),
  watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl (census), mag/phone_relay.py
  (lines 80-169), mag/bones_adapter.py (lines 1-120), mag/embassy_deliver.py
  (whole), scripts/gauntlet_free_30.ps1, .agents/skills/chan/SKILL.md,
  dashboard/static/chan.html (whole), probe_panel_spec_results.json,
  comic_spec_probe.json, econ_probe_results_arm_a.json, econ_probe_results_arm_b.json.
- Ran: register census (venv python, output "rows 16, Counter({'beat': 8,
  'consensus': 4, 'dice': 2, 'metagame': 2})"); ledger tail and 14:3xZ filter
  (5 rows 14:34:47Z to 14:35:22Z, all ok true); `.venv\Scripts\python.exe -c
  "import discord"` -> "discord 2.7.1"; `schtasks /Query /TN MagGauntletFree30`
  in git-bash (failed, flag mangling) then PowerShell `Get-ScheduledTask`
  (succeeded, State Ready); `git grep -l -i discord -- *.py` (18 files);
  multipart/webhook greps (zero adapter hits); `ollama list` (gemma:2b,
  gemma2:2b-instruct, gemma4:latest and 15 more on box); one WebSearch on the
  Google model identity; one WebFetch of docs.discord.com/developers/reference.
- Not run: any live Discord post (SVG-attachment preview stays OWED); any
  register write; any probe refire (sibling results on disk were read instead).

## Verdicts

### F1 gauntlet rig armed, firing every 30 min, staging zero: CONFIRMED

Every byte checked:
- Log fire stamps exact: logs/gauntlet_free.log:162,170,178,186,194
  (12:15:05Z, 12:45:02Z, 13:15:01Z, 13:45:11Z, 14:16:44Z, each "GAUNTLET-FEED:
  staged 0 trials (queue 0 pending, 12 already graded)", each exit 0). The log
  continues healthy past the lens's read to 15:50:05Z (line 218-225).
- Register census reproduced exactly: 16 rows, beat 8 / consensus 4 / dice 2 /
  metagame 2. No comic family.
- Fleet ledger 14:3xZ rows exist: 5 rows 14:34:47Z through 14:35:22Z, all
  ok true. Nit: the window opens at 14:34:47Z (mistral), not the lens's
  14:34:54Z (that is the nvidia-1 row); subset claim, not an error.
- Staging point tools/gauntlet_feed.py:99-138 (build_batch) and grading point
  tools/gauntlet_grade.py:138-171 both byte-accurate. The move's --count flag
  exists (gauntlet_feed.py:143).

Sharpeners the lens dropped:
1. The rig failed silently THIS morning: gauntlet_free.log:2-8, ModuleNotFoundError
   exit 1 at 01:56:15Z and 02:18:19Z, cured into the burners cage
   (scripts/gauntlet_free_30.ps1:32-35, docker compose run burners; the -T
   stdin fix at :15-20). The falsifier's 60-minute paranoia is justified by
   same-day history, not hypothetical.
2. The falsifier conflates seat-failure with rig-failure: gauntlet_grade.py:149-151
   skips trials whose only ledger rows are ok False, silently; a comic item
   popped by a failing provider retries (free_lane_fleet.py:336-339 retires
   only ok-fires) but shows nothing in the register inside the window.
3. The move's command `python -m tools.gauntlet_feed --count 6` uses bare
   python, the exact class that produced the 01:56Z failure (AGENTS.md: PATH
   python is the Hermes venv). The move must read
   `.venv\Scripts\python.exe -m tools.gauntlet_feed --count 6`.

### F2 M1 result does not transfer to the fleet: WEAKENED

Code cites all byte-true:
- watch/inbox/48h_synth/m1_bench.json:5-9 (unconstrained_valid 0,
  format_schema_valid 30, verdict "M1 CONFIRMED").
- tools/m1_grammar_bench.py:36-38 (body["format"] = schema) and :36
  (temperature 0).
- tools/free_lane_fleet.py:260-268: openai/cohere body carries
  model/stream/max_tokens/temperature/messages only; ollama body carries
  model/prompt/stream/options. No format or response_format anywhere.
- Corrected beat rows at 00:15:05Z: register rows 12-15, mistral 8/8 (v1, v2),
  cohere 6/6 (v3). Nit: cohere v4 is FAIL 3/12 on the 12-move variant, so
  "cohere 6/6" is the 6-move row only; line grammar is 2/2 on mistral, 1/2 on
  cohere.

Why weakened, not confirmed: the same bank directory this lens wrote into
already holds fired measurements that contradict the recommendation, and a
second confound was dropped.
1. The preferred branch (line grammar through the queue door) has been fired
   and measured weak: econ_probe_results_arm_a.json, arm "A: queue door,
   unconstrained line grammar", 13 fired, 2 pass (mistral 0/4, cohere 0/3,
   llama-3.2-11b 1/4, qwen2.5:7b 1/2). The beat-family precedent does not
   carry to the comic grammar at fleet temperature.
2. The rejected branch (format door) measured strong where fired:
   econ_probe_results_arm_b.json, gemma:2b 5/5 json_ok but 2/5 pass,
   qwen2.5:7b 5/5 pass, median 9.1s; comic_spec_probe.json gemma4:latest
   3/3 on parseable, schema_ok, in_character, minimal.
3. Dropped confound: M1 ran temperature 0 (m1_grammar_bench.py:36) while every
   fleet seat fires temperature 0.3 (free_lane_fleet.py:262 and :267); even a
   response_format amendment would not transfer M1's 30/30 cleanly. The one
   arm proven at 0.3 is the beat line grammar, which is why it looked strong.
The finding's code facts stand; its engineering disjunction resolves the
opposite way to the data: the format-door amendment (or direct ollama door)
is the measured-strong route, the line-grammar-through-fleet route measured
2/13.

### F3 1200-char truncation + grader-artifact precedent + token caps: CONFIRMED

- tools/free_lane_fleet.py:296 `return True, text.strip()[:1200]` exact.
- tools/gauntlet_grade.py:153 `text = str(row.get("detail", ""))` grades the
  truncated string verbatim.
- The BEAT_ONSET confession is at tools/gauntlet_grade.py:66-71, word for word
  the class the lens described ("a perfect half-beat grid ... graded 0/4
  parseable ... Corrected rows are appended, never rewritten"); register rows
  1-4 (FAILs, 00:13:21Z) vs corrected rows 12-15 (00:15:05Z) verified.
- Ollama cap tools/free_lane_fleet.py:267 num_predict 300 verified.

Additions: the openai/cohere seats carry max_tokens 700 (free_lane_fleet.py:262),
so the 1200-char truncation binds first on 5 of 7 seats and the 300-token cap
binds only the ollama seat; and the ledger's chars field is computed
post-truncation (len(out) at :325, out already sliced at :296), so chars == 1200
exactly is already a free truncation flag the grader can read, making the
proposed length column nearly zero-cost.

### F4 no Discord file door + SVG embed bar: CONFIRMED

- mag/phone_relay.py:93-95 (urllib Request, data json.dumps, Content-Type
  application/json) and :137-159 (_dm_channel, "Never a shared guild channel")
  verified. Universal scoped and censused: git grep for multipart / files[ /
  send_file / File( over both adapters returns zero hits (only .is_file()
  checks at phone_relay.py:66,79,114,141 and bones_adapter.py:337).
- mag/bones_adapter.py:60-61 (GUILD_ID/CHANNEL_ID pins), :66 (MAX_MESSAGE
  1900), :99-105 (fmt_block code fence + truncate) verified.
- discord.py 2.7.1 importable: re-run this sitting, output "discord 2.7.1".
- Discord docs fetched this sitting (docs.discord.com/developers/reference):
  uploads need multipart/form-data with files[n] and payload_json; embed
  attachments whitelist quoted verbatim: "Only .jpg, .jpeg, .png, .webp, and
  .gif may be used at this time." SVG appears nowhere on the page. The lens's
  doc claims are exact.
- Census beyond the lens: repo-wide Discord-webhook grep finds only the
  hermes_wings stolen-code bridge name-list (watch/hermes_wings/src/toolsets.py:628),
  external reference code, not an estate surface; mag/embassy_deliver.py is a
  GitHub publisher (git init/push, gh repo create), not Discord; mag/salon_50.py
  carries no Discord send path. The two-surface claim survives the census.

Dropped conditions: bones_adapter already imports discord.py 2.7.1
(mag/bones_adapter.py:50-51), so the library's native File/multipart support
makes the guild channel the cheap upload door (a small adapter extension),
while phone_relay is raw urllib JSON and would need hand-rolled multipart;
and the PNG-twin tax is Discord-only (see chan addition below).

## What the lens missed (additions)

1. THE PROBE IS FIRED, NOT DESIGNED. The lens's own bank directory holds
   sibling-lane results from this same sitting: probe_panel_spec_results.json
   (ts 2026-10-07T14:56Z, 32 rows, direct ollama), comic_spec_probe.json
   (21 rows, 4 seats x arms), econ_probe_results_arm_a/b.json (13 + 10 fired).
   Blind spot 2 ("no register row exists until the F1 feeder amendment lands")
   is true only of GAUNTLET_REGISTER.jsonl and false as a statement of the
   fold's knowledge: parseable/schema/in-character/minimal measurements exist
   on disk. The fold's "ONE falsifiable probe" deliverable is already answered
   in part: gemma4:latest 3/3 on all axes (comic_spec_probe.json:185-210, 255-261),
   qwen2.5:7b format-door 5/5 pass (econ arm B), fleet line-grammar 2/13
   (econ arm A), deepseek-r1:1.5b the failure seat at spec_valid 1/8
   (probe_panel_spec_results.json:28-35).
2. The named Google seat is absent from the fleet but present on the box.
   PROVIDERS (tools/free_lane_fleet.py:115-137) is seven providers, zero
   Google models; the ollama seat fires qwen2.5:7b only. `ollama list` this
   sitting shows gemma:2b (1.7 GB), gemma2:2b-instruct-q5_K_M (1.9 GB) and
   gemma4:latest (9.6 GB) installed. The queue-door route can therefore never
   fire the operator's named seat class; the direct-door probes already did.
   Move: add an eighth provider entry on the same loopback URL with
   model gemma:2b (the _ALLOWED_URLS guard at :139 is URL-keyed so the same
   URL passes), or accept the direct door as the Google-seat lane.
3. Queue-pop assignment breaks same-seat A/B. free_lane_fleet.py:310-312 pops
   each queue item to exactly ONE provider per cycle, so "one JSON trial and
   one line twin through the same queue" lands them on different seats; the
   econ arm A by_model table (4/3/4/2) is exactly this pop shape. The format
   delta is confounded with the seat delta unless ids are replicated per arm
   (the consensus a/b/c pattern in gauntlet_feed.py:135-137 is the precedent).
4. Blind spot 3 is closed: the task registry answers from PowerShell.
   `Get-ScheduledTask -TaskName 'MagGauntletFree30'` returns State Ready;
   action is wscript.exe //B //Nologo scripts\run_hidden.vbs wrapping
   powershell.exe scripts\gauntlet_free_30.ps1. The lens's enumeration failure
   was git-bash flag mangling, reproduced verbatim this sitting
   (`schtasks /Query` -> "Invalid argument/option - 'C:/Program Files/Git/Query'").
5. The chan board is text-only, and that flips the SVG tax. chan.html:131-140
   renderComment escapes all HTML and emits no img tag; catalog thumbs are
   styled divs (chan.html:51-53, 210-215); the post schema carries text only
   (chan.html:186-191). A comic cannot ride the board today, but the board is
   a browser surface: one whitelisted image-URL field renders SVG natively
   with no PNG twin. The PNG conversion is a Discord-leg tax only, not a
   carrier-wide constraint, which slightly reshapes the lens's F4 conclusion.
6. Model identity (blind spot 1) searched, not resolved: no single "runs on
   nothing" Google announcement found; 2026 candidates are Gemma 4 (announced
   2026-04-02, E2B/E4B edge sizes, blog.google) and EmbeddingGemma 2 (740M,
   embedding-only, cannot hold a chat register). Identity stays OWED and is
   moot for the probe: gemma4 and gemma:2b are banked locally with fired
   results (addition 1).

## Standing OWED after this pass

- Discord SVG file-attachment (non-embed) inline preview: still unverified,
  needs one live post through an amended door.
- The operator's exact named model: INTERPRETIVE, Part B (accuracy lens).
- Downstream fold-out of the gauntlet register (blind spot 5): not audited
  here either; 16 rows banked, zero folded out, and now three more result
  files join the unread-register risk class unless the fold reconciles them.

Verdict line: F1 confirmed, F2 weakened, F3 confirmed, F4 confirmed. The lens's
code-reading is byte-clean throughout (every path:line cite checked true); its
probe-design recommendation is what broke, contradicted by fired results
sitting in its own bank directory.
