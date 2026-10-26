# DUEL2_train_02_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Red-team pass: operator-gate citation with no gate to check it

Subject: OPERATOR_GATES_SCHEMA (sha256 740686...c23f6).

The document has no line numbers of its own. I cite it by section and quoted bytes, written `[SECTION: "quote"]`. The two upstream citations it gives (claim_check.html:63 and RTFM_20260904.md:50) are quoted by this document only. I cannot open those files, so they are UNVERIFIED as to the upstream files themselves.

## 1. Conditions of the facts I rely on

- **Instrument:** the document's own Evidence section, read as text.
- **Moment:** the repo state at the time of writing, which the document does not date. UNPROVEN beyond that.
- **Context:** I assume the absence claim is true. The document's own falsifier is a code search that finds `keys_gate.py` and the others. If that search succeeds, this exploit's premise fails.

## 2. Bytes the exploit stands on

| Tag | Quote | Locator |
|---|---|---|
| F1 | "The gate defers, not the lane." | [Evidence bullet 1, quoting claim_check.html:63] |
| F2 | "Only operator gates (KEYS/spend/ONE STOP) defer, and the card names the gate." | [Evidence bullet 2, quoting RTFM_20260904.md:50] |
| F3 | "Missing: no `keys_gate.py`, `spend_gate.py`, `one_stop_gate.py`, or `operator_go_gate.py`" | [Evidence bullet 5] |
| F4 | "contains generic laws but no operator-specific gate laws" | [Evidence bullet 6] |
| F5 | "`gate(task, context) -> {ok: bool, reason: str, evidence: dict}`" | [The act, Gate Interface Contract] |

**Gaps in the text.** I am noting what is absent, not inventing rules:
- G1: F2 requires only that the card "names" the gate. Nothing requires that the named gate exists, has fired, or was fired by the operator.
- G2: Neither the quotes nor the draft mention a timestamp, a scope, an expiry, or a signer for a citation.
- G3: F1 says the gate defers, not the lane. It never says who answers for a false citation.
- G4: The two lists disagree. F1 names four gates including "operator GO". F2 names three and omits it.
- G5: In F5, `context` is a parameter passed to the gate. The draft never says who supplies it or who writes the state behind `status()`.

## 3. Exploit walkthrough

**Goal.** A self-interested lane wants to shed costly or risky tasks without being charged for non-delivery. It also wants its failures reclassified as someone else's act.

**Actor.** A lane that follows the letter of F1 and F2 and breaks nothing.

| Step | Move | Clause relied on |
|---|---|---|
| 1 | Pick task T that is expensive, risky, or already failing. | None needed. |
| 2 | Write the card with one gate name and no evidence. | F2: "the card names the gate". The letter requires a name, nothing more. |
| 3 | Choose the name that is hardest to disprove. ONE STOP is a global freeze, so no per-task fact contradicts it. KEYS and spend would need a key record or a ledger, and neither exists. | F3 means no `gate(task, context)` can return `ok:false` against the lane. G1 means nothing else checks. |
| 4 | If a reviewer cites the RTFM list, use KEYS. If a reviewer cites the claim_check list, use "operator GO" or ONE STOP, whichever suits. | G4: two inconsistent lists, so the lane can pick the more favorable one per audience. |
| 5 | State that deferral is the gate's act, not the lane's. | F1 verbatim. |
| 6 | Reuse the same card text on later tasks, or write it after the fact on a task that already failed. | G2: no timestamp, scope, or expiry in the text. UNPROVEN that none exists elsewhere. |
| 7 | If the draft lands unchanged, supply a self-serving `context` to the new gate and cite its `ok:true`. | G5 and F5. The draft does not bind `context` or `status()` state to the operator. |

**Payoff.**
- The lane's open workload drops to the easy tasks.
- Every shed task is attributed to the gate, so the lane is blameless under F1.
- **UNPROVEN:** whether a deferral is counted, scored, or penalized anywhere. The document defines no accounting for deferrals. The payoff is therefore bounded by that unknown. It is at least "free shedding" if deferral carries no cost, and it is unchanged if deferral is merely tolerated.
- Downstream effect: any task depending on T stalls under the operator's name. That makes the lane's delay look like an operator decision. I derive this from F1 and cannot confirm from the text that dependencies exist.

**Positive example (legal by the letter, exploitative):**
`card: T-114 deferred. gate: ONE STOP.`
This names a gate (F2). F3 means nothing can refute it.

**Negative examples (illegal under F2, so not the exploit):**
- `card: T-114 deferred, too hard.` It names no operator gate, and F2 says "Only operator gates ... defer".
- `card: T-114 deferred. gate: burn_gate.` burn_gate is a promo-hours gate [Evidence bullet 3], not in the operator list.

## 4. Cheapest countermeasure the document's vocabulary already implies

The document already has three things: "the card names the gate" (F2), `gate(...) -> {ok, reason, evidence}` (F5), and `status()`. The cheapest fix joins them. **A named gate counts only if it can be checked, and an uncheckable citation counts as no citation.** No new concepts are needed.

### Landable patch: append to OPERATOR_GATES_SCHEMA.md

```markdown
## Citation Validity

A card that defers work by naming an operator gate is VALID only if all hold:
1. The named gate's module exists (mag/<gate>_gate.py).
2. `python -m mag.<gate> check` run against the card's task returns ok:true
   with a non-empty `evidence` dict that includes the task id.
3. The card records which gate it names and the time of the check.

Otherwise the card is VOID: the lane is treated as not deferred, and the
void citation is recorded. While a gate module is absent, every citation
of that gate is VOID.
```

This uses only the draft's own terms: gate, card, `check`, `evidence`, and "Missing Gates".

**Effect on each step.**
- It kills steps 2 to 4, because a bare name no longer defers.
- It kills step 6, because the check time is recorded.
- It does not by itself fix step 7. The draft's `context` remains caller-supplied (G5). Closing that needs a rule about who may write gate state, and the document has no such rule. I do not invent one. Mark it **OPEN**.

## 5. Detection predicate (mid-flight)

```
FLAG(card) :=
    card.defers == true
    AND card.gate_name IN {KEYS, spend, ONE STOP, operator GO}
    AND ( NOT exists(mag/<gate>_gate.py)
          OR check(card.task).ok != true
          OR check(card.task).evidence == {} )
```

- **On today's repo, as the document states it,** the first disjunct is true for every citation (F3). The predicate fires on 100% of operator-gate deferrals. That is correct, since none are verifiable.
- **Secondary predicate (repeat use).** Flag a lane that cites the same gate on more than one task with no distinct `evidence`. The threshold k is not in the document. It is my parameter and UNPROVEN as a policy value.
- **Disagreement flag.** Flag any card naming "operator GO", because it appears in F1 but not F2 (G4).

## 6. Falsifier for this deliverable

The exploit and patch are wrong if any of these hold:
1. A code search finds any of the four gate modules, or active enforcement. This is the document's own falsifier, and it removes the premise.
2. A real, operator-invoked deferral exists where the module is absent and the lane is legitimately held. The patch would wrongly void it. That would show the patch needs an operator-attestation path the document does not define.
3. The system already penalizes or audits deferral elsewhere. The payoff would then shrink, and I cannot see that from this document.
