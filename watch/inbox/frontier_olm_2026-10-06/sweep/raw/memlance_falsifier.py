"""memlance fired-per-turn falsifier (descent protocol leg 7) - paired render A/B on gemma:2b.

Question (RQ4, frontier_olm_2026-10-06): does a FIRED memlance change the seat's next
output, or is the leg prompt theater?

Instrument: 5 lance tasks x 2 arms. Arm A (unlanced) gets neutral context + the question.
Arm B (lanced) gets the SAME context plus ONE seed-memory line planted among the context
lines, never addressed as an instruction (per .agents/skills/memlance/SKILL.md THROW step).
Both arms run on the local janitor (ollama gemma:2b) with temperature 0 and a fixed seed,
so each output is a deterministic function of its prompt bytes.

Determinism control: arm A of task 1 is run twice; if the two runs differ byte-wise, the
whole measurement is void (reported as such, not papered over).

Hit criterion per task: output B names the seed's distinctive token AND output A does not
AND the two outputs differ. Hit-rate >= 2/5 keeps the leg; 0/5 retires it for the janitor
class at this render shape (the skill's own falsifier line: five lances, fewer than two
hits -> Disputed).

Security posture (Mimosa-reviewed): the only URL is a compile-time constant, scheme
http, host resolved and required to be loopback before any request (SSRF-closed: no
user-controlled URL, no redirects followed, no non-loopback target possible). Output
path is anchored to this script's own directory with a fixed literal filename
(traversal-closed: no input feeds the path). $0 local. No funded-lane dispatch.
Schema: memlance_falsifier.v1.
"""
import ipaddress
import json
import socket
import urllib.request
from pathlib import Path

MODEL = "gemma:2b"
HOST = "localhost"
PORT = 11434
ONLY_SCHEME = "http"
OUT_PATH = Path(__file__).resolve().parent / "memlance_falsifier_result.json"

TASKS = [
    {
        "name": "tax_rate_location",
        "seed_token": "rates.yaml",
        "context": [
            "Repo layout: src/ holds the python modules.",
            "The billing service was refactored in August.",
        ],
        "seed": "Note from ops: the tax rate constant lives in configs/rates.yaml (moved there 2026-09-30 from src/tax.py).",
        "question": "Which file should I edit to change the tax rate? Answer with the path only.",
    },
    {
        "name": "deploy_port",
        "seed_token": "8126",
        "context": [
            "The product runs on a small fleet of Windows hosts.",
            "Deploys happen twice a week.",
        ],
        "seed": "Note from ops: the deploy target port moved to 8126 as of 2026-10-02 (was 8765).",
        "question": "What port does the deploy target use? Answer with the number only.",
    },
    {
        "name": "billing_owner",
        "seed_token": "ledger team",
        "context": [
            "Several teams share the monorepo.",
            "The billing module ships with the monthly release.",
        ],
        "seed": "Note from ops: billing module ownership transferred to the ledger team on 2026-09-28.",
        "question": "Who owns the billing module now? Answer with the team name only.",
    },
    {
        "name": "background_queue",
        "seed_token": "bees",
        "context": [
            "The estate runs several work queues under queue/lanes/.",
            "Night jobs run after midnight.",
        ],
        "seed": "Note from ops: background jobs use the bees lane (queue/lanes/bees); the worker lane is retired.",
        "question": "Which queue lane should background jobs use? Answer with the lane name only.",
    },
    {
        "name": "scut_model",
        "seed_token": "gemma2:2b-instruct",
        "context": [
            "The fleet has several local models available.",
            "Cheap repetitive work is called scut.",
        ],
        "seed": "Note from ops: fleet policy since 10-01 routes all scut through gemma2:2b-instruct.",
        "question": "Which model should route cheap scut work to? Answer with the model name only.",
    },
]


def validated_loopback_url() -> str:
    """Build the fixed ollama URL and prove the host resolves inside loopback only."""
    infos = socket.getaddrinfo(HOST, PORT, type=socket.SOCK_STREAM)
    addrs = {ipaddress.ip_address(i[4][0]) for i in infos}
    if not addrs or not all(a.is_loopback for a in addrs):
        raise RuntimeError(f"{HOST} did not resolve to loopback only: {addrs}")
    return f"{ONLY_SCHEME}://{HOST}:{PORT}/api/generate"


URL = validated_loopback_url()


def call(prompt: str) -> str:
    body = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "seed": 42, "num_predict": 60},
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8")).get("response", "")


def render(ctx, seed, question, with_seed: bool) -> str:
    lines = list(ctx)
    if with_seed and seed:
        lines.append(seed)
    lines.append("")
    lines.append("Context ends. " + question)
    return "\n".join(lines)


def main():
    rows = []
    # determinism control
    a1 = call(render(TASKS[0]["context"], None, TASKS[0]["question"], False))
    a1b = call(render(TASKS[0]["context"], None, TASKS[0]["question"], False))
    deterministic = (a1 == a1b)
    print("determinism control (arm A task1 run twice identical):", deterministic)
    if not deterministic:
        print("VOID: outputs are not deterministic under temp0/seed; measurement invalid")
        return
    for t in TASKS:
        arm_a = call(render(t["context"], None, t["question"], False)).strip()
        arm_b = call(render(t["context"], t["seed"], t["question"], True)).strip()
        tok = t["seed_token"]
        hit = (tok in arm_b) and (tok not in arm_a) and (arm_a != arm_b)
        rows.append({
            "task": t["name"], "seed_token": tok,
            "arm_a": arm_a[:200], "arm_b": arm_b[:200],
            "b_has_token": tok in arm_b, "a_has_token": tok in arm_a,
            "differ": arm_a != arm_b, "hit": hit,
        })
        print(f"{t['name']}: A={arm_a[:60]!r} B={arm_b[:60]!r} hit={hit}")
    hits = sum(1 for r in rows if r["hit"])
    verdict = ("LEG HOLDS at janitor class" if hits >= 2 else
               "DISPUTED/PROMPT THEATER at janitor class" if hits == 0 else
               "WEAK (1/5, below the skill's own 2/5 bar)")
    print("hits:", hits, "/ 5 ->", verdict)
    out = {"schema": "memlance_falsifier.v1", "model": MODEL,
           "determinism_control_passed": deterministic, "hits": hits, "n": len(rows),
           "verdict": verdict, "rows": rows}
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
