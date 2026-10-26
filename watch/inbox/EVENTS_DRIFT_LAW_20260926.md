# EVENTS.jsonl drift law (B2-161, 2026-09-26)

Decision: **refresh-owner re-register**. Frozen-snapshot is falsified by
bytes: the stream was verified a frozen projection of LINKS.jsonl rows
275-331 (B2-146), yet armed writers have since appended and the last row is
now dated 2026-09-26T11:53:49Z (51 rows, sha 91D40DDA.., byte-equal to the
B2-197 registration at index_events seq 1789823567015749413, 13:53:59Z).
A no-writer policy cannot hold when writers are armed and have already fired.

Rules, effective on landing of this note:

1. The registered truth for EVENTS.jsonl is the NEWEST register event in
   watch/inbox/index_events.jsonl whose `file` field is EVENTS.jsonl (class
   DATA). Readers must take max(seq), not first match.
2. The owner of an append is the lane whose writer touches the file. Every
   append carries the duty to re-register in the same critical section:
   one `op: register` row, class DATA, purpose naming the append and the new
   row count. An append without its re-register is a stale-truth defect owned
   by the appending lane.
3. A reader that finds current bytes disagreeing with the newest register
   does not roll back (no-erase law). It files a true-up register naming the
   racing append, or leaves the bytes and files the defect to the owner lane.
4. The B2-146 prefix property (rows 1..51origin matching LINKS 275-331) stays
   a historical fact, not a maintenance obligation; the B2-197 prefix seal
   (12:31:49Z appends noted at the 13:53:59Z registration) is the precedent:
   growth past the projection is legal, silence about it is not.

Precedent kept: the ESSENTIALS_PACK_20260926 hash-refresh event 3056 is the
same pattern (semantic change owes a re-seal, the old sha is never rewritten).

Landed by: watch/inbox/burn_wave_20260926/B2_161_events_drift_policy_20260926.md
