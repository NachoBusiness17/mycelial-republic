# DESCRIPTION TRI-STATE - the fleet's own saved workflow metadata vs its run receipts

Written 2026-10-02 by the cross-drop lane (gala ouroboros, division B).
Method: drop-dig's tri-state law (claims vs bytes) pointed at the fleet's own
metadata. Every claim below was checked against bytes this session; raw command
output: `watch/inbox/gala_20260925/ouroboros/lanes/cross-drop.check.txt`
(sections C1-C20, moment 2026-10-02T12:33:30Z, HEAD a92cef8dd).
The 18 saved workflows live in `.zcode/workflows/*.dwf.ts`. Verdicts: TRUE
(bytes back the claim), FALSE (bytes contradict it), PARTLY (some lanes or
numbers hold, others do not), UNVERIFIED (no estate surface binds the number).

## The headline finding

The estate tri-states strangers' briefs but never its own saved metadata.
`.zcode/` is gitignored (`.gitignore:198`; only `the-gala.dwf.ts` is tracked,
C8), so saved workflow descriptions are invisible to citation_lint
(`--changed` over tracked files), to the violation ratchet, and to ERRATA 001's
carrier census (which grepped tracked files only). Proven live: the 191.8M
phantom that ERRATA 001 struck in STORY.md:240 and SKILL.md:50 is still riding
in `olm-mine.dwf.ts`'s saved description (C7). Second proof: `gap-analysis.dwf.ts`
carries a gap-analysis header on a mickey17-v2 body and nobody noticed (C1).

## The description-lie table

| workflow | claim in saved description | verdict | bytes that rule |
|---|---|---|---|
| olm-mine | 8 areas x 4 sources (arXiv, HN, Reddit, X) | TRUE | script: SOURCES = 4 doors (line 116), "exactly 8 areas" (line 230); 20260928 run banked exactly 32 sweep .md = 8 areas x 4 sources (C5) |
| olm-mine | confirmers re-fetch the top 24 finds | TRUE | CONFIRM_CUT = 24 (lines 109, 321) |
| olm-mine | 32/32 miners, 21/24 confirmed | TRUE | 32 sweep files on disk; register.jsonl 21/21 rows parse; receipt: "32-return mine (21 confirmed finds, 3 unconfirmed items)" (frontier_olm_20260928/RECEIPT.md, C6) |
| olm-mine | "Provenance: 191.8M-token run 2026-09-29" | FALSE (struck phantom, still live) | ERRATA 001: "the 191.8M-token mine headline is a phantom; STRUCK" (48h_synth/ERRATA.md:9); zero "191" hits in the named DIGEST.md (C7); no frontier_olm_2026-09-29 bank folder exists; the run is the 20260928 slug, folded/rewritten 2026-09-29 |
| olm-mine | workflow_gate PASS digest 2487787e949f | TRUE | REGISTRY.jsonl row 2026-09-30T01:18:10Z, name frontier-olm-mine.dwf.ts, PASS (C9) |
| gap-analysis | 15 auditors / 15/15 lanes | TRUE at archive, with a coverage nuance | 15 lane jsons a01-a15 on disk (run slug suffix -15 = 15 targets); but the register itself merged only 8 siblings at its 18:30Z poll (GAP_REGISTER.md:13-14, 237); a09-a14 landed 18:45-19:36, after rollup, and never amended the register (C2, C3) |
| gap-analysis | 75 rows | TRUE | 70 parseable rows + 5 inside a01-olm-day2.json (present but malformed JSON, parse fails at line 38) = 75 (C2) |
| gap-analysis | tier-2 12/12 | TRUE | deep_tier2 arrays in 5 checks files: 12 verdicts, all "verified" (C2) |
| gap-analysis | "Pass slug for the register folder" (args: period, slug) | FALSE - wrong-body workflow | body reads args.topic/args.targets/args.width (lines 85-108) and throws "no targets passed" (line 110) when fired with its documented args; LANES root memory/runs/mickey17_v2 (line 91); LANE_SYS says "MICKEY-17 v2.1 frontier-steal burn" (line 114); fold gate tools/mickey17_v2_fold.py; publishes MASTER_MICKEY17_V2.md; 40 diff lines vs mickey17-v2.dwf.ts (C1) |
| gap-analysis | (implicit) gate-registered | FALSE | zero REGISTRY rows for gap-analysis under any name (C17) |
| game-digs x5 | 30 parallel diggers | TRUE | 30 briefs per vein (GAMES_BRIEFS_*.json all length 30); one digger per brief (C10) |
| game-digs x5 | producer-side shrink() on every report site | TRUE | 3 report sites per script, all wrapped report(shrink(...)); 4th grep hit per file is the comment (C10); mtimes Sep 27 07:21 match "PATCHED 2026-09-27" |
| game-digs x5 | verdict clone/reskin/skip, receipt lands in watch/inbox | TRUE | GAMEDIG_<vein>_20260926.md x5 + MASTER ATLAS 20260927; creature-farming receipt tallies 30 findings: 14 clone, 16 reskin (C10) |
| drop-dig | 7/7 lanes | PARTLY | 7 lane jsons fired and landed (adjacent, aida, atlas, lbrain, ownmem, pam, ragos); but the brief named 7 systems + adjacent = 8 lanes, and localmind got no lane and zero receipt mentions anywhere (C11) |
| drop-dig | 14 register rows | TRUE but coverage-blind | signals jsonl = exactly 14 rows; systems = Aida, Atlas, LBrain, OwnMem, RAG-OS + 9 adjacent; NO row for PAM (the run's top finding is receipt-only, the exact disease gap register a07 flagged) and none for localmind (C11) |
| drop-dig | PAM's SHA-256 claim wrong | TRUE | pam.md:18-19: census over sdk/python/pam (16 files): sha256=0, blake3=11, ed25519=19 (C18) |
| drop-dig | forgery passes verify live-proven | TRUE | pam.md:53-54: "strip the signature entirely: verify() with no key returns **True** on the forged artifact" (C18) |
| wide-dig | 8/8 lanes; tweet's 100x deflated to 26.5x measured; neuromorphic LLM negative (370M SOTA) | TRUE | spiking-wide_RECEIPT.md:18,21 "8 of 8", "8/8 lane-JSON parse on its corrected rerun"; energy-frontier.md:24 "26.5x TTFT speedup at 1M tokens and >100x at 4M (fitted extrapolation)"; neuromorphic-hardware.md:38 370M parameters published SOTA (C12, C19) |
| fill-ball | 7/7 lanes closed every register top-gap same-sitting | PARTLY (overclaim) | 7 receipts + 7 lane jsons TRUE (fillball/ has citation-lint, corpus-fold-land, day1-digest, elder-salvage, errata, percolator-candidates, seed-seal); but the register's ranked table has 12 rows and fills 1 (bake), 8 (index-last), 9 (KVarN), 10 (trio), 11 (tickets), 12 (move 1) got no fill-ball lane (C15) |
| librarian-expedition | 61 durable primaries landed (90.6MB), 975 artifacts inventoried | TRUE | gathering-log.md:100-103: holdings delta "exactly the 61 rows landed here", 61/61 full-chain PASS, "90,594,721 B across 61 primaries"; my table recount: 61 landing rows, byte cells sum 90,594,554 (167 B under the stated total, cell-pick heuristic, not a contradiction); inventory.md:21 "975 files" (C13) |
| salon-mine | laws minted (V4-Never-Ran, ghost-citation-gate, persona-prior-not-soul, PRE-REGISTER-OR-DESK) | TRUE | all four names bind to receipt bytes (m01 json, m13.md, m10 json/check) (C14) |
| salon-mine | "parked on quota at 50 rows" | UNVERIFIED (unbindable number) | zero hits for "parked on quota" or "50 rows" across watch/inbox/ and memory/; m20-synthesis.json has zero "50" hits (C14, C20). The parking itself is real (lane jsons m06/m09/m11/m14/m16/m18/m19 absent; quota-reset commit a48c38543 landed the same night) but "at 50 rows" binds to nothing |
| salon-mine | proven on the 25-transcript vault | NOT RE-VERIFIABLE | the vault folder now holds 36 .txt (C20); the receipts cite individual transcripts (e.g. m01: SALON-Salon.txt, 118,270 bytes, 2,047 lines) but no estate surface lists the 25-transcript manifest at run time |
| ractor-engine | workflow_gate PASS digest 5253afd2d68d G1-G7 | TRUE | REGISTRY row 2026-10-02T01:49:54Z PASS (C16); turn-gate determinism shape present (25 "turn" hits in script) |
| tree-doctrine-dig | 30 old-book + 10 historical-case + 10 modern-fold diggers; gated, digest da62eaa8c17f | TRUE | script line 99: "Dispatching 50 diggers: 30 old books, 10 historical cases, 10 modern folds"; REGISTRY 2026-09-25T18:52:43Z PASS; TREE_DOCTRINE_V2_DIGEST_20260925.md exists (C16) |
| mickey17-v2 | spec pointer | TRUE | watch/inbox/MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md exists (15,069 B); the engine body is proven live by the gap-analysis run, which ran this same body shape 15 lanes deep (C1) |
| the-50, the-gala, game-mechanics-deep-dig | pointers + gating | TRUE | THE_50_PROGRAM_20260918.md exists; the-gala.dwf.ts carries 12 REGISTRY rows incl. five on 10-01; game-mechanics-deep-dig has 4 REGISTRY rows (C16, C17) |

Score: of the checked claims, the three named focal questions resolve as
olm-mine 8x4+24 TRUE (but its provenance sentence is a struck phantom plus a
misdated run), gap-analysis 15 auditors TRUE at archive with the 8-at-rollup
nuance (but the saved script is the wrong engine entirely), game-digs TRUE on
all three counts. The lies concentrate where nobody re-reads: provenance
sentences and the body/metadata seam.

## Corrections that belong in the saved metadata

1. olm-mine.dwf.ts description: replace "Provenance: 191.8M-token run
   2026-09-29 (32/32 miners, 21/24 confirmed)" with "Provenance: 20260928 run,
   32/32 miners, 21/24 confirmed (receipt
   watch/inbox/frontier_olm_20260928/RECEIPT.md)". The 191.8M was struck by
   ERRATA 001; the run date is the 20260928 slug, not 09-29.
2. gap-analysis.dwf.ts: the header and body disagree. Either restore a body
   that implements the described engine (period/slug args, a15-rollup,
   GAP_REGISTER output) or rewrite the header to the body's real interface
   (topic + targets + width, mickey17_v2 fold) and rename. As saved, firing it
   with its own documented args dies at "no targets passed" (line 110). Also
   file the missing REGISTRY row after the next gate check.
3. drop-dig lineage: add the two missing register rows (PAM, localmind) to
   localfirst_memory_landscape_signals.jsonl or restate the receipt as "14
   rows across 12 systems; PAM receipt-only; localmind never dug" in the next
   amend, so "7/7 lanes" stops implying full brief coverage.
4. fill-ball description: "7/7 lanes closed every register top-gap" should
   read "closed 7 of the register's 12 one-sitting fills (ranks 2, 3, 4, 5
   seat-half, 6, 7 + meta-gap 2); ranks 1, 8, 9, 10, 11, 12 open".
5. salon-mine description: cut "parked on quota at 50 rows" or bind it to a
   byte (no estate surface carries it). Keep the laws list; those bind.

## The law this hands back (for the standing loop)

Saved workflow metadata is a claims surface and it is ungoverned: gitignored,
outside citation lint, outside the ratchet, outside the errata carrier census.
The corrections above should land as harness amendments (AmendWorkflow /
SaveWorkflow), never as hand edits to the metadata blocks - hand-edited
metadata blocks are the documented cause of unreadable saved workflows. A
periodic description-vs-receipt tri-state (this lane's method, one lane, one
sitting) belongs on the weekly cadence beside gap-analysis.

Not done by this lane: no metadata was edited (the corrections are named, not
applied); no code under mag/ or tools/ was touched, so the violation ratchet
was not run; the salon vault's 25-transcript manifest at run time could not be
reconstructed from any estate surface.
