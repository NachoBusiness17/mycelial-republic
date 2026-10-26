# break-security.md - hostile second pass over the dogfood security lens (2026-10-03)

Pass: break-security, byte-checking every evidence cite in
watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/security.md (the lens
report) against the estate. Three findings verdicted: F1 CONFIRMED (two
precision corrections), F2 CONFIRMED (one number killed), F3 CONFIRMED
(extended in both directions). Every check below was run this sitting unless
marked NOT RUN. No em-dash bytes in this file.

## Verdicts

### F1 (gate PASS credential is self-asserted prose; stale digests; 7 of 12 first gated tonight; string-presence lambdas): CONFIRMED, with corrections

Every cite re-verified by running it:

- ractor-engine.dwf.ts:12 carries "workflow_gate PASS digest 5253afd2d68d
  G1-G7." (Read this sitting.) Current bytes hash 90b1990da9ae under the
  gate's own grammar, recomputed independently: python sha256 over the
  text-mode read, [:12], replica of tools/workflow_gate.py:300
  (`hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]`, inside the
  cited :294-300 read block). STALE, confirmed.
- olm-mine.dwf.ts:10-11 carries "workflow_gate PASS digest 2487787e949f".
  Current bytes hash 70571fea3957, recomputed the same way. STALE,
  confirmed. Registry shows 2487787e949f was the DRAFT
  .zcode/workflow-drafts/frontier-olm-mine.dwf.ts digest at
  2026-09-30T01:18:10Z, so the header was true once, for other bytes.
- Registry: memory/workflows/REGISTRY.jsonl rows 2026-10-02T16:13:42Z and
  :43Z hold 90b1990da9ae for ractor-engine; the 2026-10-04T02:33Z batch
  rows hold the current digests for all 12. Confirmed.
- G3/G7 string-presence: tools/workflow_gate.py:55-61 (G3 passes on
  "Previous critique" at :59 or "reported these issues" at :57) and
  :75-79 (G7 = literal "no em-dashes" AND "never fabricate"/
  "no-fabrication"/"never synthesize"). Confirmed: phrase presence, not
  behavior.
- Gate x12 rerun, this sitting: `.venv/Scripts/python.exe
  tools/workflow_gate.py check --script .zcode/workflows/<name>.dwf.ts
  --no-register` for each of the 12 named workflows. All PASS, exit 0;
  ractor-engine soft-WARN G6 exactly as the lens said. Substitution
  noted: I used --no-register so the audit would not append rows; the
  lens's stamp (security.md:228-230) names the same command WITHOUT
  --no-register, meaning its 12 checks minted the 02:33Z batch rows.
- My rerun adds one warn the lens missed: tree-doctrine-dig soft-WARNs G3
  (judge-model stamp absent), and its own batch row
  (2026-10-04T02:34:06Z) carries the same G3 soft warn.

Corrections to the finding text:

1. COUNT VS BATCH: 6 of the 12 got their first saved-identity row IN the
   13-second batch (olm-mine 02:33:47Z, fill-ball :49, salon-mine :53,
   librarian-expedition :55, wide-dig :58, drop-dig 02:34:00Z; the 6 span
   13 seconds). The 7th, gap-analysis, got its first saved-path row at
   2026-10-03T21:17:54Z, about 5h16m earlier the same sitting, NOT in the
   batch. The condensed sentence "7 ... only tonight in a 13-second batch"
   conflates the two; the lens's own evidence text lists both timestamps
   correctly. Substance survives: 7 of 12 had zero saved-identity gating
   before the dogfood window.
2. ATTRIBUTION (cures the lens's blind spot 4): the batch writer is the
   security lens itself. security.md:228-230 names "gate check x12 ...
   for each of the 12 (all PASS, ractor-engine soft-WARN G6)", the batch
   rows carry exactly that warn pattern, and the batch window
   (02:33:47-02:34:06Z = 22:33-22:34 EDT) falls inside the sitting that
   filed security.md (23:12 EDT). The lens reported the registry backfill
   it itself caused as an external fact.
3. OBSERVER EFFECT: audit runs without --no-register are
   indistinguishable from submission rows in REGISTRY.jsonl (both are
   PASS rows with the current digest). Any future "first gated at" census
   inherits this. The gate has no audit-vs-submit marker (whole file
   read, tools/workflow_gate.py:1-335).

Falsifier intact: no registry row carries a current digest dated before
2026-10-03 for the 6 batch-firsters (registry sweep this sitting), and no
header digest recomputes clean.

### F2 (gala-template fold gate fails open; receipt not required to carry gate status): CONFIRMED, one number killed

Line cites all byte-checked against .zcode/workflows/wide-dig.dwf.ts:

- :287-297 CONFIRMED: gate spawn at :287, one gate-repairer pass whose ask
  is "Diagnose and repair so it exits 0" (:292), rerun at :294, then :296
  computes gateClean and :297 logs "STILL FAILING, fold ships UNVERIFIED"
  with no throw or return; execution continues to the fold at :309.
- :312 CONFIRMED: "Its sections (authoritative):\n" + gate.stdout is fed
  to the folder regardless of gateClean; gateClean is never referenced
  again in the file (grep-level read of :280-364).
- :350-353 CONFIRMED: the herald ask's required sections are header,
  scoreboard, decision ledger, refired + buried, review verdict, filing
  verdict. No gate status section.
- :356-357 CONFIRMED: artifact.file(..., { primary: true }).
- fold_gate.sh fails loud: watch/inbox/gala_20260925/fold_gate.sh:21-27
  (wrong-bash guard, exit 2) and :95-96 (`if bad: sys.exit(2)`). The
  fail-open is in the workflow's handling, confirmed.

Corrections and strengthening:

1. THE 167 IS DEAD. Two instruments this sitting:
   `diff wide-dig.dwf.ts the-gala.dwf.ts | grep -c '^[<>]'` = 40 changed
   lines; `diff -u wide-dig.dwf.ts the-gala.dwf.ts | wc -l` = 52. The
   lens's other distances DO reproduce under the unified instrument:
   drop-dig 54, salon-mine 54, librarian-expedition 50, fill-ball 48
   (lens said 44-53; my 48-54). the-gala is INSIDE the clone family at
   every measure I ran, not a 167-line outlier. This makes the finding
   stronger: the template family is 6 members including the-gala, all
   within ~40-54 unified diff lines of wide-dig, so the fail-open is a
   6x replication, and the-gala is not a diverged origin.
2. SECOND FAMILY FOUND (addition): gap-analysis vs mickey17-v2 = 59
   changed lines (near-clones), while the-50 vs tree-doctrine-dig = 422
   (not family). The fleet's clone structure is at least: gala family 6,
   game-dig family 5 (per dogfood.md F4), mickey family 2, singles.
3. RECEIPT PRECEDENT (addition, sharpens the move): gate status HAS been
   carried in gala receipts historically, as GATE PASS:
   watch/inbox/gala_20260925/ball-20260929_RECEIPT.md:50 ("GATE PASS
   (ask's scripted sections, authoritative). Ballroom 8 danced ...") and
   wave5-repair_RECEIPT.md:17 ("Re-witnessed at receipt time by running
   `bash ... fold_gate.sh ...` (exit 0, GATE PASS)"). Both samples are
   PASS-carrying; no receipt carrying a FAILING gate status was found
   (12 of 18 receipts mention gate patterns; I read the two above). So
   the wide-dig herald section list is a REGRESSION from estate receipt
   practice, and F2's move (thread gateClean into the required sections)
   restores precedent rather than inventing it. The falsifier stays
   unfired: the one known failing-gate run (wave5, the exit-127 spawn
   failure documented in fold_gate.sh:6-15) has its failure in the side
   repair receipt fold-gate-repair.md, not in the primary receipt's
   section contract.

### F3 (zero instruction-trust-boundary across the fleet): CONFIRMED and extended

- Reran the lens's exact instrument untruncated:
  `grep -n -i -E 'untrusted|injection|as data|not instructions|do not
  obey|ignore any instruction' .zcode/workflows/*.dwf.ts` over all 19
  files (glob census: 19 .dwf.ts on disk this sitting; global
  ~/.zcode/workflows does not exist, so this is the complete fleet).
  Exactly 1 hit: ractor-engine.dwf.ts:113, the security-lens persona
  string ("lethal-trifecta frame (private data + untrusted content +
  communication)"). Quantifier law satisfied: full tree, untruncated,
  instrument named.
- olm-mine.dwf.ts:118-136 CONFIRMED (four web doors: arXiv, hn.algolia,
  old.reddit, api.fxtwitter); :161-164 CONFIRMED (SWEEP_SYSTEM: "You have
  WebSearch and WebFetch. " + LAWS); :412-428 CONFIRMED (fold writes
  DIGEST.md, register.jsonl :417, percolator_candidates.jsonl :419, and
  :424 injects raw sweeps JSON into the folder ask); LAWS at :111-114
  CONFIRMED (fabrication, em-dashes, citations, spawn flags; no
  instruction-origin clause).
- wide-dig.dwf.ts:341-345 CONFIRMED: the filer appends lane-derived rows
  to memory/corpus/LINKS.jsonl (:341-342) and to
  memories/session/next-window-handoff.md (:344). Severity note the lens
  left implicit: AGENTS.md's Clippy block orders every new window to
  "execute the frozen spec: /memories/session/next-window-handoff.md",
  so the handoff leg of the triangle is a boot-executed file, the
  strongest sink in the estate.
- EXTENSION, defense side: the lens's blind spot said skills were not
  swept. Swept this sitting with a validated instrument:
  `grep -rln -i -E 'untrusted|prompt.?injection|content is data|as
  data|never follow|not instructions' .agents/skills --include='*.md'`
  over 44 md files, control grep ('law') matched 26 files, quarantine
  patterns matched 0. There is no canonical quarantine sentence anywhere
  in skills to import; F3's move writes new text. But the estate DOES
  hold the doctrine unported: docs/concepts/GRAYSWAN_NG_AISRP_BRIEF.md:30
  defines Indirect Prompt Injection ("Hiding malicious instructions in
  data AI reads externally"), memory/facts/fuel_feed.jsonl:6 banks a
  2026-08-24 percolator compiled_invariant describing prompt-injection
  middleware, and the vendored MCP spec carries untrusted-input rules
  (docs/mirrors/mcp/spec/2026-07-28/basic/index.mdx:477). The lens's
  "not ignorance, an unported lesson" line is confirmed on the defense
  side too, with two more citations than it had.

## What the lens missed (additions)

1. The audit mints the ledger it audits. The 02:33Z batch the lens
   counted as fleet backfill was produced by the lens's own gate check
   x12 (security.md:228-230, no --no-register), and its own batch rows
   then served as F1's evidence. Evidence: REGISTRY.jsonl
   2026-10-04T02:33:47-02:34:06Z, 12 rows, warn pattern matches the
   stamp. Falsifier: the stamp naming --no-register (it does not) or a
   different session's receipt claiming the 12x run. Move: audits always
   run --no-register, and either add an "audit": true marker to the gate
   or a REGISTRY-consumer convention separating audit rows from
   submission rows (~15 min).
2. the-gala = 167 diff lines is wrong by two instruments (40 changed / 52
   unified); the-gala sits inside the 6-member clone family. Falsifier: a
   third instrument reproducing 167 for wide-dig vs the-gala. Move: none,
   correction only; F2's fix cost unchanged.
3. The herald's section list is a regression: estate receipts already
   carried "GATE PASS" sections (ball-20260929_RECEIPT.md:50,
   wave5-repair_RECEIPT.md:17). Falsifier: those lines absent on disk
   (they are present). Move: fold into F2's ~15 min fix, zero extra.
4. The verification stamp undercounts its own warns: tree-doctrine-dig's
   batch row (2026-10-04T02:34:06Z) carries the G3 soft warn; the stamp
   names only ractor-engine's G6. Falsifier: row shows no G3 soft (it
   does). Move: amend the stamp, ~2 min.

## Blind-spot audits

- workflow_introspection_unavailable: reproduced from this seat
  (ListWorkflowRuns returned the same error this sitting), so fire-count
  claims remain receipt-census proxies for me too. NOT RUN: any run
  journal read.
- Runtime CREATE_NO_WINDOW question: wide-dig.dwf.ts:229 byte-confirmed
  (`world.run("powershell", ["-NoProfile", "-Command", "Start-Sleep
  -Seconds 600"], { timeoutMs: 660000 })`, no creationflags visible in
  the call). The dwf runtime source is outside this repo, so this stays
  OWED exactly as the lens marked it. Also NOT RUN: any workflow fire.
- bash.exe shim: exists at repo root (bash.exe and bash, 6,144 bytes
  each, mtime Sep 29 09:27), corroborating the banked F4. Internals not
  inspected this sitting.

## Verification stamp (commands run this sitting)

- ls .zcode/workflows/ (19 .dwf.ts) ; ls ~/.zcode/workflows/ (absent)
- python sha256 text-mode [:12] over all 19 files (gate grammar replica)
- python registry extraction over memory/workflows/REGISTRY.jsonl
  (75 rows total, 69 with .zcode paths; first saved-identity joins; batch
  row warn arrays)
- workflow_gate.py check --script x12 with --no-register (all PASS,
  exit 0; ractor-engine WARN G6; tree-doctrine-dig WARN G3)
- Read: tools/workflow_gate.py (whole), ractor-engine.dwf.ts :1-20 and
  :244-273, olm-mine.dwf.ts :1-30 :105-169 :400-434, wide-dig.dwf.ts
  :218-242 and :280-364, fold_gate.sh :1-100, security.md (whole),
  dogfood.md (whole)
- grep untrusted/instruction patterns: .zcode/workflows/*.dwf.ts (1 hit),
  .agents/skills (44 files, control 26, quarantine 0), memory/rib +
  memory/facts + docs (fuel_feed.jsonl:6, GRAYSWAN :30, mcp spec)
- diff instruments: grep -c '^[<>]' and diff -u | wc -l for wide-dig vs
  drop-dig, salon-mine, librarian-expedition, fill-ball, the-gala;
  gap-analysis vs mickey17-v2; the-50 vs tree-doctrine-dig
- find watch/inbox/gala_20260925 -name '*RECEIPT*' (18); grep gate lines
  in 12 receipts; read ball-20260929_RECEIPT.md:50 and
  wave5-repair_RECEIPT.md:17 context
- ListWorkflowRuns attempt (workflow_introspection_unavailable)
- wc -l REGISTRY.jsonl (75); grep 191 in tools/citation_lint.py (:12-13);
  ls bash.exe bash at repo root

NOT RUN this sitting: any workflow fire, any pytest, the run journal,
fold_gate.sh execution, any exploit attempt.

Filed by break-security. Banked at
watch/inbox/ractor_engine/2026-10-02-workflow-dogfood/break-security.md.
