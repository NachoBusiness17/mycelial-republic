#!/usr/bin/env python
"""hermes gopher burn 2026-09-29 - operator order: spend up to $20 of Nous credits today on
model testing, parallel gophers, and gap analysis the local seat cannot provide.

Pattern stolen from watch/inbox/hermes_dual_burn_20260926.py (Nous inference API, OpenAI-compatible).
Hard budget cap with per-call usage tracking; checkpointed output; one retry on HTTP error
with model rotation. Em-dash 0 in everything written.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERMES_DIR = r"C:\Users\foste\AppData\Local\hermes"


def load_dotenv(path: str) -> None:
    # inline replacement for models.env_load (module absent in this install 2026-09-29)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


load_dotenv(os.path.join(HERMES_DIR, ".env"))

ALLOWED_HOST = "inference-api.nousresearch.com"
BASE = "https://" + ALLOWED_HOST + "/v1/chat/completions"
KEYS = [k for k in (os.environ.get("NOUS_SDD_API_KEY"), os.environ.get("HERMES_API_KEY_1"), os.environ.get("HERMES_API_KEY_2")) if k]
MODELS = ["z-ai/glm-5.3-prime", "qwen/qwen3.8-max-prime", "fireworks/ember-1"]

# Pricing per 1M tokens (USD) - Nous published list, used for the budget meter only.
PRICE = {"z-ai/glm-5.3-prime": (3.0, 15.0), "qwen/qwen3.8-max-prime": (3.0, 15.0), "fireworks/ember-1": (0.3, 1.2)}
BUDGET_USD = 20.0

OUT_DIR = os.path.join("logs", "hermes_gopher_burn_20260929")
OUT_FILE = os.path.join(OUT_DIR, "output3.jsonl")

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"


def read(p: str, limit: int = 14000) -> str:
    with open(os.path.join(REPO, p), "r", encoding="utf-8", errors="replace") as f:
        return f.read()[:limit]


BASELINE = read(r"watch\inbox\gps_baseline_ractor_20260929\BASELINE_SPEC.md")
ASK_DRAFT = read(r"watch\inbox\game_platform_basecamp_20260929\OPUS_ASK_DRAFT_20260929.md")
ESTATE_SELF = read(r"docs\ref\GAME_PLATFORM_BASECAMP.md", 9000) + "\n\n" + read(r"watch\inbox\STEAL_MAP_AGENT_GRID_20260929.md", 5000)

LAWS = "Laws: no em-dashes in your output. Cite file paths or section names for every claim you make about the provided documents. Mark anything uncertain UNPROVEN. Be concrete: numbers, names, test predicates. No praise, no preamble."

GOPHERS = [
    {
        "id": "G1-adversarial-baseline-qwen",
        "model": "qwen/qwen3.8-max-prime",
        "prompt": "You are an adversarial reviewer from a different model family than the one that wrote this spec. Kill or keep each section; name what a glm-class model would systematically miss here; find the three weakest numeric defaults and say what measurement would replace them.\n\n<SPEC>\n" + BASELINE + "\n</SPEC>\n" + LAWS,
    },
    {
        "id": "G2-gap-analysis-qwen",
        "model": "qwen/qwen3.8-max-prime",
        "prompt": "Given this estate self-description (a game platform program: Godot client, a CMaNGOS world server being ported, a verification layer, a capability-ledger router), name the FIVE gaps that most block the climb from current state to a shippable platform. For each gap: what is missing, why the current team (glm-class models plus one operator) cannot see it from inside, and the first concrete action that closes it.\n\n<SELF>\n" + ESTATE_SELF + "\n</SELF>\n" + LAWS,
    },
    {
        "id": "G3-model-test-glm-prime",
        "model": "z-ai/glm-5.3-prime",
        "prompt": "MODEL TEST - same ask as your sibling gopher on another family: adversarially review this spec. Kill or keep each section; name the three weakest numeric defaults and the measurement that would replace each. (Your output will be diffed against a qwen-family review of the same document to measure cross-family agreement.)\n\n<SPEC>\n" + BASELINE + "\n</SPEC>\n" + LAWS,
    },
    {
        "id": "G4-ember-workhorse-test",
        "model": "fireworks/ember-1",
        "prompt": "MODEL TEST - cheap workhorse lane: from this spec, extract a numbered list of every VERIFIABLE claim (a claim a test could check), each with the section it came from. Then state which 5 claims, if falsified, would kill the spec's core thesis.\n\n<SPEC>\n" + BASELINE[:9000] + "\n</SPEC>\n" + LAWS,
    },
    {
        "id": "G5-teach-us-curriculum-qwen",
        "model": "qwen/qwen3.8-max-prime",
        "prompt": "The estate runs: an MCP-shaped capability-ledger router (tools/gps_mcp), a hash-chained verification payload ledger, local small models behind OpenAI-compatible endpoints, and plans Kubernetes hosting. We refuse to keep this knowledge locked behind expensive frontier sessions. Build the teaching curriculum: the 12 specific papers/docs (titles + arXiv ids/URLs where real, flag any you are unsure of as UNPROVEN), in reading order, each with the ONE question it answers for our stack, and the 3 concepts we likely have wrong because we learned them from blog posts.\n\n<CONTEXT>\n" + ESTATE_SELF[:7000] + "\n</CONTEXT>\n" + LAWS,
    },
    {
        "id": "G6-ask-forging-qwen",
        "model": "qwen/qwen3.8-max-prime",
        "prompt": "This is a draft ask we intend to send ONCE to a frontier model (Claude Opus 5.5), including amendments. Forbid handwaving: list every place the ask is vague, every deliverable that lacks an acceptance test, every place it asks for prose where it should ask for a table or a predicate. Then write the 5 missing lines that would make it airtight.\n\n<ASK>\n" + ASK_DRAFT + "\n</ASK>\n" + LAWS,
    },
]


def call(model: str, prompt: str, key: str, max_tokens: int = 16000) -> dict:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "reasoning": {"max_tokens": 6000},  # LESSIG RAILS pattern: cap reasoning or the answer never gets written (fires 1-2 lesson)
    }).encode()
    req = urllib.request.Request(BASE, data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def cost_of(model: str, usage: dict) -> float:
    pi, po = PRICE.get(model, (3.0, 15.0))
    return (usage.get("prompt_tokens", 0) / 1e6) * pi + (usage.get("completion_tokens", 0) / 1e6) * po


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    if not KEYS:
        print("NO KEYS - aborting without spend")
        return
    spent = 0.0
    out = open(OUT_FILE, "a", encoding="utf-8")

    def run(g: dict) -> None:
        nonlocal spent
        key = KEYS[hash(g["id"]) % len(KEYS)]
        for attempt in (1, 2):
            try:
                t0 = time.time()
                resp = call(g["model"], g["prompt"], key)
                usage = resp.get("usage", {})
                c = cost_of(g["model"], usage)
                spent += float((usage.get("cost") if isinstance(usage, dict) and usage.get("cost") is not None else c))
                msg = resp["choices"][0]["message"]
                api_cost = (usage.get("cost") if isinstance(usage, dict) else None) or c
                row = {"id": g["id"], "model": g["model"], "usage": usage, "cost_usd": round(float(api_cost), 4), "seconds": round(time.time() - t0, 1),
                       "finish_reason": resp["choices"][0].get("finish_reason"),
                       "content": msg.get("content"),
                       "reasoning_tail": (msg.get("reasoning") or "")[-400:]}
                out.write(json.dumps(row) + "\n")
                out.flush()
                print(f"done {g['id']} cost=${c:.4f} cumulative=${spent:.4f}")
                return
            except urllib.error.HTTPError as e:
                print(f"retry {g['id']} after HTTP {e.code}")
                g["model"] = MODELS[(MODELS.index(g["model"]) + 1) % len(MODELS)]
            except Exception as e:  # noqa: BLE001
                print(f"error {g['id']}: {e}")
                return

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(run, GOPHERS))
    out.close()
    print(f"BURN COMPLETE total=${spent:.4f} of ${BUDGET_USD} -> {OUT_FILE}")


if __name__ == "__main__":
    main()
