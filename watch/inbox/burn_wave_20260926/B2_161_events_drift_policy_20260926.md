# B2-161 EVENTS.jsonl drift policy (2026-09-26)

## Verdict

LANDED. Decision: refresh-owner re-register. Frozen-snapshot was rejected on
bytes: the stream's armed writers already extended it past the B2-146
LINKS.jsonl 275-331 projection (last row 2026-09-26T11:53:49Z), so a no-writer
policy is not enforceable. The decision is filed as a short LAW note at
watch/inbox/EVENTS_DRIFT_LAW_20260926.md with four rules: newest-register-is-
truth, append-owes-re-register in the same critical section, no rollback on
stale sha (true-up instead), and the prefix property demoted to historical
fact.

## Evidence file:line quotes

- watch/inbox/EVENTS.jsonl current bytes: 51 rows, sha256
  91D40DDA9B1B902B993FD6EAEB868BBAB003289A622BB4E9FD1518C3B021628B, computed
  this lane, byte-equal to the registration in watch/inbox/index_events.jsonl
  seq "1789823567015749413" (13:53:59.162Z, class DATA): "51 rows
  2026-09-20..26 byte-match LINKS.jsonl origin lines 275-331 (B2-146);
  reclassified living sealed by B2-197: armed writers appended 12:31:49Z
  today, prefix seal ends the refresh-churn cycle".
- Last EVENTS.jsonl row ts "2026-09-26T11:53:49Z": growth past the frozen
  projection is already live, which is the fact that kills frozen-snapshot.
- Precedent row cited by the brief: ESSENTIALS_PACK_20260926 hash-refresh
  event 3056 (semantic change owes a re-seal; old sha never rewritten).

## Work done

1. Measured EVENTS.jsonl bytes, row count, last-row ts; compared sha to the
   newest index registration (equal: no drift at decision time).
2. Read the B2-197 registration purpose text and the B2-146 prefix claim.
3. Wrote the decision as watch/inbox/EVENTS_DRIFT_LAW_20260926.md (four
   rules, precedent named, no existing file edited).
4. Filed this receipt, LEDGER row, QUEUE pointer, INDEX registration for the
   law note and this receipt.

## Falsifier

This decision is inverted if any of the following holds: (a) every armed
writer of EVENTS.jsonl is disarmed or retired by date X and no append occurs
for a full window, making frozen-snapshot viable again (the law then overspecifies
owner duty; revisit); (b) an append lands without its re-register and no
true-up names it within the same day (rule 2 is not being enforced by any
surface); (c) the law note bytes drift from the newest register without a
true-up (the law itself went stale, by its own rule 3 the drift must be
named, not rolled back).

## Bibliography closed

watch/inbox/EVENTS.jsonl (bytes read, sha computed); watch/inbox/index_events.jsonl
seq 1789823567015749413 and the ESSENTIALS_PACK refresh event cited by the
brief (read from the registration purpose text; event 3056 not independently
re-counted, accepted as registered precedent); B2-146 byte-verification
accepted via the registration text. No web calls.
