# B13 — codetaur KAN-continuity: confirm + extend

- **Wave:** 20260916 · **Lane:** B13 · **Writer:** zcode-wave-b13
- **Ask (from operator drop 20260914, queue/lanes/research/inbox.jsonl):** "Confirm + extend codetaur thread 2099236759825707232 (KAN continuity claim: fits function, breaks flow)" — witness 4 of RASHOMON_SURFACE_ELEPHANT_20260914.md, purpose: verify wording, collect prior art on KAN interpolation failure.
- **Pointer:** https://x.com/codetaur/status/2099236759825707232 (canonical_sha256 5C46E0EF…A555F, LINKS.jsonl seq 1789370679416060)

## Log (append as you go)

- [done] Searched queue/lanes/research/inbox.jsonl + watch/inbox (LINKS.jsonl, index_events.jsonl, INDEX.json) for "codetaur"/"KAN". Found: the ask line, the LINKS entry, and witness 4 in RASHOMON_SURFACE_ELEPHANT_20260914.md. No archived tweet text anywhere — witness 4 fragment is the only local wording.
- [done] Fetched the status via fxtwitter (api.fxtwitter.com/codetaur/status/2099236759825707232) — **POINTER DEFECT FOUND**: the ID resolves to a marble-maze/three.js post, not a KAN post. Text: "testing astra's parametric modeling capabilities by asking it to reconstruct these marble maze pieces from reference photos, and then use them in threejs to make a marble maze builder with box3d physics." Metadata: created 2026-09-13 20:40:20 UTC, 82,953 views, 62 replies, 16 quotes, author verified ("agentic coder, webgpu engineer, SWE @WindBorneWx", Palo Alto).
- [done] Recovery attempts for the true KAN post: fxtwitter `/thread` (returns root only, no replies), nitter.net / nitter.poast.org (empty), lightbrd.com / nitter.space (Cloudflare-gated), x-sou.com profile + status formats (no status pages), DuckDuckGo HTML (tweet not indexed; 3 days old), Bing (no X results), WebSearch (codetaur KAN combo returns nothing; only the marble-maze post is indexed for that window). **Verdict on recovery: the KAN wording cannot be verified against a live post with free tooling.** Either it was a reply/quote (unindexed) or the operator filed the viral marble-maze ID instead of the KAN post ID. Same honest status as witnesses 14–16: fragment on file, fetch thin, ledger says so.
- [done] Core claim stated (as recorded, witness 4): "Everyone hypes Kolmogorov-Arnold networks; nobody talks about what they break: *continuity*. You can fit the function and lose the flow — interpolate the weights, get nonsense gradients." Strongest steelman: KANs fit function values while the weight-space geometry carries no transferable continuous structure — spline coefficients live on input-adaptive, per-run grids, so checkpoint/model interpolation is not even basis-aligned; "copying the nodes does not copy the between."
- [done] Fact-check vs literature (arXiv export API, free):
  - KAN (Liu, Wang, Vaidya, Ruehle, Halverson, Soljačić, Hou, Tegmark — arXiv:2404.19756, 2024-04-30, v5 2025-02-09): learnable edge activations as B-splines (default degree k=3 → activations are C² smooth). Output-space continuity is FINE BY CONSTRUCTION; smoothness is the selling point vs ReLU. Grid extension exists precisely because each spline has a bounded grid domain.
  - KAN 2.0 (Liu, Ma, Wang, Matusik, Tegmark — arXiv:2408.10205, 2024-08-19): the real value is the science interface — feature discovery, modularity, symbolic formula extraction (prune → symbolify). Propose/verify ladder, not raw accuracy.
  - KAN or MLP: A Fairer Comparison (Yu, Yu, Wang — arXiv:2407.16674, 2024-07): at matched params/FLOPs, MLP wins on ML/CV/audio/NLP; KAN keeps an edge ONLY on symbolic formula representation. "Fits the function" is the small half.
  - 2025–2026 follow-ups: noise fragility confirmed (ER-KANs, arXiv:2608.14773: vanilla KAN test MSE degrades 7.9x under σ=0.1 noise vs 1.7x MLP); adversarial-robustness benchmark exists (KAN-Robust-Bench, arXiv:2608.21488); tabular mixed — KANs statistically beat MLPs on some structured-data tasks (arXiv:2607.13413); SLM-scale edge audit done, but apparent interpretability wins are partly low-capacity grid-2 basis artifacts (arXiv:2607.15525); the seam formalized — KART representation stability under bounded adversarial translations is an open problem with new constructive results (Dzhenzher et al., arXiv:2608.30710, 2026-08-31).
- [done] Extend — mechanism the thread missed (canon-relevant): **grid extension + symbolification = the KAN's built-in propose→verify ladder, i.e. symbolic regression as receipt.** The spline fit is the proposal; the extracted symbolic formula plus its declared grid range is the auditable artifact — checkable bytes, not a checkpoint. The interpolation failure the thread found is exactly why you never promote weights: each grid is a bounded pointer, and when residuals spike outside the grid you extend the grid and re-file (re-fit), you do not average old coefficients. Maps 1:1 to house law: model text can propose / only the switchboard authorizes; trust bytes not reports; residual + registry + leaf. Splines propose; receipts verify.
- [done] Verdict + citations filed below.

## Verdict

**OVERSOLD** — the seam is real where the thread aims it (weight-space interpolation across KAN checkpoints is meaningless because spline grids are run-adaptive, and noise fragility is now measured: 7.9x vs 1.7x MSE), but "breaks continuity" is false in output space (B-spline activations are smooth by construction) and "nobody talks about it" was already stale by 2026.

## Canonical citations (ready to file)

1. Liu, Ziming, et al. "KAN: Kolmogorov-Arnold Networks." arXiv:2404.19756 (2024-04-30; v5 2025-02-09). https://arxiv.org/abs/2404.19756
2. Liu, Ziming, Pingchuan Ma, Yixuan Wang, Wojciech Matusik, Max Tegmark. "KAN 2.0: Kolmogorov-Arnold Networks Meet Science." arXiv:2408.10205 (2024-08-19). https://arxiv.org/abs/2408.10205
3. Yu, Runpeng, Weihao Yu, Xinchao Wang. "KAN or MLP: A Fairer Comparison." arXiv:2407.16674 (2024-07-23; v2 2024-08-17). https://arxiv.org/abs/2407.16674

2026 extenders (verified same session, file if the lane wants them): ER-KANs arXiv:2608.14773 (noise fragility numbers); KANs for Small Language Models arXiv:2607.15525 (edge audit + grid-2 basis artifact caveat); Dzhenzher, S.V., et al. "Kolmogorov–Arnold against bounded translations" arXiv:2608.30710 (KART stability formalized).

## Defect to route back

The operator ask's status ID (2099236759825707232) points at the wrong post (marble maze, not KAN). Witness 4's KAN wording remains a fragment on file only — unverified against a live post. If the operator can re-supply the true ID (or confirm it was a reply), wording verification is a one-call fxtwitter fetch.
