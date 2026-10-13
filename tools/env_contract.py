"""env_contract -- the stolen MiMo env contract, estate-native (AC8 steal #1).

MiMo-V2.6-RL-oss ships every RL environment as a manifest.json (uploads /
setup / wait_ports / mcp_servers) and computes reward at rollout into
/logs/verifier/reward.json -- the environment, not a model, is the judge
(watch/inbox/last_mile_20260930/AC3_MIMO.md). Their lane costs a bespoke
docker image plus a wall-clock verifier budget (verifier_timeout_sec=1800
uniform). The estate's legality environments are an in-process seeded
water-graph engine with an exact constraint propagator for a verifier, so
the same contract shape lands with different physics
(watch/inbox/last_mile_20260930/AC8_MIMO_VS_ESTATE.md):

    manifest.json (one per environment family) -- schema env_manifest.v1:
        env_id          family name ("legality-water-graph-mountain-v1")
        engine          "water_graph" (mag/water_graph.py, the real engine)
        engine_version  git describe of the engine file (sha256 fallback)
        engine_sha256   the byte pin -- the ONLY field the drift check
                        trusts (trust bytes, not reports)
        verifier        "propagator" (tools/legality_propagator.py; the
                        agreement law means verdict semantics drift when
                        the propagator drifts, so it is pinned too)
        task_shape      the gps capability key for verdicts from this family
        reward_style    "rule" (MiMo's uniform style; ours is exact)
        timeout_sec     0 -- the declared advantage: exact + instant. Their
                        1800s verifier budget exists so a hung lane cannot
                        stall the meter; a 0-second oracle needs no budget.
        determinism     "seeded" -- same seed -> byte-identical rollouts
        label_set       the exact 5-way legality vocabulary

    reward.json (JSONL, one row per judged case) -- schema env_reward.v1:
        case_id, task_shape, verdict (binary 1/0 -- the gps feed shape of
        CapabilityLedger.record_verdict), label (the exact 5-way legality
        label; gps is binary by design, the nuance lives in the row),
        evidence_hash (64-hex, audit-walks the source artifact the way
        gwap's row_sha256 does in mag/gwap_to_gps.py).

FAIL-CLOSED LAWS: validate_manifest recomputes the live engine and verifier
sha256 and refuses ENGINE_DRIFT / VERIFIER_DRIFT / *_MISSING -- the
freshness law: a manifest describing bytes that no longer exist is a lie,
and the reader raises instead of warning. feed_reward_file is two-pass like
mag/gwap_to_gps.py: every row is validated and key-mapped into a plan
BEFORE the first record_verdict call, so any refusal leaves the ledger
untouched; and model_id is NEVER guessed (explicit model_id or
case_to_model, else NO_KEY_MAP -- the no-identity-fallback law).

Byte determinism: canonical sorted-key JSON, no wall clock anywhere in
manifest or reward rows. engine_version is repo-state-dependent (tags,
dirty tree) and is a human-facing pin only; the drift law reads
engine_sha256, never the version string.

Nothing production depends on this yet -- this is the format landing.

WIRING (AH7, 2026-09-29): run_legality makes the contract real for the
water-graph legality family. Semantics (the spec this wiring owns):

  - The PROPAGATOR is the judged subject. Each seeded case (state vector +
    action drawn from tools/legality_dataset.py's generators, read-only)
    is judged twice: by the engine-run ground truth (label_sample, the
    REAL WaterGraph) and by the oracle (tools/legality_propagator.py
    propagate). The row's binary verdict is AGREEMENT (1 = the propagator
    reproduced the engine's full verdict dict; 0 = disagreement, which the
    agreement law calls a bug in the propagator); `label` carries the
    engine's exact 5-way ground truth, the nuance the binary cannot.
  - No feed under drift: run_legality validates the family manifest
    (default tools/gps_mcp/env_manifest.v1.json) fail-closed BEFORE any
    case is judged, and refuses MANIFEST_MISMATCH when env_id/task_shape
    disagree with the requested rows -- rows that lie about their family
    are worse than no rows.
  - reward.json is regenerated per run (truncated, then appended by
    emit_reward): same seed + same engine/verifier bytes -> byte-identical
    rows. The ledger feed is append-only (record_verdict is a log), so a
    rerun honestly adds another N samples of the same measurement.
  - model_id defaults to "legality-propagator-v1" -- explicit, never
    guessed (the no-identity-fallback law); the capability row it builds
    is the propagator's measured agreement rate on task_shape
    legality-water-graph-v1.

CLI:  python tools/env_contract.py emit --out <dir>
      python tools/env_contract.py validate <manifest.json>
      python tools/env_contract.py run-legality [--cases 100] [--seed 17]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_SCHEMA = "env_manifest.v1"
REWARD_SCHEMA = "env_reward.v1"
MANIFEST_NAME = "manifest.json"
REWARD_NAME = "reward.json"

# The one environment family this contract lands with: the W3K legality
# corpus' Mountain water graphs (tools/legality_dataset.py).
DEFAULT_ENV_ID = "legality-water-graph-mountain-v1"
DEFAULT_ENGINE = "water_graph"
DEFAULT_ENGINE_PATH = "mag/water_graph.py"
DEFAULT_VERIFIER = "propagator"
DEFAULT_VERIFIER_PATH = "tools/legality_propagator.py"
DEFAULT_TASK_SHAPE = "legality-water-graph-v1"
REWARD_STYLE = "rule"
TIMEOUT_SEC_EXACT = 0  # 0 = exact/instant: no wall-clock verifier budget
DETERMINISM = "seeded"
LABEL_SET = [
    "illegal_unknown_verb",
    "illegal_unknown_target",
    "illegal_dry_pool",
    "legal_no_gain",
    "legal_gain",
]

# Wiring homes (AH7): where the live contract artifacts sit by default.
# The manifest lives beside the gps ledger it feeds; reward.json is a run
# artifact under logs/ (regenerated deterministically, referenced by receipts).
DEFAULT_MANIFEST_OUT = "tools/gps_mcp/env_manifest.v1.json"
DEFAULT_REWARD_OUT = "logs/legality_env/reward.json"
DEFAULT_LEDGER_PATH = "tools/gps_mcp/gps_ledger.db3"
# The judged subject of the wiring: the oracle whose agreement with the
# engine IS the capability being measured (agreement law).
DEFAULT_ORACLE_MODEL_ID = "legality-propagator-v1"

# field name -> python type (bool is rejected where int is required: bool
# is an int subclass and "timeout_sec": true is a lie, not a zero)
_MANIFEST_FIELDS: dict[str, type] = {
    "schema": str,
    "env_id": str,
    "engine": str,
    "engine_path": str,
    "engine_version": str,
    "engine_sha256": str,
    "verifier": str,
    "verifier_path": str,
    "verifier_sha256": str,
    "task_shape": str,
    "reward_style": str,
    "reward_schema": str,
    "timeout_sec": int,
    "determinism": str,
    "label_set": list,
}

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class EnvContractError(Exception):
    """Reason-coded refusal (house pattern: .reason carries the machine code)."""

    def __init__(self, reason: str, message: str = "") -> None:
        self.reason = reason
        super().__init__(message or reason)


def _require(condition: bool, reason: str, message: str) -> None:
    if not condition:
        raise EnvContractError(reason, message)


# ---------------------------------------------------------------- pins ----
def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(args: list[str], repo_root: Path) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(repo_root), *args],
                             capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def _git_describe(path: Path, repo_root: Path) -> str | None:
    """git describe of one file inside the repo, or None when unavailable
    (no git, not a repo, untracked path, timeout). Never raises: the version
    string is a human-facing pin; the sha256 is the law.

    Cause-and-evidence: `git describe -- <path>` does not exist -- describe
    reads object names, not pathspecs, so a direct attempt dies with
    "fatal: Not a valid object name" (rc 128) and would silently force
    every pin onto the sha256 fallback. The file pin is therefore two
    steps: the last commit that TOUCHED the file (git log -1), then
    describe of that commit (--always keeps it alive in a tagless repo by
    yielding the abbreviated commit hash). --dirty is likewise omitted:
    git rejects --dirty combined with a commit-ish."""
    try:
        rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return None
    touched = _git(["log", "-1", "--format=%H", "--", rel], repo_root)
    if not touched:
        return None  # untracked or unborn: caller falls back to the sha pin
    return _git(["describe", "--tags", "--always", touched], repo_root)


def pin_file(path: Path, repo_root: Path | None = None) -> dict[str, str]:
    """Byte pin + human version for one engine/verifier file.

    Returns {"version", "sha256"}; version prefers `git describe` of the
    file and falls back to "sha256:<hex>" when git cannot describe it."""
    _require(path.is_file(), "PIN_TARGET_MISSING", f"cannot pin {path}: not a file")
    sha = _sha256_file(path)
    root = repo_root if repo_root is not None else ROOT
    described = _git_describe(path, root)
    return {"version": described if described else f"sha256:{sha}",
            "sha256": sha}


def _rel_or_abs(path: Path, repo_root: Path) -> str:
    """Store repo-relative posix when the file lives under the repo root,
    else the absolute path -- so a manifest stays portable for in-repo
    files and honest about outside pins."""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


# ------------------------------------------------------------ manifest ----
def emit_manifest(
    path: Path | str,
    *,
    env_id: str = DEFAULT_ENV_ID,
    engine: str = DEFAULT_ENGINE,
    engine_path: Path | str = DEFAULT_ENGINE_PATH,
    verifier: str = DEFAULT_VERIFIER,
    verifier_path: Path | str = DEFAULT_VERIFIER_PATH,
    task_shape: str = DEFAULT_TASK_SHAPE,
    reward_style: str = REWARD_STYLE,
    timeout_sec: int = TIMEOUT_SEC_EXACT,
    determinism: str = DETERMINISM,
    label_set: list[str] | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Write the environment family's manifest.json and return it.

    `path` may be a directory (manifest.json is created inside) or a direct
    *.json file path. The engine/verifier paths resolve against repo_root
    (default: repo root) when relative. timeout_sec declares the verifier's
    wall-clock budget; 0 means exact/instant (the estate's oracle runs in
    process with no clock at all)."""
    for name, value in (("env_id", env_id), ("engine", engine),
                        ("task_shape", task_shape),
                        ("reward_style", reward_style),
                        ("determinism", determinism)):
        _require(isinstance(value, str) and bool(value.strip()),
                 "BAD_MANIFEST_FIELD", f"{name} must be a non-empty string")
    _require(isinstance(timeout_sec, int) and not isinstance(timeout_sec, bool)
             and timeout_sec >= 0,
             "BAD_MANIFEST_FIELD", "timeout_sec must be an int >= 0 (0 = exact)")

    root = repo_root if repo_root is not None else ROOT
    eng = Path(engine_path)
    eng = eng if eng.is_absolute() else root / eng
    ver = Path(verifier_path)
    ver = ver if ver.is_absolute() else root / ver
    eng_pin = pin_file(eng, root)
    ver_pin = pin_file(ver, root)

    manifest: dict[str, Any] = {
        "schema": MANIFEST_SCHEMA,
        "env_id": env_id,
        "engine": engine,
        "engine_path": _rel_or_abs(eng, root),
        "engine_version": eng_pin["version"],
        "engine_sha256": eng_pin["sha256"],
        "verifier": verifier,
        "verifier_path": _rel_or_abs(ver, root),
        "verifier_sha256": ver_pin["sha256"],
        "task_shape": task_shape,
        "reward_style": reward_style,
        "reward_schema": REWARD_SCHEMA,
        "timeout_sec": timeout_sec,
        "determinism": determinism,
        "label_set": list(label_set) if label_set is not None else list(LABEL_SET),
    }

    out = Path(path)
    if out.suffix != ".json":
        out = out / MANIFEST_NAME
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, sort_keys=True,
                              separators=(",", ":")) + "\n", encoding="utf-8")
    return manifest


def read_manifest(path: Path | str) -> dict[str, Any]:
    """Parse + shape-check a manifest. Fail-closed: MISSING_MANIFEST,
    BAD_MANIFEST (unparsable, foreign schema, missing/mistyped field)."""
    p = Path(path)
    _require(p.is_file(), "MISSING_MANIFEST", f"manifest not found: {p}")
    try:
        manifest = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise EnvContractError("BAD_MANIFEST", f"{p.name} is not JSON: {exc}")
    _require(isinstance(manifest, dict), "BAD_MANIFEST",
             f"{p.name} is not a JSON object")
    _require(manifest.get("schema") == MANIFEST_SCHEMA, "BAD_MANIFEST",
             f"{p.name} schema {manifest.get('schema')!r} is not "
             f"{MANIFEST_SCHEMA}")
    for field, want in _MANIFEST_FIELDS.items():
        value = manifest.get(field)
        _require(field in manifest, "BAD_MANIFEST",
                 f"{p.name} missing required field {field!r}")
        _require(isinstance(value, want) and not (
            want is int and isinstance(value, bool)), "BAD_MANIFEST",
            f"{p.name} field {field!r} is {type(value).__name__}, "
            f"want {want.__name__}")
    return manifest


def _resolve(declared: str, override: Path | str | None, root: Path) -> Path:
    if override is not None:
        p = Path(override)
        return p if p.is_absolute() else (root / p)
    p = Path(declared)
    return p if p.is_absolute() else (root / p)


def validate_manifest(
    path: Path | str,
    *,
    engine_path: Path | str | None = None,
    verifier_path: Path | str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Fail-closed freshness check: a manifest against the live engine bytes.

    Recomputes sha256 of the engine file (and the verifier, the oracle
    whose drift silently changes verdict semantics) and refuses on drift or
    disappearance. Returns a summary dict on success; never warns in place
    of refusing. The version string is never consulted -- bytes only."""
    manifest = read_manifest(path)
    root = repo_root if repo_root is not None else ROOT
    eng = _resolve(manifest["engine_path"], engine_path, root)
    _require(eng.is_file(), "ENGINE_MISSING",
             f"engine file {eng} declared by {manifest['env_id']} not found")
    live_eng = _sha256_file(eng)
    _require(live_eng == manifest["engine_sha256"], "ENGINE_DRIFT",
             f"engine {manifest['engine']}: manifest pins "
             f"{manifest['engine_sha256'][:12]}.. live bytes are "
             f"{live_eng[:12]}.. ({eng}); re-emit the manifest or revert "
             f"the engine -- never ignore the drift")
    ver = _resolve(manifest["verifier_path"], verifier_path, root)
    _require(ver.is_file(), "VERIFIER_MISSING",
             f"verifier file {ver} declared by {manifest['env_id']} not found")
    live_ver = _sha256_file(ver)
    _require(live_ver == manifest["verifier_sha256"], "VERIFIER_DRIFT",
             f"verifier {manifest['verifier']}: manifest pins "
             f"{manifest['verifier_sha256'][:12]}.. live bytes are "
             f"{live_ver[:12]}.. ({ver}); the oracle changed under the "
             f"contract -- re-emit the manifest")

    return {
        "env_id": manifest["env_id"],
        "engine": manifest["engine"],
        "engine_version": manifest["engine_version"],
        "engine_sha256": live_eng,
        "verifier": manifest["verifier"],
        "verifier_sha256": live_ver,
        "task_shape": manifest["task_shape"],
        "timeout_sec": manifest["timeout_sec"],
        "ok": True,
    }


# -------------------------------------------------------------- reward ----
def _normalize_verdict(verdict: Any) -> int:
    """Binary verdict, gps feed shape (CapabilityLedger accepts bool/0/1/
    pass/fail; the contract row pins 1/0 so reward.json is self-describing)."""
    if isinstance(verdict, bool):
        return int(verdict)
    if isinstance(verdict, int) and verdict in (0, 1):
        return verdict
    if isinstance(verdict, str):
        low = verdict.strip().lower()
        if low in ("pass", "true"):
            return 1
        if low in ("fail", "false"):
            return 0
    raise EnvContractError(
        "BAD_VERDICT",
        f"verdict {verdict!r} is not bool/0/1/pass/fail; the reward row is "
        f"binary (gps feed shape) -- carry the exact 5-way label in `label`")


def emit_reward(
    case_id: str,
    verdict: Any,
    evidence_hash: str,
    *,
    env_id: str = DEFAULT_ENV_ID,
    task_shape: str = DEFAULT_TASK_SHAPE,
    label: str | None = None,
    dest: Path | str | None = None,
) -> dict[str, Any]:
    """Build one reward.json row (schema env_reward.v1) and optionally
    append it, canonical JSONL, to `dest`.

    Row shape matches mag/gwap_to_gps.py's feed: (task_shape, verdict
    binary, evidence_hash) are exactly the CapabilityLedger.record_verdict
    arguments, case_id identifies the judged case, label keeps the exact
    legality vocabulary (the nuance gps's binary cannot carry). No wall
    clock: identical calls produce identical bytes."""
    _require(isinstance(case_id, str) and bool(case_id.strip()),
             "BAD_CASE_ID", "case_id must be a non-empty string")
    _require(isinstance(evidence_hash, str)
             and bool(_HEX64.match(evidence_hash.strip().lower())),
             "BAD_EVIDENCE_HASH",
             f"evidence_hash {evidence_hash!r} is not 64-hex; the audit "
             f"walks it, so a weak hash refuses")
    row: dict[str, Any] = {
        "schema": REWARD_SCHEMA,
        "env_id": env_id,
        "task_shape": task_shape,
        "case_id": case_id,
        "verdict": _normalize_verdict(verdict),
        "label": label,
        "evidence_hash": evidence_hash.strip().lower(),
    }
    if dest is not None:
        out = Path(dest)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(row, sort_keys=True,
                                separators=(",", ":")) + "\n")
    return row


def _read_reward_rows(path: Path) -> list[dict[str, Any]]:
    _require(path.is_file(), "MISSING_REWARD_FILE",
             f"reward file not found: {path}")
    rows: list[dict[str, Any]] = []
    for lineno, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EnvContractError("BAD_REWARD_ROW",
                                   f"{path.name}:{lineno} is not JSON: {exc}")
        _require(isinstance(row, dict) and row.get("schema") == REWARD_SCHEMA,
                 "BAD_REWARD_ROW",
                 f"{path.name}:{lineno} is not a {REWARD_SCHEMA} row")
        _require(isinstance(row.get("case_id"), str)
                 and bool(row["case_id"].strip())
                 and isinstance(row.get("task_shape"), str)
                 and bool(row["task_shape"].strip())
                 and isinstance(row.get("verdict"), int)
                 and not isinstance(row["verdict"], bool)
                 and row["verdict"] in (0, 1)
                 and isinstance(row.get("evidence_hash"), str)
                 and bool(_HEX64.match(row["evidence_hash"])),
                 "BAD_REWARD_ROW",
                 f"{path.name}:{lineno} fails the {REWARD_SCHEMA} shape "
                 f"(case_id/task_shape str, verdict 0|1, evidence 64-hex)")
        rows.append(row)
    return rows


def _model_id_for(row: dict[str, Any],
                  model_id: str | None,
                  case_to_model: dict[str, str] | None) -> str:
    """Explicit model_id for the file, else a per-case map; NEVER a guess
    (a guessed key seeds some other model's capability row -- the
    mag/gwap_to_gps.py no-identity-fallback law, verbatim)."""
    if model_id is not None:
        return model_id
    if case_to_model is not None:
        case = row["case_id"]
        _require(case in case_to_model, "UNMAPPED_CASE",
                 f"case_id {case!r} missing from case_to_model")
        return case_to_model[case]
    raise EnvContractError(
        "NO_KEY_MAP",
        "supply model_id or case_to_model; model_id is never guessed")


def feed_reward_file(
    reward_path: Path | str,
    gps: Any,
    *,
    model_id: str | None = None,
    case_to_model: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Feed a reward.json into the gps capability ledger.

    Two-pass fail-closed, the mag/gwap_to_gps.py law: every row is
    validated and key-mapped into a plan BEFORE the first record_verdict
    call, so any refusal (missing file, foreign row, unmapped key) leaves
    the ledger untouched -- no partial feed. `gps` is a CapabilityLedger or
    a path to one. Returns {rows_seen, fed, task_shapes, evidence_hashes,
    model_ids}."""
    from tools.gps_mcp.ledger import CapabilityLedger

    _require(model_id is None or isinstance(model_id, str), "NO_KEY_MAP",
             "model_id must be a string when given")
    path = Path(reward_path)
    owns_ledger = not isinstance(gps, CapabilityLedger)
    ledger = gps if isinstance(gps, CapabilityLedger) else CapabilityLedger(gps)
    rows = _read_reward_rows(path)

    report: dict[str, Any] = {
        "reward_path": str(path),
        "rows_seen": len(rows),
        "fed": 0,
        "task_shapes": set(),
        "evidence_hashes": [],
        "model_ids": set(),
    }

    # Pass 1: validate + key-map everything; pass 2 cannot refuse anymore.
    plan: list[tuple[str, str, int, str]] = []  # model_id, task_shape, verdict, evidence
    for row in rows:
        plan.append((_model_id_for(row, model_id, case_to_model),
                     row["task_shape"], row["verdict"], row["evidence_hash"]))
    try:
        for mid, shape, verdict, evidence in plan:
            ledger.record_verdict(model_id=mid, task_shape=shape,
                                  verdict=verdict, evidence_hash=evidence)
            report["fed"] += 1
            report["task_shapes"].add(shape)
            report["evidence_hashes"].append(evidence)
            report["model_ids"].add(mid)
    finally:
        if owns_ledger:
            ledger.close()
    report["task_shapes"] = sorted(report["task_shapes"])
    report["model_ids"] = sorted(report["model_ids"])
    return report


# ------------------------------------------------------- wiring (AH7) ----
def _judged_case_evidence(case: dict[str, Any]) -> str:
    """evidence_hash for one legality row: sha256 over the canonical bytes
    of the full judged case (graph, action, BOTH verdict dicts) -- the audit
    walk: anyone holding the row can rebuild this material from the seed,
    re-run engine and propagator on it, and reproduce hash + verdict, the
    way gwap's row_sha256 audit-walks its source row."""
    return hashlib.sha256(json.dumps(case, sort_keys=True,
                                     separators=(",", ":"))
                          .encode("utf-8")).hexdigest()


def run_legality(
    *,
    cases: int = 100,
    seed: int = 17,
    manifest_path: Path | str = DEFAULT_MANIFEST_OUT,
    reward_path: Path | str = DEFAULT_REWARD_OUT,
    ledger_path: Path | str | None = DEFAULT_LEDGER_PATH,
    model_id: str = DEFAULT_ORACLE_MODEL_ID,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Make the contract real for the water-graph legality family (AH7).

    The PROPAGATOR is the judged subject (the module WIRING spec): each
    seeded case from tools/legality_dataset.py's generators (read-only) is
    judged twice -- engine-run ground truth (label_sample, the REAL
    WaterGraph) and the oracle (propagate) -- and the row's binary verdict
    is AGREEMENT (1 = the propagator reproduced the engine's full verdict
    dict); `label` carries the engine's exact 5-way ground truth. The
    family manifest is validated fail-closed BEFORE any case is judged (no
    feed under drift), and env_id/task_shape must match the rows this run
    emits (MANIFEST_MISMATCH). reward.json is regenerated per run
    (truncated, then appended): same seed + same engine/verifier bytes ->
    byte-identical rows; the ledger feed is append-only through
    feed_reward_file's two-pass law. model_id is explicit, never guessed.

    Returns {manifest, cases, seed, agree, agreement_rate, labels,
    reward_path, reward_sha256, fed, model_id, ledger_path}."""
    _require(isinstance(cases, int) and not isinstance(cases, bool)
             and cases > 0,
             "BAD_CASES", "cases must be a positive int")
    root = repo_root if repo_root is not None else ROOT

    # No feed under drift: the manifest is the gate, checked FIRST -- a
    # drifted engine/verifier must refuse before a single case is judged,
    # so the ledger can never gain rows measured against stale bytes.
    summary = validate_manifest(manifest_path, repo_root=root)
    _require(summary["env_id"] == DEFAULT_ENV_ID
             and summary["task_shape"] == DEFAULT_TASK_SHAPE,
             "MANIFEST_MISMATCH",
             f"manifest env {summary['env_id']!r} / task_shape "
             f"{summary['task_shape']!r} is not the legality family "
             f"{DEFAULT_ENV_ID!r} / {DEFAULT_TASK_SHAPE!r} that the rows "
             f"this run emits describe -- rows that lie about their family "
             f"are worse than no rows")

    # Read-only use of the dataset generators: the wiring judges their
    # (state, action) draws, it never regenerates the corpus itself.
    from tools.legality_dataset import (label_sample,  # noqa: E402
                                        make_graph_spec, sample_action)
    from tools.legality_propagator import propagate  # noqa: E402

    def _rooted(p: Path | str) -> Path:
        q = Path(p)
        return q if q.is_absolute() else root / q

    out = _rooted(reward_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("", encoding="utf-8")  # regenerated per run

    rng = random.Random(seed)
    agree = 0
    by_label: dict[str, int] = {}
    for i in range(cases):
        spec = make_graph_spec(rng)
        verb, target = sample_action(rng, spec)
        engine = label_sample(spec, verb, target)  # runs the REAL engine
        oracle = propagate(spec, verb, target)     # constraints only
        verdict = 1 if oracle == engine else 0     # the agreement law
        label = engine["label"]
        _require(label in LABEL_SET, "BAD_LABEL",
                 f"engine label {label!r} is outside the manifest label_set; "
                 f"the family vocabulary drifted -- re-emit the manifest")
        agree += verdict
        by_label[label] = by_label.get(label, 0) + 1
        case_id = f"legality-{seed:05d}-{i:04d}"
        emit_reward(case_id, verdict,
                    _judged_case_evidence({"case_id": case_id, "graph": spec,
                                           "verb": verb, "target": target,
                                           "engine": engine, "oracle": oracle}),
                    label=label, dest=out)

    fed = 0
    ledger_used: str | None = None
    if ledger_path is not None:
        lp = _rooted(ledger_path)
        fed = feed_reward_file(out, lp, model_id=model_id)["fed"]
        ledger_used = str(lp)

    return {
        "manifest": str(manifest_path),
        "cases": cases,
        "seed": seed,
        "agree": agree,
        "agreement_rate": agree / cases,
        "labels": dict(sorted(by_label.items())),
        "reward_path": str(out),
        "reward_sha256": _sha256_file(out),
        "fed": fed,
        "model_id": model_id,
        "ledger_path": ledger_used,
    }


# ----------------------------------------------------------------- cli ----
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="MiMo-style env contract: manifest.json + reward.json "
                    "for the estate's legality environments (AC8 steal #1)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("emit", help="write an environment family manifest.json")
    e.add_argument("--out", type=Path, required=True,
                   help="output directory (or direct *.json path)")
    e.add_argument("--env-id", default=DEFAULT_ENV_ID)
    e.add_argument("--task-shape", default=DEFAULT_TASK_SHAPE)
    e.add_argument("--engine-path", default=DEFAULT_ENGINE_PATH)
    e.add_argument("--verifier-path", default=DEFAULT_VERIFIER_PATH)
    e.add_argument("--timeout-sec", type=int, default=TIMEOUT_SEC_EXACT,
                   help="verifier wall-clock budget; 0 = exact/instant")

    v = sub.add_parser("validate",
                       help="fail-closed drift check: manifest vs live bytes")
    v.add_argument("manifest", type=Path)
    v.add_argument("--engine-path", default=None,
                   help="override the declared engine file (tests, audits)")
    v.add_argument("--verifier-path", default=None)

    r = sub.add_parser("run-legality",
                       help="AH7 wiring: judge N legality cases (engine vs "
                            "propagator), emit reward.json, feed the gps "
                            "ledger")
    r.add_argument("--cases", type=int, default=100)
    r.add_argument("--seed", type=int, default=17)
    r.add_argument("--manifest", type=Path, default=Path(DEFAULT_MANIFEST_OUT))
    r.add_argument("--reward", type=Path, default=Path(DEFAULT_REWARD_OUT))
    r.add_argument("--ledger", type=Path, default=Path(DEFAULT_LEDGER_PATH))
    r.add_argument("--model-id", default=DEFAULT_ORACLE_MODEL_ID)
    r.add_argument("--no-feed", action="store_true",
                   help="judge + emit reward.json only; never touch the ledger")

    args = ap.parse_args(argv)
    try:
        if args.cmd == "run-legality":
            rep = run_legality(cases=args.cases, seed=args.seed,
                               manifest_path=args.manifest,
                               reward_path=args.reward,
                               ledger_path=None if args.no_feed else args.ledger,
                               model_id=args.model_id)
            print(f"validated {rep['manifest']} "
                  f"(engine+verifier pins match live bytes)")
            print(f"agreement: {rep['agree']}/{rep['cases']} "
                  f"({rep['agreement_rate']:.2%})  labels: {rep['labels']}")
            print(f"reward: {rep['reward_path']} sha256 "
                  f"{rep['reward_sha256'][:12]}.. ({rep['cases']} rows)")
            print(f"fed {rep['fed']} verdict rows -> {rep['ledger_path']} "
                  f"model_id {rep['model_id']} task_shape "
                  f"{DEFAULT_TASK_SHAPE}")
        elif args.cmd == "emit":
            m = emit_manifest(
                args.out, env_id=args.env_id, task_shape=args.task_shape,
                engine_path=args.engine_path,
                verifier_path=args.verifier_path,
                timeout_sec=args.timeout_sec)
            print(f"manifest: {args.out / MANIFEST_NAME}"
                  if args.out.suffix != ".json" else f"manifest: {args.out}")
            print(f"  env {m['env_id']}  engine {m['engine']} "
                  f"({m['engine_path']})")
            print(f"  version {m['engine_version']}")
            print(f"  engine sha256 {m['engine_sha256'][:12]}..  "
                  f"verifier sha256 {m['verifier_sha256'][:12]}..")
            print(f"  task_shape {m['task_shape']}  reward_style "
                  f"{m['reward_style']}  timeout_sec {m['timeout_sec']} "
                  f"(0 = exact/instant)  determinism {m['determinism']}")
        else:
            ok = validate_manifest(args.manifest,
                                   engine_path=args.engine_path,
                                   verifier_path=args.verifier_path)
            print(f"OK env {ok['env_id']}: engine {ok['engine']} sha256 "
                  f"{ok['engine_sha256'][:12]}.. matches pin; verifier "
                  f"{ok['verifier']} matches pin; task_shape "
                  f"{ok['task_shape']}, timeout_sec {ok['timeout_sec']}")
    except EnvContractError as exc:
        print(f"REFUSED {exc.reason}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
