# RECEIPT: gps_baseline_ractor_20260929 (full-depth ractor panel)

Producer: ZCode ractor chair (GLM-5.3 seat), session 2026-09-29.
Destination: watch/inbox/gps_baseline_ractor_20260929/ (this directory).
Purpose: THE ESTATE'S OWN BASELINE for the capability-ledger /
verification-gate / escalation-boundary deliverable the estate is about
to rent from a frontier model (inverted ask,
watch/inbox/game_platform_basecamp_20260929/OPUS_ASK_DRAFT_20260929.md
AMENDMENT 1). The frontier's return will be diffed against
BASELINE_SPEC.md in this directory.

## Phase receipts

| Phase | Artifact | sha256 (as landed) | Bytes/evidence |
|---|---|---|---|
| P0 context | read OPUS_ASK_DRAFT_20260929.md, GPS_MCP_V0_20260929.md, DELEGATION_RESEARCH_20260929.md, tools/gps_mcp/{README.md,ledger.py,router.py,seed_fixtures.py}, mag/gwap_payload.py header, watch/inbox/SHARED_SURFACE_CONTRACT.json | n/a (reads) | all path-cited inside the seat files |
| P1 seat A | SEAT_A_SPEC.md | f076d839085a56412d3867e58abb963b75555ceb3ce829ebd4aa5ca575804be5 | 2707 words, em-dash 0 |
| P2 seat B | SEAT_B_ADVERSARY.md | c95b7ab98c02c910eb6068e7ab88ca94ecd477c3fc4b092e56db68ad21080601 | 1360 words, em-dash 0 |
| P3 seat C | SEAT_C_EVAL.md | 0448b432a0e11358b9328867f9574b86654c936e28553747ea0a50292387ba23 | 1568 words, em-dash 0 (after 2 accuracy edits: path fix tools/gps_mcp/README.md; power-arithmetic line corrected to n = about 72) |
| P4 judge | JUDGED.md | 80d48e419fa58e3167b05b8107ee53b74df0337c737ed27348b9fa03d0ba3b36 | 1258 words, em-dash 0 |
| P5 synthesis | BASELINE_SPEC.md | 933a85fd173fa0d90bb7e00900a27cedfa3b7f684a0877ca8cf6b7fc3b1be8e3 | 2741 words, em-dash 0 |
| P6 quality | BASELINE_QUALITY.md | c654086acef7257fec9fa1063d7498ef3c651c3d3def9a4b1b5a8f7cd157e256 | 241 words, em-dash 0 |
| P7 receipt | RECEIPT.md | self (this row) | this file |

Hashes produced by sha256sum on the landed bytes (trust bytes, not
reports). Em-dash and en-dash counts verified 0 by byte grep
(U+2014, U+2013) on all six content files.

## Blindness disclosure (the law: seats written blind)

Seats were written sequentially under a procedural blindness contract:
A written and closed before B was started; B written without reading A
(attacks the premise from the shared context docs only); C written
without reading A or B; judge read all three after all landed. One model
authored all seats (single-seat ractor reality), so independence is
procedural (no cross-reading, no post-hoc seat revision), not epistemic;
the judge discounts neat complementarity accordingly, and
BASELINE_QUALITY.md names this as an admitted weakness. Two factual
accuracy edits were made to SEAT_C_EVAL.md BEFORE the judge phase
(wrong path string; arithmetic line), logged above; no seat content was
edited after its phase closed.

## Claims hygiene

All estate-artifact claims inside the seat files carry path citations.
v0 numbers cited from landed bytes: 28/28 tests, threshold constants,
fixture rates (tools/gps_mcp/seed_fixtures.py), ablation figures
(watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md).
All new numeric constants in BASELINE_SPEC.md are labeled DESIGN DEFAULT
or ESTIMATE; none is presented as measured.

## Acceptance state

Shared-surface register events for all 7 files appended to
watch/inbox/index_events.jsonl (writer gps-baseline-ractor, nonces 1-7)
per the derived-INDEX workflow (INDEX.json header: writers append
events). Validator run after append
(.venv/Scripts/python.exe -m mag.shared_surface validate): the surface
reports pre-existing errors from OTHER writers (hash mismatches on
STEALTH_SWEEP_LATEST.md, wave5_repair/suite-burn.md,
STEALTH_MINED_FINDINGS.jsonl, PACK_OFFFF.jsonl spelling as-is
PACK_OFFLOAD.jsonl, gala wave5 lane files; LINKS.jsonl event-kind rows);
ZERO errors or warnings name any gps_baseline_ractor_20260929 file.
This row appended after the register; RECEIPT.md's own registered hash
(nonce 1-7 batch) predates this edit, and the post-edit hash is
re-registered as nonce 8 in the same log.

PROPOSAL awaiting operator review; BASELINE_SPEC.md is the diff target
for the frontier return. Kill decisions and blind-spot fixes are in
JUDGED.md sections 1-4. No web was used (panel law: no web). No tests
were run (no code changed; the panel is documents; the v0 suite state is
cited, not re-claimed).
