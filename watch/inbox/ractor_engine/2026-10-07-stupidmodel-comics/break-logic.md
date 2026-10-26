# BREAK-LOGIC PASS: the stupid-model comics lane (hostile second pass, 2026-10-07)

Target: `logic.md` (this directory), the logic lens's five findings plus its
census correction. Method: every file:line cite re-read this sitting, every
checkable command re-run untruncated with instrument named, and the probe's
load-bearing arms RE-FIRED by importing the banked probe module verbatim
(`break_logic_rerun.py`, banked `break_logic_rerun.json`, same SCHEMA /
SOURCES / PROMPT / scoring, temperature 0, 9 calls, $0 local ollama). The
transmitted report copy truncated mid-finding-4; the verdicts below are
against the authoritative banked `logic.md`. No em-dashes.

## VERDICTS

### Census correction (logic.md:9-20): CONFIRMED, byte-exact

My rerun of the same instrument (`git grep -li <word> -- mag tools corpus
watch`, untruncated, this sitting) reads xkcd 26 / stickfigure 0 / mermaid 84
/ voxel 83 / comics 16 / electron 283, reproducing the lens's re-census
exactly and confirming the ask's numbers (23 / 3 / 65 / 69 / 67 / 241) do not
hold on today's tree. The lens's scope grammar was stated; the correction is
lawful and now double-banked.

### FINDING 1 (format door vs fleet, never fired together): CONFIRMED

Every cite holds. `tools/m1_grammar_bench.py:36-38` passes `body["format"]`
to local ollama; `watch/inbox/48h_synth/m1_bench.json` reads prompts 30,
unconstrained_valid 0/30, format_schema_valid 30/30. `tools/free_lane_fleet.py:260-268`
builds both body kinds (openai/cohere and ollama) with no format field; the
ONLY occurrence of the token "format" in that file is `fromisoformat` at
`tools/free_lane_fleet.py:345` (grep, whole file). The provider table at
`tools/free_lane_fleet.py:114-134` is exactly 7 providers (openrouter x2,
mistral, cohere, nvidia x2 running meta/llama-3.2-11b-vision-instruct,
ollama-local), so the universal "no format field on any of the 7 providers"
survives an untruncated read. Queue schema `{id, kind, prompt, max_tokens?}`
at `tools/free_lane_fleet.py:16`; `tools/gauntlet_feed.py:79-85` stages
prompt text only. The register claims (mistral 8/8 exact, collapse at 12)
bank at `watch/inbox/GAUNTLET_FREE_LANDED_20261006.md:34-37`. The remote-arm
falsifier (which providers refuse json_schema) was NOT fired this pass: it
needs the fleet door built first (the lens's own move); reported as not run.

### FINDING 2 (probe ran; door carries spec; gemma4 perfect): WEAKENED

What confirms: the banked `comic_spec_probe.json` internally matches every
number the lens reported (summary block: gemma:2b 0/3 -> 3/3 schema_ok;
qwen2.5:7b 0/3 -> 3/3; qwen2.5:3b in_character 2/3 -> 1/3 counter-instance;
gemma4 3/3 on all four). The ollama garden listing (live `/api/tags` this
sitting) holds gemma4:latest, gemma4-desk, gemma4-hermes, plus all probe
seats. AGENTS.md:7 names gemma4 as the short-worker janitor. The Gemma 4
identity is web-verified this pass: announced 2026-04-02, open weights,
on-device (blog.google, ai.google.dev, mashable; searches banked below).

What breaks: my replication rerun (identical banked constants, temperature 0,
moments apart) reads gemma:2b UNCONSTRAINED schema_ok 1/3, not 0/3 (the
merkle-collision call passed unconstrained), and gemma4:latest in_character
2/3, not 3/3 (its merkle call missed the digit+keyword rule this time). The
format arm's structural lift DOES reproduce exactly: gemma:2b FORMAT 3/3
schema_ok + 3/3 minimal; gemma4 3/3 parseable + schema_ok + minimal. So the
direction survives but two headline numbers are unstable at n=3 even at
temperature 0, and "the only seat passing the strict digit rule" does not
survive replication. The 30-prompt falsifier is not optional polish anymore;
it is a blocker before any seat assignment is banked. Provenance defect
compounding this: the banked gemma4 rows (comic_spec_probe.json:185-210)
carry no `sample` field, which every row the banked script's main() writes
carries (`comic_spec_probe.py:148-149`), and no banked script writes those
rows (only comic_spec_probe.py names comic_spec_probe.json; the three
gemma4-carrying scripts in this dir write their own results files). The
headline arm was unbanked-code until this pass; `break_logic_rerun.json` is
now the banked reproduction, rows sample-carrying.

### FINDING 3 (strict in-character rule was grader law): CONFIRMED, CONVERGENT

The in-code self-strike documentation checks (`tools/gauntlet_grade.py:66-71`
beat-regex comment; `:81-88` dice suspend-to-tool pattern) and the keyword
rescore direction is consistent with the banked samples. Two strengthenings:
(1) my rerun independently produced a THIRD instance of the same class, gemma4
in_character flipping 3/3 to 2/3 on identical inputs across sittings, which
is grader-boundary noise, not model regression; (2) caveat: the rescore
cannot be reproduced from the bank alone because banked samples truncate at
120-160 chars, so the keyword-only 3/3 / 2/3 / 2/3 recompute rests on the
lens's in-memory outputs. The renderer-footer cure and read-back falsifier
stand.

### FINDING 4 (discord door text-only; SVG cannot ride inline): CONFIRMED, upgraded

`mag/phone_relay.py:87-103` is JSON-body-only, pinned host, redirect-refused;
grep for attachments/multipart over mag/phone_relay.py + mag/salon_50.py
returns zero matches (git grep exit 1); phone_relay is the only mag/ file
referencing api.discord.com (grep over mag/). The SVG premise is no longer
OWED: web-verified this pass, Discord does not support SVG in embeds or
message images (support.discord.com feature request; discord.js guide), and
the standard workaround is SVG-to-PNG conversion at post time, which is
exactly the dep fork the lens adjudicated against on zero-dep grounds. The
adjudication (captions as text + surface URL) stands, and the falsifier (one
live post; operator demanding inline) remains the honest settle.

### FINDING 5 (composes five instruments; raster adjudicated out): CONFIRMED, two scope notes

Every compose cite byte-checks: MAG DANCE damage-map contract (beat grid as
combat tick grid, skeleton zones, PARTS match, deterministic golden angle) at
`watch/inbox/MAG_DANCE_V02_20261004.md:30-50`; `mag/surface_render.py:90-98`
baremetal_svg; roll-shape register row (mistral exact-to-8, qwen contested)
at `watch/inbox/ROLL_SHAPE_TURING_CASTLE_20261007.md:21-23` and the imaging
canon ("the maze does not teach the model, it images it") at `:106-110`;
`mag/volume_fidelity.py:1-9` (9,305 parts into a voxel grid) for the LOD-0
tie; imagegen's own boundary at SKILL.md:58-63 (when-not-to-use: SVG for
deterministic code-native output); image-blast key gate at
`.agents/skills/image-blast/SKILL.md:14-21` (planning only, keys absent).
Scope notes: (a) the imagegen cite resolves only at the user-global root
`C:\Users\foste\.zcode\skills\imagegen\SKILL.md:58-63`; the project-relative
`.zcode/skills/imagegen/` path does not exist in this repo; (b) the compose
list omits the starter-kit murmur party line the ask named (see additions).

## ADDITIONS (what the lens missed)

1. The starter-kit murmur lane is documented IN THIS TREE, not only in the
   sibling forest repo. `watch/inbox/STARTER_KIT_50WIDE_20261004.md` (439
   lines) audits it deeply: the murmur party-line lane (line 115, the
   int-murmur-partyline lane), the dead mnouretdinov/murmur Docker image
   shipped in three starter-kit files with the measured replacement
   mumblevoip/mumble-server (lines 27 and 123). The lens's blind-spot claim
   "this tree holds only one murmur hit" is a scoped grep wearing a universal:
   `git grep -il murmur -- .` reads 175 tracked files tree-wide, 19 under
   watch/, exactly one CODE hit in mag+tools (`mag/game_campaign.py:1718`,
   verified). The starter-kit CODE is elsewhere, the estate knowledge is here.
2. Pilot-n instability is measured, not hypothetical: see finding 2. The
   kill line (~90 percent at 30 prompts) now has two concrete wobbles behind
   it, and the seat-assignment line in the carrier design should not bank
   until that gate runs.
3. The gemma4 append provenance gap (no sample field, no generating script)
   is a trust-bytes defect in the lens's own bank; this pass's
   break_logic_rerun.py/.json discharges it by reproducing the arm with
   banked code and sample-carrying rows.
4. Discord SVG refusal: web-verified this pass (sources below), upgrading
   the lens's OWED to evidence; and the SVG-to-PNG workaround being the
   ecosystem standard means the zero-dep adjudication is a real fork with
   named costs on both sides, decidable by one live post.
5. The ask's session grounding holds: sess_7318df04 exists
   (`memory/zknot/LATEST.md:90-95`, 44 user messages) and its artifacts dir
   carries light-maze tool results (C:\Users\foste\.zcode\cli\artifacts\
   sess_7318df04-6115-449d-b554-2f93d5ee2a6e, "light maze" grep hit). The
   msg-346 byte-pin specifically remains OWED: no main transcript file was
   found at depth 4 of .zcode storage this pass.

## COMMANDS RUN THIS PASS (instrument record)

- `git grep -li <w> -- mag tools corpus watch` for w in xkcd stickfigure
  mermaid voxel comics electron: 26 / 0 / 84 / 83 / 16 / 283.
- `git grep -il murmur -- .` : 175 files; `-- watch` : 19; `-- mag tools` :
  one hit at mag/game_campaign.py:1718.
- `git grep -n "format" -- tools/free_lane_fleet.py` : only :345 fromisoformat.
- `git grep -c "attachments|multipart" -- mag/phone_relay.py mag/salon_50.py`
  : zero matches (exit 1).
- `git grep -n "api.discord.com|discord.com/api" -- mag/` : phone_relay only.
- `curl -s http://localhost:11434/api/tags` : 17 models incl gemma4:latest,
  gemma4-desk, gemma4-hermes, gemma:2b, qwen2.5:7b, qwen2.5:3b-instruct.
- `.venv/Scripts/python.exe .../break_logic_rerun.py` : 9 calls, banked
  break_logic_rerun.json; summary: gemma:2b UNCONSTRAINED 1/3 schema_ok,
  FORMAT 3/3 + 3/3 minimal; gemma4 FORMAT 3/3 parseable/schema_ok/minimal,
  2/3 in_character.
- Reads: m1_grammar_bench.py, free_lane_fleet.py, gauntlet_feed.py,
  gauntlet_grade.py, phone_relay.py, surface_render.py, volume_fidelity.py,
  m1_bench.json, GAUNTLET_FREE_LANDED_20261006.md, MAG_DANCE_V02_20261004.md,
  ROLL_SHAPE_TURING_CASTLE_20261007.md, STARTER_KIT_50WIDE_20261004.md,
  comic_spec_probe.py, comic_spec_probe.json, logic.md, imagegen SKILL.md,
  image-blast SKILL.md, AGENTS.md.

## WEB SOURCES (fetched this pass)

- Gemma 4 identity: [blog.google](https://blog.google) (Apr 2, 2026
  announcement), [ai.google.dev](https://ai.google.dev),
  [mashable](https://mashable.com), [deepmind.google](https://deepmind.google).
  Size lists disagree across sources (26B/31B vs 1B/4B/12B/27B); the
  operator's "runs on nothing" sub-1B reading is unconfirmed by these
  snippets; smallest confirmed bucket is 1B. gemma4:latest passing locally is
  the operative fact either way.
- Discord SVG: [support.discord.com](https://support.discord.com) (SVG not
  supported in embeds), [discordjs.guide](https://discordjs.guide)
  (attachment pattern), [dev.to](https://dev.to) (SVG-to-PNG workaround).

Not run: the remote-provider json_schema refusal trial (needs the fleet door
built; finding 1's move), the m1-scale 30-prompt rerun (finding 2's
falsifier, now mandatory), any live Discord post (finding 4's falsifier).
