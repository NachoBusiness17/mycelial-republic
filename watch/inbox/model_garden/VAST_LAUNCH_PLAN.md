# VAST LAUNCH PLAN - salons on a rented vast.ai GPU (LANE VAST-1, LAUNCH PREP)

Staged 2026-10-01/02 by lane VAST-1. Status: PREPARED, NOT EXECUTED. Nothing in this
file rents, creates, or pays anything. The operator's GO is one action (section 6).
No account was created, no payment entered, no secret value read or printed during
preparation. Web claims carry links; estate claims carry repo-relative receipts.

Prior art this plan stands on (all byte-backed in-repo):
- mag/vast_launcher.py (serve_plan, _load_vast_key, credit; laws: destroy-after, .env-less box)
- state/vast/ (the whole 2026-08-27..09-05 campaign: launch_vast.py, experiment.py,
  box_contract.sh v2.2/3, blade_buyer, governor, spend_ledger.jsonl, TESTING_BOX_PLAN.md,
  EXPERIMENT_CONCURRENT_20260905.md)
- scripts/vast_paces.py (model ladder + concurrency ladder, receipts to state/vast/)
- scripts/garden_battery_local.py + GRID_local-20261001-a.json (local-endpoint battery,
  fence NOT weakened, lane-local script pattern)
- memory/plans/mate_moe_v0/EXPERIMENT.md, memory/rib/RIB_GPU_LADDER_20261001.md,
  tools/pain_replication/runner.py (the three GPU-relevant instruments)

## 0. THE NO-SACRED-COWS RACTOR (read this before the plan)

Operator order folded in: "check vast ai for best practices and pricing around what we
want lets ractor it out no sacred cows." Steelmanning the KILL:

- The API lanes already win on price. The estate's own honest frame, written 09-05
  before any of today's enthusiasm: "$0 API lanes win raw price forever - the vast leg
  is NOT cheaper tokens." A 24GB box at $0.18/hr on-demand is $4.32/day; the 09-30
  day synthesis shows 9-family grids + swarms + salons landing for under $3 total.
  Renting a GPU to serve salon families COSTS MORE PER DAY than the API bill it
  would replace.
- The GPU ladder rib's workload gate (RIB_GPU_LADDER_20261001.md gate 5) says the GPU
  only pays when there is real FP8/MoE QPS demand or the mating-to-MoE door is BUILT.
  The door is not built: MATE_MOE_v0's CPU falsifier (memory/plans/mate_moe_v0/
  EXPERIMENT.md) is STAGED, NOT RUN, $0, one sitting, operator-GO pending. Buying GPU
  hours before the falsifier answers is paying for a door that may be dead on arrival.
- The Qwen3-8B replication is ALSO staged-and-gated (zero model cells run), and its
  frozen amendment pins CPU fp32 with quantization forbidden (tools/pain_replication/
  runner.py). It does not want a GPU; it wants a free 38GB RAM window on the estate box.
- The overmind brain costs cents per loop-hour against a $1 hard cap
  (tools/overmind_loop.py caps; glm-5.3-flash pricing in tools/model_garden.py PRICING).

Per-workload verdicts (the honest ladder):

| Workload | Verdict | Why |
|---|---|---|
| Salon/swarm serving, 2-4 small families | NEEDS-RENT-NOW as a TRIAL only | operator-ordered experiment; buys width-without-ratelimits + private weights, NOT cheaper tokens; 10h trial is $1.00-3.40 |
| MATE_MOE_v0 2B/E=4 rerun | WAIT-ON-FALSIFIER | CPU 0.5B leg is $0 and unrun; even the 2B/E=4 Q4_K_M rerun is ~3GB and fits the estate 6GB card; only a 3B-scale fp32 eval (~40GB weights) truly needs rent |
| Qwen3-8B replication | WAIT-ON-FALSIFIER | frozen spec = CPU fp32, quant forbidden; free path is a 38GB local RAM window; rent only a RAM-rich box if windows never open (GPU bf16 would need a prereg amendment) |
| Overmind brain local (glm-flash-class) | API-CHEAP-ALREADY | cents per loop-hour under a $1 cap; box_contract.sh v2.2/3 bring-up exists as a passenger if a box is up anyway |
| code_swarm / garden batteries | API-CHEAP-ALREADY | free-tier + cheap keys cover them; local grid already runs $0 on ollama (GRID_local-20261001-a.json) |
| Saelis-31B live hosting | NEEDS-RENT (dormant) | cannot run locally at all; 48GB Q8 or 24GB Q4 quality drop; only when the operator wants her live (~$0.55 per 4h blade, TESTING_BOX_PLAN.md item 5) |
| Ghost QLoRA fine-tune | NEEDS-RENT when a batch exists | package built 2026-08-09 (memory/working.md), ~$0.12/run on a 4090; blocked on CLI install, not on plan |
| DeepGEMM/FP8 software-gate dogfood | WAIT | workload gate not fired; if it fires, an H100 rent satisfies the gate test for ~$13/10h instead of a $4000 buy |

The honest one-line recommendation: RUN THE FREE FALSIFIER FIRST (MATE_MOE_v0 CPU leg,
one sitting, $0), and let the operator's salon trial ride a single cheap interruptible
box for 10 hours ($1-3.40) because he ordered the experiment, not because it saves
money; rent nothing bigger until the falsifier feeds or Saelis/training demand fires.
The plan lands either way; the GO stays his.

## 1. WORKLOAD CENSUS (from the estate's own receipts)

1. MATE_MOE_v0 (memory/plans/mate_moe_v0/EXPERIMENT.md). Leg 1: 0.5B parents, fp32,
   CPU, context 512, one sitting, ~$0 - the falsifier that decides the mating-to-MoE
   door. Leg 2 (only if it feeds): 2B-class, E=4, Q4_K_M in llama.cpp, log tok/s.
   VRAM math (weights): MoE params ~= non-MLP + E x MLP. Qwen2.5-1.5B parents
   (MLP ~75% of 1.54B): E=4 gives ~5.0B params -> fp32 ~20GB, bf16 ~10GB,
   Q4_K_M ~3GB. At 3B parents: ~10B params -> fp32 ~40GB, bf16 ~20GB, Q4 ~5.8GB.
   So the rerun leg fits a 24GB card in bf16 or even the estate 6GB card at Q4;
   only 3B-scale fp32 wants an A100-40+.
2. Qwen3-8B interference replication (tools/pain_replication/runner.py +
   INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md). CPU-only fp32, quantization
   forbidden (AI5 spec law), ~33GB weights, hard gate free RAM >= 38GB, 26s per
   ~116-token forward on the estate Zen2, cell-level resume, zero cells run.
   STAGED-AND-GATED per DAY_SYNTHESIS_20260930.md.
3. Overmind theory (tools/overmind_loop.py, overmind_brain.py, box_contract.sh).
   Brain = glm-5.3-flash API ask per tick, $1 hard cap per loop-hour. The local
   variant already has a full vast bring-up: box_contract.sh v2.1/2.2/3 pulls
   GLM-5.3-Flash UD-Q4_K_XL, prebuilt llama.cpp CUDA binaries (no toolchain needed
   on the ollama image), aria2 stall-proof downloads, phase status server on :8001.
4. Salon/swarm shapes (mag/frontier_salon.py, salon_50.py, scale_salon.py,
   tools/code_swarm.py). API-shaped: code_swarm FAMILIES rows carry
   model/base_env/base_url and fire through the gated model_garden rail; frontier
   salons ride seat_steer/party_subchain. All can point at any OpenAI-compatible
   endpoint, including a local vLLM (section 4).
5. GPU ladder BUY gates (memory/rib/RIB_GPU_LADDER_20261001.md): ARCH SM90/SM100,
   VRAM 24GB min, PRICE capex triggers, SOFTWARE CUDA 12.8+/NVRTC/vLLM-FP8 dogfood,
   WORKLOAD demand-side. How RENT differs per gate:
   - ARCH: buy restricts to SM90/SM100 (SM120 verify-first, never Ada for this).
     Rent INVERTS it: pay hours to TEST an arch claim (H100 for DeepGEMM FP8,
     5090 for SM120 FP4 variance) with zero capex; renting Ada/3090 for plain
     serving is fine even though it is never-to-buy.
   - VRAM: buy demands 24GB min/32 preferred on the desk; rent buys VRAM by the
     hour, 48-80GB for exactly the hours that need it.
   - PRICE: buy triggers are capex thresholds; rent has no capex, the trigger is
     dph-vs-value plus the covenant floor (state/vast/covenant.json).
   - SOFTWARE: buy requires the stack dogfoodable; rent is the CHEAPEST way to
     satisfy dogfood (templates now, hours not months).
   - WORKLOAD: unchanged by renting. The gate is demand-side; a rental does not
     fire it. This is the rib's real message and the ractor's spine.

GPU-value ranking: (1) salon trial on operator order (cheap, 24GB enough),
(2) Saelis-31B live (48GB when wanted), (3) ghost QLoRA (any 16-24GB, per batch),
(4) MATE_MOE 2B/E=4 bf16 or Q4 legs (24GB plenty), (5) H100 FP8 dogfood only if the
workload gate ever fires, (6) 8B replication: RAM-rich CPU box, GPU not required.

## 2. INSTANCE SPEC (current market, 2026-10)

Prices are marketplace-live and move hourly; treat as planning bands. Sources:
vast.ai pricing pages and third-party trackers
([vast.ai/pricing](https://vast.ai/pricing),
[Spheron 2026 breakdown](https://www.spheron.network/blog/vastai-pricing-2026),
[ComputePrices A5000](https://computeprices.com/providers/vast/gpus/rtxa5000),
[Thundercompute](https://www.thundercompute.com/blog/vast-ai-vs-thunder-compute)),
plus the estate's own measured rents: 3090 $0.069/hr Argentina rel 0.993 (09-05),
3090 $0.113-0.148 (08-28 shopping), 4090 watch-best $0.121, 5090 $0.353/hr Nevada
rel 0.996 (state/vast/experiment_receipts.jsonl, TESTING_BOX_PLAN.md).

| Tier | Card | VRAM | Interruptible | On-demand median | 10h trial | 100h month |
|---|---|---|---|---|---|---|
| SCOUT (recommended first) | RTX 3090 | 24GB | $0.09-0.12 | $0.18 | $0.90-1.80 | $9-18 |
| SALON comfort | RTX 5090 | 32GB | $0.34 | $0.60 | $3.40-6.00 | $34-60 |
| (alternative) | RTX 4090 / A5000 | 24GB | $0.29-0.35 / $0.19-0.20 | $0.45 / $0.232 | $2.00-4.50 | $20-45 |
| JUDGMENT | A100 40GB | 40GB | $1.00-1.50 | ~$1.60 | $10-16 | $100-160 |
| ARCH TEST | H100 80GB | 80GB | $0.90-1.73 | $2.27-2.80 | $9-28 | $90-280 |

What each tier fits (weights math from section 1):
- 24GB (3090/4090/A5000): 3 vLLM families concurrently (2 x 7B/8B AWQ ~6GB each
  + 1 x 2-3B ~2-5GB + KV + ~1GB CUDA context per process -> 18-21GB);
  MATE_MOE 1.5B/E=4 fp32 (20GB) or 3B/E=4 bf16 (20GB); 8B bf16 eval (16GB);
  Saelis-31B Q4 (18.7GB, quality drop); ghost QLoRA on 1.5-7B.
- 32GB (5090): the above plus a 4th family with real KV headroom; SM120
  verify-first arch (the ladder's own test case).
- 40GB+ (A100/H100): 8B fp32 in VRAM (33GB), MATE_MOE 3B/E=4 fp32 (40GB),
  Saelis-31B Q8_0 (32.6GB), DeepGEMM FP8 dogfood (SM90 pays full).
Selection filters (estate-proven, state/vast launch rails): reliability >= 0.98
(estate range 0.97-0.996), verified host, rentable, disk >= 40GB (150GB if pulling
32B weights), cpu_ram >= 48GB nice-to-have, inet_down >= 500Mb/s, two launch
failures = stop (the 09-05 400 invalid_args abort rule).

## 3. THE PROVISION PLAN (skeleton: scripts/vast_provision.ps1, guarded, not run)

Written as a plan document + a guarded PowerShell skeleton. Default invocation
prints the plan and exits; only `-Go` can spend, and only the operator runs that
(see section 6). Phase shape (all commands operator-paste-ready, none executed here):

- Phase 0 CREDIT (no spend): `.\.venv\Scripts\python.exe -m mag.vast_launcher credit`
  reads GET /users/current only (buyer stood down). Gate: credit >= $10.
- Phase 1 SEARCH: vast CLI `vast search offers 'gpu_ram>=24 rentable=true
  verified=true reliability>0.98 inet_down>=500 disk_space>=40' --order dph` or the
  API equivalent GET /api/v0/bundles (state/vast/launch_vast.py pattern). Pick the
  tier row from section 2.
- Phase 2 CREATE (interruptible for the trial): image choice per lane:
  - serve lane: `vllm/vllm-openai:latest` (OpenAI-compatible server, port 8000,
    --api-key auth) or `ollama/ollama:latest` for GGUF/MoE legs (the estate's
    verified boot image; box_contract.sh v3 lesson: prebuilt llama.cpp CUDA
    binaries because the ollama image ships no toolchain).
  - train lane: `pytorch/pytorch:2.x-cuda12.x-runtime` + pip install peft trl
    bitsandbytes (memory/training/vast_package requirements).
  - arch-test lane: CUDA 12.8+ devel image per the ladder SOFTWARE gate.
  Docker options: `-p 8000:8000 -p 11434:11434`; disk 40-60GB; onstart script
  generates the service bearer key ON THE BOX (openssl rand -hex 24), writes it to
  /root/brain/status.json channel, never into the image or repo.
- Phase 3 VERIFY: poll the box's mapped port until first 200 with the bearer key;
  nvidia-smi identity into the receipt (estate law); `python scripts/vast_paces.py
  --endpoint http://127.0.0.1:8000` through the tunnel for the model + concurrency
  ladders; boot-to-work tax measured (09-05 gate: < 30 min).
- Phase 4 SALONS: point the swarm/salon surface at the endpoint (section 4).
- Phase 5 TEARDOWN (the standing LAW): pull results to watch/inbox/model_garden/
  and memory/runs/..., then `vast destroy instance <ID>`. Destroy, not stop:
  stopped instances still bill storage at $0.10/GB/month (state/vast/launch_vast.py
  STORAGE_USD_GB_MO; vast pricing docs). No persistent state on rent: anything not
  pulled before destroy is gone. Kill-word anytime (state/vast/experiment.py
  teardown pattern) with hard ceilings: trial <= $5, month <= $50.

Key posture (estate laws, all inherited):
- VASTAI_API_KEY stays in .env on the estate box (name verified present 2026-10-01;
  value never read or printed). It is NEVER uploaded to a rented box; rented boxes
  are .env-less by design (09-05 inherited law: zero fleet secrets travel; public
  weights only).
- SSH: generate the keypair locally (ssh-keygen per vast docs), paste the PUBLIC
  key into Account -> Keys (or `vastai create ssh-key`); keys attach at container
  creation ([SSH guide](https://docs.vast.ai/guides/instances/connect/ssh),
  [keys reference](https://docs.vast.ai/guides/reference/keys)). Private key never
  leaves the estate box.
- Service bearer key: generated on the box at boot, surfaced via SSH channel only.

## 4. SALON-ON-GPU ARCHITECTURE (wiring the estate to the endpoint)

Two honest paths; the fence decision is the crux.

Path A (RECOMMENDED, zero fence edits): SSH tunnel + lane-local script.
`ssh -N -L 8000:localhost:8000 root@<ip> -p <port>` then the endpoint is
http://127.0.0.1:8000/v1 locally. The canonical tools/model_garden.py runner
REFUSES this endpoint by design (bare-https + allowlisted-host + public-host fence,
lines 98-129; GRID_local-20261001-a.json deviation note: "fence NOT weakened").
So local-served families fire through a lane-local script in the
scripts/garden_battery_local.py pattern (plain HTTP client to the loopback
endpoint, identical ask bytes, same grader), which the 2026-10-01 local grid
already proved end to end. code_swarm gets its local family by staging ask.json
rows with the local base_url for the lane-local runner, not the canonical one.

Path B (the one-line fence change, named with its risk): in tools/model_garden.py
FAMILY_TABLE (lines 65-74), add exactly one row after `"api.z.ai": "zai",`:
`"<proxy-host>": "vastlocal",`. Risks, stated plainly:
1. The vast port proxy is plain TCP on a raw shared IP (docs: mappings like
   65.130.162.74:33526 -> 8081; no TLS termination,
   [networking guide](https://docs.vast.ai/guides/instances/connect/networking)).
   A https base_url to that host fails cert verification unless you add on-box TLS
   (Caddy self-signed), and the temptation then is to disable verification, which
   mutes the whole SSRF fence. The fence also requires the entry to be the literal
   proxy host, which is an ephemeral rented IP: the "one place to extend" invariant
   rots into per-rent churn.
2. Any proxy-exposed port is publicly reachable (shared IP, internet-scannable);
   the docs' own guidance is token-auth or tunnel. vLLM must run with --api-key
   regardless of path.
Verdict: keep the canonical runner pure; Path A is the estate-law answer. If a
named TLS-terminated proxy surface is ever used, Path B becomes a domain row
(`"vast.ai": "vastlocal"`) and is a fence-owner decision, not a lane edit.

inference_budget recipes for local-served families (mag/inference_budget.py):
- No animal match -> DEFAULT recipe governs (floors: small 8000-12000, review
  24000). Local constraint is ctx: battery-measured runtime ctx 8192 on the
  gemma lanes, so cap max_tokens 2048 for small asks (GRID_local used 2048) and
  do not send review-shape (18KB+ body) asks to sub-16k-ctx locals.
- gemma local (gemma:2b, gemma4, gemma2:2b q5): plain {"max_tokens": N} only.
- Qwen local (Qwen2.5 AWQ on vLLM): strip reasoning/thinking params entirely
  (qwen-flash recipe analog; unknown body params are not free).
- glm local (UD-Q4 via llama-server): no thinking control; box_contract v2.1
  serve shape.
- Cost accounting: local families are not token-priced; record cost as
  dph / 3600 x latency (the vast_paces $/Mtok formula) in the lane receipt;
  tools/model_garden.py PRICING stays untouched (GRID_local banked cost_usd 0.0
  for the ollama lane; a rented box replaces 0.0 with the dph-derived figure).

## 5. BEST-PRACTICES SWEEP (vast.ai operational gotchas, sourced)

- Interruptible vs on-demand: on-demand and reserved always take precedence;
  interruptible instances pause when outbid and resume when priority returns;
  data is preserved while paused but the instance is non-functional; official
  guidance = checkpoint often, back up outputs, use interruptible only for
  fault-tolerant work
  ([rental types](https://vast.ai/article/Rental-Types),
  [instance types](https://docs.vast.ai/guides/instances/choosing/instance-types),
  [FAQ](https://docs.vast.ai/guides/reference/faq/rental-types)).
  Trial posture: interruptible for the 10h salon trial (eviction costs a rerun,
  not data, because results stream back per-ask); on-demand the day Saelis or a
  training run goes live. Reserved (up to 50% off, 1/3/6-month) is wrong for
  trial-scale; reconsider only if a 100h/month salon becomes standing.
- Reliability: scores start low on new machines and grow with uptime (90%+ within
  days of stability); a drop alone does not de-verify a host, an active error
  does. Filter reliability >= 0.98, prefer machines with long track records and
  datacenter hosts over hobbyists
  ([verification stages](https://docs.vast.ai/host/verification-stages),
  [understanding verification](https://docs.vast.ai/host/understanding-verification)).
- Scams/bad hosts: the platform is legitimate (Trustpilot ~4.4/5 across ~200-250
  reviews); complaints cluster on individual flaky hosts, not the marketplace.
  Estate mitigations that remain law: nvidia-smi identity into the receipt,
  probe-first, two-launch-failures-stop, destroy-after-use.
- SSH keys: keypair generated locally, PUBLIC key added under Account -> Keys (or
  `vastai create ssh-key`), attaches at container creation; instance SSH rides
  the proxied root@ip -p port form
  ([SSH](https://docs.vast.ai/guides/instances/connect/ssh),
  [CLI hello world](https://docs.vast.ai/cli/hello-world),
  [Windows guide](https://docs.vast.ai/guides/instances/connect/windows-guide)).
- Images: prefer stock registry images over custom builds for bring-up speed
  (estate-verified: ollama/ollama boots clean; vllm/vllm-openai for serving;
  pytorch cuda runtime for training). Custom Dockerfiles only when the arch test
  needs CUDA 12.8+ devel + NVRTC (ladder SOFTWARE gate).
- Ports/exposure: docker -p opens internal ports mapped to RANDOM external ports
  on a SHARED public IP; 64-port limit per instance; env vars VAST_TCP_PORT_<x>
  carry the mappings into scripts; exposed services are public, so auth or tunnel
  ([networking](https://docs.vast.ai/guides/instances/connect/networking),
  [Jupyter TLS example](https://docs.vast.ai/guides/instances/connect/jupyter)).
  Estate law stands: bearer key at the server, SSH tunnel for the estate, never a
  raw unauthenticated 0.0.0.0 service as the only layer.
- Persistence/teardown: destroy = data gone; stop = data kept but storage billed
  ($0.10/GB/month; state/vast/launch_vast.py constant + pricing docs); the
  destroy-after-use law exists because idle boxes and stopped-storage are the
  quiet drains (the 08-28 governor STAND_DOWN receipts show the covenant policing
  exactly this).
- Egress: no per-GB egress line-item appears in vast's pricing model (dph +
  storage); network quality varies per host, so filter inet_down/inet_up on the
  offer row before renting (estate 08-28 shopping notes; vast search offers
  fields). Verify on the box at boot with a speed probe before pulling 30GB of
  weights through a thin pipe.

## 6. THE GATE (operator-only) + THE ONE-ACTION GO

Operator-only, never lane-executable:
1. Account + credit: top up and confirm credit >= $10 (console or
   `python -m mag.vast_launcher credit`). Lane reads balance, never moves it.
2. The rent itself: running `scripts/vast_provision.ps1 -Go` (or pasting the
   Phase 1-2 commands by hand). No lane, agent, or scheduler may pass -Go.
3. SSH public-key paste into Account -> Keys.
4. Any FAMILY_TABLE fence edit (Path B) if ever chosen.
5. Spend above the trial ceiling ($5) or any tier above SCOUT.

THE GO SEQUENCE (one action, after credit check):
  powershell -ExecutionPolicy Bypass -File scripts\vast_provision.ps1 -Go -Tier scout
That single command: searches with the estate filters, creates ONE interruptible
24GB instance with the serve image + onstart bearer-key bring-up, prints the SSH
tunnel line + kill-word + live ceiling. Everything after (verify, salons, teardown)
is lane work under the ceilings; teardown is automatic at the trial hour cap and
manual via the kill-word at any moment.

Receipt law: the run lands results + spend in watch/inbox/model_garden/
(VAST_SALON_TRIAL receipt) and memory/runs/model_garden/usage.jsonl; the census
carrier in AGENTS.md is untouched by this plan.
