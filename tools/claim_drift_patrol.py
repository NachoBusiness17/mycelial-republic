"""Claim drift patrol: rerun each watch/claims.jsonl row's verification on demand.
GENETIC BURN G1 lane i02-patrol-build (2026-10-18); design G0 lane g06. Binds the REAL
landed interfaces, which outrank the design where they differ: i03's battery
(tests/test_claim_drift_patrol.py, g06 flat rows) and i01's ledger (mag/claim_ledger.py
+ watch/claims.jsonl, mag_claims.v1 pins/typed verifiers); load_ledger() accepts BOTH
shapes. Exit ladder (g06 s5): 0 green = first line "CLAIM-PATROL: ok" (B2-338); 1
STALE/CONTRADICTED (hook WARN arm); 2 cannot-verify (B2-277 blind differs from stale;
F4 every exit-2 names its row). Accept-by-name baseline (sha256 rule NUL id NUL detail,
16 hex): suppressed rows still print GROWTH on churn or age (B2-273); expired
acceptances re-violate; --prune reaps cured fps. --check is bytes-only (B2-69);
--collect runs flat argv verifiers and v1 delegate_tool argv; other v1 verifier types
and non-GREEN registration_verdict rows surface red or UNVERIFIABLE, never a silent
pass (fail-closed, never a guess). Line-density note: the <400-line bar cost blank
lines; the full law text lives in the i02 lane report.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
ESTATE_ROOT = Path(__file__).resolve().parents[1]
LEDGER_DEFAULT = Path("watch") / "claims.jsonl"
BASELINE_DEFAULT = Path("configs") / "claim_drift_baseline.json"
OK_PREFIX = "CLAIM-PATROL: ok"
UNVER_PREFIX = "CLAIM-PATROL: UNVERIFIABLE"
V1_SCHEMA = "mag_claims.v1"
FLAT_REQUIRED = ("id", "claim_text", "carrier_path", "claim_regex", "moment", "owner")
V1_REQUIRED = ("schema", "id", "claim_text", "carrier_path", "pins", "moment", "owner",
               "consumer", "verifier", "on_fail", "registration_verdict", "receipt")
DETAIL = {"STALE": ("stale", "claim lags carrier"),
          "CONTRADICTED": ("contradicted", "verifier contradicts claim")}
FLAG_NAMES = {"MULTILINE": re.MULTILINE, "IGNORECASE": re.IGNORECASE, "DOTALL": re.DOTALL}
INT_LINE_RE = re.compile(r"^([\d,]+)$")
class PatrolError(Exception):
    """Cannot-verify: the caller must exit 2, never guess (B2-277)."""
def parse_moment(value):
    """ISO date or ISO instant -> date; None when unparsable (fail-closed)."""
    if not isinstance(value, str) or not value.strip():
        return None
    s = value.strip()
    try:
        return datetime.fromisoformat(s[:-1] + "+00:00" if s.endswith(("Z", "z")) else s).date()
    except ValueError:
        return None
def _pin_flags(value):
    acc = 0
    for name in ([value] if isinstance(value, str) else (value or [])):
        if name not in FLAG_NAMES:
            raise PatrolError(f"unknown regex flag {name!r}")
        acc |= FLAG_NAMES[name]
    return acc
def _compile_or_die(source, label):
    if not isinstance(source, str) or not source:
        raise PatrolError(f"{label}: claim_regex required non-empty string")
    try:
        return re.compile(source)
    except re.error as exc:
        raise PatrolError(f"{label}: claim_regex does not compile ({exc})") from None
def _load_v1_pins(row, where):
    """Compile a mag_claims.v1 row's pins into the common internal form."""
    pins = row["pins"]
    if not isinstance(pins, list) or not pins:
        raise PatrolError(f"{where}: pins must be a non-empty array")
    out = []
    for i, pin in enumerate(pins):
        label = f"{where}: pins[{i}]"
        if not isinstance(pin, dict) or not str(pin.get("pin_id") or "").strip():
            raise PatrolError(f"{label}: must be an object with a non-empty pin_id")
        try:
            mask = _pin_flags(pin.get("flags"))
            rx = re.compile(_compile_or_die(pin.get("claim_regex"), label).pattern, mask)
            locator = re.compile(pin["locator_regex"], mask) if pin.get("locator_regex") else None
            mode, fields = pin.get("mode", "single"), pin.get("capture_fields", [])
            if mode not in ("single", "finditer_all") or not isinstance(fields, list) \
                    or not all(isinstance(f, str) for f in fields) or len(fields) > rx.groups:
                raise PatrolError(f"bad mode/capture_fields (mode={mode!r}, fields={fields!r}, regex groups={rx.groups})")
        except (PatrolError, re.error) as exc:
            raise PatrolError(f"{label}: {exc}") from None
        out.append({"pin_id": pin["pin_id"], "_regex": rx, "_locator": locator, "mode": mode, "capture_fields": list(fields), "expected": pin.get("expected")})
    row["_pins"] = out
def _load_row(row, where):
    """Validate one row in either landed shape (g06 flat or mag_claims.v1)."""
    is_v1 = row.get("schema") == V1_SCHEMA
    missing = [k for k in (V1_REQUIRED if is_v1 else FLAT_REQUIRED)
               if k not in row or row[k] is None or row[k] == ""]
    if missing:
        raise PatrolError(f"{where}: missing required key(s) {missing}")
    row["_moment"] = parse_moment(row["moment"])
    if row["_moment"] is None:
        raise PatrolError(f"{where}: moment not an ISO date/instant: {row['moment']!r}")
    if is_v1:
        _load_v1_pins(row, where)
    else:
        rx = _compile_or_die(row["claim_regex"], where)
        row["_pins"] = [{"pin_id": "claim", "_regex": rx, "_locator": None, "mode": "single", "capture_fields": None, "expected": None}]
def load_ledger(path) -> list:
    """Load and validate the ledger; every PatrolError names "<path>:<1-based line>"."""
    p = Path(path)
    if not p.is_file():
        raise PatrolError(f"ledger missing: {p}")
    rows, seen = [], {}
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        where = f"{p}:{n}"
        if not line.strip():
            raise PatrolError(f"{where}: blank line (never skip a ledger line)")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PatrolError(f"{where}: unparseable JSON line ({exc.msg})") from None
        if not isinstance(row, dict):
            raise PatrolError(f"{where}: line is JSON but not an object")
        _load_row(row, where)
        if row["id"] in seen:
            raise PatrolError(f"{where}: duplicate id {row['id']!r} (first seen on line {seen[row['id']]})")
        seen[row["id"]] = n
        rows.append(row)
    return rows
def claim_patrol(moment, today, stale_days, carrier_touched, text_differs) -> dict:
    """Tier-1 pure verdict core (g06 s3): age past the bar AND a moved-world signal."""
    if moment > today:
        return {"ok": False, "verdict": "UNVERIFIABLE", "exit": 2, "reason": f"future moment {moment.isoformat()} is a fabrication smell; refresh the row"}
    age, moved = (today - moment).days, bool(carrier_touched or text_differs)
    if age > stale_days and moved:
        why = "; ".join(w for on, w in ((carrier_touched, "carrier committed after the moment"), (text_differs, "carrier bytes drifted from the registered claim")) if on)
        return {"ok": False, "verdict": "STALE", "exit": 1, "reason": f"claim {age}d old, past the {stale_days}d bar, and the world moved under it ({why}); refresh carrier and row together and name a receipt"}
    why = "carrier moved inside the window (snapshot tolerance)" if moved else "carrier untouched, bytes unchanged"
    return {"ok": True, "verdict": "OK", "exit": 0, "reason": f"claim {age}d old of {stale_days}d bar; {why}"}
def verify_patrol(claimed, real, value_kind="int", tolerance=20) -> dict:
    """Tier-2 pure verdict core: at-bar contradiction is symmetric (B2-244)."""
    if claimed is None or real is None:
        return {"ok": False, "verdict": "UNVERIFIABLE", "exit": 2, "reason": "claimed or measured value missing; cannot verify, never guess"}
    if value_kind == "text":
        if str(claimed) != str(real):
            return {"ok": False, "verdict": "CONTRADICTED", "exit": 1, "reason": f"verifier says {real!r}, carrier claims {claimed!r}"}
        return {"ok": True, "verdict": "OK", "exit": 0, "reason": "text claim matches verifier"}
    try:
        c_int, r_int = int(str(claimed).replace(",", "")), int(str(real).replace(",", ""))
    except (TypeError, ValueError):
        return {"ok": False, "verdict": "UNVERIFIABLE", "exit": 2, "reason": f"claimed value {claimed!r} uncastable as int"}
    if abs(c_int - r_int) >= tolerance:
        return {"ok": False, "verdict": "CONTRADICTED", "exit": 1, "reason": f"verifier measures {r_int}, carrier claims {c_int}, delta {abs(c_int - r_int)} at tolerance {tolerance} (symmetric: under-claim is B2-244, over-claim invented)"}
    return {"ok": True, "verdict": "OK", "exit": 0, "reason": f"verifier {r_int} vs claim {c_int}, inside tolerance {tolerance}"}
def fingerprint(rule: str, claim_id: str, detail: str) -> str:
    return hashlib.sha256(f"{rule}\0{claim_id}\0{detail}".encode("utf-8")).hexdigest()[:16]
def carrier_touched(root: Path, carrier_rel: str, moment: date) -> bool:
    """Any git commit dated strictly after the moment day touched the carrier."""
    try:
        proc = subprocess.run(["git", "log", "--format=%cI", "--", carrier_rel], cwd=str(root), capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PatrolError(f"git log failed for {carrier_rel}: {exc}") from None
    if proc.returncode != 0:
        raise PatrolError(f"git log failed for {carrier_rel}: {proc.stderr.strip()}")
    days = []
    for line in proc.stdout.splitlines():
        try:
            days.append(datetime.fromisoformat(line.strip()).date())
        except ValueError:
            continue
    return any(d > moment for d in days)
def _pin_matches(pin, text) -> list:
    rx, locator, mode = pin["_regex"], pin["_locator"], pin["mode"]
    if locator is None:
        if mode == "finditer_all":
            return list(rx.finditer(text))
        first = rx.search(text)
        return [first] if first else []
    hits = []
    for lm in locator.finditer(text):
        nl = text.find("\n", lm.end())
        found = rx.search(text[lm.end():] if nl == -1 else text[lm.end():nl])
        if found:
            hits.append(found)
    return hits
def _cap_eq(cap, want) -> bool:
    if isinstance(want, (int, float)) and not isinstance(want, bool):
        try:
            return float(str(cap).replace(",", "")) == float(want)
        except ValueError:
            return False
    return str(cap) == str(want)
def _pin_differs(pin, matches) -> bool:
    """True when the pin's current captures drift from its registration expected."""
    fields, expected, mode = pin["capture_fields"], pin["expected"], pin["mode"]
    if not fields:
        return False  # presence-only pin: a match IS the claim
    if mode == "finditer_all":
        if not isinstance(expected, dict):
            return not matches
        got = {str(m.group(1)): str(m.group(2)) for m in matches}
        return got != {str(k): str(v) for k, v in expected.items()}
    if not matches or not isinstance(expected, dict):
        return not matches
    found = matches[0]
    return any(expected.get(n) is not None and not _cap_eq(found.group(i), expected[n]) for i, n in enumerate(fields, 1))
def _unver(reason: str) -> dict:
    return {"ok": False, "verdict": "UNVERIFIABLE", "exit": 2, "reason": reason}
def _check_row(row, root, today, stale_override):
    """Tier-1 for one row -> (verdict, evidence, claim_now, matches_by_pin)."""
    carrier = root / row["carrier_path"]
    if not carrier.is_file():
        return _unver(f"carrier missing: {row['carrier_path']} (blind differs from stale, B2-277)"), [], None, {}
    text = carrier.read_text(encoding="utf-8", errors="replace")
    evidence, differs, by_pin = [], False, {}
    for pin in row["_pins"]:
        matches = _pin_matches(pin, text)
        by_pin[pin["pin_id"]] = matches
        if not matches:
            return _unver(f"pin {pin['pin_id']!r} claim_regex does not match {row['carrier_path']} (reworded past its frozen grammar? update the row with a receipt)"), evidence, None, by_pin
        if _pin_differs(pin, matches):
            differs = True
            evidence.append(f"pin {pin['pin_id']}: captures drifted from registration expected")
    if row.get("schema") != V1_SCHEMA and by_pin["claim"][0].group(0) != row["claim_text"]:
        differs = True
        evidence.append("carrier bytes no longer match the registered claim_text")
    claim_now = json.dumps([[str(g) for g in by_pin[p["pin_id"]][0].groups()] for p in row["_pins"]])
    if row["_moment"] > today:
        return claim_patrol(row["_moment"], today, 0, False, False), evidence, claim_now, by_pin
    bar = stale_override if stale_override is not None else int(row.get("stale_days", 7))
    verdict = claim_patrol(row["_moment"], today, bar, carrier_touched(root, row["carrier_path"], row["_moment"]), differs)
    reg = row.get("registration_verdict")
    if verdict["ok"] and reg in ("STALE-AT-REGISTRATION", "CONTRADICTED"):
        verdict = {"ok": False, "verdict": "STALE" if reg == "STALE-AT-REGISTRATION" else "CONTRADICTED", "exit": 1, "reason": f"registered {reg} at {row['moment']}: the ledger's own testimony says the carrier lags machine truth; cure the row or accept-by-name"}
    return verdict, evidence, claim_now, by_pin
def _run_argv(argv, root, timeout):
    """Run argv cwd=root. Returns (rc, last stdout line) or (None, verdict dict)."""
    try:
        proc = subprocess.run([str(a) for a in argv], cwd=str(root), capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, _unver(f"verifier could not run: {exc}")
    if proc.returncode != 0:
        return None, _unver(f"verifier exited {proc.returncode}")
    lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    if not lines:
        return None, _unver("verifier produced no parsable output")
    return proc.returncode, lines[-1]
def _collect_row(row, root, matches, tol_override):
    """Tier-2 for one tier-1-green row -> verdict dict (g06 s3 tier 2)."""
    verifier, timeout = row.get("verifier"), float(row.get("verifier_timeout", 600))
    if row.get("schema") == V1_SCHEMA:
        if isinstance(verifier, dict) and verifier.get("type") == "delegate_tool":
            argv = (verifier.get("args") or {}).get("cmd")
            if not isinstance(argv, list) or not argv:
                return _unver("verifier delegate_tool has no cmd argv")
            rc, payload = _run_argv(argv, root, timeout)
            if rc is None:
                return payload
            bar = verifier.get("bar") or {}
            if rc == 0:
                return {"ok": True, "verdict": "OK", "exit": 0, "reason": "delegate verifier exited 0"}
            if rc == 1:
                return {"ok": False, "verdict": "CONTRADICTED", "exit": 1, "reason": f"delegate verifier exited 1: {bar.get('exit_1', 'red')}"}
            return _unver(f"delegate verifier exited {rc}: {bar.get('exit_2', 'cannot-verify')}")
        kind = verifier.get("type") if isinstance(verifier, dict) else type(verifier).__name__
        return _unver(f"deep check for verifier type {kind!r} not implemented in v0; run the row's owner command (fail-closed, never a guess)")
    if not isinstance(verifier, list) or not verifier:
        return _unver("row has no verifier argv; --collect is UNVERIFIABLE (never a silent pass)")
    rc, tail = _run_argv(verifier, root, timeout)
    if rc is None:
        return tail
    kind = row.get("value_kind", "int")
    if row.get("verifier_regex"):
        found = re.search(row["verifier_regex"], tail)
        if not found or not found.groups():
            return _unver("verifier_regex found no capture in the verifier tail")
        tail = found.group(1)
    elif kind != "text" and not INT_LINE_RE.match(tail):
        return _unver("verifier tail is not an integer (unparsable output)")
    elif kind != "text":
        tail = INT_LINE_RE.match(tail).group(1)
    ms = matches.get(row["_pins"][0]["pin_id"]) or []
    group = int(row.get("claim_group", 1))
    if not ms or group < 1 or group > len(ms[0].groups()):
        return _unver(f"claim_group {group} out of range for the claim regex")
    tol = tol_override if tol_override is not None else row.get("tolerance", 20)
    return verify_patrol(ms[0].group(group), tail, value_kind=kind, tolerance=tol)
def _survey(rows, root, today, args, baseline, deep, suppress):
    """Run tier-1 (+tier-2 when deep) over rows -> result dicts."""
    results = []
    for row in rows:
        rid = row["id"]
        if row.get("enabled") is False:
            results.append({"id": rid, "verdict": "SKIPPED", "exit": 0, "reason": "enabled=false (named every run; never silent)", "evidence": [], "claim_now": None, "growth": None, "fp": None})
            continue
        try:
            verdict, evidence, claim_now, matches = _check_row(row, root, today, args.stale_days)
        except PatrolError as exc:
            verdict, evidence, claim_now, matches = _unver(f"cannot verify: {exc}"), [], None, {}
        if verdict["ok"] and deep:
            verdict = _collect_row(row, root, matches, args.collect_tolerance)
        fp, growth = None, None
        if not verdict["ok"] and verdict["verdict"] in DETAIL:
            rule, detail = DETAIL[verdict["verdict"]]
            fp = fingerprint(rule, rid, detail)
            entry = baseline["accepted"].get(fp) if suppress else None
            if isinstance(entry, dict):
                if entry.get("expires") and str(entry["expires"]) < today.isoformat():
                    evidence.append(f"acceptance {fp} expired {entry['expires']}: re-violating")
                else:
                    verdict = {"ok": True, "verdict": "ACCEPTED", "exit": 0, "reason": f"accepted by {entry.get('by', '?')} ({fp}); cure the claim or re-accept by name"}
                    stamp = entry.get("accepted_claim_text")
                    if isinstance(stamp, str) and stamp != claim_now:
                        growth = "accepted claim text has churned on the carrier; acceptance is a named pause, not an infinite license"
                    day = parse_moment(entry.get("accepted_moment") or "")
                    if day is not None and (today - day).days > int(row.get("stale_days", 7)):
                        growth = (growth or "acceptance has aged past its bar; ") + "re-accept by name or refresh the row"
        results.append({"id": rid, "verdict": verdict["verdict"], "exit": verdict["exit"], "reason": verdict["reason"], "evidence": evidence, "claim_now": claim_now, "growth": growth, "fp": fp})
    return results
def _print_results(results, head):
    print(head)
    for res in results:
        print(f"  {res['id']}: {res['verdict']} - {res['reason']}")
        for line in res["evidence"]:
            print(f"    {line}")
        if res["growth"]:
            print(f"    GROWTH: {res['id']} - {res['growth']}")
def _aggregate(results, ledger):
    for prefix, code, pred in ((UNVER_PREFIX, 2, lambda r: r["exit"] == 2),
                               ("CLAIM-PATROL: CONTRADICTED", 1, lambda r: r["exit"] == 1 and r["verdict"] == "CONTRADICTED"),
                               ("CLAIM-PATROL: STALE", 1, lambda r: r["exit"] == 1 and r["verdict"] == "STALE")):
        bucket = [r for r in results if pred(r)]
        if bucket:
            return code, f"{prefix} - {bucket[0]['id']}: {bucket[0]['reason']}"
    green = sum(1 for r in results if r["verdict"] != "SKIPPED")
    return 0, f"{OK_PREFIX} - {len(results)} claims checked, {green} green (ledger {ledger})"
def _baseline_file(path, data=None) -> dict:
    """Load (data=None) or save the accept-by-name baseline map."""
    p = Path(path)
    if data is None:
        if not p.is_file():
            return {"version": 1, "updated": None, "accepted": {}}
        try:
            loaded = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise PatrolError(f"baseline {p} unparseable ({exc.msg})") from None
        if not isinstance(loaded, dict) or not isinstance(loaded.get("accepted", {}), dict):
            raise PatrolError(f"baseline {p}: must be an object with an accepted map")
        loaded.setdefault("accepted", {})
        return loaded
    p.parent.mkdir(parents=True, exist_ok=True)
    data["version"] = data.get("version", 1)
    data["updated"] = datetime.now().isoformat(timespec="seconds")
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="claim_drift_patrol")
    for flag, kw in [("--root", dict(default=None)), ("--ledger", dict(default=None)), ("--check", dict(action="store_true")),
                     ("--collect", dict(action="store_true")), ("--baseline-update", dict(action="store_true")), ("--prune", dict(action="store_true")),
                     ("--by", dict(default=None)), ("--note", dict(default="")), ("--id", dict(dest="ids", action="append")),
                     ("--stale-days", dict(type=int, default=None)), ("--collect-tolerance", dict(type=int, default=None)), ("--baseline", dict(default=None))]:
        ap.add_argument(flag, **kw)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ESTATE_ROOT
    ledger = Path(args.ledger) if args.ledger else root / LEDGER_DEFAULT
    baseline_path = Path(args.baseline) if args.baseline else root / BASELINE_DEFAULT
    today = date.today()
    try:
        rows = load_ledger(ledger)
        baseline = _baseline_file(baseline_path)
    except PatrolError as exc:
        print(f"{UNVER_PREFIX} - {exc}")
        return 2
    if args.ids:
        unknown = [i for i in args.ids if i not in {r["id"] for r in rows}]
        if unknown:
            print(f"{UNVER_PREFIX} - unknown --id {unknown[0]!r} in ledger {ledger}")
            return 2
        wanted = set(args.ids)
        rows = [r for r in rows if r["id"] in wanted]
    if args.baseline_update:
        if not args.by:
            print(f"{UNVER_PREFIX} - --baseline-update requires --by WHO (accept-by-name law)")
            return 2
        results = _survey(rows, root, today, args, baseline, deep=False, suppress=False)
        reds = [r for r in results if r["exit"] == 1]
        for res in reds:
            rule, detail = DETAIL[res["verdict"]]
            entry = {"rule": rule, "id": res["id"], "detail": detail, "by": args.by, "note": args.note, "accepted_moment": today.isoformat(), "accepted_claim_text": res["claim_now"]}
            baseline["accepted"][fingerprint(rule, res["id"], detail)] = entry
        _baseline_file(baseline_path, baseline)
        _print_results(results, f"CLAIM-PATROL: baseline updated - {len(reds)} red row(s) accepted by {args.by} into {baseline_path}")
        return 0
    if args.prune:
        results = _survey(rows, root, today, args, baseline, deep=False, suppress=False)
        red_fps = {r["fp"] for r in results if r["exit"] == 1 and r["fp"]}
        before = len(baseline["accepted"])
        baseline["accepted"] = {fp: e for fp, e in baseline["accepted"].items() if fp in red_fps}
        _baseline_file(baseline_path, baseline)
        _print_results(results, f"CLAIM-PATROL: pruned {before - len(baseline['accepted'])} accepted row(s) no longer re-derivable as red from {baseline_path}")
        return 0
    results = _survey(rows, root, today, args, baseline, deep=bool(args.collect), suppress=True)
    code, head = _aggregate(results, ledger)
    _print_results(results, head)
    return code
if __name__ == "__main__":
    sys.exit(main())
