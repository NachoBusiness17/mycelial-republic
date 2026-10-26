"""proposals: signed seat-to-seat branch proposals over watch/receipts (2026-10-17).

A small protocol so seats (Grok, Gemini, DeepSeek, ZCode, Hermes, free models)
can propose changes to each other and reach a quorum WITHOUT any of them
touching git. Three message kinds, each Ed25519-signed with the seat's
handshake key (mag/seat_handshake.py, allowlist configs/seat_allowlist.json):

  proposal   {seat, title, targets[], diff | patch_path, rationale, created}
  review     {proposal_id, seat, verdict: approve|reject, reason, created}
  promotion  {proposal_id, seat, state: "ready", tally, created}

Storage (append-only, exclusive-create, never overwritten, never deleted):

  watch/receipts/proposals/<id>/proposal.json
  watch/receipts/proposals/<id>/review_<seat>_<utc>_<nonce8>.json
  watch/receipts/proposals/<id>/promotion_<utc>_<nonce8>.json

  <id> = p_<utc YYYYmmddTHHMMSSZ>_<sha256(canonical payload)[:12]>

SIGNED BYTES: seat_handshake.canonical(kind, canonical_json(payload), seat_id,
ts, nonce); payload.seat must equal the signing seat. Submission also checks
the 60 s skew; stored messages are re-verified (signature + allowlist, no
clock) on every tally, so a revoked seat's votes stop counting.

QUORUM (tally): latest verdict per DISTINCT allowlisted seat, author
excluded; duplicate votes from one seat count once. ready = approvals >=
quorum.default (default 2) OR an approve from an operator_seats member
(operator override), and no reject from an operator seat. promote() writes a
promotion marker ONLY when tally says ready. Nothing here applies a diff,
checks out a branch or merges: git belongs to the operator's git window.

NON-GLM RULE (2026-10-17, harness2): with quorum.require_non_glm_approval
(configs/seat_allowlist.json; default true when absent) ready ALSO needs at
least one approver that is not a leave-protocol mate (seat id not "mate:*")
and whose allowlist row model_family is not GLM. Mates may vote, but a
room of GLM mates can never adopt its own change alone. Seat ids with a
colon are stored under seat_slug() filenames.

Schema: seat_proposal.v1 · stdlib + mag.seat_handshake
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mag import seat_handshake as sh

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS_DIR = ROOT / "watch" / "receipts" / "proposals"
SCHEMA = "seat_proposal.v1"
ID_RE = re.compile(r"^p_[0-9]{8}T[0-9]{6}Z_[0-9a-f]{12}$")
KINDS = ("proposal", "review", "promotion")
DIFF_CAP = 262144        # bytes of inline diff
TEXT_CAP = 4000          # rationale / reason
TITLE_CAP = 200
MAX_TARGETS = 50
DEFAULT_QUORUM = 2


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


# ─────────────────────────────── validation ───────────────────────────────

def _rel_ok(p: Any) -> bool:
    if not isinstance(p, str) or not p or len(p) > 300:
        return False
    s = p.replace("\\", "/")
    if s.startswith("/") or re.match(r"^[A-Za-z]:", s) or "\n" in s:
        return False
    return ".." not in s.split("/")


def _denied(p: str) -> bool:
    from mag.deepseek_direct_runner import is_denied

    return is_denied(p) is not None


def _secret_hits(text: str) -> dict[str, int]:
    from mag.deepseek_direct_runner import redact_lines

    _, counts = redact_lines(text.splitlines())
    return counts


def validate_payload(kind: str, payload: Any) -> None:
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    seat = payload.get("seat")
    if not isinstance(seat, str) or not sh.SEAT_RE.fullmatch(seat):
        raise ValueError("payload.seat invalid")
    if not isinstance(payload.get("created"), str):
        raise ValueError("payload.created (ISO time) required")
    if kind == "proposal":
        allowed = {"seat", "title", "targets", "diff", "patch_path", "rationale", "created"}
        extra = set(payload) - allowed
        if extra:
            raise ValueError(f"unknown proposal fields: {sorted(extra)}")
        title = payload.get("title")
        if not isinstance(title, str) or not title.strip() or len(title) > TITLE_CAP:
            raise ValueError(f"title required, <= {TITLE_CAP} chars")
        targets = payload.get("targets")
        if (not isinstance(targets, list) or not targets or len(targets) > MAX_TARGETS
                or not all(_rel_ok(t) for t in targets)):
            raise ValueError("targets must be 1-50 repo-relative paths (no absolute, no ..)")
        if any(_denied(t) for t in targets):
            raise ValueError("a target is on the secret denylist")
        diff, patch = payload.get("diff", ""), payload.get("patch_path", "")
        if not isinstance(diff, str) or not isinstance(patch, str):
            raise ValueError("diff / patch_path must be text")
        if bool(diff) == bool(patch):
            raise ValueError("exactly one of diff or patch_path is required")
        if diff:
            if len(diff.encode("utf-8")) > DIFF_CAP:
                raise ValueError(f"diff exceeds {DIFF_CAP} bytes; file it and pass patch_path")
            if _secret_hits(diff):
                raise ValueError("diff trips the secret scanner; refused")
        if patch and (not _rel_ok(patch) or _denied(patch)):
            raise ValueError("patch_path must be a repo-relative, non-denied path")
        rat = payload.get("rationale", "")
        if not isinstance(rat, str) or len(rat) > TEXT_CAP or _secret_hits(rat):
            raise ValueError(f"rationale must be text <= {TEXT_CAP} chars, no secrets")
    else:
        if not isinstance(payload.get("proposal_id"), str) or not ID_RE.fullmatch(payload["proposal_id"]):
            raise ValueError("proposal_id invalid")
        if kind == "review":
            allowed = {"seat", "proposal_id", "verdict", "reason", "created"}
            if set(payload) - allowed:
                raise ValueError(f"unknown review fields: {sorted(set(payload) - allowed)}")
            if payload.get("verdict") not in ("approve", "reject"):
                raise ValueError("verdict must be approve or reject")
            reason = payload.get("reason", "")
            if not isinstance(reason, str) or len(reason) > TEXT_CAP or _secret_hits(reason):
                raise ValueError(f"reason must be text <= {TEXT_CAP} chars, no secrets")
        else:
            if payload.get("state") != "ready":
                raise ValueError("promotion state must be 'ready'")


# ─────────────────────────────── signing ──────────────────────────────────

def sign_message(kind: str, payload: dict[str, Any], *, key_path: str | Path | None = None,
                 seed: bytes | None = None, seat_id: str | None = None,
                 now: float | None = None) -> dict[str, Any]:
    """Client side: {"schema", "kind", "payload", "sig"} ready to submit."""
    if seed is None:
        seat_id, seed = sh.load_key(key_path)
    payload = dict(payload)
    payload.setdefault("seat", seat_id)
    payload.setdefault("created", _now_iso())
    if payload["seat"] != seat_id:
        raise ValueError("payload.seat must be the signing seat")
    validate_payload(kind, payload)
    fields = sh.sign_request(kind, canonical_json(payload), seed=seed, seat_id=seat_id, now=now)
    return {"schema": SCHEMA, "kind": kind, "payload": payload, "sig": fields}


def verify_message(msg: Any, allowlist: dict[str, Any], *, now: float | None = None,
                   skew_s: int | None = None) -> str:
    """seat_id when valid; raises ValueError otherwise. skew_s=None skips the clock."""
    if not isinstance(msg, dict) or msg.get("schema") != SCHEMA:
        raise ValueError("not a seat proposal message")
    kind, payload, fields = msg.get("kind"), msg.get("payload"), msg.get("sig")
    validate_payload(kind, payload)
    if not isinstance(fields, dict):
        raise ValueError("sig missing")
    seat = sh.verify_signature(kind, canonical_json(payload), fields, allowlist)
    if seat is None or seat != payload.get("seat"):
        raise ValueError("signature invalid, seat unknown, or seat mismatch")
    if skew_s is not None:
        t = time.time() if now is None else now
        if abs(t - int(fields["ts"])) > skew_s:
            raise ValueError("timestamp outside skew window")
    return seat


# ─────────────────────────────── storage ──────────────────────────────────

def _root(root: str | Path | None) -> Path:
    return Path(root) if root else PROPOSALS_DIR


def _pdir(pid: str, root: str | Path | None = None) -> Path:
    if not isinstance(pid, str) or not ID_RE.fullmatch(pid):
        raise ValueError("invalid proposal id")
    base = _root(root).resolve()
    d = (base / pid).resolve()
    if d.parent != base:
        raise ValueError("proposal path escapes watch/receipts/proposals/")
    return d


def _write_new(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "x", encoding="utf-8", newline="\n") as fh:  # never overwrite
        fh.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")


def _messages(d: Path) -> list[tuple[Path, dict[str, Any]]]:
    out = []
    for p in sorted(d.glob("*.json")):
        try:
            out.append((p, json.loads(p.read_text(encoding="utf-8"))))
        except (OSError, ValueError):
            out.append((p, {}))
    return out


def _nonce_used(d: Path, seat: str, nonce: str) -> bool:
    for _, m in _messages(d) if d.is_dir() else []:
        s = m.get("sig") or {}
        if s.get("seat_id") == seat and s.get("nonce") == nonce:
            return True
    return False


def _allow(allowlist: dict[str, Any] | None) -> dict[str, Any]:
    return allowlist if allowlist is not None else sh.load_allowlist()


def submit(msg: dict[str, Any], *, root: str | Path | None = None,
           allowlist: dict[str, Any] | None = None, now: float | None = None) -> dict[str, Any]:
    """Verify (incl. skew) and file one signed message. Returns where it landed."""
    al = _allow(allowlist)
    seat = verify_message(msg, al, now=now, skew_s=int(al.get("skew_s", sh.DEFAULT_SKEW_S)))
    kind, payload, nonce = msg["kind"], msg["payload"], msg["sig"]["nonce"]
    if kind == "proposal":
        sha = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
        pid = f"p_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{sha[:12]}"
        d = _pdir(pid, root)
        if d.exists():
            raise ValueError("proposal already filed")
        target = d / "proposal.json"
    else:
        pid = payload["proposal_id"]
        d = _pdir(pid, root)
        if not (d / "proposal.json").is_file():
            raise ValueError("no such proposal")
        if _nonce_used(d, seat, nonce):
            raise ValueError("nonce replay")
        if kind == "promotion":
            t = tally(pid, root=root, allowlist=al)
            if not t["ready"]:
                raise ValueError("quorum not met; promotion refused")
        prefix = "review" if kind == "review" else "promotion"
        target = d / f"{prefix}_{sh.seat_slug(seat)}_{_stamp()}_{nonce[:8]}.json"
    if target.resolve().parent != d:
        raise ValueError("message path escapes the proposal folder")
    _write_new(target, msg)
    try:
        rel = target.resolve().relative_to(ROOT.resolve())
    except ValueError:
        rel = Path(pid) / target.name
    return {"ok": True, "kind": kind, "proposal_id": pid, "seat": seat,
            "path": str(rel).replace("\\", "/")}


def require_non_glm_approval(al: dict[str, Any]) -> bool:
    v = (al.get("quorum") or {}).get("require_non_glm_approval", True)
    return not (v is False or (isinstance(v, str) and v.strip().lower() in ("false", "0", "no", "off")))


GROKBOT_PREFIX = "grokbot-"


def grokbot_counts_as_non_glm(al: dict[str, Any]) -> bool:
    """2026-10-18: quorum.grokbot_counts_as_non_glm, default False (opt-in only)."""
    v = (al.get("quorum") or {}).get("grokbot_counts_as_non_glm", False)
    return v is True or (isinstance(v, str) and v.strip().lower() in ("true", "1", "yes", "on"))


def is_grokbot_seat(seat: str, al: dict[str, Any]) -> bool:
    row = (al.get("seats") or {}).get(seat) or {}
    return (str(seat).startswith(GROKBOT_PREFIX)
            or "grokbot" in (str(row.get("kind") or "").lower(), str(row.get("model_family") or "").lower()))


def is_non_glm_seat(seat: str, al: dict[str, Any]) -> bool:
    if str(seat).startswith(sh.MATE_PREFIX):
        return False
    # 2026-10-18: Grok Bot box seats never satisfy the non-GLM rule silently.
    if is_grokbot_seat(seat, al):
        return grokbot_counts_as_non_glm(al)
    row = (al.get("seats") or {}).get(seat) or {}
    return "glm" not in str(row.get("model_family") or "").lower()


def tally(pid: str, *, root: str | Path | None = None,
          allowlist: dict[str, Any] | None = None) -> dict[str, Any]:
    al = _allow(allowlist)
    d = _pdir(pid, root)
    msgs = _messages(d) if d.is_dir() else []
    quorum = int((al.get("quorum") or {}).get("default", DEFAULT_QUORUM))
    operators = set(al.get("operator_seats") or [])
    author, invalid, latest = None, [], {}
    promoted = False
    for path, m in msgs:
        try:
            seat = verify_message(m, al)
        except ValueError:
            invalid.append(path.name)
            continue
        if m["kind"] == "proposal":
            author = seat
        elif m["kind"] == "review" and m["payload"]["proposal_id"] == pid:
            prev = latest.get(seat)
            key = (m["payload"]["created"], path.name)
            if prev is None or key > prev[0]:
                latest[seat] = (key, m["payload"]["verdict"])
        elif m["kind"] == "promotion":
            promoted = True
    votes = {s: v for s, (_, v) in latest.items() if s != author}
    approvers = sorted(s for s, v in votes.items() if v == "approve")
    rejecters = sorted(s for s, v in votes.items() if v == "reject")
    op_approve = any(s in operators for s in approvers)
    op_reject = any(s in operators for s in rejecters)
    need_non_glm = require_non_glm_approval(al)
    non_glm = sorted(s for s in approvers if is_non_glm_seat(s, al))
    non_glm_ok = (not need_non_glm) or bool(non_glm)
    ready = (author is not None and not op_reject
             and (len(approvers) >= quorum or op_approve) and non_glm_ok)
    return {"proposal_id": pid, "author": author, "valid_proposal": author is not None,
            "quorum": quorum, "approvers": approvers, "rejecters": rejecters,
            "distinct_votes": len(votes), "operator_override": op_approve and len(approvers) < quorum,
            "operator_reject": op_reject, "require_non_glm_approval": need_non_glm,
            "non_glm_approvers": non_glm, "non_glm_ok": non_glm_ok,
            "ready": ready, "promoted": promoted,
            "invalid_messages": invalid,
            "note": "ready marks only; nothing is applied or merged (git belongs to the git window)"}


def list_proposals(*, root: str | Path | None = None,
                   allowlist: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    base = _root(root)
    out = []
    if not base.is_dir():
        return out
    for d in sorted(base.iterdir()):
        if not (d.is_dir() and ID_RE.fullmatch(d.name)):
            continue
        t = tally(d.name, root=root, allowlist=allowlist)
        try:
            p = json.loads((d / "proposal.json").read_text(encoding="utf-8"))["payload"]
            title, targets = p.get("title"), p.get("targets")
        except (OSError, ValueError, KeyError, TypeError):
            title, targets = None, None
        out.append({"proposal_id": d.name, "title": title, "targets": targets,
                    "author": t["author"], "approvers": t["approvers"],
                    "rejecters": t["rejecters"], "ready": t["ready"], "promoted": t["promoted"]})
    return out


def show(pid: str, *, root: str | Path | None = None,
         allowlist: dict[str, Any] | None = None) -> dict[str, Any]:
    d = _pdir(pid, root)
    if not (d / "proposal.json").is_file():
        raise ValueError("no such proposal")
    return {"proposal_id": pid, "messages": [m for _, m in _messages(d)],
            "tally": tally(pid, root=root, allowlist=allowlist)}


# ─────────────────────────────── MCP tool wrappers ────────────────────────

def _server_sign(kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Sign with the key of the seat that SPAWNED this stdio server (env path)."""
    if not os.environ.get(sh.ENV_KEY_PATH, "").strip():
        raise ValueError("unsigned call: pass `signed` (a message from scripts/proposals.py sign) "
                         f"or spawn the server with {sh.ENV_KEY_PATH} set to your seat key")
    return sign_message(kind, payload)


def tool_propose(title: str = "", targets: list | None = None, rationale: str = "",
                 diff: str = "", patch_path: str = "", signed: dict | None = None,
                 **refused: Any) -> dict[str, Any]:
    """File a signed proposal under watch/receipts/proposals/ (never applied)."""
    if refused:
        raise ValueError(f"unknown arguments refused: {sorted(refused)}")
    if signed is None:
        payload = {"title": title, "targets": list(targets or []), "rationale": rationale}
        if diff:
            payload["diff"] = diff
        if patch_path:
            payload["patch_path"] = patch_path
        signed = _server_sign("proposal", payload)
    if signed.get("kind") != "proposal":
        raise ValueError("signed message is not a proposal")
    return submit(signed)


def tool_review(proposal_id: str = "", verdict: str = "", reason: str = "",
                signed: dict | None = None, **refused: Any) -> dict[str, Any]:
    """File a signed approve/reject review of one proposal."""
    if refused:
        raise ValueError(f"unknown arguments refused: {sorted(refused)}")
    if signed is None:
        signed = _server_sign("review", {"proposal_id": proposal_id, "verdict": verdict,
                                         "reason": reason})
    if signed.get("kind") != "review":
        raise ValueError("signed message is not a review")
    return submit(signed)


def tool_proposals(action: str = "list", proposal_id: str = "", **refused: Any) -> dict[str, Any]:
    """List proposals, or show/tally one (read-only)."""
    if refused:
        raise ValueError(f"unknown arguments refused: {sorted(refused)}")
    if action == "list":
        return {"ok": True, "proposals": list_proposals()}
    if action == "show":
        return {"ok": True, **show(proposal_id)}
    if action == "tally":
        return {"ok": True, **tally(proposal_id)}
    raise ValueError("action must be list, show or tally")
