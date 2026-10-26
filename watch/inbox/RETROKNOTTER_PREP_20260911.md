# RETRO-KNOTTER PREP — staging spec for the orphan fold (NO chain writes)

Date: 2026-09-11 · Lane: zcode, wave standing cycle slot 1 of 6 (night rotation) ·
Status: STAGING ONLY. The chain is not touched in this slot. Nothing here appends until
the truth-gate fix (§1) is in force and operator GO lands.

Absorbed (not duplicated): watch/inbox/SURGERY_FORENSICS_20260911.md (6,661 → 4,914 →
7,377 chain states; cut/rebuild anatomy; content-addressed filename binding; root-reuse
falsifier), KPI_LEDGER_DECODE_20260911.md (kpi as independent chain-length witness; the
15 kpi-only leaves 6,662-6,676; tip_root DISPUTED as row-level witness — use n_leaves),
SILENCE_DOSSIER_20260911.md (the 2,960 silence knots, day census, corrupt inventory),
GHOST_ARITHMETIC_20260911.md (ts-vs-event dating law), state/CURRENT.md step_i, and the
audit the step points at: watch/audit/FULL_AUDIT_20260908/FULL_AUDIT_20260908.md §6
(LINKAGE-PASS is not TRUTH-PASS; no append lock in grounding_wave.py::post; admission
accepts the caller's SUPPORTED label).

---

## 1. APPEND-LOCK SPEC DRAFT — what must exist before ANY chain append

**Why (the audit's findings, verbatim in substance):**
- `grounding_wave.py::post` rereads the full ledger per append with NO append lock —
  concurrent writers race. The kpi decrease census already shows the cost: 192 ±5-leaf
  jitters of multi-writer counting noise, plus the Aug-23..25 retraction band.
- Admission accepts the caller's SUPPORTED label with no entailment check and no second
  witness.
- Astra witness #5's false-receipt attack: a row claiming 1,000,000,000 posts with a real
  prev-hash PASSED the verifier. Verdict: chain PASS is a LINKAGE gate, not a TRUTH gate.
- step_i names the fix: "append lock + second witness or rename LINKAGE-PASS."

**Requirement A — the append lock (mechanics):**
1. One lock, one instance: a single lockfile beside the chain
   (`memory/biography/verkle_chain.jsonl.lock`), taken exclusively (O_CREAT|O_EXCL, or
   fcntl/portalocker) by EVERY appender — mag/records.py, mag/grounding_wave.py, any
   retro-knotter, any backfill path. No side doors.
2. Lock held across the whole critical section: read tip → build row → hash → append →
   flush → fsync → release. No reader-writer split: appends are serialized end to end.
3. Stale-lock rule: the lockfile carries {pid, hostname, ts_utc}. A newcomer may break a
   lock only if the pid is dead AND the lock age exceeds a threshold (suggest 300s); the
   break is itself logged as a row in the lock journal. A live-pid lock is never broken —
   the contender backs off and retries.
4. Sequence-number fence: after acquiring the lock, re-read the tip; if it moved since
   the contender's pre-lock read, rebuild the row against the new tip (no stale-parent
   appends). The chain's own invariant does the rest: parent_verkle_root must equal the
   previous row's verkle_root (0 breaks chain-wide today; the lock keeps it that way).
5. Guard continuity: mag/chain_guard.py stays the flag-loss guard; the lock extends
   coverage from "silent flag loss" to "concurrent append loss." Same guard family, one
   more tooth.

**Requirement B — the second witness (truth gate):**
1. Writer ≠ witness: the appending process computes the row; a DIFFERENT process (and
   ideally different lane/key) verifies before the row commits: re-derives leaf_hash from
   canonical payload, re-checks parent linkage, AND checks the content claim against
   ground — knot file exists on disk and hashes to the claimed leaf_hash; dossier_commit
   resolves for session-bound rows. Linkage alone is not enough; that is the lesson of
   witness #5.
2. The witness emits its own receipt: {row verkle_root, verdict, gate: TRUTH|LINKAGE,
   ts}. A row without a witness receipt is quarantined (staged, not chained).
3. Admission stops trusting the caller's label: a SUPPORTED claim entering the chain
   carries evidence paths, and the witness spot-checks at least the hash-of-content
   binding. Entailment checking stays a later organ; hash-to-ground is the minimum gate.
4. The rename fallback: if B is not yet wired, every verify output reads "LINKAGE-PASS",
   never bare "PASS" (audit §8 law 2: every PASS names its gate). This is the floor, not
   the destination.

**Gate for this fold:** the retro-knotter may not append until A + B are live (or the
rename is in force AND A is live — a lock without a second witness would fold 16,000+
rows through the exact gate witness #5 broke). Operator GO on the truth-gate fix comes
first per step_i; the fold queues behind it.

## 2. FOLD ORDER — three classes, oldest claim first, strict append-at-tip

Chain law respected throughout: the chain is strictly linear (parent = previous root,
chain-wide, 0 breaks). Retro rows are APPENDED at the current tip (idx 7,377 onward);
nothing is inserted mid-chain, nothing pre-existing is rewritten. Each retro row carries
its historic position in `recovery.witness`, never in a faked parent link. Within each
class, append in event-date ascending order so the folded band reads chronologically.

**Step 0 — partition recount (before any folding):** the mission's two class counts were
taken by different censuses — 2,960 = ALL knot files date-prefixed Aug-16..31 (silence
dossier); 13,693 = dated files never referenced by any chain row (forensics). They
overlap imperfectly (e.g. idx 1144, the last pre-silence row, IS one of the 2,960's
Aug-16 files; forensics counts only 3 orphans on Aug-31 because the rebuild chained
310/313). Fold-eligibility gate for every file: exists in `memory/biography/knots/`,
date-prefix in class range, AND its filename's 8-hex tag matches no current-chain
leaf_hash/dossier_commit prefix AND its filename appears in no current-chain row.
Recount produces the true per-class fold counts; the numbers below are planning targets.

**Class 1 — the 2,960 silence knots (FIRST; event-dated Aug-16 → Aug-31).**
- Why first: freshest files, richest witness set, and an independent contemporary count
  witness — this is the only class where a second ledger (kpi.jsonl) watched the same
  window live.
- Witness set: (a) the knot files themselves — 2,944 parsable (2,943 session_scalar +
  1 usage_digest) + 16 zero-byte/corrupt artifacts that are NOT folded as content, only
  recorded as gaps; (b) the silence dossier's day census; (c) logs/kpi.jsonl as the
  independent chain-length witness for the dark window (n_leaves only — tip_root is
  DISPUTED as a row-level witness per the KPI card's schema finding); (d) dedupe against
  the 249 current rows event-dated Aug-16..30 (rebuild re-knots of the same periods —
  dedupe by session_id + tag, not by date alone).
- Hash method: canonicalize the leaf payload → sha256 = leaf_hash (recomputed at fold
  time, must equal the filename tag prefix per the content-addressed binding — 50/50
  sample-verified in forensics); parent = tip at fold moment; historic anchor recorded as
  {event_date from filename, writer token, session_id}.

**Class 2 — the remaining dated orphans (target ≈ 13,693 minus class-1 overlap ≈
10,733; recount at step 0; span 2026-07-10 → mid-Aug).**
- Two sub-classes, different witness strength:
  - **Cut survivors (1,452 files in this pile):** their original chain rows survive
    VERBATIM in `memory/biography_backup/biography_backup_20260830/verkle_chain.jsonl`
    (leaf_hash, session_id, dossier_commit, original ts). Strongest witness in the whole
    fold: fold by byte-faithful restore of the original row metadata — original leaf_hash
    is KEPT (not recomputed), original ts preserved as `original_ts`, and the row is
    marked recovered (§3).
  - **Never-chained backlog (the rest of the 13,693):** witness = the knot file itself
    only (the old chain never indexed it). Hash method: same as class 1 — recompute
    sha256 of canonical payload, bind to filename tag, verify before append.
- Also routed here: the 304 cut-dropped files absent from disk and the 18 chained
  filenames missing from disk are NOT foldable from files — they stay on the forensics
  unrecoverable inventory unless the tarball dig (`knots.bak-orphanlane-20260906T224709Z.tar`,
  66.9MB) surfaces them. The fold does not fabricate.

**Class 3 — the 15 kpi-only leaves, counts 6,662-6,676 (LAST; dossier_commit path).**
- What they are: appends kpi watched live on Aug-28..30 (6,661 → 6,676 before the cut),
  after the Aug-30 backup was taken — present in NO chain file and NO backup. Witnessed
  by count only.
- Witness set: logs/kpi.jsonl rows in the Aug-28..30 window (ts + n_leaves increments;
  n_leaves only, never tip_root). That witnesses THAT they existed, not WHAT they said.
- Hash method: dossier_commit path — pull the Aug-28..30 session dossiers, bind each
  leaf to its session, rebuild leaf content from the dossier, then hash canonically.
  Hard rule: never invent a leaf_hash for unseen content. Per leaf, exactly one of three
  dispositions: (a) dossier resolves → fold as a rebuilt row marked recovered, content
  basis = dossier_commit; (b) dossier absent → record a documented GAP entry in the fold
  ledger (kpi ts + count position), no row appended; (c) content surfaces from an
  unaudited path later → reopen. An honest 15-row gap beats one fabricated knot.

## 3. AMENDMENT STAMP FORMAT — `recovered-2026-09-11`, never silent backdate

Every folded row carries a `recovery` block, self-declaring, machine-checkable:

```json
"recovery": {
  "stamp": "recovered-2026-09-11",
  "class": "silence | dated-orphan-cut-survivor | dated-orphan-backlog | kpi-only",
  "witness": ["<path or kpi ts+count anchors that justify the row>"],
  "original_ts": "<row's true historic ts, ONLY when a backup row or kpi row supplies it>",
  "original_index": "<backup-chain index, cut survivors only>"
}
```

Laws the stamp enforces:
1. `ts` on a folded row is ALWAYS the fold moment (append time). Historic time lives only
   in `original_ts` and in the filename's event date. A backdated `ts` is a lie about
   when the record entered the chain — forbidden, no exceptions, no "just this once."
2. Filenames are never renamed to look contemporaneous; a knot keeps the name it was
   born with. Event dating comes from the filename, append dating from ts, and the two
   are different ledgers by law (ghost-arithmetic finding).
3. Precedent in the record: `repaired_from_pointer` already appears on exactly 5 rows and
   `verkle_repair_state.json` already marks a repair moment — this stamp is the same
   convention generalized, not a new religion.
4. Silent means silent-in-reverse too: no folded row without the block. A fold script
   that emits an unstamped row fails its own run.

## 4. FALSIFIER — the whole fold is wrong if ANY of these fire

Backup-first: the fold runs against a fresh chain backup (`verkle_chain.jsonl.bak-prefold-*`);
one seat folds, a different seat verifies (one builds, one verifies).

- **Byte-prefix invariance:** post-fold rows 0..7,376 are byte-identical to pre-fold. Any
  changed byte = silent backdate or rewrite = fold reverts.
- **Uniqueness (forensics root-reuse test re-run):** 0 duplicate filenames, 0 duplicate
  leaf_hash, 0 duplicate verkle_root chain-wide after the fold. Any duplicate = identical
  content re-knotted = fold reverts and the dupes are dispositioned by hand.
- **Binding:** 100% of folded rows' 8-hex tags resolve to a knot file on disk whose
  recomputed canonical sha256 equals the row's leaf_hash. One mismatch = fold reverts.
- **Count reconciliation:** folded class-1 count equals the step-0 recount of eligible
  silence files (within the 16 corrupt artifacts, dispositioned as gaps); class-3 folds
  exactly 15 rows or carries a per-leaf written gap disposition. The kpi anchor stays
  exact: pre-fold 7,377, and kpi's post-fold writes must show the new tip marching
  forward, never backward.
- **Stamp census:** 100% of folded rows carry `recovered-2026-09-11` + class + witness;
  0 folded rows carry a `ts` earlier than the fold window's start.
- **Reopen triggers from the sibling cards:** any of the 304 absent files or the 15
  kpi-only leaves surfacing later with content contradicting the fold's dispositions
  reopens the fold verdict.

## CYCLE GENETICS

Worked: absorbing the sibling cards BEFORE writing — hunting the 2,960's provenance
caught that the mission's two class counts use different censuses (all-files vs
never-referenced), which would have double-folded ~hundreds of knots; tri-state + receipts
kept every spec clause anchored to a measurement. Next cycle should change: demand the
step-0 partition recount as its OWN slot output (a counted partition file, not a clause
inside a spec), and have wave slots cross-link absorbed siblings in their first 5 lines so
provenance hunts cost one read instead of four.

---

Staged by retro-knotter-prep worker (zcode, slot 1/6, night rotation 2026-09-11).
Read-only except this file. No chain writes. Chain tip untouched: 7,377 leaves, 8bd58896.
