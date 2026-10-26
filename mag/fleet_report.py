"""fleet_report: the fleet_report.v1 SALUTE-style report + notices channel (2026-10-17).

Doctrine: watch/LIBRARY/FLEET_COORDINATION_DOCTRINE_20261017.md (P8 report
format, P4 notices). Nothing new is transported: a report is the BODY of an
ordinary shared receipt (estate_bridge.shared_receipt_append ->
watch/receipts/seat_*.json). The receipt writer calls check_body() on every
body, so a body that claims schema fleet_report.v1 and fails validation is
REFUSED before a byte lands (code-is-law: the format lives in the writer, not
in a reviewer).

Kinds: SPOTREP (SALUTE: size, activity, location, unit, time, equipment),
SITREP (status, readiness), NOTICE (hazard in force until cancelled),
RELIEF (watch turnover, "I stand relieved"), ACK (read-back of a notice or a
receipt).

Schema: configs/fleet_report.v1.schema.json (JSON Schema 2020-12). The venv
has no jsonschema package (stdlib law), so validate() interprets exactly the
subset that file uses: const, enum, type string/array, maxLength, pattern,
minItems/maxItems/items, required, additionalProperties false, and the
allOf if-kind-then-required blocks. One source of truth: the file.

Names-only law: any string field whose text changes under
warm_surface.redact_text (a secret-shaped value) is REFUSED, so a NOTICE about a
key can carry the key NAME but never its value.

Notices: notices() scans watch/receipts/seat_*.json for NOTICE / ACK bodies.
A notice stays in force until a later NOTICE carries cancels=<notice_id> or
its in_force_until (ISO UTC) passes; "until_cancelled" never lapses. Served at
mag://warm/notices (mag/warm_surface.py) with each notice's ACK list.

Schema: fleet_report.v1 · stdlib only
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "fleet_report.v1"
SCHEMA_PATH = ROOT / "configs" / "fleet_report.v1.schema.json"
RECEIPTS_DIR = ROOT / "watch" / "receipts"
KINDS = ("SPOTREP", "SITREP", "NOTICE", "RELIEF", "ACK")
SCAN_CAP = 5000  # newest seat_*.json receipts scanned for notices/acks

_SCHEMA_CACHE: dict[str, Any] = {}


class ReportInvalid(ValueError):
    """A body that claims fleet_report.v1 but fails the schema."""


def load_schema() -> dict[str, Any]:
    """The JSON Schema document (cached per mtime)."""
    try:
        mtime = SCHEMA_PATH.stat().st_mtime
    except OSError as e:
        raise ReportInvalid(f"fleet_report schema missing: {SCHEMA_PATH.name}") from e
    if _SCHEMA_CACHE.get("mtime") != mtime or _SCHEMA_CACHE.get("path") != str(SCHEMA_PATH):
        _SCHEMA_CACHE.update(mtime=mtime, path=str(SCHEMA_PATH),
                             doc=json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    return _SCHEMA_CACHE["doc"]


def now_dtg() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_dt(value: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    if dt.tzinfo is None:
        return None  # UTC must be explicit
    return dt


def _secret_shaped(text: str) -> bool:
    from mag.warm_surface import redact_text

    return redact_text(text) != text


def _check_prop(name: str, value: Any, spec: dict[str, Any], errors: list[str]) -> None:
    if "const" in spec and (value != spec["const"] or type(value) is not type(spec["const"])):
        errors.append(f"{name}: must be {spec['const']!r}")
        return
    if "enum" in spec and value not in spec["enum"]:
        errors.append(f"{name}: must be one of {spec['enum']}")
        return
    typ = spec.get("type")
    if typ == "string":
        if not isinstance(value, str):
            errors.append(f"{name}: must be a string")
            return
        if "maxLength" in spec and len(value) > spec["maxLength"]:
            errors.append(f"{name}: longer than {spec['maxLength']} chars")
        if "pattern" in spec and not re.fullmatch(spec["pattern"], value):
            errors.append(f"{name}: does not match {spec['pattern']}")
        if spec.get("format") == "date-time" and _parse_dt(value) is None:
            errors.append(f"{name}: must be ISO 8601 with an explicit zone (UTC)")
        if _secret_shaped(value):
            errors.append(f"{name}: secret-shaped or host-path value refused (names only, never values)")
    elif typ == "array":
        if not isinstance(value, list):
            errors.append(f"{name}: must be a list")
            return
        if len(value) < spec.get("minItems", 0):
            errors.append(f"{name}: needs at least {spec['minItems']} item(s)")
        if "maxItems" in spec and len(value) > spec["maxItems"]:
            errors.append(f"{name}: more than {spec['maxItems']} items")
        item_spec = spec.get("items") or {}
        for i, item in enumerate(value):
            _check_prop(f"{name}[{i}]", item, item_spec, errors)


def validate(report: Any) -> list[str]:
    """Return a list of error strings ([] = valid fleet_report.v1)."""
    if not isinstance(report, dict):
        return ["report must be a JSON object"]
    doc = load_schema()
    props: dict[str, Any] = doc.get("properties") or {}
    errors: list[str] = []
    for key in doc.get("required") or []:
        if key not in report:
            errors.append(f"missing required field: {key}")
    if doc.get("additionalProperties") is False:
        extra = sorted(k for k in report if k not in props)
        if extra:
            errors.append(f"unknown field(s): {extra}")
    for key, value in report.items():
        if key in props:
            _check_prop(key, value, props[key], errors)
    kind = report.get("kind")
    for block in doc.get("allOf") or []:
        cond = ((block.get("if") or {}).get("properties") or {}).get("kind") or {}
        if "const" in cond and cond["const"] == kind:
            for key in (block.get("then") or {}).get("required") or []:
                if key not in report:
                    errors.append(f"{kind} requires field: {key}")
    if kind == "NOTICE" and isinstance(report.get("in_force_until"), str):
        v = report["in_force_until"]
        if v != "until_cancelled" and _parse_dt(v) is None:
            errors.append("in_force_until: ISO 8601 UTC or 'until_cancelled'")
    return errors


def canonical_body(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=1)


def check_body(body: str, seat: str | None = None) -> dict[str, Any] | None:
    """Receipt-writer hook. None = not a fleet report (plain receipt, allowed).

    A body that parses as a JSON object whose schema starts with fleet_report
    is validated against fleet_report.v1; failure raises ReportInvalid (a ValueError,
    so mcp_server returns in-band isError and nothing lands). The report's
    seat must equal the receipt's seat. Returns a small index record.
    """
    text = body.strip() if isinstance(body, str) else ""
    if not text.startswith("{"):
        return None
    try:
        obj = json.loads(text)
    except ValueError:
        return None
    if not isinstance(obj, dict):
        return None
    if not str(obj.get("schema", "")).startswith("fleet_report"):
        return None  # ordinary JSON receipt; only a body CLAIMING the schema is judged
    errors = validate(obj)
    if seat is not None and obj.get("seat") != seat:
        errors.append(f"seat: report seat {obj.get('seat')!r} != receipt seat {seat!r}")
    if errors:
        raise ReportInvalid("fleet_report.v1 refused: " + "; ".join(errors))
    index = {"schema": SCHEMA, "kind": obj["kind"], "dtg": obj["dtg"]}
    for key in ("notice_id", "cancels", "ack_of", "category"):
        if key in obj:
            index[key] = obj[key]
    return index


def build_report(kind: str, seat: str, fields: dict[str, Any], *,
                 model: str = "", dtg: str | None = None) -> dict[str, Any]:
    """Fill schema/kind/dtg/seat(/model) around caller fields; no validation."""
    report: dict[str, Any] = {k: v for k, v in (fields or {}).items() if v is not None}
    report.update(schema=SCHEMA, kind=str(kind).upper(), seat=seat,
                  dtg=dtg or report.get("dtg") or now_dtg())
    if model and "model" not in report:
        report["model"] = model
    return report


def file_report(*, seat: str, kind: str, report: dict[str, Any] | None = None,
                model: str = "", title: str = "", **refused: Any) -> dict[str, Any]:
    """File ONE fleet_report.v1 (SPOTREP/SITREP/NOTICE/RELIEF/ACK) as a shared receipt.

    The server fills schema, kind, dtg and seat; `report` carries the kind's
    fields. Invalid reports are refused (nothing lands). Lands under
    watch/receipts/ via estate_bridge.shared_receipt_append (server-named,
    exclusive-create, redacted).
    """
    if refused:
        raise ValueError(f"estate_fleet_report takes seat/kind/report/model/title only; "
                         f"refused: {sorted(refused)}")
    if isinstance(report, str):
        try:
            report = json.loads(report)
        except ValueError as e:
            raise ValueError("report must be a JSON object") from e
    if report is not None and not isinstance(report, dict):
        raise ValueError("report must be a JSON object")
    if str(kind).upper() not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    full = build_report(kind, seat, report or {}, model=model)
    errors = validate(full)
    if errors:
        raise ReportInvalid("fleet_report.v1 refused: " + "; ".join(errors))
    if not title:
        head = full.get("notice_id") or full.get("subject") or full.get("activity") \
            or full.get("ack_of") or full.get("status") or ""
        title = f"{full['kind']} {head}".strip()[:200]
    from mag.estate_bridge import shared_receipt_append

    out = shared_receipt_append(seat=seat, body=canonical_body(full), model=model, title=title)
    out["fleet_report"] = {"kind": full["kind"], "dtg": full["dtg"],
                           **({"notice_id": full["notice_id"]} if "notice_id" in full else {})}
    return out


# ─────────────────────────────── notices channel ───────────────────────────

def _iter_reports(receipts_dir: Path | None = None):
    d = receipts_dir or RECEIPTS_DIR
    try:
        files = sorted(d.glob("seat_*.json"))[-SCAN_CAP:]
    except OSError:
        return
    for path in files:
        try:
            rec = json.loads(path.read_text(encoding="utf-8"))
            obj = json.loads(rec.get("body") or "")
        except (OSError, ValueError, TypeError):
            continue
        if isinstance(obj, dict) and obj.get("schema") == SCHEMA and obj.get("kind") in KINDS:
            yield path, rec, obj


def notices(receipts_dir: Path | None = None, now: datetime | None = None) -> dict[str, Any]:
    """Notices in force (newest first) with ACKs; cancelled/lapsed listed briefly."""
    now = now or datetime.now(timezone.utc)
    filed: dict[str, dict[str, Any]] = {}
    cancelled: dict[str, dict[str, Any]] = {}
    acks: dict[str, list[dict[str, Any]]] = {}
    for path, rec, obj in _iter_reports(receipts_dir):
        if obj["kind"] == "NOTICE":
            nid = obj.get("notice_id")
            if nid and nid not in filed:  # first filing wins; re-filing needs a new id
                filed[nid] = {"notice": obj, "receipt": f"watch/receipts/{path.name}"}
            if obj.get("cancels"):
                cancelled[obj["cancels"]] = {"by": nid, "dtg": obj.get("dtg"),
                                             "seat": obj.get("seat")}
        elif obj["kind"] == "ACK":
            acks.setdefault(str(obj.get("ack_of")), []).append(
                {"seat": obj.get("seat"), "dtg": obj.get("dtg"), "note": obj.get("note", ""),
                 "receipt": f"watch/receipts/{path.name}"})
    in_force, closed = [], []
    for nid, item in filed.items():
        n = item["notice"]
        until = n.get("in_force_until")
        lapsed = False
        if until and until != "until_cancelled":
            dt = _parse_dt(until)
            lapsed = dt is not None and dt <= now
        row = {"notice_id": nid, "category": n.get("category"), "subject": n.get("subject"),
               "affects": n.get("affects"), "action_required": n.get("action_required"),
               "names": n.get("names", []), "in_force_until": until,
               "filed_by": n.get("seat"), "dtg": n.get("dtg"), "receipt": item["receipt"],
               "acks": acks.get(nid, [])}
        if n.get("cancels"):
            row["cancels"] = n["cancels"]
        if nid in cancelled:
            closed.append({**row, "state": "cancelled", "cancelled_by": cancelled[nid]})
        elif lapsed:
            closed.append({**row, "state": "lapsed"})
        else:
            in_force.append({**row, "state": "in_force"})
    in_force.sort(key=lambda r: str(r.get("dtg")), reverse=True)
    closed.sort(key=lambda r: str(r.get("dtg")), reverse=True)
    return {
        "ok": True, "schema": "fleet_notices.v1", "read_at": now.isoformat(),
        "in_force_count": len(in_force), "in_force": in_force, "closed_recent": closed[:20],
        "ack_how": "estate_fleet_report(seat=<you>, kind=\"ACK\", report={\"ack_of\": \"<notice_id>\"}) "
                   "or: python scripts/fleet_report.py ack --seat <you> --of <notice_id>",
        "cancel_how": "file a NOTICE with cancels=<notice_id> (a cancellation is a new notice, never an edit)",
    }


def tool_notices() -> dict[str, Any]:
    """Read the fleet notices in force (until cancelled) with their ACKs; read-only."""
    return notices()


# ─────────────────────────────── MCP input schema ──────────────────────────
INPUT_SCHEMAS: dict[str, Any] = {
    "estate_fleet_report": {
        "type": "object",
        "properties": {
            "seat": {"type": "string", "pattern": r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,31}$",
                     "description": "your seat name (grok, gemini, deepseek, zcode, hermes, free...)"},
            "kind": {"type": "string", "enum": list(KINDS)},
            "report": {"type": "object",
                       "description": "the kind's fields per configs/fleet_report.v1.schema.json; "
                                      "SPOTREP: size, activity, location, unit, time, equipment; "
                                      "SITREP: status, readiness; NOTICE: notice_id, category, subject, "
                                      "affects[], action_required, in_force_until; RELIEF: status, "
                                      "outstanding, leases[], stand_relieved=true; ACK: ack_of. "
                                      "schema/kind/dtg/seat are filled by the server"},
            "model": {"type": "string", "description": "model id you are running as (optional)"},
            "title": {"type": "string", "maxLength": 200},
        },
        "required": ["seat", "kind", "report"],
        "description": "files ONE validated fleet_report.v1 under watch/receipts/ (invalid = refused); "
                       "names only, secret-shaped values refused",
    },
    "estate_notices": {"type": "object", "properties": {},
                       "description": "read-only: notices in force + ACKs (same as mag://warm/notices)"},
}
