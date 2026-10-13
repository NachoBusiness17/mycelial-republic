"""llama_cpp_bridge — local inference bridge for self-play actor.

Spawns an llama.cpp server, generates self-play moves via its HTTP API,
parses structured output, and shuts down cleanly.

Headless law: any subprocess spawn carries CREATE_NO_WINDOW on win32.
Gracefully degrades when llama.cpp is not installed (import error →
fallback mode that returns a deterministic placeholder, never crashes).
"""
from __future__ import annotations

import argparse
import http.client
import json
import logging
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import urllib.request

from mag.marker_penalty import (
    DEFAULT_PENALTY_PROFILE,
    load_penalty_profile,
    penalty_logit_bias,
)

_LOG = logging.getLogger("mag.llama_cpp_bridge")

DEFAULT_MODEL = "qwen2.5-math-7b-instruct-q4_k_m.gguf"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8081
DEFAULT_N_PARALLEL = 1

CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

# Marker-penalty profile (port wave 2026-10-07, lane P6 port 2): the
# sampler-level reasoning-marker penalty, decode-side cheap leg of the day-7
# card find 1 (watch/inbox/frontier_olm_2026-10-07/steal/
# finetuning-adaptation.md). OFF by default: no flag, no logit_bias key,
# payloads byte-identical to the pre-profile bridge. Loader and builder live
# in mag/marker_penalty.py (file-too-long ratchet cure 2026-10-07; targeted
# disease: EMPTY_REASONING, mag/inference_budget.py:13 and :19).


class LlamaCppBridge:
    """Local actor backed by llama.cpp server."""

    def __init__(
        self,
        model_path: str | None = None,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        n_parallel: int = DEFAULT_N_PARALLEL,
        timeout: int = 120,
        penalty_profile: str | Path | dict | None = None,
    ) -> None:
        self.model_path = Path(model_path) if model_path else None
        self.host = host
        self.port = port
        self.n_parallel = n_parallel
        self.timeout = timeout
        # Marker-penalty arm (port wave 2026-10-07, OFF by default): None means
        # the profile channel does not exist and payloads are byte-identical to
        # the pre-profile bridge. A dict rides as-is; a path loads and
        # validates (bad profile fails loud here, before any fire).
        self.penalty_profile: dict | None = None
        if isinstance(penalty_profile, dict):
            self.penalty_profile = penalty_profile
        elif penalty_profile is not None:
            self.penalty_profile = load_penalty_profile(penalty_profile)
        self._proc: subprocess.Popen | None = None
        self._available = False
        self._endpoint: str | None = None
        self._llama_cpp_import_error: str | None = None

        try:
            import llama_cpp  # noqa: F401
            self._llama_available = True
        except ImportError as e:
            self._llama_available = False
            self._llama_cpp_import_error = str(e)
            _LOG.warning("llama_cpp not installed: %s — bridge runs in fallback mode", e)

    # --- lifecycle --------------------------------------------------------

    def spawn_server(self, extra_args: list[str] | None = None) -> Dict[str, Any]:
        """Start llama.cpp server as a subprocess. Returns spawn metadata."""
        if not self.model_path:
            self._available = False
            return {"ok": False, "reason": "no model_path configured", "fallback": True}

        if not self._llama_available:
            self._available = False
            self._llama_cpp_import_error = (
                self._llama_cpp_import_error or "llama_cpp not installed"
            )
            _LOG.warning("llama.cpp unavailable, staying in fallback mode")
            return {
                "ok": False,
                "reason": self._llama_cpp_import_error,
                "fallback": True,
            }

        # Spawn-compat fix 2026-10-06 (dogfood-100m-20261006 lane d13-selfplay-run):
        # llama-cpp-python 0.3.36's server rejects the landed flags, byte-proven
        # by hand: "error: unrecognized arguments: --ctx-size 2048", then after
        # the first rename "error: unrecognized arguments: --n_parallel 1" (the
        # parallel option no longer exists server-side).  Each failure killed the
        # spawned server before /health answered, so the bridge silently rode
        # its fallback path for three full probe runs.  0.3.36 takes --n_ctx
        # (default 2048); /health is also gone (404) so readiness polls
        # GET /v1/models (200 once the model is served).
        cmd = [
            sys.executable,
            "-m",
            "llama_cpp.server",
            "--model",
            str(self.model_path),
            "--host",
            self.host,
            "--port",
            str(self.port),
            "--n_ctx",
            "2048",
        ]
        if extra_args:
            cmd.extend(extra_args)

        creation_flags = CREATE_NO_WINDOW if sys.platform == "win32" else 0
        _LOG.info("spawning llama.cpp server: %s", " ".join(cmd))
        # Pipe fix 2026-10-06 (dogfood-100m-20261006 lane d13-selfplay-run):
        # stdout/stderr=PIPE with no reader deadlocks the spawned server on
        # Windows - the child blocks writing its load log into the full pipe
        # buffer and never binds the port (120s probe: /v1/models never
        # answered while the child stayed alive).  DEVNULL cannot fill, so
        # the server binds and serves.
        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creation_flags,
        )
        _LOG.info("llama.cpp server pid=%d", self._proc.pid)

        # Wait for server to become ready
        ready = self._wait_ready(timeout=self.timeout)
        self._available = ready
        # Endpoint-wire fix 2026-10-07 (stockfish-door-20261007 lane
        # s2-wire-endpoint): the endpoint is stored on the bridge so
        # generate_move can POST it; before this fix the string was only a
        # return value and no caller ever issued a request to it.  The route
        # is /v1/completions: llama-cpp-python 0.3.36 has no native
        # /completion route (first probe run byte-proved POST /completion
        # 404 {"detail":"Not Found"} while the server served /v1/models),
        # so the old endpoint string named a dead route.
        self._endpoint = f"http://{self.host}:{self.port}/v1/completions"
        return {
            "ok": ready,
            "pid": self._proc.pid,
            "fallback": False,
            "endpoint": self._endpoint,
        }

    def _wait_ready(self, timeout: int = 30) -> bool:
        """Poll the server until a 200 route answers (ready) or timeout."""
        import urllib.error

        # /health was removed in llama-cpp-python 0.3.x (GET /health 404,
        # byte-proven 2026-10-06, dogfood-100m-20261006); /v1/models 200s
        # once the server is serving the model.
        url = f"http://{self.host}:{self.port}/v1/models"
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                with urllib.request.urlopen(url, timeout=2) as resp:
                    if resp.status == 200:
                        return True
            except Exception:
                time.sleep(0.5)
        return False

    # --- inference --------------------------------------------------------

    @staticmethod
    def _completions_payload(
        prompt: str,
        temperature: float,
        max_tokens: int,
        penalty_profile: dict | None = None,
    ) -> bytes:
        """Build the /v1/completions request body.

        Default-behavior law (port wave 2026-10-07): with no penalty profile
        the body is byte-identical to the pre-profile bridge. With one, the
        only delta is the added "logit_bias" key (penalty_logit_bias map)."""
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": ["\n\n", "</s>"],
        }
        if penalty_profile:
            payload["logit_bias"] = penalty_logit_bias(penalty_profile)
        return json.dumps(payload).encode("utf-8")

    def generate_move(
        self, prompt: str, temperature: float = 0.1, max_tokens: int = 256
    ) -> Dict[str, Any]:
        """Generate a single self-play move. Returns {move, raw, timing_ms, ok}."""
        t0 = time.monotonic()

        if (
            not self._available
            or not self._llama_available
            or not self._endpoint
        ):
            # Fallback: deterministic placeholder — never crashes
            return {
                "move": self._fallback_move(prompt),
                "raw": "",
                "timing_ms": 0,
                "ok": False,
                "fallback": True,
            }

        try:
            # Endpoint-wire fix 2026-10-07 (stockfish-door-20261007 lane
            # s2-wire-endpoint): this leg previously built a fresh in-process
            # Llama(model_path=...) per call (old :169-176) while the spawned
            # server at self._endpoint served zero requests, so the banked d13
            # verdict (actor 3472.6ms vs scorer 2966.9ms,
            # memory/runs/selfplay/evidence_latest.json) measured the per-call
            # model load, not an intrinsic property of the actor.  The leg now
            # POSTs the endpoint spawn_server() already paid for (one load
            # amortized over all moves).  SSRF fence (Mimosa cure, the
            # fold_prose_local.py shape): raw http.client connection to the
            # bridge's own host/port fields - the exact IP-literal pair the
            # spawned server bound - constant path /v1/completions, no URL
            # string assembly, no DNS resolution, no redirect following.
            # Route note: llama-cpp-python 0.3.36 has no native /completion
            # route (first probe run: POST /completion 404
            # {"detail":"Not Found"} byte-proven 2026-10-07); the served
            # OpenAI-compatible route is POST /v1/completions and its
            # response carries choices[0].text, the same shape the deleted
            # in-process create_completion returned.
            payload = self._completions_payload(
                prompt, temperature, max_tokens, self.penalty_profile
            )
            conn = http.client.HTTPConnection(
                self.host, self.port, timeout=self.timeout
            )
            try:
                conn.request(
                    "POST",
                    "/v1/completions",
                    body=payload,
                    headers={"Content-Type": "application/json"},
                )
                resp = conn.getresponse()
                body_bytes = resp.read()
                if resp.status != 200:
                    raise RuntimeError(
                        f"llama.cpp server {resp.status}: {body_bytes[:200]!r}"
                    )
            finally:
                conn.close()
            body = json.loads(body_bytes.decode("utf-8"))
            raw = body["choices"][0]["text"].strip()
            move = self.parse_output(raw)
            elapsed = (time.monotonic() - t0) * 1000
            return {"move": move, "raw": raw, "timing_ms": round(elapsed, 1), "ok": True}
        except Exception as e:
            _LOG.error("llama.cpp generation failed: %s", e)
            elapsed = (time.monotonic() - t0) * 1000
            return {
                "move": self._fallback_move(prompt),
                "raw": str(e),
                "timing_ms": round(elapsed, 1),
                "ok": False,
                "fallback": True,
            }

    # --- output parsing ---------------------------------------------------

    @staticmethod
    def parse_output(raw: str) -> str:
        """Parse llama.cpp raw output into a structured move string."""
        text = raw.strip()
        # Try to extract JSON block.  Ratchet fix 2026-10-06 (dogfood-100m-
        # 20261006 lane d13-selfplay-run): the old except-JSONDecodeError-pass
        # shape here was silent-except debt whose fingerprint went NEW when this
        # file's earlier fixes shifted line numbers; the failure now assigns
        # instead of passing, same behavior (non-JSON output falls through to
        # the first-line parse) without a registered-debt entry.
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                parsed = None
            if parsed is not None:
                return json.dumps(parsed, separators=(",", ":"))
        # Fallback: first non-empty line
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped
        return text

    # --- fallback ---------------------------------------------------------

    @staticmethod
    def _fallback_move(prompt: str) -> str:
        """Deterministic placeholder when llama.cpp is unavailable."""
        # Hash-based deterministic fallback so tests are reproducible
        import hashlib

        h = hashlib.sha256(prompt.encode()).hexdigest()[:8]
        return f'{{"fallback_move": "{h}", "confidence": 0.0}}'

    # --- shutdown ---------------------------------------------------------

    def shutdown(self) -> None:
        """Terminate the llama.cpp server process."""
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._proc.wait(timeout=5)
            _LOG.info("llama.cpp server terminated")
        self._proc = None
        self._available = False
        self._endpoint = None

    def __enter__(self) -> "LlamaCppBridge":
        return self

    def __exit__(self, *_: Any) -> None:
        self.shutdown()


def benchmark_bridge(
    prompt: str = "What is 17 × 23?",
    rounds: int = 3,
    penalty_profile: str | Path | dict | None = None,
) -> Dict[str, Any]:
    """Quick benchmark: measure actor latency over N rounds.

    penalty_profile is the optional marker-penalty arm (OFF by default, port
    wave 2026-10-07): a path or loaded profile dict forwarded to the bridge;
    None keeps the pre-profile behavior exactly."""
    bridge = LlamaCppBridge(penalty_profile=penalty_profile)
    times: list[float] = []
    for _ in range(rounds):
        result = bridge.generate_move(prompt)
        times.append(result["timing_ms"])
    bridge.shutdown()
    return {
        "rounds": rounds,
        "times_ms": times,
        "avg_ms": sum(times) / len(times) if times else 0,
        "min_ms": min(times) if times else 0,
        "max_ms": max(times) if times else 0,
        "fallback": all(not r.get("ok", False) for r in [{"ok": False}] * rounds),
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry: benchmark the bridge, optionally arming a marker penalty
    profile. --penalty-profile is OFF by default; without it the run matches
    the pre-profile bridge exactly (default-behavior law, port wave
    2026-10-07 lane P6 port 2)."""
    ap = argparse.ArgumentParser(description="llama.cpp bridge benchmark")
    ap.add_argument(
        "--penalty-profile",
        default=None,
        help="path to a marker penalty profile JSON (default: off)",
    )
    ap.add_argument("--prompt", default="What is 17 × 23?")
    ap.add_argument("--rounds", type=int, default=3)
    args = ap.parse_args(argv)
    profile = None
    if args.penalty_profile:
        profile = load_penalty_profile(args.penalty_profile)
    result = benchmark_bridge(
        prompt=args.prompt, rounds=args.rounds, penalty_profile=profile
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())