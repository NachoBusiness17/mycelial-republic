# RECEIPT — K13: Kubernetes mapping spec for the tub fleet (K13_K8S_TUB_MAPPING)

Lane: background wave-lane, fleet repo local_sovereign_agent
Date: 2026-09-16
Mission: operator question "how does kubernetes fit — can the mycelial tubs be mapped to
them?" → write the concrete mapping spec: (1) tub→pod manifest sketch, (2) honest runtime
choice (k3s vs ESPHome/systemd), (3) Agones for the bones-world sessions, (4) the
reconciliation metaphor made literal (experiments as desired-state manifests composed with
the pre-registration/hash law), (5) $0 verification on existing hardware or a Pi.
Budget law: no paid APIs; WebSearch/WebFetch free; no git.
Status: OPEN (receipt created before any other work — interruption protocol).

## Progress log

- [step 0] Receipt file created before any other work (interruption protocol).
- [step 1] Context grounded in repo bytes:
  - Rig: `watch/inbox/physical_computing/receipts/C17_CUBE_INSTRUMENT_PLAN.md` — ESP32
    + 2×ADS1115 + Ag/AgCl, ≈$55 BOM, pre-registered stage 0/1/2 ladder with kill criteria,
    trail law (`memory/runs/cube01/trail.jsonl`, `mag_sensor_event.v1`, row kinds incl.
    `registration`, `void`, hash chain + G1/G2/G3 gates), `state.json` = stage +
    registration hashes. Fleet target: a dozen tubs; dead twin is a first-class arm.
  - World: `mag/wow_world.py` — deterministic, file-backed session engine
    (`memory/runs/wow_world/sessions/*.json`), world bound by `world_sha256_12`, receipt
    written on close, resume REFUSES a foreign world hash. **It is a CLI over files, not a
    socket server** — load-bearing for the Agones verdict below.
  - Presence: `dashboard/mud_relay.py` — LAN-only HTTP relay on :8766, presence-only
    (positions/vitals, 6 s expiry, no authority).
  - Agones on radar: `watch/inbox/STEALS_LEDGER_20260916.md` line 20 —
    "googleforgames/agones | Apache-2.0 | 7,022 | watch | game-server scaling on k8s —
    the venue substrate if game-c grows". Status there is already `watch`, not `adopt`.
- [step 2] Spec written below (sections 1–5), receipt ends with the required closing
  triple: mapping table, runtime recommendation, honest "what k8s buys that a scheduler
  doesn't".
- [step 3] Fact-check fired (WebSearch, free): k3s = single <100 MB binary, ARM-first,
  min 2 GB RAM / 2 cores for a server node, 512 MB / 1 core for an agent (docs.k3s.io);
  Agones current release supports k8s 1.34–1.36, installs CRDs, needs game-server port
  ranges open per node, allocation via atomic GameServerAllocation or the mTLS
  agones-allocator service (agones.dev). Sources: docs.k3s.io/installation/requirements,
  agones.dev/site/docs/installation, agones.dev/site/docs/reference/gameserverallocation.

## 1. THE MAPPING — tub = pod (with one honest wrinkle)

**The wrinkle first:** an ESP32 has ~520 KB RAM and cannot run a kubelet, so
`tub = node` is metaphor only. The operational mapping is **tub = pod fronted on a
gateway**: the pod runs on the gateway host (Windows box today, Pi at fleet scale), and
the ESP32 is the pod's leg out into physical space. What CAN live in the k8s world is
everything the tub's *reader* needs: config, probes, labels, lifecycle.

**Layers:**
- **Firmware layer** — the ESP32 sketch + readout config (ADS1115 addrs/gain, pairs,
  sample rate, stimulus pin, batch size) is the per-tub `ConfigMap`. Today's truthful
  implementation of "firmware as desired state" is **ESPHome YAML per tub**: device boots,
  reports its config, the dashboard shows drift, OTA = rolling update. ESPHome is already
  a reconciliation loop for exactly this layer — no cluster required.
- **Host layer** — one reader process per tub (ingest → hash-chained trail rows) = the
  pod; the trail directory (`memory/runs/<tub>/`) = the hostPath volume, append-only.

**Manifest sketch (k8s flavor, as spec — see §5 for the $0 way to run it):**

```yaml
# ---- per-tub ConfigMap: the readout law of ONE tub (per-tub via kustomize overlay)
apiVersion: v1
kind: ConfigMap
metadata:
  name: tub01-readout
  labels:
    mag.tub/id: tub01
    mag.tub/species: pleurotus-ostreatus
    mag.tub/arm: live                  # live | dead-twin
    mag.tub/stage: "0"                 # 0|1|2 — readiness is THIS, declared
    mag.tub/colonization-date: "2026-09-29"
    mag.tub/twin: twin-a
data:
  readout.yaml: |
    schema: mag_readout.v1
    tub: tub01
    adc:
      - {addr: 0x48, name: diff-primary, gain: 16, pairs: [[A0, A1]]}
      - {addr: 0x49, name: diff-twin,   gain: 16, pairs: [[A0, A1]]}
    sample_hz: 1
    batch: 60                 # 1 sample-batch trail row per minute (bounded row law)
    stimulus: {kind: prbs7-led, pin: GPIO26, pulse_s: 300}
    trail: /trail/trail.jsonl # hostPath -> memory/runs/cube01/
---
# ---- the reader pod: one per tub, generated from the fleet registry
apiVersion: v1
kind: Pod
metadata:
  name: tub01-reader
  labels: {app: tub-reader, mag.tub/id: tub01, mag.tub/arm: live, mag.tub/stage: "0"}
spec:
  restartPolicy: Always
  containers:
  - name: reader
    image: mag/tub-reader:stage0        # locally built, $0, no registry
    volumeMounts:
    - {name: readout, mountPath: /config}
    - {name: trail, mountPath: /trail}
    readinessProbe:                     # = colonization-stage gate (below)
      httpGet: {path: /readyz, port: 9090}
      periodSeconds: 300
    livenessProbe:                      # = flatline detector (below)
      httpGet: {path: /healthz, port: 9090}
      periodSeconds: 60
      failureThreshold: 3
  volumes:
  - name: readout
    configMap: {name: tub01-readout}
  - name: trail
    hostPath: {path: /srv/mag/runs/cube01, type: Directory}
```

**Liveness = flatline detector.** `/healthz` fails when ANY of: (a) the last N
sample-batches have RMS below the stage-0 shorted-input floor (electrode flatlined =
EVIDENCE_DEAD); (b) hash-chain verify of the trail fails (G1 breach); (c) sample gap
fraction exceeds the S0.3 bound. k8s then restarts the container — which is exactly
C17's vocabulary: **kill = rig-kill, not claim-kill**; the restart appends an explicit
`gap` row (declared, never backfilled) and counts toward C17's max-2 rig iterations
before re-scope. Self-healing and the pre-registered kill ladder are the same sentence.

**Readiness = colonization stage.** `/readyz` returns 200 only when
`state.json.stage` matches the manifest's declared `mag.tub/stage` AND the matching
`kind:"registration"` trail row's hash is present in `state.json`. A tub whose observed
stage disagrees with its declared stage leaves the Service endpoints — visible drift,
no silent analysis over the wrong stage. (An analysis dashboard selects endpoints, not
processes: ready = legal to read, not merely alive.)

**A dozen tubs ≠ `replicas: 12`.** Honest point: no two tubs are identical (twin arms,
electrode ids, stages, dates), so a StatefulSet's identical-pod replicas model does not
fit. The fleet is instead **one registry file + a generator**:

```yaml
# watch/inbox/physical_computing/fleet/TUBS.yaml  (durable artifact, the real "fleet manifest")
tubs:
  - {id: tub01, arm: live,  species: pleurotus-ostreatus, stage: 0, colonization: 2026-09-29, twin: twin-a}
  - {id: tub01d, arm: dead-twin, species: killed-substrate, stage: 0, colonization: 2026-09-29, twin: twin-a}
  # ... 12 rows total; a ~40-line stdlib generator emits ConfigMap+Pod per row
```

The generator output is what `kubectl apply -f` (or, today, systemd + ESPHome OTA)
consumes. The registry file is also the artifact that survives — same rule as INDEX.json:
bytes, not vibes.

## 2. The honest runtime choice: k3s vs ESPHome/systemd at 12 tubs

First, scope the question honestly: **k8s never touches the tub itself.** No container
runtime runs on an ESP32; firmware is flashed, not scheduled. So k3s-vs-systemd is
strictly a question about the *gateway host layer* (ingest, health, dashboard,
trail-writing, the bones world).

| | ESPHome + systemd (status quo, extended) | k3s on the gateway |
|---|---|---|
| Firmware fleet | native fit — per-tub YAML, config-drift view, OTA rollout built in | no help at all (still ESPHome below k8s) |
| Reader processes | one systemd unit per tub, `Restart=always` ≈ the liveness probe, ~20 lines | pod restarts + probes — same behavior, more moving parts |
| Per-tub config | flat files / the TUBS.yaml registry | ConfigMaps + kustomize overlays |
| Footprint | ~0 (runs on the existing Windows host or a 512 MB-class Pi agent) | server node wants **2 GB RAM / 2 cores minimum** [V: docs.k3s.io] — most of a Pi 4 |
| New failure modes | ~none (files + one process manager) | certs/tokens, sqlite/etcd datastore, arm image builds or multi-arch, upgrade treadmill, CNI/port edges |
| What it uniquely buys | — | multi-host scheduling, atomic allocation, one API across every host |
| Our topology | 1 host, 1–12 devices, all on one LAN | we do not have a multi-host problem |

**Recommendation: ESPHome + systemd now. k3s at ≥25 tubs, or ≥2 gateway hosts, or when
tubs leave the LAN** (second site needing single-pane desired state). The mission's own
hypothesis — "ESPHome now, k3s at 25+ tubs" — survives contact with the numbers: at 12
devices on one host, k3s is a 2 GB tax buying solutions to problems we don't have, and it
would still run ESPHome underneath for the only layer that touches mycelium. Write the
manifests anyway (§1) because they are also the systemd/ESPHome source of truth — the
spec costs a text file; the cluster costs a Pi.

**Revisit triggers (write these down so the decision isn't vibes later):** first second
gateway host; first off-LAN tub; first need for binary image rollbacks of the reader;
fleet crossing ~25 devices where per-host unit files stop being greppable.

## 3. Agones for the bones world — worth it at Adam-plus-friends? No. Watch stands.

**What Agones actually gives** [V: agones.dev]: GameServer/Fleet CRDs on a k8s ≥1.34
cluster, an SDK health-ping sidecar, **atomic** GameServerAllocation (no two players
handed the same server), Fleet autoscaling down to zero, per-node game-port ranges.

**What the bones world actually is** [V: `mag/wow_world.py`]: a deterministic CLI over
files. Sessions are JSON in `memory/runs/wow_world/sessions/`, the world is bound by
`world_sha256_12`, resume REFUSES a foreign world hash, and the receipt is the terminal
write. There is no socket to allocate. Presence between players already exists as the
LAN-only relay on :8766 (`dashboard/mud_relay.py`), which is authority-free by design.

**If we ever adopted it**, the shape would be: a thin `wow_gateway` shim (TCP/WS in,
verb calls out to `WorldSession.load/turn/save`) as the GameServer container; session +
receipt files on a hostPath volume; receipt-on-SIGTERM wired to Agones pod shutdown:

```yaml
# SPEC ONLY — not deployed. Kept so later adoption is a manifest, not a rewrite.
apiVersion: agones.dev/v1
kind: Fleet
metadata: {name: bones-world}
spec:
  replicas: 0                       # scale-to-zero between sessions
  template:
    spec:
      ports: [{name: default, portPolicy: Dynamic, containerPort: 7654}]
      template:
        spec:
          containers:
          - name: gateway
            image: mag/wow_gateway:v1
            lifecycle:
              preStop: {exec: {command: ["python", "-m", "mag.wow_gateway", "flush-receipts"]}}
```

Discord `/play` → bot calls GameServerAllocation → gets `ip:port` → client connects;
`replicas: 0` + allocation is the scale-to-zero story.

**The honest verdict: overkill at Adam-plus-friends.** Concurrency 1–5 over one file-
backed deterministic world has no allocation contention to arbitrate; a single systemd
process (or socket activation — which IS $0 scale-to-zero today) plus the existing
:8766 relay covers it, with zero cluster tax. The STEALS_LEDGER already has Agones as
`watch`, and this receipt confirms that grade. **Adopt triggers:** >~20 concurrent
sessions, sessions spanning multiple hosts, or untrusted public players needing
per-session isolation. **Design now so the door stays open:** (a) build the
`wow_gateway` shim with its SIGTERM→receipt contract (useful even bare — crash-safe
receipts), (b) keep the session/receipt file law intact since those bytes become the
Agones volumes, (c) keep the Fleet YAML above as spec.

## 4. The reconciliation metaphor made literal — experiments as desired state

k8s loops on one idea: a declared **spec**, an observed **status**, and a controller
that diffs them forever. Our law already has all three nouns — with one deliberate,
honest divergence:

| k8s | our implementation |
|---|---|
| spec (desired state) | the experiment manifest, compiled to a `kind:"registration"` trail row (thresholds + analysis-script hash bound BEFORE the stage's data closes — C17's iron rule) |
| status (observed) | `state.json` (stage, registration hashes) + the admission view of the trail |
| controller loop | the drift patrol / nightly janitor: recompute the hash chain (G1), re-hash raw CSV chunks against `src_sha256_12` (G2), run the replay warrant (G3), compare declared stage vs observed |
| drift → reconcile | **here we diverge, on purpose:** k8s repairs by MUTATION (edit the world to match spec); our law repairs by APPEND (`void`/`contest` rows, EVIDENCE_MUTATED / EVIDENCE_DEAD, re-anchor rule) — the ledger is never rewritten to match desire |
| `kubectl diff` / `--dry-run` | `mag.cube01_replay --verify --dry`: recompute what the registration WOULD bind, show drift, write nothing |
| GitOps (ArgoCD) | the drift patrol reading TUBS.yaml + state.json — deliberately a ~50-line stdlib loop, not ArgoCD |
| kubelet restart-on-failed-probe | C17's "kill = rig-kill, not claim-kill" — restart, append a `gap` row, count the rig iteration |

**Experiment-as-manifest** (the shape; note every field below is already a field of the
registration row C17 requires — the manifest is just its YAML face):

```yaml
apiVersion: mag.experiments/v1
kind: Experiment
metadata: {name: cube01-stage2, tub: cube01}
spec:
  stage: 2
  trials: {n: 100, balance: "50/50", order: seeded-rng}
  alpha: 0.025                      # Bonferroni x2, one-sided binomial
  baselines: [shuffled-labels, dead-twin-identical-drive]
  analysis: {module: mag.cube01_stage2, sha256_12: BOUND-AT-REGISTRATION}
  stimulus: {A: led-2hz-60s, B: marker-only-sham}
```

**Composition with the pre-registration/hash law:** applying the manifest = appending
the `registration` row carrying `manifest_sha256_12`. Any analysis run against a hash
that was not registered before that stage's data closed is **VOID by construction**
(C17's own sentence, unchanged). The manifest therefore adds a *readable, diffable,
reviewable face* to the registration row — k8s contributes the ergonomics (you can
`diff` an experiment, review it in a PR-shaped artifact, and the controller enforces
it forever), not the law. The law was already ours.

## 5. $0 verification — everything above runs on existing hardware or a Pi

| piece | hardware floor | $0 proof available TODAY |
|---|---|---|
| per-tub ConfigMaps + TUBS.yaml registry | a text file | write the registry + 40-line stdlib generator; validate emitted manifests offline with `kubectl apply --dry-run=client` / kubeconform (no cluster needed) |
| k3s itself (if ever) | server node min 2 GB RAM / 2 cores [V] — i.e. a whole Pi 4, or the Windows host via WSL2 as a disposable testbed | binary is free (Apache-2.0); nothing to buy |
| flatline + readiness probes | the Windows host (cube01 already lands there) | ~80-line stdlib script over stage-0 CSV batches: variance-vs-floor, chain re-hash, gap fraction |
| ESPHome firmware desired-state | the existing ESP32 ($9, already in the $55 BOM) | ESPHome dashboard + OTA, free |
| wow_gateway shim + receipt-on-SIGTERM | the Windows host | testable bare with a TERM signal — no Agones, no cluster |
| Agones Fleet YAML | none (spec only) | offline validation against the CRD schema only |
| drift-patrol controller | existing nightly janitor slot | it already re-hashes chains per A2 §3; extend with stage-vs-manifest diff |

Nothing in this spec requires a single new dollar before stage 0's ≈$31 electronics
(C17), and nothing requires a cluster ever — the cluster is one of three futures, all
priced: (a) 12 tubs on one host → files + systemd, (b) ≥25 tubs / multi-host → k3s on
a dedicated 2 GB+ box, (c) multiplayer world growth → Agones inside that k3s.

## FINAL — the closing triple

**The mapping table:**

| tub concept | k8s concept | our actual implementation |
|---|---|---|
| tub (container + substrate + electrodes) | Pod (fronted on the gateway — ESP32 can't run a kubelet) | ESP32 → gateway reader process → trail rows |
| firmware + readout law of one tub | per-tub ConfigMap | ESPHome YAML per tub (durable copy in `watch/inbox/physical_computing/fleet/`) |
| fleet of 12 tubs | StatefulSet replicas | NOT replicas — `TUBS.yaml` registry + stdlib generator emitting per-tub manifests |
| flatline = sensor dead | livenessProbe | variance-vs-stage-0-floor + chain re-hash + gap fraction → restart + `gap` row (rig-kill) |
| colonization stage | readinessProbe + `mag.tub/stage` label | `/readyz`: `state.json` stage == registered stage hash, else tub leaves endpoints |
| species / arm / twin / colonization date | labels | fields of `TUBS.yaml`, hash-bound into the trail at registration |
| stage 0/1/2 experiment (pre-registered) | desired-state spec (CRD face) | `kind:"registration"` trail row; manifest YAML is its reviewable face; unregistered analysis = VOID |
| controller reconciliation | diff(spec, status) loop | drift patrol / janitor: G1+G2+G3 + admission view; drift APPENDED (void/contest), never mutated |
| firmware/readout rollout | rolling update | ESPHome OTA |
| bones-world session | Agones GameServer (spec only) | `wow_gateway` shim (stdlib), receipt written on SIGTERM; sessions/receipts stay the source of truth |
| scale-to-zero between sessions | Fleet `replicas: 0` + allocation | socket activation / on-demand spawn today; :8766 relay carries presence |
| a tub dies honestly | pod eviction + event | EVIDENCE_DEAD void rows + the C17 retreat ladder ("physical altar"), pre-registered |

**Runtime recommendation:** ESPHome + systemd now; write the manifests (they cost a
text file and double as the systemd/ESPHome source of truth); adopt k3s only at ≥25
tubs, ≥2 gateway hosts, or first off-LAN tub; Agones stays `watch` — overkill at
Adam-plus-friends, and the SIGTERM→receipt shim keeps the later door open for free.

**What k8s gives us that a simple scheduler doesn't — honest answer: little, for now.**
Concretely it would add: a single declarative API across multiple hosts, atomic
game-server allocation, and binary rollbacks of reader images — all multi-host or
contention problems we do not have at 1–12 tubs on one LAN. What it gives us TODAY for
free is vocabulary and discipline, not runtime: desired state / status / reconcile /
probe are already implemented in this repo in the stronger, append-only form
(hash-chained registration rows, drift-as-append, rig-kill probes). Map the concepts,
keep the manifests as spec, don't run the cluster.

Status: FILED 2026-09-16 — spec complete, proposal tier (two-eyes pending; no cluster
gets stood up without operator word, per the same gate as stage-0 spend).
