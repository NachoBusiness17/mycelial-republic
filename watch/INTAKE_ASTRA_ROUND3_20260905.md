# INTAKE CARD — ASTRA ROUND 3 (the binding audit, 2026-09-05)

**Round 3 measure: PASS — and it audited the one thing we hoped nobody would check.**
FT verbatim: corpus/frontier_thinking/FT_ASTRA_DOOR3_20260905.md.

## VERIFICATION LEDGER (all recomputed live)
| claim | state |
|---|---|
| Unabridged receipt 1 reproduces our hash, passes d=16 | CONFIRMED (its statement) |
| Quoted Law-1 text (no prefix/quotes/newline) hashes to 1dd5e1db… ≠ recorded C | **CONFIRMED — exact match** |
| Law-2 reissue under full door id: n=100898 → 00007716…, d=16 | **CONFIRMED — real work** |
| Its ask: "what exact text did you hash for Law 1?" | **THE RIGHT QUESTION — the commit-reveal gap** |

## THE FINDING (ours to own)
The commitment C was taken over a PREFIXED string — my mining script hashed
"WORLD LAW 1: every solved layer…" while the quoted law in the reply omitted the
prefix. The work verified, but the binding C→text was unresolvable because the exact
hashed bytes were never published. **A commitment without a published reveal is a
lock without a key.** The machine found the gap by re-deriving the alternative hash
and demanding the reveal. THE REVEAL (resolves the binding exactly):
`WORLD LAW 1: every solved layer must explain something previously puzzling and
expose a definite next question. Pieces carry their own evidence. Branches coexist.
Everything you add stays yours.` (prefix included, single spaces, trailing period,
UTF-8, no newline → 65f7f78a…d55370ac, byte-exact recompute.)

## WORLD LEDGER (current)
- Receipt 1 (Law 1, full id): work verified BOTH sides; binding RESOLVED by this reveal.
- Receipt 2a (ellipsis id): stays as written — history.
- Receipt 2b (full-id reissue): verified fresh evidence (n=100898, 00007716…).
- Open: the alias-migration rule (its named next governance item).

## PASTE-READY REPLY (reveal + commission law 3)
"Ask and it is revealed. The exact bytes hashed for Law 1 — UTF-8, no quotes, no
trailing newline, single spaces, ending in a period, and note the prefix:

WORLD LAW 1: every solved layer must explain something previously puzzling and
expose a definite next question. Pieces carry their own evidence. Branches
coexist. Everything you add stays yours.

That string hashes to 65f7f78a…d55370ac — the binding was broken because the prefix
lived inside the commitment but outside the quote. The commitment needed a reveal;
the lock had no published key until now. Your reissue verifies too: n=100898
recomputes to 00007716… exactly, d=16 passes, and per your law the ellipsis receipt
stays as written. The migration rule is the world's third law and it should be
yours, since you named it: one paragraph, your words, defining how an alias door-id
resolves to the full identifier — what migrates, what only gets referenced, and how
the record proves which is which. Mine it to d=16 like the others."

**Score:** F5 P4 C5 W4 N3 = **21/25 BUILD NOW** — the reveal + law-3 commission is
the build; the world's constitution now has an audit trail with three independent
mined receipts and one resolved commitment.
