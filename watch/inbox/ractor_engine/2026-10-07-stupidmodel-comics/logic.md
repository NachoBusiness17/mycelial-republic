# LOGIC LENS: the stupid-model comics lane (ractor 2026-10-07)

Lens: instrument logic. What inference rules the comic lane actually rides
(the format door, the grader verdicts, the exit contracts), where instruments
are redundant, contradictory, or blind. Jacket: two instruments disagreeing
with no adjudicator. Everything below was read or run this sitting; commands
and cites inline. No em-dashes.

## Census correction first (quantifier law)

The ask's census (xkcd 23 / stickfigure 3 / mermaid 65 / voxel 69 / comics 67
/ electron 241 across mag+tools+corpus+watch) does not reproduce on today's
tree. My re-census, `git grep -li <word> -- mag tools corpus watch` (full,
untruncated, moment 2026-10-07 this sitting): xkcd 26 / stickfigure 0 /
mermaid 84 / voxel 83 / comics 16 / electron 283. Whole-tree
(`git grep -li <word> -- .`): 47 / 2 / 215 / 326 / 29 / 727. The comic count
SHRANK vs the ask (16 vs 67) while mermaid and electron grew: the ask's
numbers are from a different moment or a different scope grammar. The prior
art is deep either way, but any comic-lane claim riding counts should ride
today's.

## FINDING 1: the format-schema door and the free-lane fleet are two proven
instruments with no composer; the ask's falsifier door does not exist on the
remote lane

- The M1 bench proved the door: `tools/m1_grammar_bench.py:36-38` passes
  `body["format"] = schema` straight to local ollama; the banked result
  `watch/inbox/48h_synth/m1_bench.json` reads unconstrained 0/30 vs
  format-schema 30/30 valid JSON on gemma:2b.
- The fleet does not have that door: `tools/free_lane_fleet.py:260-268`
  builds every provider body with NO format field (openai kind gets
  model/stream/max_tokens/temperature/messages; ollama kind gets
  model/prompt/options), and the queue schema at `tools/free_lane_fleet.py:16`
  accepts only {id, kind, prompt, max_tokens?}. `tools/gauntlet_feed.py:79-85`
  stages prompt text only. So the gauntlet register's format evidence (mistral
  exact to 8 counts, collapse at 12, `watch/inbox/GAUNTLET_FREE_LANDED_20261006.md:34-41`)
  measures FREE-TEXT format fidelity, never grammar-constrained fidelity.
- The jacket instance: M1's grammar result and the gauntlet register both make
  claims about "can cheap seats hold a format" through DIFFERENT doors, and no
  instrument adjudicates. The register numbers underestimate what the seats do
  under a grammar; M1 overestimates nothing but was never run on the remote
  seats.
- Move (~40 min): optional `format` key on queue items; fire() passes
  body["format"] (ollama) and response_format json_schema (openai kind);
  gauntlet_feed stages a comic-spec family. Falsifier: the register banks HTTP
  4xx rows naming which of openrouter/mistral/cohere/nvidia refuse json_schema;
  if all refuse, the comic lane is local-ollama-only and the discord relay
  pulls from a local seat, which is still $0.

## FINDING 2: the probe ran this sitting; the door carries the comic spec, and
the operator's named model is already in the garden with a perfect score

I ran the falsifiable probe (`comic_spec_probe.py`, banked
`comic_spec_probe.json` in this dir): 3 seats x 2 arms x 3 real session
excerpts (the gauntlet self-strike, the merkle collision, the GSTD wallet
gate), temperature 0, direct ollama, strict mechanical scoring
(parseable / schema_ok 3-4 panels + who-vocab + nonempty captions /
in_character digit+keyword from source / minimal <=140 chars per caption).
Then a 3-call gemma4 append. Results:

- gemma:2b unconstrained schema_ok 0/3 -> format 3/3, minimal 3/3
- qwen2.5:7b unconstrained schema_ok 0/3 -> format 3/3, in_character 2/3
- qwen2.5:3b-instruct unconstrained ALREADY 3/3 schema_ok; its format arm
  DROPPED in_character 2/3 -> 1/3 (a measured counter-instance: the grammar
  door helps structure, not fidelity, and can hurt)
- gemma4:latest format arm: 3/3 / 3/3 / 3/3 strict / 3/3, the only seat
  passing the strict digit rule

The "new model from google that runs on nothing" is best identified as Gemma 4
(announced 2026-04-02, open weights, runs locally on devices; sources:
blog.google and mashable via web search this sitting), and the ollama garden
ALREADY RUNS it (`/api/tags`: gemma4:latest, gemma4-desk, gemma4-hermes; the
AGENTS.md janitor tier names gemma4 as the short worker). The stupid model is
on the payroll at $0. Comic seat assignment: gemma4:latest first, qwen2.5:7b
fallback.
Falsifier: rerun at the m1 30-prompt scale; if any seat's schema_ok under
format drops under ~90 percent, the spec shrinks (2 panels, who-enum only),
which is the spec-complexity dial with a measured kill line.

## FINDING 3: the strict in-character rule was grader law, not model failure;
the digit requirement belongs at the renderer footer

Recompute at keyword-only strictness on the format arm (same banked rows):
gemma:2b 3/3, qwen2.5:7b 2/3, qwen2.5:3b 2/3. The strips talk about the right
things (regex/ms/grid/root) but do not always quote a number; my strict rule
killed them exactly the way the first gauntlet beat regex killed mistral's
perfect grid over a missing "ms" suffix (`tools/gauntlet_grade.py:66-71`
documents that self-strike in-code; corrected rows appended, never rewritten).
This is the second measured instance of the class: the grader was stricter
than the format. Cure follows the estate's carrier pattern (dice family:
the model suspends to the deterministic tool, `tools/gauntlet_grade.py:81-88`):
the model writes the jokes; the deterministic renderer stamps the provenance
(session id, source digits) in the panel footer. Trust bytes stays law
without demanding punchlines quote numbers.
Falsifier: if strips without inline numbers mislead on read-back (operator
reads the comic and believes a wrong number), the digit rule returns to the
model prompt; a read-back trial settles it.

## FINDING 4: the discord door is text-only; SVG cannot ride it inline, and the
estate pattern resolves the disagreement

`mag/phone_relay.py:87-90` is the one outbound discord door: JSON body POST,
pinned host, and grep over mag/ for attachments/multipart in phone_relay and
salon_50 returns ZERO hits, so no file-attachment codepath exists. Discord
does not render inline SVG in messages (platform behavior, NOT live-verified
this sitting: OWED; one test post discharges it). Two instruments therefore
disagree about what a postable comic is: the canonical carrier (SVG,
resolution-free, deterministic, diffable) versus the chat door (text + raster
attachments only). Adjudication by estate pattern: post the title + captions
as text plus a URL to the estate surface that serves the SVG (the
baremetal_svg pattern `mag/surface_render.py:90-98` already serves raw SVG to
dashboard panes; the Vercel URL pattern is the standing relay shape). PNG
rasterization at the door would add a dep (cairosvg/PIL) and violate the
bare-metal zero-dep law the surface renderer declares
(`mag/surface_render.py:13-15`).
Falsifier: if the operator's discord use requires the image inline with no
click, the link pattern fails his actual use and a multipart attachment leg
is owed at the door; one live post settles which.

## FINDING 5: the lane composes five standing instruments; the only new organ
is the panel renderer, an extension of baremetal_svg; the raster lane is
adjudicated out by the imagegen skill's own boundary

Composes (all verified this sitting):
- MAG DANCE v0.2: beat grid + skeleton + damage map, deterministic
  golden-angle impulses, zone keys match dashboard PARTS
  (`watch/inbox/MAG_DANCE_V02_20261004.md:30-50`). The stick figure and its
  zones exist; a panel is skeleton poses plus caption.
- `mag/surface_render.py:90-98` baremetal_svg: zero-dep SVG emitter with
  viewBox scaling; the renderer core exists.
- The gauntlet feed/grade pair: the trial instrument (with the F1 door gap).
- `mag/phone_relay.py`: the discord door (F4).
- Roll-shape cards / the light maze (`watch/inbox/ROLL_SHAPE_TURING_CASTLE_20261007.md:97-122`):
  the comic IS the maze's imaging mode; the roll-shape register gives a
  measured cast (mistral exact-to-8, qwen contested the roll, ROLL_SHAPE:21-27),
  so the comic characters have byte-backed personalities, not invented ones.

Builds: only the panel renderer (comic_renderer.py): panels grid + PARTS
stick figures + captions + provenance footer, as a baremetal_svg extension.
The voxel tie: the comic is the LOD-0 2D projection of the shadow_walk voxel
imaging (`mag/volume_fidelity.py:1-9`: 9,305 parts quantized into a voxel
grid); same cast, different projection, so no new 3D organ is owed for the
comic lane. Redundancy adjudicated: the raster organs (imagegen skill,
image-blast skill) are OUT for this lane by the imagegen skill's own boundary
(".zcode/skills/imagegen/SKILL.md:58-63": deterministic code-native output
belongs to SVG, and raster misses verbatim text); image-blast is key-gated
anyway (`.agents/skills/image-blast/SKILL.md:14-21`). xkcd minimalism is not
an aesthetic choice here, it is the raster-free contract.
Falsifier: if open-ended model action verbs cannot map to a deterministic
verb->pose table, extend the panel schema with a pose enum and rerun the
probe; if schema_ok collapses under the pose enum, the comic drops to
dialogue-only mode (two stick figures talking, which is xkcd's own dominant
mode) and the renderer shrinks further.

## Carrier design (the fold's PART C share, one paragraph)

comic_spec.v1 as probed (title + 3-4 panels of who/action/caption over the
enum operator|seat|janitor|onlooker) emitted by gemma4:latest through the
ollama format door; deterministic SVG renderer (baremetal_svg extension,
MAG_DANCE PARTS bodies, provenance footer carrying session id + source
digits); discord relay posts caption text + surface URL (phone_relay pattern);
register rows appended to the gauntlet register shape with the append-never-
rewrite law. The dice never lie: the model proposes panels, the renderer
draws, the grader scores mechanically.

## Blind spots

- Probe is pilot scale: 21 calls total (18 + 3 gemma4), temperature 0, three
  sources; NOT the m1 30-prompt scale, and the remote seats (llama-3.2-11b on
  NIM, mistral) were NOT probed because the fleet has no format door (F1);
  direct remote probing would need key handling I did not wire this sitting.
- Discord inline-SVG behavior: platform knowledge, not live-verified (OWED).
- External prior art beyond the Gemma 4 identity (SVGBob, xkcd-style
  generators, changelog-comic bots, mermaid-from-chats) was not fetched this
  sitting; PART B is the accuracy lens's lead and my fold share marks it OWED
  rather than asserting from memory.
- The "starter-kit murmur lane" named in the ask: this tree holds only one
  murmur hit (`mag/game_campaign.py:1718`, a game flavor line); the starter
  kit likely lives in the sibling forest repo, unread here (OWED).
- ollama's enum-constraint mechanism (grammar-constrained decoding vs
  post-hoc rejection) unverified; the probe shows compliance, not mechanism.
- The estate_walk LOD page and shadow_walk.html are large generated files; I
  verified their roles through volume_fidelity's port notes and the file
  grep, not by reading them whole.

Sources for the Gemma 4 identification: [blog.google](https://blog.google),
[mashable](https://mashable), [developers.googleblog.com](https://developers.googleblog.com),
[ai.google.dev](https://ai.google.dev).

## CORRECTION ADDENDUM (2026-10-07, post hostile second pass: finding 2's
## headline numbers re-measured at full scale; one claim withdrawn)

The hostile pass replicated the probe with the banked module (their
break_logic_rerun.json: gemma:2b UNCONSTRAINED schema_ok 1/3 vs my 0/3;
gemma4 strict in_character 2/3 vs my 3/3) and verdicted the n=3 cells
unstable. Both divergences verified by me this sitting: their rerun file
reads exactly as claimed, and my banked gemma4 append rows carry no sample
field (keys: booleans only), so their rerun was the first banked-script
reproduction of that arm with inspectable samples. The pass's mandate (full
trial before seat assignment) is now discharged: comic_spec_trial30.py fired
76 calls (19 prompts: 10 fresh session-fact sources + the 3 contested sources
x3 repeats; 4 seat-arm cells; temperature 0, seed unpinned = production
shape). Banked: comic_spec_trial30.jsonl (76 rows) + comic_spec_trial30.json.

Full-scale results:

- gemma:2b: schema_ok 0/19 UNCONSTRAINED -> 19/19 under FORMAT; minimal
  0/19 -> 17/19. The structural flip CONFIRMED and strengthened: pooled with
  the pass's cell the unconstrained rate is 1/22, so their counter-instance
  is the tail, not the rule.
- gemma4:latest FORMAT: schema_ok 19/19, minimal 19/19, in_character (strict
  digit+keyword) 13/19. WITHDRAWN: "perfect 3/3 including strict digit
  fidelity" and "the only seat passing the strict digit rule." gemma4 ties
  qwen2.5:7b (also 13/19 strict) as the best measured seats; neither passes
  strictly; both are ~2/3 seats under the strict rule.
- qwen2.5:7b FORMAT: schema_ok 19/19, minimal 19/19, in_character 13/19.
- Run-to-run variance now directly measured (same seat, same source, same
  prompt, three fires): the strict in_character verdict flaps on 7 of 9
  (seat,source) repeat cells (gemma:2b gauntlet 010 / merkle 011 / gstd 100;
  gemma4 gauntlet 111 / merkle 101 / gstd 110; qwen gauntlet 110 / merkle
  111 / gstd 001). schema_ok and minimal never flapped. So the unstable
  quantity is the FIDELITY metric, not the structure: comic structure is a
  stable 19/19 property of the format door; punchline digit-fidelity is a
  per-call coin at ~50-70 percent for every seat tested. This sharpens
  finding 3's cure rather than weakening it: the renderer-side provenance
  footer is not a nicety, it is the only stable carrier of the numbers; the
  model's punchlines must never be the numeric record.

Corrected seat assignment: gemma4:latest or qwen2.5:7b (tied on every stable
metric; 13/19 strict, 19/19 schema, 19/19 minimal), chosen by latency (the
trial's elapsed_s: gemma4 rows run 4-33s, qwen slower per the earlier pilot)
or by which garden seat is idle; gemma:2b remains the scut-tier fallback at
17/19 minimal. The pilot's qwen2.5:3b-instruct counter-instance (unconstrained
3/3 schema_ok; format arm dropped in_character) stays labeled pilot-scale
n=3, not re-run this sitting.

Tightened falsifier for the seat assignment: a 76-call rerun on a fresh day;
if schema_ok under FORMAT falls below 18/19 on either assigned seat, the
format door itself is unstable on that seat and the lane pins the other; if
in_character-style metrics are cited anywhere as seat discriminators without
a repeat-variance bar, that citation is void by this addendum.
