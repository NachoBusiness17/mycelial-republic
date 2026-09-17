"""build_lane_game — the BUILD window of the 24/7 two-key drive.

Operator order (2026-09-17): "we have two open router keys... task the other on a build:
steal the game and fill it with our shit." This lane drives OPENROUTER_API_KEY_2
(model from OPENROUTER_MODEL, currently stealth/ox-alpha) to draft RUINS GO levels
and promotes them ONLY through the game's own regression gate
(node test_ruins_go.js --pack-all: schema + BFS solvability under engine laws).

HOUSE LAWS, structurally:
  * model output is a DRAFT. Promotion = the node validator's PASS line. No exceptions.
  * proposals append to build_lane/proposals.jsonl with the verbatim answer (never dropped);
  * candidate files live in dashboard/static/games/ only during validation, then move to the
    inbox as promoted/rejected records — the games dir never accumulates unvetted data;
  * SSRF guard: https only, host allowlist {openrouter.ai}, resolved IPs must be public,
    redirects refused;
  * one run at a time (lock; stale holders self-clear after 15 min).

RUN:  .venv\\Scripts\\python.exe scripts\\build_lane_game.py --batch 1
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
ALLOWED_HOSTS = {"openrouter.ai"}

_LANES = {"base": "https://openrouter.ai/api/v1", "key": "OPENROUTER_API_KEY_2",
          "model_env": "OPENROUTER_MODEL", "model_default": "stealth/union-alpha"}

SYSTEM = (
    "You are a level designer for RUINS GO, a grid-turn tomb puzzle. The world only moves "
    "when the player moves. You output ONE level as JSON in a fenced ```json block and "
    "nothing else after it. Schema: {\"id\": \"P##\", \"name\": \"two words\", \"chapter\": 1-4, "
    "\"ins\": \"one-line inscription, plain, no em-dashes\", \"hint\": \"one line, teaches "
    "without solving\", \"rows\": [7 strings of exactly 7 chars from: ' ' void, '.' floor, "
    "'1' height1, '2' height2, '#' pillar, 'b' bridge, 'p' plate, 'k' crank, 'x' collapse "
    "ledge, 's' spear, 'E' exit], \"player\": [x,y], \"blocks\": [[x,y]], \"snakes\": [[x,y]], "
    "\"lizards\": [[ax,ay,bx,by]], \"twin\": [x,y], \"gems\": [[x,y]]} — omit empty lists. "
    "LAWS: snakes step toward the player once per player step and never enter E or cranks; "
    "lizards patrol their line and kill on contact; stepping onto a crank latches ALL "
    "bridges on; a plate holds bridges while player/block/twin stands on it; 'x' collapses "
    "to void when left; spears kill on odd move-counts; height changes of exactly 1 only; "
    "the player's start cell MUST have at least two legal first moves. "
    "MANDATORY SELF-CHECK in your reasoning BEFORE the json block: walk your "
    "claimed_solution [\"U\",\"L\",...] move by move on the grid you built; verify every "
    "step is a legal move (terrain, height diff <= 1, no deadly occupant at arrival, "
    "bridge state correct at that moment); if ANY step fails, fix the level and re-walk "
    "it. Include \"claimed_solution\" as a top key (the validator ignores it). Keep the "
    "level solvable in under 25 moves. Every cell you place must matter."
)

BRIEFS = [
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


def _call(model: str, key: str, prompt: str, timeout: int = 240) -> dict:
    t0 = time.time()
    rec: dict = {"lane": "build-ox", "model": model, "ts": _now()}
    try:
        _validate_base(_LANES["base"])
    except ValueError as e:
        rec.update({"ok": False, "error": "SSRF_GUARD", "detail": str(e)[:200]})
        return rec
    # no max_tokens cap: these are 100k+ context windows and the reasoning channel
    # spends freely before content (fleet receipt: rationing caused every empty_content;
    # the solved problem is to let the model run to its own stop).
    body = {"model": model, "temperature": 0.4,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]}
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
        txt = (d["choices"][0]["message"].get("content") or "").strip()
        if not txt:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": f"finish={d['choices'][0].get('finish_reason')} "
                                  f"tokens={d.get('usage', {}).get('completion_tokens')}"})
        else:
            rec.update({"ok": True, "answer": txt, "chars": len(txt),
                        "usage": d.get("usage") or {}})
    except urllib.error.HTTPError as e:
        rec.update({"ok": False, "error": f"HTTP {e.code}",
                    "detail": e.read().decode("utf-8", "replace")[:200]})
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"})
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


def _load_state() -> dict:
    if STATE.is_file():
        st = json.loads(STATE.read_text(encoding="utf-8"))
    else:
        st = {"done": [], "dead": {}, "runs": 0, "promoted": 0, "rejected": 0}
    # transport failures (dead model id, reasoning-budget empties) are not brief-merit
    # deaths: prune them so the brief gets its real two attempts.
    st["dead"] = {sid: why for sid, why in (st.get("dead") or {}).items()
                  if not any(t in str(why) for t in ("empty_content", "HTTP", "SSRF"))}
    return st


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="build-lane-game")
    ap.add_argument("--batch", type=int, default=1)
    a = ap.parse_args(argv)

    OUT.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    if LOCK.is_file() and (time.time() - LOCK.stat().st_mtime) < 900:
        print(json.dumps({"ok": True, "note": "LOCKED"}))
        return 0

    env = _env()
    key = env.get(_LANES["key"])
    state = _load_state()
    if not key:
        state["dead"]["key"] = f"{_LANES['key']} missing"
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        print(json.dumps({"ok": False, "error": "NO_KEY", "key_name": _LANES["key"]}))
        return 0
    # model chain: sticky working model first, then env preference, then known fallbacks.
    # (receipt 2026-09-17: stealth/ox-alpha's window ended; OpenRouter's 404 body revealed
    #  it WAS z-ai glm-5.3-flash and invited the direct id — the "parallel line to 5.3
    #  flash" the operator named.)
    chain = [m for m in [state.get("model"),
                         env.get(_LANES["model_env"]),
                         "z-ai/glm-5.3-flash",
                         "stealth/union-alpha"] if m]
    seen: set[str] = set()
    model = None
    for m in chain:
        if m in seen:
            continue
        seen.add(m)
        probe = _call(m, key, "Reply with exactly: READY", timeout=60)
        if probe.get("ok"):
            model = m
            break
        rec_detail = (probe.get("detail") or "")
        if probe.get("error") == "HTTP 404" and "glm-5.3-flash" in rec_detail:
            continue  # dead stealth id with the migration pointer
        model = m  # other errors: still try it for the real batch (row will record it)
        break
    if model is None:
        model = chain[-1]
    state["model"] = model

    todo = [(sid, brief) for sid, brief in BRIEFS
            if sid not in state["done"] and sid not in state["dead"]][: max(1, a.batch)]
    if not todo:
        print(json.dumps({"ok": True, "note": "QUEUE_EMPTY",
                          "promoted": state.get("promoted", 0),
                          "rejected": state.get("rejected", 0)}))
        return 0

    LOCK.write_text(_now(), encoding="utf-8")
    results = []
    try:
        for sid, brief in todo:
            prompt = (f"Design one RUINS GO level. Brief: {brief} "
                      f"Constraints: 7x7 grid, solvable, under 25 moves, exactly one exit. "
                      f"Output only the ```json block.")
            rec = _call(model, key, prompt)
            rec.update({"brief": sid})
            defn = _extract_level(rec.get("answer") or "") if rec.get("ok") else None
            verdict, vline = None, None
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
                        dest = RECEIPTS / f"promoted_{sid}.json"
                    else:
                        dest = RECEIPTS / f"rejected_{sid}.json"
                    shutil.move(str(cand), str(dest))
                    state["promoted" if verdict else "rejected"] = \
                        state.get("promoted" if verdict else "rejected", 0) + 1
                else:
                    verdict, vline = False, f"schema: {why}"
                    (RECEIPTS / f"rejected_{sid}.json").write_text(
                        json.dumps(defn, indent=1), encoding="utf-8")
                    state["rejected"] = state.get("rejected", 0) + 1
            else:
                verdict, vline = False, "no json block" if rec.get("ok") else rec.get("error")
                state["rejected"] = state.get("rejected", 0) + 1
            rec.update({"verdict": "PASS" if verdict else "FAIL", "gate": vline})
            with PROPOSALS.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if verdict:
                state["done"].append(sid)
            else:
                state.setdefault("attempts", {})
                state["attempts"][sid] = state["attempts"].get(sid, 0) + 1
                if state["attempts"][sid] >= 2:
                    state["dead"][sid] = vline[:120] if vline else "failed twice"
            results.append({"brief": sid, "verdict": rec["verdict"], "gate": (vline or "")[:120]})
    finally:
        state["runs"] = state.get("runs", 0) + 1
        state["updated"] = _now()
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        LOCK.unlink(missing_ok=True)

    print(json.dumps({"ok": True, "schema": SCHEMA, "model": model,
                      "batch": len(results),
                      "promoted": sum(1 for r in results if r["verdict"] == "PASS"),
                      "rejected": sum(1 for r in results if r["verdict"] == "FAIL"),
                      "totals": {"promoted": state.get("promoted", 0),
                                 "rejected": state.get("rejected", 0)},
                      "results": results}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
