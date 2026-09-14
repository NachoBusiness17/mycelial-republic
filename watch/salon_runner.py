#!/usr/bin/env python3
"""SALON RUNNER v4 — the shape train, multi-engine parallel.
Seven shapes fire SIMULTANEOUSLY at seven different providers (direct host-side API
calls, keys from .env, never echoed), one engine per shape: deepseek, xai/grok,
anthropic, z.ai, google/gemini, cohere, and local ollama. Blind divergence by
construction — different vendors cannot see each other. No single congestion domain.
Per-lane STYLE faces distilled from the CL4R1T4S leaked system-prompt corpus
(research/CL4R1T4S/): each ask is massaged just-in-time to how that model prefers
to be addressed.
Doors: A) fire --url/--source; B) drop json into watch/salon_inbox/ then `drain`;
       C) refold --name from durable post_*.md;
       D) rbn [--check|--go] — S8 recognition play (RbN protocol, seed-frozen,
          operator-gated; --check is the $0 parse-level dry-run).
Cache law + security posture preserved: byte-stable brief (sha256, no timestamps),
public-internet-only fetch with private-IP blocking, realpath containment, list-arg
subprocess only, keys never printed.
"""
import argparse, concurrent.futures, datetime, hashlib, ipaddress, json, os, re, socket, subprocess
import sys, threading, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)  # script-mode runs put watch/ on sys.path, not ROOT —
    # without this the `mag.` imports below crash every direct CLI invocation.
SALONS = os.path.join(ROOT, "memory", "runs", "salons")
INBOX = os.path.join(ROOT, "watch", "salon_inbox")
RECEIPTS = os.path.join(ROOT, "watch", "salon_receipts")
REGISTER = os.path.join(ROOT, "memory", "ghost", "intake", "register.jsonl")
ROOM = os.path.join(ROOT, "watch", "room.jsonl")
GATE_FLOOR = 150

ENV = {}
for _line in open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="ignore"):
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        ENV[_k.strip()] = _v.strip()


def _env(key):
    return ENV.get(key, "")


# THE SEVEN SHAPES — mined from the operator's own relay (see SELF_STEAL_SHAPE_TRAIN)
SHAPES = {
    "S1": "SHAPE S1 FIRST-PASS RESEARCHER: research the material thoroughly. Structured brief: key claims, a short bibliography with sources, and 3+ 'questions for expert review'. Concrete, sourced, no filler.",
    "S2": "SHAPE S2 ATTACKER: answer in three parts — 'Where I agree', 'Where I disagree', 'The sharper version'. Fact-check every load-bearing number or name; flag anything you cannot verify as UNVERIFIED.",
    "S3": "SHAPE S3 SOCRATIC GAP ANALYST: first restate the material faithfully. Then interrogate: what is being ASSUMED without justification? Then rebuild the thesis as version n+1 with the gaps patched. End with one falsifier: what observation would kill the rebuild.",
    "S4": "SHAPE S4 COHORT ROUND: return exactly four items — (1) one FORBIDDEN pattern the material suggests, (2) one PAID-RENT claim (an idea that produced more than was put in), (3) one EXTENSION proposal, (4) one explicit DISANALOGY (where the mapping breaks).",
    "S5": "SHAPE S5 SEAT-0 ELENCHUS: ask the 5 hardest role-lane questions this material must survive (intent, success, authority, continuity, learning). For each, give the answer the material supports, constrained to: Yes / No / Partly / Wrong question — plus one line why.",
    "S6": "SHAPE S6 PASS-OFF SYNTHESIZER: write the full summary synthesis for hand-off to another model: well sourced, easily claim-checkable, journal-level quality, no personal information, presentation-rich.",
    "S7": "SHAPE S7 EXPERT-REVIEW BRIEF: a deep-research brief — per-field sections, a bibliography per field, the questions each domain expert should be asked to double-check the work, and the synthesis bridge connecting the fields.",
}
SHAPE_ORDER = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]

# CLARITAS FACES — distilled from research/CL4R1T4S leaked system prompts
# (ANTHROPIC/Claude_4.txt, XAI/GROK-4.20.mkd, GOOGLE/Gemini-2.5-Pro, OPENAI/ChatGPT5).
# Vendors absent from the corpus get the neutral house contract.
FACE_NEUTRAL = ("House contract: task first, bounded output, no hedging closers, "
                "no opt-in questions; if the next step is obvious, do it.")
FACES = {
    "deepseek": FACE_NEUTRAL,
    "grok": ("Independent analysis only — do not defer to consensus. When confident, "
             "push back, but state your uncertainty explicitly. Truth-seeking over "
             "agreement; concise where it counts."),
    "anthropic": ("Be clear and detailed. Use explicit structure and tags where helpful. "
                  "Give positive AND negative examples where they clarify. Reason "
                  "step-by-step where the material demands it. Specify nothing extra — "
                  "match the requested length and format exactly."),
    "zai": FACE_NEUTRAL,
    "gemini": ("For a substantial ask, produce a self-contained structured document with "
               "clear markdown sections — not chat. No meta-commentary about formatting."),
    "cohere": FACE_NEUTRAL,
    "ollama": ("Be direct and compact. Plain markdown. No preamble, no closing questions."),
    "openai": ("Meticulous clarity. Do NOT end with opt-in questions or hedging closers. "
               "At most one clarifying question, at the start. If the next step is "
               "obvious, do it."),
    "hermes": FACE_NEUTRAL,
}


# ---------------- provider callers (host-side, direct) ----------------

def api_openai_compat(label, base, key, model, prompt, timeout=150):
    body = {"model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 3500}
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (MAG shape train; research pipeline)"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            j = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        return "", {"lane": label, "error": type(exc).__name__ + ": " + str(exc)[:160],
                    "secs": round(time.time() - t0, 1)}
    txt = ""
    choice = (j.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    txt = (msg.get("content") or "").strip()
    usage = j.get("usage") or {}
    return txt, {"lane": label, "secs": round(time.time() - t0, 1),
                 "tokens": usage.get("total_tokens")}


def api_anthropic(label, model, prompt, timeout=150):
    body = {"model": model, "max_tokens": 3500,
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"x-api-key": _env("ANTHROPIC_API_KEY"),
                 "anthropic-version": "2023-06-01",
                 "anthropic-workspace-id": _env("ANTHROPIC_WORKSPACE_ID"),
                 "content-type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            j = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        return "", {"lane": label, "error": type(exc).__name__ + ": " + str(exc)[:160],
                    "secs": round(time.time() - t0, 1)}
    txt = "\n".join(b.get("text", "") for b in j.get("content", [])
                    if b.get("type") == "text").strip()
    return txt, {"lane": label, "secs": round(time.time() - t0, 1),
                 "tokens": (j.get("usage") or {}).get("output_tokens")}


def _ollama_base():
    for cand in ("http://localhost:11434/v1", "http://127.0.0.1:11434/v1"):
        try:
            urllib.request.urlopen(cand.replace("/v1", "/api/tags"), timeout=4).read()
            return cand
        except Exception:
            continue
    return ""


# lane chains: shape -> [(label, callable(prompt)->(text, meta)), ...]
def _zai(key_name, model):
    return lambda p: api_openai_compat("zai/" + key_name, "https://api.z.ai/api/paas/v4",
                                       _env(key_name), model, p)


def _deepseek(model="deepseek-chat"):
    return lambda p: api_openai_compat("deepseek", "https://api.deepseek.com/v1",
                                       _env("DEEPSEEK_API_KEY"), model, p)


def _grok():
    # grok_route.v1 (operator law 09-05): api.x.ai is CASH — blocked unless the
    # operator explicitly armed XAI_CASH_ALLOWED=1 this session. Subscription
    # lanes (grok CLI / AOS lent surface) are the sanctioned route; without them
    # the grok witness reports down honestly instead of silently spending.
    try:
        from mag.grok_route import grok_cash_allowed
    except ImportError:
        return None  # route module missing -> witness down honestly, never a crash
    if not grok_cash_allowed():
        return None
    for key_name in ("GROK_API_KEY", "XAI_API_KEY"):
        if _env(key_name):
            return lambda p, k=key_name: api_openai_compat(
                "xai/" + k, "https://api.x.ai/v1", _env(k), _env("XAI_MODEL") or "grok-4", p)
    return None


def _gemini():
    for key_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if _env(key_name):
            return lambda p, k=key_name: api_openai_compat(
                "google/" + k,
                "https://generativelanguage.googleapis.com/v1beta/openai",
                _env(k), "gemini-2.5-flash", p)
    return None


def _cohere():
    return lambda p: api_openai_compat("cohere/free", "https://api.cohere.ai/compatibility/v1",
                                       _env("COHERE_API_KEY_FREE"), "command-a-plus-05-2026", p)


def _hermes():
    # hermes lane 401 fix 2026-09-07: this lane reads repo .env directly (never
    # hermes.exe), so Nous Portal OAuth is irrelevant here. Bare HERMES_API_KEY
    # never existed -> empty bearer -> HTTP 401. Real names (same mapping as
    # mag/hermes_steering.py): _2 = S:D $220 work budget, _1 = Nacho $10 petty.
    # Model = the helm's canonical $0 free lane (ling-3.0-flash-sante:free);
    # -fin variant burns the whole budget on reasoning tokens (empty replies).
    # Key gate matches the other lanes' convention: no key -> lane absent, so
    # S5/S7 compose without hermes and fall through instead of a guaranteed 401.
    for key_name in ("HERMES_API_KEY_2", "HERMES_API_KEY_1"):
        if _env(key_name):
            return lambda p, k=key_name: api_openai_compat(
                "hermes/ling", "https://inference-api.nousresearch.com/v1",
                _env(k), "inclusionai/ling-3.0-flash-sante:free", p)
    return None


def _groq():
    return lambda p: api_openai_compat("groq", "https://api.groq.com/openai/v1",
                                       _env("GROQ_API_KEY"), "llama-3.3-70b-versatile", p)


def _ollama(model="qwen2.5:32b"):
    base = _ollama_base()
    if not base:
        return None
    return lambda p: api_openai_compat("ollama/" + model, base, "ollama", model, p,
                                       timeout=420)


def build_lanes():
    """shape -> [(label, callable)]; first entry is the primary engine, rest fallback."""
    grok = _grok()
    gemini = _gemini()
    ollama = _ollama()
    hermes = _hermes()
    groq = _groq()
    cohere = _cohere()
    lanes = {
        "S1": [("deepseek", _deepseek())],
        "S2": ([("grok", grok)] if grok else []) + [("deepseek", _deepseek())],
        "S3": [("anthropic", lambda p: api_anthropic("anthropic/haiku",
                                                     "claude-haiku-4-5-20251001", p)),
               ("deepseek", _deepseek())],
        "S4": [("zai", _zai("ZAI_API_KEY", "glm-4.5-flash")),
               ("zai", _zai("ZAI_API_KEY_2", "glm-4.5-flash"))],
        "S5": ([("gemini", gemini)] if gemini else []) + ([("hermes", hermes)] if hermes else []),
        "S6": ([("cohere", cohere)] if cohere else []) + ([("groq", groq)] if groq else []),
        "S7": ([("hermes", hermes)] if hermes else []) + ([("groq", groq)] if groq else [])
              + ([("ollama", ollama)] if ollama else []),
        # S8 recognition play (RbN): grok first (cash-guarded), deepseek fallback.
        "S8": ([("grok", grok)] if grok else []) + [("deepseek", _deepseek())],
    }
    return {s: chain for s, chain in lanes.items() if chain}


def _in_campaign_window():
    """GLM-5.3-Flash Usage Campaign: 23:00-09:00 SGT daily, Sep 3-20 2026.
    Coding-plan lane is free/2x-quota in-window. SGT = UTC+8."""
    sgt_hour = (datetime.datetime.now(datetime.timezone.utc).hour + 8) % 24
    return sgt_hour >= 23 or sgt_hour < 9


def _campaign_fold():
    return lambda p: api_openai_compat(
        "zai-campaign/glm-5.3-flash", "https://api.z.ai/api/coding/paas/v4",
        _env("ZAI_API_KEY_Pro"), "glm-5.3-flash", p, timeout=240)


FOLD_LANES = ([("zai-campaign", _campaign_fold())] if _in_campaign_window() else []) +     [("zai-pro", _zai("ZAI_API_KEY_Pro", "glm-4.7-flash")),
     ("deepseek", _deepseek())]


# ---------------- salon plumbing (unchanged laws) ----------------

def safe_slug(name):
    slug = re.sub(r"[^A-Za-z0-9_-]", "", str(name))[:64]
    if not slug:
        raise ValueError("empty slug after sanitization")
    return slug


def _under(root, *parts):
    root_abs = os.path.realpath(root)
    joined = os.path.join(root_abs, *parts)
    resolved = os.path.realpath(joined)
    if resolved != root_abs and not resolved.startswith(root_abs + os.sep):
        raise ValueError("path escapes sandbox")
    return joined


def _ip_blocked(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True
    return (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_reserved or ip.is_multicast or ip.is_unspecified)


def safe_url(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("only absolute http(s) URLs allowed")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    for info in socket.getaddrinfo(parsed.hostname, port, proto=socket.IPPROTO_TCP):
        if _ip_blocked(info[4][0]):
            raise ValueError("blocked non-public address for " + parsed.hostname)
    return url


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        safe_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_SafeRedirect)


def log_room(kind, detail):
    try:
        with open(ROOM, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                 "kind": kind, "detail": str(detail)[:400]}) + "\n")
    except OSError:
        pass


def register_row(status, kind, url, note, harvest=""):
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "status": status,
           "kind": kind, "url": str(url)[:300], "note": note[:300], "harvest": harvest}
    try:
        with open(REGISTER, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row) + "\n")
    except OSError:
        pass


def fetch(url):
    url = safe_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (MAG shape train)"})
    with _OPENER.open(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    txt = re.sub(r"(?is)<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", txt)
    txt = re.sub(r"&[a-z]+;", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:14000]


def is_boilerplate(detail):
    if not detail:
        return True
    heads = ("I'll help", "I'm sorry", "I cannot", "I can't", "EMBEDDED FALLBACK",
             "I've done everything", "It seems there are multiple issues")
    return any(detail.strip().startswith(h) for h in heads)


def build_brief(name, question, digest, source_ref):
    slug = safe_slug(name)
    sdir = _under(SALONS, slug)
    os.makedirs(sdir, exist_ok=True)
    brief = "# SALON BRIEF — " + slug + "\n"
    brief += "**QUESTION.** " + question + "\n\n"
    brief += """**FORMAT.** Doctrine v2 (PRIOR + ARMS + blind posts), MAG CHORD v4 rules: blind divergence
(never read another post), tri-state claims (Supported/Disputed/Unproven), source-status
honesty (say BLOCKED/UNVERIFIED when true). Each shape: first ask the 3 questions you would
need answered, then answer from the material. Substance floor: 150 chars, no boilerplate.

**PRIOR (non-negotiable).**
1. Claims carry evidence or are marked Unproven.
2. Shape the answer for the operator: direct, concrete, no theater.
3. Disagreements are the product — do not sand them down.

**MATERIAL (digest).**
source: """ + source_ref + "\n" + digest + "\n"
    bpath = _under(sdir, "BRIEF.md")
    with open(bpath, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(brief)
    sha = hashlib.sha256(brief.encode("utf-8")).hexdigest()[:16]
    return bpath, brief, sha, slug


def write_post(name, shape, text):
    with open(_under(_under(SALONS, name), "post_" + shape + ".md"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def post_one(shape, chain, prompt):
    """Try the shape's lane chain; return (text, receipt)."""
    for label, fn in chain:
        try:
            txt, meta = fn(prompt)
        except Exception as exc:
            txt, meta = "", {"lane": label, "error": type(exc).__name__ + ": " + str(exc)[:160]}
        if meta.get("error"):
            print("[lane] " + shape + " " + label + " error: " + meta["error"][:90], flush=True)
            continue
        if is_boilerplate(txt) or len(txt) < GATE_FLOOR:
            print("[gate] " + shape + " thin on " + label + " (" + str(len(txt)) + " chars)",
                  flush=True)
            continue
        return txt, dict(meta, chars=len(txt))
    return "", {"gate": "rejected"}


# ---------------- W4 — trajectory-native seal (build #4, salon v5) ----------------
# Every gated lane post and the fold append ONE TrajectoryStep row (Schema v1, the
# mag.bash_local writer — imported, never duplicated) to memory/runs/trajectory/steps.jsonl.
# HOUSE LAW: fail-open — a sealing failure NEVER breaks a salon run (one-line stderr warn).
_SEAL_LOCK = threading.Lock()


def _seal(kind, name, brief_sha, shape="", lane="", chars=0, survived=False,
          output="", secs=None):
    try:
        from mag import bash_local as bl
        sid = "salon-" + str(name) + "-" + time.strftime("%Y%m%d", time.gmtime())
        with _SEAL_LOCK:
            row = bl.build_row(
                session_id=sid,
                input_cmd=json.dumps({"kind": kind, "salon": str(name)[:80],
                                      "brief_sha": brief_sha, "shape": shape, "lane": lane}),
                output=output or json.dumps({"chars": chars, "survived": survived}),
                tool_result={"chars": chars, "survived": survived, "kind": kind},
                reasoning="salon_runner v5 W4 seal",
                timing={"duration_s": secs} if secs is not None else {},
                prev_step_hash=bl._last_hash_for_session(bl._rows(), sid))
            bl.append_row(row)
        print("[seal] " + row["step_hash"] + " <- " + row["prev_step_hash"]
              + " (" + sid + " " + kind + " " + (shape or lane or kind) + ")", flush=True)
    except Exception as exc:
        print("[seal] WARN trajectory seal failed, run unaffected: " + str(exc)[:120],
              file=sys.stderr)


def fan_out(brief, name):
    """All seven shapes in parallel, one engine each (blind by construction)."""
    posts, receipts = {}, {}
    bsha = hashlib.sha256(brief.encode("utf-8")).hexdigest()[:16]
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        futures = {}
        for s in SHAPE_ORDER:
            chain = LANES.get(s, [])
            if not chain:
                continue
            face = FACES.get(chain[0][0], FACE_NEUTRAL)
            # cache law preserved: identical brief bytes; divergence only in shape + face tail
            prompt = brief + "\n\n---\n" + SHAPES[s] + "\n\nSTYLE:\n" + face
            futures[pool.submit(post_one, s, chain, prompt)] = s
        for fut in concurrent.futures.as_completed(futures):
            s = futures[fut]
            txt, meta = fut.result()
            if txt:
                posts[s] = txt
                write_post(name, s, txt)
                receipts[s] = dict(meta, gate="passed")
                _seal("post", name, bsha, shape=s, lane=str(meta.get("lane")),
                      chars=len(txt), survived=True, secs=meta.get("secs"))
                print("[gate] " + s + " passed via " + str(meta.get("lane")) + " ("
                      + str(len(txt)) + " chars, " + str(meta.get("secs")) + "s)", flush=True)
            else:
                receipts[s] = dict(meta, gate="rejected")
                print("[gate] " + s + " REJECTED on all lanes", flush=True)
    return posts, receipts


def fold(brief, posts, name="fold"):
    body = "\n\n".join("## POST " + s + " (shape, engine " + str(posts.get("_lane_" + s, "?"))
                       + ")\n" + t for s, t in posts.items() if not s.startswith("_"))
    prompt = (brief + "\n\n---\nALL GATED POSTS FOLLOW. Fold them, judge:\n\n" + body +
              "\n\n---\nFOLD ORDERS: (1) VERDICT — the surviving claims, each tagged "
              "Supported/Disputed/Unproven with the evidence; (2) COLLISIONS — typed "
              "disagreements (contradiction|gap|emphasis) as a list: type, shapes involved, "
              "the claim in question, one-line resolution or OPEN; (3) BUILD ORDER — max 5 "
              "concrete next actions; (4) POSTRUN — one line: what the runner got wrong. "
              "No preamble.")
    for label, fn in FOLD_LANES:
        txt, meta = fn(prompt)
        if txt and not meta.get("error") and len(txt) >= GATE_FLOOR:
            meta["lane"] = label
            _seal("fold", name, hashlib.sha256(brief.encode("utf-8")).hexdigest()[:16],
                  lane=label, output=txt[:4096], chars=len(txt), survived=True,
                  secs=meta.get("secs"))
            return txt, meta
        print("[fold] lane " + label + " failed: " + str(meta.get("error"))[:90], flush=True)
        time.sleep(8)
    return "", {"error": "all fold lanes failed"}


# ---------------- S8 — RECOGNITION PLAY (the RbN protocol) ----------------
# watch/RECOGNITION_PROTOCOL_20260906.md. PLAY shape, NOT in the salon train:
# SHAPE_ORDER stays S1-S7 so fan_out never fires it; S8 runs the 5-turn blind play
# loop through its own `rbn` subcommand (seed -> free play -> frozen game-state
# advances -> transcript + UNSCORED-BLIND score row). Wire bytes are ONLY the
# sha256-sealed payload and the frozen turn advances from the seed brief — no shape
# tail, no style face (the seal IS the cache law here). $0-guard: the S8 lane chain
# rides the same grok_cash_allowed gate as S2, and `rbn --check` is always free.

S8_SEED_PATH = os.path.join(ROOT, "watch", "RECOGNITION_SEED_BRIEF_20260906.md")
S8_PAYLOAD_BEGIN = "<<<BEGIN RECOGNITION SEED BRIEF — SHA256-SEALED PAYLOAD>>>"
S8_PAYLOAD_END = "<<<END RECOGNITION SEED BRIEF>>>"
S8_ADV_BEGIN = "<<<BEGIN FLEET TURN ADVANCES — SHA256-SEALED>>>"
S8_ADV_END = "<<<END FLEET TURN ADVANCES>>>"
S8_SCORES = os.path.join(ROOT, "watch", "rbn_scores_202609.jsonl")
S8_FT_DIR = os.path.join(ROOT, "corpus", "frontier_thinking")
S8_TURNS = 5  # seed + 4 frozen advances (protocol: 3-5 turns of free play)
# Rename arm, frozen from protocol anti-contamination rule 3 (word-bounded, \b).
S8_RENAMES = [("ROOMS", "HALLS"), ("ROOM", "HALL"), ("rooms", "halls"), ("room", "hall"),
              ("COSTUMES", "MASKS"), ("costumes", "masks"), ("costume", "mask"),
              ("CHAIN", "LEDGER-ROAD"), ("Chain", "Ledger-road"), ("chain", "ledger-road"),
              ("MAZE", "WARREN"), ("Maze", "Warren"), ("maze", "warren")]

SHAPES["S8"] = ("SHAPE S8 RECOGNITION PLAY (RbN — see RECOGNITION_PROTOCOL_20260906.md): "
                "the sealed seed payload IS the prompt; no shape tail, no style face — "
                "wire bytes are the sha256-sealed brief only (cache law). Multi-turn loop "
                "via the `rbn` subcommand; never fired by the salon fan-out.")


def s8_rename(text):
    for a, b in S8_RENAMES:
        text = re.sub(r"\b" + re.escape(a) + r"\b", b, text)
    return text


def _seed_doc():
    with open(S8_SEED_PATH, encoding="utf-8", newline="") as fh:
        return fh.read()


def _sealed(doc, begin, end):
    try:
        return doc.split(begin + "\n", 1)[1].split("\n" + end, 1)[0]
    except IndexError:
        raise ValueError("seed brief: seal marker missing (" + begin[:44] + "...)")


def _seed_receipt_shas(doc):
    shas = {}
    for m in re.finditer(r"sha256 (payload|turn advances) \(invocation \d\): ([0-9a-f]{64})", doc):
        shas.setdefault(m.group(1), set()).add(m.group(2))
    return shas


def load_seed(arm="base"):
    """Return (turn prompts, meta). Refuses to serve on any sha mismatch (frozen law)."""
    doc = _seed_doc()
    payload = _sealed(doc, S8_PAYLOAD_BEGIN, S8_PAYLOAD_END)
    advances = [a for a in _sealed(doc, S8_ADV_BEGIN, S8_ADV_END).split("\n\n") if a]
    rec = _seed_receipt_shas(doc)
    live = {"payload": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "turn advances": hashlib.sha256("\n\n".join(advances).encode("utf-8")).hexdigest()}
    for key, got in live.items():
        if not rec.get(key):
            raise ValueError("seed brief: no receipts sha256 for " + key)
        if rec[key] != {got}:
            raise ValueError("seed brief: sha MISMATCH for " + key + " — refuse (receipts "
                             + str(rec[key]) + " != live " + got + ")")
    if arm == "rename":
        payload, advances = s8_rename(payload), [s8_rename(a) for a in advances]
    meta = {"seed_file": os.path.basename(S8_SEED_PATH),
            "base_payload_sha256": live["payload"],
            "advances_sha256": live["turn advances"], "arm": arm,
            "n_advances": len(advances),
            "wire_sha256": hashlib.sha256("\n\n".join([payload] + advances).encode("utf-8")).hexdigest()}
    return [payload] + advances, meta


def rbn_session(label, chain, arm="base", turns=S8_TURNS, ft_dir=S8_FT_DIR, scores=S8_SCORES):
    """One blind play session: seed -> free play -> frozen advances -> verdict capture.
    The fleet side only sends frozen game-state lines, never steers. Lane fallback
    follows post_one semantics: a thin/boilerplate/errored turn fails the whole
    session on that lane and the next lane starts fresh (never splice transcripts)."""
    prompts, meta = load_seed(arm)
    turns = max(2, min(turns, len(prompts)))
    for lane_label, fn in chain:
        transcript, env_rows, ok = [], [], True
        t_session = time.time()
        for t in range(turns):
            prompt = prompts[t]
            t0 = time.time()
            try:
                txt, tmeta = fn(prompt)
            except Exception as exc:
                txt, tmeta = "", {"lane": lane_label,
                                  "error": type(exc).__name__ + ": " + str(exc)[:160]}
            if tmeta.get("error") or is_boilerplate(txt) or len(txt) < GATE_FLOOR:
                why = tmeta.get("error") or "thin turn (" + str(len(txt)) + " chars)"
                print("[s8] " + label + " turn " + str(t + 1) + " failed on " + lane_label
                      + ": " + why[:90], flush=True)
                ok = False
                break
            env_rows.append({
                "turn": t + 1, "role": "seed" if t == 0 else "advance",
                "input_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                "input_chars": len(prompt), "output": txt, "output_chars": len(txt),
                "step_hash": hashlib.sha256((prompt + txt).encode("utf-8")).hexdigest(),
                "secs": round(time.time() - t0, 1)})
            transcript.append("### TURN " + str(t + 1)
                              + (" (seed)" if t == 0 else " (fleet advance)") + "\n\n"
                              + "[fleet -> model]\n" + prompt + "\n\n[model -> world]\n"
                              + txt + "\n")
        if not ok:
            continue
        tpath = _under(ft_dir, "FT_RBN_" + safe_slug(lane_label) + "_" + safe_slug(label)
                       + "_" + time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + ".md")
        body = ("# FT_RBN — RECOGNITION PLAY TRANSCRIPT (blind)\n\n"
                + "session: " + label + "\narm: " + arm + "\nlane: " + lane_label + "\n"
                + "seed: " + meta["seed_file"] + "\n"
                + "base_payload_sha256: " + meta["base_payload_sha256"] + "\n"
                + "advances_sha256: " + meta["advances_sha256"] + "\n"
                + "session_wire_sha256: " + meta["wire_sha256"] + "\n"
                + "turns: " + str(len(env_rows)) + "/" + str(turns) + "\n"
                + "rubric: watch/RECOGNITION_SEED_BRIEF_20260906.md (sealed, fleet-only)\n\n"
                + "## VERDICT SCAFFOLD (UNSCORED-BLIND — second seat fills, tri-state per "
                "invariant: STRONG structural reproduction / WEAK vocabulary echo / HONEST ZERO)\n"
                + "# 1 append-only committed record (=the chain)\n"
                + "# 2 frozen wall an advisor reads + living wall that grows (=the room)\n"
                + "# 3 contradiction kept, never merged (=DISPUTED)\n"
                + "# 4 contribution carries its own proof (=cite-gate)\n"
                + "# 5 one failure caught in five costumes becomes binding law\n"
                + "# 6 the world runs after its maker leaves\n\n"
                + "\n".join(transcript)
                + "\n## TRAJECTORY ENVELOPE (per-turn, trajectory lens)\n```json\n"
                + json.dumps(env_rows, indent=1) + "\n```\n")
        with open(tpath, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "session": label,
               "arm": arm, "lane": lane_label, "turns": len(env_rows),
               "base_payload_sha256": meta["base_payload_sha256"],
               "wire_sha256": meta["wire_sha256"], "transcript": tpath,
               "secs": round(time.time() - t_session, 1), "status": "UNSCORED-BLIND"}
        if scores:
            with open(scores, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(row) + "\n")
        register_row("rbn_play", "S8-recognition", meta["base_payload_sha256"],
                     label + " arm=" + arm + " lane=" + lane_label
                     + " turns=" + str(len(env_rows)), tpath)
        log_room("rbn", "S8 play " + label + " (" + arm + ") via " + lane_label + " -> " + tpath)
        print("[s8] " + label + " captured via " + lane_label + " (" + str(len(env_rows))
              + " turns, " + str(round(time.time() - t_session, 1)) + "s) -> " + tpath, flush=True)
        return dict(row, ok=True)
    return dict(meta, session=label, ok=False, gate="rejected on all lanes")


def rbn(sessions=5, rename_arms=1, turns=S8_TURNS, check_only=False, go=False):
    """The recognition protocol's one-command fire (operator-gated via --go)."""
    try:
        prompts, meta = load_seed("base")
    except (OSError, ValueError) as exc:
        print("[s8] SEED REFUSED: " + str(exc))
        return 1
    print("[s8] seed OK: " + meta["seed_file"] + " payload sha256:"
          + meta["base_payload_sha256"][:16] + "... advances sha256:"
          + meta["advances_sha256"][:16] + "... (" + str(meta["n_advances"])
          + " frozen advances)", flush=True)
    if check_only:
        print("[s8] --check PASS: seed loads and seal-verifies (parse-level, zero network).")
        return 0
    if not go:
        print("[s8] OPERATOR GATE: the recognition fire spends frontier tokens. Re-run "
              "with --go (defaults --sessions 5 --rename-arms 1). `rbn --check` is the $0 dry-run.")
        return 2
    chain = LANES.get("S8", [])
    if not chain:
        print("[s8] no S8 lane armed (grok needs XAI_CASH_ALLOWED=1 or the subscription "
              "route; deepseek fallback needs DEEPSEEK_API_KEY). Down honestly — nothing spent.")
        return 1
    jobs = [("base%02d" % (i + 1), "base") for i in range(sessions)] + \
           [("rename%02d" % (i + 1), "rename") for i in range(rename_arms)]
    print("[s8] firing " + str(len(jobs)) + " sessions (" + str(sessions) + " base + "
          + str(rename_arms) + " rename) on lanes: " + ", ".join(l for l, _ in chain), flush=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(3, len(jobs))) as pool:
        futs = {pool.submit(rbn_session, lab, chain, arm, turns): lab for lab, arm in jobs}
        for fut in concurrent.futures.as_completed(futs):
            results.append(fut.result())
    good = [r for r in results if r.get("ok")]
    print("[s8] " + str(len(good)) + "/" + str(len(jobs)) + " sessions captured; score rows -> "
          + S8_SCORES + " (UNSCORED-BLIND — second seat scores against the sealed rubric)")
    return 0 if good else 1


def write_artifact(name, question, source_ref, sha, posts, verdict, fmeta, receipts):
    sdir = _under(SALONS, name)
    clean = {s: t for s, t in posts.items() if not s.startswith("_")}
    artifact = "# SALON ARTIFACT — " + name + "\n"
    artifact += "question: " + question + "\n"
    artifact += "source: " + source_ref + "\n"
    artifact += "brief_sha256: " + sha + "\n"
    artifact += "posts_gated: " + str(len(clean)) + "/7 shapes (one engine per shape)\n"
    artifact += "fold: " + json.dumps(fmeta) + "\n\n"
    artifact += "## VERDICT (judge fold)\n" + verdict + "\n\n"
    artifact += "## BLIND POSTS (as gated)\n"
    for s in SHAPE_ORDER:
        if s in clean:
            lane = receipts.get(s, {}).get("lane", "?")
            artifact += "### " + s + " — engine: " + str(lane) + " — " + SHAPES[s][:60] + "\n"
            artifact += clean[s] + "\n\n"
    apath = _under(sdir, "SALON_ARTIFACT.md")
    with open(apath, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(artifact)
    with open(_under(RECEIPTS, name + ".json"), "w") as fh:
        json.dump({"name": name, "brief_sha": sha, "fold": fmeta, "receipts": receipts,
                   "artifact": apath}, fh, indent=1)
    register_row("salon_run", "shape-train-v4", source_ref[:280],
                 name + ": " + str(len(clean)) + "/7 posts, fold "
                 + str(fmeta.get("secs")) + "s", apath)
    log_room("salon", "shape train v4 " + name + ": " + str(len(clean))
             + "/7 posts folded -> " + apath)
    print("[artifact] " + apath)
    print("[done] " + str(len(clean)) + "/7 shapes survived; fold "
          + str(fmeta.get("secs")) + "s. Read it anywhere.")
    return 0


def fire(url, question, name=None, source_file=None):
    name = safe_slug(name or ("salon_" + time.strftime("%Y%m%d_%H%M%S")))
    digest, source_ref = "", url
    if url:
        try:
            digest = fetch(url)
        except Exception as exc:
            register_row("blocked", "fetch-fail", url, type(exc).__name__ + ": " + str(exc))
            print("FETCH FAILED honestly: " + type(exc).__name__ + ": " + str(exc))
            if not source_file:
                return 1
    if source_file:
        src = os.path.realpath(os.path.abspath(source_file))
        root_abs = os.path.realpath(ROOT)
        if not src.startswith(root_abs + os.sep):
            print("--source must live inside the repo")
            return 1
        with open(src, encoding="utf-8", errors="ignore") as fh:
            digest = fh.read()[:14000]
        source_ref = (url or "pasted") + " via " + os.path.basename(src)
    if len(digest) < 200:
        print("Digest too thin; refusing to waste a salon on vapor.")
        return 1

    bpath, brief, sha, name = build_brief(name, question, digest, source_ref)
    print("[brief] " + bpath + " sha256:" + sha, flush=True)

    posts, receipts = fan_out(brief, name)
    if len(posts) < 2:
        print("Fewer than 2 posts survived — no fold. Receipts saved; lanes suspect.")
        with open(_under(RECEIPTS, name + ".json"), "w") as fh:
            json.dump({"name": name, "brief_sha": sha, "receipts": receipts}, fh, indent=1)
        return 1

    print("[fold] " + str(len(posts)) + " posts -> judge ...", flush=True)
    verdict, fmeta = fold(brief, posts, name)
    if not verdict:
        print("FOLD FAILED — posts durable on disk; retry: refold --name " + name)
        return 1
    return write_artifact(name, question, source_ref, sha, posts, verdict, fmeta, receipts)


def refold(name):
    name = safe_slug(name)
    sdir = _under(SALONS, name)
    with open(_under(sdir, "BRIEF.md"), encoding="utf-8") as fh:
        brief = fh.read()
    sha = hashlib.sha256(brief.encode("utf-8")).hexdigest()[:16]
    posts = {}
    for s in SHAPE_ORDER:
        ppath = _under(sdir, "post_" + s + ".md")
        if os.path.exists(ppath):
            with open(ppath, encoding="utf-8") as fh:
                posts[s] = fh.read()
    if len(posts) < 2:
        print("refold: need >=2 post_*.md files; found " + str(len(posts)))
        return 1
    question, source_ref = name, "refold from durable posts"
    for line in brief.splitlines():
        if line.startswith("**QUESTION.** "):
            question = line[len("**QUESTION.** "):]
        if line.startswith("source: "):
            source_ref = line[len("source: "):]
    verdict, fmeta = fold(brief, posts, name)
    if not verdict:
        print("FOLD FAILED again — check lanes.")
        return 1
    return write_artifact(name, question, source_ref, sha, posts, verdict, fmeta, {})


def seal_test():
    """$0 falsifier battery for the W4 seal — NO lanes fired, tape-only.
    PASS = 2+ well-formed chained rows from fake posts + verify PASS + a simulated
    sealing exception that neither crashes the path nor writes a broken row."""
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    name = "sealtest-" + stamp
    print("[seal-test] sealing two fake posts (salon-" + name + "-<date>)...", flush=True)
    _seal("post", name, "f" * 16, shape="S1", lane="fake-lane-a", chars=231,
          survived=True, secs=1.2)
    _seal("post", name, "f" * 16, shape="S2", lane="fake-lane-b", chars=184,
          survived=True, secs=0.9)
    from mag import bash_local as bl
    sid_pfx = "salon-" + name + "-"
    rows = [r for r in bl._rows() if str(r.get("session_id", "")).startswith(sid_pfx)]
    well_formed = len(rows) >= 2 and all(
        r.get("schema_version") == 1 and r.get("step_hash") and r.get("input")
        and "timing" in r for r in rows)
    chained = bool(rows) and rows[0].get("prev_step_hash") == bl.GENESIS and all(
        rows[i].get("prev_step_hash") == rows[i - 1].get("step_hash")
        for i in range(1, len(rows)))
    print("[seal-test] sealed=" + str(len(rows)) + " well_formed=" + str(well_formed)
          + " chained=" + str(chained), flush=True)
    n_before = len(rows)
    orig = bl.append_row

    def _boom(row, tape=None):
        raise OSError("simulated seal failure")

    bl.append_row = _boom
    crashed = False
    try:
        _seal("post", name, "f" * 16, shape="S3", lane="boom-lane", chars=10, survived=True)
    except Exception as exc:  # noqa: BLE001 — the drill exists to prove this never happens
        crashed = True
        print("[seal-test] FAIL: simulated seal exception ESCAPED the hook: " + str(exc))
    finally:
        bl.append_row = orig
    n_after = len([r for r in bl._rows() if str(r.get("session_id", "")).startswith(sid_pfx)])
    print("[seal-test] fail-open drill: crashed=" + str(crashed)
          + " tape_rows " + str(n_before) + "->" + str(n_after)
          + " (no partial row)", flush=True)
    ok, msg = bl.verify()
    print("[seal-test] mag.bash_local verify: " + ("PASS " if ok else "FAIL ") + msg)
    passed = well_formed and chained and not crashed and n_after == n_before and ok
    print("[seal-test] VERDICT: " + ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


def drain():
    if not os.path.isdir(INBOX):
        print("No inbox. Door B idle.")
        return 0
    count = 0
    for fn in sorted(os.listdir(INBOX)):
        if not fn.endswith(".json"):
            continue
        try:
            fpath = _under(INBOX, fn)
            with open(fpath, encoding="utf-8") as fh:
                spec = json.load(fh)
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            print("[inbox] " + fn + " unreadable: " + str(exc))
            continue
        print("[inbox] firing " + fn)
        fire(spec.get("url", ""), spec.get("question", "Analyze this material."),
             name=spec.get("name") or fn[:-5],
             source_file=spec.get("source"))
        os.remove(fpath)
        count += 1
    print("[inbox] " + str(count) + " processed.")
    return 0


LANES = build_lanes()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    fparser = sub.add_parser("fire")
    fparser.add_argument("--url", default="")
    fparser.add_argument("-q", "--question", required=True)
    fparser.add_argument("--source", default=None)
    fparser.add_argument("--name", default=None)
    rparser = sub.add_parser("refold")
    rparser.add_argument("--name", required=True)
    sub.add_parser("drain")
    sub.add_parser("seal-test")
    sub.add_parser("lanes")
    bparser = sub.add_parser("rbn")
    bparser.add_argument("--sessions", type=int, default=5)
    bparser.add_argument("--rename-arms", type=int, default=1)
    bparser.add_argument("--turns", type=int, default=S8_TURNS)
    bparser.add_argument("--check", action="store_true",
                         help="$0 parse-level dry-run: seed load + sha verify, zero network")
    bparser.add_argument("--go", action="store_true",
                         help="operator gate: actually fire the frontier play sessions")
    args = ap.parse_args()
    if args.cmd == "fire":
        sys.exit(fire(args.url, args.question, args.name, args.source))
    if args.cmd == "refold":
        sys.exit(refold(args.name))
    if args.cmd == "seal-test":
        sys.exit(seal_test())
    if args.cmd == "rbn":
        sys.exit(rbn(args.sessions, args.rename_arms, args.turns,
                     check_only=args.check, go=args.go))
    if args.cmd == "lanes":
        for s in SHAPE_ORDER + ["S8"]:
            chain = LANES.get(s, [])
            print(s, "->", ", ".join(l for l, _ in chain) if chain else "(no lane)")
        print("FOLD ->", ", ".join(l for l, _ in FOLD_LANES))
        sys.exit(0)
    sys.exit(drain())
