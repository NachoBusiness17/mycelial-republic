# H247_A2_TOKEN_CUE_FAMILY_TABLE (anthropic/claude-haiku-4.5, turn 1, channel: content)

# RIB AMENDMENT BLOCK: TOKEN-CUE COLUMN + S1 BATTERY PROTOCOL
**Dated 2026-10-06, POST-DATUM to RIB_MODEL_GATES_20261001.md**
**Amend-never-rewrite: this block rides the existing per-animal harness profiles; the FAMILY_TABLE law text above is untouched.**

---

## (1) THE LAW IN ONE LINE

Token cue is a measured per-animal harness axis — a fixed starting phrase prepended to reasoning asks that recovers RL-trained performance on base models without training or parameter cost. Cue state correlates with hidden representations of distinct training-document types (2610.06851:abstract, "hidden state representations induced by different cues correlate with different document types from the training set"). Fixed cues ('.\n\nOkay' / 'Alright,') lift base-model pass@1 to RL-trained levels (2610.06851:abstract, "the cue '.\n\nOkay' raises Olmo-3-7B's MATH-500 pass@1 from 42% to 78%").

---

## (2) FAMILY_TABLE ROW SHAPE — TOKEN_CUE FIELD

**Add one column to every FamilyRecipe dataclass:**

```python
@dataclass
class FamilyRecipe:
    # ... existing fields ...
    token_cue: str = ""              # default empty = no cue injected
                                     # explicit string = prepended to reasoning asks
    token_cue_measured_date: str = "" # ISO8601Z when cue was last measured on this animal
    token_cue_notes: tuple[str, ...] = ()
```

**Shape precedent:** mirrors `thinking_control` (dict of extra_body params, explicit, measured, synced to memory/behavioral/animals). The `token_cue` field holds the literal string to prepend; empty string is the default (no cue state, no injection).

**Example rows (SPECULATIVE, S1 receipt not yet banked):**

```python
FamilyRecipe(
    key="gemma:2b",
    matches=("gemma:2b",),
    token_cue="",                    # BASELINE ARM: no cue, measured S1
    token_cue_measured_date="",      # no measurement yet
    # ... other fields ...
),

# SPECULATIVE S1 ARM 2: cue='.\n\nOkay'
FamilyRecipe(
    key="gemma:2b-cue-okay",
    matches=("gemma:2b",),           # same model, same matching logic
    token_cue=".\n\nOkay",           # explicit prepend
    token_cue_measured_date="2026-10-06T00:00:00Z",  # placeholder S1 receipt date
    token_cue_notes=(
        "S1 battery baseline arm 2 (token cues 2610.06851): "
        "42-item math subset, 3 arms (empty / '...Okay' / 'Alright,'), "
        "pass@1 and tokens/sec per arm, local route_chat",
    ),
),

# SPECULATIVE S1 ARM 3: cue='Alright,'
FamilyRecipe(
    key="gemma:2b-cue-alright",
    matches=("gemma:2b",),
    token_cue="Alright,",
    token_cue_measured_date="2026-10-06T00:00:00Z",
    token_cue_notes=(
        "S1 battery baseline arm 3 (token cues 2610.06851)",
    ),
),
```

**Non-example (what NOT to do):**
- Do NOT rewrite the existing deepseek row; add a new row with the same matches and a different key.
- Do NOT use `None` or omit `token_cue`; empty string is the default (the no-cue state).
- Do NOT carry `token_cue_measured_date` without a receipt: the field is void until S1 or a later battery lands.

---

## (3) S1 BATTERY PROTOCOL

**Name:** S1 Token-Cue Recovery Baseline (2026-10-06)  
**Instrument:** `tools/route_chat.py` (estate's sanctioned inference route, local)  
**Animals:** gemma:2b + two additional garden animals (TBD, from `tools/model_garden.py` current roster)  
**Test set:** one fixed ~50-item math subset (MATH-500 subset per 2610.06851, or equivalent local curated set; exact inventory in receipt)  

**Three arms (mutually exclusive per animal):**

| Arm | token_cue value | Description |
|-----|-----------------|-------------|
| A (baseline) | `""` (empty) | No cue prepended; base model state |
| B | `".\n\nOkay"` | Literal two-character period, two newlines, 'Okay' |
| C | `"Alright,"` | Literal word 'Alright' plus comma |

**Measurements per arm per animal:**

- **pass@1** (binary, %) — correctness rate on the 50-item subset (matching 2610.06851 MATH pass@1 metric; instrumental: LLM judge or symbolic correctness check, named in receipt)
- **tokens/sec** — throughput (completion_tokens / wall-clock seconds, mean across all items in arm)

**Execution:** Fire each (animal, arm, item) triple exactly once via `route_chat` with:
- `model=<animal_id>`, `max_tokens=4096` (fixed per arm), `temperature=0.8` (fixed)
- item prompt (from the fixed ~50 set)
- For arms B and C: prepend the `token_cue` string to the prompt text before sending

**Receipt shape (named `S1_CUE_RECEIPT`):**

```json
{
  "battery": "S1_token_cue_recovery_baseline",
  "date": "2026-10-06T14:30:00Z",
  "animals": [
    {
      "model_id": "gemma:2b",
      "arms": [
        {
          "arm": "A",
          "token_cue": "",
          "pass_at_1_pct": 34.0,
          "tokens_per_sec": 18.5,
          "item_count": 50,
          "judge": "symbolic"
        },
        {
          "arm": "B",
          "token_cue": ".\n\nOkay",
          "pass_at_1_pct": 56.0,
          "tokens_per_sec": 18.2,
          "item_count": 50,
          "judge": "symbolic"
        },
        {
          "arm": "C",
          "token_cue": "Alright,",
          "pass_at_1_pct": 48.0,
          "tokens_per_sec": 17.9,
          "item_count": 50,
          "judge": "symbolic"
        }
      ]
    },
    {
      "model_id": "<garden_animal_2>",
      "arms": [ ... ]
    },
    {
      "model_id": "<garden_animal_3>",
      "arms": [ ... ]
    }
  ],
  "source": "watch/inbox/s1_cue_battery_20261006.md",
  "notes": "All fires local via route_chat; math subset inventory in source; judge method per animal in arm detail"
}
```

**Positive example (arm separation is signal):**
- Arm A (no cue): 34% pass@1. Arm B ('.\n\nOkay'): 56% pass@1. Arm C ('Alright,'): 48% pass@1. Spread >10 percentage points → cue effect is not noise → S1 validates the law for this animal.

**Negative example (no arm separation):**
- All three arms: 42.0%, 41.8%, 42.2% pass@1. Standard deviation <1 point across arms. Throughput indistinguishable. On 2+ animals, this falsifies the cue column as theater (see FALSIFIER below).

---

## (4) FALSIFIER

**Measurement:** Run S1 on 2+ animals from the garden (gemma:2b mandatory + at least one other). For each animal, compare pass@1 across the three arms (A, B, C).

**Falsification condition:**
- On 2+ animals, arm separation in pass@1 is NOT statistically significant (e.g., all arms within ±3 percentage points, or p > 0.05 on a paired test).
- Tokens/sec shows no systematic difference across arms (all within ±5% of the mean per animal).
- The effect does not replicate: arm B or C consistently outperform arm A on the same animal subset.

**If falsified:** The `token_cue` column is removed from FAMILY_TABLE; S1 is marked as VOID; 2610.06851's finding does not transfer to this estate's animals and inference route. The amendment is struck.

**If validated:** S1 receipt is banked to `watch/inbox/s1_cue_battery_20261006/S1_CUE_RECEIPT.json`. FAMILY_TABLE rows are populated with best-performing cue per animal + measured_date. S2-S5 probes (see EVIDENCE section 2) are unblocked.

---

## AMENDMENT SCOPE & CONDITIONS

- **Applies to:** Every FamilyRecipe row in mag/inference_budget.py FAMILY_TABLE, backdated 2026-10-06 (S1 battery start date).
- **Does NOT apply to:** Existing thinking_control, forbidden_keys, floors, or uncap logic. Those rows stand untouched.
- **Moment:** This amendment takes effect when S1 receipt is filed. Until then, `token_cue=""` (no injection) on all animals.
- **Conditions:** 2610.06851 (arXiv abs page, 43,482 bytes, fetched first-hand 2026-10-06); cue effect only measured on the paper's animals (Olmo-3-7B, Qwen3-14B). S1 replicates on estate animals before the column is law.

---

## MARKED SPECULATIVE

All rows referencing S1 receipt and measured_date are marked SPECULATIVE until S1 fires and the receipt is banked. The law text itself (section 1) is grounded in 2610.06851:abstract (file:arXiv/2610.06851, lines abstract-to-introduction).
