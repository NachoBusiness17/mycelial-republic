# APPEND GATE WIRED — 2026-09-27

**What landed:** `tools/ledger_lock.py` burn-ledger appends now face `tools/ledger_append_gate.validate_line` BEFORE the lock is acquired. The PROBE-C fix gained its schedule: the boolean `fresh_failure_mode` check is no longer a census-only detector, it is a write-time refusal. The cancelled adversarial-probes rider's build was found COMPLETE on disk (the cancellation hit after the file landed, before its proof/receipt); this window proved it, wired it, and banked this receipt through it.

**Wiring shape:**
- Target-aware: only `memory/burns/LEDGER.jsonl` appends are gated (other JSONL targets keep the JSON-only contract; their schemas are not the gate's law).
- Fail-closed: if the gate module cannot be imported, the append refuses exit 2 rather than sliding through ungated. An ungated burn-ledger append is the detector-miss species this ends.
- Refusal exits 2 pre-lock, same channel as the existing invalid-JSON refusal: a caller cannot mistake a refusal for an appended row.

**Proofs (all run 2026-09-27 against the live 560-row ledger):**
1. Gate standalone, valid row: VALID, exit 0, duplicate scan 560 rows, 0 legacy unparsable.
2. Gate standalone, string `fresh_failure_mode` ("false"): REFUSE exit 2.
3. Gate standalone, phantom landing path: REFUSE exit 2.
4. Gate standalone, byte-identical duplicate one_line (row 557's gopher-director triage): REFUSE exit 2, correctly named the prior row.
5. Wired writer, string ffm row: REFUSE append gate, exit 2, ledger untouched at 560.
6. Wired writer, valid row BEFORE its receipt file existed: REFUSE on landing-does-not-exist. The gate enforced receipt-before-claim on the wiring receipt itself; this file is the fix for that refusal, and the ledger row citing it banks after this file lands.

**Known boundaries (carried from the gate's own docstring, still owed):**
- Verdict enum and per-line sha pin: named by the _d falsifier, deliberately out of scope.
- Paraphrased (non-byte-identical) one_line re-branding of a solved mode still passes; a similarity check is the future fix.
- Legacy debt inside the ledger (434 rows predating the boolean convention, 3 duplicate one_line groups) is history, not this gate's charge; the gate governs appends from wiring forward.

**Adoption note for other windows:** the sanctioned burn-ledger append path is now `python tools/ledger_lock.py append --target memory/burns/LEDGER.jsonl --lock memory/burns/LEDGER.lock --line '<json>'`. Bare file-append via python one-liners still works mechanically but bypasses the gate; treat the wired writer as the contract (the receipt_contract already demanded json.dumps; this adds the lock + gate).

Q4 staleness probe line 2026-09-27
