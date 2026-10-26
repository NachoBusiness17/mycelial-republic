# WAVE 2 · LANE 9 — NARRATIVE DRIFT
### What the fleet says about itself vs what the bytes say
*2026-09-26 · read-only, no repairs · seat: L9 narrative-drift*

The fleet has ~100+ receipts in `watch/inbox/` and 3,213 `.md` files under `watch/`. That
corpus is where the fleet's self-image lives. This lane reads the self-image and checks it
against bytes. The verdict is not "the fleet lies" — it is worse and more useful than that:
**the fleet is honest about what it does not know, and careless about what it thinks it
knows.** The receipts are exemplary about hedges and reckless about numbers.

---

## HEADLINE FINDINGS

| # | Finding | Byte status |
|---|---|---|
| 1 | **The census carrier in `AGENTS.md` is 384 tests wrong and the fleet has refreshed it 5 times today without fixing it** | CONFIRMED (2,294 live vs 1,910 claimed) |
| 2 | **The verkle chain lost 2,115 rows in a self-inflicted incident; the fleet's own receipts document it in detail and no doc has been updated** | CONFIRMED (9,873 → 7,757/7,829) |
| 3 | **`docs/ref/SPORE_CONTINUITY_SCHEMA.md` hardcodes a dead chain tip (7,392 leaves / root 0a141dcb)** | CONFIRMED FALSE |
| 4 | **14.3% of receipts (431/3,009) state confident conclusions with no instrument, no command, no byte, and no tri-state marker** | CONFIRMED by scanner |
| 5 | **The confident-voice rate is 43% at line level — but that over-counts. The honest file-level number is 14.3%.** | Both reported |
| 6 | **The single most-deferred category is not work — it is re-verification of work already claimed done** | 1,166 receipts |

---

## 1. THE NARRATIVE vs THE BYTES — the 10 most recent substantial receipts

Read by mtime, excluding `audit_20260926/`. Each claim below was spot-checked against a byte.

### F1. The census carrier — the flagship, and it is still wrong

`AGENTS.md:27` claims:

> **Tests:** 1,910 tests collected / 303 files (2026-09-26 census, `pytest --collect-only -q`, receipt `watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md`

Live, same tree, same day, this lane:

```
$ ./.venv/Scripts/python.exe -m pytest --collect-only -q
2294 tests collected in 6.38s

$ ./.venv/Scripts/python.exe tools/census_drift_patrol.py --collect
CENSUS-PATROL: COLLECT-DRIFT - collected drift: pytest holds 2294 vs carrier
               claim 1910 (delta +384, bar 20)
```

**The drift is not a static error. It is a race the fleet lost five times in one day.**
Reading the receipt chain in order, every one of these was "byte truth" when filed:

| Receipt | Claimed collected | Note |
|---|---|---|
| B2_69 (09:49) | 1,837 | the census that replaced the retired 1,341 |
| B2_216 (~10:04) | 1,854 | "+17 items / +2 files" — **explicitly explains the delta** |
| B2_244 | 1,879 | builds the `--collect` gate; refreshes carrier to 1,879/302 |
| B2_244 (20 min later) | 1,892 | "+13 more items landed by concurrent lanes" |
| B2_246 | 1,910 | refreshes carrier to 1,910/303; **ships the daily scheduled check** |
| B2_247 | 1,914 | live base gate "exit 0" — **+4 delta, inside the bar of 20** |
| `AUDIT_GOPHER` (20:37) | 2,288 | **flags it: "detector works, detector is armed, detector was not consulted"** |
| this lane (22:0x) | **2,294** | delta now **+384** |

**The finding underneath the finding:** the `--collect` gate shipped at B2-244 with a
tolerance bar of 20 to absorb exactly this intra-day landing noise. The noise was ~+13 per
20 minutes. So the gate has been mathematically incapable of firing on a day when tests are
landing continuously. It reads `exit 0` and prints "collect ok" while the claim is 384 off.
**A gate sized for its own failure mode became blind to it.**

B2-216 deserves credit: it is the one receipt in the chain that names the denominator law
and explains *why* two counts differ. That is the correct behavior. It was not applied at
the other four refreshes.

### F2. Gopher's audit is the counter-example — and its own number is already stale

`watch/inbox/AUDIT_GOPHER_20260926.md` is the best-evidenced receipt in the corpus. Every
finding carries a command, a byte count, a sha256, or a `file:line`. It states its own blind
spot in a "Not measured" section. It found the 1.18 GB duplicated-ledger pair with matching
hashes, and root-caused it to a single-star `.gitignore` pattern at line 142.

It measured **2,288** collected. Byte truth is now **2,294**. Six tests landed in the hour
between a rigorous audit and this one. **Even the fleet's best instrument is a snapshot, and
the repo's own census denominator law says so out loud.** Gopher's own F1 finding is
therefore not "the number is wrong" but "a number is always wrong" — and the fleet keeps
treating each refresh as the fix.

### F3. ATLAS's leak law — verified, and the sharpest thing in the corpus

`watch/inbox/ATLAS_SELF_STEAL_20260927.md` claims a "leak law": momentum is lost wherever a
receipt lands without a ledger row, a ledger row without an index key, or an index without a
reader. Spot-checked:

| ATLAS claim | Byte check | Verdict |
|---|---|---|
| "99 receipts landed-unindexed" | not independently recounted | UNVERIFIED |
| "552-row burn ledger" | `wc -l memory/burns/LEDGER.jsonl` → **557** | MOVED +5 |
| "ESTATE_INDEX (1.7M rows)" | newline count → **1,700,130** | EXACT |
| "librarian report 16 days stale owing 198 primary pulls" | mtime 2026-09-10, header `## RETRIEVAL-PLAN (198)` | EXACT |
| "FTS5 indexes path+title ONLY" | `tools/corpus.py:198` selects `r.id, r.path, r.zone, r.ext, r.bytes, r.mtime, r.title` | EXACT |
| "brief organ frozen 2026-09-26" | `memory/briefs/latest.md` is `-r--r--r--`, mtime 09-26 14:01 | EXACT |
| "SEATS.md (Aug 14) and HABIT.md (Aug 6)" | git: SEATS last commit **Aug 19**, HABIT **Aug 6** | Aug 19 vs Aug 14 |

ATLAS found the single most important structural fact in this report, and 4 of 6 checkable
numbers are exact. The burn ledger drifted +5 in the hour between filing and checking — which
is F1's disease again, at smaller scale, and nobody will ever notice because +5 is not
alarming.

**ATLAS's own GAP 1 is the sharpest finding, and it is the fleet contradicting itself.**
ATLAS says the frozen brief is still consumed by both the AGENTS.md load order and
context-pack. Byte check on `AGENTS.md`:

- **line 51:** `state/CURRENT.md` (live truth; `memory/briefs/latest.md` FROZEN 2026-09-26 **and must not be consumed as live**)
- **line 55:** `- Prefer `memory/briefs/latest.md`, `memory/live_from_grok.md`, ...`

**The same file, five lines apart, says "never read this" and "prefer this."** ATLAS caught
the conflict; nobody has fixed it. `mag/context_pack.py` calls `latest_brief_text()`
(line 531) into every mode tier, so a cold seat is injected with the August fossil it was
frozen to stop receiving. This is not a wrong number — it is a *law that contradicts itself in
the boot file*, and it survives because the census patrol only parses the Tests bullet.

### F4. WIDTH_LEDGER and LITE_LANE doctrine — properly cited

`WIDTH_LEDGER_20260926.md` claims 109.4M tok/h at width 10. Traced to
`B2_25_envelope_remeasure_20260926.md:25` (37,386,533 tokens / 0.34165 h) and — better —
**independently reproduced** by `B2_424_envelope_harvest_20260926.md`, which re-derives all
four figures from live bytes with exit 0. This is the corpus's gold standard: a claim, its
arithmetic, and a second tool that regenerates it.

The ledger also models the honest case. "Regular GLM: **NOTHING: zero data in the entire
estate**" and "DARK" is the fleet correctly declaring a blank instead of inventing a number.
That discipline is real and it is why the census failures stand out.

### F5. THIRD_WAY_FALSIFIER_REGISTRY — self-labels its own unbacked cells

11 falsifiers, 8 `pending-playtest`, 3 `armed`, 0 fired. It states in bold that F2 and F4
were carried "by name and observable instrument only" and that "a byte-read of the salon's
F2/F4 wording is owed before playtest day so the registry's threshold cells stop saying
'per salon'." **This is the law obeying itself.** Two of its own cells are marked unbacked,
in writing, with a date.

---

## 2. THE CONFIDENT-VOICE PROBLEM — quantified

The repo's law, `AGENTS.md:27`: **"Trust bytes, not reports."** And: **"never trust a
hand-written count."** The question is how often the receipts violate that.

**Method, stated so it can be attacked.** Two passes, because one pass lies.

**Pass A (line level, over-fires).** 1,762 receipts in `watch/inbox/`. A line counts as an
*assertion* if it makes a factual claim; it counts as *unbacked* if it carries no evidence
marker of any kind — no path, no `file:line`, no command, no receipt id, no byte count, no
sha, no date, no instrument name.

> **7,957 of 18,493 assertion lines (43.0%) carry no evidence marker. 1,360 of 1,762 receipts (77.1%) contain at least one.**

**This number is inflated** and I will not lead with it. Hand-inspection of the worst
offenders shows most hits are JavaScript source listings and vendor corpus text where a
marker would be meaningless. Two of the "worst" files are a harvested Claude system prompt
and a Bearable export — not fleet receipts at all.

**Pass B (file level, strict).** 3,009 receipts, 400 B–500 KB. A receipt is *evidenceless*
only if the **entire file** contains no command, no exit code, no fenced verbatim-output
block, no `file:line` cite, no receipt/gate id, no byte count, no sha, and no tri-state
marker. It is then split by whether it hedges.

| Bucket | Count | Rate |
|---|---:|---:|
| Instrumented (some evidence anywhere in file) | 1,966 | 65.3% |
| No instrument at all | 1,043 | 34.7% |
| — of which hedged (says "unproven"/"owed"/"not measured") | 568 | 18.9% |
| — **of which confident: states conclusions, no evidence, no hedge** | **431** | **14.3%** |

> **THE HEADLINE NUMBER: 431 of 3,009 receipts (14.3%) state confident conclusions with no
> instrument, no command, no byte count, and no tri-state marker.**

The 568 hedged ones are the fleet's conscience working. The 431 are the leak.

### 5 examples, quoted, with paths

**1. `watch/inbox/wave_20260916/receipts/N12_INVENTORY_CONSUMER.md`** — 85 unbacked / 114 asserts, 74.6%
```
PASS  1 game script compiles + window.MUD live
PASS  2 respawn point is the courtyard bonfire (dup-key bug gone)
```
*(In fairness: the file does carry a verbatim harness block and `63/63 lanes green, EXIT=0`. The verdict lines are unbacked *individually*; the file as a whole is instrumented. This is the shape of the leak — a file earns credibility once, then inherits it for every line.)*

**2. `watch/inbox/TREE_DOCTRINE_V2_DIGEST_20260925.md`** — 102 unbacked / 173 asserts, 59.0%
```
Superlative metric, fixed once so the crowns do not collide: C8 leads on recurrence breadth
(two stop texts independently fetched in seven of eleven case files...)
```
A quantitative claim ("seven of eleven") with no citation of which eleven files.

**3. `watch/inbox/FROM_MUD_TO_WOW_20260914.md`** — 41 unbacked / 76 asserts, 53.9%
```
SUPERHOT. ... Verified numerically: idle enemy drift 0 pixels, moving enemy drift 31.5,
player movement 140 — in the same window.
```
"Verified numerically" is the receipt's own word, and it names no script, no command, no file.

**4. `watch/inbox/wave_20260916/receipts/W3_SOULS_MESSAGES.md`** — 50 unbacked / 61 asserts, 82.0% (worst rate among fleet-authored receipts)
```
PASS  1 it compiles + window.FS lives
PASS  2 Adam's three: nell strongest AND slowest, allzaban fastest
```

**5. `watch/inbox/DEEPSEEK_ADVERSARIAL_ARC_20260918.md`** — 38 unbacked / 41 asserts, **92.7%**
```
Result: silent consensus collapse that the blind external judges never see, because the...
```
The highest unbacked rate in the corpus, and it is presented as an established result.

### Why the fleet's own laws don't catch this

The law is written and correct. The enforcement surface is **narrow**: `census_drift_patrol.py`
`parse_carrier` reads exactly one grammar from exactly one bullet. It cannot see a
conclusion. It cannot see a receipt. There is no gate anywhere in the estate that reads a
sentence and asks *what produced this number.* The ratchet, the census patrol, the
chain_guard, the freshness gate — all instrument-grade, all silent on narrative. **The fleet
built excellent byte-detectors and zero prose-detectors, then wrote a law about prose.**

---

## 3. NARRATIVE DRIFT OVER TIME — the number that moved without anyone noticing

**Topic: the verkle chain leaf count.** Recurs in receipts from Aug 30 to today.

| Date | Claim | Source |
|---|---|---|
| 08-30 | 18,080 knots | `watch/SALON_RIB_COMPACTION_20260831.md:12` |
| 09-01 | 6,312 knots, "0 orphans" | `watch/FLEET_AUDIT_20260901.md:41` |
| 09-05 | 7,243 / 7,268 / 7,269 knots (three values, one day) | `DAY_CAPACITY_RUNBOOK`, `OPS_RECAP_24H`, `SWARM_SNAPSHOT` |
| 09-11 | **7,377** leaves, chain FROZEN | `CHAIN_STOP_INVESTIGATION_20260911.md:44` |
| 09-14 | 8,247 leaves | `FROM_MUD_TO_WOW_20260914_WITNESSES.md:15` |
| 09-26 (am) | **9,873** leaves | `B2_82_verkle_reanchor_20260926.md` |
| 09-26 (pm) | **7,757** leaves | `B2_388_stale_tip_writer_hunt_20260926.md` |
| **now** | **7,829** rows | `wc -l memory/biography/verkle_chain.jsonl` |

### Did anyone notice it moved? Yes — twice, and both times it was an incident, not a census.

The 7,377 → 9,873 rise was **never narrated**. Receipts simply state a new number each time.
No receipt says "the chain grew by 2,496 since last week" or asks why. Each number is
presented as the current fact with no delta to any prior number.

The 9,873 → 7,757 drop **was** caught — because it was an incident, self-inflicted, and
documented with exemplary honesty:

`B2_388_stale_tip_writer_hunt_20260926.md`:
> **(2) THE INCIDENT:** this lane's first probe run was not hermetic ... so the probe
> reproduced the disease ON THE ESTATE: `memory/biography/verkle_chain.jsonl` fell from
> **9,890 rows to 2 sandbox rows** and `verkle_tip.json` was overwritten.

`B2_344_dangling_disposition_20260926.md` then measured the lasting damage:
> The chain shrank from 9,873 rows ... to 7,758 rows now: **2,115 rows removed** by a
> post-16:45Z rewrite that also stripped flags. `chain_guard` live: dangling 1,396,
> **dangling_unflagged 963**, state REGRESSION.

**The finding: the fleet detects drift only when something breaks.** A chain that grew by
2,500 leaves over three weeks produced zero commentary across ~40 receipts. A chain that lost
2,115 rows in forty minutes produced four receipts, a canary re-mark, two repair briefs
(B2-521, B2-522), and a self-declared REGRESSION state. **Attention is allocated by blast
radius, not by change.** The undramatic drift is invisible; only the catastrophe gets a
narrative.

And the explanation was never written. B2-388 says the probe "was not hermetic." B2-344 says
a "hot re-fold writer" stripped the flags. Neither receipt states which writer, when it
started, or why the 16:45Z pin held and then didn't. A backfill brief (B2-521) exists. The
2,115 lost rows are **open and unexplained** as of this writing.

---

## 4. THE DICTATED-NUMBER PATTERN — hand-written numbers presented as current

The repo's own **census denominator law (B2-216)** demands: *"Name instrument, moment, and
delta before comparing counts; never difference two counts taken at different moments."*
Tested: for each hand-written number, can I find the instrument and date that backs it?

### NUMBERS WITH BACKING INSTRUMENTS (these are fine)

| Number | Instrument | Date | Verdict |
|---|---|---|---|
| 109.4M tok/h width 10 | `B2_25` arithmetic + `B2_424` independent reproduction | 09-26 | **REPRODUCIBLE** |
| 1,700,130 ESTATE_INDEX rows | newline count on the file itself | 09-26 | **EXACT** |
| 1.18 GB duplicate pair | sha256 `7f3b2bc4…` on both files | 09-26 | **EXACT** |
| .gitignore root cause | `.gitignore:142` | 09-26 | **VERIFIABLE** |
| 2,288 collected (gopher) | `pytest --collect-only -q` | 09-26 | was exact, now 2,294 |
| 198 librarian pulls owed | `LIBRARIAN_REPORT.md` header | 09-10 | **EXACT** |
| 17 Sep-era JSONs with no writer | — | — | UNVERIFIED (plausible) |

### NUMBERS WITH **NO BACKING INSTRUMENT** — the dictated set

| # | Number | Where stated | Instrument? | Verdict |
|---|---|---|---|---|
| **D1** | **1,910 tests / 303 files** | `AGENTS.md:27` | cites B2_69, but B2_69 read **1,837/301**. The carrier cites a receipt that does not contain the number it is cited for. | **FALSE, +384** |
| **D2** | **7,392 leaves, root 0a141dcb** | `docs/ref/SPORE_CONTINUITY_SCHEMA.md:168` | **none.** No date, no instrument, no receipt. | **FALSE.** Live: 7,829 leaves, root `88a68909…`. Doc "Last Updated 2026-09-13", "Next Review 2026-09-20" — **6 days overdue, never reviewed.** |
| **D3** | "Zero 429s, zero rejections, zero quota hits" / "The most reliable free lane in the zoo" | `docs/ref/LING_API_REFERENCE.md:68` | none. Scope-limited to "Sep 7-13" but stated in a **RELIABILITY RECORD** with no re-measurement since. | **UNBACKED, 13 days stale**, and structurally unfalsifiable — no re-measure gate exists |
| **D4** | "All seats append to `state/shared_activity.jsonl`. **Every** context pack includes the last few rows so Codex, Grok x2, and DeepSeek agents see what the others are doing" | `docs/COORDINATION.md:21` | file exists (28.9 MB, live mtime) but **no writer census**. Given ATLAS's own finding that 17 feeds have no writer, "all seats" is unverified and probably false. | **UNBACKED** |
| **D5** | "Continuity Index: 100.0% (last 24h)" | `docs/ref/SPORE_CONTINUITY_SCHEMA.md:169` | **none.** No script named. Given D2 is false and the chain lost 2,115 rows, 100.0% is not credible. | **FALSE-LOOKING** |
| **D6** | "552-row burn ledger" | `ATLAS_SELF_STEAL_20260927.md:21` | none named | **MOVED** → 557 |
| **D7** | "99 receipts landed-unindexed" | `ATLAS_SELF_STEAL_20260927.md:23` | none named | **UNVERIFIED** |
| **D8** | "SEATS.md (Aug 14)" | `ATLAS_SELF_STEAL_20260927.md:29` | none | **WRONG** → git says Aug 19 |
| **D9** | "11K receipts" | `ATLAS_SELF_STEAL_20260927.md:23` | none | **AMBIGUOUS** — 3,213 `.md` under `watch/`, ~854 at inbox top level. Denominator undefined. |
| **D10** | "1,048 cards / 23 buckets", "154 files", "1,519,630 files" | `AGENTS.md` standing arc (the Sancho boot memory) | none in the current tree | **STALE** — this whole arc is dated 09-03→09-11 and is still served as "Current arc" |

**D1 is the important one.** The census carrier cites a receipt as its provenance, and that
receipt contains a *different number*. This is not a missing instrument — it is an **actively
misleading** one. It is precisely the failure the retired 1,341 headline was killed for, and
it was reintroduced by the very receipt that retired it.

---

## 5. THE PROSE THAT OVERCLAIMS

Grep across `docs/` (49 files) + `AGENTS.md`:

| Term | Hits |
|---|---:|
| never | 474 |
| all | 432 |
| every | 345 |
| must | 253 |
| cannot | 130 |
| always | 99 |
| impossible | 9 |
| guaranteed | 1 |
| cannot fail | 1 |

1,441 absolute-claim lines total. The 10 strongest, checked for truth:

| Claim | Location | TRUE? |
|---|---|---|
| "Chain Tip Verification: `verkle_tip.json` (current: **7,392 leaves, root: 0a141dcb**)" | `docs/ref/SPORE_CONTINUITY_SCHEMA.md:168` | **FALSE.** 7,829 / `88a68909`. Hardcoded, undated, unreviewed. |
| "Continuity Index: **100.0%** (last 24h)" | `docs/ref/SPORE_CONTINUITY_SCHEMA.md:169` | **NOT CREDIBLE** alongside D2, and the chain lost 2,115 rows on 09-26. |
| "All durable cross-surface work lands on the shared inbox... must **never** be the sole copy" | `AGENTS.md:12` | **VIOLATED IN THE TREE.** 1,309 untracked paths, 889+ untracked under `watch/`. 1,145 inbox `.md` tracked vs 857 on disk at top level. The receipts are the record and the record is uncommitted. |
| "`memory/briefs/latest.md` FROZEN 2026-09-26 and **must not** be consumed as live" | `AGENTS.md:51` | **CONTRADICTED 4 LINES LATER** by `AGENTS.md:55` "Prefer `memory/briefs/latest.md`". Live consumer: `mag/context_pack.py:531`. |
| "**Zero** 429s, zero rejections, zero quota hits — the most reliable free lane in the zoo" | `docs/ref/LING_API_REFERENCE.md:68` | **UNBACKED.** No instrument, no re-measure in 13 days, and the estate's own `WIDTH_LEDGER` documents 1,780 429/1302 events on a single session for a *different* lane — the class of claim doesn't survive contact with the width work. |
| "**All** seats append to `state/shared_activity.jsonl`... **every** context pack includes the last few rows" | `docs/COORDINATION.md:21` | **UNVERIFIED.** No writer census exists — which is exactly ATLAS's GAP 3. |
| "**All** durable cross-surface work..." / "**Never** commit `.env`" | `docs/BOOT_DOC.md:88,102` | **LIKELY TRUE** (not tested — `.env` is `.gitignore`d), and stated as a *prohibition*, which is the correct register. **This is what a good absolute claim looks like.** |
| "**Always** use Mag python — **never** bare `python` on PATH" | `docs/FRAMEWORK_LOAD.md:151` | **LIKELY TRUE** and load-bearing; not falsifiable by inspection, enforced by habit not gate. Correct register. |
| "**All** hashes (`input_hash`, `output_hash`) **MUST** be SHA256... canonized before hashing" | `docs/ref/ANNALEA_STANDARD.md:31` | **UNVERIFIED.** A normative spec in `docs/ref/`, not a checked invariant. No gate reads it. |
| "Falsifier Status: **All** claims testable with provided scripts" | `docs/ref/SPORE_CONTINUITY_SCHEMA.md:170` | **FALSE-LOOKING.** The adjacent D2 claim has no script and is false. |

**The finding: the overclaims cluster in exactly one place — `docs/ref/`.** That is where
speculative upstream standards (`ANNALEA_STANDARD`, `LING_API_REFERENCE`,
`MCP_MANIFEST_SPEC`, `ZAI_API_EXPERT_REFERENCE`) sit *beside* fleet-truth documents, in the
same directory, in the same voice, with no marker distinguishing "this is a vendor spec we
copied" from "this is what we measured." A reader landing on
`SPORE_CONTINUITY_SCHEMA.md` has no way to know its two hardcoded numbers are a month stale
and its review date is 6 days overdue.

The strongest claims that are **true** are all *prohibitions* ("never commit `.env`", "never
bare `python`"). The strongest claims that are **false** are all *state assertions* ("7,392
leaves", "100.0%", "all seats append"). **The fleet writes its laws in absolutes correctly and
its status reports in absolutes carelessly.** An overclaimed *law* is still a law — nobody
checks a prohibition. An overclaimed *status* is a lie that ages into a false present tense.

---

## 6. WHAT THE FLEET IS AFRAID OF — the avoidance pattern

Raw vocabulary across 3,172 receipts:

| Term | Hits | | Term | Hits |
|---|---:|---|---|---:|
| dead | 2,394 | | debt | 522 |
| unproven | 2,170 | | blocked | 417 |
| stale | 1,314 | | defer | 321 |
| **owed** | **1,161** | | skipped | 292 |
| pending | 723 | | not run | 180 |
| skip | 688 | | unread | 176 |
| unverified | 666 | | backlog | 149 |

A word tally is weak evidence — "dead" is mostly prose. What matters is **what** gets
deferred, and the answer is not what you'd expect:

| Category | Receipts | Reading |
|---|---:|---|
| **cross-lane handoff** ("owed to", "next lane", "follow-up") | **1,625** | The fleet's default disposal is *give it to someone else*. |
| **re-verification / re-run of already-claimed work** | **1,166** | **This is the real finding.** |
| operator-gated (keys/spend/GO) | 281 | Legitimate — the operator owns spend. |
| measurement/probe owed | 80 | Small. The fleet does measure. |
| playtest / field validation | 31 | Everything real waits for Sep-29. |
| code/config migration owed | 17 | Tiny. |

### TOP-3 DEFERRED

1. **Re-verification of work already reported done (1,166 receipts).** The single most-deferred
   category is not new work and not blocked work. It is *going back and checking whether the
   last thing was true.* `watch/ARCHAEOLOGY_DIG_20260909.md:72` is the cleanest statement:
   > **MAX_DISTILL epoch 1 INCONCLUSIVE (08-27) — never re-fired**

   An experiment that ran, returned nothing, and has sat unre-run for **30 days**. The
   receipts treat this as archaeology, not as debt.

2. **Cross-lane handoff (1,625 receipts).** Work is closed by *transferring* it. The
   receiving lane is rarely named and the handoff is rarely confirmed. This is how
   `MAX_DISTILL` and the 198 librarian pulls and the 10 unpromoted workflow drafts all
   accumulated: each was individually legitimate to hand off, and no one owns the sum.

3. **Self-admitted unmeasured things (94 receipts) — and this is where the fear is visible.**
   Not deferred to a person. Deferred to a *category*. The phrase recurs:
   > "liveness was **NOT verified** ... Existence verified, pulse not."
   > "silent render **assumed, not verified**"
   > "the item-level split ... is **not byte-recoverable**, stated as unknown"

   The fleet is *comfortable* saying "unverified." It is uncomfortable with **not knowing
   which lane owns the re-check**. The 1,625 handoffs and the 1,166 un-re-verified items are
   the same behavior: the fleet would rather name a gap than close a loop.

### The incentive this reveals

Every avoidance pattern in this repo routes through one mechanism: **a receipt can be filed
without the thing it describes being true**, provided the receipt is honest about being
*pending*. The confidence penalty is zero; the honesty tax is rewarded with tri-state labels
and praise. So the rational move for any seat is to file a well-labeled "owed" rather than
spend a wave closing something. The corpus rewards the appearance of rigor over its
exercise — and the 43%-line-level / 14.3%-file-level evidenceless rate is what that
incentive looks like at scale.

Two counterweights exist and both are load-bearing: **Gopher's audit** (a seat that measured
instead of narrated) and **`THIRD_WAY_FALSIFIER_REGISTRY`** (a document that marks its own
unbacked cells). The fleet can produce rigor. It just doesn't produce it by default.

---

## 7. WHAT THE FLEET KNOWS AND CANNOT SEE

The blind spots the receipts admit, in their own words:

1. **"the corpus is NOT repo-only"** (`RECORD_POOL_CENSUS_20260911.md`) — and yet every gate in
   this report, and the census patrol, and FTS, and the chain, are repo-only. The corpus
   widened; the instruments didn't.
2. **"no content-layer search ... any claim inside 11K receipts is unfindable unless you
   already know the filename"** (ATLAS §2). This report needed a purpose-built scanner to
   answer a question the fleet already has a doctrine for. The answer existed in the corpus
   and was unreachable. **The retrieval gap is why this lane's 43% figure is new information
   to the fleet.**
3. **"nothing answers which surfaces still have a living writer"** (ATLAS GAP 3). Lanes
   starved for 19.3h; 17 feeds with no writer; a 1,309-path untracked tree. No instrument
   sees any of it.
4. **"existence verified, pulse not"** — the fleet's dominant epistemics. It is very good at
   establishing that a thing was *written* and has no instrument for whether it still
   *works*. Every finding in this report is that shape: a file exists, a receipt asserts a
   state, nothing checks.

**The single sentence the fleet has not written down:** it has instruments for bytes and
none for sentences, and the gap between the two is where all of this lives.

---

## APPENDIX — reproducibility

All commands run from `local_sovereign_agent/` on 2026-09-26, read-only. No repairs.

```
./.venv/Scripts/python.exe -m pytest --collect-only -q          # 2294 tests collected
./.venv/Scripts/python.exe tools/census_drift_patrol.py --collect  # COLLECT-DRIFT +384
wc -l memory/biography/verkle_chain.jsonl                      # 7829
wc -l memory/burns/LEDGER.jsonl                                # 557
ls -la memory/briefs/latest.md                                 # -r--r--r-- 09-26 14:01
ls -la watch/LIBRARIAN_REPORT.md                               # 09-10 19:08
git status --porcelain | grep -c "^??"                         # 1309
```

Scanners: `w2l9_scan.py` (line-level), `w2l9_strict.py` (file-level), `w2l9_drift.py`
(number series), `w2l9_overclaim.py` (absolutes + deferrals). Machine-readable output:
`memory/audit_20260926/w2l9_narrative.json`.

**Limits of this audit, stated honestly.** The 43% line-level figure over-fires on code
listings; the 14.3% file-level figure is the one to quote. Pass B requires a 400 B–500 KB
file, so very small receipts are excluded. The deferral categories are regex over vocabulary
and will over-count "cross-lane handoff"; the *ordering* is robust, the exact counts are not
instrument-grade. I did not re-run the MUD harness to verify N12/W3 — those receipts carry
verbatim output and I judged them instrumented at file level while still flagging their
individual verdict lines. And I did not verify D3–D5 negatively: I can show no instrument
exists, which is not the same as showing the claim false.
