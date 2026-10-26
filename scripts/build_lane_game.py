"""build_lane_game — the BUILD window of the 24/7 two-key drive.

Operator order (2026-09-17): "we have two open router keys... task the other on a build:
steal the game and fill it with our shit." This lane drives OPENROUTER_API_KEY_2
(model from _LANES below) to draft RUINS GO levels
and promotes them ONLY through the game's own regression gate
(node test_ruins_go.js --pack-all: schema + BFS solvability under engine laws).

MODEL FLIP 2026-09-26 (operator burn order B2-55): stealth/union-alpha 404s 12x today
(build_lane/proposals.jsonl 2026-09-26 rows, generations 72 -> 84, briefs
DD-blob-double + DD-split-path, all transport-dead). The 404 body itself names the
successor: "This model was Unbiased's Pareto. Use it now:
https://openrouter.ai/unbiased/pareto". Primary is now unbiased/pareto (probed live
READY via this file's own _call, 2026-09-26); z-ai/glm-5.3-flash stays fallback.
The 2026-09-17 MODEL LAW (primary always, loud downgrades only) is unchanged in shape;
only the primary's id moves with its window.

HOUSE LAWS, structurally:
  * model output is a DRAFT. Promotion = the node validator's PASS line. No exceptions.
  * proposals append to build_lane/proposals.jsonl with the verbatim answer (never dropped);
  * candidate files live in dashboard/static/games/ only during validation, then move to the
    inbox as promoted/rejected records — the games dir never accumulates unvetted data;
  * SSRF guard: https only, host allowlist {openrouter.ai}, resolved IPs must be public,
    redirects refused;
  * one run at a time (lock; stale holders self-clear after 15 min).

RUN:  .venv\\Scripts\\python.exe scripts\\build_lane_game.py --batch 1
CENSUS: .venv\\Scripts\\python.exe scripts\\build_lane_game.py --census
Class mapping (B2-117, keyed to the frozen denominator 41 from
B2_33_rejection_recount_20260926.md over the committed 2026-09-17 snapshot,
git 3d12289f9): write-time error "KeyError" (KeyError 'choices') and explicit
"200_error_body" fold into class 200-error-body (frozen 16 = 12 + 4);
"HTTP 404" -> http-404 (11); "empty_content" -> empty_content (9);
"IncompleteRead" -> incomplete-read (1); gate "schema: ..." -> schema-gate (2);
gate FAIL with "exhausted @" (BFS solvability) -> merit (2). 16+11+9+1+2+2 = 41.
--census reclassifies the live proposals.jsonl with this mapping, reports the
frozen-window tally vs live tally, and exits 0 on frozen reconciliation.
Schema: build_lane_game.v1
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "watch" / "inbox" / "union_fullsend_20260917" / "build_lane"
PROPOSALS = OUT / "proposals.jsonl"
STATE = OUT / "state.json"
LOCK = OUT / "run.lock"
GAMES = ROOT / "dashboard" / "static" / "games"
PACK = GAMES / "ruins_go_pack.json"
RECEIPTS = OUT / "receipts"  # promoted/rejected candidates move here

SCHEMA = "build_lane_game.v1"
ENV_FILES = [ROOT / ".env", Path.home() / "AppData" / "Local" / "hermes" / ".env"]
ALLOWED_HOSTS = {"openrouter.ai", "api.z.ai"}

_LANES = {"base": "https://openrouter.ai/api/v1",
          "keys": ["OPENROUTER_API_KEY_2", "OPENROUTER_API_KEY"],  # rotate on 429/401/402
          "models": ["unbiased/pareto", "z-ai/glm-5.3-flash"]}

# --lane lite: the SAME evolution loop on the z.ai Lite seat (glm-5.3-flash),
# its own state dir + locks (runs in parallel with the union window), law-15 paced.
_LANES_LITE = {"base": "https://api.z.ai/api/coding/paas/v4",
               "keys": ["ZAI_API_KEY_Lite"],
               "models": ["glm-5.3-flash"]}
# operator 2026-09-17: "i know what ox is, thats an old config. we're using union."
# (env OPENROUTER_MODEL=stealth/ox-alpha is stale; ox's own 404 revealed it was
#  glm-5.3-flash. 2026-09-26: the union window also ended; primary is unbiased/pareto,
#  glm-5.3-flash kept as the last-resort fallback.)

SYSTEM = (
    "You are a level designer for RUINS GO, a grid-turn tomb puzzle. The world only moves "
    "when the player moves. You evolve levels against a mechanical validator: it replays "
    "your level under the engine's exact laws and proves (or fails to prove) that some "
    "sequence of legal moves reaches the exit. You will see its verdicts. Iterate until "
    "it passes. Novel, surprising, fair designs are the goal; the gate is the fitness "
    "function, not a formality."
)

# The stable fat prefix — identical bytes every call and every generation, so the
# provider prompt-cache pays for it once (self-stolen from the TT3 pattern: context
# pack + growing turns; z.ai receipts show cached=9247 on exactly this shape).
CONTEXT = """ENGINE LAWS (exact, enforced by the validator):
L1 step-clock: the world ticks only when the player displaces; a blocked bump is not a move.
L2 ledges: step up or down exactly ONE height ('.'=0,'1'=1,'2'=2). Two is forbidden.
L3 pushes: blocks move same-height or slide down one; never up; never through anything; never onto cranks or exits.
L4 bridges: stepping onto a crank 'k' LATCHES all bridges on; a plate 'p' holds them while any of player/block/twin stands on it; a retracted 'b' is void to everyone.
L5 collapse: an 'x' cell becomes void the moment the player leaves it. No way back.
L6 spears: 's' kills if the player ENDS a move on it at an ODD move-count; even counts are safe.
L7 snakes: after each player move, each snake steps ONE cell toward the player (same height only, never onto cranks/exits, blocked by blocks/void). Contact kills both ways. They cannot be killed, only denied.
L8 lizards: patrol the straight line between (ax,ay) and (bx,by), one cell per player move, reverse at the ends or when blocked. Contact kills.
L9 twin: if present, mirrors the player's direction after each player move; denied (void/height/occupied), it waits. It can hold plates. It cannot be harmed.
L10 exit 'E' wins on arrival; gems are optional.

TERRAIN: ' ' void · '.' floor · '1','2' heights · '#' pillar(_blocks) · 'b' bridge · 'p' plate · 'k' crank · 'x' collapse · 's' spear · 'E' exit. Grid is 7x7. Exactly one E. Player start MUST have at least two legal first moves.

VERIFIED EXAMPLES (these passed the gate; design in this family):
EXAMPLE 1 "the weight" (block holds a plate to hold a bridge), solvable in 8 moves:
rows: ["       ","       "," ...   "," ..pb.E."," ...  . ","       ","       "], player [0,3], blocks [[1,3]], gems [[5,4]]. Push the block right onto the plate, cross the latched bridge to E.
EXAMPLE 2 "the snake" (ring room; the snake's refusal to enter E parks it as a guard), solvable in 4 moves:
rows: ["       "," ..... "," . . . "," . E . "," ..... ","       ","       "], player [1,1], snakes [[5,4]], gems [[5,1]]. Walk the top lane right, then down through the center to E while the snake chases and parks against the E it will not enter.
EXAMPLE 3 "the other self" (twin mirrors and parks on a plate), solvable in 6 moves:
rows: ["       ","  ...# ","  ...p ","  ...  "," ...b. ","     E ","       "], player [2,2], twin [4,2], gems [[4,1]]. Step right twice so the twin lands on the plate and is denied further moves; descend, cross the bridge it holds, reach E.

VALIDATOR FAILURE GLOSSARY:
- "exhausted @N" = the solver explored every reachable state and NO move sequence reaches E. Causes: player sealed in, a required cell guarded at the wrong parity, a bridge never on when needed, a collapse path that must be revisited. Check: does your claimed_solution actually walk? Does the enemy timing leave a live path at EVERY step?
- "cap @N" = state space too large. Remove an enemy or shrink the arena.
- "schema: ..." = fix the named field. Rows must each be exactly 7 chars; all coordinates inside the grid; entity cells must be walkable terrain.

OUTPUT CONTRACT: one fenced ```json block, nothing after it. Keys: id, name, chapter, ins (one plain line, no em-dashes), hint (teaches without solving), rows (7x7), player [x,y], and only the entity lists you use: blocks [[x,y]], snakes [[x,y]], lizards [[ax,ay,bx,by]], twin [x,y], gems [[x,y]]. Include claimed_solution (list of "U"/"D"/"L"/"R") — walk it yourself on your grid, move by move, BEFORE emitting; fix whatever breaks. Under 25 moves. Every cell must matter."""

BRIEFS = [
    # BRIEFS_FILE (watch/inbox/union_fullsend_20260917/build_lane/briefs.json) is merged
    # at run start when present — the queue tender feeds it without driver edits.
    ("P-collapse-crank", "chapter 1 'the ledger'. Mechanic: collapse ledges ('x') leading to a crank that latches a bridge to the exit. One gem behind a collapsing dead-end that is safe only if visited in the right order. Inscription theme: receipts before work."),
    ("P-snake-guard", "chapter 2 'the keeper'. Mechanic: one snake guarding a ring or corridor; the exit is placed so the snake's refusal to enter 'E' parks it on the wrong side. Inscription theme: the keeper calls his own by name."),
    ("P-spear-rhythm", "chapter 2 'the sentry'. Mechanic: a spear corridor ('s' alternating with '.') whose safe parity forces exactly one waiting move; plus a lizard crossing the approach. Inscription theme: the falsifier constrains the analysis, not the experiment."),
    ("P-block-plate-two-islands", "chapter 1 'the weight'. Mechanic: two islands, one block, one plate; the block must be pushed down a ledge (height drops) onto the plate to hold the bridge. Inscription theme: two banks, one river, never merged."),
    ("P-twin-plate", "chapter 3 'the other self'. Mechanic: twin mirrors the player; twin must end parked on a plate (denied by void/pillars) while the player crosses the bridge to the exit. Inscription theme: the minimal honest stone commits beforehand to what would make it wrong."),
    ("P-height-snake", "chapter 3 'the climb'. Mechanic: height-1 ledge bypass OVER a same-height snake patrol; the snake cannot climb. Inscription theme: canonical flows to derived, never backward."),
    ("P-queen-gauntlet", "chapter 4 'the queen of venom'. Mechanic: two snakes converging on a collapsing spiral ('x' ring), exit at the center or far end, solvable only forward. Inscription theme: the world only moves when you move."),
    ("P-crank-latch-sequence", "chapter 3 'two rivers'. Mechanic: two bridge crossings with ONE crank whose latch is stepped once early, plus a collapse detour to the gem that must not trap the player. Inscription theme: a hash by itself does not prove when."),
    ("P-sentry-weave", "chapter 2 'the crossing'. Mechanic: two lizards on parallel lines with offset phases; the player weaves between them to a spear-timed door. Inscription theme: an unexamined no is a silent skip."),
    ("P-scale-finale", "chapter 4 'the scale'. Mechanic: a plate that must be held by a BLOCK the player pushes onto it, while a twin mirrors and a snake hunts; three systems, one order. Inscription theme: charcoal is free."),
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _env() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in ENV_FILES:
        if not p.is_file():
            continue
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                out.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return out


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "redirect refused (SSRF guard)",
                                     headers, fp)


_OPENER = urllib.request.build_opener(_NoRedirect)


def _validate_base(base: str) -> None:
    u = urllib.parse.urlsplit(base)
    if u.scheme != "https" or not u.hostname:
        raise ValueError(f"base must be https://host, got {base!r}")
    host = u.hostname.lower()
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"host {host!r} not in allowlist")
    for info in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            raise ValueError(f"{host} resolves to non-public {ip}; refusing")


_FLIP_CARDS = ROOT / "watch" / "inbox" / "burn_lane_flip_cards.jsonl"
_USE_IT_NOW_RE = re.compile(r"Use it now:\s*(https?://[^\s\"'<>\\]+)", re.I)


def _file_retirement_flip(dead_model: str, body_text: str, _seen: dict = {}) -> dict | None:
    """B2-189 (2026-09-26): a retirement 404 body names its own successor in-band
    ('This model was X. Use it now: https://openrouter.ai/owner/name' — the
    union-alpha case waited for a human lane to parse it). On a match, append one
    flip-card row {ts, dead_model, successor, successor_url, source} to
    watch/inbox/burn_lane_flip_cards.jsonl so the next window death files itself.
    Append-only; deduped per (dead_model, successor) per process; never raises
    (flip-card filing must not break the lane)."""
    try:
        m = _USE_IT_NOW_RE.search(body_text or "")
        if not m:
            return None
        url = m.group(1).rstrip(".,;)")
        tail = url.split("openrouter.ai/")[-1]
        successor = "/".join(tail.split("/")[-2:]) if "/" in tail else tail
        card = {"ts": _now(), "dead_model": dead_model, "successor": successor,
                "successor_url": url, "source": "build_lane_404_body"}
        k = (dead_model, successor)
        if _seen.get(k):
            return None
        _seen[k] = True
        _FLIP_CARDS.parent.mkdir(parents=True, exist_ok=True)
        existing = ""
        if _FLIP_CARDS.is_file():
            existing = _FLIP_CARDS.read_text(encoding="utf-8")
            if f'"dead_model": "{dead_model}", "successor": "{successor}"' in existing:
                return None
        with open(_FLIP_CARDS, "a", encoding="utf-8") as f:
            f.write(json.dumps(card, ensure_ascii=False) + "\n")
        return card
    except Exception:
        return None


def _call(model: str, keys: list[str], prompt: str | None, timeout: int = 600,
          messages: list[dict] | None = None, lite: bool = False) -> dict:
    """Rotate keys on 429/401/402 (operator: multiple OpenRouter keys, use them).
    Accepts either a one-shot prompt or a full multi-turn `messages` list (the
    evolution loop grows the conversation; generation N sees its own failures).
    No max_tokens, generous timeout: the operator's law — never kill the model
    before nuance can be obtained."""
    t0 = time.time()
    rec: dict = {"lane": "build-union", "model": model, "ts": _now()}
    try:
        _validate_base(_LANES["base"])
    except ValueError as e:
        rec.update({"ok": False, "error": "SSRF_GUARD", "detail": str(e)[:200]})
        return rec
    if messages is None:
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt or ""}]
    else:
        messages = [{"role": "system", "content": SYSTEM}] + messages
    if lite:
        # law 15 structural: the Lite seat is paced before a token leaves
        try:
            from mag import lite_guard
            g = lite_guard.check("build_lane_lite")
            if not g.get("ok"):
                rec.update({"ok": False, "error": "LITE_PACED", "detail": g.get("deny", "")})
                rec["latency_ms"] = 0
                return rec
        except Exception:
            pass
    for ki, key in enumerate(keys):
        body = {"model": model, "temperature": 0.4, "messages": messages}
        req = urllib.request.Request(
            _LANES["base"].rstrip("/") + "/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "User-Agent": "mag-build-lane/1.0",
                     "HTTP-Referer": "https://local-sovereign-agent.invalid",
                     "X-Title": "Mag Build Lane"})
        try:
            with _OPENER.open(req, timeout=timeout) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            if "choices" not in d:
                # HTTP 200 with an error body (seen on stealth lanes): rotate like a 429
                body_err = json.dumps(d.get("error") or d, ensure_ascii=False)[:200]
                rec.update({"ok": False, "error": "200_error_body", "detail": body_err,
                            "key_index": ki})
                if ki < len(keys) - 1:
                    continue
                rec["latency_ms"] = int((time.time() - t0) * 1000)
                return rec
            txt = (d["choices"][0]["message"].get("content") or "").strip()
            if not txt:
                rec.update({"ok": False, "error": "empty_content",
                            "detail": f"finish={d['choices'][0].get('finish_reason')} "
                                      f"tokens={d.get('usage', {}).get('completion_tokens')}"})
            else:
                rec.update({"ok": True, "answer": txt, "chars": len(txt),
                            "usage": d.get("usage") or {}, "key_index": ki})
            rec["latency_ms"] = int((time.time() - t0) * 1000)
            return rec
        except urllib.error.HTTPError as e:
            full_body = e.read().decode("utf-8", "replace")
            detail = full_body[:200]
            rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail,
                        "key_index": ki})
            if e.code == 404:
                # B2-189: parse the in-band successor from the FULL body
                # before the 200-char detail truncation
                card = _file_retirement_flip(model, full_body)
                if card:
                    rec["retirement_flip_card"] = card
            if e.code in (429, 401, 402) and ki < len(keys) - 1:
                continue  # rotate to the next key
            rec["latency_ms"] = int((time.time() - t0) * 1000)
            return rec
        except Exception as e:
            rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}",
                        "key_index": ki})
            rec["latency_ms"] = int((time.time() - t0) * 1000)
            return rec
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


def _extract_level(answer: str) -> dict | None:
    m = re.search(r"```json\s*(\{.*?\})\s*```", answer, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def _schema_ok(defn: dict) -> tuple[bool, str]:
    if not isinstance(defn, dict):
        return False, "not an object"
    rows = defn.get("rows")
    if not isinstance(rows, list) or not (3 <= len(rows) <= 15):
        return False, "rows 3..15"
    w = len(rows[0]) if rows else 0
    if not (3 <= w <= 15):
        return False, "width 3..15"
    legal = set(" .12#bpkxsE")
    for r in rows:
        if not isinstance(r, str) or len(r) != w or any(c not in legal for c in r):
            return False, "bad row"
    if "E" not in "".join(rows):
        return False, "no exit"
    if not isinstance(defn.get("player"), list) or len(defn["player"]) != 2:
        return False, "player"
    return True, ""


def _validate_via_gate(cand_name: str) -> tuple[bool, str]:
    """Run the game's own gate; parse this candidate's verdict line."""
    p = subprocess.run(["node", "test_ruins_go.js", "--pack-all"],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=300)
    for ln in (p.stdout or "").splitlines():
        if cand_name in ln:
            return ln.strip().startswith("PASS"), ln.strip()
    return False, (p.stdout or p.stderr or "no verdict").strip()[:300]


# B2-117: frozen 09-17 rejection census (B2_33_rejection_recount_20260926.md,
# recounted from committed bytes git 3d12289f9). Denominator 41 exact:
# 200-error-body 16 (12 "KeyError: 'choices'" + 4 explicit "200_error_body"),
# http-404 11, empty_content 9, schema-gate 2, incomplete-read 1, merit 2.
FROZEN_CENSUS_20260917 = {
    "200-error-body": 16,
    "http-404": 11,
    "empty_content": 9,
    "schema-gate": 2,
    "incomplete-read": 1,
    "merit": 2,
}
# The committed snapshot is the first 71 rows (B2-33: 71 rows committed at git
# 3d12289f9, 41 FAIL; a byte-prefix of the live file), through the last frozen
# IncompleteRead/empty_content rows early 2026-09-18Z.
FROZEN_COMMIT = "3d12289f9"
COMMITTED_PREFIX_ROWS = 71


def _error_class(rec: dict) -> str:
    """B2-117 class mapping: fold KeyError 'choices' into 200-error-body by the
    reviewer convention the frozen census used; BFS "exhausted @" gate FAILs are
    the 2 merit rows; schema gate FAILs carry the "schema: " prefix."""
    err = str(rec.get("error") or "")
    gate = str(rec.get("gate") or "")
    if (rec.get("verdict") == "FAIL" and not err and gate.startswith("schema:")):
        return "schema-gate"
    if (rec.get("verdict") == "FAIL" and not err and gate.startswith("FAIL")
            and "exhausted @" in gate):
        return "merit"
    if "KeyError" in err or "200_error_body" in err:
        return "200-error-body"
    if "404" in err:
        return "http-404"
    if "empty_content" in err:
        return "empty_content"
    if "IncompleteRead" in err:
        return "incomplete-read"
    return "unclassified"


def _census() -> dict:
    """Recount proposals.jsonl under the frozen mapping and reconcile the
    frozen window (the committed snapshot, git 3d12289f9, 71 rows whose 41
    FAIL rows are the B2-33 denominator) against FROZEN_CENSUS_20260917.
    Prefers the committed bytes via `git show`; falls back to the first
    COMMITTED_PREFIX_ROWS rows of the live file (B2-33 proved the committed
    71 are a byte-prefix of the live file). Read-only; never appends."""
    committed = None
    prov = "live-prefix"
    try:
        import subprocess as _sp
        rel = PROPOSALS.relative_to(ROOT).as_posix()
        out = _sp.run(["git", "show", "%s:%s" % (FROZEN_COMMIT, rel)],
                      capture_output=True, timeout=60)
        if out.returncode == 0:
            committed = out.stdout.decode("utf-8", "replace")
            prov = "git:%s" % FROZEN_COMMIT
    except Exception:
        committed = None
    if committed is None and PROPOSALS.is_file():
        committed = "\n".join(
            PROPOSALS.read_text(encoding="utf-8").splitlines()[:COMMITTED_PREFIX_ROWS])
    rows = [json.loads(ln) for ln in (committed or "").splitlines() if ln.strip()]
    live_rows = []
    if PROPOSALS.is_file():
        live_rows = [json.loads(ln) for ln in
                     PROPOSALS.read_text(encoding="utf-8").splitlines() if ln.strip()]
    fails = [r for r in rows if r.get("verdict") == "FAIL"]
    frozen_tally: dict[str, int] = {}
    for r in fails:
        c = _error_class(r)
        frozen_tally[c] = frozen_tally.get(c, 0) + 1
    live_tally: dict[str, int] = {}
    for r in (x for x in live_rows if x.get("verdict") == "FAIL"):
        c = _error_class(r)
        live_tally[c] = live_tally.get(c, 0) + 1
    reconciled = (frozen_tally == FROZEN_CENSUS_20260917
                  and len(rows) == COMMITTED_PREFIX_ROWS)
    return {"ok": True, "schema": SCHEMA, "census": "B2-117",
            "frozen_denominator": sum(FROZEN_CENSUS_20260917.values()),
            "frozen_census_20260917": FROZEN_CENSUS_20260917,
            "frozen_source": prov,
            "frozen_window_rows": len(rows),
            "frozen_window_fail_rows": len(fails),
            "frozen_window_tally": frozen_tally,
            "reconciled": reconciled,
            "live_rows": len(live_rows),
            "live_fail_rows": sum(1 for x in live_rows if x.get("verdict") == "FAIL"),
            "live_tally": live_tally,
            "source": str(PROPOSALS)}


# B2-188 (2026-09-26): ACROSS-RUNS transport tripwire. The disease this cures:
# 12 consecutive HTTP 404 generations burned across 3 cron runs (11:29/11:36/
# 11:38Z 2026-09-26, watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl)
# with ZERO alarm, because the in-run guard ("two consecutive transport deaths
# end this RUN") only sees the 4 deaths of its own run and each fresh cron run
# starts silent. This run-end check counts the CONSECUTIVE 404 tail of
# proposals.jsonl (the persistent record), persists the streak in state, and
# alarms once per streak at ALARM_N, naming the dead model, the last real
# success, and the provider successor pointer when a 404 body names one
# (the union-alpha body names its successor in-band).
TRANSPORT_TRIPWIRE_ALARM_N = 8
TRIPWIRE = OUT / "transport_tripwire.jsonl"


def _successor_from_body(detail: str) -> str | None:
    """Pull the successor model/URL a retirement 404 body names in-band."""
    import re as _re
    if not detail:
        return None
    m = _re.search(
        r"(?:migrat\w*|successor|replaced? by|use|switch to|decommission\w*)"
        r"[^.\"\\]{0,120}?\b([a-z0-9_.\-]+/[a-z0-9_.\-]+)\b",
        detail, _re.I)
    if m:
        return m.group(1)
    m = _re.search(r"(https?://[^\s\"\\]+)", detail)
    return m.group(1) if m else None


def _transport_tripwire(state: dict) -> dict | None:
    """Run-end check: alarm after N consecutive transport-dead (404) rows."""
    try:
        lines = PROPOSALS.read_text(encoding="utf-8",
                                    errors="replace").strip().splitlines()
    except OSError:
        return None
    recs = []
    for ln in lines[-64:]:
        try:
            recs.append(json.loads(ln))
        except Exception:
            continue
    streak = 0
    model = None
    newest_body = ""
    newest_ts = None
    for rec in reversed(recs):
        if rec.get("ok"):
            break
        if "404" not in str(rec.get("error") or ""):
            break
        streak += 1
        if newest_ts is None:
            newest_ts = rec.get("ts")
            model = rec.get("model")
            newest_body = str(rec.get("detail") or "")
    last_ok = next((r.get("ts") for r in reversed(recs) if r.get("ok")),
                   state.get("last_transport_success"))
    state["transport_404_streak"] = streak
    state["last_transport_success"] = last_ok
    if streak < TRANSPORT_TRIPWIRE_ALARM_N:
        return None
    # dedupe on the streak SIGNATURE (length + newest death ts), not length
    # alone: a fresh streak of the same length must re-alarm (B2-188 pin).
    signature = "%s:%s" % (streak, newest_ts)
    if state.get("transport_alarm_signature") == signature:
        return None  # already alarmed for this streak; no repeat noise
    alarm = {
        "ts": _now(), "alarm": "TRANSPORT_404_STREAK", "streak": streak,
        "threshold": TRANSPORT_TRIPWIRE_ALARM_N, "model": model,
        "last_success": last_ok, "window_records": len(recs),
        "successor": _successor_from_body(newest_body),
    }
    try:
        with TRIPWIRE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(alarm, ensure_ascii=False) + "\n")
    except OSError:
        pass
    state["transport_alarm_signature"] = signature
    state["transport_alarm_last"] = alarm["ts"]
    print("TRANSPORT TRIPWIRE: %s" % json.dumps(alarm, ensure_ascii=False),
          file=sys.stderr)
    return alarm


def _load_state() -> dict:
    if STATE.is_file():
        st = json.loads(STATE.read_text(encoding="utf-8"))
    else:
        st = {"done": [], "dead": {}, "runs": 0, "promoted": 0, "rejected": 0}
    # transport failures (dead model id, reasoning-budget empties, 200-with-error bodies)
    # are not brief-merit deaths: prune them so the brief gets its real two attempts,
    # and reset the attempt counter the transport death burned.
    transport = ("empty_content", "HTTP", "SSRF", "KeyError")
    dead = st.get("dead") or {}
    st["dead"] = {sid: why for sid, why in dead.items()
                  if not any(t in str(why) for t in transport)}
    for sid in dead:
        if sid not in st["dead"]:
            st.setdefault("attempts", {})[sid] = 0
    return st


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="build-lane-game")
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--census", action="store_true",
                    help="B2-117: recount proposals.jsonl under the frozen "
                         "2026-09-17 class mapping (denominator 41), read-only")
    a = ap.parse_args(argv)

    if a.census:
        print(json.dumps(_census()))
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    if LOCK.is_file() and (time.time() - LOCK.stat().st_mtime) < 900:
        print(json.dumps({"ok": True, "note": "LOCKED"}))
        return 0

    env = _env()
    keys = [env[k] for k in _LANES["keys"] if env.get(k)]
    state = _load_state()
    if not keys:
        state["dead"]["key"] = "no OpenRouter keys in env"
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        print(json.dumps({"ok": False, "error": "NO_KEY", "key_names": _LANES["keys"]}))
        return 0
    # MODEL LAW (operator order 2026-09-17, after the cron silently downgraded the lane
    # to glm: "why was the model switched to 5.3 again, its the fucking cron job -- fix
    # it and make sure this doesnt happen again"):
    #   PRIMARY is the window's model, ALWAYS. A transient probe failure (429, hiccup,
    #   200-error-body) is NOT a migration: retry the primary, and if it is truly down,
    #   the fallback serves THIS RUN ONLY and is never persisted to state. The sticky
    #   model can only ever be the primary. Downgrades must be loud (this receipt) not
    #   silent (the old auto-stick behavior -- removed).
    # FLIP RECEIPT 2026-09-26 (B2-55): primary stealth/union-alpha -> unbiased/pareto.
    # Evidence: 12 HTTP 404 rows on 2026-09-26 in build_lane/proposals.jsonl
    # (DD-blob-double + DD-split-path, gens 72 -> 84), 404 body names the successor;
    # probe of both models via this file's _call returned ok=true 2026-09-26.
    primary = "unbiased/pareto"
    fallback = "z-ai/glm-5.3-flash"
    # SCHEDULE LAW (operator: glm-5.3-flash is FREE from 11:00 local daily on the Lite
    # seat — he should never have to remind us): after 11:00 the Lite lane is a scheduled
    # primary — the run alternates the OpenRouter primary + glm so both free windows
    # burn together. (2026-09-26 flip: "union" slot below is now the current primary;
    # the old literal stealth/union-alpha here would have resurrected the dead model
    # on alternating runs after 11:00.)
    import datetime as _dt
    if _dt.datetime.now().hour >= 11:
        primary = "unbiased/pareto" if state.get("runs", 0) % 2 == 0 else fallback
    model = None
    for _try in (1, 2):  # transient failures get a second probe before any fallback
        probe = _call(primary, keys, "Reply with exactly: READY", timeout=90)
        if probe.get("ok"):
            model = primary
            break
        time.sleep(5 * _try)
    used_fallback = False
    if model is None:
        detail = probe.get("detail") or ""
        if "404" in str(probe.get("error")) and primary in detail:
            model = fallback  # window genuinely ended (not transient)
            used_fallback = True
        else:
            model = primary  # unknown error: keep the primary, let the batch row record it
    state["model"] = primary  # the ONLY value ever persisted
    state["last_fallback_used"] = used_fallback

    all_briefs = list(BRIEFS)
    briefs_file = OUT / "briefs.json"
    if briefs_file.is_file():
        try:
            extra = json.loads(briefs_file.read_text(encoding="utf-8"))
            seen_ids = {b[0] for b in all_briefs}
            all_briefs += [(r["id"], r["brief"]) for r in extra if r["id"] not in seen_ids]
        except Exception:
            pass
    todo = [(sid, brief) for sid, brief in all_briefs
            if sid not in state["done"] and sid not in state["dead"]][: max(1, a.batch)]
    if not todo:
        print(json.dumps({"ok": True, "note": "QUEUE_EMPTY",
                          "promoted": state.get("promoted", 0),
                          "rejected": state.get("rejected", 0)}))
        return 0

    LOCK.write_text(_now(), encoding="utf-8")
    MAX_GEN = 6
    results = []
    try:
        for sid, brief in todo:
            # the stable fat prefix (cache-paid once) + this brief's angle
            msgs = [{"role": "user", "content":
                     CONTEXT + "\n\nTHIS LEVEL'S BRIEF: " + brief +
                     "\n\nDesign it. Walk your claimed_solution move by move first. "
                     "Output the full ```json block."}]
            promoted = False
            gens = 0
            last_gate = "none"
            all_transport = True  # stays True only if every gen died before the gate
            for gen in range(1, MAX_GEN + 1):
                rec = _call(model, keys, None, messages=msgs)
                rec.update({"brief": sid, "gen": gen})
                gens = gen
                if rec.get("ok"):
                    all_transport = False
                defn = _extract_level(rec.get("answer") or "") if rec.get("ok") else None
                verdict = False
                vline = "no json block" if rec.get("ok") else (rec.get("error") or "call failed")
                if defn:
                    sok, why = _schema_ok(defn)
                    if sok:
                        cand = GAMES / f"ruins_go_pack_cand_{sid}.json"
                        cand.write_text(json.dumps([defn], indent=1), encoding="utf-8")
                        verdict, vline = _validate_via_gate(cand.name)
                        if verdict:
                            pack = json.loads(PACK.read_text(encoding="utf-8")) if PACK.is_file() else []
                            if not any(l.get("id") == defn.get("id") for l in pack):
                                pack.append({k: v for k, v in defn.items()
                                             if k != "claimed_solution"})
                                PACK.write_text(json.dumps(pack, indent=1), encoding="utf-8")
                            shutil.move(str(cand), str(RECEIPTS / f"promoted_{sid}_g{gen}.json"))
                            state["promoted"] = state.get("promoted", 0) + 1
                        else:
                            shutil.move(str(cand), str(RECEIPTS / f"gen_{sid}_g{gen}.json"))
                    else:
                        vline = f"schema: {why}"
                        (RECEIPTS / f"gen_{sid}_g{gen}.json").write_text(
                            json.dumps(defn, indent=1), encoding="utf-8")
                last_gate = (vline or "")[:160]
                rec.update({"verdict": "PASS" if verdict else "FAIL", "gate": last_gate})
                with PROPOSALS.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                if verdict:
                    promoted = True
                    break
                # FEED THE VERDICT BACK — the gate is the fitness function; the model
                # gets its own output plus the failure and iterates. Never kill the
                # search before nuance can be obtained (operator law, 2026-09-17).
                msgs.append({"role": "assistant", "content": rec.get("answer") or "(no output)"})
                msgs.append({"role": "user", "content":
                             "The validator REJECTED generation " + str(gen) +
                             ". Verdict: " + str(vline) +
                             ". Diagnose the failure yourself using the glossary, "
                             "re-walk your claimed_solution move by move ON YOUR GRID, "
                             "fix what breaks (keep your theme and inscription), and "
                             "output the full corrected ```json block."})
                # two consecutive transport deaths end this RUN (network, not merit)
                if not rec.get("ok") and gen >= 2:
                    prev = json.loads(PROPOSALS.read_text(encoding="utf-8",
                                                          errors="replace").strip().splitlines()[-2])
                    if not prev.get("ok"):
                        break
            state["generations"] = state.get("generations", 0) + gens
            # AMENDMENT 001: a run that died in transport (dead model id / 404 /
            # empty body) never reached the gate, so it burns neither the rejection
            # count nor an attempt — only gate rejections and schema failures do.
            transport = ("empty_content", "HTTP", "SSRF", "KeyError")
            died_in_transport = (not promoted and all_transport
                                 and any(t in last_gate for t in transport))
            if promoted:
                state["done"].append(sid)
            elif died_in_transport:
                state["transport_pruned"] = state.get("transport_pruned", 0) + 1
            else:
                state["rejected"] = state.get("rejected", 0) + 1
                state.setdefault("attempts", {})
                state["attempts"][sid] = state["attempts"].get(sid, 0) + 1
                if state["attempts"][sid] >= 2:
                    state["dead"][sid] = f"no pass in {gens} gens x2 runs: {last_gate[:100]}"
            results.append({"brief": sid, "gens": gens,
                            "verdict": "PASS" if promoted else "FAIL",
                            "gate": last_gate[:120]})
    finally:
        state["runs"] = state.get("runs", 0) + 1
        state["updated"] = _now()
        _transport_tripwire(state)  # B2-188: across-runs streak, alarm at threshold
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        LOCK.unlink(missing_ok=True)

    print(json.dumps({"ok": True, "schema": SCHEMA, "model": model,
                      "batch": len(results), "max_gen": MAX_GEN,
                      "promoted": sum(1 for r in results if r["verdict"] == "PASS"),
                      "rejected": sum(1 for r in results if r["verdict"] == "FAIL"),
                      "totals": {"promoted": state.get("promoted", 0),
                                 "rejected": state.get("rejected", 0),
                                 "generations": state.get("generations", 0)},
                      "results": results}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
