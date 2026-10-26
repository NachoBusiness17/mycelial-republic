---
name: freelane-runner-and-operator-corrections-20260927
description: Free-lane tandem runner architecture (B2-178 autonomous loop driver) + operator corrections on key naming and FCFS queue
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Free-lane tandem runner (B2-178) went autonomous 9/27: stdlib-only loop driver (sha 7a3b4571) pushing a 57,375-item estate queue through all 8 alive lanes (groq gpt-oss-120b, openrouter k1/k2, nous, together, cohere, zai Pro+Lite). Four estate tasks: LINKS title normalization (210 rows), LINKS dedupe candidates (27 pairs), caption-ledger enrichment (2,726 rows), corpus metadata classification (54,412 files). Privacy by construction: caption text, filenames, file contents never leave the machine; outbound prompts carry structure only. Rate shapes honored per lane (groq 8s spacing + 185K TPD guard, openrouter 3.5s/key, zai 10s + 15s on 1305). Hourly receipts + close totals at 23:30 with no sitter. Files: B2_178_freelane_runner.py, B2_178_events.jsonl, B2_178_counters.json.

**Operator corrections (2026-09-27):**
1. Key naming: "both together ai keys work too just weird stuff you dont expect" — the B2-296 lane that "fixed" mistral key casing was solving a non-problem; both mixed-case and canonical .env key names work on the operator's box. Do not normalize operator key names unless a real cross-platform failure actually breaks something.
2. FCFS queue: the operator challenged the 10x usefulness analysis; byte census showed 97 debt / 27 frontier / 274 neutral by filename — the neutral majority means filename classification cannot settle the value question. The real structural fact: dispatch is strictly first-come-by-number with zero value ranking, so queue composition is a choice, not a property of the machine.

**Swarm architecture at scale (B2-476 deep compute lane):** adventure_2d6 raised from 0.483 to 0.932/0.935 across all six regions via full-normals rebuild using free-lane builders. Deep unbounded lanes produce results bounded briefs cannot (the brief's 30-min falsifier honestly filed as GRAZE-ZONE).
