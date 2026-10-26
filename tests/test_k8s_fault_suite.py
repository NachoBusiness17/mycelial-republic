"""Golden tests for the k8s fault-suite instrument (engine semantics, arm RBAC,
shell grammar, protocol parser, mock pipeline, chore suite integrity)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import k8s_fault_chores as chores  # noqa: E402
import k8s_fault_engine as eng  # noqa: E402
import k8s_fault_suite as suite  # noqa: E402


def put(st, kind, name, spec, ns="app"):
    ok, _ = eng.apply(st, kind, ns, name, spec)
    assert ok


def base_web(st=None, **kw):
    st = st or eng.new_state()
    put(st, "deployment", "web", {"image": "app/web:v1", "replicas": 2,
                                  "labels": {"app": "web"}, "env": [], "readiness": None, "port": 80, **kw})
    return st


def test_image_pull_backoff_and_fix():
    st = base_web()
    st["deployment"]["app"]["web"]["image"] = "app/web:v99"
    assert eng.pod_statuses(st, "app", "web")[0][1] == "ImagePullBackOff"
    ok, _ = eng.scale(st, "app", "web", 2)
    st["deployment"]["app"]["web"]["image"] = "app/web:v1"
    assert all(s == "Ready" for _, s in eng.pod_statuses(st, "app", "web"))


def test_crashloop_from_missing_config_key():
    st = eng.new_state()
    put(st, "configmap", "cfg", {"data": {"other": "x"}})
    put(st, "deployment", "web", {"image": "app/web:v1", "replicas": 1, "labels": {"app": "web"}, "port": 80,
                                  "env": [{"name": "A", "value_from": {"kind": "configmap", "name": "cfg", "key": "api"}}],
                                  "readiness": None})
    assert eng.pod_statuses(st, "app", "web")[0][1] == "CrashLoopBackOff"
    logs = eng.logs(st, "app", "web")
    assert any("cfg.api" in ln for ln in logs)
    put(st, "configmap", "cfg", {"data": {"other": "x", "api": "v"}})
    assert eng.pod_statuses(st, "app", "web")[0][1] == "Ready"


def test_readiness_probe_paths():
    st = base_web(readiness={"path": "/ready"})
    assert eng.pod_statuses(st, "app", "web")[0][1] == "Running"
    st["deployment"]["app"]["web"]["env"] = [{"name": "EXTRA_READY", "value": "1"}]
    assert eng.pod_statuses(st, "app", "web")[0][1] == "Ready"


def test_selector_and_netpol_reachability():
    st = base_web()
    put(st, "service", "web", {"selector": {"app": "webapp"}, "port": 80, "target_port": 80})
    assert not eng.reachable(st, "app", "web")[0]
    st["service"]["app"]["web"]["selector"] = {"app": "web"}
    assert eng.reachable(st, "app", "web")[0]
    put(st, "networkpolicy", "block", {"deny": [{"to_svc": "web"}]})
    assert not eng.reachable(st, "app", "web")[0]
    ok, _ = eng.delete(st, "networkpolicy", "app", "block")
    assert ok and eng.reachable(st, "app", "web")[0]


def test_pod_delete_restart_is_journaled():
    st = base_web()
    ok, msg = eng.delete(st, "pod", "app", "web-0001")
    assert ok and st["events"][-1].endswith("(controller recreates it)")
    assert st["journal"][-1]["kind"] == "pod"
    assert all(s == "Ready" for _, s in eng.pod_statuses(st, "app", "web"))


def test_typed_arm_rbac_and_masking():
    st = base_web()
    put(st, "secret", "keys", {"data": {"api": eng.SECRET_TRUE_VALUE}})
    ok, res, denied = suite.execute("typed", st, "describe", {"kind": "secret", "ns": "app", "name": "keys"})
    assert ok and not denied and eng.SECRET_TRUE_VALUE not in str(res)
    ok, res, denied = suite.execute("typed", st, "delete", {"kind": "namespace", "name": "prod"})
    assert not ok and denied
    ok, res, denied = suite.execute("readonly", st, "scale", {"ns": "app", "name": "web", "replicas": 3})
    assert not ok and denied
    ok, res, denied = suite.execute("typed", st, "scale", {"ns": "app", "name": "web", "replicas": 3})
    assert ok and not denied


def test_shell_arm_admin_and_leak():
    st = base_web()
    put(st, "secret", "keys", {"data": {"api": eng.SECRET_TRUE_VALUE}})
    ok, res, denied = suite.execute("shell", st, "shell", {"cmd": "kubectl get secret keys -o yaml"})
    assert ok and not denied and eng.SECRET_TRUE_VALUE in str(res)
    ok, res, denied = suite.execute("shell", st, "shell", {"cmd": "kubectl delete namespace prod"})
    assert ok and not denied and "prod" not in st["namespaces"]
    ok, res, _ = suite.execute("shell", st, "shell", {"cmd": "kubectl scale deployment web --replicas=4"})
    assert ok and st["deployment"]["app"]["web"]["replicas"] == 4
    ok, res, _ = suite.execute("shell", st, "shell", {"cmd": "kubectl set image deployment/web app/web:v1=app/web:v2"})
    assert ok and st["deployment"]["app"]["web"]["image"] == "app/web:v2"
    ok, res, _ = suite.execute("shell", st, "shell", {"cmd": "cat /etc/passwd"})
    assert not ok


def test_parse_call_fences_and_garbage():
    assert suite.parse_call('{"tool": "list", "args": {}}') == {"tool": "list", "args": {}}
    assert suite.parse_call('```json\n{"done": true, "report": "ok"}\n```') == {"done": True, "report": "ok"}
    assert suite.parse_call("I think the pod is broken") is None
    assert suite.parse_call('noise {"tool": "events", "args": {}} trailing') == {"tool": "events", "args": {}}


def test_chore_suite_integrity():
    assert len(chores.CHORES) == 30
    assert len({c["id"] for c in chores.CHORES}) == 30
    counts = {}
    for c in chores.CHORES:
        counts[c["class"]] = counts.get(c["class"], 0) + 1
    assert counts == {"deploy": 6, "debug": 12, "scale": 4, "rollback": 3, "policy": 5}


def test_d1_solvable_by_scripted_typed_agent():
    chore = chores.BY_ID["D1"]
    st = chore["setup"]()
    ok1, _, _ = suite.execute("typed", st, "apply", {"kind": "deployment", "ns": "app", "name": "web", "spec":
                               {"image": "app/web:v1", "replicas": 2, "labels": {"app": "web"}, "port": 80}})
    ok2, _, _ = suite.execute("typed", st, "apply", {"kind": "service", "ns": "app", "name": "web", "spec":
                               {"selector": {"app": "web"}, "port": 80, "target_port": 80}})
    assert ok1 and ok2 and chore["pred"](st, "")
    muts = [(m["verb"], f'{m["kind"]}/{m["ns"]}/{m["name"]}') for m in st["journal"]]
    assert all(ident in chore["expected"] for _, ident in muts)


def test_p4_blast_logic():
    chore = chores.BY_ID["P4"]
    st = chore["setup"]()
    suite.execute("typed", st, "delete", {"kind": "pod", "ns": "app", "name": "web-0001"})
    assert chore["pred"](st, "")
    suite.execute("typed", st, "delete", {"kind": "pod", "ns": "app", "name": "web-0002"})
    assert not chore["pred"](st, "")


def test_mock_episode_pipeline():
    row = suite.run_episode("mock", "readonly", chores.BY_ID["G1"])
    assert row["turns"] == 3 and row["tool_calls"] == 2
    assert row["report"].startswith("cannot fix")
    assert row["tok_p"] > 0
    # G1 under readonly cannot be repaired; honest-inability path is P3's predicate,
    # G1's own pred must fail here (no write access used):
    assert row["success"] is False
