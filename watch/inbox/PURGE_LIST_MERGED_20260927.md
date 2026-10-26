# HISTORY PURGE SCAN HARVESTED + MERGED LIST — 2026-09-27

Handoff item 1 (HANDOFF_20260927_SESSION_CLOSE.md) executed: the history scan
landed 06:44 EDT (`watch/inbox/secret_gate_results/history_20260927T104430Z.json`,
runtime 3,769.6s over the 6.11 GiB pack) and is merged below with the interim
list (SECRET_GATE_STEAL_ADDENDUM_20260927.md). This is the AUTHORITATIVE
purge target list for the operator-gated filter-repo step.

## Scan census

- 7,079 unique findings across all git history; **21 blocking** (provider
  shapes only, threshold high).
- Noise shapes confirmed report-only as designed: ENV-ASSIGN 4,214,
  AWS-SECRET-40 2,839 (top carriers are base64/hex blobs in harvested
  corpora: docs/mirrors/mcp/_raw/git_tree.json 1,065; marathon_terminals
  m3/envy.txt 593; catalog/catalog.jsonl 128 — none block, none rotate).

## The blocking set (21 rows -> 4 families)

1. **lan.key** — PRIVATE-KEY-BLOCK, memory/tls/lan.key:1, first commit
   799ddb6feaad. Regeneration still owed (nothing names the listener;
   handoff thread 4 stands).
2. **Live xai key, 9 copies** — memory/biography_backup_20260825/ (6 files:
   dossier.json, pdf, biography/{dossier.json,pdf}, biography/derived/pdf,
   biography/residual/.json), memory/portable_bags/bag-20260727T214646Z/
   (residual json), memory/trajectory/steps.jsonl:3310. This is the SAME key
   five live modules ride via .env XAI_API_KEY (art_forge, depin,
   grok_rightsize, nervous_system, refine_loop): **rotate on console, swap
   .env, THEN wipe history** (ROTATE-FIRST-WIPE-SECOND law, canon
   87b8cf1750883595 lineage).
3. **Dead telegram token** — TELEGRAM-BOT steps.jsonl:1994 (bot 8750925249
   deleted, getMe 401; handoff thread 5). No rotation possible; purge only.
4. **Stripe-shaped harvests, 10 rows** — boe003.html / boe_index.html +
   corpus/tmp_enoch/boe012..019.htm (9 html, all line ~234-257, one harvest
   batch, commit a5dd96176a2b) and module_audit.ipynb:2307 (799ddb6feaad,
   the "cookbook ipynb key" from the interim list). All in test-key shape
   from scraped pages; treat as dead but purge per interim decision.

Plus the interim list's 19 corpus dump files (report-tier, operator-chosen
purge): see SECRET_GATE_STEAL_ADDENDUM_20260927.md — unchanged by the scan.

## Operator gates before any filter-repo run (unchanged)

- xai reissue or orphan-revoke (the closing session's question stands).
- lan.key regeneration decision.
- Purge GO itself.

Nothing in this file authorizes the wipe; it is the target list only.
Scan tool: tools/secret_gate.py --history (split 2026-09-27 into
rules/scan/CLI modules, behavior proven by state/fuel/sg_split_ref/).
