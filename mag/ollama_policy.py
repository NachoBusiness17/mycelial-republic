"""Ollama load policy — one-hot GPU on 6GB AMD (RX 5600 XT).

Keeps janitor (gemma:2b) + one active role model; evicts others from VRAM.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any

from config import ROOT, ollama_base

JANITOR = os.environ.get("MAG_JANITOR_MODEL", "gemma:2b")
DESK_DEFAULT = os.environ.get("MAG_DESK_MODEL", "gemma4-desk")
KEEP_ALIVE = os.environ.get("MAG_OLLAMA_KEEP", "gemma:2b,gemma4-desk,qwen-desk")

# Digest pins: the migration path from tag strings to pinned identity. A tag is a mutable
# registry pointer (2026-10-07, verified against the live Ollama registry: qwen3:4b and
# qwen3:4b-thinking served byte-identical manifests, sha256 359d7dd4..., so the plain tag
# silently re-pointed at the thinking-only artifact and every recorded thinking condition
# went stale with zero errors); the layer digest GET /api/tags reports is the identity that
# cannot move unnoticed. Expected digests ride MAG_PIN_DIGESTS as "tag=hex,tag=hex" (the
# hex may carry a "sha256:" prefix); verify_pins() compares at boot-verify or via
# `python -m mag.ollama_policy --verify` and REFUSES the rung on mismatch. A pin with no
# digest is listed warn-once as unpinned (the migration path), never refused.
# Receipt: watch/inbox/frontier_olm_2026-10-07/steal/open-local-language-models via reddit.md
_UNPINNED_WARNED: set[frozenset[str]] = set()


def _base() -> str:
    return ollama_base().rstrip("/")


def keep_alive_models() -> list[str]:
    """KEEP_ALIVE tag list, split and stripped."""
    return [t.strip() for t in KEEP_ALIVE.split(",") if t.strip()]


def pinned_model_names() -> list[str]:
    """Every pinned tag: janitor, desk default, and the KEEP_ALIVE members."""
    pins = [JANITOR.strip(), DESK_DEFAULT.strip(), *keep_alive_models()]
    seen: list[str] = []
    for p in pins:
        if p and p not in seen:
            seen.append(p)
    return seen


def pin_digests() -> dict[str, str]:
    """Expected digests from MAG_PIN_DIGESTS ("tag=hex,tag=hex"), read at call time."""
    raw = os.environ.get("MAG_PIN_DIGESTS", "")
    out: dict[str, str] = {}
    for part in raw.split(","):
        part = part.strip()
        if not part or "=" not in part:
            continue
        tag, _, digest = part.partition("=")
        tag = tag.strip()
        digest = digest.strip()
        if tag and digest:
            out[tag] = digest
    return out


def _digest_hex(digest: str) -> str:
    """Normalize a digest to bare lowercase hex (strip an optional sha256: prefix)."""
    d = (digest or "").strip().lower()
    return d[len("sha256:"):] if d.startswith("sha256:") else d


# Cloud-suffix REFUSE (2026-10-12): Ollama 0.12+ serves "-cloud" models (e.g.
# gpt-oss:120b-cloud) through the same localhost:11434 door; the daemon detects the
# suffix, attaches the account credentials, and proxies the request to its datacenter,
# so a local address is not locality. Cause+evidence:
# watch/inbox/frontier_olm_adhoc/steal/open-local-language-models.md (returnededitor
# find 3; the flag that asked for this port rode watch/inbox/frontier_olm_2026-10-10)
# and the raw capture watch/inbox/frontier_olm_adhoc/sweep/raw/art_return_ollama.html
# ("A model with a -cloud suffix behaves like any other model: you can list it, run
# it, point your existing tools at it"). verify_pins() refuses any pinned or installed
# tag carrying the suffix outright; no digest pin is required to trip it.
CLOUD_SUFFIX = "-cloud"


def _is_cloud_tag(tag: str) -> bool:
    """True when a model name carries Ollama's cloud suffix (locality is broken)."""
    return tag.strip().lower().endswith(CLOUD_SUFFIX)


def _request_json(method: str, path: str, body: dict[str, Any] | None = None,
                  timeout: float = 3.0) -> tuple[int, Any]:
    """One daemon call. Returns (status, parsed body); status 0 on transport failure."""
    url = f"{_base()}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(getattr(resp, "status", 0) or 200), json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            return int(exc.code), json.loads(exc.read().decode("utf-8"))
        except Exception:
            return int(exc.code), {}
    except Exception as exc:
        return 0, {"ok": False, "error": str(exc)[:200]}


def list_tags(timeout: float = 3.0) -> dict[str, str]:
    """GET /api/tags -> {installed tag: digest hex}. Empty on daemon failure."""
    status, body = _request_json("GET", "/api/tags", timeout=timeout)
    if status != 200 or not isinstance(body, dict):
        return {}
    out: dict[str, str] = {}
    for m in body.get("models") or []:
        if isinstance(m, dict) and m.get("name"):
            out[str(m["name"])] = _digest_hex(str(m.get("digest") or ""))
    return out


def _lookup_digest(installed: dict[str, str], tag: str) -> str | None:
    """Exact tag match first, then base-name match (a pin may be installed as tag:latest)."""
    if tag in installed:
        return installed[tag]
    base = tag.split(":")[0]
    for name, digest in installed.items():
        if name.split(":")[0] == base:
            return digest
    return None


def _warn_unpinned_once(unpinned: list[str]) -> None:
    """Warn once per process (per unique unpinned set) on stderr."""
    key = frozenset(unpinned)
    if key in _UNPINNED_WARNED:
        return
    _UNPINNED_WARNED.add(key)
    print(
        "[ollama_policy] unpinned tags (no digest in MAG_PIN_DIGESTS): "
        + ", ".join(sorted(unpinned)),
        file=sys.stderr,
    )


def verify_pins(timeout: float = 3.0) -> dict[str, Any]:
    """Tag-digest gate: compare pinned digests against GET /api/tags.

    REFUSES (ok False) any digest-pinned tag whose installed digest differs, printing the
    mismatch (tag, expected, actual); a digest-pinned tag missing from the daemon is also a
    refusal (identity unprovable). Independently of digests, any pinned OR installed tag
    carrying the Ollama cloud suffix ("-cloud") is a refusal (reason "cloud_suffix"): that
    tag proxies through the same localhost door to the vendor's datacenter, so a local
    address is not locality. Daemon-down fail-closes only when digest pins exist (a pinned
    identity must be provable); cloud-suffix refusals over pinned names fire even with the
    daemon down (the config alone is the drift); with no digest pins and no cloud tags the
    gate is the warn-once unpinned listing, the migration path.
    """
    pins = pinned_model_names()
    digests = pin_digests()
    status, body = _request_json("GET", "/api/tags", timeout=timeout)
    daemon_ok = status == 200 and isinstance(body, dict)
    installed: dict[str, str] = {}
    if daemon_ok:
        for m in body.get("models") or []:
            if isinstance(m, dict) and m.get("name"):
                installed[str(m["name"])] = _digest_hex(str(m.get("digest") or ""))
    refused: list[dict[str, Any]] = []
    matched: list[dict[str, str]] = []
    for tag, expected in sorted(digests.items()):
        actual = _lookup_digest(installed, tag)
        if actual is None:
            refused.append({"tag": tag, "expected": expected, "actual": None,
                            "reason": "not_installed"})
            continue
        if actual != _digest_hex(expected):
            refused.append({"tag": tag, "expected": expected, "actual": actual,
                            "reason": "digest_mismatch"})
            continue
        matched.append({"tag": tag, "digest": actual})
    # Cloud-suffix scan over BOTH surfaces the drift can enter through: the estate's own
    # pin config and the daemon's installed inventory. One -cloud tag anywhere refuses
    # the rung (see the CLOUD_SUFFIX comment block above for cause+evidence).
    for tag in sorted({*pins, *installed}):
        if _is_cloud_tag(tag):
            refused.append({"tag": tag, "expected": None, "actual": None,
                            "reason": "cloud_suffix"})
    unpinned = [t for t in pins if t not in digests]
    ok = not refused
    if digests and not daemon_ok:
        ok = False
    if unpinned:
        _warn_unpinned_once(unpinned)
    return {
        "ok": ok,
        "daemon_ok": daemon_ok,
        "daemon_status": status,
        "pins": pins,
        "matched": matched,
        "refused": refused,
        "unpinned": unpinned,
    }


def thinking_condition(model: str, timeout: float = 3.0) -> dict[str, Any]:
    """POST /api/show for one model, normalized to the thinking default.

    Three daemon response shapes, all measured on this estate's 0.34.3 daemon
    (watch/inbox/frontier_olm_2026-10-07/sweep/show_resp_*.json):
      structured     {"thinking": {"values": [...], "default": X}}  (gemma4)
      capability     capabilities lists "thinking", no values/default block (deepseek-r1:1.5b)
      absent         no thinking key anywhere (qwen2.5:7b)
    The absent key is the one-bug law's MEASURED ON state (memory/rib/RIB_MODEL_GATES_
    20261001.md:120): any shape without a structured default assumes ON, never OFF. A
    structured default maps True/False to on/off and passes string levels (low/high/max
    class) through verbatim.
    """
    name = (model or "").strip()
    if not name:
        return {"ok": False, "model": name, "shape": "unreachable", "thinking": "on",
                "assumed": True, "error": "empty model"}
    status, body = _request_json("POST", "/api/show", {"model": name}, timeout=timeout)
    if status == 0 or not isinstance(body, dict):
        err = str(body.get("error") or "daemon unreachable")[:200] if isinstance(body, dict) \
            else "daemon unreachable"
        return {"ok": False, "model": name, "shape": "unreachable", "thinking": "on",
                "assumed": True, "error": err}
    if status != 200:
        return {"ok": False, "model": name, "shape": "error", "thinking": "on",
                "assumed": True, "error": f"HTTP {status}"}
    block = body.get("thinking")
    capabilities = [c for c in (body.get("capabilities") or []) if isinstance(c, str)]
    if isinstance(block, dict) and "default" in block:
        default = block.get("default")
        if isinstance(default, bool):
            level = "on" if default else "off"
            assumed = False
        elif isinstance(default, str) and default.strip():
            level = default.strip()
            assumed = False
        else:
            level, assumed = "on", True  # unparseable default: assume ON, never OFF
        return {"ok": True, "model": name, "shape": "structured", "default": default,
                "values": block.get("values"), "thinking": level, "assumed": assumed}
    # No structured default: capability shape (advertised without values/default) or the
    # absent key. Both assume ON per the one-bug law.
    shape = "capability_only" if "thinking" in capabilities else "absent"
    return {"ok": True, "model": name, "shape": shape, "default": None,
            "thinking": "on", "assumed": True}


def thinking_conditions(timeout: float = 3.0) -> dict[str, Any]:
    """The condition ledger read: /api/show per pinned model."""
    rows = [thinking_condition(t, timeout=timeout) for t in pinned_model_names()]
    return {"ok": all(r.get("ok") for r in rows), "conditions": rows, "n": len(rows)}


def list_loaded() -> list[dict[str, Any]]:
    try:
        with urllib.request.urlopen(f"{_base()}/api/ps", timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return [m for m in (data.get("models") or []) if isinstance(m, dict)]
    except Exception:
        return []


def _ollama_stop(model: str) -> dict[str, Any]:
    name = (model or "").strip()
    if not name:
        return {"ok": False, "error": "empty model"}
    try:
        proc = subprocess.run(
            ["ollama", "stop", name],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ROOT),
        )
        return {
            "ok": proc.returncode == 0,
            "model": name,
            "stdout": (proc.stdout or "").strip()[:200],
            "stderr": (proc.stderr or "").strip()[:200],
        }
    except Exception as exc:
        return {"ok": False, "model": name, "error": str(exc)[:200]}


def enforce_one_hot(*, keep: str | None = None, also_keep_janitor: bool = True) -> dict[str, Any]:
    """Unload all loaded models except keep (+ janitor if also_keep_janitor)."""
    if os.environ.get("MAG_OLLAMA_ONE_HOT", "1").strip().lower() in ("0", "false", "no", "off"):
        return {"ok": True, "skipped": True, "reason": "MAG_OLLAMA_ONE_HOT off"}

    primary = (keep or DESK_DEFAULT).strip()
    allowed = {primary.split(":")[0], primary}
    if also_keep_janitor:
        allowed.add(JANITOR)
        allowed.add(JANITOR.split(":")[0])

    loaded = list_loaded()
    stopped: list[dict[str, Any]] = []
    kept: list[str] = []

    for m in loaded:
        name = str(m.get("name") or "")
        base = name.split(":")[0]
        if name in allowed or base in allowed:
            kept.append(name)
            continue
        stopped.append(_ollama_stop(name))

    return {
        "ok": True,
        "keep": primary,
        "janitor": JANITOR if also_keep_janitor else None,
        "kept": kept,
        "stopped": stopped,
        "n_loaded_before": len(loaded),
        "n_stopped": sum(1 for s in stopped if s.get("ok")),
    }


def ensure_desk_model(model: str | None = None) -> dict[str, Any]:
    """One-hot for desk turn — evict hermes/full gemma4, keep desk + janitor."""
    target = (model or DESK_DEFAULT).strip()
    out = enforce_one_hot(keep=target, also_keep_janitor=True)
    out["desk_model"] = target
    return out


def status() -> dict[str, Any]:
    loaded = list_loaded()
    rows = []
    for m in loaded:
        size = float(m.get("size") or 0)
        vram = float(m.get("size_vram") or 0)
        rows.append(
            {
                "name": m.get("name"),
                "size_gb": round(size / 1e9, 2) if size else None,
                "vram_gb": round(vram / 1e9, 2) if vram else None,
                "gpu_pct": round(100 * vram / size, 1) if size and vram else None,
                "context_length": m.get("context_length"),
            }
        )
    return {
        "ok": True,
        "janitor": JANITOR,
        "desk_default": DESK_DEFAULT,
        "one_hot": os.environ.get("MAG_OLLAMA_ONE_HOT", "1") not in ("0", "false", "no", "off"),
        "loaded": rows,
        "n_loaded": len(rows),
    }


def main(argv: list[str] | None = None) -> int:
    """--verify: the tag-digest gate, exit 1 on refusal. --thinking: the condition ledger."""
    args = list(sys.argv[1:] if argv is None else argv)
    if "--verify" in args:
        out = verify_pins()
        print(json.dumps(out, indent=2, default=str))
        if out.get("refused"):
            for r in out["refused"]:
                print(f"REFUSED {r['tag']}: expected {r['expected']} actual {r['actual']}"
                      f" ({r['reason']})", file=sys.stderr)
        return 0 if out.get("ok") else 1
    if "--thinking" in args:
        print(json.dumps(thinking_conditions(), indent=2, default=str))
        return 0
    print("usage: python -m mag.ollama_policy --verify | --thinking")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
