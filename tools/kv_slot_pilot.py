#!/usr/bin/env python3
"""KV slot cold store pilot (Mag Estate, lane A4).

Replays the 10 longest stored agent sessions against a local llama-server that
loads an EXISTING .ollama GGUF blob (no re-download), with q8_0 KV quantization
and --slot-save-path slots named <model-digest>-<prompt-hash>.bin, restored on
prefix match.

Exit codes: 0 = pilot ran; 3 = NOT_INSTALLED (staged); 1 = error.

Stdlib only (Python 3.11). House python:
  C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROJECT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
BLOBS = Path(r"C:\Users\foste\.ollama\models\blobs")
MANIFESTS = Path(r"C:\Users\foste\.ollama\models\manifests\registry.ollama.ai\library")
KV_DIR = Path(r"C:\Users\foste\.llama-kv-slots")
SESSIONS_DIR = PROJECT / "memory" / "agent_sessions"
DEFAULT_MODEL = "qwen2.5:7b"  # manifest: MANIFESTS/qwen2.5/7b
TOP_N = 10
MODEL_LAYER = "application/vnd.ollama.image.model"

# Common llama.cpp install locations on Windows, checked beyond PATH.
# The vendored in-tree build is checked FIRST (2026-10-05, lane B4): tools/llamacpp/
# ships llama-server.exe (plus llama-bench.exe and siblings, Vulkan + CPU backends),
# so find_llama_server() resolves with zero install steps on this machine.
# Fix receipt: watch/inbox/build_wave_20261005/b4_kv_sweep.md
COMMON_PATHS = [
    PROJECT / "tools" / "llamacpp" / "llama-server.exe",
    Path(r"C:\Program Files\llama.cpp\llama-server.exe"),
    Path(r"C:\llama.cpp\llama-server.exe"),
    Path(r"C:\tools\llama.cpp\llama-server.exe"),
    Path(os.path.expandvars(r"%LOCALAPPDATA%\llama.cpp\llama-server.exe")),
    Path(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\llama-server.exe")),
    Path.home() / "llama.cpp" / "llama-server.exe",
    Path.home() / "scoop" / "shims" / "llama-server.exe",
    Path.home() / ".cargo" / "bin" / "llama-server.exe",
]

INSTALL_STEP = (
    "NOT_INSTALLED\n"
    "Install llama.cpp (provides llama-server). Exact step, verified present in winget\n"
    "(`winget search --id ggml.llamacpp -e` -> `llama.cpp  ggml.llamacpp  b11057  winget`):\n"
    "  winget install --id ggml.llamacpp -e --source winget\n"
    "Then re-run:\n"
    "  C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe \\\n"
    "    C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\tools\\kv_slot_pilot.py\n"
    "Plan: tools/kv_slot_pilot.md"
)

# ---------------------------------------------------------------------------
# Loopback-pinned HTTP transport (anti-SSRF by construction):
#   * scheme is the literal "http"  -  never taken from input;
#   * host is the literal IP "127.0.0.1"  -  no hostname, so no DNS resolution
#     and therefore no DNS rebinding surface;
#   * every request path must match a strict allowlist regex; slot filenames
#     are produced only by slot_name() (hex hashes), never from external input;
#   * redirects are disabled;
#   * the port must be the port of the llama-server this script spawned itself.
# This client never fetches an operator- or session-supplied URL and downloads
# nothing (model blobs are reused in place).
# ---------------------------------------------------------------------------
_API_PATH = re.compile(
    r"^/(?:health"
    r"|completion"
    r"|slots/0\?action=(?:save|restore)&filename=[0-9a-f]{16}-[0-9a-f]{16}\.bin"
    r")$"
)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def http(port: int, method: str, path: str, payload: dict | None = None) -> dict:
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError(f"bad port: {port!r}")
    if not _API_PATH.match(path):
        raise ValueError(f"non-allowlisted API path rejected: {path!r}")
    url = f"http://127.0.0.1:{port}{path}"
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"})
    try:
        with _OPENER.open(req, timeout=600) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"llama-server {method} {path} -> HTTP {e.code}") from e


def find_llama_server() -> str | None:
    """Locate llama-server on PATH or in common install paths."""
    found = shutil.which("llama-server")
    if found:
        return found
    for p in COMMON_PATHS:
        if p.is_file():
            return str(p)
    return None


def resolve_gguf_blob(model: str) -> Path:
    """Map an Ollama model tag to its existing GGUF blob (no download)."""
    name, _, tag = model.partition(":")
    manifest = MANIFESTS / name / (tag or "latest")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for layer in data.get("layers", []):
        if layer.get("mediaType") == MODEL_LAYER:
            digest = layer["digest"].split(":", 1)[1]
            blob = BLOBS / f"sha256-{digest}"
            if not blob.is_file():
                raise FileNotFoundError(f"manifest maps {model} to missing blob {blob}")
            return blob
    raise ValueError(f"no {MODEL_LAYER} layer in manifest {manifest}")


def longest_sessions(n: int) -> list[dict]:
    """Rank sessions by total message characters; keep top n with a user message."""
    ranked: list[tuple[int, Path, str]] = []
    for p in SESSIONS_DIR.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        msgs = data.get("messages")
        if not isinstance(msgs, list):
            continue
        first_user = next(
            (m.get("content", "") for m in msgs
             if isinstance(m, dict) and m.get("role") == "user"), "")
        if not first_user:
            continue
        score = sum(len(str(m.get("content", ""))) for m in msgs if isinstance(m, dict))
        ranked.append((score, p, str(first_user)))
    ranked.sort(reverse=True)
    return [{"path": str(p), "score": s, "prompt": pu} for s, p, pu in ranked[:n]]


def slot_name(model_digest: str, prompt: str) -> str:
    """<model-digest>-<prompt-hash>.bin (16 hex chars each; see kv_slot_pilot.md §5)."""
    return f"{model_digest[:16]}-{hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:16]}.bin"


def wait_healthy(port: int, timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if http(port, "GET", "/health").get("status") == "ok":
                return
        except (RuntimeError, OSError, json.JSONDecodeError):
            pass
        time.sleep(1.0)
    raise TimeoutError("llama-server did not become healthy")


def launch_candidates(exe: str, blob: Path, port: int) -> list[list[str]]:
    base = ["-m", str(blob), "--host", "127.0.0.1", "--port", str(port),
            "--slot-save-path", str(KV_DIR),
            "--cache-type-k", "q8_0", "--cache-type-v", "q8_0",
            "-c", "32768", "--parallel", "1"]
    return [
        # (1) newer builds: --flash-attn on  (2) older boolean --flash-attn
        # (3) degrade to K-only q8_0 (V-quant needs flash attention)  -  logged.
        [exe, *base, "--flash-attn", "on"],
        [exe, *base, "--flash-attn"],
        [exe, "-m", str(blob), "--host", "127.0.0.1", "--port", str(port),
         "--slot-save-path", str(KV_DIR), "--cache-type-k", "q8_0",
         "-c", "32768", "--parallel", "1"],
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="KV slot cold store pilot (see kv_slot_pilot.md)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="Ollama tag (manifest lookup)")
    ap.add_argument("--port", type=int, default=8081)
    ap.add_argument("--top", type=int, default=TOP_N)
    args = ap.parse_args()

    exe = find_llama_server()
    if not exe:
        print(INSTALL_STEP)
        return 3
    print(f"llama-server: {exe}")

    blob = resolve_gguf_blob(args.model)
    model_digest = blob.stem.removeprefix("sha256-")
    print(f"model {args.model} -> existing blob {blob.name} ({blob.stat().st_size} bytes)")

    KV_DIR.mkdir(parents=True, exist_ok=True)
    sessions = longest_sessions(args.top)
    if len(sessions) < args.top:
        print(f"WARNING: only {len(sessions)} eligible sessions in {SESSIONS_DIR}")
    print(f"replaying {len(sessions)} longest sessions (by total message chars):")
    for i, s in enumerate(sessions, 1):
        print(f"  {i:2d}. {Path(s['path']).name}  score={s['score']}")

    proc = None
    used_flags = None
    for cand in launch_candidates(exe, blob, args.port):
        try:
            proc = subprocess.Popen(
                cand, cwd=str(KV_DIR),
                creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError as e:
            print(f"launch failed ({e}); trying next flag set")
            continue
        time.sleep(2.0)
        if proc.poll() is not None:
            print(f"llama-server exited rc={proc.returncode}; trying next flag set")
            proc = None
            continue
        used_flags = cand
        break
    if proc is None:
        print("ERROR: could not launch llama-server with any known flag set")
        return 1
    kv_flags = [k for k in used_flags
                if k in ("--slot-save-path", "--cache-type-k", "q8_0",
                         "--cache-type-v", "--flash-attn", "on")]
    print(f"launched with KV flags: {' '.join(kv_flags)}")

    results = []
    try:
        wait_healthy(args.port, timeout=300)
        # Pass 1: cold prefill + slot save as <model-digest>-<prompt-hash>.bin.
        for s in sessions:
            name = slot_name(model_digest, s["prompt"])
            r = http(args.port, "POST", "/completion",
                     {"prompt": s["prompt"], "n_predict": 1, "cache_prompt": True})
            s["cold"] = r.get("timings", {}).get("prompt_ms")
            if not (KV_DIR / name).exists():
                http(args.port, "POST", f"/slots/0?action=save&filename={name}")
            s["slot"] = name
        # Pass 2: slot restore on prefix match + warm prefill.
        for s in sessions:
            http(args.port, "POST", f"/slots/0?action=restore&filename={s['slot']}")
            r = http(args.port, "POST", "/completion",
                     {"prompt": s["prompt"], "n_predict": 1, "cache_prompt": True})
            warm = r.get("timings", {}).get("prompt_ms")
            cold = s["cold"]
            ok = bool((KV_DIR / s["slot"]).exists() and cold and warm and warm < cold)
            results.append({"session": Path(s["path"]).name, "slot": s["slot"],
                            "cold_prompt_ms": cold, "warm_prompt_ms": warm,
                            "speedup": (round(cold / warm, 2) if cold and warm else None),
                            "pass": ok})
            print(f"  {results[-1]['session']}: cold={cold}ms warm={warm}ms "
                  f"speedup={results[-1]['speedup']} pass={ok}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()

    wins = sum(1 for r in results if r["pass"])
    print(f"PILOT RESULT: {wins}/{len(results)} sessions sped up; slots dir: {KV_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
