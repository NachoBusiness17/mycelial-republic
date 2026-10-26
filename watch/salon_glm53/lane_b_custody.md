# LANE B — GLM-5.3 Flash CUSTODY / LINEAGE
seat: worker subagent · 2026-09-01 07:06Z · sources: GLM53_LINEAGE_DROP, WEIGHTS_PLAN, MODEL_VAULT_MANIFEST, MODEL_ATLAS_PASSPORTS

## 1) What THIS DROP changes in Phase-5 GLM lineage mapping
Status legend: P=proven (Flash-specific disclosure) · L=lineage-evidence (GLM-5-family report, NOT Flash-confirmed) · U=unknown (vendor non-disclosure)

- P — Flash began from a NEW base model (redesigned arch+recipe), NOT a public distilled GLM-5. (@drop "not publicly described as compressed or distilled"; "trained from a new base model"). CORRECTS the 22:46Z hunch "glm-5.3-flash (distilled)" in WEIGHTS_PLAN Phase 5 — drop explicitly rejects the distillation label.
- P — 320B total / 18B active; natively multimodal; 30T-token corpus; 1M context; hybrid sparse+linear attention. (bottom line + arch section)
- L — GLM-5 pipeline (pretrain→mid→SFT→reasoning-RL→agentic-RL→general-RL→distillation/regression) is the nearest public recipe. (training materials + tuning sections)
- L — repo-level SWE data: ~10M issue–PR pairs, ~160B unique tokens in that component. (training materials) — the ONE spec number for candidate datasets.
- L — reasoning-RL uses Codeforces, TACO, synthetic CP, open math/science sets. (reasoning RL section)
- L — research ancestors cited by GLM-5, NOT confirmed-Flash: DeepSeek-V3.2 Sparse Atten, NExtLong, EntropyLong, Gated Delta Networks, GRPO, GSPO, DataComp-LM. (research table + its own caveat).
- U — FLASH-SPECIFIC: exact mixture %, licenses, doc counts, dedup/contamination thresholds, token schedule, teacher mix, SFT sizes, RM arch, RL run count/duration, total FLOPs, hardware-hours/energy, safety mix, checkpoint↔GLM-5 relation, per-component ablations. (What remains unknown — 15 items verbatim).

NET: drop converts Flash lineage from "one artifact" to "family recipe + Flash-disclosure gap." Phase-5's real bankable object shrinks to datasets we can cite with L-status, with a fixed unknowns ledger.

## 2) Publicly bankable family datasets per checkpoint (custody cost)
All banked data must be a family-cited lineage-evidence item (L), NEVER claimed as Flash training data.

- **10M issue–PR pairs** — L-status, ~160B tokens. PUBLIC EVIDENCE: Software Heritage metadata + code-host snapshots described, but the PAIR SET itself is NOT a public release — not directly bankable. Custody: $0 to bank Software Heritage snapshots (public; sha256-verify), cost ~repo-size GBs. UNVERIFIED any official zai/hf release exists.
- **Codeforces / TACO** — L-status (reasoning-RL). PUBLIC: Codeforces problems are public (license varies); TACO is an open benchmark (Apache-2.0 on HF). BANKABLE, cost small (<1GB), license-clean for curation rows.
- **Open math/science** — L-status, no named set. Public: OpenMathInstruct-family, GSM8K/MATH (research/CC) exist — LICENSE-CHECK per set; not Flash-confirmed.
- **NExtLong / EntropyLong** — L-status ONLY (both cited as long-context synthesis influence). PATCHED-IN, not training corpora; bank only the papers (research refs), not a dataset.
- **DataComp-LM** — L-status (data-curation influence). PUBLIC dataset on HF (CC and MIT subsets) — bankable ~TB-scale; custody cost = drive bandwidth, not license (mostly open).
- **Agent/terminal trajectories** — L-status, referenced NOT released. The 10K envs / 1K concurrent rollouts are VENDOR-INTERNAL. NOT bankable as a set; the trajectory/RECEIPT pattern is our mirror (MIRROR-class, estate doctrine), not a custody object.

CUSTODY RULING per WEIGHTS_PLAN Phase 5 "datasets banked alongside each checkpoint": bank only the L-status PUBLIC sets (TACO, DataComp-LM, CF problems, math sets) with per-revision license passports; label every set lineage-evidence, never Flash-training. All Flash-specific rows go in the unknowns ledger, $0 cost, not hoarded.

## 3) Passport schema delta — MODEL_ATLAS_PASSPORTS
Propose two top-level fields (drop section "What this means for our model library" supports both):

```json
"lineage_evidence": [
  {"component":"flash_base","class":"P","detail":"new base model, not distilled","source":"zai/flash-release"},
  {"component":"swe_issue_pr","class":"L","detail":"~10M issue-PR pairs, ~160B tok (GLM-5)","source":"glm5-report/2602.15763"},
  {"component":"reasoning_rl","class":"L","detail":"Codeforces/TACO/synthetic CP","source":"glm5-report"},
  {"component":"flash_data_mix","class":"U","detail":"exact % UNDISCLOSED","source":null}
],
"unknowns": [
  "flash data-source percentages",
  "dataset licenses + doc counts",
  "dedup/contamination thresholds",
  "flash pretrain/mid-train token schedule",
  "teacher-model mixture",
  "SFT dataset sizes",
  "RM architecture/training data",
  "number+duration of RL runs",
  "total training FLOPs",
  "hardware hours + energy",
  "safety-tuning mixture",
  "flash checkpoint <-> GLM-5 relation",
  "per-component ablation provenance"
]
```
- `class`: P/L/U as in §1 — machine-usable for atlas build.
- `.source` nullable when UNKNOWN; never fabricate.
- Vault law preserved: passports still gate on sha256-complete + license (MODEL_VAULT_MANIFEST exec-law 1); lineage_evidence/unknowns are META additions, not replacement of artifact hashes.
- GLM-5.3-Flash existing atlas row (zai/glm-5.3-flash@characterized) gets these two fields backfilled in the next atlas pass.

## Bottom line
Drop downgrades the Phase-5 "distilled Flash" assumption to UNPROVEN (new base model instead), narrows bankable data to L-status PUBLIC sets (TACO/DataComp-LM/CF/math), and demands each passport carry a lineage_evidence + unknowns ledger. $0 custody now; drive only for DataComp-LM-scale public sets.
