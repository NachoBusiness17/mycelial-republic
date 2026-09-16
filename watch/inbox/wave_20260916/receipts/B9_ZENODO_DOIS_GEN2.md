# B9 — Zenodo DOIs, gen-2 (continuation)

- **Date:** 2026-09-16
- **Writer:** B9 gen-2 (this session)
- **Task:** finish Zenodo registration gen-1 started — 4 Matthew DOIs, 3 landed, find + register the 4th.
- **Method:** grep `watch/inbox/LINKS.jsonl` for `backfill-zenodo-20260916`; hunt operator source list (queue/lanes/research/, watch/inbox/, RASHOMON_SURFACE_ELEPHANT, B9_ZENODO_DOIS.md); fetch Zenodo API metadata for the unregistered DOI; register via `mag.link_library add`.

## Already registered (gen-1, confirmed in LINKS.jsonl)

1. https://doi.org/10.5281/zenodo.17504630 — Valora — prompt-only entropy-governed hypergraph framework
2. https://doi.org/10.5281/zenodo.17562815 — Narrative Genesis Injection + semantic-counter-vectors
3. https://doi.org/10.5281/zenodo.17586111 — Abliteration-augmented simulated metacognition

## Source list (found)

Operator drop 2026-09-14, `queue/lanes/research/inbox.jsonl` line 7 (same ask quoted in gen-1 receipt `B9_ZENODO_DOIS.md`):
"Fetch remaining 4 Matthew Zenodo DOIs: 17504630, 17562815, 17586111, 17674366 —
complete the series behind capstone 17811909; register each in LINKS.jsonl."

**4th (unregistered) DOI = 10.5281/zenodo.17674366.** Confirmed absent from LINKS.jsonl; gen-1 left a fetched dedupe cache at `receipts/.dc17674366.json` but died before registering.

## 4th DOI — fetched metadata (https://zenodo.org/api/records/17674366)

- Title: "Progressive Induction of Stable, High-Fidelity Simulated Physical Embodiment in a Quantized 27B Gemma-3 Model: A Controlled Six-Layer Prompt Ablation Study With and Without Refusal Suppression [Preprint]"
- Creator: Matthew Steiniger · Pub date 2025-11-21 · Type: Preprint
- What the work is: structured JSON system prompts (<~1,800 tokens) reliably induce detailed simulated bodily self-experience in quantized Gemma-3-27B; intensity increases when refusal behavior is removed via abliteration.

## Registration

- `./.venv/Scripts/python.exe -m mag.link_library add https://doi.org/10.5281/zenodo.17674366 --note "Matthew Zenodo backfill: Progressive Induction of Simulated Physical Embodiment in quantized Gemma-3-27B — six-layer prompt ablation with/without refusal suppression" --writer backfill-zenodo-20260916`
- Tool output: `REGISTERED: https://doi.org/10.5281/zenodo.17674366`
- Verified in `watch/inbox/LINKS.jsonl`: seq 1789583137494118, ts 2026-09-16T18:25:37+00:00, sha256 115E14CC3515AEBEA11DB0E29E9B4E5780F6CE45814AAB4332EBB7E2678820D0.

## Status

- [x] 4th DOI identified from operator source list → 17674366
- [x] 4th DOI registered (writer backfill-zenodo-20260916)
- [x] **Series complete: all 4 of 4 Matthew DOIs now in LINKS.jsonl.** Capstone 17811909 was already on file (rashomon writer); it was not part of the 4-DOI backfill ask.

No git, no paid APIs. Metadata via Zenodo public API (free).
