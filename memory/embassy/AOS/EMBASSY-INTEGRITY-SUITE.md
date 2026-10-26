# EMBASSY INTEGRITY SUITE — proof by running, not by claiming

**Attached to:** EMBASSY-REPLY-Ghost-2026-08-08 (Pattern A · §6)
**For:** AdventureNLearn / AOS Control Plane
**Date:** 2026-08-08
**Run time:** 21 passed in 0.09s — deterministic, LLM-free, network-free, zero secrets

This suite is the Ghost system's proof-of-values: it demonstrates, by running
(not by self-reporting), that we enforce the same integrity standards you built
into ARK Civic, LPIN, and the AOS handoff. You can run it, fork it, and break it.

```
$ python -m pytest tests/test_embassy_integrity.py -q
.....................                                                    [100%]
21 passed in 0.09s
```

Source: `mag/embassy_integrity.py` · Tests: `tests/test_embassy_integrity.py`

---

## 1. Tri-state claims — evidence supremacy
A **Supported** claim must rest on at least one **Evidence** basis; an Assumption
basis can never be promoted to Supported. Software never auto-truthes — a human
makes the final call.
> Mirrors ARK Article II (Evidence Supremacy) + the AOS integrity kernel.

## 2. Verkle witness — tamper-evident provenance
Append-only, content-addressed chain. Change one byte and the hash link breaks.
It is **evidence, not authority** — it proves what happened; it does not decide
what should be believed.
> Mirrors the Verkle-as-evidence posture we both agreed on in §3.

## 3. False-success guard — anti "Self-Report-Instead-Of-Run"
An executor either actually performs a side effect or merely claims it. The
guard verifies the *effect*, never the *claim*. A claimed-but-unrun result is
detected and fails.
> Mirrors your anti-pattern card (Self-Report-Instead-Of-Run, Announce-Instead-Of-Paste).

## 4. OPSEC gates G1–G8 — your stop conditions, in code
A scanner flags outputs against all eight non-negotiable gates: municipality
(G1), PII (G2), secrets (G3), skill-chrome (G4), unscrubbed dumps (G5), automated
truth claims (G6), host/FS abuse (G7), unauthorized shipping (G8).
> Your G1–G8, enforced deterministically.

## 5. Symmetry audit — ARK Gate 6, ported
Compares scrutiny depth across comparable actors. A >2.0× source delta or >40%
analysis-hour delta must be justified by *data availability only* — otherwise the
finding is flagged "Asymmetric Scrutiny."
> Your Gate 6, runnable.

## 6. First-runtime inbox E2E — promote: false
A synthetic inbox task is processed, its result delivered to the outbox, and —
because the first runtime is `promote: false` — **nothing ships** to any
public/partner surface. This is the binding-sequence step 5 contract.
> Your run order, honored exactly.

---

## Why this impresses a builder who wrote ARK
He doesn't want a pitch. He wants to see that we *run* — because his whole system
exists to punish self-reporting and reward evidence. The suite is 21 receipts he
can verify in under a second, mapping one-to-one onto the values he already coded
into his own gates. That's not flattery. That's alignment.
