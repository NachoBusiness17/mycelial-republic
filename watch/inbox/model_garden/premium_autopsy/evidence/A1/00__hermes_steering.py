#!/usr/bin/env python3
"""HERMES STEERING ORGAN — Mag dispatches and steers Hermes as a remote body.

Hermes (hermes.exe) is a gopher body of the fleet (SOUL.md ractor amendment).
This organ is the steering wheel Mag holds: pack + goal only, outcomes filed
back as files with SUMMARY:/DELIVERABLE: sections.

Commands:
  dispatch "<goal>" [--persona NAME] [--dir WORKDIR] [--model M] [--timeout S]
                     [--account sdd|nacho]
      Run hermes chat -Q "<goal>" --in WORKDIR --no-restore-cwd, capture the
      output to memory/runs/hermes_jobs/<ts>.md, and append a receipt row to
      memory/runs/hermes_dispatch_log.jsonl.
      --account routes the job over the Nous Portal lane (provider nous-api):
        sdd   = S:D account, $220 armed 2026-09-07 (fleet work budget)
        nacho = Nacho Business account, $10 (petty)
      Key comes from state/hermes_routing.json -> .env (never echoed). Default
      (no --account) stays the cheap z.ai glm-5.3-flash lane.
      Personas: hermes v0.21.0 chat has NO --persona flag, so the persona
      prompt is prepended to the goal. Sources, in order:
        1. agent.personalities.<NAME> in hermes config.yaml
        2. mag/hermes_personas/<NAME>.md
  steer --resume SESSION "<nudge>"
      Mid-run steering: hermes chat -Q "<nudge>" --resume SESSION.
  jobs [n]
      Tail of the dispatch log (default 10).

Fleet laws honored: $0 on the Lite lane, pack+goal only from Mag, never echo
API keys, receipts are files. 2026-09-07, seat helm.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from mag import steer_seal  # A1 anti-forgery gate (-m mag.hermes_steering)
except ImportError:  # direct-script invocation: mag/ itself is on sys.path
    import steer_seal

ROOT = Path(__file__).resolve().parents[1]
HERMES = Path(os.environ.get("HERMES_EXE", r"C:\Users\foste\AppData\Local\hermes\bin\hermes.exe"))
HERMES_HOME = Path(os.environ.get("HERMES_HOME", r"C:\Users\foste\AppData\Local\hermes"))
LOG = ROOT / "memory" / "runs" / "hermes_dispatch_log.jsonl"
JOBS = ROOT / "memory" / "runs" / "hermes_jobs"
PERSONAS_DIR = ROOT / "mag" / "hermes_personas"
ROUTING = ROOT / "state" / "hermes_routing.json"

# Nous Portal accounts (state/hermes_routing.json is the authority; this is the
# fallback map). Values are .env VAR NAMES, never key material. Each account maps
# to a named hermes provider (config.yaml providers.nous-<account>) whose key_env
# is NOUS_<ACCOUNT>_API_KEY — the helm injects that env var per dispatch.
_ACCOUNT_ENV_FALLBACK = {"sdd": "HERMES_API_KEY_2", "nacho": "HERMES_API_KEY_1"}


def _account_env(account: str | None) -> dict[str, str]:
    """Env injection for a Nous-lane dispatch: NOUS_<ACCOUNT>_API_KEY -> the key.

    Reads the var NAME from state/hermes_routing.json (fallback map above), the
    VALUE from .env at run time. The key itself is never logged or printed.
    """
    if not account:
        return {}
    var = _ACCOUNT_ENV_FALLBACK.get(account)
    if ROUTING.is_file():
        try:
            var = (json.loads(ROUTING.read_text(encoding="utf-8"))
                   .get("accounts", {}).get(account, {}).get("env_var")) or var
        except Exception:
            pass
    if not var:
        raise SystemExit(f"unknown account {account!r}; routing file missing entry")
    for line in (ROOT / ".env").read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith(var + "="):
            val = line.split("=", 1)[1].strip()
            if val:
                return {f"NOUS_{account.upper()}_API_KEY": val}
    raise SystemExit(f"{var} empty or missing in .env — cannot route account {account!r}")

SESSION_RE = re.compile(r"\b(\d{8}_\d{6}_[0-9a-f]{4,})\b")


def _harvest_session_id(workdir: Path) -> str:
    """Best-effort: newest session id from `hermes sessions list` scoped to workdir name."""
    try:
        proc = subprocess.run([str(HERMES), "sessions", "list"], capture_output=True,
                              text=True, errors="replace", timeout=60)
        needle = workdir.name[:14]
        for ln in (proc.stdout or "").splitlines():
            parts = [p.strip() for p in ln.split("  ") if p.strip()]
            if len(parts) >= 4 and needle in parts[1]:
                m = SESSION_RE.search(parts[-1])
                if m:
                    return m.group(1)
    except Exception:
        pass
    return ""


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append_receipt(row: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_persona(name: str) -> str:
    """Persona prompt by name: hermes config personalities first, then our dir."""
    cfg = HERMES_HOME / "config.yaml"
    if cfg.is_file():
        txt = cfg.read_text(encoding="utf-8", errors="replace")
        m = re.search(rf"^\s+{re.escape(name)}:\s*(>+|-)?\s*\n?((?:\s{2,}.*\n|\s+.*\n)*)",
                      txt[txt.find("personalities"):], re.MULTILINE) if "personalities" in txt else None
        if m:
            block = (m.group(2) or "").strip()
            if block:
                return block
    p = PERSONAS_DIR / f"{name}.md"
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="replace").strip()
    known = [q.stem for q in PERSONAS_DIR.glob("*.md")] if PERSONAS_DIR.is_dir() else []
    raise SystemExit(f"unknown persona {name!r}; have file personas {known} "
                     f"+ hermes config personalities (helpful, concise, technical, ...)")


def _extract_sections(out: str) -> dict:
    """Best-effort extraction of SUMMARY:/DELIVERABLE: sections from output."""
    sections: dict[str, str] = {}
    marks = [("SUMMARY", re.compile(r"^\s*SUMMARY\s*:.*$", re.MULTILINE | re.IGNORECASE)),
             ("DELIVERABLE", re.compile(r"^\s*DELIVERABLE\s*:.*$", re.MULTILINE | re.IGNORECASE))]
    spans = []
    for name, rx in marks:
        m = rx.search(out)
        if m:
            spans.append((m.start(), name))
    spans.sort()
    for i, (start, name) in enumerate(spans):
        end = spans[i + 1][0] if i + 1 < len(spans) else len(out)
        sections[name] = out[start:end].strip()
    return sections


def _default_nous_model() -> str:
    """The $0 test model for Nous-lane dispatches (state/hermes_routing.json authority)."""
    if ROUTING.is_file():
        try:
            m = (json.loads(ROUTING.read_text(encoding="utf-8"))
                 .get("lanes", {}).get("nous", {}).get("free_test_model"))
            if m:
                return m
        except Exception:
            pass
    return "inclusionai/ling-3.0-flash-sante:free"


def _run_hermes(goal: str, workdir: Path, *, model: str | None, timeout: int,
                yolo: bool, max_turns: int | None, resume: str | None,
                account: str | None = None) -> tuple[int, str, str]:
    cmd = [str(HERMES), "chat", "-Q", "-q", goal]  # -q = query, -Q = quiet oneshot
    if resume:
        cmd += ["--resume", resume]
    else:
        cmd += ["--in", str(workdir), "--no-restore-cwd"]
    if account:
        # v12 providers: dict entries are selected by MODEL PREFIX at startup
        # (resolve_startup_model_route consults user_providers when no explicit
        # --provider is passed — an explicit --provider returns None, which is
        # what killed the flag-based attempts).
        model = f"nous-{account}/{model or _default_nous_model()}"
    if model:
        cmd += ["-m", model]
    if yolo:
        cmd += ["--yolo"]
    if max_turns:
        cmd += ["--max-turns", str(max_turns)]
    env = dict(os.environ)
    env.u
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 16586 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
": str(workdir or ""), "exit": exit_code, "output_path": str(out_path),
           "session_id": args.resume, "duration_s": dur, "model": args.model or ""}
    _append_receipt(row)
    print(f"exit={exit_code} dur={dur}s out={out_path}")
    for k, v in _extract_sections(out).items():
        print(v)
    return 0 if exit_code == 0 else 1


def cmd_jobs(args) -> int:
    if not LOG.is_file():
        print("no dispatches yet")
        return 0
    rows = [json.loads(ln) for ln in
            LOG.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    for r in rows[-args.n:]:
        kind = r.get("kind", "dispatch")
        label = r.get("resume", "") if kind == "steer" else r.get("persona", "") or r.get("dir", "")
        print(f"{r['ts']} {kind:8s} exit={r['exit']:>3} {label} :: {r.get('goal','')[:80]}")
        print(f"    -> {r.get('output_path','')}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Hermes steering organ (Mag -> hermes.exe)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dispatch", help="send a goal to a fresh Hermes session")
    d.add_argument("goal")
    d.add_argument("--persona", default=None)
    d.add_argument("--dir", default=None, help="workdir to scope the job (default: repo root)")
    d.add_argument("--model", default=None)
    d.add_argument("--account", default="sdd", choices=["sdd", "nacho"],
                   help="route over the Nous Portal lane (sdd=$220 work budget [default], "
                        "nacho=$10 petty); the config default model is $0 — pass --model "
                        "for big brains")
    d.add_argument("--max-turns", type=int, default=None)
    d.add_argument("--timeout", type=int, default=900)
    d.add_argument("--yolo", action="store_true", help="bypass approval prompts (headless jobs)")
    d.set_defaults(fn=cmd_dispatch)

    s = sub.add_parser("steer", help="nudge a live/resumable Hermes session")
    s.add_argument("--resume", required=True, help="session id (or 'latest')")
    s.add_argument("nudge")
    s.add_argument("--dir", default=None)
    s.add_argument("--model", default=None)
    s.add_argument("--max-turns", type=int, default=None)
    s.add_argument("--timeout", type=int, default=900)
    s.add_argument("--yolo", action="store_true")
    s.set_defaults(fn=cmd_steer)

    j = sub.add_parser("jobs", help="tail the dispatch log")
    j.add_argument("n", nargs="?", type=int, default=10)
    j.set_defaults(fn=cmd_jobs)

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
