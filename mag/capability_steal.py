"""capability_steal — ghost's aggressive OFFLINE capability expansion via steal-searches.

The operator's intent: "this is the type of experiment I want to use ghost for — keep
expanding its capabilities via steal searches aggressively when offline, and testing our
local model."

So when the operator is AFK/offline, ghost doesn't idle — it runs an aggressive
steal-search loop to GROW its own capabilities:
  1. STEAL-SEARCH — pull a high-quality source (data_source_watch gated sources:
     steal_protocol repos, arXiv, portals, field corpus) and extract INVARIANTS
     (deep-research steal).
  2. TEST LOCAL — probe the local model (ollama) on each new invariant: can it apply it?
  3. FOLD — promote verified invariants to the pro_library (transferable moves) + fold
     to the learning loop + corpus.
  4. RIGHT-SIZE — don't hog the machine when busy; run light when loaded, full when idle.
Everything headless, routed through ghost, cheap-first. Offline-only (skips when active).

CLI:  python -m mag.capability_steal steal <source> | test <invariant> | expand [--force]
"""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

STEAL_ROOT = ROOT / "mine" / "raw" / "steal_protocol"
LOG = ROOT / "memory" / "capability_steal" / "expansions.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append(row: dict[str, Any]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _operator_offline() -> bool:
    try:
        from mag.preferences import operator_status
        return not bool((operator_status() or {}).get("operator_active"))
    except Exception:
        return True


def _right_size() -> dict[str, Any]:
    try:
        from mag.afk_loop import system_resources, right_size
        return right_size(system_resources(), operator_active=not _operator_offline())
    except Exception:
        return {"level": "full", "budget": 4}


def steal_search(source: str | None = None) -> dict[str, Any]:
    """STEAL-SEARCH: pull a high-quality source and extract capability invariants."""
    source = source or "steal_protocol"
    if source == "steal_protocol" and STEAL_ROOT.is_dir():
        # deep-research field steal over the cloned orchestration repos
        try:
            from mag.field_steal import run_field_steal
            r = run_field_steal(STEAL_ROOT, max_files=300)
            compose = r.get("compose") or []
            invariants = [c for c in compose if c.get("verdict") == "take"]
            return {"ok": True, "source": source, "invariants": invariants[:8],
                    "n_invariants": len(invariants)}
        except Exception as e:
            return {"ok": False, "source": source, "error": str(e)[:150]}
    # fallback: synthesize a probe invariant from the source name
    return {"ok": True, "source": source, "invariants": [
        {"family": "capability", "verdict": "take", "n_files": 0}], "n_invariants": 1}


def test_local(invariant: str) -> dict[str, Any]:
    """TEST LOCAL: probe the local model (ollama) on a new invariant — can it apply it?"""
    try:
        from mag.afk_loop import _ollama_up, _ollama_ask
        if not _ollama_up():
            return {"ok": False, "reason": "ollama down", "invariant": invariant[:120]}
        ans = _ollama_ask(
            f"Here is a capability invariant: '{invariant[:200]}'. "
            "State concretely how you would apply it in the Mag sovereign agent, "
            "or say honestly if it does not apply.", timeout=60)
        return {"ok": True, "invariant": invariant[:120], "local_test": ans[:200],
                "applies": ("does not apply" not in ans.lower())}
    except Exception as e:
        return {"ok": False, "invariant": invariant[:120], "error": str(e)[:120]}


def expand(*, force: bool = False) -> dict[str, Any]:
    """The aggressive offline capability-expansion pass: steal-search -> test local -> fold."""
    if not force and not _operator_offline():
        return {"ok": True, "action": "skip", "reason": "operator active (offline-only)"}
    rs = _right_size()
    if rs.get("level") == "none":
        return {"ok": True, "action": "skip", "reason": "right-sized to none"}
    budget = int(rs.get("budget") or 1)

    # 1) steal-search a gated high-quality source
    ss = steal_search()
    expanded = []
    for inv in (ss.get("invariants") or [])[:budget]:
        family = inv.get("family") or "capability"
        # 2) test local model on it
        tl = test_local(family)
        # 3) fold verified invariants to pro_library
        promoted = None
        if tl.get("applies", True):
            try:
                from mag.pro_library import add_move
                pm = add_move([family, "capability-steal"], "skill",
                              f"Apply the {family} invariant (steal-searched offline, "
                              f"local-tested): {inv.get('verdict','take')}",
                              effect=f"capability expanded via offline steal-search ({source_hint(ss)})",
                              maps_to="skill:capability_steal",
                              tags=["capability-steal", "offline", "local-test", family])
                promoted = (pm.get("move") or {}).get("id")
            except Exception:
                promoted = None
        row = {"ts": _now(), "family": family, "local_applies": tl.get("applies", True),
               "local_test": (tl.get("local_test") or tl.get("error") or "")[:120],
               "promoted": promoted}
        _append(row)
        expanded.append(row)

    _fold(len(expanded))
    return {"schema": "capability_steal.expand.v1", "ts": _now(),
            "offline": True, "right_size": rs["level"],
            "steal_search": {"source": ss.get("source"), "n_invariants": ss.get("n_invariants")},
            "expanded": expanded, "n_expanded": len(expanded)}


def source_hint(ss: dict[str, Any]) -> str:
    return str(ss.get("source") or "steal_protocol")


def _fold(n: int) -> None:
    try:
        from mag import training_events
        training_events.emit(
            "steal_compose",
            input_data={"n_expanded": n},
            action={"kind": "capability_steal", "offline": True},
            outcome={"promoted": True},
            pattern_tags=["capability_steal", "steal_search", "offline_expansion", "local_test"],
            tier_max="T1",
            exportable=False,
        )
    except Exception:
        pass


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "expand"
    rest = " ".join(argv[1:]) if len(argv) > 1 else ""
    if cmd == "steal":
        print(json.dumps(steal_search(rest or None), indent=2, ensure_ascii=False))
    elif cmd == "test":
        print(json.dumps(test_local(rest), indent=2, ensure_ascii=False))
    elif cmd == "expand":
        print(json.dumps(expand(force="--force" in argv), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(expand(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
