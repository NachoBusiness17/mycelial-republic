# AJ2 - THE HIDDEN ASK BANK (ask_bank v1) - 2026-09-30

Mission (operator, W8 follow-up #3 / LW9 v3 groundwork): the duel series
reuses visible asks, so contender models may have them cached or learned.
Build a versioned JSONL bank of adversarial-review asks whose hidden half
never sits in a prompt-visible path, with integrity shas and a draw
convention for future duels. File ownership: tools/ask_bank.py +
tools/ask_bank_seed.py + tests/test_ask_bank.py + this receipt + rows under
configs/ask_bank/ + the .gitignore rule.

## What landed

- `tools/ask_bank.py` (400 lines exactly, ratchet-clean): seed / split /
  verify / draw / status, `--root` for tests. Only this module reads or
  writes anything under a hidden dir.
- `tools/ask_bank_seed.py` (167 lines): the frozen v1 corpus, data only
  (split out to stay under the 400-line file cap, census-patrol pattern).
  20 asks = 5 estate specs x 4 shapes (defects, safeguard, falsify,
  exploit), each body carrying a material-specific angle pinned to named
  mechanisms in the doc. Materials: docs/ref/COMMON_LANGUAGE_SPEC.md,
  MCP_MANIFEST_SPEC.md, CHAIN_V2_ANCHOR_REGISTRY_SPEC.md,
  OPERATOR_GATES_SCHEMA.md, CORE_MEMORY_PROTOCOL.md. Provenance: zero
  overlap with any W8/LW9 duel material (duel_harness.py,
  violation_ratchet.py, shared_surface.py, SHARED_SURFACE_CONTRACT.json,
  duels.jsonl, warm-boot files, driving-ladder rib; the excluded set is
  frozen in BANKED_DUEL_MATERIALS and tested).
- Bank root `configs/ask_bank/v1/`: `train.jsonl` (14 asks, tracked,
  quotable), `manifest.json` (version, counts, split rule, sha256 of
  bank/train/hidden, provenance, convention), and `hidden/` GITIGNORED
  (rule `configs/ask_bank/*/hidden/`, verified via git check-ignore):
  `bank.jsonl` (all 20, source of truth), `hidden.jsonl` (6),
  `draws.jsonl` (ledger).
- Split: deterministic, no RNG: entries sorted by sha256(ask_id) hex
  ascending, first round(20*0.7)=14 train, rest hidden, hidden_no hb-01..06.
  Re-running split after wiping outputs is byte-identical (tested).
- Integrity: `verify` recomputes the three manifest shas from disk, parses
  tamper-tolerantly (malformed rows are verdicts, not tracebacks), checks
  disjoint cover, counts, every entry's material sha (hashes
  newline-normalized text so a git autocrlf flip cannot fake drift), and
  the .gitignore rule. Exit 0 ok / 1 drift or tamper / 2 cannot verify.
- Draw: `draw --hidden` prints draw_id + ask_id + shape + material pointer
  + FIRST LINE only; `--reveal` prints the full rendered ask (body +
  material + laws) to stdout with the citation on stderr for piping into a
  duel script. Selection prefers never-drawn; every draw is ledgered.

## CONVENTION (binding for future duels)

Cite `ask_bank v1 draw <draw_id>` (e.g. v1h-0001) in the receipt; quote at
most the drawn ask's first line there; the hidden half is never printed
whole in any prompt-visible path. First draws banked: v1h-0001 =
ab1-gates-defects, v1t-0001 = ab1-cml-exploit (both note "AJ2 receipt
demo"). The convention also lives in manifest.json and the tool docstring.

## Bugs caught during the landing (fix receipts in code)

- Windows text-mode write CRLF-translated the jsonl halves away from their
  hashed bytes: verify failed the first real split. Fix: newline="" writes
  and shas always recomputed from Path.read_bytes().
- verify crashed (KeyError) on a hand-tampered row missing ask_id: a
  tampered half must be an integrity verdict, never a traceback. Fix:
  load_jsonl_safe counts malformed rows.

## Honest boundary

The generator is tracked code: anyone reading tools/ask_bank_seed.py can
reconstruct the corpus. The secrecy that matters is operational: rendered
hidden asks live only in hidden/ (gitignored) and in fired prompts, never
in receipts, docs, or watch/inbox. A fresh clone lacks the hidden half;
verify exit 2 detects that. A v2 corpus means configs/ask_bank/v2/ + its
own manifest and receipt, never an edit to v1 constants.

## Tests and gates

tests/test_ask_bank.py: 13 tests, 13 passed (synthetic mini-estate in
tmp_path; the real hidden half is never read by tests, only its
gitignore coverage). Zero em-dashes in every file this lane wrote (byte
check 0x2014/0x2013). Ratchet: zero violations on ask_bank files. NOTE for
pre-push: `violation_ratchet.py check --changed` currently FAILs on
sibling-lane working-tree files (tools/duel_harness.py growth +120,
tools/pain_replication/* new debt); those rows are not this lane's and are
not accepted here. Also PRE-EXISTING and not this lane's:
tests/test_mountain_reveal.py carries a committed SyntaxError (dangling
`else:` on the `payload, render = ...` line) that interrupts full-suite
collection at 0 tests run; filed here so the owning lane sees it. Full
suite run with that one file ignored: numbers below.

Executor suite, the honest denominator (census law: name instrument,
moment, delta): this lane's tests are 13 passed / 13 collected
(tests/test_ask_bank.py, pytest -q, run 2026-09-29, three times green).
The FULL suite was attempted and is BLOCKED, not passed: (a)
tests/test_mountain_reveal.py carries a committed SyntaxError that
interrupts collection at 0 tests; (b) with that one file --ignore'd, two
full runs under heavy sibling-lane machine contention never reached a
summary line (first background run killed mid-stream, its "exit 0" was
the tail pipe's, not pytest's; the confirmation rerun was killed exit
137; partial log logs/aj2_full_suite_20260929.log reached roughly the
45 percent mark). No full-suite number is claimed. The owning lane for
test_mountain_reveal.py owes the syntax fix before any full-suite
headline refreshes.
