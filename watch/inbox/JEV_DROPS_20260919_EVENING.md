# JEV DROPS — 2026-09-19 evening wave (15 operator links, tri-state)

Fetched via vxtwitter (fxtwitter 404'd on all IDs). One link carried no Jev
content and is filed as off-topic, not forced. This card is the research
receipt behind SALON2_BRIEF_20260919.md sections 2 and 5.

## The load-bearing three

1. **Bespoke Nimble — the open Jev exists** (NFT_Chen, QRT Hugo Duprez).
   Open data + open recipe + open weights. Qwen3.5-9B LoRA, NOT distilled
   from Jev (Jev only scored it). Contrastive curation: negatives made by
   flipping ONE key fact (implicit calibration). Fully synthetic data, 10
   categories, train/eval split. No RL yet. Parallel constrained decoding:
   no long generation, reads candidate token probabilities directly.
   Self-eval: Qwen 66 -> Nimble 90 -> Jev 93 (same 10 categories). ~100ms
   on H100, runs on a MacBook. Caveat tweeted by the author: no unified
   benchmark, may drop outside the 10 domains. UNVERIFIED from our seat
   (tweet + repo pointers only; weights not pulled). Salon verdict:
   sovereignty front-runner, gated on OUR weekly >=0.880 meter, never
   oracle-scored.
2. **The drone split** (MKhordoo x2, QRT CompleteSkeptic origin). Green =
   the S1 oracle's own confidence; purple = "I'm not sure, ask the big
   model." 99 percent self-steered, escalation only on uncertainty, ~300ms
   decisions, deliberate slowdown in dense fields. That is the tier ladder
   with a confidence trigger, demonstrated. Vendor-adjacent demo: SUPPORTED
   as architecture claim, UNVERIFIED as numbers.
3. **Runtime level generation** (Hugo Duprez via the Nimble QRT). Parkour
   terrain chosen by the oracle while the player runs: platform type,
   width, gap, height in one request, ~320ms, under $0.003. "Code governs
   legality, the model governs the next cut." Pre-baked content yields to
   runtime decisions bound to player state. Maps directly onto RUINS GO
   rooms and maze_arena. UNVERIFIED, architecturally load-bearing.

## The rest, tri-state

- TheBalkanHacker: Jev as anti-pattern linter for LLM codegen — AST rules
  get gamed (Goodhart named), judgment tier does not. SUPPORTED as the
  abide pattern for code; fleet application: lint our own codegen for
  AI-tells (em-dashes, not-X-but-Y) — already demonstrated in tonight's
  wave.
- simplifyinAI: "split intelligence from execution"; 3 typed outputs; build
  now, swap the oracle later without rebuilding the agent graph. SUPPORTED
  (it is our adapter pattern, restated).
- michael_chomsky: "the great jevification" + QRT: classifier.dev "now
  outperforms Jev and is free." UNVERIFIED, unprobed beyond the claim.
- hityyhz: keystroke oracle launcher, ~100ms intent reads, full confidence
  per keystroke. UNVERIFIED demo; maps to FIND/FILE/LOAD surfaces.
- _chenglou: Google TabFM, zero-shot foundation model for tabular data,
  "intelligence in spreadsheet" — the credited ancestor of column-typed
  reads. POINTER (research owed, not adopted).
- shannholmberg / DataChaz / sarvagya_kul / tarasshyn: the demo wave
  (second brain, 10-step roadmap article [login-walled, UNVERIFIED], job
  matching 400 companies $0.0005, session mining 3M events $2.17 with
  "213 draft PRs" — DISPUTED framing: Jev cannot write PRs; the pipeline
  around it wrote them).
- urchadeDS + JoshKuechly + Layton_Gott: the specialist counterattack.
  GLiNER2 open over a year, tuneable in under an hour, local, 8.8x faster;
  CUA-S1-FORMS claimed 706K params / 99.7 vs hosted 83.6. PROBE RESULT:
  trycua/cua README + releases show driver nightlies only; model NOT found
  (GitHub repo search total_count 0). CUA-S1 stays UNPROVEN until weights
  exist. GLiNER repos exist (HTTP 200 fastino-ai/GLiNER2, urchade/GLiNER).
- nzevh_: laptop build, day 117, wires. NO Jev content. Off-topic, filed
  honestly.

## Probes run this session

- api.typesafe.ai/v1/systemone: ALIVE. GET 405; POST without key returns
  authentication_error. Live front door, key-gated. Fleet holds no typesafe
  key; operator states Hermes has it (HERMES_API_KEY_1/2 present in .env).
- Endpoint SSRF posture for the adapter: same rules as mag/verb.py
  (https-only, host allowlist, resolved-IP boundary check).
