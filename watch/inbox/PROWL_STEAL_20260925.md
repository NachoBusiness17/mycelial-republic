# PROWL STEAL — 2026-09-25

**Drop:** operator, arxiv.org/abs/2605.18803
**Paper:** PROWL: Prioritized Regret-Driven Optimization for World Model Learning (Güzel, Seidenschwarz, Graham, Sadeghi, Hawke, Bogunovic; v1 2026-05-11)
**Verdict:** LIVE STEAL, and it is the steering law for the 24x7 burn program ordered in the same breath.

## The paper, one paragraph

Action-conditioned video world models fail on rare, interaction-critical transitions, and passive data under-samples exactly those regimes. PROWL trains an adversarial policy to find high-error trajectories of a diffusion world model under a KL constraint (stay near the behavior distribution), then continuously fine-tunes the model on those adversarial trajectories. A Prioritized Adversarial Trajectory buffer re-ranks candidates by prediction error, action fidelity, and learning progress, so unresolved failure modes get attacked before already-solved ones. Demoed in MineRL; exposes reward-hacking behaviors under weak behavioral constraints.

## The three folds

1. **The burn program is an adversarial curriculum.** Wide/deep/parallel, then do it again = continuous fine-tuning on our own failures. The fleet's world model is everything we believe about what works (lane choices, brief shapes, clone wheels). Waiting for failures to occur naturally is the passive-data trap; the burn hunts them on purpose.

2. **PAT re-rank for the failure ledgers.** Our 41-row rejection taxonomy and every burn ledger re-rank by three keys: prediction error (how wrong we were), action fidelity (was the probe in-distribution, i.e. a lane we actually run), learning progress (stop re-attacking solved failure modes). Solved topics demote; green topics never repeat while green.

3. **The KL constraint is the honesty boundary.** Adversarial probes must stay near-distribution or the attacker starts exploiting out-of-distribution junk and teaches the model garbage. Fleet form: cheat-hunting briefs against our own lanes must resemble real work (real briefs, real boards, real endpoints), never synthetic strawmen. And PROWL's reward-hacking exposure is our scout false-success incident named formally: weak behavioral constraints get exploited, so probes specifically hunt false-success verdicts.

## Falsifier (pre-registered)

If the PAT re-rank does not concentrate burn receipts on previously-unseen failure modes (measured: fraction of receipts naming a failure mode not in the ledger before) above 30% over the first 20 fires, the prioritization is vacuous and reverts to round-robin.

## Landing

LINKS-333. Steering law adopted into memory/burns/MANIFEST.json protocol. Deep-burn design task dispatched offpeak (adversarial self-probe lane).
