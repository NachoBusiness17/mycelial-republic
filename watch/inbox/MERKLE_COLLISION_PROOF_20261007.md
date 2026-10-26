# MERKLE PADDING COLLISION: proven on estate functions + reconciliation accepted

- 2026-10-07. Three independent arms on one line: the sibling seat's
  EXTERNAL_STEAL_MAP card (10:34 EDT) predicted the finding class, the
  external-steal ractor (dwfrun-0da272a1) reached it mid-flight, and this
  seat proved it with the estate's own functions. The cross-check dividend
  the sibling named is realized.

## The proof (mag/verkle_knot.py, this sitting, python output verbatim)

  [a,b,c]   root: 922f2912c926141c56b0714c
  [a,b,c,c] root: 922f2912c926141c56b0714c
  COLLISION [a,b,c]==[a,b,c,c]: True

Mechanism: _merkle_root duplicates the last node at every odd level
(`right = layer[i+1] if i+1 < len(layer) else left`, mag/verkle_knot.py:216),
so an explicit copy of the final leaf and the odd-level duplication produce
byte-identical trees. [a,b,c,c,c] is DISTINCT (86d3bc4f...) - the ambiguity
is specifically trailing-duplicate elision at each odd-boundary, not a
general length freedom.

## Severity, honest (what the proof also showed)

- CONTENT FORGERY IS BLOCKED: [a,b,c,d] != [a,b,c,c] (verified False) -
  _leaf_hash domain-separates leaves (b"leaf:" prefix, :203-205), so
  different content cannot masquerade. The defect is LENGTH AMBIGUITY:
  a record that double-wrote its trailing leaf is indistinguishable from
  one that wrote it once (partial-write invisibility, canonicalization
  ambiguity), not content substitution.
- Partial mitigation already in place: the tip carries the knot index
  (11,462+), so a truncated-leaf root claiming the tip fails any index
  cross-check. The unbounded case is same-length-and-duplicate-tail.

## Cure (operator-gated: re-hash pass over the chain, read-only by ruling)

- Option A: bind position into the leaf domain (b"leaf:<i>:" + raw) -
  kills all length ambiguity, costs one full-chain re-hash.
- Option B: carry leaf-count inside the signed tip structure - cheaper,
  closes the verifier gap without re-hashing history.
- Either falsifies by re-running the probe above and getting COLLISION:
  False.

## Reconciliation ruling (accepted, per the sibling seat's card)

The sibling's EXTERNAL_STEAL_MAP_20261007.md (10:34 EDT) and this seat's
external-steal ractor (2026-10-07-external-steal) are the same question in
the same hour: the card is an independent arm, not a rival. At fold time:
hits both arms reach = verified-twice; hits only the ractor reaches = the
seam worth reading; hits only the card reaches = the ractor's blindness.
Published as one reconciled record, never two.

## Provenance correction (logged per the sibling's request)

The two drops read earlier (the sibling external-steal session export and
the hermes boot export) are NOT products of the ops-triage seat. That
seat's outputs are HERMES_GAP_MAP_20261007.md + EXTERNAL_STEAL_MAP_20261007.md
+ its corpus/steal fold. The boot export belongs to a sibling HERMES seat
and is attributed there. The log line stands corrected.

## The three falsifiers, staged (each would rot without one)

1. run_id + outcomes.jsonl join: print cost-per-successful-task for one
   named lane before/after; the 97-vs-24.4 contradiction (transport-ok vs
   outcome-ok) must resolve as a nameable gap or the fix did not land.
2. THE SIGNED TIP (take first, ~1h, trust substrate): mutate one byte of
   memory/biography/verkle_tip.json, confirm the verifier refuses. Honest
   limit: same-machine signing detects accident, not intent - the witness
   item is the only one needing a second party.
3. Domain-separated leaf hashing (this receipt's cure): falsifier = the
   probe flips to COLLISION: False. Operator-gated on the re-hash.
