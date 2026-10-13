"""tests for surface_adapters — the NATIVE steering layer, self-stolen from our own API machinery.
Deterministic $0 coordinator.

RIB (frozen spec):
  registry()   -> derived surface adapter map: each surface -> {kind: native|browser, configured,
      driver}. The truth is env/disk-derived, never hand-maintained.
  adapter(s)   -> best driver for a surface: NATIVE when free+configured, else BROWSER fallback.
  steer(s,g)   -> steer natively (deepseek API / slack webhook) or via browser (seat_steer). Honest
      if not configured/down — never fabricates.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import surface_adapters as sa  # noqa: E402


def test_registry_derived_and_complete():
    r = sa.registry()
    assert r["ok"] is True
    names = {s["surface"] for s in r["surfaces"]}
    for surf in ("deepseek", "slack", "chatgpt", "grok_web"):
        assert surf in names
    # each surface has a kind + a driver decision (native/browser/unconfigured-native)
    for s in r["surfaces"]:
        assert s["kind"] in ("native", "browser")
        assert s["driver"] in ("native", "browser", "unconfigured-native")


def test_adapter_native_when_free_else_browser():
    # browser surfaces always resolve to the browser fallback (no free native API)
    a = sa.adapter("chatgpt")
    assert a["ok"] is True and a["driver"] == "browser"
    # unknown surface is honest
    assert sa.adapter("nope")["ok"] is False


def test_native_call_honest_when_unconfigured():
    saved = os.environ.get(sa.SURFACE_DRIVERS["slack"]["key_env"])
    try:
        os.environ.pop(sa.SURFACE_DRIVERS["slack"]["key_env"], None)
        r = sa.native_call("slack", "test")
        assert r["ok"] is False
        assert "unconfigured" in r["error"]
    finally:
        if saved is not None:
            os.environ[sa.SURFACE_DRIVERS["slack"]["key_env"]] = saved


def test_steer_never_fabricates():
    # browser surfaces go through seat_steer and report honestly (may be down — never invents)
    r = sa.steer("chatgpt", "status")
    assert r["ok"] in (True, False)
    assert r["schema"] == "surface_adapters.v1"
    assert "surface" in r
    if r["ok"]:
        assert r.get("answer")
    else:
        assert r.get("error") or not r.get("answer")
