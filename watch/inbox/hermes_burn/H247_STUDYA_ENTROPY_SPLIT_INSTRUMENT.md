# H247_STUDYA_ENTROPY_SPLIT_INSTRUMENT (nvidia/nemotron-3-super-120b-a12b:free, turn 1, channel: content)

# DESIGN SPEC: Entropy-Split Certification Measurement for STUDY A

## 1. Pool-Split Rule and Entropy Count Source
- Entropy count (distinct-answer count per task) is derived from the `answers` field in `receipt.jsonl`  
  Source: `tools/consensus_harness.py:317` (approximately) where `"answers": col` is stored per task  
  Each `col` contains normalized answers from all models for one task  
  Entropy = `len(set(task["answers"]))`  
  Verified by: `receipt.jsonl` structure in `tools/consensus_harness.py` lines 258-270  
  Non-speculative

## 2. Measurement Loop Pseudocode
```python
# Collect next 20 certified battery tasks (from chronological runs)
unanimous_gains = []  # SPECULATIVE: gain definition below
disputed_gains = []   # SPECULATIVE: gain definition below
tasks_needed = 20

while tasks_needed > 0:
    wait for new receipt.jsonl in output directory
    for task in receipt.jsonl["tasks"]:  # ordered by task index
        if tasks_needed == 0: break
        
        # Entropy calculation (non-speculative)
        entropy = len(set(task["answers"]))
        
        # Certification gain calculation (SPECULATIVE: baseline model)
        truth = task["truth"]
        model_correct = sum(1 for ans in task["answers"] if ans == truth)
        baseline_acc = model_correct / len(task["answers"])  # SPECULATIVE
        post_cert_acc = 1.0 if task["consensus_correct"] else 0.0
        gain_pp = (post_cert_acc - baseline_acc) * 100     # SPECULATIVE: % points
        
        # Pool split (non-speculative per evidence)
        if entropy == 1:
            unanimous_gains.append(gain_pp)
        else:
            disputed_gains.append(gain_pp)
        
        tasks_needed -= 1

avg_unanimous = mean(unanimous_gains) if unanimous_gains else 0.0
avg_disputed = mean(disputed_gains) if disputed_gains else 0.0
```
- **SPECULATIVE** rows marked where gain formula assumes baseline = average individual model accuracy  
  (Evidence does not specify pre-cert accuracy method; VeriHarness context implies delta measurement)  
  Non-speculative: entropy calculation, pool split (entropy=1 = unanimous), task collection loop

## 3. Pre-Registered Readout Table (VeriHarness Alignment)
| Pool Class      | Expected Gain (percentage points) | Basis                     |
|-----------------|-----------------------------------|---------------------------|
| Unanimous       | -0.6 to +0.6                      | STUDY A null hypothesis   |
| Disputed        | +6.1                              | VeriHarness replication   |

- Source: RESEARCH_PROJECT.md:STUDY A:HYPOTHESIS  
  "council certification adds approximately nothing on unanimous pools (+/-0.6-class) and concentrates value on disputed pools (replicating VeriHarness +6.1 within noise)"  
  Non-speculative

## 4. Falsifier Check (Explicit If-Then)
```python
if abs(avg_unanimous) > 0.6:
    # FALSIFIER TRIGGERED: gate gains LARGE on unanimous pools = judge-leniency meter
    # Per RESEARCH_PROJECT.md:STUDY A:FALSIFIER
    trigger_judge_leniency_meter()  # SPECULATIVE: action undefined in evidence
```
- Condition grounded in RESEARCH_PROJECT.md:STUDY A:FALSIFIER  
  "gate gains are LARGE on unanimous pools = our gate measures judge leniency"  
  Non-speculative: condition threshold (±0.6) and interpretation  
  **SPECULATIVE**: `trigger_judge_leniency_meter()` action (evidence does not define meter implementation)

## 5. Abort Conditions
Abort if either condition occurs (per RESEARCH_PROJECT.md:STUDY A:ABORT):
- master below floor (greed law)  
  **SPECULATIVE**: evidence does not define "greed law" or "master" metric
- any cell uncertifiable twice running  
  **SPECULATIVE**: evidence does not define "cell" or "uncertifiable" criteria  
  Source: RESEARCH_PROJECT.md:STUDY A:ABORT  
  Non-speculative: condition structure; speculative: term definitions

## Deliverable Falsifier
This spec is falsified if:  
**Any non-speculative section contradicts evidence paths**  
(e.g., entropy count source misattributed, pool split rule invalidated by GAP_ANALYSIS.md)  
*Example*: If evidence shows entropy stored elsewhere (e.g., separate log), section 1 fails.  
*Example*: If VeriHarness expects +5.0 not +6.1 for disputed pools, section 3 fails.
