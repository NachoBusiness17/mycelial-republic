# INTAKE CARD — RaulJunco event-driven mistakes (2026-09-04)

NAME — X listicle: "top 4 mistakes in event-driven systems" → converges on our own event.v1 durability gap; falsifier fired in our organ same pass.

## ITEM (verbatim)
https://x.com/RaulJuncoV/status/2095180444757049756?s=20 — Raul Junco (@RaulJuncoV), posted 2026-09-02:

> "After years building event-driven systems.
>
> Here are the top 4 mistakes I have seen:
>
> 1. Duplication
>
> Events often get re-delivered due to retries or system failures. Without proper handling, duplicate events can:
>
> • Charge customers twice
> • Corrupt analytics
> • Trigger false alarms
>
> Solutions:
> • Implement idempotency keys
> • Use unique event IDs
>
> 2. Not guaranteeing order
>
> When events arrive out of sequence, state becomes inconsistent.
>
> Solutions:
> • Use Apache Kafka
> • Implement sequence numbers
>
> 3. Dual write problem
>
> Writing to a database and message broker without a distributed transaction can cause data inconsistency.
>
> Solutions:
> • Transactional Outbox Pattern
> • CDC
>
> 4. Non-backward-compatible changes
>
> Updating event schemas without backward compatibility breaks consumers.
>
> Solutions:
> • Versioned schemas
> • Schema evolution strategies (Avro, Protobuf)"

## RECEIPTS
- Root post fetched whole: webReader (cross-confirmed by web search snippet). Sources: x.com status 2095180444757049756 (via webReader render), x.com/.../photo/1 (search index).
- THREAD/REPLIES/COMMUNITY NOTES: WALLED. webReader returned root only; WebFetch on x.com timed out at 60s; search indexes carry no reply text for this status ID. Reply content = walled, see TRI-STATE.
- MEASURE (ran, $0, this pass): 32 concurrent emits through `state/vast/event_stream.py` → **CHAIN BROKEN** at first fork (two writers both claimed seq=353, same ts), 9 duplicate seqs, 2 lost writes (30/32 landed). Chain was clean (349 events) before the test. Repaired backup-first: falsifier rows removed → `CHAIN OK — 349 events`; evidence preserved at `memory/runs/harness/events.jsonl.prefalsifier_20260904`.
- Code receipt: `state/vast/event_stream.py` emit() = read-modify-write on last_event(), no lock, no dedup key, no unique event ID, schema "versioning" = name only (grep: zero hits for dedup/idempot/sequence/version/schema logic).

## SCORE — F:4 P:3 C:4 W:2 N:1 = 14/25 (BUILD, WINDOWED)
- FIT 4 — bolts onto organs we already run: event.v1 stream, steer bus, room.jsonl, board; no new vendor. Not 5: the item is generic advice, not a composable part.
- PULL 3 — feeds Desk/economist arc (gap organs), one_surface missing wire, board-runaway morning organs. Orthogonal to QLoRA/Rocinante/shadow-fields critical path.
- COST 4 — $0 (grep + falsifier + one-pass patch), free lanes.
- WINDOW 2 — Desk gap organs named-but-unbuilt, but queue front is colony-sims drain + economist audit + lite probe. Sits behind them.
- NOVELTY 1 — textbook re-find (Kleppmann DDIA / Confluent canon). Filed as a re-find; repetition-is-emphasis.

## READ
[SOCRATIC] assumption attacked: "a stranger's engagement listicle can't teach a fleet that runs its own hash-chained event stream." Instrument: $0 concurrency falsifier against our own emit(). What survives: not the post's fixes — our architecture's dependence on an UNENFORCED single-writer convention.

- ASSERT (steel-man, author-acceptable): most event-driven failures reduce to four preventable classes — duplicate delivery, unordered delivery, non-atomic dual writes, breaking schema changes — each with a named standard fix (idempotency keys, sequence numbers, transactional outbox/CDC, versioned schemas).
- ATTACK (two named causes, each with evidence):
  1. Genre + content = textbook re-find. The four classes are DDIA ch. 5/11 and Confluent documentation verbatim; the post shape (image, "after years building...", 4-item list) is engagement genre. Evidence: corpus already names the same gaps (Desk salon 09-03: "retry-dedup identity" gap organ + "WAL-before-side-effect missing"; one_surface salon: "steer receipts → event.v1 missing wire" = dual-write class; board runaway 09-03 = live duplicate-writer incident).
  2. The named fixes are shallower than the problems. "Kafka ensures ordering" holds only per-partition (Confluent-documented); "idempotency keys" dodges the hard part — the dedup store itself must commit atomically with state or you relocate the dual-write problem; "versioned schemas" ≠ compatibility without a registry + compatibility mode.
- MEASURE (executed, not described): see RECEIPTS — our own stream broke under 32 concurrent emitters. Mistake classes #1/#2 are now Supported **in our own organ** by our own receipt. The governor-sole-committer law is the only idempotency we have, and it is convention, not code.

## TRI-STATE
- **Supported** — the four failure classes are real and standard; classes 1/2 measured live in our organ. Evidence: this card's falsifier receipt, `events.jsonl.prefalsifier_20260904`, `state/vast/event_stream.py`.
- **Disputed** — "Use Apache Kafka / ensures messages processed in correct order" as stated: true only per-partition. Evidence: Confluent ordering semantics docs.
- **Unproven** — (a) our schema-evolution exposure: event.v1 versioned by name only; `actor` field added post-v0; no reader-breakage known but untested. (b) everything below the wall: replies, quote-posts, community notes (fetch blocked; not scored from, per Amendment 2 the card says so rather than assuming).

## VERDICT — BUILD (windowed), 14/25
The post's content is REMEMBER-grade (textbook re-find, filed as repetition-is-emphasis). What promotes the verb to BUILD: the falsifier converted a named-but-unproven Desk gap organ ("retry-dedup identity") into a **measured defect** — emit() needs a file lock (or enforced single-writer) + a dedup key. One pass, $0, existing organ, morning-organs lane. Windowed behind: economist audit drain, colony-sims steal, swarm-scale GO.

## DOGFOOD
1. INVARIANT PASS — reinforce: receipts-over-claims (listicle claims vs our falsifier receipt), cheapest-lane ($0 test), files-are-data (stream broken and repaired as data, backup-first), coverage thesis (a forked record where two writers both claim "it happened" IS the coverage failure class). No contradictions with the 47. EXTEND: single-writer-as-architecture is idempotency only when ENFORCED — convention is not a lock.
2. STOCKFISH PASS — opcode `intake.card` → routes to event_stream organ patch (morning-organs / Desk gap-organs lane); flight-recorder tag = subsystem:event_stream, class:durability. Placement clean — no placement failure.

## Two counters (L0)
- FORBIDS: concurrent multi-writer emits into events.jsonl without a lock — this falsifier is the forbidden-pattern proof.
- PAID RENT: one receipt that upgrades a salon-named gap organ to a measured defect, for $0.

## THE CROP (what this pass did not see)
- Replies/quote-posts/community notes (walled) — a seat with an X-logged-in surface (phone driver lane) should mine them before this genre is fully trusted.
- HARNESS_SPEC.md read only via the .py bytes, not the spec's durability section.
- Emitter census owed: who calls emit() concurrently in practice (grep of callers not run).
- Next chair: the economist/flight-recorder owner — this receipt belongs in the per-op envelope as subsystem=event_stream, durability class.

## ROUTE
- Card: `watch/INTAKE_RAULJUNCO_EVENT_MISTAKES_20260904.md` (slug unique vs watch/ shelf).
- Typed room row appended to `watch/room.jsonl` (kind: intake.card).
- No OUTBOX wire (not BUILD NOW). Patch spec for the windowed build lives in this card's VERDICT section.
- Falsifier backup: `memory/runs/harness/events.jsonl.prefalsifier_20260904`.
