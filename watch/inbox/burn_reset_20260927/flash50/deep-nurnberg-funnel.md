# deep-nurnberg-funnel: the estate's knowledge funnel as a measured rate-distortion chain

The ask: the estate processes information through raw logs, receipts, findings, laws, ribs, and the
context pack; each stage compresses and abstracts; design the FUNNEL OPTIMIZATION: optimal
compression per stage, total information loss, what a perfect funnel preserves.

The name is the right joke inverted. The Nurnberger Trichter (the "Nuremberg funnel") is the
17th-century German teaching manual and the satirical print that goes with it: a scholar pours
learning through a funnel into the student's skull, knowledge transfer as plumbing. The estate
builds the opposite machine. Nothing is poured down; everything is distilled up, from labor. The
funnel's wide mouth is the raw log spew of a fleet that runs all day, and its narrow stem is a
1,196-character janitor pack. This item measures that stem, stages by stage, with the estate's own
instruments, and designs what the optimal funnel would preserve.

## 0. Instruments run this ask (receipts)

Every number below is from bytes read or commands run this session, 2026-09-28:

1. Size census (PowerShell Measure-Object over the trees): `logs/` = 1,808.8 MB across 5,533
   files; `watch/inbox/` = 6,055.9 MB across 12,148 files; `memory/rib/` = 156 KB across 45 ribs;
   AGENTS.md = 16,671 B; memory/MEMORY.md = 108,449 B (485 lines); watch/inbox/INDEX.json =
   466,153 B.
2. Same census via `.venv/Scripts/python.exe` for the rest: memory/biography/verkle_chain.jsonl =
   5,783,771 B, 8,249 knots; memory/warm_state.json = 908 B; memory/percolator/invariants.json =
   109,231 B; watch/inbox/PACK_OFFLOAD.jsonl = 691 rows before my builds, 695 after; pile files
   (state_summaries 144 rows / 81,772 B, classified 154 / 124,691 B, training_rows 270 / 97,287 B);
   configs/violation_baseline.json = 377,045 B; burn_reset_20260927 subtree = 210 files, 7.2 MB.
3. Live pack builds: `.venv/Scripts/python.exe -c` importing `mag.context_pack`, calling
   `build_context_pack(mode='full', fast=True)` + `format_context_pack_text`. Rendered full pack =
   4,496 chars (budget 4,500); janitor pack = 1,196 chars (budget 1,200). Doctrine excerpt built =
   4,235 chars.
4. Fossil arm: `.venv/Scripts/python.exe tools/thought_quantizer.py --check` printed
   "THOUGHT-QUANTIZER: fresh, 4.0h old (v0.3)", exit 0.
5. Live ladder trace: rebuilding the full pack appended 4 rows to PACK_OFFLOAD.jsonl
   (2026-09-28T20:22:43, stages 1, 2, 3, 4: "L4 Heat (live_tail, attention)", "L3 Task
   (compacted)", "L0d/L0f context blocks", "hard clip"). Post-build assertions on the rendered
   text: "RIB Doctrine" absent, "Current objective" present, "Compiled laws" present, "Zeitgeist"
   absent, "Solved history" absent.
6. Quantizer internals: read tools/thought_quantizer.py in full; compile_report.json stats read
   from disk: in=331, kept=307, refused_telemetry=2, refused_fragments=9, dedupes=13,
   error_quoting_laws_kept=37; packs written 24 frontier / 12 flash / 12 local.
7. Sibling coverage check: deep-quantizer-theory.md (17,721 B) already measures stage 4 (the
   quantizer) as a compression system, with its own instrument _quant_measure.py; this item cites
   it for that stage and does not re-derive it. _entropy_budget_census.py counted the estate's
   order-structures for the entropy-budget item. Neither sibling covers stages 1-3, 5-6 or the
   terminal render, which is this item's ground.

## 1. The funnel is real and it is bytes: the stage map

The ask names six stages. The estate actually implements each one as running code with a byte
budget. Measured mass at each stage (this session):

| Stage | Artifact | Measured size | Writer code |
|---|---|---|---|
| S0 raw logs | logs/ (kpi.jsonl 1,055.5 MB, dashboard_sv.err.log 179.8 MB, backend_sv.log 82.7 MB) | 1,808.8 MB / 5,533 files | every service |
| S0' session/memory raw | verkle_chain.jsonl | 5.78 MB / 8,249 knots (~701 B/knot) | mag verkle knot writer |
| S1 receipts | watch/inbox/ + INDEX.json (1,415 rows of {class, path, purpose, sha256}) | 6,055.9 MB / 12,148 files; index 466 KB | mag.shared_surface / receipts |
| S2 findings | memory/pile/ (144+154+270 rows) and percolator invariants.json (352 leaves) | ~304 KB pile; 109 KB invariants | mag/state_snapshot.py:36-41, percolator |
| S3 laws | quantized_thought packs: frontier 8,193 B / 24 rows, flash 4,914 B / 12 rows, local 4,714 B / 12 rows; violation_baseline.json 377 KB accepted debt | ~26 KB packs | tools/thought_quantizer.py:121-197 |
| S4 ribs | memory/rib/ (RIB_DRIVING_LADDER_20260928.md 1,774 B, RIB_SELF_MY_LAW.md 581 B) | 156 KB / 45 ribs | operator + seats, file-backed |
| S5 context pack | rendered pack text | 4,496 chars full / 1,196 chars janitor | mag/context_pack.py:993-1279 |

Plus the boot artifact below all of it: warm_state.json, 908 B, written by
mag/hermes_warm_boot.py:39-59 from the chain tip (16-char root prefixes, leaf count, tag). The
chain-to-warm ratio alone is about 6,400:1.

The estate's constitution for this funnel is already written down: "Trust bytes, not reports"
(AGENTS.md, given material). That single sentence is the design constraint the rest of this item
elaborates: every stage is a report, so every stage must terminate in pointers back to bytes.

## 2. Measured compression ratios, stage by stage

Adjacent-stage ratios from the table above:

- S0 to S0': full service spew to verkle knots: about 300:1 on today's tree (1.81 GB logs vs 5.78 MB
  chain; the chain only carries session-scale knots, not telemetry, so this ratio is really
  "what was worth remembering," which is the point).
- S1 body to S1 index: 6,055.9 MB of receipts to a 466 KB index holding 1,415 entries, about
  13,000:1, at ~329 B per entry. The entry shape {class, path, purpose, sha256} is a bounded
  pointer: the body is never inlined, the hash makes drift detectable. Index coverage measured at
  1,415 of 12,148 files (11.6 percent), so the index is selective by whatever wrote it, not total.
- S2 source to S2 findings: the percolator dedupes raw repeated phrases into 352 leaves carrying
  49,095 chars of distinct text (from invariants.json measured this session). The count field is
  where the funnel's deepest danger lives, see section 6e.
- S3 source to S3 laws: 49,095 source chars survive classify+dedupe into 307 weighted laws, then
  the top-cut takes 24+12+12 = 48 rows (thought_quantizer.py:162,169, sizes at 228-229): an 84
  percent top-cut between "kept" and "packed." Text ratios: 49,095 to 2,200 frontier chars (22:1),
  to 789 flash chars (62:1), to 12 local laws of 10 words each (LOCAL_MAX_WORDS=10,
  thought_quantizer.py:54,116-118).
- S4 ribs to boot doctrine: 45 ribs, 156 KB, squeezed to a 4,235-char title+goal excerpt by
  `_rib_doctrine` (mag/context_pack.py:305-340), about 38:1, roughly 94 chars per rib.
- S5 everything to pack: MODE_CONFIG budgets (mag/context_pack.py:52-146): janitor 1,200 chars
  (brief 400, bonds 500, live 0), route 1,800, build 5,500, audit 7,500, plan 11,000, full 4,500;
  MAG_FULL_CONTEXT escape hatch clamps to 8k..200k with a 48,000 default
  (mag/context_pack.py:283-294). Full estate surfaces (1.81 GB logs + 6.06 GB receipts) to a
  4,496-char pack: 1.75 million : 1. To the janitor pack: about 6.9 million : 1.

Those are the volume ratios. They are the least interesting number in this item, because the
estate's actual losses are not proportional to volume. Section 6 decomposes.

## 3. The terminal stage today: what my own pack builds proved

The single most consequential finding of this item was produced by running the funnel and
inspecting its output, not by reading code:

1. Every sampled full-mode pack overflows. PACK_OFFLOAD.jsonl held 691 rows from 173 overflow
   events; stages 1, 2, 3 fired 173 times each and stage 4 (hard clip) fired 172 times. When a
   full-mode pack overflows at all, it overflows all the way to the hard clip: the clip ladder is
   a cliff, not a ramp. My own two builds reproduced this exactly (4 new rows, all four stages).
   Mode distribution of shed events: 604 of 691 rows are mode=full.
2. The shed at stage 3 removes the entire understanding layer. The rendered 4,496-char full pack
   contains the standing objective and the 12 compiled flash laws, and contains NO RIB doctrine,
   NO zeitgeist, NO solved history. Verified by substring assertion on the rendered text this
   session. So on the current tree, stage 5's effective deliverable for stage 4 is zero chars:
   the 45 ribs / 156 KB / 38:1 squeeze produces an excerpt that the ladder then discards 100
   percent of the time in full mode. The funnel's last hop is currently total loss for the
   understanding layer.
3. Why: the protected L0 tier alone nearly fills the budget. The code's own receipt comment says
   it (mag/context_pack.py:1084-1090 and 1261-1268): the quantizer landing 3eb6dc251 added ~1 KB
   of compiled laws after a 2.2 KB objective, and in build mode the L0 tier alone exceeded the
   whole 8,000-char budget, so L0d/L0f context blocks were made sheddable at stage 3. Correct
   priority (worker contract outlives context), but with a 4,500 full-mode budget and roughly
   3.5 KB of protected content, only ~0.7 KB of context survives, which is less than nothing:
   the ladder reaches stage 4 and clips bytes anyway.
4. A cap that never binds. `_rib_doctrine`'s budget guard is
   `if len(entry) > total + max_chars: break` (mag/context_pack.py:336-337). It compares one
   entry's length against the running total plus budget, so it can only fire if a single ~270-char
   entry exceeds the whole 2,800 budget. It never fires. Measured doctrine: 4,235 chars, 1.5x its
   stated cap. Double failure: the soft cap never binds upstream, and the hard shed erases the
   product downstream.
5. Two different staleness bars at the same stage. The compiler's fossil arm demands recompile at
   24 h (tools/thought_quantizer.py:200,212; measured "fresh, 4.0h old"); the render-side gate in
   `_quantized_laws` tolerates 7 days before hiding the law behind a debt pointer
   (mag/context_pack.py:376-378). A pack can pass the boot gate for six days while failing the
   compiler's own bar. Not fatal, but it is an inconsistency between two truth-maintenance
   systems guarding the same bytes.

The janitor tier deserves its own sentence: the last offload rows before mine (20:15:33 today)
show a janitor pack climbing all four stages of a 1,200-char budget. The funnel's narrowest
consumer is chronically clipped, and janitor packs carry no doctrine by design (context tier is
render-gated to plan/full/build/audit, mag/context_pack.py:1092), so the clipping costs them
brief and bonds mass, i.e. task inputs, not context.

## 4. Theory: what "optimal compression" means for an estate

Four results from the literature carry the design, none of them invented here:

- Rate-distortion (Shannon 1948). For a source X and a distortion measure D, R(D) is the minimum
  rate at which X can be described while honoring D. The theorem's practical content: there is no
  "optimal compression" in the abstract, only optimal compression FOR a distortion you are willing
  to eat. The estate's version of D is never storage cost (disks are full anyway, 6 GB of
  receipts proves storage is free); it is re-derivation cost: the tokens, minutes, and wrong turns
  a downstream seat burns when a stage dropped detail it later needed.
- The data processing inequality (Cover and Thomas 1991). If the funnel is a Markov chain
  raw -> receipt -> finding -> law -> rib -> pack, then no stage can add information about the
  underlying event. Abstraction gains generality only by discarding instance information. The
  funnel's abstraction is therefore never "free"; the design question is exactly which instances
  deserve downstream fidelity.
- The information bottleneck (Tishby, Pereira, Bialek 1999). The principled answer to the DPI
  question: compress X into Z minimizing I(X;Z) while maximizing I(Z;Y) for a relevance variable
  Y. For this estate, Y is concrete and measurable: the set of correct actions the NEXT seat must
  take (commit the fix, run the named test, respect the law, cite the receipt). A stage is good
  exactly when its output is a sufficient statistic for Y, not for "what happened." Fisher's
  sufficiency (1922) is the zero-compression-loss limit of the same idea.
- Log-structured storage (O'Neil et al. 1996 LSM-tree; Rosenblum and Ousterhout 1992 LFS). The
  estate IS an LSM tree for organizational memory: logs are the WAL/memtable, receipts are L0,
  findings are compacted runs, laws are the highest compacted level, and the context pack is the
  read path with a bloom-filter-like admission (INDEX hashes; pack budgets). Storage theory's
  tradeoff maps exactly: write amplification is the distillation labor the fleet spends; read
  amplification is the tokens a seat must load. The funnel is well-designed when both are paid
  deliberately, and diseased when one is paid invisibly. The 173-event clip cliff is invisible
  read amplification: every full-mode seat pays the same re-derivation tax and no ledger records
  it (the offload rows record the shedding, not the downstream cost of what was shed).

One more anchor: Simon (1971) on the attention economy ("a wealth of information creates a poverty
of attention"), and Pirolli and Card's information foraging (1999): for a seat, the pack is a
patch and the receipt pointers are scent. Optimal funnel design maximizes scent per token, which
is precisely what the {class, path, purpose, sha256} index row shape and the path:line citation
law do. MDL (Rissanen 1978) and Kolmogorov complexity (1965) set the philosophical floor: provable
minimality is uncomputable, so the estate is right not to chase it, and right instead to measure
distortion empirically on real reads (the census-drift patrol and fossil arm are exactly
empirical distortion meters).

## 5. The design: optimal compression at each stage

Rate-distortion says: set each stage's distortion from the downstream decision curve. Concretely,
per stage, with the estate's own numbers as the baseline:

**S0 raw logs (keep at 1:1, compress at read time).** The measured practice is already right:
append-only logs (1.81 GB), bounded-tail reads (the FW-45 bounded tail door, from this branch's
commit record), tail in the pack's L4 heat only. Distortion here must stay zero because this is
the layer "trust bytes" defers to. Any lossy compression at S0 converts every later dispute into
he-said-she-said. Verdict: optimal as-is; the only defect is that kpi.jsonl at 1,055 MB is
telemetry nobody reads, which is a retention policy question, not a funnel question.

**S1 receipts (body 1:1, index at ~13,000:1, extend coverage).** The sha256 pointer row is the
funnel's crown jewel: 329 bytes buys byte-exact recoverability forever. Two debts: measured
coverage is 1,415 of 12,148 files (11.6 percent), so 88 percent of the receipt mass is outside
the recall layer; and the receipt prose itself duplicates evidence, which is fine (disks are
free) as long as every claim in prose carries its pointer (the receipt law already demands this;
AGENTS.md clippy bullets carry "Receipt:" paths as given material shows). Optimal: gate coverage
per class the way the ratchet gates debt by name, rather than leaving it best-effort.

**S2 findings (dedupe hard, counts as provenance, never weight).** The percolator's measured
state: 352 leaves, 49,095 distinct chars, and a count distribution whose top row holds 232,214 of
290,461 total echo counts (80 percent of all repetition mass in ONE row, measured this session).
The funnel's S2 is extremely good at dedup and therefore at manufacture of false consensus: a
phrase repeated by a stuck loop looks like 232,214 confirmations. The v0.3 law already wrote the
fix into code: weight = recency x shape, raw counts are "provenance only"
(tools/thought_quantizer.py:18-19,151-152, and the compile_report's "inflated echo - provenance
only" verdict string). Optimal S2 adds one thing the code lacks: a count-ceiling censure. When
count exceeds some N, the row should DEMOTE (recency decay should not be the only thing keeping
an echo from outranking a once-learned truth), because recency and echo are orthogonal axes.
Falsifiable proposal: cap effective count contribution at the 95th percentile of the leaf
distribution rather than at infinity.

**S3 laws (22:1 frontier, 62:1 flash, top-cut by weight, keep the two-pass gate).** The measured
compile: 331 in, 307 kept, only 11 refused (2 telemetry, 9 fragments), 13 dedupes, 37
error-quoting laws saved by the v0.3 heal. The 220-char flash bar (FLASH_MAX_CHARS,
thought_quantizer.py:53) plus first-sentence truncation (to_flash, 110-113) is the stage the
sibling deep-quantizer-theory measured precisely; cite it for the exact prefix-property
distortion. This item's addition: the gate is permissive (96.7 percent kept), so S3 pushes most
sifting DOWN to S5's budget, where the cost is highest (whole sections shed). Optimal S3 would
spend more discrimination while text is cheap: a third pass scoring law-vs-advice (not everything
imperative is load-bearing), and a freshness-aware top-cut so that a 4-hour-old compile with 352
leaves and a 307-kept census does not present 48 rows as "the law" when 259 weighted survivors
never render anywhere.

**S4 ribs (38:1 excerpt, but the cap is broken).** Ribs are the estate's manual bottleneck
solutions: human-curated, 0.5 to 3 KB, each carrying goal lines extractable by the boot excerpt
(mag/context_pack.py:327-335). Optimal S4 is small engineering, not redesign: fix the guard at
context_pack.py:336-337 to `if total + len(entry) > max_chars: break` so the 2,800 budget binds,
and count ribs rendered, not ribs existing. The deep failure is not here, it is downstream.

**S5 pack (the budget is miscalibrated against the protected tier; the ladder needs a fourth
property).** The ladder's ordering is correct by receipt: contract (frozen BUILD) outlives
directives outlives context outlives heat (mag/context_pack.py:1238-1278 and the 3eb6dc251
comment). What is wrong is arithmetic: 604 of 691 shed events are mode=full against a 4,500
budget that its own protected content fills to ~78 percent. Optimal S5 has three rules:
  1. Budget law: the protected tier (policy + policy_mid) must fit inside ~60 percent of
     max_chars, else the budget is a fiction. Today it is a fiction for full mode and for
     janitor (whose 1,200 budget climbed all four ladder stages today at 20:15:33).
  2. Shed-with-pointer: `_emit_pack_offload` (mag/context_pack.py:34-49) names the shed sections
     but discards the shed bytes; nothing persists the pre-shed text. A shed dump file per event
     (even one JSONL blob) converts stage-3 loss from irrecoverable to amortized.
  3. Feedback ratchet: a daily census of PACK_OFFLOAD stage distribution, alarm at >30 percent of
     builds reaching stage 3+, mirroring violation_ratchet's accept-debt-by-name discipline.
     Measured baseline for that ratchet: today, 99.4 percent of events reach stage 4.

And the escape hatch stays: MAG_FULL_CONTEXT at up to 200k chars with the 72/28 head-tail split
(mag/context_pack.py:297-302) is the funnel's legal un-compression path. A perfect funnel keeps
one.

## 6. Total information loss: the decomposition

The naive number: 7.86 GB of S0+S1 surfaces compress to a 4.5 KB full pack, a ratio of 1.75
million to 1 (6.9 million to 1 for janitor). That number is nearly meaningless, because most of
the 7.86 GB is recoverable by pointer. The honest ledger has five classes:

**(a) Amortized loss (bounded by pointers).** Any claim that survives with a path, a line, or a
sha256 is re-expandable at the cost of a read. The INDEX rows, verkle knots, receipt citations,
and AGENTS.md receipts make this the dominant class. Loss here is retrieval latency, not
information. The funnel is, on this class, close to the "perfect" bound already: the data
processing inequality is satisfied in its benign direction because the pointer is part of the
message.

**(b) Shed-but-logged loss.** Sections the ladder drops get an offload row naming them, but the
bytes are gone and unindexed. Measured: 173 events, stages 1 through 4, 172 ending in hard clip;
the dropped content (L4 heat, L0d doctrine, zeitgeist, solved history, task mass) is identified
but not stored. This class is the funnel's repairable waste: one schema field (store the shed
text) converts it to class (a).

**(c) Never-captured loss.** Stdout that scrolled, seat state that never reached a knot, session
context that died with a process. Unmeasurable by construction; the pile habit
(mag/state_snapshot.py capture at escalation/session close, kinds at :41) and the verkle chain
are the countermeasures. The honest statement: this class is bounded only by instrumenting
capture at moments of high value, which the estate already does at close and escalate.

**(d) Dead-stage loss (the fossil class).** The quantizer's own history is the receipt
(tools/thought_quantizer.py:4-10): the v0.2 packs compiled once on 09-18, never re-run, zero live
consumers, while the invariant stream grew from 132 to 300+ rows. For nine days an entire funnel
stage produced output that nothing consumed: 100 percent loss, invisible without an audit arm.
The v0.3 fossil check now exists (ran this session, exit 0), and the census-drift patrol watches
the AGENTS.md carrier the same way. This is the estate's historically dominant loss mode, and it
is not compression at all: it is production without consumption. A funnel stage that nothing
reads is a shredder with extra steps.

**(e) Echo loss (the inverse failure).** 290,461 accumulated counts collapse into 352 leaves; the
top leaf alone carries 232,214. Compression that dedupes repetition also dedupes the EVIDENCE
that repetition was mechanical. The funnel can make a stuck loop look like a chorus. The v0.3
provenance-only rule (weight = recency x shape, counts never weight) is the standing mitigation;
section 5's count-ceiling censure is the proposed completion.

So the answer to "what is the total information loss": by bytes, about 1.75e6:1 for a full seat
and 6.9e6:1 for a janitor; by decision-relevant information, the estate's measured losses
concentrate in (b) and (d): 172 hard-clipped packs on the record, and one stage (S4 doctrine)
rendering zero bytes to full-mode seats 100 percent of the time on the current tree, both of
which this session measured directly.

## 7. What a perfect funnel preserves: eight invariants

A perfect funnel does not preserve bytes (storage made that cheap and pointless); it preserves
recoverability and accountability of every transformation. Eight invariants, each already
half-built somewhere in the estate:

1. **Addressability.** Every artifact at every stage carries a byte-exact pointer (sha256, path,
   path:line). INDEX rows and verkle leaves do this; the receipt law mandates it. The pack's own
   sections should cite their source stage the way laws cite receipts.
2. **Shed auditability.** Every compression event writes what it dropped and why. PACK_OFFLOAD is
   the general pattern; extend it to persist the shed bytes (class b becomes class a).
3. **Resurrection.** One legal expansion path per seat tier (full-context hatch with head-tail,
   FTS corpus_search, git history). The funnel must be an index, not a shredder; if there is no
   path from a law back to its receipt, it is not a law, it is a rumor.
4. **Falsifiability.** Laws carry falsifiers and receipts (the FW-15 amendment row pattern, salon
   pre-registration, both in this branch's commit record). A law is a compressed experiment that
   a future seat can re-run from its pointer.
5. **Decay model.** Compression without expiry becomes sediment. The 7-day staleness gates, the
   census-carrier tripwire (B2-215, AGENTS.md given material), the fossil arm, and the FROZEN
   brief quarantine (memory/briefs/latest.md frozen 2026-09-26, AGENTS.md) are four instances of
   one invariant: every summary must know when it stops being true. Close the 24h-vs-7d bar gap
   at S3.
6. **Provenance-weight separation.** Counts are echo; weight is recency x shape. The 232,214
   count must never outrank a once-verified law. (Section 5's censure proposal.)
7. **Budget feedback.** Every budget that sheds must publish its shed rate and accept debt by
   name. The ratchet principle applied to the clip ladder: today's 99.4 percent hard-clip rate
   would already be a screaming red row.
8. **Loss ordered by decision criticality, not by layer.** The ladder's own law after 3eb6dc251:
   worker contract outlives directives outlives context outlives heat. Keep it, and add the
   corollary the doctrine shed violates: the system's UNDERSTANDING layer (ribs) is
   decision-critical for novelty, so either it fits the protected tier at some mode, or the
   protected tier is mis-sized for that mode.

## 8. Owed, falsifiable fixes (smallest first)

- F1: fix `_rib_doctrine` guard to `if total + len(entry) > max_chars: break`
  (mag/context_pack.py:336-337). Falsifier: doctrine excerpt <= 2,800 chars on this tree.
- F2: budget law for mode=full: protected tier <= 60 percent of 4,500, or raise the full-mode
  budget to fit objective + laws + a bounded doctrine. Falsifier: 30-day PACK_OFFLOAD census with
  stage-3 rate < 30 percent.
- F3: shed dump: `_emit_pack_offload` gains an optional path to the pre-shed text (one JSONL per
  event or a bounded ring). Falsifier: a shed event exists whose bytes can be recovered from disk.
- F4: offload ratchet script (daily census, alarm >30 percent stage-3+). Falsifier: the census
  printed from PACK_OFFLOAD.jsonl matches the day's builds.
- F5: S3 third pass (law-vs-advice) + count-ceiling censure at S2. Falsifier: compile_report
  grows a kept-but-unpacked count that trends to zero; the 232,214-count leaf carries a demotion
  verdict.
- F6: unify the S3 staleness bars (24h compiler arm vs 7d render gate) or document why they
  differ. Falsifier: no pack can render law bytes that the compiler arm calls stale.

None of these are spec'd or landed here; this item is analysis only, and each fix would need its
own spec-first landing per build discipline.

## 9. Sources

Code read this session: mag/context_pack.py (full); tools/thought_quantizer.py (full);
mag/hermes_warm_boot.py (1-100); mag/state_snapshot.py (1-80). Data measured this session: logs/,
watch/inbox/ (incl. INDEX.json, PACK_OFFLOAD.jsonl, SHARED_SURFACE_CONTRACT.json 3,791 B),
memory/rib/, memory/pile/, memory/percolator/invariants.json, memory/corpus/quantized_thought/
(all four files), memory/biography/verkle_chain.jsonl + verkle_tip.json, memory/warm_state.json,
AGENTS.md, memory/MEMORY.md, state/CURRENT.md, memory/bonds_active.md,
configs/violation_baseline.json. Commands run: the size censuses in section 0, two live
build_context_pack + format_context_pack_text rounds with post-render substring assertions, and
`.venv/Scripts/python.exe tools/thought_quantizer.py --check` (exit 0, fresh 4.0h). Sibling
instruments cited, not re-derived: flash50/deep-quantizer-theory.md (17,721 B, headings read),
flash50/_quant_measure.py, flash50/_entropy_budget_census.py. Given material: AGENTS.md (census
law, ratchet law, driving ladder, brief freeze), this branch's commit log (FW-45 bounded tail,
3eb6dc251 quantizer landing, FW-15 falsifier pattern). Literature: Shannon (1948); Cover and
Thomas, Elements of Information Theory (1991); Tishby, Pereira, Bialek, The Information Bottleneck
Method (1999); Fisher (1922); O'Neil et al., The Log-Structured Merge-Tree (1996); Rosenblum and
Ousterhout (1992); Bloom (1970); Rissanen (1978); Kolmogorov (1965); Miller (1956); Cowan (2001);
Pirolli and Card (1999); Simon (1971). The Nurnberger Trichter: 17th-century German rhetoric
manual and the satirical funnel-to-skull print, the machine this estate refuses to be.
