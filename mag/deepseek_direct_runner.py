"""deepseek_direct_runner - grounded DeepSeek design calls, one per steal (2026-10-17).

Replaces the single-prompt proposal (one call asking for five designs with
file:line citations but carrying NO source) with FIVE calls, one per steal,
each carrying the real repo files for that steal, line-numbered, so every
citation the model returns can be checked against bytes it was actually given.

Safety rails (enforced in code, not doctrine):
  * hard path DENYLIST (.env*, *key*, *secret*, secret_gate_results/, free_keys/,
    steps.jsonl, memory/trajectory/, .git/, *.pem, id_rsa*, credentials*) checked
    BEFORE any file is opened; globs are filtered through the same check.
  * secret-looking strings (sk-, xai-, ghp_/github_pat_, AKIA, AIza, Bearer,
    PEM blocks, long base64 next to key/token/secret) are redacted line-by-line
    before packing (line numbers are preserved).
  * DEEPSEEK_API_KEY is read from os.environ only, used only in the request
    header, never printed, logged or written (not even a prefix).
  * dry-run is the default; nothing touches the network without --live.

Post-check (falsifier): after a live response every `path:line` / `path:a-b`
citation is checked against the packed set (path packed, lines inside the
packed range). Any bad citation -> receipt status FAILED_FALSIFIER.

Outputs: memory/runs/deepseek_direct/<UTC ts>/
  steal_N_prompt.md, steal_N_response.md, steal_N_receipt.json (live only),
  manifest.json, SUMMARY.md. Optional one-file pointer at
  watch/LIBRARY/DEEPSEEK_DIRECT_POINTER.md only if watch/LIBRARY/ exists.
  Never writes into watch/inbox/.

CLI:
  python -m mag.deepseek_direct_runner --steal all              # dry-run (default)
  python -m mag.deepseek_direct_runner --steal 3 --dry-run
  python -m mag.deepseek_direct_runner --live --steal all       # needs DEEPSEEK_API_KEY
  python -m mag.deepseek_direct_runner --live --steal 2 --model deepseek-v4-pro --max-tokens 32000

Pricing source: https://api-docs.deepseek.com/quick_start/pricing (read 2026-10-17).
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "deepseek_direct_runner.v1"
ENDPOINT = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-flash"
DEFAULT_BUDGET_TOKENS = 200_000
DEFAULT_MAX_TOKENS = 16_000
DEFAULT_TIMEOUT_S = 600.0
DEFAULT_RETRIES = 4
CHARS_PER_TOKEN = 4  # rough estimate, stated as such everywhere it is used
MAX_FILE_BYTES = 2_000_000
RUNS_REL = Path("memory") / "runs" / "deepseek_direct"
LIBRARY_REL = Path("watch") / "LIBRARY"
POINTER_NAME = "DEEPSEEK_DIRECT_POINTER.md"
WARM_STATE_REL = Path("memory") / "warm_state.json"

# USD per 1M tokens. Source: api-docs.deepseek.com/quick_start/pricing, read 2026-10-17.
# Peak = 01:00-04:00 and 06:00-10:00 UTC Mon-Fri (Chinese public holidays are
# off-peak but NOT modelled here, so a holiday run is over-estimated, never under).
PRICING: dict[str, dict[str, Any]] = {
    "deepseek-flash": {
        "version": "DeepSeek-V4.1-Flash-1017",
        "peak": {"in_hit": 0.006, "in_miss": 0.30, "out": 1.20},
        "offpeak": {"in_hit": 0.003, "in_miss": 0.15, "out": 0.60},
    },
    "deepseek-v4-pro": {
        "version": "DeepSeek-V4-Pro-0813",
        "peak": {"in_hit": 0.044, "in_miss": 1.32, "out": 3.96},
        "offpeak": {"in_hit": 0.022, "in_miss": 0.66, "out": 1.98},
    },
}
PRICING_SOURCE = "https://api-docs.deepseek.com/quick_start/pricing (read 2026-10-17)"

# --------------------------------------------------------------------------- steals
# Every path below was found on disk by rg/Select-String on 2026-10-17. Globs are
# allowed and pass through the same denylist. `gaps` records what grep did NOT find,
# so the model is told plainly instead of inventing an organ.
STEALS: dict[int, dict[str, Any]] = {
    1: {
        "name": "warm-pack loopback service on 127.0.0.1:8420",
        "goal": ("Serve the warm pack (memory/warm_state.json + context_pack output) from a "
                 "loopback-only HTTP service bound to 127.0.0.1:8420 so seats fetch a warm "
                 "pack instead of rebuilding it per boot."),
        "files": [
            "mag/hermes_warm_boot.py",
            "mag/context_pack.py",
            "mag/rib_boot.py",
            "mag/boot_regen.py",
            "mag/grok_warm_rib.py",
            "scripts/gemini_warm_pack.ps1",
            "mag/cast_server.py",
            "mag/api_server.py",
            "tests/test_ah5_warmboot.py",
            "tests/test_context_pack_delivery.py",
        ],
        "globs": [],
        "gaps": [
            "No listener on port 8420 exists in any .py/.ps1 file (rg '8420' found none).",
            "Existing loopback servers found: mag/cast_server.py (stdlib ThreadingHTTPServer, "
            "127.0.0.1:8766) and mag/api_server.py (uvicorn, 127.0.0.1:8001; :8000 reserved for "
            "backend.server per its comments).",
            "memory/warm_state.json writers found: mag/hermes_warm_boot.py, mag/rib_boot.py, "
            "mag/boot_regen.py, scripts/gemini_warm_pack.ps1 (plus tools/ask_bank_seed.py, "
            "tools/ouroboros.py, tools/reflux_delta_probe.py, not packed).",
        ],
    },
    2: {
        "name": "SQLite WAL claim-lease task queue plus a PID reaper",
        "goal": ("A single SQLite (journal_mode=WAL) task queue with atomic claim + lease expiry, "
                 "and a reaper that frees leases whose holder PID is dead, replacing ad-hoc "
                 "file claims."),
        "files": [
            "mag/bay_organs.py",
            "mag/window_throttle.py",
            "tools/instance_guard.py",
            "mag/job_floor.py",
            "scripts/ack_reaper.py",
            "tools/brief_reaper.py",
            "mag/batch_drain.py",
            "mag/claim_repair.py",
            "tools/ledger_lock.py",
            "tests/test_instance_guard.py",
            "tests/test_ack_reaper.py",
            "tests/test_spec_gate_job_floor.py",
        ],
        "globs": [],
        "gaps": [
            "No SQLite WAL usage exists in mag/, tools/ or scripts/: the only journal_mode pragma "
            "found is 'PRAGMA journal_mode=OFF' in tools/corpus_fts_rebuild.py (not packed).",
            "Existing claim/lease code is FILE-based (claim dirs / claim files with TTL or grace), "
            "e.g. mag/bay_organs.py claim_dir/claim_is_active, mag/window_throttle.py claim, "
            "tools/instance_guard.py claim_process/claim_ask, mag/job_floor.py claim_job.",
        ],
    },
    3: {
        "name": "five-family provider dialect sanitizer (stop repeated HTTP 400s)",
        "goal": ("One sanitizer that rewrites an outgoing chat payload into the dialect each "
                 "provider family accepts (reasoning params, reasoning_content round-trip, "
                 "tool_choice, max_tokens naming, etc.) before send, so known-bad shapes "
                 "never reach the wire and stop producing HTTP 400s."),
        "files": [
            "mag/inference_budget.py",
            "tools/hermes_burn.py",
            "tools/model_garden.py",
            "tools/task_wall.py",
            "tools/free_lane_fleet.py",
            "tools/gstd_fleet_provider.py",
            "tools/provider_error_tally.py",
            "mag/probe_route.py",
            "mag/route_chat.py",
            "mag/lane_breaker.py",
            "tools/gps_mcp/providers.py",
            "tests/test_inference_budget.py",
            "tests/test_provider_error_tally.py",
        ],
        "globs": [],
        "gaps": [
            "mag/inference_budget.py already holds a per-family recipe table with HTTP 400 notes "
            "(its FAMILY_TABLE); the five families are NOT named in the brief: derive them only "
            "from that table or say UNKNOWN.",
            "No module named *sanitiz*/*dialect* exists for provider payloads "
            "(mag/riddler_sanitize.py and scripts/sanitize_dossiers.py exist but are unrelated "
            "and not packed).",
        ],
    },
    4: {
        "name": "gestalt diffusion clustering of the corpus",
        "goal": ("Cluster the corpus by diffusing similarity over a neighbour graph (rather than "
                 "one greedy cosine pass) so whole-gestalt themes emerge, reusing the existing "
                 "embed and cluster organs."),
        "files": [
            "tools/mem_echo.py",
            "tools/gps_mcp/gps_embed.py",
            "tools/concept_span_check.py",
            "tools/oral_law_dedupe.py",
            "tools/corpus_lens.py",
        ],
        "globs": [],
        "gaps": [
            "No gestalt or diffusion clustering exists anywhere in mag/, tools/, scripts/ "
            "(rg 'gestalt|diffusion_cluster|label_propagation|spectral|hdbscan' found nothing "
            "relevant). This is a NEW organ.",
            "Nearest organs: tools/mem_echo.py (ollama embeddings + greedy cosine clustering), "
            "tools/gps_mcp/gps_embed.py (EmbeddingGemma ONNX embedder), "
            "tools/concept_span_check.py cluster(), tools/oral_law_dedupe.py cluster().",
        ],
    },
    5: {
        "name": "verification of backup bundles on Google Drive (rclone gdrive_sd / gdrive_nacho, fleet-archive/)",
        "goal": ("Verify that backup bundles copied to the ~10 TB Google Drive (rclone remotes "
                 "gdrive_sd and gdrive_nacho, under fleet-archive/) are complete and match "
                 "source hashes, with the same COMPLETE/INCOMPLETE discipline as the local "
                 "chain backup."),
        "files": [
            "scripts/backup_chain.py",
            "tests/test_backup_chain_completeness.py",
            "memory/rib/RIB_BOB_PRIMARY_20261017.md",
            "watch/inbox/DISK_INVENTORY_20261008.md",
            "watch/inbox/CHAIN_FIX_BUNDLE_GO_20261016.md",
        ],
        "globs": [],
        "gaps": [
            "No code in mag/, tools/ or scripts/ calls rclone or names gdrive_sd, gdrive_nacho "
            "or fleet-archive; those names appear only in prose (memory/rib/"
            "RIB_BOB_PRIMARY_20261017.md mentions fleet-archive/; DISK_INVENTORY mentions an "
            "rclone backend). The rclone remote config is NOT in the repo and must not be read.",
            "The only verification organ is scripts/backup_chain.py verify() (local "
            "biography_backup folders: sha256 + count/bytes >= 99%, BACKUP_COMPLETE.json).",
        ],
    },
}

# --------------------------------------------------------------------------- denylist
DENY_COMPONENT_GLOBS = (".env*", "*key*", "*secret*", "secret_gate_results", "free_keys",
                        "steps.jsonl", "*.pem", "*.pfx", "*.p12", "id_rsa*", "id_ed25519*",
                        "credentials*", ".netrc", ".git", "rclone.conf")
DENY_PREFIXES = (("memory", "trajectory"),)


def is_denied(rel: str | Path) -> str | None:
    """Return a reason string if this repo-relative path must never be opened, else None."""
    s = str(rel).replace("\\", "/").strip()
    if not s or s.startswith("/") or re.match(r"^[A-Za-z]:", s):
        return "absolute_path"
    parts = [p for p in s.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        return "path_escape"
    for p in parts:
        low = p.lower()
        for g in DENY_COMPONENT_GLOBS:
            if fnmatch.fnmatchcase(low, g):
                return f"denylist:{g}"
    lowparts = tuple(p.lower() for p in parts)
    for pre in DENY_PREFIXES:
        if lowparts[: len(pre)] == pre:
            return "denylist:" + "/".join(pre)
    return None


# --------------------------------------------------------------------------- redaction
_REDACT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("sk", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_\-]{16,}")),
    ("xai", re.compile(r"\bxai-[A-Za-z0-9_\-]{16,}")),
    ("github", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("aws", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("google", re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}")),
    ("slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("bearer", re.compile(r"(?i)(\bbearer\s+)([A-Za-z0-9._\-+/=]{20,})")),
    ("kv", re.compile(r"(?i)((?:api[_\-]?key|apikey|key|token|secret|passw(?:or)?d|auth)"
                      r"[\"']?\s*[:=]\s*[\"']?)([A-Za-z0-9+/_\-=.]{24,})")),
]
_PEM_BEGIN = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
_PEM_END = re.compile(r"-----END [A-Z0-9 ]*PRIVATE KEY-----")
REDACTED = "[REDACTED]"


def _looks_secret(v: str) -> bool:
    """A value next to key/token/secret is redacted only if it looks like key material:
    letters AND digits, and not a snake_case/dotted code identifier."""
    if not (re.search(r"[A-Za-z]", v) and re.search(r"\d", v)):
        return False
    if re.fullmatch(r"[a-z][a-z0-9]*(?:[_.][a-z0-9]+)+", v):
        return False
    return True


def _kv_sub(m: re.Match[str]) -> str:
    return m.group(1) + REDACTED if _looks_secret(m.group(2)) else m.group(0)


def redact_line(line: str, counts: dict[str, int] | None = None) -> str:
    for name, pat in _REDACT_PATTERNS:
        if name == "kv":
            before = line.count(REDACTED)
            line = pat.sub(_kv_sub, line)
            n = line.count(REDACTED) - before  # only count real substitutions
        elif pat.groups >= 2:
            def _sub(m: re.Match[str]) -> str:
                return m.group(1) + REDACTED
            line, n = pat.subn(_sub, line)
        else:
            line, n = pat.subn(REDACTED, line)
        if n and counts is not None:
            counts[name] = counts.get(name, 0) + n
    return line


def redact_lines(lines: list[str]) -> tuple[list[str], dict[str, int]]:
    """Redact secrets line by line; never changes the number of lines."""
    counts: dict[str, int] = {}
    out: list[str] = []
    in_pem = False
    for ln in lines:
        if in_pem or _PEM_BEGIN.search(ln):
            if not in_pem:
                counts["pem"] = counts.get("pem", 0) + 1
            in_pem = not _PEM_END.search(ln)
            out.append(REDACTED)
            continue
        out.append(redact_line(ln, counts))
    return out, counts


def redact_text(text: str) -> str:
    return "\n".join(redact_lines(text.split("\n"))[0])


# --------------------------------------------------------------------------- packing
def est_tokens(text: str) -> int:
    return (len(text) + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN


def split_lines(text: str) -> list[str]:
    """Split like an editor counts lines (\\n only; \\r stripped; no phantom last line)."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [ln[:-1] if ln.endswith("\r") else ln for ln in lines]


@dataclass
class PackedFile:
    path: str
    total_lines: int
    sha256: str
    mtime: float
    lines: list[str]
    redactions: dict[str, int] = field(default_factory=dict)
    keep_lines: int = -1  # -1 = all
    note: str = ""

    @property
    def last_line(self) -> int:
        return self.total_lines if self.keep_lines < 0 else self.keep_lines

    @property
    def truncated(self) -> bool:
        return 0 <= self.keep_lines < self.total_lines

    def render(self) -> str:
        n = self.last_line
        head = (f"<<<FILE {self.path} | lines 1-{n} of {self.total_lines} | "
                f"sha256 {self.sha256[:16]}"
                + (" | TRUNCATED" if self.truncated else "") + ">>>")
        body = "\n".join(f"{i:>5}| {ln}" for i, ln in enumerate(self.lines[:n], 1))
        tail = f"<<<END FILE {self.path}>>>"
        if self.truncated:
            tail = (f"[... lines {n + 1}-{self.total_lines} omitted for the token budget; "
                    f"do not cite them ...]\n" + tail)
        return head + "\n" + body + ("\n" if body else "") + tail + "\n"

    def est_tokens(self) -> int:
        return est_tokens(self.render())


def pack_file(root: Path, rel: str) -> tuple[PackedFile | None, str | None]:
    """Pack one repo-relative file. The denylist is checked BEFORE the file is opened."""
    rel = rel.replace("\\", "/")
    why = is_denied(rel)
    if why:
        return None, why
    p = (root / rel)
    try:
        rp = p.resolve()
        rr = root.resolve()
    except OSError:
        return None, "resolve_failed"
    if rr not in rp.parents:
        return None, "outside_root"
    why = is_denied(rp.relative_to(rr).as_posix())  # re-check after symlink resolution
    if why:
        return None, why
    if not rp.is_file():
        return None, "missing"
    st = rp.stat()
    if st.st_size > MAX_FILE_BYTES:
        return None, "too_large"
    raw = rp.read_bytes()
    if b"\x00" in raw[:8192]:
        return None, "binary"
    text = raw.decode("utf-8", errors="replace")
    lines, counts = redact_lines(split_lines(text))
    return PackedFile(path=rel, total_lines=len(lines), sha256=hashlib.sha256(raw).hexdigest(),
                      mtime=st.st_mtime, lines=lines, redactions=counts), None


def resolve_steal_paths(root: Path, steal: dict[str, Any]) -> tuple[list[str], list[dict[str, str]]]:
    seen: list[str] = []
    skipped: list[dict[str, str]] = []
    for rel in steal.get("files", []):
        rel = rel.replace("\\", "/")
        if rel not in seen:
            seen.append(rel)
    for g in steal.get("globs", []):
        why = is_denied(g)
        if why:
            skipped.append({"path": g, "reason": why})
            continue
        for m in sorted(root.glob(g)):
            if not m.is_file():
                continue
            rel = m.relative_to(root).as_posix()
            why = is_denied(rel)
            if why:
                skipped.append({"path": rel, "reason": why})
            elif rel not in seen:
                seen.append(rel)
    return seen, skipped


def fit_budget(files: list[PackedFile], available_tokens: int) -> list[str]:
    """Truncate the largest (oldest on ties) file until the pack fits. Returns notes."""
    notes: list[str] = []
    while files and sum(f.est_tokens() for f in files) > available_tokens:
        live = [f for f in files if f.last_line > 0]
        if not live:
            break
        victim = max(live, key=lambda f: (f.est_tokens(), -f.mtime))
        over = sum(f.est_tokens() for f in files) - available_tokens
        cur = victim.last_line
        per_line = max(1, victim.est_tokens() // max(cur, 1))
        new = max(0, min(cur - 1, cur - over // per_line - 1))
        if new < 20:
            new = 0
        victim.keep_lines = new
        victim.note = (f"truncated to lines 1-{new} of {victim.total_lines}" if new
                       else f"dropped all {victim.total_lines} lines (header kept)")
    for f in files:
        if f.truncated:
            notes.append(f"{f.path}: {f.note} for the {available_tokens}-token file budget "
                         f"(largest/oldest first)")
    return notes


# --------------------------------------------------------------------------- prompts
SYSTEM_PROMPT = """You are a senior engineer writing a PATCH PLAN for one change to a Python repo.
You are given real files from that repo, each wrapped as
<<<FILE path | lines 1-N of M | sha256 ...>>> ... <<<END FILE path>>>, with every line prefixed
by its 1-based line number. Rules, all mandatory:
1. Cite ONLY files and line numbers that appear in the packed files, in the exact form
   `path:LINE` or `path:START-END`, using the repo-relative path exactly as in the FILE header.
   Never cite a line beyond the packed range of that file (truncated files say so).
2. If something is not visible in the packed files, write UNKNOWN. Never guess a path, a
   function name, a line number, a provider behaviour or a config value.
3. New files you propose are named WITHOUT line numbers (e.g. "new: mag/foo.py").
4. Output a concrete patch plan, not a vision document. Use exactly these sections:
   ## 1. Existing organs (what already exists, with citations)
   ## 2. Patch plan (per file: create/modify, functions/classes with signatures, what changes)
   ## 3. Tests (test file names, test function names, what each asserts)
   ## 4. Falsifier checks (observable commands or assertions that would prove the change wrong)
   ## 5. UNKNOWN (everything you could not ground in the packed files)
5. Keep it under about 1500 words. No marketing language.
"""


def read_anchor(root: Path) -> dict[str, Any]:
    """Report memory/warm_state.json if present. Reported only, never trusted."""
    p = root / WARM_STATE_REL
    out: dict[str, Any] = {"path": WARM_STATE_REL.as_posix(), "present": p.is_file(),
                           "trusted": False}
    if not out["present"]:
        return out
    try:
        d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        ch = d.get("chain") if isinstance(d, dict) else None
        ch = ch if isinstance(ch, dict) else {}
        out.update({
            "schema": d.get("schema") if isinstance(d, dict) else None,
            "generated": d.get("generated") if isinstance(d, dict) else None,
            "verify": d.get("verify") if isinstance(d, dict) else None,
            "index": ch.get("index"),
            "root": ch.get("verkle_root"),
            "chain_ts": ch.get("ts"),
        })
    except Exception as e:  # noqa: BLE001
        out["error"] = type(e).__name__
    return out


def build_user_prompt(n: int, steal: dict[str, Any], files: list[PackedFile],
                      anchor: dict[str, Any], notes: list[str], skipped: list[dict[str, str]]) -> str:
    out = [f"# Steal {n}: {steal['name']}", "", "## Goal", steal["goal"], "",
           "## What grep found missing (stated plainly; do not invent these organs)"]
    out += [f"- {g}" for g in steal.get("gaps", [])] or ["- (none recorded)"]
    out += ["", "## Reported anchor (memory/warm_state.json, UNVERIFIED, do not rely on it)"]
    if anchor.get("present"):
        out.append(f"- index={anchor.get('index')} root={anchor.get('root')} "
                   f"generated={anchor.get('generated')} verify={anchor.get('verify')}")
    else:
        out.append("- not present")
    out += ["", "## Packed files (the ONLY citable sources)"]
    out += [f"- {f.path} (lines 1-{f.last_line} of {f.total_lines}"
            + (", TRUNCATED" if f.truncated else "") + ")" for f in files]
    if skipped:
        out += ["", "## Listed but not packed"]
        out += [f"- {s['path']}: {s['reason']}" for s in skipped]
    if notes:
        out += ["", "## Packing notes"] + [f"- {x}" for x in notes]
    out += ["", "## Files", ""]
    out += [f.render() for f in files]
    out += ["", "Write the patch plan now, following the system rules and the five sections."]
    return "\n".join(out)


# --------------------------------------------------------------------------- cost
def is_peak(now: datetime) -> bool:
    now = now.astimezone(timezone.utc)
    return now.weekday() < 5 and (1 <= now.hour < 4 or 6 <= now.hour < 10)


def cost_usd(model: str, window: str, in_miss: int, in_hit: int = 0, out: int = 0) -> float | None:
    pr = PRICING.get(model)
    if not pr:
        return None
    r = pr[window]
    return round((in_miss * r["in_miss"] + in_hit * r["in_hit"] + out * r["out"]) / 1e6, 6)


def usage_cost(model: str, usage: dict[str, Any], when: datetime) -> dict[str, Any] | None:
    if not usage or model not in PRICING:
        return None
    hit = int(usage.get("prompt_cache_hit_tokens") or 0)
    miss = usage.get("prompt_cache_miss_tokens")
    miss = int(miss) if miss is not None else max(0, int(usage.get("prompt_tokens") or 0) - hit)
    out = int(usage.get("completion_tokens") or 0)
    window = "peak" if is_peak(when) else "offpeak"
    return {"window": window, "usd": cost_usd(model, window, miss, hit, out),
            "in_miss": miss, "in_hit": hit, "out": out, "source": PRICING_SOURCE,
            "note": "Chinese public holidays not modelled (would be off-peak)."}


# --------------------------------------------------------------------------- citations
_EXT = r"(?:py|ps1|psm1|md|json|jsonl|toml|ya?ml|txt|sh|js|mjs|ts|cfg|ini)"
CITE_RE = re.compile(
    r"(?P<path>[A-Za-z0-9_.\-/\\]+\." + _EXT + r")"
    r"(?:(?::L?|#L)(?P<a>\d+)(?:\s*[-\u2013]\s*L?(?P<b>\d+))?)"
)


def check_citations(text: str, packed: dict[str, tuple[int, int]]) -> dict[str, Any]:
    """Every path:line citation must name a packed file and fall inside its packed range."""
    ok: list[str] = []
    bad: list[dict[str, Any]] = []
    basenames: dict[str, list[str]] = {}
    for p in packed:
        basenames.setdefault(p.rsplit("/", 1)[-1], []).append(p)
    for m in CITE_RE.finditer(text):
        raw = m.group(0)
        path = re.sub(r"^(?:\./)+", "", m.group("path").replace("\\", "/"))
        a = int(m.group("a"))
        b = int(m.group("b") or a)
        target = path if path in packed else None
        if target is None:
            cands = [p for p in packed if p.endswith("/" + path)] or (
                basenames.get(path, []) if "/" not in path else [])
            if len(cands) == 1:
                target = cands[0]
        if target is None:
            bad.append({"cite": raw, "reason": "not_packed"})
            continue
        lo, hi = packed[target]
        if b < a:
            a, b = b, a
        if a < lo or b > hi:
            bad.append({"cite": raw, "reason": f"out_of_range (packed {lo}-{hi})"})
        else:
            ok.append(raw)
    return {"citations_ok": len(ok), "citations_bad": len(bad), "bad": bad[:200],
            "unknown_mentions": len(re.findall(r"\bUNKNOWN\b", text))}


# --------------------------------------------------------------------------- http
class LiveCallError(RuntimeError):
    pass


RETRY_STATUS = {408, 409, 425, 429}


def call_deepseek(api_key: str, payload: dict[str, Any], *, timeout: float = DEFAULT_TIMEOUT_S,
                  retries: int = DEFAULT_RETRIES, endpoint: str = ENDPOINT,
                  urlopen: Callable[..., Any] | None = None,
                  sleep: Callable[[float], None] = time.sleep) -> tuple[dict[str, Any], int]:
    """POST one chat completion. Retries 429/5xx/timeouts with backoff. The key is used only
    in the Authorization header and never appears in any return value or exception text."""
    opener = urlopen or urllib.request.urlopen
    body = json.dumps(payload).encode("utf-8")
    last = "unknown"
    for attempt in range(1, retries + 2):
        req = urllib.request.Request(endpoint, data=body, method="POST", headers={
            "Content-Type": "application/json", "Accept": "application/json",
            "Authorization": "Bearer " + api_key})
        delay = None
        try:
            with opener(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                return data, attempt
        except urllib.error.HTTPError as e:
            code = e.code
            try:
                snippet = redact_text(e.read().decode("utf-8", errors="replace"))[:500]
            except Exception:  # noqa: BLE001
                snippet = ""
            last = f"HTTP {code}: {snippet}"
            if not (code in RETRY_STATUS or 500 <= code < 600):
                raise LiveCallError(last) from None
            ra = (e.headers or {}).get("Retry-After") if hasattr(e, "headers") else None
            try:
                delay = min(120.0, float(ra)) if ra else None
            except ValueError:
                delay = None
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = f"{type(e).__name__}: {redact_text(str(getattr(e, 'reason', e)))[:200]}"
        except json.JSONDecodeError:
            last = "invalid JSON response"
        if attempt > retries:
            break
        sleep(delay if delay is not None else min(60.0, 2.0 * 2 ** (attempt - 1)) + random.random())
    raise LiveCallError(f"gave up after {retries + 1} attempts: {last}")


# --------------------------------------------------------------------------- run
def utc_stamp(now: datetime | None = None) -> str:
    return (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")


def parse_steals(arg: str) -> list[int]:
    if arg.strip().lower() == "all":
        return sorted(STEALS)
    out: list[int] = []
    for tok in arg.split(","):
        n = int(tok.strip())
        if n not in STEALS:
            raise ValueError(f"unknown steal {n}; valid: {sorted(STEALS)} or all")
        out.append(n)
    return out


def prepare_steal(root: Path, n: int, model: str, budget: int, max_tokens: int,
                  anchor: dict[str, Any]) -> dict[str, Any]:
    steal = STEALS[n]
    rels, skipped = resolve_steal_paths(root, steal)
    files: list[PackedFile] = []
    for rel in rels:
        pf, why = pack_file(root, rel)
        if pf is None:
            skipped.append({"path": rel, "reason": why or "unknown"})
        else:
            files.append(pf)
    shell = build_user_prompt(n, steal, [], anchor, [], skipped)
    overhead = est_tokens(SYSTEM_PROMPT) + est_tokens(shell) + 600  # 600 = file-list/notes slack
    notes = fit_budget(files, max(0, budget - overhead))
    user = build_user_prompt(n, steal, files, anchor, notes, skipped)
    prompt_tokens = est_tokens(SYSTEM_PROMPT) + est_tokens(user)
    prompt_md = ("<!-- system -->\n" + SYSTEM_PROMPT + "\n<!-- user -->\n" + user)
    return {
        "n": n, "steal": steal, "files": files, "skipped": skipped, "notes": notes,
        "user": user, "prompt_md": prompt_md,
        "prompt_sha256": hashlib.sha256(prompt_md.encode("utf-8")).hexdigest(),
        "prompt_est_tokens": prompt_tokens,
        "packed_ranges": {f.path: (1, f.last_line) for f in files if f.last_line > 0},
        "cost_est": {
            "input_peak_usd": cost_usd(model, "peak", prompt_tokens) if model in PRICING else None,
            "input_offpeak_usd": cost_usd(model, "offpeak", prompt_tokens) if model in PRICING else None,
            "max_output_peak_usd": cost_usd(model, "peak", 0, 0, max_tokens) if model in PRICING else None,
            "basis": f"chars/{CHARS_PER_TOKEN} estimate, all input billed as cache-miss",
        },
    }


def manifest_entry(prep: dict[str, Any]) -> dict[str, Any]:
    return {
        "steal": prep["n"], "name": prep["steal"]["name"],
        "prompt_file": f"steal_{prep['n']}_prompt.md",
        "prompt_sha256": prep["prompt_sha256"], "prompt_est_tokens": prep["prompt_est_tokens"],
        "files": [{"path": f.path, "lines_packed": f.last_line, "total_lines": f.total_lines,
                   "sha256": f.sha256, "est_tokens": f.est_tokens(), "truncated": f.truncated,
                   "redactions": f.redactions} for f in prep["files"]],
        "skipped": prep["skipped"], "notes": prep["notes"], "gaps": prep["steal"].get("gaps", []),
        "cost_est": prep["cost_est"],
    }


def run_live_one(prep: dict[str, Any], api_key: str, model: str, max_tokens: int,
                 timeout: float, retries: int, outdir: Path,
                 urlopen: Callable[..., Any] | None = None) -> dict[str, Any]:
    n = prep["n"]
    started = datetime.now(timezone.utc)
    receipt: dict[str, Any] = {
        "schema": SCHEMA, "steal": n, "name": prep["steal"]["name"], "model": model,
        "endpoint": ENDPOINT, "mode": "live", "started_utc": started.isoformat(),
        "prompt_sha256": prep["prompt_sha256"], "prompt_est_tokens": prep["prompt_est_tokens"],
        "max_tokens": max_tokens,
    }
    payload = {"model": model, "max_tokens": max_tokens, "stream": False, "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prep["user"]}]}
    try:
        data, attempts = call_deepseek(api_key, payload, timeout=timeout, retries=retries,
                                       urlopen=urlopen)
    except LiveCallError as e:
        receipt.update({"status": "ERROR", "error": str(e),
                        "finished_utc": datetime.now(timezone.utc).isoformat()})
        (outdir / f"steal_{n}_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        return receipt
    choice = (data.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    content = msg.get("content") or ""
    reasoning = msg.get("reasoning_content") or ""
    usage = data.get("usage") or {}
    resp_md = (f"# Steal {n} response ({data.get('model', model)})\n\n" + content + "\n")
    (outdir / f"steal_{n}_response.md").write_text(redact_text(resp_md), encoding="utf-8")
    if reasoning:
        (outdir / f"steal_{n}_reasoning.md").write_text(redact_text(reasoning), encoding="utf-8")
    cites = check_citations(content, prep["packed_ranges"])
    if not content.strip():
        status = "EMPTY_CONTENT"
    elif cites["citations_bad"]:
        status = "FAILED_FALSIFIER"
    elif cites["citations_ok"] == 0:
        status = "NO_CITATIONS"
    else:
        status = "OK"
    receipt.update({
        "status": status, "http_attempts": attempts, "response_model": data.get("model"),
        "response_id": data.get("id"), "finish_reason": choice.get("finish_reason"),
        "usage": usage, "cost_estimate": usage_cost(model, usage, started),
        "citation_check": cites, "citations_ok": cites["citations_ok"],
        "citations_bad": cites["citations_bad"],
        "response_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "finished_utc": datetime.now(timezone.utc).isoformat(),
    })
    (outdir / f"steal_{n}_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return receipt


def write_summary(outdir: Path, mode: str, model: str, anchor: dict[str, Any],
                  entries: list[dict[str, Any]], receipts: dict[int, dict[str, Any]]) -> None:
    lines = [f"# DeepSeek direct runner - {outdir.name}", "",
             f"- mode: **{mode}**  model: `{model}`  endpoint: {ENDPOINT}",
             f"- pricing: {PRICING_SOURCE}" if model in PRICING else "- pricing: UNKNOWN for this model",
             f"- anchor (reported, unverified): index={anchor.get('index')} root={anchor.get('root')}",
             "", "| steal | files packed | est. prompt tokens | est. input $ peak / off-peak | status | cites ok/bad |",
             "|---|---|---|---|---|---|"]
    for e in entries:
        r = receipts.get(e["steal"], {})
        ce = e["cost_est"]
        money = ("UNKNOWN" if ce["input_peak_usd"] is None
                 else f"${ce['input_peak_usd']:.4f} / ${ce['input_offpeak_usd']:.4f}")
        status = r.get("status", "DRY_RUN" if mode == "dry-run" else "NOT_RUN")
        cites = f"{r.get('citations_ok', '-')}/{r.get('citations_bad', '-')}"
        lines.append(f"| {e['steal']} {e['name']} | {len(e['files'])} | {e['prompt_est_tokens']:,} "
                     f"| {money} | {status} | {cites} |")
    lines += ["", "Token counts are chars/4 estimates. Live receipts carry real usage when the API returns it."]
    for e in entries:
        lines += ["", f"## Steal {e['steal']}: {e['name']}"]
        lines += [f"- `{f['path']}` lines 1-{f['lines_packed']} of {f['total_lines']}, ~{f['est_tokens']:,} tok"
                  + (" (TRUNCATED)" if f["truncated"] else "")
                  + (f" redactions={f['redactions']}" if f["redactions"] else "") for f in e["files"]]
        lines += [f"- not packed: `{s['path']}` ({s['reason']})" for s in e["skipped"]]
        lines += [f"- gap: {g}" for g in e["gaps"]]
    (outdir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_pointer(root: Path, outdir: Path, mode: str) -> Path | None:
    lib = root / LIBRARY_REL
    if not lib.is_dir():
        return None
    rel = outdir.relative_to(root).as_posix() if root in outdir.parents else str(outdir)
    p = lib / POINTER_NAME
    p.write_text(f"# DeepSeek direct runner - latest run\n\n- {mode}: `{rel}/SUMMARY.md`\n"
                 f"- written {datetime.now(timezone.utc).isoformat()} by mag/deepseek_direct_runner.py\n",
                 encoding="utf-8")
    return p


def run(argv: list[str] | None = None, *, root: Path | None = None,
        urlopen: Callable[..., Any] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="deepseek_direct_runner", description=__doc__.split("\n")[0])
    ap.add_argument("--steal", default="all", help="N, N,M or all (default all)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="pack prompts + manifest only (default)")
    g.add_argument("--live", action="store_true", help="call the API (needs DEEPSEEK_API_KEY)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"default {DEFAULT_MODEL}; or deepseek-v4-pro")
    ap.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    ap.add_argument("--budget-tokens", type=int, default=DEFAULT_BUDGET_TOKENS,
                    help="per-call input budget (chars/4 estimate)")
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_S)
    ap.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    ap.add_argument("--out-root", default=None, help="override output root (tests)")
    ap.add_argument("--no-pointer", action="store_true", help="skip the watch/LIBRARY pointer")
    a = ap.parse_args(argv)
    root = (root or ROOT).resolve()
    try:
        steals = parse_steals(a.steal)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    live = bool(a.live)
    api_key = ""
    if live:
        api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
        if not api_key:
            print("error: DEEPSEEK_API_KEY is not set; live run refused (nothing sent).",
                  file=sys.stderr)
            return 2
    mode = "live" if live else "dry-run"
    out_root = Path(a.out_root).resolve() if a.out_root else root / RUNS_REL
    outdir = out_root / utc_stamp()
    if "watch/inbox" in outdir.as_posix().lower():
        print("error: refusing to write under watch/inbox/", file=sys.stderr)
        return 2
    outdir.mkdir(parents=True, exist_ok=True)
    anchor = read_anchor(root)
    preps = [prepare_steal(root, n, a.model, a.budget_tokens, a.max_tokens, anchor) for n in steals]
    for p in preps:
        (outdir / f"steal_{p['n']}_prompt.md").write_text(p["prompt_md"], encoding="utf-8")
    entries = [manifest_entry(p) for p in preps]
    manifest = {"schema": SCHEMA, "mode": mode, "model": a.model,
                "model_version": PRICING.get(a.model, {}).get("version", "UNKNOWN"),
                "endpoint": ENDPOINT, "created_utc": datetime.now(timezone.utc).isoformat(),
                "budget_tokens": a.budget_tokens, "max_tokens": a.max_tokens,
                "chars_per_token": CHARS_PER_TOKEN, "pricing_source": PRICING_SOURCE,
                "pricing": PRICING.get(a.model), "anchor": anchor, "steals": entries,
                "total_prompt_est_tokens": sum(e["prompt_est_tokens"] for e in entries)}
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    receipts: dict[int, dict[str, Any]] = {}
    if live:
        for p in preps:
            print(f"[live] steal {p['n']}: ~{p['prompt_est_tokens']:,} tok -> {a.model}", flush=True)
            receipts[p["n"]] = run_live_one(p, api_key, a.model, a.max_tokens, a.timeout,
                                            a.retries, outdir, urlopen=urlopen)
            r = receipts[p["n"]]
            print(f"[live] steal {p['n']}: {r['status']} cites ok={r.get('citations_ok', '-')} "
                  f"bad={r.get('citations_bad', '-')}", flush=True)
    write_summary(outdir, mode, a.model, anchor, entries, receipts)
    ptr = None if a.no_pointer else write_pointer(root, outdir, mode)
    for e in entries:
        ce = e["cost_est"]
        money = "cost UNKNOWN" if ce["input_peak_usd"] is None else (
            f"input ~${ce['input_peak_usd']:.4f} peak / ${ce['input_offpeak_usd']:.4f} off-peak")
        print(f"steal {e['steal']}: {len(e['files'])} files, ~{e['prompt_est_tokens']:,} tok, {money}")
    print(f"out: {outdir}")
    if ptr:
        print(f"pointer: {ptr}")
    if not live:
        return 0
    stats = [r.get("status") for r in receipts.values()]
    if any(s == "ERROR" for s in stats):
        return 4
    if any(s == "FAILED_FALSIFIER" for s in stats):
        return 3
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
