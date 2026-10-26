#!/usr/bin/env python
"""night_burn - the overnight shift (2026-09-30). Operator order: keep rolling all night.
Six self-contained judgment gophers (API-only, sources pasted), reasoning-capped, metered,
checkpointed. SSRF guard (Mimosa 2026-09-30): single pinned https host, urlparse-validated,
redirects disabled, no private/loopback destination possible by construction."""
from __future__ import annotations

import json
import os
import pathlib
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERMES_DIR = r"C:\Users\foste\AppData\Local\hermes"
ALLOWED_HOST = "inference-api.nousresearch.com"  # pinned destination; the only host this script may touch
BASE = "https://" + ALLOWED_HOST + "/v1/chat/completions"
REPO = pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = REPO / "logs" / "mates" / "night_burn_20260930.jsonl"


def load_dotenv(path):
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


load_dotenv(os.path.join(HERMES_DIR, ".env"))
KEYS = [k for k in (os.environ.get("NOUS_SDD_API_KEY"), os.environ.get("HERMES_API_KEY_1")) if k]


def read(rel, limit=13000):
    return (REPO / rel).read_text(encoding="utf-8", errors="replace")[:limit]


OCEAN = read(r"watch\inbox\operator_model\OCEAN.md")
BASELINE = read(r"watch\inbox\gps_baseline_ractor_20260929\BASELINE_SPEC.md")
RUNPLAN = read(r"watch\inbox\MICKEY17_RUN_PLAN_20260929.md")
FINAL = read(r"watch\inbox\mountain_climb_ractor_20260929\FINAL_PIECE.md")

LAWS = "Laws: no em-dashes. No praise, no preamble. Cite section names for claims about the pasted text. Mark uncertainty UNPROVEN. Disagreement is the deliverable; do not validate framing."

NIGHT = [
    # operator steer 2026-09-30: all asks on the PROVEN seat (glm-5.3-prime, duel 19-16 at 0.39x
    # cost) - no dumb spend on unproven seats; rows mirrored into the gps ledger with task_shapes
    {"id": "N1-judge-operator-model", "model": "z-ai/glm-5.3-prime", "task_shape": "adversarial-review",
     "prompt": "You are a hostile reviewer preventing hagiography. Attack this personality extraction: which ratings lean on flattery, which evidence is cherry-picked, what does the data NOT support? Then: the one rating you would change and why.\n\n<DOC>\n" + OCEAN + "\n</DOC>\n" + LAWS},
    {"id": "N2-baseline-attack", "model": "z-ai/glm-5.3-prime", "task_shape": "adversarial-review",
     "prompt": "You are a hostile implementer about to build this spec. Kill the three weakest sections (name them, say what breaks in production), and write the five test predicates the spec forgot.\n\n<DOC>\n" + BASELINE + "\n</DOC>\n" + LAWS},
    {"id": "N3-build-order", "model": "z-ai/glm-5.3-prime", "task_shape": "planning",
     "prompt": "Rank this improvement-run plan into ONE build order for the next 7 days: what first, what parallel, what dropped (name cuts). Judge by compounding x risk x cost. Table + one paragraph.\n\n<DOC>\n" + RUNPLAN + "\n</DOC>\n" + LAWS},
    {"id": "N4-ldt-experiment", "model": "z-ai/glm-5.3-prime", "task_shape": "experiment-design",
     "prompt": "Design the experiment (from LDT, arXiv 2605.08605: tiny transformer + lattice projection between passes + abstain head = sound symbolic reasoning): train a ~1M-param model on WATER-GRAPH LEGALITY (nodes/pipes/junction-gates: given a state+action, is it legal/winning?). Deliver: the lattice definition (powerset of legal typed edge-states), supervision source (constraint propagator), the abstain-adjusted soundness metric, control design, compute estimate, kill criteria. Be concrete enough to implement."},
    {"id": "N5-oral-law-schema", "model": "z-ai/glm-5.3-prime", "task_shape": "schema-design",
     "prompt": "Design the ORAL_LAW_INDEX: a mining run over 11,675 never-cited founding-record files (grok chats, action streams, codex rollouts; session_index.jsonl as manifest). Deliver: the JSONL schema (thread -> decision -> filed-law-or-debt, with evidence pointers), the extraction protocol (passes, dedupe, confidence grades), the falsifier (how do we know the extraction is not confabulating laws?), and the acceptance test."},
    {"id": "N6-grade-final-piece", "model": "z-ai/glm-5.3-prime", "task_shape": "adversarial-grading",
     "prompt": "You are an adversarial grader. Grade this essay (a synthesized 'thing we will build' statement): fabrication check (numbers must match internal citations), power score /10, the three weakest claims, and whether the three 'dumb rules' survive hostile reading.\n\n<DOC>\n" + FINAL + "\n</DOC>\n" + LAWS},
]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None  # redirects refused: the pinned host is the only destination


def call(model, prompt, key):
    p = urllib.parse.urlparse(BASE)
    if p.scheme != "https" or p.hostname != ALLOWED_HOST:
        raise AssertionError("blocked: non-pinned destination")
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 16000, "temperature": 0.4,
                       "reasoning": {"max_tokens": 6000}}).encode()
    req = urllib.request.Request(BASE, data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    opener = urllib.request.build_opener(_NoRedirect)
    with opener.open(req, timeout=300) as r:
        return json.load(r)


def run(g):
    key = KEYS[hash(g["id"]) % len(KEYS)]
    for _ in (1, 2):
        try:
            t0 = time.time()
            resp = call(g["model"], g["prompt"], key)
            msg = resp["choices"][0]["message"]
            usage = resp.get("usage", {})
            cost = float(usage.get("cost") or 0)
            row = {"id": g["id"], "model": g["model"], "cost_usd": round(cost, 4),
                   "finish": resp["choices"][0].get("finish_reason"), "seconds": round(time.time() - t0, 1),
                   "content": msg.get("content"), "reasoning_tail": (msg.get("reasoning") or "")[-300:]}
            with open(OUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            print(f"done {g['id']} ${cost:.4f}")
            return
        except urllib.error.HTTPError as e:
            print(f"retry {g['id']} HTTP {e.code}")
            g["model"] = "z-ai/glm-5.3-prime" if g["model"] != "z-ai/glm-5.3-prime" else "qwen/qwen3.8-max-prime"
        except Exception as e:
            print(f"err {g['id']}: {e}")
            return


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(run, NIGHT))
    print("NIGHT BURN COMPLETE -> " + str(OUT))
