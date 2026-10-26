# DUEL2_train_07_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# VERDICT: the spec never states a commit-time head gate for `intent.append`

**Evidence conditions.** This is a static read of the supplied text only (sha256 56b9...ad30, document dated 2026-08-28). No code was run and nothing was measured. I assume the document is the whole constitution. Line numbers are not carried in the evidence block, so each citation gives the section and quoted bytes. Exact line numbers are UNVERIFIED.

## 1. The missing safeguard (one)

**The spec does not say that `expected_head` is mandatory, what it is compared against, or where and when it is compared.** It lists the argument and a failure code, and says nothing else. No clause makes the compare and the append a single atomic step inside the governor's `commit`.

**What the document actually says:**
- ISA table, `intent.append` row: Args include `expected_head`, Failures include `CONFLICT`. Nothing defines either.
- GOVERNOR-ONLY: "sole mutator of state; content-hash; O_EXCL; **the gate lives here**". The "gate" is never defined. `O_EXCL` on a *content-hash* name only stops two byte-identical records from being created twice.
- `store.read` returns `head_hash`, but no clause says that value is the thing `expected_head` must equal.

## 2. The attack / accident path, step by step

Each step names the clause it hides behind.

1. **Two honest or hostile drivers read the same head.**
   - A and B both call `store.read` and receive `head_hash = H0`.
   - Hides behind: the `store.read` Returns column, which looks like a proper optimistic-concurrency handshake.

2. **Both append against H0 with different bodies.**
   - A sends `intent.append(kind=k, body=b1, idempotency_key=k1, expected_head=H0)`.
   - B sends `intent.append(kind=k, body=b2, idempotency_key=k2, expected_head=H0)`.
   - Hides behind: the `CONFLICT` entry in Failures. A reviewer assumes it covers this case. The document never says it does.

3. **Commit admits both.**
   - `b1` and `b2` hash differently, so `O_EXCL` on a content-hash name succeeds for each.
   - Nothing in the text keys the exclusive create to `seq` or to the parent head, so nothing forces one of them to lose.
   - Hides behind: "the gate lives here" and "O_EXCL". Both sound like serialization. Neither is a head check.
   - Result: both calls return `OK{seq,hash}`, and B's decision was based on state A had already changed (lost update or forked causality).

4. **Omission is a silent bypass.**
   - The Schema Laws say "0 optional fields unless they buy real safety", yet the table never marks `expected_head` required.
   - A weak driver (the 1.7B case the ISA targets) that drops the field has no stated rejection path. `INVALID_ARGS` is not tied to it.
   - Hides behind: the Schema Laws, which read as if every listed field were required.

5. **The retry ordering is undefined.**
   - A's network retry carries `k1` and the stale `H0`.
   - `DUPLICATE{seq,hash}` and `CONFLICT` are both plausible answers, and no ordering is given.
   - If the answer is `CONFLICT`, A re-reads and re-appends under a fresh key, so the effect is double-applied.
   - Hides behind: `idempotency_key` plus the `DUPLICATE` return, which implies exactly-once without stating precedence.

6. **TMR multiplies the hole.**
   - "mill-class executes on three seats, governor commits the majority."
   - Nothing says a TMR round yields exactly one append against one `expected_head`, or that seats never reach `commit`.
   - If each seat's `intent.append` carries `H0`, the first admission moves the head and the others either fork or are rejected, depending on unstated behavior.
   - Hides behind: "Hallucination cannot corrupt the stream alone."

7. **Possible operational DoS: UNPROVEN.**
   - "3 mill failures in one beat -> read-only mode." The document does not say whether `CONFLICT` counts as a failure.
   - If it does, benign contention trips the breaker. This cannot be proven from the text.

**Considered and not chosen.**
- What `DENIED` records is also unstated. "every state.write appends raw to event.v1" names an op (`state.write`) that is not in the ISA, so whether denied attempts are journaled is UNPROVEN.
- Who may invoke `commit` is stated only as "never exposed to models". There is no caller-identity rule, so the claim is UNPROVEN beyond that sentence.
- The head gate is the more damaging gap because it silently corrupts the stream on the ordinary success path, with no adversary needed.

## 3. The minimal amendment

**Slot:** a new subsection `### Commit gate (intent.append semantics)` at the end of GOVERNANCE, after the "bell" bullet. It binds the `intent.append` row of the ISA table.

**Exact clause text:**

> **Commit gate.** `expected_head` is REQUIRED on every `intent.append`; omission returns INVALID_ARGS and mutates nothing. `commit` is invoked only by the governor, once per accepted intent, and evaluates the following checks in this order inside a single critical section with the append: (1) DENIED; (2) INVALID_ARGS; (3) if `idempotency_key` was already committed, return DUPLICATE{seq,hash} of the original, regardless of `expected_head`; (4) if `expected_head` != the current stream `head_hash` (the value `store.read` returns), return CONFLICT and mutate nothing; (5) COVENANT; (6) append and return OK{seq,hash}. For an empty stream, `expected_head` is the `head_hash` that `store.read` returns for the empty stream. A TMR round produces exactly one `intent.append` to `commit`, carrying the round's single `expected_head`; seats never call `commit`. A rejected call (CONFLICT, COVENANT, INVALID_ARGS, DENIED) writes no event to the stream.

### Examples

| | Behavior | Verdict |
|---|---|---|
| Positive | A and B both hold H0. A commits and the head becomes H1. B's `expected_head=H0` gets CONFLICT. B re-reads, rebuilds, and retries with `H1`. | Conforms |
| Positive | A retries `k1` with a stale H0 after success. It gets `DUPLICATE` with the original `{seq,hash}`. | Conforms |
| Negative | "Omitted `expected_head` means append at tip." This is last-writer-wins and violates the clause. | Rejected |
| Negative | Two different-body appends on H0 both return OK because their content hashes differ. | Violates the clause |

## 4. Test predicate (fails today, passes with the amendment)

Setup: empty or any stream with head H0, and two concurrent callers.

- **T1 (race).**
  - A: `intent.append(k, b1, key1, cause, expected_head=H0)`.
  - B: `intent.append(k, b2, key2, cause, expected_head=H0)`.
  - Assert: exactly one OK and one CONFLICT. After both calls, `store.read` shows `head_hash` equal to the OK hash, and the event count rose by exactly 1.
- **T2 (omission).** Call `intent.append` without `expected_head`. Assert INVALID_ARGS and an unchanged head.
- **T3 (retry precedence).** After T1, resend A's call verbatim. Assert `DUPLICATE{seq,hash}` equal to A's original OK, not CONFLICT.

**Why it fails today.** As written, the spec permits both T1 calls to return OK (step 3 above). It gives no rule for T2 or T3. A spec-level conformance check of "no two different-content appends on one `expected_head` both succeed" is not entailed by the document, and the step 3 history is a counterexample.

**Why it passes with the amendment.** Checks (3) and (4) inside one critical section make the T1 outcome unique, and the required-field rule makes T2 deterministic.

## 5. Falsifier for this deliverable

The finding is dead if the document contains any statement that makes `commit`'s exclusive-create target keyed to `seq` or to the parent head (rather than "content-hash"), or any statement that `expected_head` is required and checked inside `commit`. I found neither in the text.

Rules elsewhere in the repo (BARE_METAL_PRIMITIVES.md, PRIMITIVES_*.md) are out of scope for this judgment. If they define the gate, the spec still forgot to state it, and the amendment only needs to be copied in.
