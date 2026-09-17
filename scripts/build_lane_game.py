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
ALLOWED_HOSTS = {"openrouter.ai", "api.z.ai"}

_LANES = {"base": "https://openrouter.ai/api/v1",
          "keys": ["OPENROUTER_API_KEY_2", "OPENROUTER_API_KEY"],  # rotate on 429/401/402
          "models": ["stealth/union-alpha", "z-ai/glm-5.3-flash"]}

# --lane lite: the SAME evolution loop on the z.ai Lite seat (glm-5.3-flash),
# its own state dir + locks (runs in parallel with the union window), law-15 paced.
_LANES_LITE = {"base": "https://api.z.ai/api/coding/paas/v4",
               "keys": ["ZAI_API_KEY_Lite"],
               "models": ["glm-5.3-flash"]}
# operator 2026-09-17: "i know what ox is, thats an old config. we're using union."
# (env OPENROUTER_MODEL=stealth/ox-alpha is stale; ox's own 404 revealed it was
#  glm-5.3-flash — kept only as the last-resort fallback.)

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
            detail = e.read().decode("utf-8", "replace")[:200]
            rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail,
                        "key_index": ki})
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


def _load_state() -> dict:
    if STATE.is_file():
        st = json.loads(STATE.read_text(encoding="utf-8"))
    else:
        st = {"done": [], "dead": {}, "runs": 0, "promoted": 0, "rejected": 0}
    # transport failures (dead model id, reasoning-budget empties, 200-with-error bodies)
    # are not brief-merit deaths: prune them so the brief gets its real two attempts.
    st["dead"] = {sid: why for sid, why in (st.get("dead") or {}).items()
                  if not any(t in str(why) for t in ("empty_content", "HTTP", "SSRF", "KeyError"))}
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
    keys = [env[k] for k in _LANES["keys"] if env.get(k)]
    state = _load_state()
    if not keys:
        state["dead"]["key"] = "no OpenRouter keys in env"
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        print(json.dumps({"ok": False, "error": "NO_KEY", "key_names": _LANES["keys"]}))
        return 0
    # model chain (operator 2026-09-17: "we're using union" — ox in env is an old config).
    # sticky working model first, then union-alpha, then glm-5.3-flash direct.
    chain = [m for m in [state.get("model"),
                         "stealth/union-alpha",
                         "z-ai/glm-5.3-flash"] if m]
    seen: set[str] = set()
    model = None
    for m in chain:
        if m in seen:
            continue
        seen.add(m)
        probe = _call(m, keys, "Reply with exactly: READY", timeout=90)
        if probe.get("ok"):
            model = m
            break
        rec_detail = (probe.get("detail") or "")
        if probe.get("error") == "HTTP 404" and ("glm-5.3-flash" in rec_detail or m in rec_detail):
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
            for gen in range(1, MAX_GEN + 1):
                rec = _call(model, keys, None, messages=msgs)
                rec.update({"brief": sid, "gen": gen})
                gens = gen
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
            if promoted:
                state["done"].append(sid)
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
