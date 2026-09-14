"""Lite-lane fold job — burn Z.AI Lite quota on today's session fold (2026-08-27).

Operator order: burn down the Lite spend. Perfect Lite-shaped job: huge
cache-friendly input (stable doctrine prefix + today's receipt log), structured
output = memory fold artifacts. Uses the Lite coding-plan key, glm-5.3-flash,
thinking=low, max_tokens sized per the 5.x starvation law.
"""
import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]

PREFIX = """You are the memory-fold engine of the local_sovereign_agent fleet.
Standing laws: tri-state claims (Supported/Disputed/Unproven); receipts over
distillates; read rows not zones; knots not vibes; backup-first; sacred cows
are bones to steal. Output schema is strict JSON."""

SESSION = """
TODAY'S RECEIPT LOG (2026-08-27, key events):
1. Elder consult ranked work B>C>A>E; corrections adopted (alarm=safety-rail; G split into 3 decisions).
2. Meter dead-man alarm added to mag/cache_watch.py check #4; ledger blackout Aug26 19:49->Aug27 06:5x healed by restart.
3. Chain-v2 anchor registry spec: docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md (7 invariants, claim-before-compile).
4. Tripartite pre-build gate minted (operator teaching): shelves grep -> known-facts sweep -> anchored elder -> smack=sensor.
5. Deep self-steal: tripartite pre-exists in FORTRESS_AND_REPUBLIC (DF mapping), standing-wave lexicon, two-witness REBUILD_SPEC; only delta = wiring it as a seat-loop gate.
6. Vast.ai arc: market feed live (state/vast/market_watch.jsonl), junkyard map (wedge machines 147517/31186 blocklisted persistently), boot rails (created/stopped 5min=destroy; loading 12min; reachability probe), buyer via official SDK (state/vast/buyer.py, ollama image + vast ssh proxy ONLY path), 100-way fan-out PROVEN 313.4 tok/s on $0.099/hr 3090, steering harness (grok-2) selftest PASS, corpus packer (grok-1) PASS 4 themes x 10 questions.
7. Brain box: contract v2.1 (UD-IQ3_XXS shards x4, prebuilt llama.cpp, heartbeat status on :8001) live on Poland 4x?? no - single 3090 SK/PL machine 20092, contract 48938500; Minnesota/Nebraska hosts UNREACHABLE from desk (network-dark, both ssh proxies + ports; ollama-image hosts reachable, foreign-image hosts dark; heavy onstart blocks sshd until done).
8. Economy: Rocinante $40k inverted to ~$7k/yr rented (operator decision pending); membership = judgment-only going forward (cache-strips); boxes = conversations; ribs = wire format.
9. Qwen3:1.7b/8b fan-out laws: right-size ctx (32K default = 33GB alloc = 31% CPU offload = 12 tok/s; 4096 = 143 tok/s); ONE resident variant (OLLAMA_CONTEXT_LENGTH baked); thinking tax generalizes (/no_think).
10. Steering smoke: doctrine prefix +0.33 paired diff over baseline (n=1, noise-level, pipeline-proof only).
11. Surfaces map: docs/ref/SURFACES_EXPLOITATION_MAP.md (z.ai MCP=free research gopher via Zread; HF=unmetered take; k3s=multi-model landlord; obliterated=censorship-tax probe; hot lattice=VRAM-resident FROZEN_RIB hologram).
12. OPEN LOOPS: council session (4 questions x 4 models) waits on BRAIN-ON-BOX; sweep rib ext-fed816a5a9 still queued; 24h feed verdict automation fires 12:35 tomorrow; Lite burn-down now ordered by operator.
"""

PROMPT = PREFIX + SESSION + """
TASK: Fold today into fleet memory. Output STRICT JSON only:
{"memory_files": [{"path": "...", "one_line": "..."}],
 "knot_candidates": [{"name": "...", "one_line": "..."}],
 "open_loops": ["..."],
 "contradictions": ["..."],
 "the_one_thing": "single sentence: what mattered most today and why"}
Max 400 words total. No markdown, no preamble."""


def load_key(name: str) -> str:
    for line in (ROOT / ".env").open():
        if line.startswith(name + "="):
            return line.strip().split("=", 1)[1]
    raise SystemExit(f"no {name}")


if __name__ == "__main__":
    r = requests.post(
        "https://api.z.ai/api/paas/v4/chat/completions",
        headers={"Authorization": f"Bearer {load_key('ZAI_API_KEY_Lite')}",
                 "Content-Type": "application/json"},
        json={"model": "glm-5.3-flash",
              "thinking": {"type": "enabled", "reasoning_effort": "low"},
              "messages": [{"role": "user", "content": "/no_think " + PROMPT}],
              "max_tokens": 8192, "temperature": 0.2},
        timeout=180)
    d = r.json()
    if "choices" not in d:
        print("ERROR:", json.dumps(d)[:300])
    else:
        msg = d["choices"][0]["message"]
        content = msg.get("content") or ""
        print(content[:2500])
        u = d.get("usage", {})
        print(f"\n[lite usage: prompt {u.get('prompt_tokens')} / completion {u.get('completion_tokens')}]")
        out = ROOT / "memory" / "runs" / "folds" / "fold_20260827_lite.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        print("fold saved:", out)
