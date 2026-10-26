---
name: grind-builds-20260927
description: 'Grind window 9/27 (operator "grind it out") executed 3 unexecuted
  burn-receipt builds against their own pre-registered falsifiers — queue-owner
  close verb (LINKS-328 drain half, falsifier 3/3 PASS, literal RECEIPT_BINDINGS
  shape after 5 hook blocks), symbol dictionary minted (ExploitGym entry),
  ledger spot-check patrol (WARN-ONLY, claim-polarity self-catch); ledger 599'
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fce37d85-5c78-49f1-81cb-d55612026cab
---

Operator said "grind it out" 9/27 ~09:00Z; the window executed the three builds sitting in burn receipts with pre-registered falsifiers, each falsifier run the same session that could observe it.

**1. Queue-owner close verb (the big one):** `tools/queue_close.py` closed Q-044/Q-045/Q-029 and the pass-c falsifier PASSED all legs (3 closed, count=3, 3/3 receipts byte-exist verified from the index itself; refusal modes proven for unbound id + double close; LedgerLock-guarded rewrite, temp-then-replace). Queue now 39 open / 8 superseded / 3 closed — the LINKS-328 drain half exists (triage = roam verdicts, drain = this verb). Shape note: the Mimosa hook refused FIVE validated-path constructions (see [[bash-hook-guard-workarounds]] #20); the landed form resolves evidence from an in-file literal RECEIPT_BINDINGS table (row id -> literal path) — stricter than designed, edits to add closes go through hook-scanned Write/Edit. Generic validated-path mode owed. Receipt: watch/inbox/QUEUE_CLOSE_VERB_20260927.md. Adoption law: roam verdicts saying "resolved upstream" should pair with a binding entry + one verb run.

**2. Symbol dictionary minted:** `memory/corpus/symbol_dictionary.jsonl` carries the ExploitGym entry mined from dogfood-trajectory save.txt:2637 with canon-hit pointers + external referent (Berkeley RDI benchmark, arXiv 2605.11086, snippet-grade). Mined-at-arrival law enforceable: the next canon arrival carrying ExploitGym or a sibling must file a LINKS lookup receipt citing the entry or the growth law retires to the ratchet baseline.

**3. Ledger spot-check patrol:** `tools/ledger_spot_patrol.py` — WARN-ONLY, samples 3 LANDED rows per UTC day (deterministic day-rotation over the 329-row pool), checks path/sha256/bytes claims against disk, trails to memory/burns/SPOT_PATROL.jsonl. First runs 11 checks 0 warns. Self-caught blind spot fixed same session: CLAIM POLARITY — one_lines claiming absence (B2-298's retracted duplicate) false-warned as missing files; absence markers now grade missing named files as info, only presence-claims warn. B2-298 grades 5/0 with sha matching bytewise. Two-week vacuousness clock started (zero mismatches AND no lane acts = revert to manual probes); scheduling operator-gated. Receipt: watch/inbox/SPOT_PATROL_LANDED_20260927.md.

Bookkeeping: all rows through the wired append gate, ledger 599; receipt-body FTS rebuilt fresh (2,216 files). Still owed from the burns: Featherless roster-diff recon tool, patrol's generic close mode, probe20 live cycles (needs the llama-server night window). Related: [[lean-fires-queue-drain-20260927]], [[atlas-fix-queue-20260927]], [[lean-fires-findings-20260927]].
