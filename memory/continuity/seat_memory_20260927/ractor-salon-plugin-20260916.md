---
name: ractor-salon-plugin-20260916
description: Operator order — open-source the ractor salon as a Mycelial
  Republic plugin for the Nous Hermes Agent catalog (SHA-pinned YAML PR,
  community tier); package build + demo salon in flight; publish = operator's gh
  call
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

2026-09-16 night, operator dropped
https://x.com/NousResearch/status/2100266422882451793 (Nous Research's Hermes Agent
PLUGIN CATALOG — curated, reviewed, SHA-pinned installs: an entry is ONE YAML file at
`plugin-catalog/<name>.yaml` in the hermes-agent repo via PR, pointing at a PUBLIC repo,
pinned to the reviewed 40-hex commit, real release tag required, community tier,
human-reviewed; "nothing enters the catalog automatically") and ordered: "Mycelial
Republic plugin? we need to open source the ractor plugin salon" + burn the Union Alpha
window and the 5.3 window in tandem full blast, concurrency usefully.

- **P1 packaging lane fired:** standalone package at `C:\Users\foste\Documents\ractor-salon\`
  (OUTSIDE the main repo tree — embedded-clone trap), fleet-scrubbed ports of
  mag/research_fanout.py (LANES registry, probe-first, call_lane, raw JSONL tape),
  mag/scale_salon.py, mag/lite_guard.py (optional pacing), the receipt-first + Rashomon
  laws as features. Apache-2.0; pyproject installable; Hermes plugin manifest (Agent
  Plugins v1, skill + MCP-server-stub bundle per the touchdesigner pattern); offline tests;
  CI workflow; git init + v0.1.0 tag INSIDE the standalone repo only.
- **P2 demo salon fired:** the README's example-output run — "Should a sovereign agent
  fleet open-source its orchestration layer? Steelman both sides, then the deciding
  argument" — across live free lanes + stealth/union-alpha (2 seeds), per-lane answers
  screened for private/identifying info before entering a public README.
- **PUBLISH = operator's call:** `gh repo create` under his account (auth checked, not
  self-served), push, tag, then the draft catalog YAML (name: ractor-salon, tier:
  community, category: tools, maintainer: operator) filed in the P1 receipt. Our
  SHA-pinned receipt law IS their install-integrity model — the plugin was always going
  to be SHA-pinned; we just call it verkle-knotted.
- Receipts: watch/inbox/wave_20260916/receipts/P1_RACTOR_PACKAGE.md, P2_DEMO_SALON.md.

## LANDED (2026-09-16 night)

- **P1 PACKAGE BUILT:** standalone repo at `C:\Users\foste\Documents\projects\ractor-salon\`
  (own git, commit 70e2d892, tag v0.1.0, 19 files, main repo untouched). src/ractor_salon/ =
  lanes.py (11-lane registry, probe-first, call_lane never raises), guard.py (SSRF boundary +
  PacingGuard ported from lite_guard), receipts.py (append-only JSONL + SHA-256 pin + Rashomon
  fold), salon.py (salon/fan modes), CLI (lanes|run|fold|status), MCP stdio stub; Hermes Agent
  Plugins v1.0.0 packaging (plugin.json + skills/run-a-salon SKILL.md + optional mcp.json).
  Apache-2.0; scrub held (env-var keys only, no fleet paths/names). **Tests: 18 passed** —
  and the port's own tests caught TWO REAL BUGS: burst record-after never fired, and retry
  rotated cells onto other lanes (erasing a lane's voice) — fixed in the package, FLAGGED
  for a gen-2 check of production mag/research_fanout.py (may carry the same flaws).
- **P2 DEMO SALON landed (25 metered calls, $0):** 10 answers across 9 live lanes +
  stealth/union-alpha ×2. Privacy scan CLEAN (README-safe verbatim). Fold: all 10 converge
  on the mechanism/secret split — publish protocols/policy engine/audit surfaces, keep keys/
  credentials/live topology. SHOWCASE PICK (union-alpha T0.2, 109w): "Closed orchestration
  asks for trust in the sovereign — precisely what sovereignty should not require."
  Runner-up or-ling3: "Sovereignty requires auditability, not secrecy."
- Traps filed: Mistral rejects OpenAI-style `seed` (HTTP 422 extra_forbidden — omit seed on
  mistral bases); groq-qwen gated lane held at max_tokens 780.
- Publish checklist (in P1 receipt): operator `gh auth login` → `gh repo create
  <owner>/ractor-salon --public --source . --push` → push tag → release → swap 2 OWNER
  placeholders → human scrub pass → file the catalog YAML PR himself.

## N5 EXTERNAL DOGFOOD LANDED (2026-09-16 night) — verdict NEEDS-FIX before publish

Installed via the documented user path (`pip install -e .`), probed 7 live lanes, ran the
salon on the fiber-optics question: 8 lanes fired, 6/8 answered, SHA pin verified
independently, 35 tests pass, $0. **2 HIGH blockers:** (1) the README's "deterministic desk"
is FALSE — `fold --tape` includes probe rows and re-stamps `now_iso()`, so no two folds are
byte-identical; (2) the question text rides on NO receipt — a tape cannot answer "what was
asked". Plus MED/LOW: no `--lanes`/`--max-lanes` CLI flags, unreconcilable answer counts
(6/11 vs 6/8 vs 5), or-nemotron CoT leak unflagged, CEREBAS_API_KEY misspelling.
Provenance: v0.1.0 tag didn't name the tested bytes — pinned as commits d13625f/4451d24/
438a1c0 in the standalone repo. Best fold line (zai-lite): "Electrodes alone record
endogenous, spatially uncontrolled activity — correlation without causation. Optical WRITE
adds a defined input." Fix blockers 1–2 before the catalog PR. Receipts:
N5_RACTOR_DOGFOOD.md + docs/BUG_REPORTS/001_external_dogfood_20260916.md (committed).
Related: [[union-alpha-free-window-20260916]], [[concert-001-four-substrate-20260916]],
[[lite-key-seat-glm53flash]], [[mesh-not-sequential]].
