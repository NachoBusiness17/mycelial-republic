# DUEL1_hidden_3_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Adversarial review: COMMON LANGUAGE SPEC v1 (syscall table, failure taxonomy, governor/model boundary, schema laws)

<measurement_conditions>
- **Instrument:** my own reading of the pasted text. I did not recompute the sha256 (`56b93e...ad30`) and did not open the file.
- **Line numbers:** counted by hand from the pasted text, with `# COMMON LANGUAGE SPEC v1` as line 1. They are UNVERIFIED against the file on disk. The quoted bytes are the authoritative citation.
- **Scope:** only this document. Anything that depends on text outside it is marked UNPROVEN.
- **Quoting:** the source uses dashes in some phrases. I quote around them, because the estate law allows plain hyphens only.
</measurement_conditions>

## Ranking summary

| Rank | Defect | Damage if unrepaired |
|---|---|---|
| 1 | Second mutation path: "sole mutator" vs `rib.exec` and an undeclared `state.write` | Stream and covenant integrity |
| 2 | Failure taxonomy is undefined, incomplete and overloaded | Wrong retry behavior, undetectable states |
| 3 | The ISA table violates the schema laws, with no exemption | Law is unenforceable, so the weak-driver guarantee is void |

---

## Defect 1 (most severe): `rib.exec` and `state.write` open a mutation path around the gate

**(a) Name:** Sole-mutator contradiction (undeclared mutation path).

**(b) Clauses:**
- Line 21: `` `commit` — sole mutator of state; content-hash; O_EXCL; **the gate lives here** ``
- Line 13: `` | `rib.exec` | rib_id (content-hash), args (that rib's schema) | {status, receipt_hash, result} | UNKNOWN_RIB, REFUSED, FAILED, TIMEOUT | ``
- Line 44: `every state.write appends raw to event.v1 before`

The table never says whether `rib.exec` may change state. `state.write` appears in no list: not the table, not GOVERNOR-ONLY, not SURFACE-ONLY. Line 16 says "Everything else composes from these or was never a primitive", so `state.write` has no declared home.

**(c) Operational failure permitted:**
1. The gate (CONFLICT via `expected_head`, COVENANT via the fold, dedup via `idempotency_key`) is documented only on `intent.append` (line 12).
2. `rib.exec` has no CONFLICT, COVENANT or `expected_head`. A rib that writes state through `state.write` therefore lands with no head check, no idempotency key and no covenant fold.
3. Two seats running the same rib can double-write. TMR (line 42) cannot catch this, because it applies only to "mill-class" ops, and the document never says which ops those are (UNPROVEN: the document never lists the "Four mill ops" cited in THE LAW).
4. The journal at line 44 then replays whatever raw bytes a `state.write` produced, including covenant-violating ones.

Negative example (permitted by the text): a model calls `rib.exec(rib_id=H, args={...})`, the rib calls `state.write`, and the result is `{status: ok, receipt_hash, result}`. No `seq`, no `head_hash` check and no COVENANT verdict ever existed.

Positive example (what the text should force): the same rib returns a `result`. The model then calls `intent.append` with `expected_head`, and the gate runs.

**(d) Conformance predicate (FAILS now, PASSES after repair):**

> P1: (i) Every operation name appearing anywhere in the document (including `state.write`) is a member of exactly one of {model-facing table, GOVERNOR-ONLY, SURFACE-ONLY}. AND (ii) the document contains a sentence stating that state reaches `commit` only via `intent.append`, or that `rib.exec` does not mutate state.

Against the document as written, (i) fails because `state.write` is in none of the three sets. (ii) fails because no such sentence exists.

**Repair, using only existing vocabulary:**
- Add: "`state.write` in the journaling clause means `commit`."
- Add: "`rib.exec` results reach state only through `intent.append`, which reaches `commit`."

---

## Defect 2: Failure taxonomy with no definitions, holes and an overloaded DENIED

**(a) Name:** Undefined and incomplete failure taxonomy.

**(b) Clauses:**
- Line 11: `` | `store.read` | addr: seq \| content-hash \| {kind, from_seq, limit} | {events[], next_seq, head_hash} | NOT_FOUND, GAP, DENIED | ``
- Line 12: `` | `intent.append` | ... | OK{seq,hash} or DUPLICATE{seq,hash} | INVALID_ARGS, CONFLICT, COVENANT, DENIED | ``
- Line 13: the `rib.exec` row quoted in Defect 1, with failures `UNKNOWN_RIB, REFUSED, FAILED, TIMEOUT`.
- Lines 42-43 and 46-47: "governor commits the majority" and "3 mill failures in one beat → read-only mode".

No sentence anywhere defines any of the 13 codes. The document gives the following structural facts:
- `store.read` takes a three-form `addr` but has no INVALID_ARGS.
- `rib.exec` takes `args (that rib's schema)` but has no INVALID_ARGS and no DENIED. It has only the undefined REFUSED and FAILED.
- `intent.append` has no TIME
