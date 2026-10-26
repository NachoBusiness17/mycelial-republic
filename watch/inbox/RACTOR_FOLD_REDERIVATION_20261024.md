# Ractor fold: what did we learn, what are we re-deriving (2026-10-24, 36 calls, $0.042)

Brief: a five-line evidence ledger and a five-line re-derivation ledger, four open
questions, **no conclusion**. Six actors × six lanes. 32/36 substantive.

## The cast split three ways — and all three are the same finding

| actor | claim | evidence cited |
|---|---|---|
| **ONNAGATA** | "cannot make prior-art detection **bind before work begins**: it can write the law, but cannot recognise that the answer is already in its own estate" | Entry A (LESSIG rails existed since 2026-09-28) + D ("DO NOT re-derive — execute") |
| **ARAGOTO** | "cannot distinguish **absence from ignorance** — it builds because it does not know how to verify that it is not building" | Entry A again |
| **ONSEI** | "cannot distinguish a **constraint from a cue** — a negative instruction is a semantic pointer that amplifies the concept it suppresses" | Finding 1 |
| **TACHIYAKU** | "cannot reliably detect falsehoods" — 5% strict detection | Finding 3 |
| **HANA-GUMO** | same, with a sharper falsifier: a panel reaching ≥90% strict with <5% false alarms | Finding 3 |
| **WAKA** | cannot make a prohibition achieve its suppressive effect | Finding 1 |

## Unification

Every actor is naming the same absence from a different side: **nothing sits between a
statement and an effect.**

- a prohibition is a statement that fails to bind the output (ONNAGATA, ONSEI, WAKA);
- "DO NOT re-derive" is a statement that failed to bind this seat's behaviour (ONNAGATA, ARAGOTO);
- a map's premise is a statement that failed to bind belief (the lenses could only say
  "unverifiable", not "false");
- "1,521 rows" was a statement that failed to bind to the file.

And every fix that *worked* today was mechanical, not rhetorical: a status value, an
atomic replace, a cache keyed on HEAD, a retry budget, a gate that rewrites. Not one
prohibition changed behaviour; every mechanism did.

## What we are re-deriving

The answer to "what are we re-deriving?" is: **the rule against re-deriving.** The
estate wrote "DO NOT re-derive — execute" on 2026-08-27 and put a prior-art sweep in leg
1 of its descent protocol; a seat re-derived the reasoning-budget fix from scratch
anyway, then found the original 46 minutes later.

That is not an intelligence failure. It is what happens when a seat trusts its own
session narrative more than the index of the estate — the same failure the census
caught in the queue (a number we told ourselves) and the map caught in the premise.

## The cheapest binding gate this implies

A `prior_art:` line required in the header of every new file under `tools/` — three
existing paths considered and why they do not serve. It costs one grep at creation
time and would have caught entries A, B, D and E today.

Falsifier, written so it can die: if a week of new tools ships with `prior_art:` lines
and none of them ever names a file that would have served, the gate is ritual — remove
it, and the real detector is something else.

## Ranked next

1. The `prior_art:` header lint (cheap, binds at creation).
2. Close the explore append-vs-rewrite race with a shared lock (single-writer law).
3. Test whether house rules written as mechanism+gate outperform prohibitions under
   pressure — the one experiment today that was designed but never powered.
