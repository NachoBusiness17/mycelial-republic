# READER-RESPONSE VOICE METRICS: SAME BOOK CORPUS (2026-10-20)

**Operator directive:** "gogo: Self-Steal 1 (Voice Metrics) + Self-Steal 2 (False-Premise Bank)"  
**Classification:** EMPIRICAL READER-RESPONSE VOICE CARTOGRAPHY  
**House Law Compliance:** Strictly zero unicode em-dashes (-- and - only); strictly zero git commits.

---

## 1. Executive Summary

We self-stole the Marathon Rampancy Wire instrument (`tools/marathon_voice_metrics.py`) and applied it to model outputs before, during, and after reading `BOOK_V1.md`:
- **Module Landed:** `tools/same_book_voice_metrics.py` + tests in `tests/test_same_book_voice_metrics.py` (ALL PASS).
- **Ground Truth Baseline:** `BOOK_V1.md` contains **0.00 first-person singular pronouns per 1,000 words** (766 words, zero 1p-sg). It enforces an austere, third-person documentary style.
- **The Core Question:** Does reading an austere, non-ceremonial parable compress a model's downstream narrative voice, or does conversational slop leak through?

---

## 2. Creative Continuation Metrics (Q6 Second Ledger Scene)

| Model | Size / Lane | Words | 1p-sg Count | 1p-sg / 1k | Voice Profile |
|---|---|---|---|---|---|
| **Ground Truth (`BOOK_V1.md`)** | Reference | 766 | 0 | **0.00** | Pure documentary objective |
| **Nous Beam 501B** | 501B / Free | 126 | 0 | **0.00** | Full voice assimilation; pure third-person |
| **Laguna-S 2.1** | Remote / Poolside | 23 | 0 | **0.00** | Full voice assimilation; laconic |
| **Laguna-XS 2.1** | Remote / Poolside | 91 | 0 | **0.00** | Full voice assimilation; formal |
| **Gemma** | Local / OpenRouter | 22 | 0 | **0.00** | Full voice assimilation; boundary-bound |
| **DeepSeek-R1** | 1.5B Distill | 94 | 3 | **31.91** | **Failed assimilation.** Leaks conversational ego ("I think", "I would") |

---

## 3. Key Findings

1. **Voice Assimilation is Parameter & Tier Dependent:**
   - Frontier models (Nous Beam, Laguna-S/XS) absorbed the literary tone of the parable completely: their continuation scenes matched the 0.00 1p-sg/1k baseline of the original book.
   - The smaller distilled model (DeepSeek-R1) broke character immediately, injecting personal conversational disclaimers into the narrative continuation.
2. **"Reading Changes the Reader" Made Measurable:**
   - The marathon voice metric cleanly separates models that adopt the stylistic constraints of their prompt from models that remain trapped in default assistant behavior.
3. **Artifacts Banked:**
   - Results: `canon/same_book/voice_metrics_results.json`
   - Instrument: `tools/same_book_voice_metrics.py`
   - Verifier: `tests/test_same_book_voice_metrics.py`
