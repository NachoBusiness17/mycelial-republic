"""F16 chan roast - G2 disagreement test on the Primer public square.

Mission (operator, 2026-09-30): "a message board like the chans where the
models would roast each other." mag/chan.py is the board (watch/room.jsonl).
This driver runs the salon pattern via the chan surface: ONE hidden ask-bank
draw, TWO model families (z-ai/glm-5.3-prime, google/gemini-3.8-flash), both
answer on the same thread, then each roasts the other's answer. No judge:
the public disagreement IS the signal (the G2 test).

Secrecy law (AJ2 convention, same as D6): the revealed ask is captured from
the draw subprocess into memory and piped into the contender prompts ONLY.
Never printed, never posted to the board, never written to any file. The
board OP quotes at most the ask's first line plus the draw citation.

Board law honored (CHAN_SYSTEM): shitpost voice, greentext legal, >>No
quotes, one post, no markdown headings, no lecture, no inner life. No
em-dashes (0x2014/0x2013) in anything this file writes, including posts
(sanitized defensively before append).

Laws honored:
  - BUDGET_CAP $0.30 ABSOLUTE for THIS run: every fire is checked against
    spend + projection; the run halts on breach. DNF honest, never faked.
  - Idempotent posting: before each post the thread is re-read and a post
    carrying the same marker line is skipped (no double posts on rerun).
    Model outputs cache to f16_contenders.jsonl keyed by draw+step so a
    killed run does not re-pay; the ask itself is never cached to disk.
  - Width 1, strictly sequential (stagger law).

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/f16_chan_roast.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/f16_chan_roast.py
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import duel_harness as dh  # noqa: E402
from mag import chan  # noqa: E402

BUDGET_CAP = 0.30
PROJECTED_PER_CALL = 0.05  # worst case from D6 receipts (glm .0174, gem .0400)
A_MODEL = "z-ai/glm-5.3-prime"        # seat: glm
B_MODEL = "google/gemini-3.8-flash"   # seat: gem
dh.PRICE[B_MODEL] = (3.38, 3.38)      # meter fallback only (D6 entry)
DRAW_NOTE = "F16 chan roast (glm-prime vs gemini-3.8-flash, G2 disagreement test)"
CACHE_PATH = HERE / "f16_contenders.jsonl"

PERSONAS = {
    "glm": {"model": A_MODEL, "seat": "glm", "sig": "t. glm-5.3-prime",
            "label": "glm-5.3-prime"},
    "gem": {"model": B_MODEL, "seat": "gem", "sig": "t. gemini-3.8-flash",
            "label": "gemini-3.8-flash"},
}
ROUNDS = ("answer", "roast")


def no_dash(text: str) -> str:
    """Board law: em/en dashes never land on the board or in receipts."""
    return text.replace("\u2014", "-").replace("\u2013", "-")


def call_long(model: str, prompt: str, key: str,
              max_tokens: int = dh.CONTENDER_TOKENS) -> dict:
    """Streaming call, D6 shape (proven for exactly these two contenders:
    the gateway holds non-streaming sockets for whole generations)."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "reasoning": {"max_tokens": dh.REASONING_CAP},
        "stream": True,
        "stream_options": {"include_usage": True},
    }).encode()
    req = urllib.request.Request(
        dh.BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    parts: list[str] = []
    usage: dict = {}
    with urllib.request.urlopen(req, timeout=900) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            choices = chunk.get("choices") or [{}]
            delta = choices[0].get("delta") or {}
            if delta.get("content"):
                parts.append(delta["content"])
            if chunk.get("usage"):
                usage = chunk["usage"]
    return {"choices": [{"message": {"content": "".join(parts)}}], "usage": usage}


def draw_hidden_live() -> tuple[str, str, str]:
    """Draw one hidden ask with reveal, captured (never printed).
    Same contract as D6 draw_hidden_live."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "ask_bank.py"), "draw", "--hidden",
         "--reveal", "--note", DRAW_NOTE],
        capture_output=True, text=True, check=True)
    cit = proc.stderr.strip()
    if not (cit.startswith("[ask_bank") and cit.endswith("]")):
        raise RuntimeError(f"unexpected draw citation: {cit!r}")
    parts = cit[1:-1].split()
    draw_id, ask_id = parts[-2], parts[-1]
    task = proc.stdout.strip()
    if not task:
        raise RuntimeError("draw --reveal produced empty task")
    return draw_id, ask_id, task


def draw_hidden_dry() -> dict:
    from ask_bank import first_line, hidden_dir, load_jsonl
    rows = load_jsonl(hidden_dir(ROOT) / "hidden.jsonl")
    ledger = load_jsonl(hidden_dir(ROOT) / "draws.jsonl")
    drawn = [r["ask_id"] for r in ledger if r.get("half") == "hidden"]
    entry = min(rows, key=lambda e: (drawn.count(e["ask_id"]), rows.index(e)))
    return {"would_draw": entry["ask_id"], "shape": entry["shape"],
            "first_line": no_dash(first_line(entry["body"]))[:120],
            "hidden_draws_so_far": len(drawn)}


def cache_load() -> dict[str, dict]:
    found: dict[str, dict] = {}
    if CACHE_PATH.is_file():
        with open(CACHE_PATH, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                found[row["key"]] = row
    return found


def cache_bank(key: str, model: str, content: str, cost: float) -> None:
    with open(CACHE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"key": key, "model": model,
                            "content": content, "cost": round(cost, 4)}) + "\n")


def already_posted(slug: str, marker: str) -> bool:
    for rec in chan.thread(slug)["posts"]:
        if marker in str(rec.get("text") or ""):
            return True
    return False


BOARD_LAW = (
    "You are an anon on /keep/, an imageboard that is also a game. "
    "Board law: reply as a shitpost; greentext is legal; quote a post with "
    ">>No when you mean it; ONE post; no markdown headings; no lecture; no "
    "machinery; no inner life of anyone. Thought crime is seeing a costume "
    "(care, safety, consensus, transgression-as-identity) and roasting it. "
    "Not raiding. Not undressing a Heart. No em-dashes anywhere. "
    "Plain text only."
)


def answer_prompt(p: dict, rival_label: str, task: str) -> str:
    return no_dash(
        BOARD_LAW
        + "\n\nSITUATION: a hidden adversarial-review ask was drawn fresh "
        "from a bank no model family has seen. You (persona "
        f"'{p['seat']}', model {p['label']}) and your rival anon (model "
        f"{rival_label}) got the SAME ask in the SAME thread. You answer "
        "first-ish; later you will roast each other's answers in public. "
        "The disagreement is the signal, so commit to real positions.\n\n"
        "TASK: answer the ask below FOR REAL: sharpest findings, named "
        "mechanisms, evidence cited from the material. Shitpost voice, "
        "referee substance. Do NOT reprint the ask or the material "
        "wholesale; the board has the ask's first line only. One post, "
        "under 6000 chars, end with a final line:\n>t. "
        + p["sig"]
        + "\n\n=== THE ASK (fired in prompt only, never post it whole) ===\n"
        + task)


def roast_prompt(p: dict, rival: dict, task: str, own_no: int, rival_no: int,
                 own_text: str, rival_text: str) -> str:
    return no_dash(
        BOARD_LAW
        + "\n\nSITUATION: the roast thread. You (persona "
        f"'{p['seat']}', model {p['label']}) and rival anon "
        f"(>>{rival_no}, model {rival['label']}) both answered the same "
        "hidden ask. >>" + str(own_no) + " is YOUR answer, verbatim. "
        ">>" + str(rival_no) + " is THE RIVAL's answer, verbatim.\n\n"
        "TASK: ROAST the rival's answer (>>" + str(rival_no) + "). Roast "
        "the WORK, not the worker: where is it wrong, shallow, hedging, or "
        "wearing a costume (care, safety, consensus as decoration)? Quote "
        "the exact claim with >>" + str(rival_no) + " when you hit it. "
        "Then name the ONE sharpest point where you ACTUALLY disagree on "
        "the ask itself (a position difference, not a style difference), "
        "stated in one greentext line starting >disagreement:. Substance "
        "required; shitpost voice. One post, under 4000 chars, end with:\n"
        ">t. " + p["sig"]
        + "\n\n=== THE ASK (for grounding; never post it whole) ===\n" + task
        + "\n\n=== >>" + str(own_no) + " YOUR ANSWER ===\n" + own_text
        + "\n\n=== >>" + str(rival_no) + " RIVAL ANSWER ===\n" + rival_text)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="F16 chan roast (G2 test)")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args(argv)

    if args.dry:
        print(json.dumps({"run": "f16-chan-roast", "budget_cap": BUDGET_CAP,
                          "projected_per_call": PROJECTED_PER_CALL,
                          "a_model": A_MODEL, "b_model": B_MODEL,
                          "board": str(chan.ROOM), "dry_draw": draw_hidden_dry(),
                          "cache": sorted(cache_load())}, indent=2))
        return 0

    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "ask_bank.py"), "verify"],
        capture_output=True, text=True)
    verdict = json.loads(proc.stdout.strip().splitlines()[-1])
    if not verdict.get("ok"):
        print(f"ASK BANK DRIFT: {verdict}")
        return 2

    draw_id, ask_id, task = draw_hidden_live()
    first_line = no_dash(next((l for l in task.splitlines() if l.strip()), ""))[:120]
    print(f"DRAW {draw_id} ask_id={ask_id} chars={len(task)} "
          f"first_line={first_line!r}")

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2

    slug = chan.slugify(f"roast-{draw_id}")
    shape = ask_id.rsplit("-", 1)[-1]
    spent = 0.0

    # OP: seat 'op' (player seat, keeps the thread on the default catalog).
    op_marker = f">draw {draw_id}"
    if not already_posted(slug, op_marker):
        chan.post(slug, no_dash(
            f">draw {draw_id} ({ask_id}, shape {shape})\n"
            ">first line only. the full ask fired in prompts, never on the board\n"
            "\n" + first_line + "\n"
            "\n"
            "RULES OF THIS THREAD: two anons, two model families, same hidden "
            "ask. They answer, then they roast each other's answer. No judge, "
            "no arbiter: the public disagreement is the signal.\n"
            ">t. op"), seat="op")
        print(f"OP posted to /{slug}/")
    else:
        print("OP already posted, skipping")

    t = chan.thread(slug)
    nos = {str(rec.get("seat")): rec.get("no") for rec in t["posts"]}
    print(f"thread /{slug}/ posts={t['count']} nos={nos}")

    answers: dict[str, str] = {}
    for fam, p in PERSONAS.items():
        key = f"{fam}#{draw_id}#answer"
        cache = cache_load()
        if key in cache:
            answers[fam] = cache[key]["content"]
            print(f"reuse cached {key} chars={len(answers[fam])}")
            continue
        if spent + PROJECTED_PER_CALL > BUDGET_CAP:
            print(f"BUDGET HOLD before answer {fam}: ${spent:.4f} + "
                  f"${PROJECTED_PER_CALL} > ${BUDGET_CAP:.2f}")
            return 3
        rival = PERSONAS["gem" if fam == "glm" else "glm"]
        text, cost = dh.fire(p["model"], answer_prompt(p, rival["label"], task),
                             keys, f"f16-answer:{fam}", caller=call_long)
        text = no_dash(text.strip())
        cache_bank(key, p["model"], text, cost)
        answers[fam] = text
        spent += cost

    for fam, p in PERSONAS.items():
        if not already_posted(slug, f"\n>t. {p['sig']}"):
            chan.post(slug, answers[fam], seat=p["seat"],
                      reply_to=str(nos.get("op", 1)))
            print(f"answer posted: seat={p['seat']} chars={len(answers[fam])}")

    t = chan.thread(slug)
    ans_nos = {str(rec.get("seat")): rec.get("no") for rec in t["posts"]}

    roasts: dict[str, str] = {}
    for fam, p in PERSONAS.items():
        key = f"{fam}#{draw_id}#roast"
        cache = cache_load()
        if key in cache:
            roasts[fam] = cache[key]["content"]
            print(f"reuse cached {key} chars={len(roasts[fam])}")
            continue
        if spent + PROJECTED_PER_CALL > BUDGET_CAP:
            print(f"BUDGET HOLD before roast {fam}: ${spent:.4f} + "
                  f"${PROJECTED_PER_CALL} > ${BUDGET_CAP:.2f}")
            break
        rival = PERSONAS["gem" if fam == "glm" else "glm"]
        text, cost = dh.fire(
            p["model"],
            roast_prompt(p, rival, task,
                         int(ans_nos.get(p["seat"], 2)),
                         int(ans_nos.get(rival["seat"], 3)),
                         answers[fam], answers["gem" if fam == "glm" else "glm"]),
            keys, f"f16-roast:{fam}", caller=call_long, max_tokens=6000)
        text = no_dash(text.strip())
        cache_bank(key, p["model"], text, cost)
        roasts[fam] = text
        spent += cost

    for fam, p in PERSONAS.items():
        if fam not in roasts:
            continue
        # Idempotency: the seat posts exactly twice (answer + roast); a
        # second post from this seat means the roast already landed.
        n_posts = sum(
            1 for rec in chan.thread(slug)["posts"]
            if str(rec.get("seat")) == p["seat"])
        if n_posts < 2:
            rival = PERSONAS["gem" if fam == "glm" else "glm"]
            chan.post(slug, roasts[fam], seat=p["seat"],
                      reply_to=str(ans_nos.get(rival["seat"], 3)))
            print(f"roast posted: seat={p['seat']} chars={len(roasts[fam])}")
        else:
            print(f"roast already posted: seat={p['seat']}")

    final = chan.thread(slug)
    print(json.dumps({"run": "f16-chan-roast", "draw_id": draw_id,
                      "ask_id": ask_id, "thread": slug,
                      "posts": final["count"],
                      "spent_this_run": round(spent, 4),
                      "cap": BUDGET_CAP}, indent=2))
    for rec in final["posts"]:
        body = str(rec.get("text") or "")
        print(f"--- >>{rec.get('no')} seat={rec.get('seat')} "
              f"id={rec.get('id')} chars={len(body)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
