# Test for substrate-native identity persistence.
# The recorded run identity is the {session_id, provider, model} triple that
# mag.agent_cli.load_run() resolves (env overrides, falling back to the last
# persisted seat session). This test simulates a substrate migration by
# re-initialising the recording module (importlib.reload) and checks the
# recorded identity stays constant.
#
# Fix receipt (burn lane substrate, 2026-09-27): the original version loaded
# `mag/state.py` via Path(__file__).parents[2] -- a module that has never
# existed in this repo (git log --all -- mag/state.py is empty) AND a parents
# index one level above the repo root, so it failed with FileNotFoundError on
# projects/mag/state.py. Identity recording actually lives in mag.agent_cli
# (load_run / normalize_seat, canonical {session_id, provider, model} shape).

import importlib
import os

import mag.agent_cli as agent_cli

_IDENTITY_ENV = {
    "MAG_AGENT_SESSION": "substrate-identity-check",
    "MAG_PROVIDER": "deepseek",
    "MAG_MODEL": "deepseek-chat",
}


def _load_identity() -> dict:
    # Pin the env inputs so identity is deterministic (and the disk fallback
    # branch of load_run is never consulted, keeping the test hermetic).
    saved = {k: os.environ.get(k) for k in _IDENTITY_ENV}
    os.environ.update(_IDENTITY_ENV)
    try:
        return agent_cli.load_run()
    finally:
        for key, prev in saved.items():
            if prev is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = prev


def test_identity_persistence():
    # Capture identity before "migration"
    before = _load_identity()
    # Simulate migration by re-initialising the recording module (clears caches)
    importlib.reload(agent_cli)
    after = _load_identity()
    assert before == after, (
        f"Identity changed across simulated substrate migration: {before} != {after}"
    )
