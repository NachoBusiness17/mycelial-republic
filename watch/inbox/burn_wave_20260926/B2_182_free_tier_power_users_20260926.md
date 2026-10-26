# B2-182 free-tier power users dig (2026-09-26)

## Verdict

LANDED, bounded by a rate-limited search lane. Two primary sources fetched
and verified today (TPU Research Cloud program page; Thunder Compute's
14-program GPU-credits roundup, already a LINKS canonical), one secondary
level corroborated by search results (GitHub Student Developer Pack /
Copilot Student plan), the community tracker layer already on file in this
repo's own LINKS.jsonl (awesome-freellm-apis 486+ APIs / 31 providers,
awesome-free-models, awesome-free-llm-apis). Patterns distilled below; no
ToS-violating practice is recorded; the "what do they know that we do not"
answer is a three-layer ladder plus a portability discipline the estate
partially runs already.

## Evidence file:line quotes

- https://sites.research.google/trc/about/ (fetched 2026-09-26): free access
  "to a cluster of over 1,000 Cloud TPU devices", for "machine learning
  researchers" worldwide via an interest form; acceptance terms: share
  results publicly (peer-reviewed papers, open source, blog posts), give
  detailed feedback on the program, accept Google T&C and AI principles.
  Frameworks: TensorFlow, PyTorch, Julia, JAX, plus a Colab path.
- https://www.thundercompute.com/blog/free-cloud-gpu-credits (fetched
  2026-09-26): student/anyone tier table (Thunder $20 student credit + 3%
  referral; Colab free limited T4 ~12h sessions; Kaggle T4/P100 with strict
  caps; Paperspace free Gradient, card required, public notebooks; Modal
  $30/month free serverless credit; Azure new-account $200/30 days, GPU
  quota separate) and startup tier (GCP up to $350K VC-backed to Series A;
  AWS Activate up to $200K; MS Founders Hub $1K start up to $150K, top
  tiers need VC/accelerator referral; DigitalOcean Hatch up to $100K;
  Alibaba $120K; OVH EUR 100K; Scaleway EUR 36K). Its own stacking claims:
  "Sequence by stage", "Stay portable: containers + S3-compatible storage",
  "Match workload to tier", and a 5-person team running continuous
  A100/H100 for 9-12 months on under 5% out-of-pocket.
- Search-results level (not fetched): GitHub Student Developer Pack carries
  premium Copilot/AI request allowances and a dedicated Copilot Student plan
  (github.blog changelog Mar 2026, devactivity.com Feb 2026 quota writeup).
- Already on file in watch/inbox/LINKS.jsonl (this repo's own scout rows):
  "486+ FREE LLM APIs from 31 providers (updated Sep 16 2026)" (github.com/
  open-free-llm-api/awesome-freellm-apis), 12britz/awesome-free-models,
  mnfst/awesome-free-llm-apis; plus live free-lane churn rows (Cerebras
  card-gating, Google AI Studio ending reports, OpenRouter roster rotation).

## Verdicts (the patterns)

1. Identity-gated compute beats raw free tiers (VERDICT: real, largest
   single lever). Student status unlocks GitHub pack + Copilot Student;
   researcher status unlocks TRC's 1,000+ TPU pool. The gate is an email
   domain or an application form, not money.
2. The credit ladder is sequenced by stage (VERDICT: real, from the
   Thunder roundup): free tiers for prototyping, student credits, startup
   programs (Founders Hub tier 1 needs no VC referral), hyperscaler credits
   last.
3. Portability is the enabler (VERDICT: real): containers + S3-compatible
   storage make credits fungible; without it you are locked to one donor.
4. Multi-provider juggling is normalized (VERDICT: real): key rotation
   chains per lane, roster trackers updated weekly by community lists, and
   the estate already runs exactly this shape (providers.yaml api_key_envs
   chains, the free-resource scout, endpoint-news passes). Their extra:
   referral loops (Thunder 3% credit/payout) as a slow credits tap.
5. What they know that we do not: (a) hackathon and startup-credit doors
   are open to small teams without funding (Founders Hub, Hatch) and the
   estate has filed zero rows against them; (b) obligation-matched compute
   (TRC) trades public artifacts for TPU-hours, which fits this estate's
   receipt-first culture better than any anonymous free tier; (c) free-tier
   churn is weekly and community trackers are the meta-source, which the
   scout already reads but the rotation policy does not yet cite.

## Work done

1. Fetched TRC about page; fetched the Thunder credits roundup (canonical
   already registered; refreshed specifics read).
2. Corroborated the GitHub Student Pack layer via search results (search
   lane otherwise 429-stormed; weak-signal claims marked as such).
3. Cross-read this repo's own LINKS.jsonl free-tier intel (10+ rows) so the
   dig names the delta rather than re-filing known lists.
4. Appended 1 LINKS.jsonl row (TRC, writer zcode-sw-11-b2-182).
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This dig is inverted if any of the following holds: (a) the TRC fetched page
does not state the 1,000+ TPU pool or the public-results obligation on a
refetch (misread); (b) a named program's terms are found to bar solo
operators or require institutional affiliation the receipt implies away;
(c) the stacking claim (9-12 months A100/H100 under 5% out-of-pocket) is
shown to require ToS-violating multi-accounting rather than sequenced
programs (then pattern 2/3 need an ethics caveat or removal); (d) a fresh
pass finds the GitHub Student Pack AI quotas materially different from the
corroborated summaries.

## Bibliography closed

sites.research.google/trc/about/ (fetched in full); thundercompute.com/blog/
free-cloud-gpu-credits (fetched in full; canonical pre-existing in LINKS);
github.blog + devactivity.com Copilot-student rows (search-result level,
not fetched); watch/inbox/LINKS.jsonl free-tier rows (canonicals listed
above, read from local bytes). Web fetches: 2; searches: several, mostly 429.
