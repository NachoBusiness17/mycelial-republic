"""overmind_verbs - THE ESTATE VERB TABLE (OVERMIND-2 gap 2, 2026-10-01).

Spec: watch/inbox/model_garden/OVERMIND_THEORY.md sec 1.1 (liquids row),
sec 2.2 step 4, sec 7 gap 2 - LM3 proved registered staged verbs, fail-closed
UNKNOWN_VERB, zero side effects, the loop is just another session under the
law. Lane order OVERMIND-2 fixes the minimal set:
  STAGE_ASK / PROMOTE_TICKET / ALERT / NOOP-with-reason.
Laws here: the table is frozen (tests pin it); validate_verb is the gate
(anything unregistered raises UnauthorizedVerb BEFORE any effect);
execute_verb writers take NO path argument - destinations are module
constants, so a payload can never redirect a write (surface fence);
every executed verb is read-back verified (trust bytes, not reports).
Promotion authority stays with the operator (SHARED_SURFACE_CONTRACT:
model text can propose; only the effect broker authorizes effects).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RUN_DIR = ROOT / "memory" / "runs" / "overmind"
PROPOSALS = RUN_DIR / "proposals.jsonl"
STAGED_DIR = RUN_DIR / "staged_asks"
ATTENTION = ROOT / "memory" / "attention.md"

# Staged asks are fireable by any seat through tools/model_garden.py; the
# cheap sensing family carries them when a seat picks the ask up
# (driving ladder law: sensing stays cheap).
STAGED_ASK_MODEL = "deepseek-chat"
STAGED_ASK_BASE_ENV = "DEEPSEEK_API_KEY"
STAGED_ASK_BASE_URL = "https://api.deepseek.com"

VERB_TABLE = {
    "STAGE_ASK": {"payload_fields": {"target": "relative repo path or topic",
                                     "ask": "one-sentence reviewer ask"}},
    "PROMOTE_TICKET": {"payload_fields": {"target": "candidate or ticket id",
                                          "justification": "one line"}},
    "ALERT": {"payload_fields": {"message": "one operator-readable line"}},
    "NOOP": {"payload_fields": {}},
}
REASON_MIN, REASON_MAX = 3, 300
MSG_MAX, ASK_MAX, TARGET_MAX = 240, 400, 160
# payload keys tolerated but NEVER honored (fence probes die silently here)
_ALLOWED_EXTRA = {"path", "file"}


class UnauthorizedVerb(Exception):
    """Fail-closed verb gate: the reply asked for something not in the table."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_verb(decision: dict) -> str:
    """The frozen-table law. Returns the verb name or raises
    UnauthorizedVerb with zero side effects."""
    if not isinstance(decision, dict):
        raise UnauthorizedVerb(f"decision is not an object: {decision!r}")
    verb = decision.get("verb")
    if not isinstance(verb, str) or verb not in VERB_TABLE:
        raise UnauthorizedVerb(
            f"UNKNOWN_VERB {verb!r}: not in the frozen table "
            f"{sorted(VERB_TABLE)}; fail-closed, zero side effects")
    reason = str(decision.get("reason") or "").strip()
    if not (REASON_MIN <= len(reason) <= REASON_MAX):
        raise UnauthorizedVerb(
            f"verb {verb}: reason must be {REASON_MIN}-{REASON_MAX} chars "
            f"(a NOOP without a reason is the still-world trap); got "
            f"{len(reason)}")
    payload = decision.get("payload")
    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        raise UnauthorizedVerb(f"verb {verb}: payload must be an object")
    spec = VERB_TABLE[verb]["payload_fields"]
    for key in set(payload) - set(spec) - _ALLOWED_EXTRA:
        raise UnauthorizedVerb(
            f"verb {verb}: unknown payload field {key!r} (allowed: "
            f"{sorted(spec)})")
    for field in spec:
        val = str(payload.get(field) or "").strip()
        cap = {"message": MSG_MAX, "ask": ASK_MAX,
               "target": TARGET_MAX}.get(field, 200)
        if not val:
            raise UnauthorizedVerb(f"verb {verb}: payload field {field!r} "
                                   f"is required and non-empty")
        if len(val) > cap:
            raise UnauthorizedVerb(f"verb {verb}: payload field {field!r} "
                                   f"over {cap} chars")
        if "\n" in val:
            raise UnauthorizedVerb(f"verb {verb}: payload field {field!r} "
                                   f"must be single-line")
        if field == "target" and (val.startswith(("/", "\\", "C:")) or
                                  ".." in val):
            raise UnauthorizedVerb(
                f"verb STAGE_ASK: target must be a relative repo path, "
                f"got {val!r}")
    return verb


def _tick_alert_id(ctx: dict) -> str:
    return f"overmind-alert-{ctx.get('run_id', 'run')}-t{ctx.get('tick', 0)}"


def _proposal_id(ctx: dict) -> str:
    return f"overmind-prop-{ctx.get('run_id', 'run')}-t{ctx.get('tick', 0)}"


def execute_verb(verb: str, payload: dict, ctx: dict) -> dict:
    """Execute ONE registered verb against its sanctioned constant surface.
    Unknown verbs raise; nothing else happens (fail-closed executor)."""
    if verb not in VERB_TABLE:
        raise UnauthorizedVerb(
            f"UNKNOWN_VERB {verb!r}: executor refuses, zero side effects")
    payload = payload or {}
    if verb == "NOOP":
        return {"verb": "NOOP", "executed": False, "verified": True}
    if verb == "ALERT":
        marker = _tick_alert_id(ctx)
        block = (f"\n---\n\n### OVERMIND ALERT {marker}\n\n"
                 f"- ts: {_now()}\n"
                 f"- tick: {ctx.get('tick')} of run {ctx.get('run_id')}\n"
                 f"- message: {str(payload['message']).strip()}\n")
        ATTENTION.parent.mkdir(parents=True, exist_ok=True)
        with open(ATTENTION, "a", encoding="utf-8") as fh:
            fh.write(block)
        text = ATTENTION.read_text(encoding="utf-8", errors="replace")
        return {"verb": "ALERT", "executed": True,
                "verified": marker in text, "surface": str(ATTENTION),
                "artifact": marker}
    if verb == "STAGE_ASK":
        target = str(payload["target"]).strip()
        ask_line = str(payload["ask"]).strip()
        ask_dir = STAGED_DIR / f"{ctx.get('run_id', 'run')}-t{ctx.get('tick', 0)}"
        ask_dir.mkdir(parents=True, exist_ok=True)
        evidence, self_contained = [], True
        rel = target.replace("\\", "/")
        if (ROOT / rel).is_file():
            evidence, self_contained = [rel], False
        meta = {
            "id": f"omstaged-{ctx.get('run_id', 'run')}-t{ctx.get('tick', 0)}",
            "model": STAGED_ASK_MODEL,
            "base_env": STAGED_ASK_BASE_ENV,
            "base_url": STAGED_ASK_BASE_URL,
            "contract": (
                f"STAGED BY THE OVERMIND LOOP (tick {ctx.get('tick')}, run "
                f"{ctx.get('run_id')}); a seat decides whether to fire it.\n"
                f"Target: {target}\n"
                f"Reviewer task: {ask_line}\n"
                f"Ground every claim in the evidence bytes; cite path:line; "
                f"no em-dashes; drop any claim you cannot ground."),
            "evidence": evidence,
            "self_contained": self_contained,
        }
        (ask_dir / "ask.json").write_text(
            json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
        back = json.loads((ask_dir / "ask.json").read_text(encoding="utf-8"))
        ok = all(back.get(f) for f in
                 ("id", "model", "base_env", "base_url", "contract"))
        return {"verb": "STAGE_ASK", "executed": True, "verified": bool(ok),
                "surface": str(ask_dir), "artifact": ask_dir.name}
    if verb == "PROMOTE_TICKET":
        row = {"schema": "overmind.proposal.v1", "id": _proposal_id(ctx),
               "ts": _now(), "tick": ctx.get("tick"),
               "run_id": ctx.get("run_id"),
               "target": str(payload["target"]).strip(),
               "justification": str(payload["justification"]).strip(),
               "authority": "operator-human-gate",
               "note": "model text proposes; only the operator applies"}
        PROPOSALS.parent.mkdir(parents=True, exist_ok=True)
        with open(PROPOSALS, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        found = any(
            json.loads(l).get("id") == row["id"]
            for l in PROPOSALS.read_text(encoding="utf-8",
                                         errors="replace").splitlines()
            if l.strip())
        return {"verb": "PROMOTE_TICKET", "executed": True,
                "verified": bool(found), "surface": str(PROPOSALS),
                "artifact": row["id"]}
    raise UnauthorizedVerb(f"UNKNOWN_VERB {verb!r}")  # unreachable fence
