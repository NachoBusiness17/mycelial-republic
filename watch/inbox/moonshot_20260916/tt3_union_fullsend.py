# TT3 UNION FULLSEND driver (moonshot 20260916). One turn per invocation:
#   .venv\Scripts\python.exe tt3_union_fullsend.py <turn_no 1..4>
# Laws: OPENROUTER_API_KEY via mag.flight_recorder.load_env (never printed, never logged) ·
# non-streaming, timeout 300s (>=180s law) · 429/402 storm -> retry w/ backoff, degrade,
# file what landed · $0 · verbatim answers filed to TT3_TURN<N>_ANSWER.md.
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
HERE = os.path.join(ROOT, "watch", "inbox", "moonshot_20260916")
sys.path.insert(0, ROOT)
from mag.flight_recorder import load_env, record_call, guard_endpoint  # noqa: E402

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "stealth/union-alpha"
STATE_PATH = os.path.join(HERE, "tt3_conversation_state.json")
CTX_PATH = os.path.join(HERE, "TT3_CONTEXT.md")
TIMEOUT = 300
MAX_ATTEMPTS = 4

PROMPTS = {
    1: ("A fleet keeps an append-only ledger and writes sealed predictions before "
        "experiments. In what rigorous sense is this retrocausal steering, and in what "
        "sense is it not? Be brutal about the distinction."),
    2: ("Translate a pre-registered falsifier into a two-state-vector-style description: "
        "final boundary condition constraining the initial experiment. Where does the math "
        "allow it and where does it become poetry?"),
    3: ("Design the cheapest instrument (<= $100, hobby tier) that would make a believer "
        "UPDATE — not convince, update. It must not be able to pass on selection effect "
        "alone."),
    4: ("The riddled stone parable: a stone covered in riddles that only read correctly "
        "after the events they describe. What is the minimal honest version of that "
        "device?"),
}

SYSTEM_TEXT = (
    "You are Union Alpha, the open judgment seat of a small multi-agent research fleet. "
    "Below is the working context the fleet fed you. Take it seriously but audit it as "
    "you go: the fleet's whole discipline is keeping REAL MATH / REAL PHYSICS / "
    "BUILDABLE / METAPHOR labels on things, and it wants you to hold that line, not "
    "soothe it. Answer with substance; no filler, no restating the prompt.\n\n"
    "===== CONTEXT PACK =====\n"
)


def call_union(messages, key):
    """One non-streaming call. Returns parsed dict (error-shaped on HTTP errors)."""
    guard_endpoint(ENDPOINT, {"openrouter.ai"})
    body = {"model": MODEL, "temperature": 0.4, "max_tokens": 16000,
            "stream": False, "messages": messages}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "User-Agent": "mag-tt3-retrocausal/1.0",
            "HTTP-Referer": "https://local-sovereign-agent.invalid",
            "X-Title": "Mag TT3 Retrocausal Fullsend",
        })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"error": {"code": "HTTP%d" % e.code}}
    except Exception as e:  # transport-level: shape it so the recorder row is typed
        return {"error": {"code": type(e).__name__, "message": str(e)[:160]}}


def extract(resp):
    """-> (text, finish_reason, usage, err_head)."""
    if resp.get("error"):
        return None, None, None, json.dumps(resp["error"])[:300]
    choices = resp.get("choices") or [{}]
    msg = choices[0].get("message") or {}
    text = msg.get("content")
    if not text:
        text = resp.get("choices", [{}])[0].get("text")
    return (text or "").strip(), choices[0].get("finish_reason"), resp.get("usage"), None


def main():
    turn = int(sys.argv[1])
    if turn not in PROMPTS:
        print("turn must be 1..4")
        sys.exit(2)
    env = load_env(ROOT)
    key = env.get("OPENROUTER_API_KEY", "")
    if not key:
        print("STATUS: NO_KEY")
        sys.exit(2)

    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as fh:
            state = json.load(fh)
    else:
        state = {"messages": [{"role": "system",
                               "content": SYSTEM_TEXT + open(CTX_PATH, encoding="utf-8").read()}]}

    user_content = PROMPTS[turn]
    note_path = os.path.join(HERE, "tt3_turn%d_note.txt" % turn)
    if os.path.isfile(note_path):
        note = open(note_path, encoding="utf-8").read().strip()
        if note:
            user_content += "\n\n[Late-landing lane intel, appended before your answer]\n" + note

    convo = list(state["messages"])
    convo.append({"role": "user", "content": user_content})

    attempts, text, finish, usage = [], None, None, None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        t0 = time.perf_counter()
        try:
            status, resp = record_call(
                call_union, "moonshot-tt3", MODEL, "tt3-retrocausal",
                messages=convo, key=key)
        except Exception as e:  # recorder re-raises; row already emitted
            attempts.append({"attempt": attempt, "ok": False,
                             "detail": "%s: %s" % (type(e).__name__, str(e)[:160]),
                             "latency_ms": int((time.perf_counter() - t0) * 1000)})
            break
        latency_ms = int((time.perf_counter() - t0) * 1000)
        t, fin, us, err_head = extract(resp)
        if t:
            text, finish, usage = t, fin, us
            attempts.append({"attempt": attempt, "ok": True, "chars": len(t),
                             "finish_reason": fin, "usage": us,
                             "latency_ms": latency_ms})
            break
        attempts.append({"attempt": attempt, "ok": False, "err_head": err_head,
                         "latency_ms": latency_ms})
        if attempt < MAX_ATTEMPTS:
            time.sleep(20 * attempt)  # storm law: back off, degrade gracefully

    state["messages"] = convo + ([{"role": "assistant", "content": text}] if text else [])
    state.setdefault("attempts", {})[str(turn)] = attempts
    with open(STATE_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)

    if text:
        out_path = os.path.join(HERE, "TT3_TURN%d_ANSWER.md" % turn)
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# TT3 Turn %d — Union Alpha (verbatim)\n\n" % turn)
            fh.write("**Prompt:** %s\n\n---\n\n%s\n" % (user_content[:400], text))
        print("STATUS: TURN%d_FILED chars=%d finish=%s latency_ms=%s -> %s"
              % (turn, len(text), finish, attempts[-1]["latency_ms"], out_path))
    else:
        print("STATUS: TURN%d_NO_CONTENT attempts=%s (file what landed)"
              % (turn, json.dumps(attempts)))


if __name__ == "__main__":
    main()
