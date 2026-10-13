"""Worldline seed hook actor-child gate (2026-10-03 process-improve wave 1).

The disease: knot_at_close emits a full WORLDLINE SEED per closing session;
with the flash-window workflow fleet every actor child closes as a session,
minting 2,156 near-identical seeds (~45MB) in ~2 days and tripping the
gap-sentinel growth alert. The cure: dwf-* actor children skip the rite;
seat-scale closes keep it. Receipt: watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import knot_at_close  # noqa: E402


def test_hook_skips_dwf_actor_children(monkeypatch):
    import mag.worldline_seed as ws
    calls = []
    monkeypatch.setattr(ws, "emit", lambda session_id, out_dir=None: calls.append(session_id))
    knot_at_close._worldline_seed_hook("dwf-dwfrun-abc123-actor_1_2")
    assert calls == []  # actor children are not seats: no seed, no dir, no hashing


def test_hook_still_seeds_seat_sessions(monkeypatch):
    import mag.worldline_seed as ws
    calls = []
    monkeypatch.setattr(ws, "emit", lambda session_id, out_dir=None: calls.append(session_id))
    knot_at_close._worldline_seed_hook("sess_20261003_night")
    assert calls == ["sess_20261003_night"]
