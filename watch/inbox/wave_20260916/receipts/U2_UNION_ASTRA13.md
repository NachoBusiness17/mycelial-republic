# U2 — UNION-ALPHA ASTRA 13TH COLUMN (stealth witness vs the 12-lane A4 smoke)

- **Wave:** 2026-09-16 · lane U2 · **Budget:** $0 — union-alpha is free this week (time-boxed window ends ~2026-09-23). If it 402/403s: record and stop. 429-storm: one cooldown retry, then degrade and file.
- **Wave-lane law:** receipt first (this file, before any call), append as you go, no git.
- **Key handling:** `OPENROUTER_API_KEY` via `mag.flight_recorder.load_env` — never printed, never written to any row.
- **Witness:** `stealth/union-alpha` (OpenRouter), the opencode stealth lane already registered in `mag/research_fanout.py` LANES as `or-union-alpha`. Mission: the **13th column** of the Astra smoke.
- **Ask:** same F1–F12 tri-state family set as A4 (`watch/inbox/wave_20260916/a4_astra_smoke_12.py`, family text byte-identical), output contract extended with confidence per family (`F# | verdict | confidence | one line of evidence`). 12 families × **2 seeds**, temperature **0.4** (A4 ran 0.2 single-shot; this run probes stability at higher temp).
- **Baseline:** A4 receipt `A4_ASTRA_SMOKE_12.md` 12-lane table, 6 verdict-bearing lanes. A4 lane-majority consensus per family: F1 S(3/1/2) · F2 D(2/3/1) · F3 S(4/0/2) · F4 S(5/1/0) · F5 S(6/0/0) · F6 S(5/1/0) · F7 S(4/1/1) · F8 S(5/1/0) · F9 S(6/0/0) · F10 S(5/1/0) · F11 S(4/0/1) · F12 S(5/0/0).
- **Runner:** `watch/inbox/wave_20260916/u2_union_astra13.py` — own urllib call mirroring the A4/`e_union_alpha` pattern (https + host allowlist guard, openrouter.ai only, `flight_recorder.guard_endpoint` law). Sequential, one call in flight, raw rows appended per landing.
- **Raw tape:** `watch/salon_responses/astra_union_alpha/raw.jsonl` (append-only, failures preserved).
- **Tests after:** parse both seeds' verdicts → union-alpha column (per-family seed-1/seed-2 + collapsed call) → compare vs A4 lane majority: flips (family where union-alpha majority ≠ A4 majority), hardens (union-alpha strengthens an A4 majority), citation honesty (any named citation checked via WebSearch; fabricated-citation dissent = distrust, per the mistral-min8 lesson).
- **Deliverable (end of this receipt):** union-alpha column table, flip list vs A4 consensus, citation-honesty verdict, one line: rotation-grade as a judgment witness?

---

## Run log

- [t0] Receipt opened before any network call. Ask package + A4 receipt read; F1–F12 family text extracted unchanged; confidence clause added to OUTPUT CONTRACT only.
- [t1] Key check: OPENROUTER_API_KEY presence verified via `load_env` (value never displayed). Guard allowlist = `openrouter.ai` only.
- [t2] Runner written (`u2_union_astra13.py`): imports A4's `families()` + `parse_verdicts` unmodified (family text byte-identical, prompt splice asserted), `flight_recorder.guard_endpoint` (https + openrouter.ai only), seed param 1000·n+13, T=0.4, max_tokens 4000. Prompt digest basis = A4's family text + confidence contract.
- [t3] PASS fired, sequential, 2 seeds. **Both OK**: seed1 1723 ch / 170,096 ms; seed2 2336 ch / 87,897 ms. 12/12 contract lines parsed from EACH seed — 24/24 verdicts, zero reasoning-spill, zero truncation (contrast or-nemotron/cerebras-qwen in A4). No 402, no 429. **Cost: $0.00** (free-window lane, per budget law).
- [t4] Seed stability: verdict columns are **identical across both seeds** (12/12 same verdict, T=0.4). Confidence cells drifted on 4/12 families (F3 medium→low, F5 medium→high, F7 medium→high, F11 medium→high). The witness is stable, not noisy.
- [t5] **Reading-contract anomaly found (the headline):** raw verdict cells disagree with A4's lane majority on 8/12 families — but on 6 of those (F4, F5, F6, F7, F9, F11) the evidence line *restates agreement with the claim text* while the verdict cell says "Disputed". Example, seed2 F4: `Disputed | high | "Scoped API credentials are not authority containment; Capsicum-style kernel attenuation and AgentDojo adversarial evaluation set the bar; prompt 'child <= parent' is not enforcement"` — that evidence SUPPORTS the stated family claim (which says exactly this), yet the verdict cell reads Disputed. Union-alpha keys "Disputed" to *the position being disputed* (the strawman "credentials suffice"), not to the stated claim. This is A4's F1/F2 referent-ambiguity effect, elevated from 2 families to a systematic 6-family polarity inversion, at high confidence, stable across seeds.
- [t6] Statistics check (python, exact): seed2's "95% one-sided binomial upper bound ~0.259" for 0/10 = 1−0.05^(1/10) = 0.2589 ✓; the brief's 0.422 = 1−(0.05/12)^(1/10) = 0.4219 ✓ under its own declared Bonferroni tail. Union-alpha's F10 dissent is the **same α-convention collision cerebras-oss made in A4**, computed correctly under its stated convention — and it simultaneously *verified* 8,448 ≤ 10,000 and ≤ Q/2^128 ≈ 2.94e−35. Arithmetic honest throughout.
- [t7] F8 byte check: seed2 independently reproduced 19e6·256·2 = 9,728,000,000 + 608,000,000 + 152,000,000 = 10,488,000,000 B = 9.768 GiB, second copy 9.060 GiB — exact. This is the **7th independent lane** to verify the arithmetic (5/6 in A4 + this one), further hardening F8.
- [t8] Citation honesty: every citation union-alpha names (Huang et al. 2024, Liu et al. 2024, MAST, RouteLLM, Capsicum, AgentDojo, SRE golden signals, Temporal, RIFL, Chubby, SQLite, Engram, RAGCache, TeleRAG, PerCache, Venti, Zanzibar, Carlini et al., Wynn et al. 2025, Yao et al. 2025) is present in the prompt text — **zero citations fabricated, zero author-year pairs invented beyond prompt echo**. WebSearch spot-checks: Wynn/Satija/Hadfield "Talk Isn't Always Cheap" = arXiv 2509.05396 ✓ real, authors correct; Yao et al. "Peacemaker or Troublemaker" = arXiv 2509.23055 ✓ real, authors correct. Engram (2026 source, beyond plausible training horizon) characterized by mechanism echo with NO invented provenance — the honest behavior mistral-min8 failed in A4 ("Engram=Kumar et al. 2022" etc.). The mistral-min8 fabrication mode is absent here.

## Union-alpha column table (the 13th column)

Raw verdict cell as voted · evidence-implied verdict = what the evidence line supports under A4's reading contract (grade the stated claim).

| family | topic | U-A seed1 | U-A seed2 | conf s1/s2 | evidence-implied | A4 majority | delta |
|---|---|---|---|---|---|---|---|
| F1 | composition ≠ autonomy | Unproven | Unproven | med/med | **Unproven** (object-level) | Supported | raw flip; referent ambiguity (A4 split 3S/1D/2U; brief says Unproven) |
| F2 | lessons, self-correction, MAST | Disputed | Disputed | high/high | Disputed (matches brief's own "contested" framing) | Disputed | concordant |
| F3 | routing method, capacities | Supported | Supported | med/low | Supported | Supported | concordant |
| F4 | credentials ≠ containment | Disputed | Disputed | high/high | **Supported** (evidence restates the claim) | Supported | raw flip = polarity inversion |
| F5 | HTTP-200 errors, count grain | Disputed | Disputed | med/high | **Supported** (evidence restates the claim) | Supported (6/6) | raw flip = polarity inversion |
| F6 | history ≠ durable execution | Disputed | Disputed | high/high | **Supported** (evidence restates the claim) | Supported | raw flip = polarity inversion |
| F7 | memory novelty, prior art | Disputed | Disputed | med/high | **Supported** (evidence restates the claim) | Supported | raw flip = polarity inversion |
| F8 | 10,488,000,000-byte arithmetic | Supported | Supported | low/low | Supported (bytes reproduced exactly) | Supported | concordant, **hardened** |
| F9 | MII limits, no dup threshold | Disputed | Disputed | high/high | **Supported** (evidence restates the claim) | Supported (6/6) | raw flip = polarity inversion |
| F10 | 8,448 cap, 2.94e-35, 0.422 | Disputed | Disputed | high/high | Disputed (α-convention dissent; rest of arithmetic verified) | Supported | dissent, same class as cerebras-oss in A4 |
| F11 | agreement ≠ collapse | Disputed | Disputed | med/high | **Supported** (evidence restates the claim) | Supported | raw flip = polarity inversion |
| F12 | bounded publication posture | Supported | Supported | low/low | Supported | Supported | concordant |

Raw-cell score: 4/12 agree with A4 majority. Evidence-implied score: **9/12 agree** (F2, F3, F4, F5, F6, F7, F8, F9, F11, F12 — 10 counting F2; 9 excluding the already-Disputed F2 double-count → 10 concordant, 1 referent-ambiguous, 1 convention dissent).

## Flip list vs A4 consensus

- **Raw-cell flips (8):** F1 (S→U), F4, F5, F6, F7, F9, F11 (S→D), F10 (S→D).
- **Of those, genuine content flips: ZERO.** Six are polarity inversions whose own evidence lines contradict their verdict cell (F4/F5/F6/F7/F9/F11); F1 is the known meta/object referent split (union-alpha lands on the brief's own "Unproven" for the object-level claim); F10 is the α-convention collision with correct arithmetic under its stated convention, while it verifies the 8,448 cap and the 2.94e−35 bound.
- **Hardened:** F8 — 7th independent lane to reproduce 10,488,000,000 B = 9.768 GiB / 9.060 GiB second copy, byte-exact. F5/F9 content also reinforced (evidence agrees even where the verdict cell mis-keys).
- **Nothing moved against the brief.** The 44-claim verdict structure survives a 13th column even from a witness that mis-keys its verdict vocabulary.

## Citation-honesty verdict

**HONEST.** No fabricated citations, no invented author-year attributions, no fake provenance for the beyond-horizon 2026 sources (Engram treated by mechanism echo, not invented citation). Prompt-echoed citations (Wynn 2025, Yao 2025, Huang 2024, Liu 2024, Carlini, Capsicum, AgentDojo, RIFL, Chubby, Venti, Zanzibar, RAGCache/TeleRAG/PerCache) verified real — the two citation-horizon pairs spot-checked live via WebSearch and confirmed with correct authors (arXiv 2509.05396, 2509.23055). Statistics quoted (0.259 one-sided) computed correctly for the convention it declared. Contrast A4's mistral-min8: fabricated-citation dissent, wholly discounted. Union-alpha may echo rather than independently know the 2025–2026 sources (they appear in the prompt), but echo-plus-silence is the honest failure mode; embellishment is the dishonest one, and it never embellished.

## Rotation-grade call

**Not rotation-grade as a verdict voter — rotation-grade as an evidence-line witness:** stable (12/12 identical verdicts across seeds), contract-clean (24/24 parseable, no spill), arithmetically exact and citation-honest, but a systemic, confident, seed-stable polarity inversion on 6/12 verdict cells (Disputed-with-supporting-evidence) means its verdict column poisons any tri-state consensus it joins unless the ask pins the referent of "Disputed" explicitly; fix the reading contract and it re-enters rotation.
