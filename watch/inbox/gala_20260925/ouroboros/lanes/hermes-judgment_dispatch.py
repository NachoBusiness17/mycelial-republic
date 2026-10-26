#!/usr/bin/env python
"""hermes-judgment lane dispatch: funded glm-5.3-prime judgment over cross-lane receipts.

Pattern: watch/inbox/HERMES_PRIME_JUDGMENT_20260929.md (direct Nous call,
max_tokens sized UP for reasoning burn: 5121 of 6277 completion tokens were
reasoning on the 09-29 run). SPEND law: usage banks to
memory/runs/hermes_burn/usage.jsonl and into the receipt header.
Evidence preflight: every receipt file passed must exist, be non-empty, and its
rendered head must appear in the message body actually sent (the
DAY1_CROSS_RACTOR E3 empty-evidence law).
Exit: 0 judgment landed and banked / 1 any failure.
"""
import ipaddress
import json
import socket
import sys
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
MAX_TOKENS = 20000
SUBSTANCE_FLOOR = 2000  # chars; below this the fire is a heartbeat, not a verdict
STAGE_A_OUT = ROOT / "watch/inbox/gala_20260925/ouroboros/PRIME_JUDGMENT_STAGE_A.md"

# Transport lessons banked 2026-10-02 (fires 2 and 3: TimeoutError x2 at 900s
# with max_tokens 48000 and 32000; fire 1 with max_tokens 16000 returned in
# ~4 min). The endpoint serves the 16k-cap shape fast; larger caps stall past
# the window. So: fire 1's shape, with the prompt cut to the six lane JSONs
# (each lane's own conclusions, rows, checks, decision_changed) plus
# cadence.md, and 25 percent more completion room than fire 1.
INCLUDE = {
    "cross-drop.json", "cross-gap.json", "cross-ractor.json",
    "fleet-inventory.json", "ouroboros-synthesis.json", "standing-wave.json",
    "cadence.md",
}
OUT = ROOT / "watch/inbox/gala_20260925/ouroboros/PRIME_JUDGMENT_20261002.md"
USAGE = ROOT / "memory/runs/hermes_burn/usage.jsonl"
ASK_ID = "GALA_OUROBOROS_PRIME_JUDGMENT_20261002"


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


def gather_receipts(lanes_dir: Path, inbox_dir: Path) -> list[Path]:
    """Cross-lane receipt bytes only: sibling lane JSONs + check/grep/quote
    outputs + inbox receipt markdown. Working .py scripts and this lane's own
    artifacts (self-testimony) are excluded."""
    files: list[Path] = []
    if lanes_dir.is_dir():
        files += sorted(
            p for p in lanes_dir.iterdir()
            if p.is_file() and p.name in INCLUDE)
    if inbox_dir.is_dir():
        files += sorted(p for p in inbox_dir.iterdir()
                        if p.is_file() and p.name in INCLUDE
                        and p.name != OUT.name)
    return files


PREAMBLE = """You are the funded judgment head of THE GALA ouroboros battery
(local_sovereign_agent estate, 2026-10-02). Cross lanes each dogfooded a
fleet instrument and banked receipts. You read their bytes below and judge the
fleet itself. The fleet's own laws apply to your answer:

- Trust bytes, not reports: cite the file header of any receipt you lean on.
- A verdict without its conditions is not a verdict: name what evidence you
  lack and what would change your mind.
- No em-dashes. Plain hyphens only.
- Prefer ONE landable deliverable over a survey.

The receipts below are the cross-lane dogfood outputs. Some may be skeletons
or in-flight markers; that itself is evidence about fleet composition and
should be judged as such.

"""

CONTRACT_A = """=== CONTRACT (stage A of 2) ===
Produce, in this exact order:
1. RANKED CONTRADICTIONS: where two receipts (or a receipt and the estate's
   stated laws) disagree, most load-bearing first. For each: the two sides
   with their file names, which side the bytes favor, and the one-sitting fix.
2. META-GAPS: failures no single lane can self-resolve because they live in
   the composition layer (handoffs between lanes, shared state, sequencing).

Do NOT write the final verdict; a second stage call handles it. Keep each
item tight: two to five sentences. Be done when both lists are complete.
"""

CONTRACT_B = """=== CONTRACT (stage B of 2) ===
Stage A already banked the ranked contradictions and meta-gaps (inlined
below; do not re-derive them). Produce ONLY:
3. THE VERDICT: does this fleet compose into an ouroboros (findings feed the
   next wave's boot path) or is it a pile of tools (findings land as prose)?
   One paragraph, a falsifier for your own verdict, and the single highest
   leverage move that would flip a pile into an ouroboros if that is what
   you see.
"""


def build_body(files: list[Path], stage: str) -> str:
    if stage == "B":
        stage_a = STAGE_A_OUT.read_text(encoding="utf-8", errors="replace")
        # Stage A is a raw reasoning dump whose first ~28k chars are planning
        # exploration; the ranked conclusions live later. Feed the conclusions
        # zone (chars 28000-78000), deterministic slice, PROPOSED-status caveat
        # already in the dump header it carries if within range.
        zone = stage_a[28_000:78_000]
        head = [PREAMBLE,
                "\n=== STAGE A OUTPUT (already banked; chars 28000-78000 of "
                "the raw dump; early planning omitted) ===\n", zone,
                "\n", CONTRACT_B, "\n=== RECEIPTS (for grounding only) ==="]
        parts = head
    else:
        parts = [PREAMBLE, CONTRACT_A, "\n=== RECEIPTS ==="]
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        cap = 60_000
        if len(text) > cap:
            text = text[:cap] + "\n... [truncated at 60000 chars]"
        parts.append(f"\n\n=== RECEIPT {p} ===\n{text}")
    parts.append(
        "\n\nProduce the deliverable the CONTRACT demands. "
        "Match the requested shape exactly.")
    return "".join(parts)


def preflight(files: list[Path], body: str) -> None:
    if not files:
        raise RuntimeError("EVIDENCE-PREFLIGHT: zero receipt files; refusing "
                           "an evidence-less fire (DAY1_CROSS_RACTOR E3)")
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        probe = text[:400].strip()
        if not probe:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: empty receipt: {p}")
        if probe not in body:
            raise RuntimeError(f"EVIDENCE-PREFLIGHT: rendered bytes of {p} "
                               "absent from the body")


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
                import time
                time.sleep(20)
    raise RuntimeError(f"transport failed after 2 tries: {last!r}")


def bank(row: dict) -> None:
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    stage = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
    if stage not in {"A", "B"}:
        raise SystemExit("stage must be A or B")
    if stage == "B" and not STAGE_A_OUT.is_file():
        raise SystemExit(f"stage B needs stage A output at {STAGE_A_OUT}")
    out_path = STAGE_A_OUT if stage == "A" else OUT
    ask_id = f"{ASK_ID}_STAGE_{stage}"
    lanes_dir = ROOT / "watch/inbox/gala_20260925/ouroboros/lanes"
    inbox_dir = ROOT / "watch/inbox/ouroboros"
    files = gather_receipts(lanes_dir, inbox_dir)
    print(f"stage {stage}; receipts gathered: {len(files)}")
    for p in files:
        print(f"  {p.name} ({p.stat().st_size} bytes)")
    body = build_body(files, stage)
    preflight(files, body)
    print(f"preflight pass: body {len(body)} chars")
    key = load_key()
    resp = call(key, body)
    usage = resp.get("usage", {})
    msg = resp["choices"][0]["message"]
    content = msg.get("content") or msg.get("reasoning") or ""
    if not content:
        refusal = msg.get("refusal")
        if refusal:
            bank({"ts": now(), "id": ASK_ID, "model": MODEL, "turn": 1,
                  "refused": refusal[:200],
                  "prompt_tokens": usage.get("prompt_tokens", 0),
                  "completion_tokens": usage.get("completion_tokens", 0),
                  "ok": False})
        raise RuntimeError("empty response: both channels empty; "
                           f"refusal={refusal!r} usage={usage}")
    finish = resp["choices"][0].get("finish_reason")
    truncated = finish == "length"
    cost = usage.get("cost")
    stub = len(content.strip()) < SUBSTANCE_FLOOR
    reasoning_text = msg.get("reasoning") or ""
    if stub and len(reasoning_text.strip()) >= SUBSTANCE_FLOOR:
        # The 2026-10-02 stub pattern (fires 1/4/5): the model burns the whole
        # completion cap in the reasoning channel and the content channel gets
        # a 1-char stub. The reasoning IS the judgment analysis; bank it as a
        # clearly-marked raw dump (steal 10.3: raw channels are exempt from
        # compliance; the assembled artifact is the enforcement surface).
        bank({"ts": now(), "id": ask_id, "model": MODEL, "turn": 1,
              "prompt_tokens": usage.get("prompt_tokens", 0),
              "completion_tokens": usage.get("completion_tokens", 0),
              "reasoning_tokens": usage.get("completion_tokens_details", {})
                                  .get("reasoning_tokens"),
              "finish_reason": finish,
              "channel": "reasoning-dump (content stub; raw reasoning banked)",
              "content_chars": len(content.strip()),
              "cost_usd": cost if isinstance(cost, (int, float)) else None,
              "ok": True})
        out_path.write_text(
            f"# GALA OUROBOROS PRIME JUDGMENT 2026-10-02 (stage {stage}, "
            "REASONING-CHANNEL DUMP)\n\n"
            f"Paid run: {MODEL} via {API_HOST}. Usage: "
            f"{json.dumps(usage, ensure_ascii=False)}\n"
            f"Lane: hermes-judgment (division A). Banked id {ask_id}.\n"
            "WARNING: this is the RAW reasoning channel, not the content "
            "channel. finish_reason=length: the model hit the completion cap "
            "mid-thinking. Un-assembled vapor-shape until a later stage "
            "verifies each claim against the receipts (DAY1 steal 10.3/10.4). "
            "Every claim here is PROPOSED, never VERIFIED.\n\n---\n\n"
            f"{reasoning_text}\n"
            "\n\n[TRUNCATED:true footer: finish_reason=length; raw reasoning "
            "dump, owed verification]\n",
            encoding="utf-8")
        print(f"REASONING-DUMP banked: reasoning {len(reasoning_text)} chars, "
              f"content stub {len(content.strip())} chars, finish={finish}")
        print(f"OUT: {out_path}")
        return 0
    if stub:
        bank({"ts": now(), "id": ask_id, "model": MODEL, "turn": 1,
              "prompt_tokens": usage.get("prompt_tokens", 0),
              "completion_tokens": usage.get("completion_tokens", 0),
              "reasoning_tokens": usage.get("completion_tokens_details", {})
                                  .get("reasoning_tokens"),
              "finish_reason": finish,
              "content_chars": len(content.strip()),
              "substance_floor": SUBSTANCE_FLOOR,
              "note": "STUB: content under substance floor (heartbeat, not "
                      "food; DAY1 steal 10.4); re-ask owed with larger "
                      "completion budget",
              "cost_usd": cost if isinstance(cost, (int, float)) else None,
              "ok": False})
        raise RuntimeError(
            f"STUB fire: content {len(content.strip())} chars under floor "
            f"{SUBSTANCE_FLOOR}; finish_reason={finish}; "
            f"reasoning_tokens={usage.get('completion_tokens_details', {}).get('reasoning_tokens')}; "
            "raise max_tokens (the 4000-killed-a-verdict lesson scales with "
            "prompt size) or trim the prompt")
    row = {"ts": now(), "id": ask_id, "model": MODEL, "turn": 1,
           "prompt_tokens": usage.get("prompt_tokens", 0),
           "completion_tokens": usage.get("completion_tokens", 0),
           "reasoning_tokens": usage.get("completion_tokens_details", {})
                               .get("reasoning_tokens"),
           "finish_reason": finish,
           "channel": "content" if msg.get("content") else "reasoning",
           "cost_usd": cost if isinstance(cost, (int, float)) else None,
           "ok": True}
    bank(row)
    header = json.dumps(usage, ensure_ascii=False)
    footer = ("\n\n[TRUNCATED:true footer: finish_reason=length; this file is "
              "an owed re-ask, not a finished landing]\n") if truncated else \
             ("\n\n[finish_reason=" + str(finish) + "]\n")
    out_path.write_text(
        f"# GALA OUROBOROS PRIME JUDGMENT 2026-10-02 (stage {stage})\n\n"
        f"Paid run: {MODEL} via {API_HOST} (NOUS_SDD_API_KEY, the funded "
        f"tier). Usage: {header}\n"
        f"Lane: hermes-judgment (division A). Banked to "
        f"memory/runs/hermes_burn/usage.jsonl id {ask_id}.\n\n---\n\n"
        f"{content}\n{footer}",
        encoding="utf-8")
    print(f"BANKED usage row: p{row['prompt_tokens']} "
          f"c{row['completion_tokens']} finish={finish} cost={cost}")
    print(f"OUT: {out_path} ({len(content)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
