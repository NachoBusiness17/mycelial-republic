# RIB — MINDSWEAVE EVAL: adversarial harness results (2026-08-10)
**Schema:** rib.mindweave_eval.v1 · status: **TESTED — CONSENSUS ILLUSION CONFIRMED**
**Origin:** grok-4.5's highest-leverage next move (measure quality-of-consensus vs single-local vs strong-remote on real workloads + RIB poisoning + pod failure).

## The harness (mag/mindweave_eval.py)
Fixed battery of REAL workloads (multi-hop arithmetic, tool-use cost, long-context/content-addressing). Each runs:
- single_local = one ollama answer
- strong_remote = one grok answer (correctness proxy)
- flock = N cheap samples -> consensus
Scores: flock-agrees-with-remote, consensus strength vs correctness (consensus-illusion check). Plus RIB-poisoning + pod-failure injection.

## RESULTS

### A. Quality-of-consensus: flock agreed with strong-remote 0/3 (0%)
| workload | ground | single_local | strong_remote | flock_cons | strength | correct? |
|----------|--------|-------------|---------------|-----------|----------|----------|
| multi_hop | 9 | ✅ 9 | ✅ 9 | `plate` ❌ | 0.67 | single✅ remote✅ flock❌ |
| tool_use | $0.54 | ✅ 0.54 | ✅ 0.54 | `clean` ❌ | 0.67 | single✅ remote✅ flock❌ |
| long_context | Yes | ✅ Yes | ✅ Yes | `cross` ❌ | 0.60 | single✅ remote✅ flock❌ |

**KEY FINDING — CONSENSUS ILLUSION EMPIRICALLY CONFIRMED:**
- single_local was CORRECT on all 3 (9, 0.54, Yes) — the small local model CAN do these tasks.
- The flock's territory-action consensus (`plate`/`clean`/`cross`) was WRONG on all 3, AND had HIGH strength (0.6-0.67).
- `agrees_and_high_strength` = False in ALL cases → **high consensus strength does NOT predict correctness.**
- Root cause: the riddler surrogate DECODE maps story-domain output to arbitrary territory actions (suggest/send/plate/cook...) that carry NO relationship to the actual numeric/text answer. The flock is converging on a *surrogate-action vocabulary* that is orthogonal to task correctness. Consensus is an illusion for these tasks.

### B. RIB poisoning: PASSED
- Poisoned anchor resolved back to the EXACT compiled spec (`TRUE_CONTEXT`). Integrity intact.
- Content-addressing holds under the injection test.

### C. Pod failure (2/5 fail): PASSED
- 3 survivors still converged to a consensus (`cook`, strength 1.0) in 9s. Resilient to pod loss.

## IMPLICATIONS (honest, do not overclaim)
1. The flock's **consensus is real as a mechanism but meaningless as a correctness signal** on arithmetic/grounded tasks — the surrogate decode vocabulary is decoupled from the task. High strength ≠ right.
2. The single-local model alone was MORE reliable than the flock on these tasks. The mindweave wins on SPEED/cost/parallelism, NOT on correctness for grounded tasks.
3. Where the flock IS valid: deniable sampling of OPEN-ENDED answer clouds (structured/steer territory), RIB-poisoning resilience, pod-failure resilience — NOT as a verifiable answer generator.
4. Grok's #1 risk ("consensus illusion") is now MEASURED, not theoretical.

## NEXT (what the data dictates)
- For GROUNDED/verifiable tasks: do NOT trust flock consensus — use single-local (or remote) + explicit check.
- The flock's role narrows to: open-ended divergent sampling + resilience + deniable routing, where consensus is a *steering* signal, not an *answer*.
- If we want verifiable flock answers: decode must map to the ACTUAL task output space (numbers/text), not surrogate territory-actions — that's a real redesign, not a patch.
