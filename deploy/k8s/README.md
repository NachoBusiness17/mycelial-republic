# Mag — Kubernetes-native deployment

The sovereign agent framework deployed as Kubernetes workloads. The architecture
maps 1:1 onto K8s primitives — this is the framework "by nature of the entire thing."

## Architecture mapping

| Mag concept | K8s primitive | Why |
|---|---|---|
| Process supervisor (autorun + ghost + dashboard) | **Deployment** `mag` (replicas: 1) | ONE supervisor — 2 pods = 2 autorun loops = double-drain |
| Dashboard / API (`:8765`, `:8000`) | **Service** `mag` (LoadBalancer) | the Control Room surface |
| Memory / logs / state (the maze, ledgers) | **PersistentVolumeClaim** `mag-state` | durable — the memory survives pod restarts |
| Config (runtime knobs, cadence) | **ConfigMap** `mag-config` | non-secret env |
| API keys | **Secret** `mag-secrets` | DEEPSEEK_API_KEY etc. |
| Queue / broker (optional) | Deployment + Service `redis` | `redis:6379` |
| Local LLM (optional) | Deployment + Service `ollama` | `ollama:11434` |
| Passive warning sweep | **CronJob** `mag-warnings` | K8s-native cadence, no hand-started terminal |

## Layout

```
deploy/k8s/
  00-namespace.yaml       # ns: mag
  mag-configmap.yaml      # runtime env + cadence knobs
  mag-secret.yaml         # API keys (CHANGE_ME -> real secrets)
  mag-pvc.yaml            # 2Gi persistent state
  mag-deployment.yaml     # the supervisor pod (replicas: 1)
  mag-service.yaml        # exposes 8765/8000
  redis.yaml              # optional queue broker
  ollama.yaml             # optional local LLM
  mag-cronjob.yaml        # passive warning sweep every 10m
  README.md
```

## Local run (Windows — the Docker prerequisite)

> **Your system currently reports Docker isn't compatible.** That's because on
> Windows, Docker needs **Docker Desktop with WSL2** (and Hyper-V/WSL2 enabled).
> This is a one-time OS-level install only you can do — Docker/K8s cannot be
> installed from inside the framework (no elevation, no system changes from code).

1. **Install Docker Desktop** (https://www.docker.com/products/docker-desktop/) and
   enable the **WSL2 backend** during install. Reboot.
2. **Install a local cluster** with `kind` (or k3d):
   ```sh
   winget install Docker.DockerDesktop
   winget install Kubernetes.kind
   kind create cluster --name mag
   ```
3. **Point kubectl at it** and build the image:
   ```sh
   docker build -t mag-sovereign:local .
   kind load docker-image mag-sovereign:local
   ```
4. **Real secrets** (never commit keys):
   ```sh
   kubectl create ns mag
   kubectl create secret generic mag-secrets -n mag \
     --from-literal=DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY \
     --from-literal=DEEPSEEK_OVERMIND_API_KEY=$DEEPSEEK_OVERMIND_API_KEY
   ```
5. **Apply**:
   ```sh
   kubectl apply -f deploy/k8s/
   ```
6. **Open the Control Room**:
   ```sh
   kubectl port-forward -n mag svc/mag 8765:8765
   # -> http://127.0.0.1:8765/
   ```

## Operate

```sh
kubectl -n mag get pods,svc,cronjob
kubectl -n mag logs deploy/mag -f          # the supervisor + autorun trail
kubectl -n mag logs job/mag-warnings-<id>  # a warning-sweep run
kubectl -n mag scale deploy/mag --replicas=1   # keep it 1 (double-drain guard)
kubectl -n mag get events --sort-by=.lastTimestamp
```

## P4 — ghost-as-operator: the knot is a Custom Resource (refactor 2026-08-10)

The whole architecture is one K8s controller pattern. The final refactor step makes it
explicit: the **Verkle knot is a CRD** (`mag-knot-crd.yaml`, kind `Knot`, group
`mag.verkle`), and **ghost is the OPERATOR** that reconciles each knot
(spec=desired / status=observed+reconciled). The source-backed memory becomes a first-class,
rescheduleable, reconcilable resource instead of a hidden pod volume.

```sh
kubectl apply -f deploy/k8s/mag-knot-crd.yaml
kubectl -n mag get knots          # the lattice as K8s resources (kind, title, state)
kubectl -n mag describe knot <name>   # spec (immutable ref_leaf card) + status (reconciled by ghost)
```

The deployment already surfaces the solved history (`mag.solved/*` annotations): single-controller,
reconcile, surfaces-as-spec, steering, standard-pattern, frontier-coordinator, verkle-substrate.
The operator reconcile (ghost reconciling Knot CRs) is the end-state that makes "castles in the sky,
foundations beneath" a native K8s loop. Migration sequencing (kind → deployment → CRD → operator)
lives in `memory/rib/RIB_REFACTOR_CONSOLIDATION_20260810.md`.

## Why replicas must stay 1

The autorun loop (fill/drain/governor/cadence) is a single logical worker. Two
pods running it = two drainers on one queue = the double-drain bug (duplicate
task spawns, races). If you need throughput, scale the **workers** (task executors),
not the supervisor.

## Next steps (Helm / GitOps)

This is plain `kubectl apply` for clarity. To make it fully GitOps-native, wrap
the same manifests in a **Helm chart** (`Chart.yaml` + `values.yaml` for image,
replicas, cadence, storage) or a Kustomize base. Ask and I'll add `deploy/helm/`.
