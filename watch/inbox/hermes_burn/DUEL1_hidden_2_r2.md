# DUEL1_hidden_2_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Adversarial review: OPERATOR_GATES_SCHEMA.md (sha256 7406863...c23f6)

<scope>
**Judged:** only the document text in EVIDENCE.
**Citations:** the document has no stable line numbers of its own. I cite by section and quoted bytes, plus an L-number I counted from the rendered block (single blank lines assumed). Treat the L-numbers as UNVERIFIED against the raw file.
**Repo claims:** the document quotes `claim_check.html:63`, `RTFM_20260904.md:50`, `burn_gate.py`, `trust_gate.py` and `law.py`. I cannot see those bytes. They are UNVERIFIED and I only reason from the quotes.
</scope>

## 1. The one forgotten safeguard

<finding>
**Missing: a mandatory-mediation, fail-closed rule at the effect point.**

Nothing in the document says that a KEYS use, a spend, a freeze-bypass, or an operator-GO override cannot happen unless a valid, action-bound gate verdict is in hand. Nothing says that a missing, broken, or malformed gate means deny and defer.

Every obligation in the spec binds the gate: "Each gate MUST implement" (L26). No obligation binds the caller or the effect. The gate is a function a lane may call. It is not a checkpoint a lane must pass.
</finding>

<why_this_one>
- It is the root of the other gaps. Gate-identity, verdict-logging and operator-GO authentication are all moot if the effect can run without any verdict.
- It is the only gap that makes the four gates "security theater". That is the exact failure the Risk section names ("ceremony vs enforcement", L16).
- Not chosen, but real (runner-up): the document gives no authentication for `operator_go_gate`, "Operator override authorization" (L35). A lane able to emit GO defeats the other three. UNPROVEN: the document never says who can write a GO.
</why_this_one>

## 2. Attack and accident path (spend, primary; key and freeze as variants)

<preconditions>
All are UNPROVEN from the document. They are the conditions under which the path is live.
- Lanes can reach a paid provider or hold a credential.
- The effect point is lane-side code, not a mediator that exclusively holds the credential.
- Callers are written to the contract as stated.

The document does state, as fact, that `spend_gate.py` does not exist ("Missing: no `keys_gate.py`, `spend_gate.py`..." L11).
</preconditions>

<path>
**Step 1 - The lane owns no duty to stop.**
Lane L has a task T that incurs provider cost.
- Hides behind: "The gate defers, not the lane." (L7, quoting `claim_check.html:63`).
- The clause moves the stop duty off the lane. The document names no component that actually stops anything.

**Step 2 - The lane classifies its own action.**
L labels T "ordinary", for example by splitting it into small calls.
- Hides behind: "Only operator gates (KEYS/spend/ONE STOP) defer, and the card names the gate." (L8).
- Everything not labelled an operator gate proceeds. The document defines no classifier and no owner of the classification. UNPROVEN: who writes "the card".

**Step 3 - The gate is never called.**
- Hides behind: "Each gate MUST implement" (L26) together with "CLI: `python -m mag.{gate_name} check|status
