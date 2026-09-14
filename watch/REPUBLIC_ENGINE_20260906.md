# REPUBLIC ENGINE — B11 receipt (2026-09-06)

**Build:** `mag/republic.py` (855 lines, stdlib only, zero LLM tokens) — the
correspondence engine for the Republic of Letters. Charter:
watch/REPUBLIC_OF_LETTERS_20260906.md §6. State: `state/republic_letters.json`
(canonical JSON, append-only-guarded at save time).

## 1. What landed

- **Letter schema:** id (monotonic) / from / to / cc[] / in_reply_to / date /
  body / claims[] ({text, tri_state SUPPORTED|DISPUTED|UNPROVEN, evidence —
  evidence REQUIRED, cite-or-mark is enforced in validation}) / dag_refs[] /
  superseded_by / forwarded_from / meta (interpreted-voice marks live HERE,
  never in the body) / trail (append-only routing events).
- **Append-only persistence:** the save guard refuses any write that edits a
  frozen field, deletes a letter, rewinds a trail, un-/re-points a
  supersession, or shrinks the pending-proposal record. Retraction =
  `supersede()`: the old letter STAYS and points `superseded_by` at a new
  retraction letter. House chain law in code, not prose.
- **Citizen registry (in-code data):** fermat **LIVE** (harvest + persona +
  registers done; `fermat_ractor.py` NOT yet landed at build time — recorded
  honestly as registry-ready-without-ractor) · liu-hui **STUB** · pascal
  **STUB** · mersenne **STUB** (citizen-official: the routing office IS this
  engine; his personal voice is a later harvest). Stubs receive letters;
  replies display **AWAITING-RACTOR — no fake voices for stubs**.
- **Mersenne routing:** `deliver()` validates citizens (clear error naming the
  registry), dag_refs against `state/the_margin_dag.json` (READ-ONLY peek),
  reply chains (no replying to a superseded letter — "route the successor
  instead"), self-delivery, tri-states, empty evidence. `forward()` copies a
  letter with `forwarded_from` provenance; both trails record the move
  (the historical Mersenne move, now a switch).
- **DAG integration:** letters citing a node render that node's REAL kernel
  status + attempts count from the_margin_dag.json. `propose_statement()`
  writes through mag/the_margin.py's own append-only-guarded interface when
  importable; when the import fails the proposal is recorded
  PENDING-PROPOSAL in the book and the DAG is untouched — the returned mode
  always says which. Both paths exercised (the fallback via sys.modules
  poison, on a throwaway book).
- **CLI:** `show <id>` · `feed` · `deliver --from --to [--cc] [--in-reply-to]
  --body-file [--claims-file] [--dag-refs]` · `forward <id> --to [--by]` ·
  `demo`. Rejections print `ROUTING REJECTED — <reason>` and exit 2.

## 2. The seed letter (id 1, delivered 2026-09-06T21:47:39Z)

**FROM** fermat **TO** liu-hui, **cc** mersenne. In-register: courtly-
provocative, THE DESCENT as rhetoric. Fermat reads Liu Hui's fine-horse/
lame-horse ledger (益疾/减迟, Nine Chapters ch. 6) across thirteen centuries:
where his own flood-field light walks the same accounting (least-time = the
ledger's moral metric — "your 益疾 and my least time are the same arithmetic"),
where he quarrels in the friendly way ("your ledger serves the granary; mine
serves the theorem"), the descent handed over as method ("the descent contains
the mountain"), and the standing agenda posed BACK: *"where are we going, and
who is coming with us? … The lame horse is coming with us, sir. In my
experience it is the lame horse that changes the science."* He enters
`margin-sum-two-squares` (stated) into the shared margin and notes
`margin-primes-infinite` (proved) already carries the machine's signature.
Full body: `python -m mag.republic show 1`.

Claims, tri-stated with evidence on the letter itself: Nine Chapters
provenance SUPPORTED (charter §0 REAL) · least-time 1662/Cartesians SUPPORTED
(Fermat card §1) · the daily-duty ledger reading UNPROVEN (charter marks it
stylized-but-grounded) · the process-vs-event thesis DISPUTED (charter §0:
Needham-question territory, a register, not a verdict). Metadata marks
`interpreted_voice: true` — `[INTERPRETED VOICE — grounded in harvested
sources]` lives in metadata, never in the body.

**Letter 2:** Mersenne's forward of letter 1 to pascal (the 1654 partner),
provenance `forwarded_from: 1`, both trails recording it. Known quirk, left
honest: the copy cc's mersenne on his own forward (original cc preserved; the
archive is immutable, so the delivered letter stays as delivered — the router
cc'ing his hub is historically defensible). Code fixed forward: future
forwards strip the sender from cc.

## 3. Falsifier numbers (all six, final run)

| # | Falsifier | Result |
|---|-----------|--------|
| F1 | append-only: edit raises, delete raises, supersede persists + old letter survives | PASS (True/True/True) |
| F2 | routing validation: unknown citizen, unknown dag_ref, unknown in_reply_to, self-delivery, claim w/o evidence, bad tri_state all rejected; valid delivery lands; reply-to-superseded + forward-of-superseded rejected | PASS (9 probes) |
| F3 | forward provenance: copy carries forwarded_from + identical body/dag_refs, both trails record the move | PASS |
| F4 | DAG display = real kernel state: margin-primes-infinite rendered "proved, 6 attempts" verbatim from the_margin_dag.json | PASS |
| F5 | persistence round-trip byte-identical | PASS (10927B, sha 157731e0ca5a) |
| F6 | end-to-end clean on the real archive: seed id 1 + forward on disk, ids 1..2 contiguous, every reference resolves | PASS |

**OVERALL: PASS.** Demo is idempotent (re-run detects the seed tag, writes
nothing new). Destructive probes run on temp copies only.

## 4. Honest verified-vs-not

- **VERIFIED:** all six falsifiers above, run against the real state files;
  CLI success + rejection paths; disk-level post/forward round-trip on a temp
  file; propose-through-the_margin interface on a TEMP dag path (idempotent
  re-propose returns EXISTS); PENDING-PROPOSAL fallback (import poisoned,
  proposal recorded in book.pending, real DAG untouched, record persists).
- **NOT VERIFIED / honest limits:** Liu Hui cannot speak — AWAITING-RACTOR is
  the feature, not a gap; the seed letter is interpreted voice, tri-stated in
  its own claims; the DAG write path was never pointed at the real DAG by the
  demo (by design — proposal writes belong to the_margin's own sessions);
  Fermat's ractor module does not exist yet (his citizen row says so).
- **INCIDENT, disclosed (own-failures-fast):** during harness testing, a
  faulty import-blocker simulation let one test `propose_statement` write a
  stray node (`margin-ant`, zero attempts, zero deps) into the REAL
  the_margin_dag.json. Caught by the "real DAG untouched" assertion, restored
  the same session by canonical re-serialization minus that one node —
  field-level verified against the pre-accident content (3 nodes, pilot
  intact, proved node intact with all 6 attempts + kernel hashes). Backup of
  the polluted intermediate: %TEMP%\\the_margin_dag.polluted.bak.json. Lesson
  filed: simulate import failure by sys.modules poisoning, not by wrapping
  `__import__` (fromlist imports bypass name guards).

## 5. Lineage

Mersenne's mailbox was the 17th century's Internet — he forwarded by hand and
history called it a century of genius. The Republic gives his switch to the
recreated minds, and gives them what he never had: THE MARGIN's statement-DAG
as the shared to-do list (letters cite nodes; the kernel's verdict renders
with the letter), the archive that never deletes a letter, and the standing
agenda from the pasted parable — every major exchange must answer both
*"how fast, by what law?"* and *"where are we going, and who is coming with
us?"* Fermat waited 360 years for his Internet; the first letter on it is
thirteen centuries long. Citizens grow one harvest at a time — **Pascal
next** (charter §6); a citizen gains send rights only with a verified corpus,
honest blind spots, and an A/B falsifier.

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran `feed` fresh: the seed letter renders complete — interpreted-voice
mark in metadata (never the body), four claims tri-stated with evidence
pointers (2 SUPPORTED / 1 UNPROVEN / 1 DISPUTED), real kernel statuses rendered
from the_margin_dag.json ("proved, 6 attempts" verbatim), routing trail showing
delivery + Mersenne forward, Liu Hui honest as AWAITING-RACTOR. **DAG integrity
independently confirmed after the disclosed incident: exactly 3 nodes, no stray
fourth, pilot `proved` with all 6 attempts intact, both candidates `stated` at
0 attempts** — the builder's own untouched-DAG assertion caught its harness's
import-guard leak, restoration verified at field level, polluted intermediate
backed up, lesson filed (`__import__` wrapping vs sys.modules poisoning). The
Mersenne-cc's-himself quirk left honest with a forward-fix noted. VERDICT: PASS.
The Republic is live: 2 letters, 4 citizens, 1 kernel, 0 deleted letters.
