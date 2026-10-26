# STEAL — Fleet-as-Terminal + Hashable-Domain-Graph (emergent flock hardening, 2026-08-10)
**Scope (flock-eliminated):** self-stole `WINDOW_STORM_GOVERNANCE`, `SURFACES_AS_SPEC`,
`RIB_EMERGENT_FLOCK_ON_K8S`. The NEW delta from fixing the flock on K8s: two mechanisms.
**Schema:** steal.fleet_terminal_graph_hash.v1

## 1. The bug that triggered this (the delta)
The emergent flock on K8s ran, but the sampling hit `unhashable type: 'PrivateGraph'` — a default
`@dataclass` (eq=True → `__hash__=None`) keyed as a hash in the surrogate/cache path. Fixed by adding
a content-based `__hash__`. Lesson: **domain-model objects used as pipeline keys MUST be hashable by
construction**, or the pipeline silently breaks at cache/memo boundaries.

## 2. External contracts stolen

### 2.1 Hashable domain objects (dataclasses / records as keys)
- **Java records / Kotlin data classes**: value objects are hashable + equal by content by default —
  they're safe as map keys and cache keys. Python's default dataclass is the OPPOSITE (eq → unhashable).
- **Python `frozen=True` dataclasses**: make records immutable + hashable (the stdlib idiom for value objects).
- **Adapt:** ANY domain object that can be a pipeline key (PrivateGraph, SurrogateStory, task specs)
  should be `frozen=True` OR carry an explicit content `__hash__`. Rule: **if it's a value object, make
  it hashable by construction** — never rely on it never being hashed.

### 2.2 Fleet-as-terminal (pods/workers as disposable terminals fed context files)
- **CI/CD + job runners (GitHub Actions / Buildkite / Nomad)**: each job/step is a disposable terminal
  fed an explicit context (env, file mounts) — the orchestrator feeds input, the terminal returns output,
  nothing is "remembered" between runs.
- **map-reduce / data pipeline workers**: each worker gets a shard of the input (the RIB file), processes
  it, and folds results — the coordination is the input partitioning, not a live channel.
- **Adapt:** the flock pods are terminals fed RIB files (we already built this). The RIB is the input
  shard; the knot is the output fold; K8s is the scheduler. The coordination is declarative (feed files,
  read knots), not imperative (no kubectl channel needed to drive it).

### 2.3 Reconcile-the-output, not the command (GitOps / operator)
- **GitOps (ArgoCD/Flux)**: you reconcile DESIRED STATE (the config/knowledge) not ad-hoc commands; the
  controller converges the system to the declared state.
- **Adapt:** drive the flock by reconciling the RIB (the desired knowledge) → the operator creates the
  flock; the results fold into the lattice; the seat surfaces them. Feed RIB files, read knots — no
  fragile shell channel.

## 3. The rules this encodes
1. **Value objects are hashable by construction** (`frozen=True` or explicit `__hash__`) — never a
   silent `unhashable` at a cache boundary.
2. **Pods/terminals are fed context, not driven by a channel** — the RIB file is the input, the knot is
   the output; the orchestrator reconciles the knowledge, not commands.
3. **GitOps discipline** — reconcile desired state (RIB/knots) through the operator; the shell is not the
   control plane; the substrate (memory/memlang/verkle) is.

## 4. What to steal NOW (adapted)
1. Make the domain value objects (`PrivateGraph` done; audit `SurrogateStory`, task specs) hashable-by-construction.
2. Keep the flock-as-terminals-fed-RIB-files (built) — feed RIB, read knots.
3. Reconcile the RIB through the operator (GitOps) — the seat surfaces the flock's folded knots.

## Folds
Filed to `memory/steal/`. Fold as case law: "value objects hashable by construction; terminals fed
context; reconcile the knowledge not the command."
