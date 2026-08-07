#!/usr/bin/env python3
"""Watch queue/handoff, solve with local Ollama (or optional cloud), write queue/results, ingest.

Default path is $0 local: OLLAMA_ESCALATE_MODEL (default qwen2.5-coder:7b, or a larger
local tag if you pull one). Cloud only if MAG_ESCALATE_CLOUD=1 and a key is present.

Usage (from Mag repo root, Mag venv):
  .\\.venv\\Scripts\\python.exe scripts\\handoff_escalation_watcher.py
  .\\.venv\\Scripts\\python.exe scripts\\handoff_escalation_watcher.py --once
  .\\.venv\\Scripts\\python.exe scripts\\handoff_escalation_watcher.py --dry

Env:
  OLLAMA_BASE              default http://127.0.0.1:11434
  OLLAMA_ESCALATE_MODEL    default qwen2.5-coder:7b
  MAG_ESCALATE_CLOUD       0|1 — allow OpenRouter/OpenAI fallback
  OPENROUTER_API_KEY       optional cloud
  OPENAI_API_KEY           optional cloud
  MAG_ESCALATE_CLOUD_MODEL default openrouter/auto or gpt-4o-mini
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_DIR = ROOT / "queue" / "handoff"
RESULTS_DIR = ROOT / "queue" / "results"
SEEN_PATH = ROOT / "logs" / "handoff_watcher_seen.json"
PY = ROOT / ".venv" / "Scripts" / "python.exe"
if not PY.is_file():
    PY = Path(sys.executable)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_seen() -> set[str]:
    if not SEEN_PATH.is_file():
        return set()
    try:
        data = json.loads(SEEN_PATH.read_text(encoding="utf-8"))
        return set(data if isinstance(data, list) else data.get("ids") or [])
    except (json.JSONDecodeError, OSError):
        return set()


def _save_seen(ids: set[str]) -> None:
    SEEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    SEEN_PATH.write_text(json.dumps(sorted(ids)[-200:], indent=2), encoding="utf-8")


def _ollama_chat(model: str, prompt: str, timeout: int = 180) -> str:
    base = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434").rstrip("/")
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Mag's escalation worker. Solve the handoff ask. "
                        "Be concrete. Prefer working code/text over preamble."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {"num_ctx": 8192},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer ollama"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    return (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
        .strip()
    )


def _cloud_chat(prompt: str, timeout: int = 120) -> tuple[str, str]:
    """Return (text, provider_label). Prefer OpenRouter, then OpenAI."""
    model = os.environ.get("MAG_ESCALATE_CLOUD_MODEL", "").strip()
    or_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OR_API_KEY")
    oa_key = os.environ.get("OPENAI_API_KEY")
    if or_key:
        url = "https://openrouter.ai/api/v1/chat/completions"
        key = or_key
        model = model or "openrouter/auto"
        label = f"openrouter:{model}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "HTTP-Referer": "http://127.0.0.1:8765",
            "X-Title": "Mag Handoff Watcher",
        }
    elif oa_key:
        url = "https://api.openai.com/v1/chat/completions"
        key = oa_key
        model = model or "gpt-4o-mini"
        label = f"openai:{model}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        }
    else:
        raise RuntimeError("MAG_ESCALATE_CLOUD=1 but no OPENROUTER_API_KEY or OPENAI_API_KEY")

    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are Mag's scarce escalation seat. Be concrete."},
                {"role": "user", "content": prompt},
            ],
        }
    ).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    text = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
        .strip()
    )
    return text, label


def _build_prompt(h: dict) -> str:
    checks = h.get("success_checks") or []
    checks_txt = "\n".join(f"- {c}" for c in checks) if checks else "- Deliverable present"
    return (
        f"Handoff id: {h.get('id')}\n"
        f"Goal: {h.get('goal')}\n"
        f"Tier: {h.get('tier')}\n"
        f"Return path: {h.get('return_path')}\n\n"
        f"## Ask\n{h.get('ask')}\n\n"
        f"## Success checks\n{checks_txt}\n\n"
        "Answer the ask fully. Put the main deliverable first."
    )


def _write_result(handoff_id: str, ok: bool, summary: str, deliverable: str, backend: str) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / f"{handoff_id}.json"
    packet = {
        "schema": "result.v1",
        "handoff_id": handoff_id,
        "ok": ok,
        "summary": summary[:4000],
        "deliverable": deliverable[:20000],
        "backend": backend,
        "created_at": _now(),
    }
    path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return path


def _ingest(handoff_id: str) -> tuple[int, str]:
    proc = subprocess.run(
        [str(PY), str(ROOT / "main.py"), "ingest", handoff_id],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def process_one(path: Path, *, dry: bool = False) -> str:
    h = json.loads(path.read_text(encoding="utf-8"))
    hid = str(h.get("id") or path.stem)
    result_path = RESULTS_DIR / f"{hid}.json"
    if result_path.is_file():
        return f"skip {hid}: result already exists"

    prompt = _build_prompt(h)
    model = os.environ.get("OLLAMA_ESCALATE_MODEL", "qwen2.5-coder:7b")
    backend = f"ollama:{model}"
    text = ""
    err = ""

    if dry:
        text = f"[dry-run] would escalate {hid} via {backend}"
        ok = True
    else:
        try:
            text = _ollama_chat(model, prompt)
            ok = bool(text)
        except Exception as e:
            err = str(e)
            ok = False
            if os.environ.get("MAG_ESCALATE_CLOUD", "0").strip() in ("1", "true", "yes"):
                try:
                    text, backend = _cloud_chat(prompt)
                    ok = bool(text)
                    err = ""
                except Exception as e2:
                    err = f"local: {err}; cloud: {e2}"
                    text = f"ESCALATION FAILED: {err}"
                    ok = False
            else:
                text = f"ESCALATION FAILED (local only): {err}"
                ok = False

    summary = (text[:400] + "…") if len(text) > 400 else text
    if not ok and err:
        summary = f"failed: {err}"
    rpath = _write_result(hid, ok, summary, text or summary, backend)
    code, ingest_out = _ingest(hid) if not dry else (0, "dry-skip ingest")
    return (
        f"{'ok' if ok else 'fail'} {hid} -> {rpath.name} backend={backend} "
        f"ingest_rc={code} {ingest_out[:200]}"
    )


def list_pending(seen: set[str]) -> list[Path]:
    if not HANDOFF_DIR.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(HANDOFF_DIR.glob("*.json")):
        if p.name.startswith("."):
            continue
        hid = p.stem
        if hid in seen:
            continue
        if (RESULTS_DIR / f"{hid}.json").is_file():
            continue
        out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Mag handoff escalation watcher")
    ap.add_argument("--once", action="store_true", help="Process pending once and exit")
    ap.add_argument("--poll", type=float, default=5.0, help="Seconds between polls")
    ap.add_argument("--dry", action="store_true", help="Write dry-run results only")
    args = ap.parse_args()

    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    seen = _load_seen()
    print(f"[watcher] root={ROOT}")
    print(f"[watcher] handoff={HANDOFF_DIR}")
    print(f"[watcher] results={RESULTS_DIR}")
    print(f"[watcher] model={os.environ.get('OLLAMA_ESCALATE_MODEL', 'qwen2.5-coder:7b')}")
    print(f"[watcher] cloud={os.environ.get('MAG_ESCALATE_CLOUD', '0')}")

    while True:
        pending = list_pending(seen)
        if pending:
            for p in pending:
                print(f"[watcher] processing {p.name} @ {_now()}")
                try:
                    msg = process_one(p, dry=args.dry)
                    print(f"[watcher] {msg}")
                    seen.add(p.stem)
                    _save_seen(seen)
                except Exception as e:
                    print(f"[watcher] ERROR {p.name}: {e}")
        elif args.once:
            print("[watcher] no pending handoffs")
            return 0
        if args.once:
            return 0
        time.sleep(max(1.0, args.poll))


if __name__ == "__main__":
    raise SystemExit(main())
