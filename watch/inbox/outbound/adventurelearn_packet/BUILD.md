# BUILD — eight pieces, each with its failure story

Build instructions for a stranger. Tokens not paths: every TOKEN below is a name you
choose on your own machine. Suggested defaults in the legend; nothing here depends on
an operating system, a language, or a vendor. All of it is standard library and $0.

**Legend (tokens):**

| Token | What it is | Suggested default |
|---|---|---|
| LEDGER | one append-only records file | `ledger.jsonl` |
| RECEIPTS | a folder of per-lane work receipts | `receipts/` |
| VERIFY | one command that re-checks the LEDGER chain | `verify` subcommand |
| CANON | your written rules + claims register | `canon.md` |
| CHALLENGES | blind challenge set + public hashes | `challenges.md` |
| VAULT | key storage outside every synced/shared surface | anywhere off the mesh |
| TIDE | the end-of-session compaction command | `tide` subcommand |

---

## (a) The append-only ledger with a hash chain

**WHY IT EXISTS.** Memory that can be edited is memory that can be negotiated with. The
chain makes the past expensive to fake and cheap to check: every row carries the hash of
the row before it and its own hash, so changing one byte anywhere breaks every hash
after it. Corrections are new rows that point at the row they correct. Nothing is
deleted; being wrong stays on the record.

**THE FAILURE IT PREVENTS.** Silent edits — and it caught a real one, in our own ledger,
the night this packet was written. A writer bypassed the admission gate and crashed
mid-row: row 122 landed with a previous-row hash matching nothing and no hash of its
own. The VERIFY command flagged it (`FAIL row 122: prev-hash mismatch (chain broken)`)
without any human noticing first. The row stays; the repair must also be append-only —
a new VOID row plus a re-anchor row — because hand-editing the tape would break the
exactly one thing the ledger exists to protect. (Our evidence:
`wave_20260916/receipts/A2_EPISTEMOLOGY_ENGINE.md` F-2; `receipts/WARM_START_20260916.md`.)

**BUILD.**
1. Choose LEDGER as a JSON-lines file. One line = one row.
2. Row shape, minimum: `prev` (hash of prior row, empty for row 1), `ts` (UTC
   timestamp), `kind`, `claim` (one sentence), `verdict`, `evidence` (file name(s) a
   person can open), `note`, `hash`.
3. Compute `hash` = SHA-256 over the row's fields (excluding `hash` itself) serialized
   with sorted keys. Two lines of any language's standard library.
4. Write an append function: refuse any row missing `hash` or whose `prev` does not
   equal the last row's `hash`. Refuse silently-edited files by never opening LEDGER
   for in-place writes — append only.
5. Write VERIFY: re-read the whole LEDGER, recompute every hash, check every `prev`
   linkage, check every named `evidence` file exists. Print PASS or the first failing
   row number. Run it on demand, not on faith.
6. Add one rule and stop: a verdict of Supported requires a witness row from a second
   seat. Unwitnessed Supported auto-demotes. (This is the truth gate; see WHY.md law 1.)

**COST.** $0. Standard library only. About an afternoon for steps 1–5.

**WHAT WOULD MAKE YOU DELETE IT.** If you never need to prove to anyone — including
future you — that a record was not edited, this is overhead; delete it and keep plain
log files. If VERIFY runs for a year and never once catches anything, downgrade the
chain to a plain append-only log and keep the hash only at the tip.

---

## (b) Receipts written before work

**WHY IT EXISTS.** The receipt is written before the lane starts: mission, budget,
laws, then a timestamped log appended as the lane works. If the lane dies, the receipt
is what it died leaving. Work that leaves no record cannot be resumed, audited, or
mourned honestly.

**THE FAILURE IT PREVENTS.** Dead lanes that take their work with them. Three
tonight-side examples, all real: a DOI-backfill lane died at 2 of 4 registrations — its
receipt kept the two landed rows, and a second lane finished the series by reading the
receipt, not by re-deciding anything (`receipts/B9_ZENODO_DOIS.md` →
`receipts/B9_ZENODO_DOIS_GEN2.md`). A games-audit lane died mid-work; its inventory
tables survived in the receipt and are the only reason the requeue knows where to
resume (`receipts/G1_GAMES_AUDIT.md`). A code-draft lane died to a server 429 leaving a
0-byte file — and the receipt plus a sidecar death-record let the retry lane skip the
investigation and go straight to the work (`wave_20260916/drafts/`,
`receipts/W1_WORLD_SKELETON.md`).

**BUILD.**
1. Make RECEIPTS. One file per lane, named `LANE_SUBJECT_DATE.md`.
2. The receipt opens with: lane name, date, mission (one sentence), budget, and the
   laws in force. This much is written before any work.
3. First log line is always `[t0] receipt written before work`.
4. Append timestamped lines as the lane works — findings, dead ends, and numbers as
   they land, not reconstructed later.
5. Status header moves IN PROGRESS → CLOSED when done. A dead lane's receipt keeps
   IN PROGRESS; that is honest. Never delete a dead lane's receipt; requeue from it.
6. One job per write: a receipt reports; it does not also re-design the system.

**COST.** $0. The real cost is discipline: roughly two minutes per lane.

**WHAT WOULD MAKE YOU DELETE IT.** If no lane has ever resumed from a dead lane's
receipt, and no audit has ever quoted one, the law is decoration — replace it with
"keep good notes" and drop the ceremony.

---

## (c) Pre-registered falsifiers with thresholds committed before data

**WHY IT EXISTS.** A test you can regrade after seeing the data is a mirror. Writing
the claim, the metric, and the kill-number down before any data exists is what makes a
result mean something — including the result that kills your favorite idea.

**THE FAILURE IT PREVENTS.** Motivated reasoning with a lab coat. The worked example
is ours, from this week. We held a claim we liked: the fleet's salon is "a thermodynamic
sampler of judgment space" — more diversity, better answers. The canon carried a
pre-registered falsifier with exact bands, written before the experiment: supported if
the rank-correlation is below −0.3, refuted if above +0.3. First probe: +0.167,
wrong-signed. We did not reinterpret; we pre-registered a decisive replicate — same
claim, 36 calls, blind-graded through a fixed shuffle seed, thresholds unchanged. It
landed at +0.327, n=36, p=0.052. Past the line. Verdict: REFUTED, by the number we
wrote when we still loved the idea. The receipt records it as a weak refutation — the
margin is 0.027 and p is marginal — because honest margins are part of the mechanism.
(`physical_computing/receipts/SALON_ESS_20260916.md`,
`physical_computing/receipts/SALON_ESS_REPLICATE_20260916.md`.)

**BUILD.**
1. Before generating any data, write five things in a receipt: the claim (one
   sentence); the metric (an exact formula); the threshold (a number and a direction);
   the grading procedure (script or fixed rubric); the blinding (e.g., a fixed shuffle
   seed applied before grading).
2. Commit the receipt. Now generate the data.
3. Grade mechanically against the registered bands. The verdict word (Supported /
   Refuted / Null) is produced by comparing two numbers, not by a discussion.
4. If the result is ambiguous (thin margin, weak power), say so in the same breath as
   the verdict. A weak refutation is still a refutation; a hidden margin is a lie.
5. File one of two artifacts afterward: a canon correction or a fossil correction.
   Silence is not an allowed outcome.

**COST.** $0. Cheapest piece here; it is a paragraph written early.

**WHAT WOULD MAKE YOU DELETE IT.** If your thresholds have never once ruled against a
claim you like, they are not thresholds — they are press releases. Delete them and stop
borrowing the credibility of real ones.

---

## (d) The Amendment Obligation

**WHY IT EXISTS.** Rules and numbers rot. Facts drift into fossils — lines that were
true once and travel on after the bytes changed. The obligation: every work cycle
amends one rule of its own, or writes down why none. It forces the system to keep
touching its own law with its own hands.

**THE FAILURE IT PREVENTS.** Fossils traveling as truth. Tonight's catches, all from
one fold pass: a memory line claimed a fanout "fired 50/50"; the run's own receipt
bytes say 39 answered, 11 failed — the 50/50 line was a fossil of an appended multi-run
tape (`WAVE_STATE_20260916.md` §3–§4; challenge C-08 in
`receipts/A1_BLIND_CHALLENGE_SET.md` makes the recount a standing graded test). A
canonical "53 handoffs" number failed an exact recount (55 occurrences across 44 of 50
answers). Three receipts carried stale IN PROGRESS headers over finished bodies. Each
got a filed correction or a queued one-line fix — and the D23 receipt that contained
the bad line got annotated, not deleted.

**BUILD.**
1. Keep CANON: your rules, each with the date it was adopted and the failure that
   produced it.
2. End every work cycle with one of exactly two writes: (i) one amendment — a rule
   changed, added, or retired, with the evidence that forced it; or (ii) one line:
   "no amendment — reason."
3. When a claim is struck, correct or quarantine every place it traveled, and keep the
   wrong version visible with a correction note. Never silently fix a fossil.
4. Corrections are new rows in LEDGER (piece a), pointing at what they correct.

**COST.** $0. One line per cycle.

**WHAT WOULD MAKE YOU DELETE IT.** If the amendment log turns into a desk — ritual
yes/no lines, no real changes for a month — retire the per-cycle obligation and keep
only the stronger rule it was guarding: a rule proven wrong by bytes is amended in the
same session, in the receipt where the proof landed.

---

## (e) The blind challenge set with sealed keys

**WHY IT EXISTS.** The author of a test grades it kindly; the author who locked the
answer key before the test began cannot. Write challenges against claims you hold,
write the expected answers, hash them, publish only the hash. Predictions are committed
before outcomes; the key is revealed after; the reveal is checked against the committed
hash.

**THE FAILURE IT PREVENTS.** A system that only its author can falsify. Our set: ten
challenges (interpreter behavior, test-census reproduction, commit stats, replay
determinism, a suspended canon claim, the fossil recount of 4d, and more), each with a
frozen threshold and a named grader. One key is already sealed: its SHA-256 is printed
in the public receipt, the key bytes live in VAULT outside every shared surface, and
the receipt states the honest threat model — same disk, so the hash is the real lock
and storage is hygiene. (All of it in `receipts/A1_BLIND_CHALLENGE_SET.md`; the
row-122 catch in 4a's story is also the outside-reader's find — see piece g.)

**BUILD.**
1. List 5–10 claims your system holds that have numbers or behaviors already on disk
   or soon computable.
2. For each: write the claim, the frozen threshold (inside/outside bands), the grader
   (a script where possible; otherwise a fixed rubric applied by a seat that is neither
   author nor predictor), and a deadline.
3. Write the answer key where outcomes are pending. Compute SHA-256 of the key file.
   Print the digest in the public document; store the bytes in VAULT, outside every
   synced or shared surface.
4. Prediction window: predictors append signed, timestamped rows to an append-only
   log before any measurement. A prediction row after the measurement row is void —
   the ordering is byte-checkable.
5. Grade. Reveal keys only after the window closes; re-hash revealed bytes first; a
   mismatch voids the key, not the predictors.
6. Every miss produces a canon or fossil correction (pieces c and d). Silence is not
   an allowed outcome.

**COST.** $0. Standard library hashing. The expensive part is attention, once.

**WHAT WOULD MAKE YOU DELETE IT.** If every claim you care about is already graded by
scripts with exit codes, the sealing layer is chrome — keep the before/after ordering
rule, drop the rest.

---

## (f) The pacing guard for metered keys

**WHY IT EXISTS.** Free tiers are free of cash, not of limits — daily quotas, drains,
per-minute walls. A fanout that assumes the lanes it probed at dusk are the lanes it
has at midnight will lose seeds mid-run. The guard: probe before fanout, cap per lane,
and when a wall hits, mark that lane do-not-retry and keep going with the rest.

**THE FAILURE IT PREVENTS.** The balance wall, hit live tonight: a lane (zai-air)
answered its calls in the dusk baseline probe; hours later, mid-fanout, it returned
HTTP 429, code 1113, "Insufficient balance or no resource package. Please recharge" —
the balance drained under us while the run was in flight. A second lane sat behind a
daily rate limit (code 1300). Neither burned retries: the guard marked both
ABORTED_PAID_WALL / do-not-retry, and the run continued on surviving lanes to
completion at $0 cash. The probe results became a rotation table for the next run —
which lanes to call, which to never call, and why, per lane. (Evidence:
`receipts/D23_SALON50_NIGHT_RESULTS.md`; `receipts/D22_PROVIDER_PROBE_20260916.md`;
`receipts/A4_ASTRA_SMOKE_12.md` failure autopsy.)

**BUILD.**
1. Before any fanout: one probe call per lane. Record status, latency, error code.
2. Keep a rotation table: lane, model, status (alive / rate-limited / paid-wall /
   fragile), the exact error string, and the verdict (use / never call). Update it
   after every run.
3. Per-lane cap: a maximum call count per lane per run, set before the run.
4. Error classes, decided in advance: quota/balance errors → mark the lane
   do-not-retry for this run and continue; truncation → retry once with a bigger
   budget; auth errors → mark dead and continue. Never let one lane's wall crash the
   fanout.
5. The fanout writes raw answers to a tape file as they land, so a mid-run death
   leaves partial ore (piece b).

**COST.** $0. One extra probe call per lane.

**WHAT WOULD MAKE YOU DELETE IT.** If your compute is all local and unmetered, walls
like these cannot happen to you; delete the guard and keep only the probe, which is
just good manners before a fanout.

---

## (g) The outside-reader seat

**WHY IT EXISTS.** A reviewer who reads your summary of your work shares your blind
spots, because it shares your summary. The outside reader is a seat — another model, or
a person — that did not write the work, is handed the raw receipts (bytes and hashes),
works from a fixed output contract, and returns a verdict: keep, kill, or amend. It is
a load-bearing seat, not a courtesy.

**THE FAILURE IT PREVENTS.** Two, in one night. First: it catches what internal review
misses. Our witness seat, reading the night's receipts cold, found that our own texts
disagreed about whether a kill threshold had been crossed (the +0.327 of piece 3c
sits 0.027 past the line; our prose variously said "refuted" and "survived") — and
demanded the threshold's provenance be filed before the word "refuted" travels
anywhere. It also split two things we had conflated: a crashed writer that corrupted a
row (piece 4a) is not a forger fabricating one. Second failure prevented: the reader
being fed prose instead of bytes. We caught that in ourselves the same night and
amended the contract: this seat gets receipt files and hashes, never our digest of
them; contracted output format; one call; no continuation dependence. Verdict after
the amended run: KEEP. (`receipts/U5_UNION_WAVE_WITNESS.md`; the challenge-set pairing
is in `receipts/A1_BLIND_CHALLENGE_SET.md` Lock 2: author ≠ predictor ≠ grader.)

**BUILD.**
1. Choose a reader that did not write the work: a different model, a different
   operator, or a human colleague.
2. Hand over bytes: the receipt files (or their hashes plus the files), never a
   summary written by the author.
3. Fix the output contract before the read: verdict (keep / kill / amend), up to N
   concrete catches, and "what would change your mind." Nothing else.
4. One call, no follow-ups. A reader that can be argued with is a co-author.
5. File the verdict as a row in LEDGER. Accepted catches become amendments (piece d)
   with the verdict cited as evidence.

**COST.** $0 on free tiers; a favor on humans.

**WHAT WOULD MAKE YOU DELETE IT.** If the reader only ever sees your prose, delete the
seat — it is a mirror with extra steps, and mirrors flatter.

---

## (h) The tide: end-of-session compaction into a warm card

**WHY IT EXISTS.** A night of parallel lanes produces scattershot: dozens of receipts,
raw tapes, dead ends. The next session does not read all of it; it reads one card. The
tide is the closing command that compacts the day into that card: counts, corrections,
the requeue list, and the single command that makes the next window fully warm.

**THE FAILURE IT PREVENTS.** Cold starts and re-mined ground. Tonight's tide produced
a master index of 60 receipts with one status line each, a paste-ready memory block,
and a gen-2 requeue table naming every stub and orphan with the exact next ask —
including the fossil fixes from piece 4d, so the corrections actually travel to the
next session instead of dying in a fold nobody reads. The warm-start lane also ran the
compaction command itself, measured the card (~1.4k tokens), and listed the seven
things the card did NOT yet hold — a gap list, because a warm card with silent holes
is a fake board. (`receipts/WARM_START_20260916.md`; `WAVE_STATE_20260916.md`.)

**BUILD.**
1. The card is one file with four sections: counts (receipts, passes, fails); 
   corrections (every fossil fixed today, in one block); requeue (every stub, with the
   one next command for each); pointers (master index, key receipts by name).
2. The tide command regenerates the card from the receipts themselves — counts read
   from files, never typed by hand. Trust bytes, not reports.
3. The card names the single command the next window runs first.
4. Run it at session close, every session. The habit is the machine.

**COST.** $0. One command and two minutes of discipline.

**WHAT WOULD MAKE YOU DELETE IT.** Check after a week: if the next window has not once
started from the card, it is shelf-ware. Delete it and let the ledger's VERIFY output
be the morning card.
