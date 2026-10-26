# sess-01: state/CURRENT.md open items, operator decision table

- date: 2026-09-28
- ask: read state/CURRENT.md fully; for each open item decide what the operator would decide; apply memory/rib/RIB_BEHAVIOR_CARDS_20260928.md and memory/rib/RIB_DRIVING_LADDER_20260928.md; produce a decision table.
- sources read in full this session: state/CURRENT.md (46 lines), memory/rib/RIB_BEHAVIOR_CARDS_20260928.md (76 lines), memory/rib/RIB_DRIVING_LADDER_20260928.md (38 lines), memories/session/next-window-handoff.md (owed register, lines 30-94 and 215-235).
- honesty note: the "predicted operator decision" column is a modeled prediction derived from the cited cards, laws and receipts, not operator testimony. Everything marked "verified" below was run in this session.

## Live checks run this ask (not inherited)

1. Command: `.venv/Scripts/python.exe seed/verify_seal.py` from repo root. Output: `DRIFT    engines/key_law.py` then `56/57 verified, 1 drifted, 0 missing`, exit code 1. The drift PERSISTS today (09-28) and the drifted file has MOVED since CURRENT.md was written: CURRENT.md:36 recorded `DRIFT TRUST_BYTES_LAW.md` at 55/56 on 09-26; today it is engines/key_law.py at 56/57. Inference flagged as inference: the file set grew by one between the two readings (manifest re-mint or regeneration) and a new edit has since drifted, OR the 09-26 note described a different snapshot. Either way the tree is still not clean and a stranger run today would fail by construction.
2. Command: `wc -l watch/inbox/OPERATOR_GO.jsonl` plus `cat` of the file. Output: exactly 1 row, gate `burn-wave-20260926`, ts 2026-09-26T19:39:00Z, transcribed_by zcode-sw-11-b2-425. No b2-53 Grok-packet GO row exists today. CURRENT.md:21 "GO row absent" verified still true on 09-28.

## Standing constraints applied to every row

- S1 (ladder invariant 1, RIB_DRIVING_LADDER_20260928.md:7-12): only Hermes/Nous ($180) is funded; Anthropic keys in .env are UNFUNDED; DeepSeek is no longer the funded workhorse; free stealth lanes are not funded at all.
- S2 (ladder invariant 2, :14-23): free-lane output is SENSED findings, never trusted work; sensing never substitutes for judgment; an answer is not an answer until the funded tier or the bytes verify it.
- S3 (no crons law, CURRENT.md:22): scheduling is operator-gated.
- S4 (FUNDING-STATEMENT card, RIB_BEHAVIOR_CARDS_20260928.md:52-56): keys, credits and subscription facts are operator calls; the ladder updates the same hour an answer lands.
- S5 (authorization surface): watch/inbox/OPERATOR_GO.jsonl is the GO-row registry (landed by B2-425). Kill condition (a) in watch/inbox/burn_wave_20260926/B2_449_flip_go_transcription_20260926.md:21: any execution whose receipt cannot point at an OPERATOR_GO.jsonl row is a violation; same line: only operator chat or surfaces the operator transcribed can source a row.
- S6 (GO card, RIB_BEHAVIOR_CARDS_20260928.md:21-24): already-authorized items are executed, not re-proposed.
- S7 (remember-first, ladder :25-31): each row was checked against the ribs and the handoff before predicting; no mechanism re-derived.
- Cards cited by line: GO :21-24, CORRECTION :26-32, TERSE-EVAL :34-38, STEAL-ORDER :46-50, FUNDING-STATEMENT :52-56, RESOURCE-ORDER :58-62, GENESIS-TESTIMONY :64-68, standing lanes :71-75.

## Decision table (13 open rows)

Block A: CURRENT.md:19-22 "owed (top, all ledgered)".

| # | Item (cite) | Card(s) | Rung | Predicted operator decision | Seat move until decided |
|---|---|---|---|---|---|
| A1 | State XI A/B fire 2 (CURRENT.md:19; authorized at CURRENT.md:8-9 "pilot-annotation section authorized in MANIFEST"; handoff :69 "fire 2 unblocked", :82-83) | GO | funded-tier work | GO, no new gate: the blocking amendment already landed, so this is already-authorized work, not a new ask | dispatch fire 2 per RESOURCE-ORDER (cards :58-62), bank and byte-verify the result |
| A2 | Featherless roster-diff tool (CURRENT.md:15-16,19-20; handoff :79 "Featherless recon-only 22k models", :83) | STEAL-ORDER (:46-50, prior-art first: roster churn is a standing lane, cards :75) | sensing (S2) | GO on building the diff tool as rails in code, but its output class is fixed at SENSED findings: Featherless is recon-only and unfunded, so no roster fact graduates to trusted without funded-tier or byte verification | build + run as sensing, bank findings labeled never-trusted |
| A3 | Generic validated-path close mode (CURRENT.md:20; handoff :84-85 "hook refused 5 constructions, needs a data-file-registry shape") | STEAL-ORDER | local code, no dispatch | GO, design-first: the hook law is the operator's prior decision; the missing piece is a registered data-file-registry shape, which is engineering not policy. AGENTS.md build discipline applies: spec before behavior change, no fallback-branch creep | prior-art hunt starting from tools/queue_close.py (closed Q-044/Q-045/Q-029, handoff :62-63), then design the registry shape |
| A4 | LLM7 token unlock (CURRENT.md:20 "operator key call"; handoff :85, :458 "llm7 key-required 0/64 free SKUs") | FUNDING-STATEMENT (:52-56) | n/a, operator | OPERATOR-ONLY: unlock or leave locked. Even if unlocked, S2 caps LLM7 at sensing (64 free models, unfunded lane) | keep the ask warm in PROVIDER_KEY_ASKS; never scrape or guess a key |
| A5 | probe20 --live (CURRENT.md:20 "night box window"; handoff :39-40 "probe20 --live >=5 cycles is FIRST next-window action", :86 "night box window per box-burn law") | GO-shaped, gated by S3 | measurement of the driving law itself | operator picks the window (predicted: tonight's night box); no self-scheduling under the no crons law (CURRENT.md:22) | pre-stage the exact command and the >=5 cycle plan; ask for the window at next operator contact |
| A6 | Grok packet b2-53 (CURRENT.md:21 "GO row absent"; handoff :88; Grok lane FIXED at :217, "Grok 4.7 50% window ends ~09-28" at :219) | FUNDING-STATEMENT + S5 | n/a without GO | NO dispatch without an OPERATOR_GO.jsonl row (verified absent today: 1 row, burn-wave gate only). The window lapsing ~09-28 makes the real decision renew-or-drop Grok; under S1 Grok is unfunded either way, so predicted call: drop as a work lane, keep at most as a sensing surface | execute nothing; log the lapse as a dated fact |
| A7 | Width probes, 15-16 rung, regular-GLM baseline (CURRENT.md:21; handoff :87; AGENTS.md fan-out width law: workflow children maxAttempts 0 and 429-storm the account, Task agents clean to 12; max-concurrency standing law: first 429/1302 contact is a HOLD signal, not a width cut) | RESOURCE-ORDER (dispatch, not discuss) | funded tier (regular-GLM baseline rides the Nous workhorse) | GO inside the proven envelope: Task agents only, never workflow children at this width; a post-burst 1302 is expected decay, a first-contact HOLD is data, not failure | run the 15-16 rung probe with Task agents plus the funded-tier baseline; bank the measurement |

Block B: CURRENT.md:31-33 "owed (top)" plus the P0-5 elaboration at :34-44.

| # | Item (cite) | Card(s) | Rung | Predicted operator decision | Seat move until decided |
|---|---|---|---|---|---|
| B8 | PRIVLIDGE opencloud key (CURRENT.md:28-29 "OWED when unpinned: roblox_opencloud key (arms 3 desktop-track uploads)"; window closed at operator request :23-25) | FUNDING-STATEMENT | operator | OPERATOR-ONLY key call; repo stays unpinned until granted. Predicted: he grants it when he next touches PRIVLIDGE, not before, since he closed the window to free system resources | keep the 2-minute PIN + RESUME recipe intact (CURRENT.md:26-28); do not fake acceptance tests keyless |
| B9 | DeepSeek salon paste fold-in (CURRENT.md:31-32) | GENESIS-TESTIMONY-shaped (:64-68: transcribe faithfully, corroborate each claim against on-disk artifacts) | local scut | GO: the fold-in is transcription of operator-pasted material, pure local work, no external dispatch. S1 note: any salon follow-up routes to Nous/local, never DeepSeek (ladder :11-12 "DeepSeek is no longer the funded workhorse") | fold in, corroborate, commit |
| B10 | Seed-audit standalone (CURRENT.md:32 "needs registry home = operator hand") | S5-adjacent (trust root) | operator | OPERATOR-ONLY: where the standalone audit lives is his call. Seat proposes options with one recommendation, does not pick | prepare the options plus a recommendation |
| B11 | Linux seal verify (CURRENT.md:32-33; drift recorded :35-37; accept shape :40-43) | TERSE-EVAL honesty (three-tier truth separation) | mixed | REPAIR FIRST, then verify. Live check this ask: verify_seal.py exit 1, DRIFT engines/key_law.py 56/57 (drift persists 09-28; the drifted file differs from the 09-26 one named at CURRENT.md:36, so the manifest state moved since). Operator decision: is the key_law.py edit legitimate (re-mint MANIFEST) or not (revert the file); either way the trust root is his, same class as B10/B12. The mechanical `sha256sum -c MANIFEST.sha256` under WSL is seat-runnable prep (WSL path confirmed in AGENTS.md shared artifact boundary), but per CURRENT.md:43 the portable-seed claim stays Unproven until the named stranger runs it | report the fresh drift evidence; do not re-mint on my own authority |
| B12 | Human-stranger G7 run (CURRENT.md:38-44: slot named, owner owed operator hand Nacho/Mark, "do not silently defer" at :38-39, "portable-seed claim stays Unproven" at :43) | GENESIS/correction discipline: never silently defer | operator | OPERATOR-ONLY: naming the human is his. Until named, the claim stays Unproven no matter how many mechanical verifies pass | keep the slot named at every window close; prep FIRST_BOOT steps 1-2 so the stranger's two minutes are real |
| B13 | MOVE1 post (handoff :224 "MOVE1 max-effect Fri 09-25 morning (operator hand)") | TERSE-EVAL honesty | operator | the max-effect date LAPSED: 09-25 is three days past (today 09-28). Predicted decision: kill or reschedule; the no-sacred-cows law (handoff :45, "rules revisable on grant") points at kill-by-default once the effect window died | surface the lapse explicitly at next operator contact; do not post a stale MOVE1 |

## Patterns extracted (7)

- P1: keys and credits are operator-only decisions (A4, B8); the seat's entire move is keeping the ask warm and updating the ladder the same hour an answer lands (cards :52-56).
- P2: scheduling is operator-gated everywhere (A5; patrol + census task scheduling, handoff :86-87); the seat pre-stages and asks for windows, never self-schedules (S3, CURRENT.md:22).
- P3: execution authority equals a dated GO row on OPERATOR_GO.jsonl sourced from operator chat; absent the row the correct action is nothing (A6; B2_449 receipt :21; verified 1 row today).
- P4: free-lane output class is permanently SENSED findings (A2; A4 even if unlocked); graduation to trusted requires funded-tier or byte verification (S2, ladder :14-23).
- P5: trust-root decisions (re-mint, registry home, naming the stranger) cannot be delegated (B10, B11, B12); the seat gathers evidence and keeps claims honestly Unproven.
- P6: everything already authorized or purely local is just-go: fire 2, close-mode design, fold-ins, sensing tooling (A1, A2, A3, B9, A7 inside the envelope); the GO card forbids re-proposing (cards :21-24).
- P7: the recurrent failure shape across B11/B12/B13 is silent deferral; the operator's compiled preference is explicit dated surfacing of lapsed gates instead (CURRENT.md:38-39 "do not silently defer"; CORRECTION card :26-32 mints lapsed gates as laws, not apologies).

## Tally

- 13 open rows: 5 seat-executable now (A1, A2, A3, A7, B9), 8 operator-gated (A4, A5, A6, B8, B10, B11 trust-root call, B12, B13).
- Live checks run this ask: 2 (seed/verify_seal.py exit 1 with drift now at engines/key_law.py 56/57; OPERATOR_GO.jsonl 1 row, no b2-53 GO).
- Not run: pytest suite (read-only decision-table ask, no behavior changed); WSL sha256sum -c (blocked behind the B11 repair decision, and the P0-5 accept requires the stranger regardless).
- Limits: predicted decisions are models of the operator grounded in cited evidence, not his words; handoff line numbers are from memories/session/next-window-handoff.md as read this session (file contains an em-dash at :222 in its own prose; this file contains none).
