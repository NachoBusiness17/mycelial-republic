# STEAL: five X-post briefs mapped onto Mag (2026-10-17)

Written 2026-10-17 around 8 PM ET by a Grok Bot worker. Read-only pass: no code changed, no git, no model calls.
Sources: the posts were fetched through the public fxtwitter API, the papers through the arXiv API, abs pages and HTML,
and Mag files were read in place. Each claim below carries its own evidence tier. Tiers are never merged:

- **measured**: I ran or read the thing myself (a file:line, a PDF page count, a toy simulation).
- **paper claim**: the authors say it. I did not reproduce it.
- **conceptual**: an idea or framework with no measurement behind it.
- **recommendation**: my proposal for Mag. It is a suggestion, not a fact.
- **creative**: a design or artwork. There is nothing to verify.

## 1. Verification table

Post times are converted from UTC to ET (UTC-4).

| # | Post (author, time ET) | Brief's claim | Verdict | What the source actually says |
|---|---|---|---|---|
| 1 | @vincieye, Oct 17 8:00 AM | Motion- and gravity-aware feed-forward 3D reconstruction, arXiv:2610.22177 | **Confirmed** | Post links arXiv 2610.22177v1. Title "Motion- and Gravity-Aware Feedforward 3D Reconstruction" by Shiyao Qian, Yuan Ren and Dongfeng Bai, submitted 2026-10-15. |
| 1 | | Uses LUPI (privileged info at training time only) | **Confirmed** (paper claim) | Abstract: residual optical flow and gravity direction are privileged signals in training, and inference uses standard visual inputs only. |
| 1 | | "Zero inference cost" | **Softened** | The post says "zero inference overhead". The paper says "without increasing test-time complexity" and "lightweight architectural changes". I found no latency or FPS figure in the paper HTML, so "zero" is the post's rounding of a complexity claim, not a measured runtime. |
| 1 | | (not in brief) | Note | The best place to inject the priors depends on the backbone: middle layers suit VGGT, late layers suit pi3. |
| 2 | @tokufxug, Oct 16 10:14 PM | Dense4D: feed-forward dense 4D correspondence across body, clothing and hair from monocular RGB, no template | **Confirmed** (paper claim) | arXiv 2610.22325 "Dense4D: Pixel-Level 4D Human Correspondence". The abstract says "to our knowledge the first feed-forward model" and "without a body template". The post itself gives no link. It says the source is in the replies, which I could not read. I found the paper by an arXiv search. |
| 2 | | Imperial College London | **Confirmed** | Project page alpguler.com/dense4d: "Riza Alp Guler, Imperial College London". arXiv lists one author, while the post says "Guler and colleagues". Code is "coming soon". |
| 2 | | "1,287 frames in 86 s" | **Misleading** | Project page: "the full 86-second sequence, 1,287 frames sampled at 15 fps, in a single forward pass". 86 s is the length of the video, not the processing time. No compute time is given. |
| 3 | @10m8mkW (Tom Wakayama), Oct 16 9:12 PM | Open-ended discovery as statistical abduction, using possibility theory and e-possibility with anytime-valid guarantees | **Confirmed** | arXiv 2610.11289 "Open-ended Scientific Discovery with Possibilistic Reasoning" by Anita Yang, Siu Lun Chau, Tomoya Wakayama, Krikamol Muandet and Masaki Adachi (2026-10-08). The paper defines e-possibility from an e-process as pi_t(theta) = min over s<=t of min{1, 1/E_s(theta)}, following Martin (2026). Its Prop. 6 proves E_t is a nonnegative supermartingale under adaptive experiments. The algorithm is "possibility frontier search". |
| 3 | | "The post gives no paper link" | **WRONG** | The post text ends with https://arxiv.org/abs/2610.11289. Wakayama is also the 3rd of 5 authors, not the sole author. |
| 4 | @clcoding, Oct 17 2:12 AM | Free book "Foundations of Large Language Models" by Tong Xiao and Jingbo Zhu, arXiv:2501.09223 | **Confirmed, one hop away** | The post names neither the authors nor the arXiv id. It links clcoding.com, and that page credits Xiao and Zhu and links arXiv 2501.09223. arXiv: v1 2025-01-16, v4 2026-10-08. The post's "315 pages" checks out: the current PDF has 315 pages (pdfinfo, measured). The book has six chapters: pre-training, generative models, prompting, alignment, inference, reasoning. |
| 5 | @jagarikin, Oct 17 3:57 PM | Penrose Rubik's Cube design with a GIF | **Confirmed** (creative) | Post text: "Out of the blue, I came up with something I call a Penrose Rubik's Cube." It has one GIF, which I did not view. There is no paper and nothing else to verify. |

Errors in the briefs: (1) #3 says there is no paper link, but there is one. (2) #2 turns an 86-second clip into
what reads like an 86-second runtime. (3) #1's "zero" is stronger than the paper's "no added test-time
complexity". (4) #4's attribution is right, but it comes from the linked blog, not from the post.

## 2. What Mag already has (measured, file:line)

- **Fleet report has no evidence-tier field.** `configs/fleet_report.v1.schema.json:8-46` lists every property:
  none is a confidence, tier or evidence field. `:46` sets `additionalProperties: false`, so a seat cannot add one
  on its own today. The stdlib validator already handles enums (`mag/fleet_report.py:91-93`) and reads the schema
  file as the single source of truth (`mag/fleet_report.py:16-20,124-136`). Notices are not `watch/receipts/N-*`
  files. They are `seat_*.json` receipts whose body is a NOTICE carrying `notice_id: N-...`. Example:
  `watch/receipts/seat_20261017T201014712000Z_grok_a8b9ea7cff54.json`. Its own narrative mixes a fact
  ("inventory fact") with an unverified note (".env not opened"), and nothing in the schema tells them apart.
  `notices()` builds the served row at `mag/fleet_report.py:278-282`.
- **The librarian's "tier" means something else.** In `scripts/inbox_librarian.py` a card's `tier` records which
  classifier placed the file (`rule`, `model`, `model-folder` or `pending`; `:389-390,407,437-455`). `confidence`
  is the local model's shelf-placement score (`:229,251,461`). Neither describes the evidence inside the document.
  A new field must not reuse the name `tier`.
- **Harness2 merges evidence into one scale.** `mag/harness_probe.py:76,134` asks the composer for a
  single `confidence: low | medium | high`. `:422-425` writes it into the law-rib AMENDMENT.
  One composer opinion from a single paired run counts as "evidence".
- **Harness2 adopts after one paired round.** `pending_candidates` never re-probes a candidate it has already used
  (`mag/harness_probe.py:300,305`). `judge` proposes on a single "composer chose the candidate" (`:374-375`).
  After that, adoption is a seat vote (`mag/proposals.py:289-322`, quorum plus the non-GLM approval). The Harness2
  steal already flags this risk: "Single-run probes are noisy ... treat one day as one sample"
  (`watch/LIBRARY/STEAL_HARNESS2_20261017.md:178-181`). The blinding is by label only (`mag/harness_probe.py:40-41`).
- **No anytime or sequential statistics anywhere.** `rg` for e-value, anytime, Ville, martingale, SPRT and
  sequential across `mag/ scripts/ configs/ tests/` finds only unrelated hits (lane load "sequential",
  off-hours "anytime"). The nearest relatives are fixed-n tests. `scripts/light_replay_falsifier.py:1-25` uses a
  one-sided two-proportion test at a fixed 100 trials. `mag/falsifier_counter.py:79` keeps engagement at
  "seen, never closed". `mag/consensus_gate.py:1-8` already holds the law that correlated agreement is not proof.
- **Build-time-only priors already exist.** The law pack is compiled offline by `tools/thought_quantizer.py:173`
  (`compile_packs`; refuses empty compiles, `MIN_KEPT_LAWS = 1` at `:96`), re-run by `scripts/lawpack_daily.ps1:1-30`,
  and age-gated by `mag/boot_regen.py:1-30`. The runtime consumer reads only the compiled pack.
  `scripts/light_replay_falsifier.py:1-20` has the same shape: one expensive "frontier pass" writes FIELD.json,
  and the "dumb" marbles only read that light at runtime.
- **INDEX.md is regenerated.** `scripts/inbox_librarian.py:312-336` rewrites `watch/LIBRARY/INDEX.md` from a fixed
  list. Hand-appended lines, including the existing Harness2 line and the one added for this report, disappear on
  the next librarian run. Fixing that would be a separate small change: keep a `## Steals` tail or read
  `STEAL_*.md` cards. Not done here.

## 3. Steal-by-steal verdicts

### (a) Evidence-tier enum: WORTH BUILDING (small)

The briefs' own meta-point is right, and Mag shows the exact gap it describes: one `confidence` scale in Harness2,
and NOTICE narratives that mix verified and unverified facts.

**Smallest build (recommendation):**
1. Add one optional property to `configs/fleet_report.v1.schema.json`:
   `"evidence_tier": {"enum": ["measured", "paper_claim", "conceptual", "recommendation", "creative", "unverified"]}`.
   The validator needs no change, because the enum path already exists (`mag/fleet_report.py:91`). Carry
   `evidence_tier` in the notices row (`:278-282`) and mention it in the MCP description (`:315-321`).
   The stdlib validator only checks string arrays, so it cannot check per-claim objects. That leaves one tier per
   report. The doctrine line for that is: one report per tier; split mixed findings into separate reports.
2. Harness2, after the other worker lands `harness_probe.py` (do not touch it now): add `tier: measured | judged`
   next to `confidence` in EXPERIENCE (`:76,134,338`) and write it into the AMENDMENT block (`:422-425`). A
   composer preference is `judged`. Only a checkable output (count, test, diff that runs) is `measured`.
3. Librarian: lowest value. If it is done at all, add a card key named `evidence_tier`, never `tier`, defaulting to
   null, with only a filename rule. For example, `STEAL_*` gets `mixed` because the report carries its own table.
   Skipping this is fine.

**Tests that prove it:**
- `tests/test_fleet_coordination.py:63` keeps passing: schema and validator agree on kinds.
- New: a NOTICE with `evidence_tier: "measured"` validates. `evidence_tier: "high"` is refused with "must be one of".
- New: `notices()` rows carry `evidence_tier` when set and omit it when absent. Old receipts still parse.
- New: a report without the field still validates, so the field is optional and nothing breaks.

### (b) Anytime-valid e-process as the Harness2 adoption rule: WORTH BUILDING (best steal)

Brief #3's machinery (e-processes and Ville's inequality, which the paper builds on; Prop. 6) fits the exact weak
point above. Today one noisy composer preference can start an adoption. With an e-process, the same candidate is
re-probed over several days, and Mag files a proposal only once the accumulated evidence crosses 1/alpha. Peeking
after every round stays valid. Mag only needs this part. Possibility frontier search and abductive utility (the
paper's open-ended discovery algorithm) do not map onto any Mag organ, so they are no steal.

**Rule (recommendation).** Count each paired round as one outcome from the blinded composer: win (it chose the
candidate), loss or tie. Start the wealth at W = 1. A win multiplies W by (1 + lam) and a loss by (1 - lam). A tie
leaves W unchanged. Use lam = 0.5. The null hypothesis is that the candidate wins at most half of the rounds that
are not ties. Under that null, W is a nonnegative supermartingale, so P(W ever reaches 1/alpha) <= alpha, however
often you look. Adopt when W >= 1/alpha. Drop the candidate when W <= 0.05 or after a round cap. Stopping early for
futility never inflates false adoptions.

**Toy simulation (measured on the box, 20,000 seeded runs, peeking after every round):**

| truth | alpha | rule | false/true adoption | median rounds to adopt |
|---|---|---|---|---|
| coin flip (p=0.5), 200 rounds | 0.10 | e-process | 8.7% false (bound 10%) | 14 |
| coin flip (p=0.5), 200 rounds | 0.05 | e-process | 3.9% false (bound 5%) | 19 |
| p=0.75, 30 rounds | 0.10 | e-process | 83% adopted | 12 |
| p=0.90, 30 rounds | 0.10 | e-process | 99.9% adopted | 6 |
| coin flip | any | today's rule (first win) | about 50% false | 1 |

Cost, stated plainly: at alpha = 0.1, a candidate needs at least 6 straight wins, or 8 wins if it also has one loss.
At k=1 that is one to two weeks of paired days (two packs a day) per adopted edit. That is the price of not adopting
noise.

**What it does NOT prove.** The guarantee covers "this blinded judge prefers the candidate more than half the time",
not "the candidate is better". The composer seats share a model family, and blinding is by label only
(`harness_probe.py:40-41`), so a systematic judge bias passes straight through. Keep the non-GLM quorum
(`proposals.py:322`) on top. `mag/consensus_gate.py:1-8` already states this law.

**Smallest build:**
1. New pure module `mag/eprocess.py` (stdlib, about 40 lines): `update(w, outcome, lam=0.5)`,
   `decide(w, alpha, floor, rounds, cap)` returning adopt, drop or continue, and a `ville_bound(alpha)` docstring.
   It has no I/O and no model calls.
2. In `harness_probe.py`, after the other worker finishes and with their agreement:
   - Store `wealth`, `rounds` and `outcomes[]` per candidate under `logs/mates/harness_probe/`.
   - Let `pending_candidates` (`:300-305`) re-queue a candidate whose decision is still "continue".
   - In `judge` (`:374`), record a candidate win as one outcome. Return `propose` only when `decide` says adopt.
   - The AMENDMENT carries `tier: measured` plus the final W and the number of rounds.
   - Config: `harness_probe.alpha` (default 0.1), `lam`, `round_cap`.

**Tests:**
- `test_eprocess_null_false_adoption`: 10k seeded coin-flip runs, 200 rounds, peeking every round. The false-adopt
  rate stays at or below alpha plus a Monte-Carlo slack of 1 percentage point.
- `test_eprocess_power`: at p=0.9 most runs adopt within 30 rounds.
- `test_ties_do_not_move_wealth`; `test_lam_must_be_in_0_1_open`; `test_wealth_never_negative`.
- `test_single_win_files_no_proposal`: one `adopt` verdict leaves the round open and creates no proposal folder.
- `test_crossing_files_one_proposal`: the round that crosses 1/alpha files exactly one proposal, and refiling is
  idempotent.
- The existing Harness2 tests and `tests/test_fleet_coordination.py` still pass.

### (c) LUPI (build-time-only priors): NO NEW BUILD

The structural idea (privileged material used offline, zero cost at runtime) already exists in Mag: the law pack
compiled by thought_quantizer and gated by boot_regen, the light-replay FIELD.json, and Harness2 itself, where the
composer sees both receipts and the mates only ever see the adopted delta. The paper's real content is training a
network with a privileged teacher and then distilling. Mag does not train the models it runs, so that part has
nowhere to go. One phrase is worth keeping in doctrine: "privileged at build, absent at run". At most, add a test
that the compiled pack never contains its build-only sources. Optional, and not specified further here.

### (d) "Foundations of Large Language Models": LIBRARY REFERENCE ONLY

This is a good reference book (arXiv 2501.09223, v4 2026-10-08, 315 pages, chapters on pre-training, generative
models, prompting, alignment, inference and reasoning). It changes no code. Suggested card if a seat wants one: a
`BETA_`/`EPSILON_` reference with `evidence_tier: paper_claim` (textbook). I did not add a catalog card, because this
task allowed only this report plus one INDEX line.

### (e) Dense4D and the Penrose cube: NO STEAL

Dense4D is human 4D vision. Mag has no vision pipeline that needs dense correspondence. The Penrose Rubik's Cube is a
creative design. Neither maps onto any existing organ, and inventing one would break the "existing organs only" rule.

## 4. Order of work

1. (b) `mag/eprocess.py` plus its tests. It is a pure module and safe to land now, because it does not touch
   harness_probe.py.
2. (a) the schema field plus its tests.
3. Wire (b) into harness_probe.py once its current builder is done.
4. The INDEX-regeneration fix (section 2, last bullet), so steal lines survive the next librarian run.

Unverified and left that way: Dense4D's real compute time, any runtime measurement for the 2610.22177 model,
the contents of the jagarikin GIF, and the reply that carries the source for #2.
