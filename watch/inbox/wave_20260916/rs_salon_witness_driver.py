"""RS — RACTOR SALON driver (wave 20260916, lane RS, FREE only, $0 cap).

Four witnesses over the world-build blueprint, one distinct live lane per witness.
Mirror of u5_union_witness_20260916.py's SSRF-safe call pattern (guard_endpoint, https,
provider allowlist). Key via mag.flight_recorder.load_env, never printed.
Laws: probe first, degrade gracefully; one call one receipt (never raises); 429 -> one
cooldown retry then rotate; 402/403 -> record and rotate. Blind divergence: witnesses
never see each other's posts (separate calls, shared byte-stable BRIEF, role in the tail).
Tape: memory/runs/rs_worldbuild_salon/raw.jsonl (append-as-you-go).
Posts: watch/inbox/wave_20260916/rs_witness_posts/<seat>.md
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from mag.flight_recorder import load_env, guard_endpoint  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENV = load_env()
RUN_DIR = os.path.join(ROOT, "memory", "runs", "rs_worldbuild_salon")
TAPE = os.path.join(RUN_DIR, "raw.jsonl")
POSTS_DIR = os.path.join(HERE, "rs_witness_posts")
os.makedirs(RUN_DIR, exist_ok=True)
os.makedirs(POSTS_DIR, exist_ok=True)

# id -> (base, model, env key, host, max_tokens|None, timeout)
LANES = {
    "groq-oss20": ("https://api.groq.com/openai/v1", "openai/gpt-oss-20b",
                   "GROQ_API_KEY", "api.groq.com", 2000, 120),
    "cerebras-qwen": ("https://api.cerebras.ai/v1", "qwen-3.8-27b",
                      "CEREBAS_API_KEY", "api.cerebras.ai", 2000, 120),
    "mistral-min8": ("https://api.mistral.ai/v1", "ministral-8b-latest",
                     "Mistral_API_KEY", "api.mistral.ai", 1500, 120),
    "or-union-alpha": ("https://openrouter.ai/api/v1", "stealth/union-alpha",
                       "OPENROUTER_API_KEY", "openrouter.ai", None, 300),
    "groq-oss": ("https://api.groq.com/openai/v1", "openai/gpt-oss-120b",
                 "GROQ_API_KEY", "api.groq.com", 2000, 120),
    "or-ling3": ("https://openrouter.ai/api/v1", "inclusionai/ling-3.0-flash-sante:free",
                 "OPENROUTER_API_KEY", "openrouter.ai", 2000, 120),
    "or-nemotron": ("https://openrouter.ai/api/v1", "nvidia/nemotron-3.5-lightning:free",
                    "OPENROUTER_API_KEY", "openrouter.ai", 2600, 150),
}

BRIEF = """BRIEF - the world-build blueprint under review ("The Bones-Legal World", beta of "our WoW clone", 2026-09-16)

Premise: a small text world played through Discord. AzerothCore (the WoW server core) is GPL-2.0 - its design laws were read, none of its content copied: no C++, no MySQL, no game client, no copied zones. The pitch: we compete on verifiable play - every session is a signed receipt that replays byte-identical - not on graphics or content volume.

Standing laws:
- WORLD: rooms as legality tables. A room is a status; a door is a legality row in one shared dispatch gate (VERB@ROOM rows). Missing/locked exit = typed refusal, never silent. Movement costs no RNG draws.
- COMBAT: souls grammar. Telegraph >=0.35s -> rollable i-frames -> punish. P-LEGAL: no hit without a rollable telegraph. Every-enemy-can-kill. (Combat verbs land at M3.)
- RNG: one recorded draw stream; same seed + same moves -> byte-identical replay. Replays are the QA.
- LOOT: signed pack receipts, not database rows. PLAYER FILE: append-only ledger; login is resume-from-ledger.
- ENCOUNTERS: Instance kernel, guarded DONE (boss must be IN_PROGRESS; the raid-door law).

Milestones: M0 rooms+movement through the gate - SHIPPED today (12 tests green; the full route replayed byte-identical across two separate interpreter processes). M1 authoritative room server (two clients, one observed state). M2 player files (cold-restart resume, byte-identical). M3 one zone, one enemy, one loot pack (P-LEGAL sweep; kill possible-but-avoidable). M4 /play Discord surface (gated on the operator's permission click). M5 fifty-wide adversarial playtest (zero unwinnable states; first punish under 60 seconds).

Decision made alone today, flagged for the operator: the boss encounter LOADS on the first successful non-movement verb in a room whose table lists it; DONE is attempted only while the boss is IN_PROGRESS; movement never draws and never loads. (The verbatim bones alternative: draws tick world-wide from first login.)"""

COMMON_TAIL = """Reply in EXACTLY three sections:
POST: your attack or extension in <=150 words.
NUANCE: ONE line naming a nuance the other seats will miss, ending with the milestone tag it amends (amends M0 / M1 / M2 / M3 / M4 / M5).
DIFFERENT: what you would build differently, <=60 words.
Blunt. No praise padding. Do not restate the brief."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def call(lane_id: str, prompt: str, temperature: float, seat: str, attempt: int = 1) -> dict:
    """One call, one receipt. Never raises."""
    base, model, key_name, host, max_tokens, timeout = LANES[lane_id]
    key = ENV.get(key_name, "")
    url = base.rstrip("/") + "/chat/completions"
    rec: dict = {"seat": seat, "lane": lane_id, "model": model, "temperature": temperature,
                 "ts": now(), "attempt": attempt}
    if not key:
        rec.update({"ok": False, "error": "NO_KEY", "detail": key_name})
        return rec
    body: dict = {"model": model, "temperature": temperature,
                  "messages": [{"role": "user", "content": prompt}]}
    if max_tokens is not None:
        body["max_tokens"] = max_tokens
    # seed param name differs per provider: mistral = random_seed; openai-style = seed.
    if host == "api.mistral.ai":
        body["random_seed"] = 20260916
    else:
        body["seed"] = 20260916
    try:
        guard_endpoint(url, {host})
    except Exception as e:  # noqa: BLE001
        rec.update({"ok": False, "error": "GUARD", "detail": str(e)[:200]})
        return rec
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-rs-salon/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "Mag RS Worldbuild Salon"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        rec["finish_reason"] = d["choices"][0].get("finish_reason")
        rec["usage"] = d.get("usage") or {}
        rec["latency_s"] = round(time.time() - t0, 2)
        if not txt:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200]})
        else:
            rec.update({"ok": True, "answer": txt, "chars": len(txt)})
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
        if e.code in (402, 403):
            rec["error"] = f"PAID WALL HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        rec.update({"ok": False, "error": type(e).__name__, "detail": str(e)[:400]})
    return rec


def append(rec: dict) -> None:
    with open(TAPE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def dispatch(lane_id: str, prompt: str, temperature: float, seat: str,
             retries: int = 1, cooldown: int = 20) -> dict:
    """Retry same lane once on 429/5xx; caller rotates lanes on final failure."""
    rec = call(lane_id, prompt, temperature, seat)
    while (not rec.get("ok") and retries > 0
           and str(rec.get("error", "")).startswith(("HTTP 429", "HTTP 5"))):
        retries -= 1
        append(rec)
        print(f"[rs] {seat}/{lane_id} {rec.get('error')} - cooldown retry in {cooldown}s",
              file=sys.stderr)
        time.sleep(cooldown)
        rec = call(lane_id, prompt, temperature, seat, attempt=2)
    append(rec)
    return rec


def main() -> None:
    witnesses = json.load(open(os.path.join(HERE, "rs_witness_charters.json"), encoding="utf-8"))
    pool = []
    for w in witnesses:
        for lid in w["lanes"]:
            if lid not in pool:
                pool.append(lid)

    print("== PROBE ==", flush=True)
    alive: dict[str, dict] = {}
    for lid in pool:
        rec = call(lid, "Reply with exactly: READY", 0.0, f"probe:{lid}")
        alive[lid] = rec
        print(f"[rs] probe {lid}: {'ALIVE' if rec.get('ok') else 'DEAD'} "
              f"({rec.get('error', '')} {rec.get('latency_s', '')})", flush=True)

    for w in witnesses:
        seat = w["seat"]
        prompt = f"{BRIEF}\n\n---\n\n{w['charter']}\n\n{COMMON_TAIL}"
        got = None
        for lid in w["lanes"]:
            if lid in pool and not alive.get(lid, {}).get("ok"):
                print(f"[rs] {seat}: skip {lid} (probe dead)", file=sys.stderr)
                continue
            print(f"[rs] {seat} -> {lid} (temp {w['temperature']})", flush=True)
            rec = dispatch(lid, prompt, w["temperature"], seat)
            if rec.get("ok"):
                got = rec
                break
            print(f"[rs] {seat}: {lid} failed: {rec.get('error')}", file=sys.stderr)
        out = os.path.join(POSTS_DIR, f"{w['id']}.md")
        with open(out, "w", encoding="utf-8") as fh:
            if got:
                fh.write(f"# {seat}\n\n- lane: {got['lane']} ({got['model']})\n"
                         f"- temperature: {got['temperature']}\n- usage: {got.get('usage')}\n\n"
                         f"{got['answer']}\n")
                print(f"[rs] {seat}: POST filed <- {got['lane']} ({got['chars']} chars)", flush=True)
            else:
                fh.write(f"# {seat}\n\nCONVENOR-DOUBLED (all lanes failed) - to be written "
                         f"by the convener at temp {w['temperature']}.\n")
                print(f"[rs] {seat}: ALL LANES FAILED - convener doubles", file=sys.stderr)
    print("== DONE ==", flush=True)


if __name__ == "__main__":
    main()
