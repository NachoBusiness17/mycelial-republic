# r-solomonoff-pretrain: Self-Play Pretraining with Zero Data (arXiv 2609.30063) - deep dive

Date: 2026-09-28. Method: every claim below was verified by fetching, during this ask, the arXiv abstract page and HTML v1 full text, the Hacker News Algolia API plus the item page, GitHub search and three repo pages (two community repos plus the authors' release, including the reproduction's REPORT.md), the HuggingFace model page and API, the alphaXiv page, and web searches. Items I could not verify are marked OWED.

## 1. Paper identity

- Title: "Self-Play Pretraining with Zero Data" (arXiv 2609.30063, cs.AI, cross-listed cs.CL). v1 only, submitted Thu 24 Sep 2026 16:23:01 UTC (881 KB source). No revisions. DOI 10.48550/arXiv.2609.30063.
- Authors: Aditya Cowsik, Kfir Dolev, Michael Y. Li, G. Bruno De Luca, Nourya Cohen, Noah D. Goodman, Yoav Levine. The abs page states "AC, KD, and MYL contributed equally; authors are listed alphabetically." The abs page itself lists no affiliations; Tel Aviv University and Stanford are the affiliations given in secondary coverage (the "AI可可AI生活" podcast listing, and Stanford AI Lab's own promo post "Can an LM, starting from random init (!!), learn to generate all of its pretraining data?").
- Core idea (from abstract + HTML v1): two models train together from random init with zero natural data. A generator is RL-trained to propose programs executed by a universal Turing machine (Brainf*ck-like, per the reproduction's reimplementation); a decoder-only Llama transformer learner does standard cross-entropy next-byte prediction on the program outputs. The generator targets the frontier of the learner's capability (adaptive curriculum), inspired by Solomonoff induction searching all computable data-generating processes. Transfer is tested cleanly because neither model ever sees natural data: zero-shot loss on natural datasets scales predictably with self-play compute.

## 2. Compute used

### Disclosed in the paper (HTML v1)
- Fixed maximum training budget: 34.36B tokens, context length 4096 across all scales.
- Model sizes: all experiments "confined to models below 25M parameters at a 4K context"; the downstream "pre-pretraining" test model is 24.4M parameters; released ladder runs 100k / 500k / 1M / 3M / 6M / 24M (six sizes, per the HuggingFace model card).
- Uniform-sampling baseline: 1.64e8 programs total, added at 1,024 new programs per round.
- Ensembling: K independent seeds per scale (K not stated); downstream warm-start runs use 4 seeds; hyperparameter tuning via coordinate descent on a geometrically-spaced grid over learner LR, generator-to-learner LR ratio, batch size, and KL coefficient beta; corpus evaluation over 16 generator checkpoints, 4 seeds per endpoint.

### Not disclosed (OWED)
- No hardware statement anywhere in the HTML v1 text: no GPU names, no GPU count, no GPU-hours, no wall-clock time, no total FLOPs, no dedicated compute section. I fetched the full HTML twice with hardware-focused prompts; both runs confirmed absence. So "how much compute in hardware terms" is OWED and cannot be honestly filled.

## 3. Headline results (paper's own numbers, HTML v1)

- Zero-shot power-law scaling L(C) = E + A*C^(-b) held on text (DCLM), CIFAR-10 images (both raw HWC and byte encoding), 16-bit and 8-bit PCM audio, MIDI music (Mutopia), Metamath, DNA, and C/Python code, entirely without gradient steps on any evaluation dataset. Compute exponents b: dclm 0.123, CIFAR-10 HWC 0.066, CIFAR-10 bytes 0.145, PCM-16 0.141, PCM-8 0.260, MIDI 0.249, Metamath 0.129, DNA 0.435, C 0.116, Python 0.113. Authors note these are "broadly similar to exponents from pre-training on the literature, if a bit higher."
- In-context learning: near-100% accuracy on reverse-string, stack, and associative-recall tasks.
- Math structure discovery: Fibonacci/geometric/quadratic/cubic sequences found by round 512 (expected first round >53,000 under uniform prior); arithmetic found at round 0 (expected ~105).
- Pre-pretraining token savings: ESC-50 320M vs 496M tokens, CIFAR-10 421M vs 588M versus random init.
- Authors' own caveats: PCFG baseline beats self-play on text and code; hyperparameter tuning used validation loss averaged over DCLM and DNA (admitted "limited leakage through hyperparameter selection"); universal pretraining "cannot recover contingent information" (world facts still need natural data); results may need "a more expressive programming language" for reusable abstractions.

## 4. Official artifact release (the replication substrate)

- GitHub: the paper's companion repo is live as github.com/nourya-aliz/self_play_pretraining (50 stars, 4 forks, single commit on main). Contents per the repo page: `figures/` (10 figures + 3 table sets, each with the published figure, plotting code, and its data; regenerable with numpy/scipy/matplotlib, no GPU), `scoring/` (code to rebuild benchmark corpora and evaluate the released checkpoints; torch + huggingface_hub), and `REPRODUCING.md`. No training code, no generator weights, and no LICENSE file was visible in the fetched tree.
- HuggingFace: nourya-cohen/solomonoff-paper is live, Apache-2.0, 6 likes, downloads not tracked. Contains learner-only checkpoints for the six-size ladder (byte-level, 256-vocab, Llama-style, 4096 context; weights saved every 256 self-play rounds up to round 8191), plus baselines/uniform-prior, reward-arm ablations (negate, shuffle, signed, last_step, loss_delta at 1M size), and curriculum arms. The model card states generator weights, optimizer states, and training code are excluded.
- URL instability worth knowing: the aujurd22 README cites the authors' repo as github.com/acowsik/self_play_pretraining, and the Maverick-Ansh REPORT.md records that "the authors' companion repo went 404 mid-session" during their work; the live owner today is nourya-aliz. Anyone cloning should follow the nourya-aliz URL.
- Net: the release is evaluation-grade, not training-grade. Independent training replication is possible only by reimplementing the generator and reward from the paper text (which is exactly what the Maverick-Ansh repo did, validating its JVP reward against autograd to 9e-8 relative error).

## 5. Community replication status

Two independent community projects exist, both created within roughly two days of this writing (0-1 stars each, so neither carries community weight yet):

### 5a. Maverick-Ansh/self-play-pretraining-zero-data (from-scratch training reproduction)
- Hardware: 2x Tesla T4 GPUs. Reimplements generator (Brainf*ck + ten macros) and the forward-mode directional-derivative reward from the paper.
- Measurement gate PASSED: on the authors' released 1M checkpoints (round 16383, 3 seeds, context 4096), their model class + bakes reproduce "published per-seed-mean bits/byte to three decimals on all seven corpora". Two hard-won details: DCLM and arithmetic must be baked with the scripts' default sample count 8192 rather than 256 (first pass off by 0.057 and 0.023 bits), and a 1-seed 24-window check was 0.3 bits low on every corpus because seed spread in the authors' 1M models is 0.08-0.5 bits.
- Recovered constants: step budget 2048 per context position; released programs need up to 8,319,126 steps for 4095 bytes; tape 2048 cells (differs from authors only on 0.5% of wrapping hits).
- Found a detector bug relevant to the paper's C5 claim: at 511-byte tapes the paper's trailing window of 2048 lets [5,0,0,...] pass as "geometric, ratio 0", yielding 1,256 junk geometric discoveries in 4,096 uniform programs; also a chance-rate caveat (10M uniform programs contain all five math families, so C5 is an enrichment claim, not an appearance claim).
- Training sweep: running at reduced scale (context 512 vs 4096; 268M tokens vs up to 34.36B; 4 rungs 99k-3.1M params vs 99k-24.4M; 1 seed per rung, 2 at 1M; fixed hypers lr 2e-3, beta_KL 0.02; only the shuffle reward arm; no PCFG baseline, tuning, pre-pretraining, or epiplexity analysis). REPORT.md sections 4 (Results) and 5 (Verdicts) were literally "(filled in ... when the sweep completes)" at time of reading: the paper's scaling claims are NOT yet independently confirmed or refuted by this repo.

### 5b. aujurd22/selfplay-paper-analysis (inference-only verification + probes)
- Hardware: a single RTX 4070 SUPER (12 GB) runs everything; the 27-checkpoint sweep takes about a minute since it is inference-only.
- Verified: recomputed bits-per-byte matches the published CSVs "to ~0.05 (500k model, same checkpoint, K=1)"; random-byte sanity stays ~8.0 bpb across arms ("no fake compression anywhere").
- Probes beyond the paper: AP-tape arithmetic loss drops ~8 to <0.5 bpb within the first ~500-1000 rounds (early internalization); ICL emergence ordering "24M r2048 < 6M r3072 < 3M marginal" with 100k/500k never emerging and 3M seed-dependent, implying the paper's effective emergence threshold is 6M, a nuance the paper does not report; ICL shows transient collapses (0.95 to 0.23 to 0.93) and one 6M seed hitting 1.00 at r6144 then decaying to 0.50 by r16383; loss ordering across corpora matches zlib compressibility at Spearman 1.00 (though absolute loss is worse than zlib); a near-pure arithmetic head exists (ablation costs AP +3.9 bpb while everything else stays at or under 1.2), plus ~10 AP-specific MLP neurons causing 3x AP degradation with text unchanged.
- No training is reproduced here; it validates the released artifacts, not the training loop.

### Replication bottom line
The evaluation pipeline is independently reproduced (two groups, matching published numbers at their stated tolerance). The training dynamics and scaling claims are not yet independently confirmed or refuted; one from-scratch training replication is in flight at ~1/128th of the token budget, verdict pending. No official training code exists to check against.

## 6. Community discussion and coverage

- Hacker News: one story, id 49848120, "Self-Play Pretraining with Zero Data", 4 points, 0 comments, submitted 2026-09-25 by E-Reverance, linking the arXiv page. Verified via hn.algolia.com API search (4 matches total; the other 3 are unrelated older comments) and the item page itself.
- alphaXiv: trending rank #2 at time of check, 2,103 views, 106 saves, but zero user comments (only an AI-generated overview). Also promoted by the @askalphaxiv X account (status 2103778101033590958).
- Stanford AI Lab promo post: "Can an LM, starting from random init (!!), learn to generate all of its pretraining data?" (surfaced in web search; ai.stanford.edu).
- slowfast.ai essay "Gardeners of Intelligence" cites it with the 24 Sep 2026 date and the random-initialization framing.
- Chinese-language coverage: the "AI可可AI生活" podcast (Apple Podcasts) covers it as its lead [AI] paper with the TAU+Stanford affiliation note; a Tencent News (腾讯新闻) explainer "从零数据自博弈" exists; X thread by @jimmy_longbow_ quotes the abstract; a xixidu Facebook roundup and Telegram channel @j_links carry links.
- Aggregators: listed in the awesome-daily-AI-arxiv GitHub repo. The HuggingFace papers page (huggingface.co/papers/2609.30063) returned HTTP 404 when fetched: no HF papers entry.
- Reddit and LessWrong: I ran targeted searches and found no dedicated threads on either. Absence in my searches is not proof of absence, but as of this ask the visible discussion mass is: aggregator listings, promo posts, and the two replication repos, with essentially zero substantive public debate thread yet (paper is 4 days old).
- The paper's name-check of Solomonoff induction is the hook most coverage leads with; the reproduction community has already nicknamed the artifact line "solomonoff-paper" (the HF repo name).

## 7. Assessment

Solid, unusually well-artifacted proof-of-concept: learner checkpoints + scoring code + figure data released on day one made same-week independent verification possible, and two small teams did verify the published numbers at inference. The two soft spots, both flagged in-paper and sharpened by the community: (1) the C5 math-discovery result needs enrichment-vs-chance framing and a stricter detector window, (2) ICL emergence has a seed-dependent 3M threshold and oscillates after emergence, neither nuance in the paper. The load-bearing question the paper itself names is whether the <25M-parameter scaling exponents survive at real scale; with training code unreleased and the one public training replication at 268M tokens versus the paper's 34.36B, that question is open on all sides. Hardware compute is undisclosed, so nothing external can audit the energy/cost side of the 34.36B-token budget.

## Sources (all fetched this session)

- https://arxiv.org/abs/2609.30063 (abstract, authors, v1 date, equal-contribution note)
- https://arxiv.org/html/2609.30063v1 (budgets, exponents, ICL, limitations; two hardware-focused fetches)
- https://hn.algolia.com/api/v1/search?query=Self-Play%20Pretraining%20Zero%20Data and https://news.ycombinator.com/item?id=49848120
- https://github.com/Maverick-Ansh/self-play-pretraining-zero-data and its REPORT.md
- https://github.com/aujurd22/selfplay-paper-analysis and its README (raw)
- https://github.com/nourya-aliz/self_play_pretraining (authors' release; acowsik URL cited in aujurd README, 404 recorded in Maverick REPORT.md)
- https://huggingface.co/nourya-cohen/solomonoff-paper and https://huggingface.co/api/models?search=self-play%20pretraining (empty result, hence no other model hosting found)
- https://www.alphaxiv.org/abs/2609.30063
- https://huggingface.co/papers/2609.30063 (HTTP 404)
- Web searches: arXiv id query; Reddit/Solomonoff query (surfaced Stanford AI Lab post, slowfast.ai essay, alphaXiv promo, awesome-daily-AI-arxiv); first query surfaced the Chinese podcast, Tencent News, X thread, Telegram
