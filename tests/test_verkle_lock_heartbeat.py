"""Heartbeat lock (2026-10-15): verkle_lock + AOS carrier lock hold
{hostname, pid, start_ts, heartbeat_ts}; only a same-host stale heartbeat may be broken,
a foreign-host lock never is, and a self-restart (same host+pid+start_ts) is not a duplicate."""
from __future__ import annotations

import json
import os
import time

import pytest


@pytest.fixture()
def vk(tmp_path, monkeypatch):
    from mag import verkle_knot as vk
    monkeypatch.setattr(vk, "LOCK", tmp_path / ".verkle.lock")
    monkeypatch.setattr(vk, "_LOCK_POLL_SECONDS", 0.01)
    return vk


def _rec(vk, **kw):
    r = {"hostname": vk._lock_hostname(), "pid": 4242424, "start_ts": 1.0, "heartbeat_ts": time.time()}
    r.update(kw)
    return r


def _old_mtime(p):
    t = time.time() - 100000
    os.utime(p, (t, t))


def test_foreign_host_lock_never_broken_even_when_stale_looking(vk):
    rec = _rec(vk, hostname="aa87041bf557-other-host", heartbeat_ts=time.time() - 100000)
    vk.LOCK.write_text(json.dumps(rec), encoding="utf-8")
    _old_mtime(vk.LOCK)  # also older than the 900s legacy mtime window
    with pytest.raises(TimeoutError):
        with vk.verkle_lock(timeout=0.3):
            pass
    assert json.loads(vk.LOCK.read_text(encoding="utf-8")) == rec  # untouched


def test_same_host_stale_heartbeat_is_broken(vk):
    vk.LOCK.write_text(json.dumps(_rec(vk, heartbeat_ts=time.time() - 1000)), encoding="utf-8")
    with vk.verkle_lock(timeout=0.5):
        held = json.loads(vk.LOCK.read_text(encoding="utf-8"))
        assert held["pid"] == os.getpid() and held["hostname"] == vk._lock_hostname()
    assert not vk.LOCK.exists()


def test_same_host_live_heartbeat_is_not_broken(vk):
    rec = _rec(vk)  # another pid on this host, heartbeat now
    vk.LOCK.write_text(json.dumps(rec), encoding="utf-8")
    with pytest.raises(TimeoutError):
        with vk.verkle_lock(timeout=0.3):
            pass
    assert json.loads(vk.LOCK.read_text(encoding="utf-8")) == rec


def test_holder_writes_record_and_heartbeats(vk, monkeypatch):
    monkeypatch.setattr(vk, "LOCK_HEARTBEAT_SECONDS", 0.05)
    with vk.verkle_lock(timeout=0.5):
        a = json.loads(vk.LOCK.read_text(encoding="utf-8"))
        assert set(a) == {"hostname", "pid", "start_ts", "heartbeat_ts"}
        time.sleep(0.3)
        b = json.loads(vk.LOCK.read_text(encoding="utf-8"))
        assert b["heartbeat_ts"] > a["heartbeat_ts"] and b["pid"] == os.getpid()
    assert not vk.LOCK.exists()


def test_release_never_unlinks_a_lock_taken_over_by_someone_else(vk):
    other = _rec(vk)
    with vk.verkle_lock(timeout=0.5):
        # simulate a (same-host, stale) takeover rewriting the record while we still hold it
        vk.LOCK.write_text(json.dumps(other), encoding="utf-8")
    assert json.loads(vk.LOCK.read_text(encoding="utf-8")) == other


def test_carrier_self_restart_is_not_a_duplicate(tmp_path):
    from mag import governor_autorun as ga
    from mag import verkle_knot as vk
    p = tmp_path / "aos_carrier.lock"
    # what this process wrote before a POSIX execv: same host, same pid, same start_ts
    p.write_text(json.dumps(vk.lock_record()), encoding="utf-8")
    dup, why = ga._carrier_lock_verdict(p)
    assert dup is False and "self" in why
    p.write_text(str(os.getpid()), encoding="utf-8")  # legacy bare-pid form of the same bug
    assert ga._carrier_lock_verdict(p)[0] is False


def test_carrier_live_duplicate_and_foreign_and_stale(tmp_path):
    from mag import governor_autorun as ga
    from mag import verkle_knot as vk
    p = tmp_path / "aos_carrier.lock"
    p.write_text(json.dumps(_rec(vk)), encoding="utf-8")
    assert ga._carrier_lock_verdict(p)[0] is True  # live same-host carrier
    p.write_text(json.dumps(_rec(vk, hostname="other-host", heartbeat_ts=time.time() - 100000)), encoding="utf-8")
    assert ga._carrier_lock_verdict(p)[0] is True  # foreign host: never taken over
    p.write_text(json.dumps(_rec(vk, heartbeat_ts=time.time() - 1000)), encoding="utf-8")
    assert ga._carrier_lock_verdict(p)[0] is False  # same host, stale: take over
