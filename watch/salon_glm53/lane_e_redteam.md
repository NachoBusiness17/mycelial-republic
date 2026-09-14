# SALON E — GLM-5.3 Lineage Red-Team / HOT-gate lens
source: /board/GLM53_LINEAGE_DROP_20260901.md (operator-authored) + task-supplied claims
rule: quotes = UNVERIFIED unless probed; ≤40 lines; board-only; no novel.

## Claim classification (per load-bearing item)

| # | Claim | Class | Basis |
|---|-------|-------|-------|
| 1 | 3× lower attention compute (vs GLM-5) | **vendor-reported** | release blog only; no arithmetic/repro |
| 2 | 4.4× lower KV-cache (vs GLM-5) | **vendor-reported** | release blog only; no audit |
| 3 | 30T-token multimodal corpus | **vendor-reported** | single release-sentence; no %/licenses/schedule |
| 4 | ~10M issue–PR pairs / 160B tokens | **citation-not-proof** | GLM-5 report (not Flash-specific) |
| 5 | Ox Alpha anonymous pre-release eval on CN accelerators | **vendor-reported** | release + GLM-5 report; separate from Pony Alpha |
| 6 | GLM-5.3 beats GPT-5.6 Sol + Claude Fable 5 (Together post) | **citation-not-proof / UNVERIFIED** | NOT in drop; no fetched bytes in receipts — no source bytes held |
| 7 | "new base, not distilled" | **vendor-reported** | release assertion; contradiction-corpus: GLM-5 report describes "cross-stage distillation" stage + checkpoints unconfirmed |

## Must-NOT-reach-operator-as-fact (probe = settle)

- **#2 4.4× KV / #1 3× attention** → probe: run Flash vs GLM-5 same long-context workload (32K/250K/1M), measure peak KV + FLOPs. Until then: vendor-reported only.
- **#3 30T corpus** → probe: cannot be independently settled from weights; probe = model-card/licenses page deref (confirm it exists verbatim); treat any composition % as UNVERIFIED.
- **#4 10M pairs / 160B tok** → probe: read GLM-5 arxiv §4 (already cited) to confirm it's family-level, not Flash; this is lineage evidence, not Flash disclosure — do NOT attribute to Flash.
- **#6 Together benchmark claim** → probe: web_fetch the Together post + result tables; TWO-strike if fetch fails. Highest-risk item: it is a third-party marketing claim with zero held bytes. BLOCKED status until probed.
- **#7 "not distilled"** → probe: weigh against GLM-5 report's own "cross-stage distillation and regression checks" stage + "exact checkpoint relationship undisclosed"; assert as vendor-claim, flag contradiction.

## GLM-4.5 accounting discrepancy — PRESERVED, not smoothed
- GLM-4.5 report: **23T tokens across multi-stage training** (arXiv:2508.06471).
- Z.AI docs: **15T for initial general-domain pretraining**, then targeted fine-tuning (docs.z.ai/guides/llm/glm-4.5).
- Holding: may be different stages/conventions; NOT reconciled. Do not collapse into one "GLM-4.5 was trained on X tokens" fact for the operator.

## Ox Alpha precedent → what it licenses for our anonymous-eval play
- Precedent: Z.AI ran a de-identified pre-release ("Ox Alpha") under real traffic on CN accelerators — proves industry norm of shipping pre-release weights for live anonymous eval, separate-track from final naming.
- Licenses us to: run our own anonymous-eval harness against a pre-release/renamed model without manufacturer coordination; use synthetic traffic + receipt pass to avoid polluting real lanes.
- Does NOT license: pretending OUR eval is "official," claiming manufacturer endorsement, or posting results under Z.AI's name. Keep our eval receipts self-identified (board-side, not vendor-side).

## Bottom line
5 of 7 are vendor-reported; #4 is family-citation; #6 is UNVERIFIED-with-no-bytes (highest red flag); #7 carries an internal contradiction. No claim here is independently-verifiable from current held bytes. Operator needs probes (above) before any of these reach a load-bearing decision.
