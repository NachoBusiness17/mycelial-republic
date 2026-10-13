"""backfill_direct.py — truncation backfill, direct-to-API (no agent seats).

Why: the orchestrator agent seats crash at boot (playwright driver EPIPE,
2026-09-22) — 34 re-seeded lanes died the same death. The backfill does not
need a seat: it needs (1) the batch's raw lines, (2) one LLM call to
reconstruct, (3) an output file. This tool does exactly that on the estate's
own DeepSeek lane (the Swarm key — appropriate use, ~$0.30 total for 40
batches), with the honesty kernel enforced in the prompt.

Security (Mimosa-reviewed pattern, same as tools/blind_probe.py): pinned
https host, resolved-IP must be public (no private/loopback/link-local),
redirects disabled.

Run:  .venv/Scripts/python.exe tools/backfill_direct.py [--batches 40]
Out:  memory/runs/truncation_backfill/batch_NN.md (only where missing)
"""
import ipaddress
import json
import socket
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEPS = ROOT / "memory" / "trajectory" / "steps.jsonl"
BATCHES = ROOT / "memory" / "runs" / "truncation_backfill" / "batches.json"
OUTDIR = ROOT / "memory" / "runs" / "truncation_backfill"
ENV = ROOT / ".env"

API_HOST = "api.deepseek.com"
API_PATH = "/chat/completions"
API = "https://" + API_HOST + API_PATH
MODEL = "deepseek-chat"


def key() -> str:
    for line in ENV.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("DEEPSEEK_API_KEY not in .env")


def guard_host(host: str, port: int = 443) -> None:
    """Resolve every address for the pinned host; refuse private/loopback/link-local."""
    infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise SystemExit(f"refused non-public resolved address: {ip}")


def post_json(payload: dict, keyv: str, timeout: int = 600) -> dict:
    guard_host(API_HOST)
    body = json.dumps(payload).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + keyv,
    })
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler())
    with opener.open(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def batch_lines(batch_idx: list[int]):
    want = set(batch_idx)
    lines = {}
    with STEPS.open(encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if i in want:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                r = d.get("result") or {}
                if isinstance(r, dict) and r.get("truncated"):
                    lines[i] = {
                        "line": i,
                        "session": (d.get("session_id") or "")[:14],
                        "command": (d.get("command") or "")[:300],
                        "excerpt": str((r or {}).get("output_excerpt") or "")[:400],
                    }
    return lines


def reconstruct(keyv: str, items: list[dict], n: int) -> str:
    rows = "\n".join(
        f"- line {x['line']}: command: {x['command']} | output excerpt: {x['excerpt'] or '(none)'}"
        for x in items
    )
    prompt = (
        "These are bash steps from a coding agent's trajectory whose outputs were "
        "truncated at capture time. Reconstruct each step's LIKELY full output from "
        "the command semantics and the excerpt. This is a coding-agent workspace "
        "(Python project 'local_sovereign_agent', games in HTML5, an append-only "
        "record). For EACH step output one line:\n"
        "line <no> | <confidence high/med/low> | reconstructed output summary (under 200 chars)\n"
        "Rules: every reconstruction is Inference, not Record. If the true output is "
        "unknowable from the command alone, write 'unknowable'. Blank is allowed; "
        "invented specifics are not. No preamble.\n\nSTEPS:\n" + rows
    )
    d = post_json({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.2,
    }, keyv)
    text = d["choices"][0]["message"]["content"]
    header = (f"# Truncation Backfill — Batch {n:02d}\n\n"
              f"Source: steps.jsonl, {len(items)} truncated bash steps. "
              f"Method: direct deepseek-chat reconstruction. "
              f"**Every reconstruction is Inference, not Record** — "
              f"unknowable where unknowable.\n\n" + text + "\n")
    return header


def main() -> int:
    keyv = key()
    spec = json.loads(BATCHES.read_text(encoding="utf-8"))
    batches = spec["batches"]
    only = int(sys.argv[sys.argv.index("--batches") + 1]) if "--batches" in sys.argv else len(batches)
    done = skipped = failed = 0
    for n, batch in enumerate(batches, 1):
        out = OUTDIR / f"batch_{n:02d}.md"
        if out.is_file():
            skipped += 1
            continue
        if done + skipped >= only:
            break
        items = batch_lines(batch)
        if not items:
            out.write_text(f"# Batch {n:02d} — no truncated steps found in range\n", encoding="utf-8")
            print(f"batch {n:02d}: empty, marked done")
            done += 1
            continue
        try:
            text = reconstruct(keyv, list(items.values()), n)
            out.write_text(text, encoding="utf-8")
            done += 1
            print(f"batch {n:02d}: ok ({len(items)} steps, {len(text)} bytes)", flush=True)
        except Exception as e:
            failed += 1
            print(f"batch {n:02d}: FAIL {str(e)[:120]}", flush=True)
            time.sleep(5)
        time.sleep(1.0)  # pace the lane
    print(f"direct backfill: done={done} skipped={skipped} failed={failed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
