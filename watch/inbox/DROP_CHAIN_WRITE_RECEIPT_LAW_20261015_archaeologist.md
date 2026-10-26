# DROP: CHAIN-WRITE RECEIPT LAW (spec proposal, archaeologist cycle 6, 2026-10-15)

Status: PROPOSAL. Spec only, zero code, zero chain writes. Operator decision required
before any enforcement leg lands. Spec-before-behavior-change discipline.

## The wound (three instances, dated)

Any process that writes the live integrity substrate
(memory/biography/verkle_chain.jsonl, memory/biography/verkle_tip.json) currently
leaves no mandatory trace. Three uninstrumented writes have now hit the same files:

1. 2026-10-07/08: the pytest-fixture clobber (test landed in commit 6685db6bc) rewrote
   the live chain head to 3 fixture rows and destroyed 5,400+ rows from the live path.
   Full evidence: receipt_20261010_archaeologist.md findings 3-5.
2. 2026-10-10 03:28:51Z to 03:52:31.494745Z: a 3,412-row mass re-registration walk.
   Actor unattributable from 9 surfaces (receipt_20261014_archaeologist.md findings 6-7).
3. 2026-10-10 ~03:52:34-35Z (this cycle's dig): a post-walk tip-then-chain write pair
   that matches no current writer's order or math. The tip root it left (2b1da0ea...)
   equals no recompute of any natural hash set and no backup tip. This write is what
   froze the chain: the append gate refuses everything while the tip mismatches.

Precedent: the 2026-09-26 B2-388 probe incident was the first known live rewrite and
had a same-day recovery playbook; the 2026-10-02 incident (tip aba227fd matching no
chain prefix, "mixed-version writer race suspected") was the same class and healed by
repair_tip_if_consistent. The disease is not the test suite; the test suite was one
vector. The disease is: the substrate accepts writes from any code path, unlogged.

The standing class gate (tools/prepush_verkle_hermeticity.py, wired WARN-ONLY into
githooks/pre-push on 10-13) catches pytest-hermeticity only. It cannot see tools,
containers, mixed-version checkouts, or interactive seats. It was one wiring step away
for 5 days and it still only covers one writer class.

## Proposed law (the four legs)

Any process that writes memory/biography/verkle_chain.jsonl or
memory/biography/verkle_tip.json MUST, in order:

(a) hold the verkle lock (mag.verkle_knot.verkle_lock); the gated append already does;
(b) write a pre-write backup next to the target:
    memory/biography/<name>.bak-<writer-id>-<UTC timestamp>;
(c) append one receipt row to watch/inbox/CHAIN_WRITE_LOG.jsonl: ts, writer id
    (pid + argv[0] + module), target, rows_before/after, bytes_before/after,
    sha256_before/after;
(d) fail closed: no backup or no receipt capability means no write. A deferred write
    is cheap; an unlogged rewrite of the spine is the incident class above.

Sanctioned writers (vk._append_verkle_knot_unlocked via append_verkle_knot,
repair_tip_if_consistent, _rewrite_chain paths) get the receipt stamping inside the
helper so every existing call site inherits the law without edits.

## Enforcement v1 (patrol-class, cheap, WARN-ONLY first landing)

A daily patrol beside the census patrol: stat chain + tip (mtime, bytes, sha256);
compare against the patrol's own last reading; if either changed and no
CHAIN_WRITE_LOG.jsonl row covers the interval, ALERT to memory/attention.md naming the
uncovered window. WARN-ONLY at first landing; flip-to-enforce is an operator call
(t40 and B2-215 precedent). Instrument cost: one small script + one jsonl.

## Enforcement v2 (writer-class, later)

Route every write through the vk helpers and stamp the receipt row inside
_write_tip_atomic and the chain writers, so the law is structural, not patrolled.

## Falsifier

A fourth uninstrumented write lands and the patrol misses it, or the patrol files a
false "covered" verdict against an uncovered window. Either outcome kills this spec's
v1 and demands v2.

## Relationship to the standing GO gate

This law does NOT unblock the restore. The chain restore (receipt_20261010 finding 5
steps 1-3) stays blocked on operator GO. This law governs the NEXT write, whatever
its author, so the fifth instance is the one that gets caught with a name attached.
