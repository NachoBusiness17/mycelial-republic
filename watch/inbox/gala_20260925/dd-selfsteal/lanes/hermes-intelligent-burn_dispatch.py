#!/usr/bin/env python
"""hermes-intelligent-burn lane dispatch: funded glm-5.3-prime judgment over the
dd-selfsteal sibling receipts.

Precedent: watch/inbox/gala_20260925/ouroboros/lanes/hermes-judgment_dispatch.py
(direct Nous call, max_tokens sized for reasoning burn, evidence preflight,
SPEND-law banking). Transport lessons carried forward:
- max_tokens 16000 shape returns in ~4 min; 32000/48000 stalled past 900s (2x TimeoutError on 2026-10-02 fires).
- glm-5.3-prime burns the completion cap in the reasoning channel (2026-10-02
  stub pattern: completion_tokens 20000 / reasoning_tokens 19998 /
  content_chars 1). Substance floor 2000 chars; reasoning-dump fallback banks
  the raw reasoning clearly marked PROPOSED.
- Key: NOUS_SDD_API_KEY in C:/Users/foste/AppData/Local/hermes/.env (repo .env
  carries only HERMES_API_KEY_1/2 names).
Ask (from the lane brief): what does the combined D&D corpus + 24h self-steal +
hermes burn economics teach the estate about the next 24 hours?
Exit: 0 judgment landed and banked / 1 any failure.
"""
import ipaddress
import json
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
ENV = Path(r"C:/Users/foste/AppData/Local/hermes/.env")
API_HOST = "inference-api.nousresearch.com"
API = f"https://{API_HOST}/v1/chat/completions"
MODEL = "z-ai/glm-5.3-prime"
# Ask minimum is 12000. 16000 chosen: the 12000-min ask fits the proven 16000
# shape (fast return), and glm reasoning burn ate 20000-token caps whole on
# 2026-10-02, so 12000 flat risks a stub.
MAX_TOKENS = 16000
SUBSTANCE_FLOOR = 2000  # chars; below this the fire is a heartbeat, not a verdict
OUT = ROOT / "watch/inbox/dd_dogfood/hermes-verdict.md"
USAGE = ROOT / "memory/runs/hermes_burn/usage.jsonl"
ASK_ID = "GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003"

EVIDENCE = [
    "watch/inbox/dd_dogfood/mountain-bridge.md",
    "watch/inbox/dd_dogfood/selfsteal-builds.md",
    "watch/inbox/dd_dogfood/games-audit.md",
    "watch/inbox/gala_20260925/dd-selfsteal/lanes/dd-actualplay-intel.json",
    "watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-burn-patterns.check.txt",
    "watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-burn-economics.check.txt",
    "watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-burn-economics.check2.txt",
    "corpus/game_estate/DND_ACTUALPLAY_INTEL_20261003.md",
    "watch/inbox/playground/tavern_20261003T190348Z/play.md",
]

LANE_ECON_NOTE = """
=== LANE-COMPUTED BURN ECONOMICS (hermes-intelligent-burn, this seat, computed 2026-10-03T18:42Z by summing memory/runs/hermes_burn/usage.jsonl; 1099 rows at that moment, ledger still accruing) ===
TOTAL_COST_USD 62.8473 over 1099 rows; by day: 2026-10-01 $37.7591 / 2026-10-02 $1.1739 / 2026-10-03 $23.9143.
By model (calls / cost): opus-5.5 426/$45.3564, fable-5.1 165/$7.9354, sonnet-5.5 297/$7.4728, glm-5.3-prime 5/$1.1739, haiku-4.5 206/$0.9088.
glm-5.3-prime history (the funded judgment head has fired only 5 times, 3 ids landed): 2026-10-02 GALA_OUROBOROS_PRIME_JUDGMENT_20261002 fires show reasoning_tokens eating the completion budget (completion 20000 / reasoning 19998 / content_chars 1 / finish_reason=length = STUB) until the stage A/B re-ask pattern landed content.
Sibling patterns check (hermes-burn-patterns.check.txt, below) extends this: re-burn waste 723 rows / $39.22 (62.1% of total), ok-ok refires on the same id; refusals 89 at $0.00; silent-empty fails 151 / $0.47; evidence-less paid fires $3.58.
The tavern live-fire is running DURING this judgment (latest run dir tavern_20261003T190348Z, turn rows in the ledger as you read).
"""

PREAMBLE = """You are the funded judgment head of THE GALA dd-selfsteal battery
(local_sovereign_agent estate, 2026-10-03). Division B lanes each mined one
surface: the D&D corpus, the Mountain bridge, the 24h build inventory, the
games audit, and the hermes burn economics. You read their receipt bytes below
and owe the estate ONE thing: what the next 24 hours are for. The estate's own
laws apply to your answer:

- Trust bytes, not reports: cite the receipt file name of any claim you lean on.
- A verdict without its conditions is not a verdict: name what evidence you
  lack and what observation would kill each recommendation.
- No em-dashes anywhere. Plain hyphens only.
- Prefer ONE landable deliverable per item over a survey; items must be
  one-sitting sized for a single seat.

=== THE ASK ===
What does the combined D&D corpus + 24h self-steal + hermes burn economics
teach the estate about the next 24 hours?

=== CONTRACT (produce in this exact order) ===
1. THE BURN LEDGER VERDICT (economics): the ledger says 62 percent of paid
   spend is re-burn waste on already-landed ids. Is the right next-24h move a
   spend freeze, a spend floor, or a routing change? Name the exact mechanism
   (which file/law changes) and the falsifier.
2. THE PLAY CARRIER VERDICT (D&D corpus + live-fire): the tavern and dungeon
   carriers ran all day with visible defects (persona drafting notes leaking
   into transcripts, judge-flagged voice misattribution, tavern persona
   agreement banking 0.0). Which ONE defect is worth the next sitting, and what
   does the operator-attested actual-play intel (PvP-as-core, cadence) say the
   carriers should become?
3. THE BUILD VERDICT (24h self-steal + games audit): from the five new
   carriers and the standing rails table, name the single highest-leverage
   one-sitting for the next 24 hours and the one ticket to drop. The games
   audit headline is "every level is winnable while ignoring its named
   mechanic": does that indictment generalize to the estate's gates?
4. THE NEXT-24H CARD: a ranked list (max 5 rows) of what the estate should do
   in the next 24 hours, each row: the one-sitting action, the landing spot
   (file path), the cost class (cash / seat-tokens / operator), and the
   falsifier. Rank by leverage per dollar.
5. WHAT WOULD CHANGE YOUR MIND: the single observation that would flip this
   whole verdict.

"""

CONTRACT_TAIL = """

Produce the deliverable the CONTRACT demands. Match the requested shape
exactly. Be done when all five sections are complete.
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_key() -> str:
    for line in ENV.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("NOUS_SDD_API_KEY="):
            val = line.split("=", 1)[1].strip().strip('"').strip("'")
            if val:
                return val
    raise SystemExit("no NOUS_SDD_API_KEY in hermes .env")


def assert_public_endpoint() -> None:
    infos = socket.getaddrinfo(API_HOST, 443, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise RuntimeError(f"endpoint fence: {API_HOST} resolves to {ip}")


def build_body() -> str:
    parts = [PREAMBLE, LANE_ECON_NOTE, "\n=== RECEIPTS ==="]
    for rel in EVIDENCE:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8", errors="replace")
        cap = 60_000
        if len(text) > cap:
            text = text[:cap] + "\n... [truncated at 60000 chars]"
        parts.append(f"\n\n=== RECEIPT {rel} ===\n{text}")
    parts.append(CONTRACT_TAIL)
    return "".join(parts)


def preflight(body: str) -> None:
    for rel in EVIDENCE:
        p = ROOT / rel
        if not p.is_file() or p.stat().st_size == 0:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: missing or empty: {rel}")
        probe = p.read_text(encoding="utf-8", errors="replace")[:400].strip()
        if not probe:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: empty head: {rel}")
        if probe not in body:
            raise RuntimeError(
                f"EVIDENCE-PREFLIGHT: rendered bytes of {rel} absent from body")


def call(key: str, body: str) -> dict:
    parsed = urllib.parse.urlsplit(API)
    if parsed.scheme != "https" or parsed.hostname != API_HOST:
        raise RuntimeError("endpoint fence: refusing non-allowlisted URL")
    assert_public_endpoint()
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": body}],
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")
    last = None
    for attempt in range(2):
        req = urllib.request.Request(
            API, data=payload, method="POST",
            headers={"Authorization": "Bearer " + key,
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                json.JSONDecodeError) as exc:
            last = exc
            if attempt == 0:
                time.sleep(20)
    raise RuntimeError(f"transport failed after 2 tries: {last!r}")


def bank(row: dict) -> None:
    sys.path.insert(0, str(ROOT))
    try:
        from tools.instance_guard import doubled_key_check
        row = doubled_key_check(USAGE, row)
    except Exception as exc:  # tripwire import must never silently absorb
        row["doubled_key_check_error"] = repr(exc)
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    body = build_body()
    preflight(body)
    print(f"preflight pass: {len(EVIDENCE)} receipts, body {len(body)} chars")
    key = load_key()
    resp = call(key, body)
    usage = resp.get("usage", {})
    msg = resp["choices"][0]["message"]
    content = msg.get("content") or msg.get("reasoning") or ""
    finish = resp["choices"][0].get("finish_reason")
    cost = usage.get("cost")
    row = {"ts": now(), "id": ASK_ID, "model": MODEL, "turn": 1,
           "prompt_tokens": usage.get("prompt_tokens", 0),
           "completion_tokens": usage.get("completion_tokens", 0),
           "reasoning_tokens": usage.get("completion_tokens_details", {})
                               .get("reasoning_tokens"),
           "finish_reason": finish,
           "channel": "content" if msg.get("content") else "reasoning",
           "cost_usd": cost if isinstance(cost, (int, float)) else None,
           "ok": True}
    if not content.strip():
        refusal = msg.get("refusal")
        bank({**row, "ok": False, "refused": (refusal or "empty")[:200],
              "cost_usd": cost if isinstance(cost, (int, float)) else None})
        raise RuntimeError(
            f"empty response: both channels empty; refusal={refusal!r} "
            f"usage={usage}")
    stub = len(content.strip()) < SUBSTANCE_FLOOR
    reasoning_text = msg.get("reasoning") or ""
    header = json.dumps(usage, ensure_ascii=False)
    if stub and len(reasoning_text.strip()) >= SUBSTANCE_FLOOR:
        bank({**row, "channel":
              "reasoning-dump (content stub; raw reasoning banked)",
              "content_chars": len(content.strip())})
        OUT.write_text(
            f"# GALA DD-SELFSTEAL PRIME JUDGMENT 2026-10-03 (REASONING-CHANNEL "
            "DUMP)\n\n"
            f"Paid run: {MODEL} via {API_HOST} (NOUS_SDD_API_KEY, the funded "
            f"tier). Usage: {header}\n"
            f"Lane: hermes-intelligent-burn (division B). Banked to "
            f"memory/runs/hermes_burn/usage.jsonl id {ASK_ID}.\n"
            f"max_tokens: {MAX_TOKENS} (ask minimum 12000; 16000 is the "
            "proven fast shape and leaves reasoning room per the 2026-10-02 "
            "stub lesson).\n"
            "WARNING: this is the RAW reasoning channel, not the content "
            "channel. finish_reason=" + str(finish) + ": the model hit the "
            "completion cap mid-thinking. Every claim here is PROPOSED, never "
            "VERIFIED, until a later stage verifies each claim against the "
            "receipts (DAY1 steal 10.3/10.4).\n\n---\n\n"
            f"{reasoning_text}\n"
            "\n\n[TRUNCATED:true footer: finish_reason=" + str(finish) +
            "; raw reasoning dump, owed verification]\n",
            encoding="utf-8")
        print(f"REASONING-DUMP banked: reasoning {len(reasoning_text)} chars, "
              f"content stub {len(content.strip())} chars, finish={finish}")
        print(f"OUT: {OUT}")
        return 0
    if stub:
        bank({**row, "ok": False, "content_chars": len(content.strip()),
              "substance_floor": SUBSTANCE_FLOOR,
              "note": "STUB: content under substance floor (heartbeat, not "
                      "food); re-ask owed with trimmed prompt"})
        raise RuntimeError(
            f"STUB fire: content {len(content.strip())} chars under floor "
            f"{SUBSTANCE_FLOOR}; finish_reason={finish}; "
            f"reasoning_tokens={usage.get('completion_tokens_details', {}).get('reasoning_tokens')}; "
            "trim the prompt or raise the cap and refire")
    bank(row)
    footer = ("\n\n[TRUNCATED:true footer: finish_reason=" + str(finish) +
              "; this file is an owed re-ask, not a finished landing]\n") \
             if finish == "length" else \
             ("\n\n[finish_reason=" + str(finish) + "]\n")
    OUT.write_text(
        f"# GALA DD-SELFSTEAL PRIME JUDGMENT 2026-10-03\n\n"
        f"Paid run: {MODEL} via {API_HOST} (NOUS_SDD_API_KEY, the funded "
        f"tier). Usage: {header}\n"
        f"Lane: hermes-intelligent-burn (division B). Banked to "
        f"memory/runs/hermes_burn/usage.jsonl id {ASK_ID}.\n"
        f"max_tokens: {MAX_TOKENS} (ask minimum 12000; 16000 is the proven "
        "fast shape and leaves reasoning room per the 2026-10-02 stub "
        "lesson).\n"
        f"Evidence preflight: {len(EVIDENCE)} receipt files rendered into the "
        "body, heads byte-verified in-sent (DAY1_CROSS_RACTOR E3 law).\n\n"
        f"---\n\n{content}\n{footer}",
        encoding="utf-8")
    print(f"BANKED usage row: p{row['prompt_tokens']} "
          f"c{row['completion_tokens']} finish={finish} cost={cost}")
    print(f"OUT: {OUT} ({len(content)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
