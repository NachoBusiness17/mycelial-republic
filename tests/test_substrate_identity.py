# Test for substrate‑native identity persistence
# This test simulates a substrate migration by re‑initialising the Mag session
# and checks that the recorded identity (session_id, provider, model) stays constant.

import json
from pathlib import Path

# Helper to load the current identity from the running Mag state file
def load_identity() -> dict:
    state_path = Path(__file__).parents[2] / "mag" / "state.py"
    # The state module defines a global IDENTITY dict when imported
    import importlib.util
    spec = importlib.util.spec_from_file_location("mag_state", state_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "IDENTITY", {})


def test_identity_persistence(tmp_path):
    # Capture identity before "migration"
    before = load_identity()
    # Simulate migration by re‑loading the module (clears caches)
    import importlib
    import mag.state as state_mod
    importlib.reload(state_mod)
    after = load_identity()
    assert before == after, f"Identity changed across simulated substrate migration: {before} != {after}"
