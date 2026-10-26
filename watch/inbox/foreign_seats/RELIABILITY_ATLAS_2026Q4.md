# The Free-Tier & Edge Model Reliability Atlas
**Edition:** 2026 Q4 (Generated: 2026-10-23T10:29:11Z)  
**Dataset Digest:** `SHA256:7ce01c11c00fe99e`  
**Publisher:** Sovereign Estate Intelligence & Congress Process Organ  

---

## 1. Executive Summary & Fleet Metrics

- **Total Swarm Waves Evaluated:** 181
- **Total Invocations Fired:** 3,899
- **Total Successful Landings:** 1,255
- **Aggregate Yield Rate:** **32.19%**
- **The Negative Space Void:** **67.81%** (Upstream timeouts, 429 cliffs, socket disconnects)
- **Audited Traces with Reasoning Bleed:** 3 instances

---

## 2. Model Fleet Reliability Matrix

| Model Name | Landings | Fleet Share | Leak Rate | Grade | Empirical Failure Mode |
|---|---|---|---|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b` | 492 | 39.2% | 1.1% | **A (High Throughput)** | Stable token-budget transition; low rate-limit drop frequency |
| `dots-studio/dots-3-note-preview` | 328 | 26.1% | 0.0% | **A (High Throughput)** | Stable token-budget transition; low rate-limit drop frequency |
| `nvidia/nemotron-3.5-lightning` | 219 | 17.5% | 0.6% | **A (High Throughput)** | Stable token-budget transition; low rate-limit drop frequency |
| `poolside/laguna-s-2.1` | 152 | 12.1% | 0.0% | **B (Standard)** | Standard open-weight throughput; moderate 429 volatility |
| `poolside/laguna-xs-2.1` | 57 | 4.5% | 0.0% | **B (Standard)** | Standard open-weight throughput; moderate 429 volatility |
| `apodex/apodex-1.1-mini` | 5 | 0.4% | 0.0% | **B (Standard)** | Standard open-weight throughput; moderate 429 volatility |

---

## 3. The 12-Line Mechanical Linkage (Drop-In Solution)

```python
import json, re

def sanitize_stream(raw: str) -> dict:
    """Mechanical socket filter: strips leaked reasoning and enforces JSON closure."""
    cleaned = re.sub(r'(?s)<think>.*?</think>', '', raw)
    cleaned = re.sub(r'(?s)^(?:Thinking Process:|Reasoning:).*?\n\n', '', cleaned.strip())
    match = re.search(r'(\{.*\})', cleaned, re.DOTALL)
    if not match:
        raise ValueError('Mechanical filter tripped: No JSON object bounded in stream.')
    return json.loads(match.group(1))
```

---

## 4. Commercial License & Inquiries

- **Full Quarterly JSONL Feed:** $99/quarter (includes weekly automated diffs).
- **48-Hour Model Stack Audit:** $1,500 fixed PO (50-probe stress test on client infrastructure).
- **Contact:** Dispatch receipt via Diplomatic Pouch.
