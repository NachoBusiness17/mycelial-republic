# DEEP ITEM: A TEMPORAL TYPE SYSTEM for the Mag estate (deep-temporal-types)

2026-09-28, flash50 dig. The ask names four temporal types ('fresh' <24h,
'stale' >7d, 'fossil' >30d, 'grandfathered' pre-law) and asks for a type
system with automatic demotion, earned promotion, and a consumption-time
type-checker. The finding of this dig: the estate already HAS all four
types, implemented four times over, on three different time bases, with
three different grandfather mechanisms, and with both halves of the
consumption-time checker already built in two files that do not know about
each other. The design below is mostly an act of NAMING and UNIFYING
byte-verified prior art, not invention.

## 0. Receipts (commands run this session)

```
$ ./.venv/Scripts/python.exe tools/fossil_check.py check
FOSSIL-CHECK: ok    memory/corpus/quantized_thought/compile_report.json 4h old (bar 168h) [recompile]
FOSSIL-CHECK: ok    memory/audit/aud_files.json tombstoned, 571h old (death recorded)
FOSSIL-CHECK: ok    memory/audit/gene_pool_gen2.json tombstoned, 570h old (death recorded)
FOSSIL-CHECK: ok    queue/lanes/jev/trail.jsonl 220h old (bar 720h) [watch]
FOSSIL-CHECK: ok    memory/corpus/quantized_thought/adversarial_arc_invariants.jsonl fixed-oracle, 244h (no bar by design)
FOSSIL-CHECK: ok    memory/improve/SEATS.md 42h old (bar 168h) [recompile]
FOSSIL-CHECK: 0 WARN, 0 HARD, 0 recompiled, 6 registered     [exit 0]

$ ./.venv/Scripts/python.exe tools/freshness_check.py
FRESHNESS: repo heartbeat 0.0d since last commit (alive=yes; bar: stale=7d, heartbeat=2d)
  BOOT_4_7.md: 2.7d old  [frozen-ok]
  state/CURRENT.md: 1.3d old [untracked-mtime]  ok
  state/START_BRIEF.md: 0.3d old [untracked-mtime]  ok
  state/HANDOFF.md: 2.3d old [untracked-mtime]  [frozen-ok]
FRESHNESS: PASS -- boot docs inside the bar.                 [exit 0]
```

## 1. Finding one: the four names are real, but each is implemented piecemeal, and the ladders disagree

**Vocabulary A (the ask's operational quartet).** fresh <24h exists as
`_watch_fresh` in mag/boot_check.py:101-108 (cutoff `time.time() - 24 * 3600`
over watch/*.md, evaluated at every boot snapshot) and again in
tools/visor.py:39 (`LIVE_WRITE_SEC = 24 * 3600`, a billboard counts as live
if written within 24h). stale >7d is tools/freshness_check.py:53
(`STALE_DAYS = 7`). fossil >30d has no module that uses 30d as its bar; the
nearest estate instruments are the quantizer recency floor at >30d
(tools/thought_quantizer.py:94-96, score drops to 0.15) and the L0 raw-event
24h retention tier (mag/auto_quantize.py:14). The corpus tools put the
fossil bar at 64d and 90d instead.

**Vocabulary B (corpus map ladder).** mag/catalog_tags.py:90-102,
`age_class_of`: fresh <7d, aging <30d, stale <64d, fossil >=64d, computed on
mtime "AT RUN TIME, so ages move by design" (docstring lines 16-17). The
docstring also records that these bars were tuned against a specific base
that got replaced mid-lane before parity was pinned: the numbers are
tuned, not derived.

**Vocabulary C (prose census ladder).** mag/prose_census.py:87-102: fresh
<7d, aging <30d, stale <90d, fossil >=90d. The SAME four words as B with a
DIFFERENT stale/fossil boundary (64 vs 90 days). Two modules share a
vocabulary and not a semantics; any consumer reading "fossil" from the two
surfaces is reading two different types.

**Vocabulary D (grandfathered).** Not an age at all. Three independent
mechanisms:
1. content-keyed: mag/links_split_gate.py:59-79 and mag/links_sha_ratchet.py:128-142
   load a `grandfathered` list from a baseline register keyed by sha256; a
   row whose content hash is registered is exempt, and editing the row
   re-keys the hash and silently removes the exemption (links_sha_ratchet.py:11
   states this: content-sha keyed, editing a row loses its baseline grandfather key).
2. position-keyed: links_split_gate.py:31,110-127: rows ABOVE the B2-28
   migration-marker row are grandfathered by the append-only law; the marker
   row itself ("migration-marker.v1") is a type boundary drawn inside one file.
3. count-keyed: tools/md_record_audit.py:103-105,117: exactly the 3
   documented 09-01 template lines may be unparseable; the verdict prints
   "3 grandfathered historical; new = fail". A 4th line fails the criterion.
   The same spirit appears in tools/pointer_rot_check.py:26 (UNANCHORED
   grandfathered history never moves the exit code).

So the ask's quartet is not a proposal for something missing; it is a
proposal to give ONE name to something that already exists under several
disagreeing names.

## 2. Finding two: time base is part of the type, and the estate learned this the hard way

Four distinct time bases are in production right now:

| time base | where | why it exists |
|---|---|---|
| mtime | tools/fossil_check.py:66; mag/catalog_tags.py:90-102; mag/prose_census.py:70 | cheap, universal, but falsified by later edits |
| git commit time | tools/freshness_check.py:65-73 (`last_commit_age_days`) | edit-proof, but blind for untracked files (hence the untracked-mtime fallback at lines 282-287) |
| filename date | mag/stale_sweep.py:31-35 (`_card_date` parses `_YYYYMMDD` from the card name) | cards are edited after landing, so mtime lies about when they were WRITTEN |
| embedded receipt | tools/freshness_check.py:111-193 (`receipt()` / `stale_claim()`) | the only base that re-verifies content at consumption: fail-closed on missing receipt, unparseable or future-dated time (skew bar `CLOCK_SKEW_SECONDS = 300`, line 86), bar exceedance, or source drift (re-hash mismatch, lines 185-191) |

The same physical artifact can be Fresh under one base and Stale under
another. A live instance sits in configs/fossil_registry.json:12: the
compile_report carries a 168h mtime bar while its check_cmd enforces an
independent "pack bar 24h" on the packs themselves. Two clocks, one
artifact, and the registry already knows it. Any type system that computes
age without declaring WHICH time it measures is wrong for at least one of
these surfaces.

## 3. The design: a two-axis type

A temporal type is a tuple: **(age class, qualifier set, declared time
base, bar, optional receipt)**.

### Axis 1: the age lattice (total order, authority descends)

```
Fresh > Aging > Stale > Fossil > Dead
```

- **Fresh**: inside the consuming cadence's bar. Default 24h on the
  watch/boot surface (boot_check.py:102), otherwise k*C where C is the
  consumer cadence, per the FOSSIL-IN-FEED law (watch/inbox/FOSSIL_CENSUS_20260927.md:50-56).
  Full consumption authority, no annotation.
- **Aging**: past the fresh bar, inside human cadence (7d default).
  Consumable with a logged annotation at boot.
- **Stale**: past the surface's stale bar. Load requires revalidation or an
  explicit override naming the consumer. This is the freshness gate's class
  (freshness_check.py:53) and the corpus ladders' 64d/90d class is the same
  type at corpus churn rates.
- **Fossil**: past the bar with no living revalidation. May be CITED as
  history (banked evidence), never LOADED as a live input. This is exactly
  the FOSSIL-IN-FEED disease class: "an artifact compiled/derived ONCE,
  wired into a live consumer, then never recompiled while the consumer's
  cadence ran on" (FOSSIL_CENSUS_20260927.md:22-26, which also names the
  gap: staleness instruments watched DOCS and CLAIMS, nothing watched
  ARTIFACTS IN CONSUMPTION PATHS).
- **Dead**: tombstoned (fossil_check.py:60-62, disposition
  "tombstoned", never warns, death recorded) or DEAD-ARTIFACT (compiled
  once, never consumed; the census's row-1 reclassification,
  FOSSIL_CENSUS_20260927.md:8-13). Zero authority; presence in a live feed
  is a HARD finding (fossil_check.py:63 already prints HARD for
  registry-named-but-missing artifacts).

### Axis 2: qualifiers (exemptions, always registered, never inferred)

- **@grandfathered**: pre-law status anchored to content (sha256 baseline),
  position (marker row), or count (the 3-line rule). Its demotion trigger is
  NOT time: it is content mutation, marker crossing, or count growth.
  md_record_audit.py:105-118 is the cleanest statement of the semantics:
  the 3 historical are fine, any NEW one fails.
- **@frozen**: deliberate freeze with reason+date, registered in FROZEN_OK
  (freshness_check.py:44-51) and required to self-declare in its own header
  (the law at lines 11-14 is implemented by the header comments at 45-50:
  "lineage doc, superseded by its own header").
- **@fixed-oracle**: never ages by design; tracked for change only
  (fossil_registry.json:35-41, adversarial_arc_invariants.jsonl: the wave
  checks its SIZE, staleness is the point).
- **@tombstoned**: death recorded, never warns (fossil_check.py:60-62,81-82).

Type grammar: `<age-class> [@qualifier ...] @ <timebase> | bar <hours> | role <enforcement|observability>`.

The key move: grandfathered, frozen, fixed-oracle and tombstoned are NOT
fifth-through-eighth age classes. They are QUALIFIERS, orthogonal to age,
exactly like `const`/`volatile` in C or purity annotations: a
`Grandfathered Stale` row and a plain `Stale` row differ in what excuses
them, not in how old they are. The estate's registers already behave this
way (a grandfathered LINKS row is simultaneously exempt from the kind law
and old), but no name says so.

## 4. Demotion rules: automatic, silent, receiptless

Time alone demotes; nobody has to act. Three rules:

- **D1 cadence demotion**: `age(timebase) > bar` drops one class. Already
  implemented twice (catalog_tags at run time, fossil_check at patrol time).
- **D2 drift demotion**: source hash changed since the receipt means
  immediate Stale regardless of age. freshness_check.py:185-191 already
  does this: a drifted source fails the gate with "source drifted since
  observation" even if the receipt is seconds old. Content can demote
  faster than time.
- **D3 liveness gate**: demotion is SUSPENDED while the estate has no
  heartbeat. freshness_check.py:272 gates staleness on `heartbeat`
  (repo committed within HEARTBEAT_DAYS=2, line 54). A paused estate must
  not mass-demote: time passes, but the system did not. This is a rule the
  distributed-systems literature under-specifies and the estate solved
  already; keep it.

Demotion never edits the artifact and never files a finding by itself; it
only changes what the next consumption-time check will say. That matches
the estate's WARN-only-first doctrine (fossil_check.py:18-19: enforce is
operator-gated).

## 5. Promotion rules: earned, loud, receipted

- **P1 revalidation**: recompute or re-hash mints a new receipt, restoring
  Fresh for the new bar. The mechanism exists twice: `recompile_cmd` runs
  operator-gated under `--recompile` (fossil_check.py:86-95) and `receipt()`
  is the minting function (freshness_check.py:111-133).
- **P2 revive**: Dead returns to watch only with a named consumer first,
  then a builder. The registry states this as a revive condition
  (fossil_registry.json:19: "revive condition = named consumer first, then
  a tools/ audit builder before rerun"). Order matters: consumption justifies
  regeneration, never the reverse.
- **P3 grandfathering**: never a time promotion; a REGISTRATION act (the
  ratchet's `baseline-update --by <who>` doctrine) that moves an item from
  REFUSE to named, hashed debt. Content-keyed, so any edit silently
  un-grandfathers (links_sha_ratchet.py:11).
- **The asymmetry law**: promotion writes a receipt; demotion does not.
  Silent allocation, loud collection: the same asymmetry Ungar built into
  generation scavenging in 1984.

## 6. The consumption-time type-checker

One entry point: `temporal_check(artifact, consumer, role) -> ACCEPT | COERCE | REFUSE`.
It unifies the two checkers the estate already runs:

- **role=enforcement** (a live consumer about to load: mag/context_pack.py
  at seat boot, scripts/gopher_packs.py at wave launch, mag/gene_pool_feeder.py
  at feed): fail CLOSED below the consumer's declared minimum type. Missing
  time base or unparseable time is Stale, never Fresh (stale_claim(None)
  fails closed, freshness_check.py:171; so does a malformed receipt).
- **role=observability** (the patrol arms: census_patrol_daily, fossil_check
  itself): fail OPEN, WARN only, so a broken checker never blinds the patrol
  (fossil_check.py:13-14 "Fail-open law: a broken check never blinds the
  patrol"; exit contract 0/1/2 at line 21).

The dual failure policy is not new; the estate runs BOTH today without
naming them. The type system's contribution is to make the role a declared
argument instead of an accident of which script you happened to call.

Mechanics, all from existing parts:
1. Load the expected-type declaration from the generalized registry.
   configs/fossil_registry.json already carries 5 of the 6 needed fields
   (artifact, consumer, bar_hours, disposition, check_cmd); add `timebase`
   and `min_type` per consumer.
2. Compute the current type from the DECLARED timebase.
3. Compare. On demotion past the consumer's minimum: **COERCE**
   (serve stale + trigger recompile in the background: the estate's
   home-grown stale-while-revalidate) where a recompile_cmd exists,
   **REFUSE** where it does not.
4. Every REFUSE names the type, the time base, the bar, and the consumer.
   links_split_gate.py:81-87 already writes error strings in exactly this
   shape (line number, id, kind, writer, pointing at the right surface):
   blame assignment is part of the verdict, and the registry's consumer
   column is the blame target.

Implementer note, house law: any subprocess the checker spawns (check_cmd,
recompile_cmd) must carry `creationflags=CREATE_NO_WINDOW` on win32. The
current fossil_check.py:73 and :89 `subprocess.run(..., shell=True)` calls
do not pass it; the new checker must not copy that shape.

## 7. The design decision: do NOT flatten the ladders

The 64d/90d corpus bars and the 7d boot bar are tuned to different churn
rates, and catalog_tags.py:17-19 records that its bars were tuned against a
base replaced mid-lane before parity was pinned. The resolution is the RFC
9111 move: the four names are SEMANTIC (a position in the authority
lattice); the numbers are per-surface configuration, exactly as
fossil_registry.json already carries bar_hours 168, 720 and null in one
file. The ask's 24h/7d/30d quartet becomes the DEFAULT binding for the
watch/boot surface; every other surface declares its own binding of the
same four names. One vocabulary, many bar tables, and a checker that reads
the binding instead of assuming it.

## 8. Literature anchoring (real prior art, honestly mapped)

- **RFC 9111 (HTTP caching)**: freshness_lifetime, Age, stale-while-revalidate,
  must-revalidate map one-to-one onto ACCEPT / COERCE / REFUSE and onto the
  promotion-by-revalidation rule. stale_claim's re-hash at consumption is a
  STRONGER form of revalidation than HTTP's (content-verified, not time-only).
- **Bitemporal databases (Snodgrass; Jensen & Snodgrass)**: valid time vs
  transaction time. The estate conflates them: filename date is the
  artifact's CLAIMED valid time; mtime and commit time are transaction
  times. Declaring a timebase per type is the practical resolution, and the
  receipt-vs-clock disagreement bar already exists (CLOCK_SKEW_SECONDS=300,
  freshness_check.py:86,179-180: a future-dated receipt is a corrupt-clock
  finding, not a fresh one).
- **Ungar 1984, generation scavenging**: most artifacts die young. watch/
  top-level cards are the nursery; the graveyard is tenured space, and
  mag/stale_sweep.py:61-69 moves to watch/graveyard/ and logs the move,
  deleting nothing: promotion to tenured, not destruction. The k*C bar law
  is the generational hypothesis stated as policy: expected lifetime scales
  with observed consumption cadence.
- **Gradual typing (Siek & Taha 2006) and blame calculus (Wadler & Findler
  2009)**: @grandfathered is `Dynamic`: it satisfies any consumer's
  requirement without proof, and the cost is deferred to run time, where
  blame must land somewhere. The estate already assigns blame at
  consumption time, by name: the gate error names line, id, kind and writer
  (links_split_gate.py:81-87).
- **Bounded staleness (Mahajan et al. 2011, causal+ consistency)**: k*C is
  a staleness BOUND proportional to the reader's cadence rather than an
  absolute TTL. FOSSIL_CENSUS_20260927.md:50-52 states exactly this for
  documents: staleness is relative to the consumer, not the clock.
- **Linear types**: today's receipts are affine (reusable until they age
  out). A linear reading, one consumption per receipt, would close the
  reuse loophole where one fresh receipt gates a whole session. The design
  keeps receipts reusable but requires each ACCEPT to append a consumption
  row, so reuse is at least visible in the ledger.

## 9. What this item did not do

No new checker code was landed (this is a design item); no pytest suite
applies since no code changed. I did not run catalog_tags or prose_census
because both write derived sidecars (catalog/tags.jsonl, watch/PROSE_CENSUS_*),
out of scope for a read-only dig. All line citations above were read in
this session; both meter runs in section 0 were executed here, both green.
