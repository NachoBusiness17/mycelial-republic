#!/usr/bin/env python
"""hermes-intelligent-burn lane STAGE B dispatch: assemble the prime verdict.

Stage A (GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003) burned the whole 16000
completion cap in the reasoning channel (content stub 1 char, finish=length,
$0.2503 banked); its raw reasoning IS the analysis (63,687 chars, PROPOSED).
Per the ouroboros precedent (GALA_OUROBOROS_PRIME_JUDGMENT_20261002_STAGE_A/B,
watch/inbox/gala_20260925/ouroboros/lanes/hermes-judgment_dispatch.py), stage B
re-asks with the conclusion zone inlined and demands assembly ONLY.
Four sibling receipts landed after the stage A fire and are folded in, labeled.
Exit: 0 assembled verdict landed and banked / 1 any failure.
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
MAX_TOKENS = 16000
SUBSTANCE_FLOOR = 2000
STAGE_A_DUMP = ROOT / "watch/inbox/dd_dogfood/hermes-verdict.reasoning-dump.md"
OUT = ROOT / "watch/inbox/dd_dogfood/hermes-verdict.md"
USAGE = ROOT / "memory/runs/hermes_burn/usage.jsonl"
ASK_ID = "GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003_STAGE_B"
ZONE_START = 20_000  # char 0-20000 of the dump is planning exploration; the
                     # assembled sections live from ~char 26k on (ouoro precedent 28000)

NEW_EVIDENCE = [
    "watch/inbox/dd_dogfood/hermes-patterns.md",
    "watch/inbox/dd_dogfood/selfsteal-laws.md",
    "watch/inbox/dd_dogfood/corpus-holdings.md",
    "watch/inbox/dd_dogfood/selfsteal-builds.md",
]

PREAMBLE = """You are the funded judgment head of THE GALA dd-selfsteal battery
(local_sovereign_agent estate, 2026-10-03). Your stage A analysis is COMPLETE
and banked below: it is the raw reasoning channel of z-ai/glm-5.3-prime (the
content channel returned a stub; the analysis lives in the reasoning). You do
NOT re-derive it. Your job now is ASSEMBLY ONLY: write the final deliverable.

Laws that bind the answer (unchanged):
- Trust bytes, not reports: cite the receipt file name of any claim you lean on.
- A verdict without its conditions is not a verdict: name the falsifier.
- No em-dashes anywhere. Plain hyphens only.
- One landable deliverable per item; one-sitting sized.

=== STAGE A ANALYSIS (raw reasoning, conclusion zone; early planning omitted;
the analysis was cut mid-sentence at the completion cap - complete any cut
thought from the analysis itself, do not invent new analysis) ===

"""

CONTRACT = """

=== NEW RECEIPTS (landed AFTER the stage A fire; fold them into the verdict
where they change a row; label any row they change) ===

@@EVIDENCE@@

=== CONTRACT (stage B of 2; produce ONLY this) ===
Assemble the final verdict in EXACTLY this shape, no planning prose, no
restating the contract:

1. THE BURN LEDGER VERDICT (economics): freeze, floor, or routing change; the
   exact mechanism (which file/law changes) and the falsifier.
2. THE PLAY CARRIER VERDICT (D&D corpus + live-fire): the ONE defect worth the
   next sitting and what the operator-attested actual-play intel says the
   carriers should become.
3. THE BUILD VERDICT (24h self-steal + games audit): the single
   highest-leverage one-sitting, the one ticket to drop, and whether the
   "winnable while ignoring its named mechanic" indictment generalizes to the
   estate's gates (stage A found it does, for the DISPATCH path, not the audit
   path; confirm or overturn with the new receipts).
4. THE NEXT-24H CARD: max 5 ranked rows, each: action, landing spot (file
   path), cost class (cash / seat-tokens / operator), falsifier.
5. WHAT WOULD CHANGE YOUR MIND: the single observation that flips the verdict.

Write the five sections now, in that order, with those exact headers. Be done
when section 5 ends. Do not add anything after it.
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
    dump = STAGE_A_DUMP.read_text(encoding="utf-8", errors="replace")
    # strip the stage A header (lines before the reasoning begins) from the zone
    zone = dump[ZONE_START:]
    if len(zone.strip()) < SUBSTANCE_FLOOR:
        raise RuntimeError("stage A zone under substance floor; dump too small")
    parts = [PREAMBLE, zone, CONTRACT.replace("@@EVIDENCE@@", _evidence_block())]
    return "".join(parts)


def _evidence_block() -> str:
    chunks = []
    for rel in NEW_EVIDENCE:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8", errors="replace")
        cap = 60_000
        if len(text) > cap:
            text = text[:cap] + "\n... [truncated at 60000 chars]"
        chunks.append(f"\n\n=== NEW RECEIPT {rel} ===\n{text}")
    return "".join(chunks)


def preflight(body: str) -> None:
    if not STAGE_A_DUMP.is_file() or STAGE_A_DUMP.stat().st_size == 0:
        raise RuntimeError("EVIDENCE-PREFLIGHT: stage A dump missing or empty")
    for rel in NEW_EVIDENCE:
        p = ROOT / rel
        if not p.is_file() or p.stat().st_size == 0:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: missing or empty: {rel}")
        probe = p.read_text(encoding="utf-8", errors="replace")[:400].strip()
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
    except Exception as exc:
        row["doubled_key_check_error"] = repr(exc)
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    body = build_body()
    preflight(body)
    print(f"preflight pass: stage A zone {ZONE_START}.. + "
          f"{len(NEW_EVIDENCE)} new receipts, body {len(body)} chars")
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
        bank({**row, "ok": False, "refused": (refusal or "empty")[:200]})
        raise RuntimeError(f"empty response; refusal={refusal!r} usage={usage}")
    stub = len(content.strip()) < SUBSTANCE_FLOOR
    header = json.dumps(usage, ensure_ascii=False)
    if stub:
        reasoning_text = msg.get("reasoning") or ""
        if len(reasoning_text.strip()) >= SUBSTANCE_FLOOR:
            bank({**row, "channel":
                  "reasoning-dump (content stub; raw reasoning banked)",
                  "content_chars": len(content.strip())})
            OUT.write_text(
                f"# GALA DD-SELFSTEAL PRIME JUDGMENT 2026-10-03 (stage B, "
                "REASONING-CHANNEL DUMP)\n\n"
                f"Paid run: {MODEL} via {API_HOST} (NOUS_SDD_API_KEY). "
                f"Usage: {header}\n"
                f"Lane: hermes-intelligent-burn (division B). Banked id "
                f"{ASK_ID}.\nWARNING: raw reasoning channel, PROPOSED only.\n\n"
                f"---\n\n{reasoning_text}\n", encoding="utf-8")
            print(f"STAGE-B REASONING-DUMP banked: {len(reasoning_text)} chars")
            return 1  # assembly still owed; lane seat assembles from dumps
        bank({**row, "ok": False, "content_chars": len(content.strip()),
              "substance_floor": SUBSTANCE_FLOOR,
              "note": "STUB: under floor; assembly owed by lane seat"})
        raise RuntimeError(
            f"STAGE-B STUB: content {len(content.strip())} chars, "
            f"finish={finish}; lane seat must assemble from the dumps")
    bank(row)
    footer = ("\n\n[TRUNCATED:true footer: finish_reason=" + str(finish) +
              "; this file is an owed re-ask, not a finished landing]\n") \
             if finish == "length" else \
             ("\n\n[finish_reason=" + str(finish) + "]\n")
    OUT.write_text(
        f"# GALA DD-SELFSTEAL PRIME JUDGMENT 2026-10-03\n\n"
        f"Paid run: {MODEL} via {API_HOST} (NOUS_SDD_API_KEY, the funded "
        f"tier). Stage A: GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003 "
        f"(reasoning-dump, $0.2503, banked); stage B (this file) assembled the "
        f"verdict from the banked analysis. Usage: {header}\n"
        f"Lane: hermes-intelligent-burn (division B). Banked to "
        f"memory/runs/hermes_burn/usage.jsonl id {ASK_ID}.\n"
        f"max_tokens: {MAX_TOKENS}. Stage A raw dump preserved at "
        f"watch/inbox/dd_dogfood/hermes-verdict.reasoning-dump.md (PROPOSED).\n"
        f"Evidence: stage A body carried 9 receipt files; stage B folded in 4 "
        "receipts that landed after the fire "
        "(hermes-patterns.md, selfsteal-laws.md, corpus-holdings.md, "
        "selfsteal-builds.md update).\n\n---\n\n"
        f"{content}\n{footer}",
        encoding="utf-8")
    print(f"BANKED usage row: p{row['prompt_tokens']} "
          f"c{row['completion_tokens']} finish={finish} cost={cost}")
    print(f"OUT: {OUT} ({len(content)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
