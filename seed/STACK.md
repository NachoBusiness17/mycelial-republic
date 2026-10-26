# STACK — the software harness, and the idea underneath it

**The idea: own your own surveillance state, turned inward.** Every meter, trail, and
record in this method points at YOUR machine and writes to YOUR disk in plaintext.
Nothing phones home. The estate this seed came from watches itself — lanes, spend,
health, history — with the same apparatus a surveillance state would use, except the
watcher, the watched, and the owner are the same person. That is the product. The
software below is just the harness that makes it possible, tiered by when you need it.

| tier | add | serves | install | you need it when |
|---|---|---|---|---|
| **0 — today** | Python 3.9+ | everything boots | python.org | now (you already have it) |
| **1 — editor** | VS Code + Cline/Continue | the method auto-loads (AGENTS.md) | code.visualstudio.com | you want to work in an editor (see VSCODE.md) |
| **2 — private models** | Ollama | the T1 tier: private data NEVER leaves the box (DATA_TIERS.md) | ollama.com, then `ollama pull llama3.1` | you have T1 data or want offline inference |
| **3 — serving meters** | FastAPI + uvicorn | a loopback API over your own trails (templates/api_server_example.py) | `pip install fastapi uvicorn` | you want your meters readable by tools/dashboards |
| **3 — state** | SQLite (stdlib) | structured state beside the JSONL trails | nothing — it's built in | a JSONL trail outgrows grep |
| **4 — the cage** | Docker + compose | container boundary: localhost-only ports, record dirs mounted, nothing else escapes | docker.com + templates/docker-compose.yml | you run lanes unattended and want the blast radius contained |
| **5 — the fleet** | k3s (cheap Kubernetes) | the same containers scheduled across boxes | k3s.io | one box honestly isn't enough (most people: it is) |

**Honesty markers, per law 4:** tiers 0-2 are all most strangers ever need. Tier 3 is an
afternoon. Tier 4 is the point where you're running real spend unattended — the cage earns
its keep exactly there. Tier 5 is aspirational until it isn't; the source estate ran fine
on one box for three years.

**What we deliberately do NOT ship:** Redis, queues, k8s manifests, dashboards-as-a-service.
Delete wrappers rather than guarding them — add each only when a meter proves you need it.

**The one rule across all tiers:** the record layer is plaintext files on your disk
(JSONL, markdown, append-only). Any tool can read it; no tool is required to. That is
what "keeping your own data" means in practice.
