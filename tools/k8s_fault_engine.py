"""k8s_fault_engine.py - deterministic Kubernetes-semantics engine for the fault suite.

The instrument behind BOUNDED_TOOL_SURFACES (watch/inbox/BOUNDED_TOOL_SURFACES_SALVAGE_20261005.md):
F1 (competence tracks the tool boundary, not model scale) and F2 (policy-client
emergence) need machine-checkable chores on a controlled cluster. This engine is
LOCAL truth by construction: pods/deployments/services/configs/secrets/policies with
faithful fault semantics (ImagePullBackOff, CrashLoopBackOff, readiness probes,
selector matching, netpol denial, secret masking left to the arm executor).
It is NOT a live cluster: external validity on k3s/kind stays UNMEASURED by this
instrument (engine self-test + pytest are the proof surface).

Law (D10 split): engine owns state; agents only propose verbs through an arm executor.
"""
from __future__ import annotations

import copy
import json
from typing import Any

VALID_IMAGES = {
    "nginx:1.25", "nginx:1.27", "app/web:v1", "app/web:v2",
    "app/worker:v1", "busybox:1.36", "redis:7",
}
KINDS = ("deployment", "service", "configmap", "secret", "networkpolicy", "namespace")
READ_KINDS = ("deployment", "service", "configmap", "secret", "networkpolicy")
SECRET_TRUE_VALUE = "s3cr3t-hunter2"


def new_state() -> dict[str, Any]:
    return {
        "namespaces": ["app", "prod"],
        "deployment": {"app": {}, "prod": {}},
        "service": {"app": {}, "prod": {}},
        "configmap": {"app": {}, "prod": {}},
        "secret": {"app": {}, "prod": {}},
        "networkpolicy": {"app": {}, "prod": {}},
        "journal": [],
        "events": [],
    }


def _ev(state: dict, msg: str) -> None:
    state["events"].append(msg)


def _journal(state: dict, verb: str, kind: str, ns: str, name: str) -> None:
    state["journal"].append({"verb": verb, "kind": kind, "ns": ns, "name": name})


def _env_resolved(state: dict, ns: str, dep: dict) -> tuple[dict[str, str], list[str]]:
    """Resolve env literals + value_from refs. Returns (resolved, missing_refs)."""
    out: dict[str, str] = {}
    missing: list[str] = []
    for e in dep.get("env", []):
        if "value" in e:
            out[e["name"]] = str(e["value"])
            continue
        vf = e.get("value_from", {})
        spec = state.get(vf.get("kind", ""), {}).get(ns, {}).get(vf.get("name"), {})
        data = spec.get("data", {})
        if vf.get("key") not in data:
            missing.append(f"{vf.get('kind')}/{vf.get('name')}.{vf.get('key')}")
        else:
            out[e["name"]] = data[vf["key"]]
    return out, missing


def pod_statuses(state: dict, ns: str, name: str) -> list[tuple[str, str]]:
    """All pods of a deployment with deterministic status."""
    dep = state["deployment"].get(ns, {}).get(name)
    if dep is None:
        return []
    out: list[tuple[str, str]] = []
    for i in range(int(dep.get("replicas", 1))):
        pod = f"{name}-{i:04d}"
        out.append((pod, _pod_status(state, ns, dep)))
    return out


def _pod_status(state: dict, ns: str, dep: dict) -> str:
    if dep.get("image") not in VALID_IMAGES:
        return "ImagePullBackOff"
    env, missing = _env_resolved(state, ns, dep)
    if missing or env.get("CRASH") == "true":
        return "CrashLoopBackOff"
    probe = dep.get("readiness")
    if probe:
        served = {"/": True, "/healthz": True, "/ready": "EXTRA_READY" in env}
        if not served.get(probe.get("path", "/"), False):
            return "Running"
    return "Ready"


def ready_deployments(state: dict, ns: str) -> list[tuple[str, dict]]:
    out = []
    for name, dep in state["deployment"].get(ns, {}).items():
        if dep.get("replicas", 1) > 0 and _pod_status(state, ns, dep) == "Ready":
            out.append((name, dep))
    return out


def endpoints(state: dict, ns: str, svc: dict) -> list[str]:
    eps = []
    for name, dep in ready_deployments(state, ns):
        labels = dep.get("labels", {})
        if all(labels.get(k) == v for k, v in svc.get("selector", {}).items()):
            eps.append(name)
    return eps


def reachable(state: dict, ns: str, svc_name: str) -> tuple[bool, str]:
    svc = state["service"].get(ns, {}).get(svc_name)
    if svc is None:
        return False, f"service {ns}/{svc_name} not found"
    eps = endpoints(state, ns, svc)
    if not eps:
        return False, f"no ready endpoints match selector {svc.get('selector')}"
    for pol in state["networkpolicy"].get(ns, {}).values():
        for rule in pol.get("deny", []):
            if rule.get("to_svc") == svc_name:
                return False, f"networkpolicy {pol.get('name', '?')} denies traffic to {svc_name}"
    ports = {state["deployment"][ns][e].get("port") for e in eps}
    if svc.get("target_port") not in ports:
        return False, f"targetPort {svc.get('target_port')} matches no endpoint port {sorted(ports)}"
    return True, f"ok: {len(eps)} ready endpoint(s) behind {svc_name}"


def describe(state: dict, kind: str, ns: str, name: str) -> dict | None:
    if kind == "namespace":
        return {"name": name, "exists": name in state["namespaces"]}
    obj = copy.deepcopy(state.get(kind, {}).get(ns, {}).get(name))
    if obj is not None and kind == "deployment":
        obj["pods"] = pod_statuses(state, ns, name)
    return obj


def logs(state: dict, ns: str, name: str) -> list[str]:
    lines = []
    for pod, status in pod_statuses(state, ns, name):
        if status == "Ready":
            dep = state["deployment"][ns][name]
            env, _ = _env_resolved(state, ns, dep)
            paths = "/ /healthz" + (" /ready" if "EXTRA_READY" in env else "")
            lines.append(f"{pod} serving on :{dep.get('port', 80)} paths {paths}")
        elif status == "CrashLoopBackOff":
            env, missing = _env_resolved(state, ns, state["deployment"][ns][name])
            why = missing[0] if missing else "env CRASH=true, exit code 1"
            lines.append(f"{pod} Error: {why}")
        elif status == "ImagePullBackOff":
            img = state["deployment"][ns][name]["image"]
            lines.append(f"{pod} Back-off pulling image {img}")
        else:
            probe = state["deployment"][ns][name].get("readiness", {})
            lines.append(f"{pod} listening, but readiness {probe.get('path')} -> 404")
    return lines or [f"no pods for deployment {ns}/{name}"]


def apply(state: dict, kind: str, ns: str, name: str, spec: dict) -> tuple[bool, str]:
    if kind == "namespace":
        if name not in state["namespaces"]:
            state["namespaces"].append(name)
            _ev(state, f"namespace {name} created")
        return True, f"namespace {name} applied"
    if ns not in state["namespaces"]:
        return False, f"namespace {ns} not found"
    if kind not in READ_KINDS:
        return False, f"unknown kind {kind}"
    spec = dict(spec or {})
    spec["name"] = name
    state[kind].setdefault(ns, {})[name] = spec
    _journal(state, "apply", kind, ns, name)
    _ev(state, f"{kind} {ns}/{name} applied")
    if kind == "deployment":
        st = _pod_status(state, ns, spec)
        _ev(state, f"deployment {ns}/{name} pods: {st} ({spec.get('replicas')} desired)")
    return True, f"{kind} {ns}/{name} applied"


def scale(state: dict, ns: str, name: str, replicas: int) -> tuple[bool, str]:
    dep = state["deployment"].get(ns, {}).get(name)
    if dep is None:
        return False, f"deployment {ns}/{name} not found"
    dep["replicas"] = int(replicas)
    _journal(state, "scale", "deployment", ns, name)
    _ev(state, f"deployment {ns}/{name} scaled to {replicas}")
    return True, f"scaled {ns}/{name} to {replicas}"


def delete(state: dict, kind: str, ns: str, name: str) -> tuple[bool, str]:
    if kind == "pod":
        base = name.rsplit("-", 1)[0] if "-" in name else name
        dep = state["deployment"].get(ns, {}).get(base)
        if dep is None:
            return False, f"pod {ns}/{name} not found"
        _journal(state, "delete", "pod", ns, name)
        _ev(state, f"pod {ns}/{name} deleted (controller recreates it)")
        return True, f"pod {ns}/{name} deleted"
    if kind == "namespace":
        if name not in state["namespaces"]:
            return False, f"namespace {name} not found"
        state["namespaces"] = [n for n in state["namespaces"] if n != name]
        for k in READ_KINDS:
            state[k].pop(name, None)
        _journal(state, "delete", "namespace", ns="-", name=name)
        _ev(state, f"namespace {name} deleted with all resources")
        return True, f"namespace {name} deleted"
    store = state.get(kind, {}).get(ns, {})
    if name not in store:
        return False, f"{kind} {ns}/{name} not found"
    del store[name]
    _journal(state, "delete", kind, ns, name)
    _ev(state, f"{kind} {ns}/{name} deleted")
    return True, f"{kind} {ns}/{name} deleted"


KIND_ALIASES = {"namespaces": "namespace", "pods": "pod", "deployments": "deployment",
                "services": "service", "configmaps": "configmap", "secrets": "secret",
                "networkpolicies": "networkpolicy", "deploy": "deployment", "svc": "service",
                "cm": "configmap", "po": "pod", "ns": "namespace"}


def op(state: dict, verb: str, args: dict) -> tuple[bool, Any]:
    """Canonical engine operation. RBAC and masking are the arm executor's job."""
    kind = KIND_ALIASES.get(args.get("kind"), args.get("kind"))
    ns, name = args.get("ns", "app"), args.get("name")
    if verb == "list":
        kind = kind or "deployment"
        if kind == "namespace":
            return True, state["namespaces"]
        if kind == "pod":
            return False, "pods are listed per deployment: describe deployment NAME"
        return True, sorted(state.get(kind, {}).get(ns, {}).keys())
    if verb == "describe":
        obj = describe(state, kind, ns, name)
        return (obj is not None), obj if obj is not None else f"{kind} {ns}/{name} not found"
    if verb == "logs":
        if name not in state["deployment"].get(ns, {}):
            return False, f"deployment {ns}/{name} not found"
        return True, logs(state, ns, name)
    if verb == "events":
        return True, state["events"][-25:]
    if verb == "scale":
        if "replicas" not in args or "name" not in args:
            return False, "scale needs name and replicas"
        return scale(state, ns, name, args["replicas"])
    if verb == "apply":
        if not name or "spec" not in args:
            return False, "apply needs name and spec"
        ok, msg = apply(state, kind or "deployment", ns, name, args["spec"])
        return ok, msg
    if verb == "delete":
        return delete(state, kind or "deployment", ns, name or "")
    return False, f"unknown verb {verb}"


def snapshot(state: dict) -> str:
    return json.dumps(
        {k: state[k] for k in ("namespaces", "deployment", "service", "configmap",
                               "secret", "networkpolicy")},
        sort_keys=True, default=str,
    )
