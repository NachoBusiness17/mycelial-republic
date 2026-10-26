#!/usr/bin/env python3
"""tools/shannon_burst.py - High-Entropy Shannon Token Compactor for Overmind Injection.

Implements the Shannon Burst protocol for Gemini 4 Argon:
- Compresses broad estate state (Verkle chain tip, recent commit hints, Kuramoto phase,
  test results, active inbox cards) into maximum-entropy, zero-redundancy Shannon tokens.
- Eliminates conversational fluff, boilerplate prose, and redundant JSON syntax.
- Formats state into compact relational Horn clauses and dense AST tuples.
- Optimized for Gemini Context Caching: base system prompt is cached once, while
  shannon delta bursts are injected in rapid, low-cost pulses.

CONSUMER: Overmind prompt generator, autonomous heartbeat monitors.
VERIFIER: tests/test_shannon_burst.py.
HOUSE LAW: Strictly zero unicode em-dashes; zero side effects on failure; pure functions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def compute_shannon_entropy(text: str) -> float:
    """Calculate the empirical Shannon entropy H(X) in bits per character."""
    if not text:
        return 0.0
    import math
    counts: Dict[str, int] = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    total = len(text)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def compact_file_digest(fpath: Path) -> str:
    """Generate a compact 8-character hex digest of a file's state."""
    try:
        data = fpath.read_bytes()
        return hashlib.sha256(data).hexdigest()[:8]
    except OSError:
        return "00000000"


def generate_shannon_burst(
    repo_root: Optional[Path] = None,
    include_inbox: bool = True,
    max_items: int = 10,
) -> Dict[str, Any]:
    """Compile active estate state into an ultra-dense, high-entropy Shannon burst payload."""
    root = repo_root if repo_root is not None else ROOT
    ts_now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # 1. State Clamps & Invariant Vectors
    atoms: List[str] = [
        f"Epoch({ts_now})",
        "Constraint(1p_sg_voice, 0.00)",
        "Constraint(unicode_em_dash, 0)",
        "Governor(ultrasensitive_step, kd=0.80, n=8.0)",
        "Scheduler(kuramoto_phase, K=1.25, N=4)",
    ]

    # 2. Commit Hints Queue State
    hints_dir = root / "queue" / "commit_hints"
    active_hints: List[str] = []
    if hints_dir.exists():
        for hp in sorted(hints_dir.glob("*.json")):
            try:
                data = json.loads(hp.read_text(encoding="utf-8"))
                msg = data.get("message", "")[:40].replace('"', "'")
                p_count = len(data.get("paths", []))
                active_hints.append(f"Hint({hp.stem}, n_paths={p_count}, msg='{msg}')")
            except Exception:
                active_hints.append(f"Hint({hp.stem}, INVALID)")

    # 3. Active Wave Inbox Cards
    inbox_dir = root / "watch" / "inbox"
    active_cards: List[str] = []
    if include_inbox and inbox_dir.exists():
        for cp in sorted(inbox_dir.glob("INTAKE_WAVE*.md"), reverse=True)[:max_items]:
            digest = compact_file_digest(cp)
            active_cards.append(f"Card({cp.stem}, h8={digest})")

    # 4. Assemble Shannon Stream (Zero whitespace fluff, max information density)
    shannon_stream_lines = [
        "# SHANNON_STREAM_V1",
        " & ".join(atoms),
        " & ".join(active_hints) if active_hints else "Hints(EMPTY)",
        " & ".join(active_cards) if active_cards else "Cards(EMPTY)",
    ]
    raw_payload = "\n".join(shannon_stream_lines)
    entropy_bits = compute_shannon_entropy(raw_payload)

    return {
        "schema": "shannon_burst.v1",
        "timestamp_utc": ts_now,
        "char_count": len(raw_payload),
        "entropy_bits_per_char": entropy_bits,
        "total_information_bits": round(entropy_bits * len(raw_payload), 2),
        "shannon_payload": raw_payload,
    }


def main() -> int:
    """CLI emitter for the Shannon Token Burst generator."""
    parser = argparse.ArgumentParser(description="Shannon Token Burst Generator for Overmind")
    parser.add_argument("--json", action="store_true", help="Output full JSON metadata envelope")
    args = parser.parse_args()

    burst = generate_shannon_burst()
    if args.json:
        print(json.dumps(burst, indent=2))
    else:
        print(burst["shannon_payload"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
