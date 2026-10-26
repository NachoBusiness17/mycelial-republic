# FEED-MINER BATCH RECEIPT - 2026-10-17: 40 REVERSE-GPS ASKS STAGED

Classification: RECEIPT + OPERATIONAL ADVANCE
Producer: Antigravity (primary seat)
Workspace: local_sovereign_agent
Context: Standing Wave Protocol - Feed-Miner Organ (2,000 asks/day pacing)
Anchor: queue/hermes_247_free_wide, tools/ask_minter.py, memory/percolator/explore.jsonl

---

## 1. Executive Summary

The free-lane miner feeding organ has been advanced. Prior fires were spinning on an un-advanced start offset (re-minting E00000..E00041, which were already landed in watch/inbox/hermes_burn/ and thus skipped at $0.00).

Actions completed:
1. Hardened tools/ask_minter.py with an auto-advance scanner across landed deliverables (watch/inbox/hermes_burn/H247_FOLD_E*.md), wide queue roots, and worker partitions. It now automatically detects the next un-minted slot and strips em-dashes.
2. Minted and staged the next batch of 40 reverse-GPS asks: H247_FOLD_E00042 through H247_FOLD_E00081 into queue/hermes_247_free_wide/.
3. Model rotation applied evenly across the 3 active free families:
   - nvidia/nemotron-3-super-120b-a12b:free (14 asks)
   - google/gemma-4-31b-it:free (13 asks)
   - dots-studio/dots-3-note-preview:free (13 asks)
4. Evidence preflight compliance: all 40 asks bind evidence: ["memory/percolator/explore.jsonl"].

---

## 2. Staged Range Catalog

- Range: H247_FOLD_E00042 to H247_FOLD_E00081 (40 asks)
- Source: memory/percolator/explore.jsonl (behavioral event and infrastructure recovery stream)
- Contract: FOLD THIS SIGNAL (plain text, no em-dashes, under 150 words): (1) TRUE-TODAY, (2) THE ORGAN, (3) THE FALSIFIER.
- Directory Structure:
  queue/hermes_247_free_wide/H247_FOLD_E00042/ask.json
  ...
  queue/hermes_247_free_wide/H247_FOLD_E00081/ask.json

---

## 3. Worker Ingestion & Firing Readiness

The hourly driver (scripts/hermes_burn_247.ps1) will pick up these 40 asks on its next fire, partitioning them via tools/batch_fire.py across _worker0, _worker1, and _worker2 at concurrency width 3 with paced spacing.

Zero 400/429 parkings: the parked families (liquid/lfm-2.5 and thinkingmachines/lab-1) remain excluded per the morning routing policy until dedicated short-stack adapters land.
