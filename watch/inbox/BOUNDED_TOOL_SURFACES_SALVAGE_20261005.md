# BOUNDED TOOL SURFACES SALVAGE - pasted research-note thread banked (2026-10-05)

**Trigger:** operator pasted a ~1,300-line development thread (tmp paste attachment, ephemeral cache) on "Bounded tool surfaces as a control plane: emergent properties of MCP-mediated agents on Kubernetes from k3s to the mesh."
**Provenance:** estate sibling seat (the thread references "the recursive epistemic architecture we've been developing" and "the salon's mirror scorer" - it knew our internals; it grew out of the Estate Seed / starter-kit lane). Two or more models iterated it (ChatGPT-citation footnotes on one arm, a second model wrote the final audit).
**Status before this receipt:** not banked anywhere; existing coverage was 3 passing mentions in watch/inbox/model_garden/MCP_EXTERNAL_STEAL.md and 1 in watch/MCP_AWESOME_DIGEST.md.

## 1. What the thread contains

1. Two iterations of a research-journal prompt (HotOS / EuroSys WS / arXiv cs.DC+cs.AI framing).
2. An artifact map of eight Kubernetes MCP servers: containers/kubernetes-mcp-server (native Go API client, no kubectl, Kiali/Helm toolsets), ry-ops/k3s-mcp-server (explicit k3s kubeconfig, ~13 typed tools), alexei-led/k8s-mcp-server (containerized kubectl/helm/istioctl/argocd with allowlist), Azure/mcp-kubernetes (access-level registration filtering), Flux159/mcp-server-kubernetes (non-destructive allowlist, secret masking), giantswarm/mcp-kubernetes (OAuth 2.1, dry-run, Cluster API federation, act-as-person not ServiceAccount), razvanmacovei/k8s-multicluster-mcp (multi-kubeconfig), Stacklok ToolHive (MCP servers AS k8s workloads).
3. A draft note with findings F1 (competence tracks tool boundary, not model scale), F2 (policy-client emergence), F3 (mesh telemetry absorption into the agent loop), plus a claim-verification registry using our tri-state vocabulary.
4. An Estate Seed manifest (engines/: claritas, cooker, estate_atlas, key_law, librarian_catalog, lite_guard, model_bakeoff, phone_relay, spine_walk, stealth_sweep, task_wall; THE_METHOD.md; verify_seal.py).
5. A final audit - the sharpest artifact in the paste - and an estate-law mapping.

## 2. The steals (new to the estate)

### 2a. F2-rescued: policy discovery by error message

The audit's strongest move: no repo in the k8s MCP corpus implements permission discovery as a first-class tool - agents infer their own envelope from error messages. Falsifier: do agents converge on a correct permission model faster when a describe_my_rbac tool exists? THIS IS A CHECKABLE GAP. Estate action: diff our own surfaces against it - the shared-surface contract + effect broker authorize effects (model text proposes, switchboard authorizes); do our seats get a first-class permissions view, or do they also learn the envelope from errors? If ours answers the gap, that is a first-artifact-class answer worth writing down; if not, describe_my_rbac is a cheap organ.

### 2b. The capability-security literature anchor

The audit names the missing frame we keep re-deriving by hand: object capabilities, POLA (principle of least authority), Miller's capability-thesis line, the Confused Deputy problem. "A small typed interface composes better under adversarial use than an ambient shell" is a known result - citing it converts our bounded-surface doctrine from anecdote into instance. Action: add the citation class to starter-kit LAWS_PROVENANCE.md.

### 2c. The audit's method laws (echo our own, stated sharper)

- A bounded-only corpus is unfalsifiable: an unbounded control arm (raw shell, same chores, same model) is mandatory or the seed claim cannot lose.
- Three confounds travel together in every comparison - boundary (typed API vs shell), vocabulary size (5 tools vs 60+), substrate (in-process vs containerized CLI). Kill the confound by truncating one server's tool set to the other's size and re-running.
- Every Observed tag must cite the specific artifact and tool name; tag repo claims LOCAL (read source) / FETCHED (ran it) / HEARSAY (README). The thread's own corpus is honestly mostly HEARSAY.
- Non-destructive flags are claims, not facts: falsify against paths the flag was not written for (CRDs, finalizers, exec). Same test for secret masking (mask in the result, check logs/errors/follow-up args).
- Fault-suite minimum spec, one k3s node: ~30 chores with machine-checkable predicates, read-only vs apply arms, two model sizes, fixed token ceiling, metrics = completion rate, human interventions, blast radius, permission-model accuracy.
- Quotable, matches our gate-numbers law: "an unmeasured finding with no specified experiment is just a prediction wearing a finding's number."

### 2d. The estate mapping (INFERRED by the thread, checks out)

- law 7 one-door-per-resource (seed/THE_METHOD.md:29) = giantswarm enableDownstreamOAuth downstream identity, no SA token mounted.
- task_wall.py lane = kubeconfig + RBAC Role; cooker.py window = CronJob lease on k3s; phone_relay.py = the act-as-person OAuth passthrough model.
- ToolHive inverts the direction (cluster hosts the agents) - the same inversion our k8s_water / worldgen lanes embody.

## 3. Doctrine convergence note

The thread's central hypothesis - "a bounded tool interface may transform an open-ended language-generation problem into a partially observed control problem, and that transformation may be one of the mechanisms by which small models become operationally capable" - is the estate's 2026-10-02 doctrine (capability gap is a tools gap, not a weights gap) re-derived with a systems-venue grammar. Another independent-convergence data point for that law.

## 4. Honest tri-state

- Repo/flag claims in the thread: HEARSAY (README-level; one arm claims "verified against live sources" but this seat did not re-verify).
- The audit's critiques: OBSERVED as text (they are reasoning, sound on their face).
- The estate mapping: INFERRED (targets confirmed to exist: seed/THE_METHOD.md:29, starter-kit structure).
- The fault suite: UNMEASURED everywhere, by the thread's own admission.

## 5. Next actions (operator-gated)

1. describe_my_rbac gap check against our own effect broker / shared-surface surfaces (cheap, same-day).
2. Capability-security citation class into starter-kit LAWS_PROVENANCE.md.
3. The k3s fault suite is runnable estate hardware class; if fired, it is the first real F1/F2 measurement anyone has (the thread shows the field has zero).
