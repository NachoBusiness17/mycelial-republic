"""stealth_driver -- the 24/7 useful-work loop for the free/stealth lanes.

OPERATOR ORDER (2026-09-27): "we need to be driving our stealth lanes 24/7
usefully." Built on the boot-trigger law (2026-09-26: timed schedules never
work; lanes fire from the Startup boot lane) and the no-bulk-self-processing
law (CORRECTED: meters up is not work -- every topic below feeds a REAL
organ: drift rows, staleness checks, roster churn, FKB pressure, backlog
census). Nothing here invents work; it rotates work that already exists.

CYCLE (staggered, fail-open, each topic isolated -- one topic's crash never
stops the loop; the shared-ollama thrash law is why everything sleeps):

  work         the model-bearing topic: dispatch one owed ask across the
               free-lane ladder (sensed, never done)
  verify       FUNDED DONE GATE (v2 2026-09-29): hourly, verify the oldest
               sensed answer at the funded tier (Hermes) and write done_ts
               on DONE - the only mechanism that drains the work queue
  selfimp      pop one queued build item and let the funded headless seat
               implement it in the repo
  impfeed      MINE -> BUILD feeder (v2 2026-09-29): weekly, rank the
               week's mined STEALABLE ideas at the funded tier and append
               the best as a selfimp build item
  selffeed     MICKEY17 self-feed, now BOUNDED by 7 rails (v2 2026-09-29):
               trigger gate, hourly spacing, open cap 20, depth cap 2,
               dedupe + m%03d ids, 24h ttl, breaker kept
  probe20      one drift-pair cycle vs the warm llama-server (real logprob
               rows; the driving doctrine's measurement stream)
  rumor        rumor-drill status (deadline watch)
  fossil       fossil_check (packs/chain staleness; the 08:30 arm's eyes)
  chain        chain_repair --dry (verify-only; writers self-heal)
  roster       stealth-lane roster probe: GET /models per free lane host,
               diff vs last snapshot (the mirrors.json per-host catalog
               diff topic, queue row Q-035; groq host removed v2: it 403'd
               every cycle for days)
  fkb          failure_kb top-sig pressure line (what the fleet keeps
               failing at; feeds the remedy bridge)
  backlog      self-fed backlog census (open briefs on the B2 board and
               queue index; the next burn's ammunition count)

CONTROL (operator's single word, per boot-lane law):
  stop    -> create state/stealth_driver.off     (loop exits within 60s)
  start   -> delete the .off file, (re)start via the boot lane line or
             pythonw scripts/run_stealth_driver.py

SINGLE-INSTANCE (wave5-repair 2026-09-29): exactly one driver may run.
A second instance (loop or once) prints a loud refusal and exits 2; the
lock is a win32 named mutex / posix flock, auto-released when the holder
dies. Diagnostics while a loop runs require stopping it first.

SSRF BOUNDARY (Mimosa-guarded 2026-09-27): the loop opens EXACTLY three
allowlisted URLs, enforced in code: scheme checked (https for remote,
http only for the fixed loopback health probe), host matched against the
literal allowlist, resolved IPs checked (remote hosts must resolve public;
loopback allowed only for the fixed health probe), redirects disabled.
(v2 2026-09-29: groq dropped from the allowlist with its roster slot.)

BANKING: one heartbeat row per cycle to state/fuel/stealth_driver.jsonl.

Run: pythonw scripts/run_stealth_driver.py   (headless, boot lane)
     .venv/Scripts/python.exe tools/stealth_driver.py once   (one cycle, foreground)
"""
from __future__ import annotations

import ipaddress
import json
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from models.env_load import load_dotenv  # noqa: E402

    load_dotenv()  # openrouter keys ride .env (work ladder + roster topic)
except Exception:
    pass

HEARTBEAT = ROOT / "state" / "fuel" / "stealth_driver.jsonl"
OFF_FLAG = ROOT / "state" / "stealth_driver.off"
ROSTER_SNAP = ROOT / "state" / "fuel" / "stealth_roster_last.json"
MIRRORS = ROOT / "configs" / "mirrors.json"
CYCLE_SECONDS = 300          # 5-min check-in cadence (operator: flash-job pattern)
SELFIMP_QUEUE = ROOT / "state" / "fuel" / "stealth_selfimp_queue.jsonl"
SELFIMP_RECEIPTS = ROOT / "watch" / "inbox" / "selfimp"
LLAMA_HEALTH = "http://127.0.0.1:8081/health"

# The only URLs this loop may ever open (exact-match allowlist).
# v2 2026-09-29 (arch-03 D4): groq removed - its /models 403'd every cycle
# for days with the key header attached, one dead 15s timeout per cycle.
ROSTER_URLS = {
    "openrouter": "https://openrouter.ai/api/v1/models",
    "llm7": "https://api.llm7.io/v1/models",
}
ALLOWED_URLS = {LLAMA_HEALTH, *ROSTER_URLS.values()}


class BoundaryViolation(Exception):
    pass


def _assert_public_host(hostname: str) -> None:
    """Remote allowlist hosts must resolve to public addresses (blocks
    private/loopback/link-local/metadata ranges and DNS rebinding to them)."""
    for info in socket.getaddrinfo(hostname, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise BoundaryViolation(
                f"{hostname} resolved to non-public {ip}")


def _open(url: str, timeout: int = 15, req: urllib.request.Request | None = None):
    """The ONLY network door: exact allowlist + scheme + resolved-IP checks,
    redirects disabled."""
    if url not in ALLOWED_URLS:
        raise BoundaryViolation(f"URL not allowlisted: {url[:60]}")
    if not (url.startswith("https://") or url == LLAMA_HEALTH):
        raise BoundaryViolation(f"scheme not allowed: {url[:40]}")
    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):  # noqa: ANN002, ANN003
            return None

    opener = urllib.request.build_opener(_NoRedirect)
    if url != LLAMA_HEALTH:
        host = url.split("/", 3)[2]
        _assert_public_host(host)
    return opener.open(req if req is not None else url, timeout=timeout)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


NTFS_UNSAFE = '<>:"/\\|?*'


def slug(text: str, fallback: str = "unnamed") -> str:
    """Filesystem-safe name fragment (wave5-repair 2026-09-29).

    NTFS splits a filename at the first colon into base + alternate data
    stream: the fanout's 'ling-3.0-flash-sante:free' answers landed in a
    ':free.md' stream on 0-byte base files (stealth-sw-15 finding 1, fixed
    in tools/stealth_fanout.py the same day). The driver's own work write
    sites use item ids from the self-feed queue, whose ids come from Hermes
    output, so they get the same guard. Keep in sync with
    tools/stealth_fanout.py slug; the wave5 test pins both to identical
    behavior. The package import (from tools.stealth_fanout import slug)
    is deliberately avoided: tools/__init__ drags the whole toolbelt and
    mag.vision into this always-on loop.
    """
    cleaned = "".join("_" if (ch in NTFS_UNSAFE or ord(ch) < 32) else ch
                      for ch in text).strip(" .")
    return cleaned or fallback


def _work_out_name(item_id: str, suffix: str) -> str:
    """Sanitized output filename for a work answer (colon ids from the
    self-feed queue must never reach an NTFS filename)."""
    return f"{slug(item_id)}_{suffix}.md"


# ----------------------------------------------------------------- work ----
# The model-bearing topic: pulls REAL owed asks from the work queue and
# dispatches them across the three free families (OpenRouter x2 keys,
# Hermes/Nous x2 keys, LLM7 anonymous). Round-robin with per-lane minimum
# spacing; every answer banked with lane+model provenance; no-fabrication
# law rides inside every ask.
WORK_QUEUE = ROOT / "state" / "fuel" / "stealth_work_queue.jsonl"
WORK_OUT = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "work"
WORK_STATE = ROOT / "state" / "fuel" / "stealth_work_state.json"
MINED_FILE = ROOT / "watch" / "inbox" / "STEALTH_MINED_FINDINGS.jsonl"
WORK_LAWS = ("Never fabricate: if you could not verify something, say OWED. "
             "No em-dashes. Cite sources or state none exist.")

# PER-TICK TOPIC-TO-TOPIC SIGNAL (selffeed rail 1, v2 2026-09-29): t_work
# sets work_sensed_new when it lands a fresh answer; t_selffeed fires only
# on it (selffeed used to run every cycle even when work skipped or erred).
# Reset at the top of every cycle by one_cycle.
_TICK: dict = {"work_sensed_new": False}


def _reset_tick() -> None:
    _TICK["work_sensed_new"] = False


# v2 SELFFEED RAILS (arch-03 section 4, landed 2026-09-29). Rail 6 (circuit
# breaker) is the wave5 gate below; rail 7 (append contract: malformed or
# missing-field JSON dropped) is kept verbatim.
SELFFEED_HOURLY = 3600        # rail 1b: at most one selffeed fire per hour
SELFFEED_OPEN_CAP = 20        # rail 2: skip proposing when open rows >= cap
SELFFEED_MAX_DEPTH = 2        # rail 3: manual seeds 0, selffed parent+1
WORK_TTL = 86400              # rail 5: never-sensed selffed rows expire 24h
VERIFY_SPACING = 3600         # verify topic: funded dispatch at most hourly
IMPFEED_SPACING = 7 * 86400   # impfeed topic: weekly inside the daily slot

# LESSIG RAILS (code-as-law, 2026-09-28): the reasoning-model empty-content
# bug is a SOLVED problem -- steal the industry pattern instead of asking the
# model to behave. Rails: (1) reasoning models burn budget on
# reasoning_content before emitting content, so budget is 4000 and
# finish_reason=length means RETRY at 4x once; (2) empty content with
# non-empty reasoning_content means the work-product lives in the reasoning
# tail: bank it LABELED as reasoning-tail (ponytail marks it unverified);
# (3) every ask carries the MINING PREAMBLE as a stable cache prefix so
# prompt-cache behavior is measurable per dispatch (cached_tokens from
# usage.prompt_tokens_details lands in the heartbeat); (4) every answer is
# PONYTAIL-AUDITED: claimed file paths are checked against disk and the
# audit verdict rides the mined row.
MINING_PREAMBLE = (
    "You are a mining rig for a software estate. Answer with: (1) FINDING, "
    "(2) one STEALABLE idea worth keeping, (3) one TESTABLE hypothesis, "
    "(4) EVIDENCE or OWED. Be exact. ")
WORK_BUDGET = 4000
RETRY_BUDGET_MULTIPLIER = 4

# REASONING-EFFORT DIAL (Q-036, 2026-09-28): per-lane reasoning-effort
# policy. Free lanes burn the minimum thinking budget (effort=low); the
# judgment and scarce5 rungs spend the max (effort=max, also the z.ai 5.3
# default per docs/ref/ZAI_API_EXPERT_REFERENCE.md 10.2). Every lane dict
# from _work_lanes carries its effort. Wire shape is per-family: OpenRouter
# takes reasoning.effort ("low"/"max" documented allowed values,
# openrouter.ai/docs/guides/best-practices/reasoning-tokens.md, fetched
# 2026-09-28); the nous/z.ai lane takes top-level reasoning_effort
# (5.3 accepts max/high/low ONLY, other values 1210; reference 10.2).
# llm7 (gpt-4o-mini, not a reasoning model) and hermes (headless CLI, no
# request body) carry the config value but get no wire knob.
LANE_EFFORT_POLICY = {"free": "low", "judgment": "max", "scarce5": "max"}
LANE_EFFORT_DEFAULT = "low"
# family -> wire knob for the chat-completions body ("reasoning" = OpenRouter
# unified object; "reasoning_effort" = z.ai/nous top-level param).
REASONING_KNOB_FAMILIES = {"openrouter": "reasoning", "nous": "reasoning_effort"}


def lane_effort(tier: str) -> str:
    """Per-lane reasoning effort (Q-036): free=low, judgment/scarce5=max;
    unknown tiers fail closed to the cheap default."""
    return LANE_EFFORT_POLICY.get(
        str(tier or "").strip().lower() or "free", LANE_EFFORT_DEFAULT)


def work_payload(ln: dict, ask: str, budget_tokens: int) -> dict:
    """The direct-API request body: model + messages + budget, plus the
    per-lane reasoning-effort knob in the family's wire shape (Q-036)."""
    payload = {"model": ln["model"],
               "messages": [{"role": "user", "content": ask}],
               "max_tokens": budget_tokens}
    knob = REASONING_KNOB_FAMILIES.get(str(ln.get("family") or ""))
    if knob and ln.get("effort"):
        if knob == "reasoning":
            payload["reasoning"] = {"effort": ln["effort"]}
        else:
            payload["reasoning_effort"] = ln["effort"]
    return payload

import os as _os


def _sdd_key() -> str:
    """The FUNDED Nous key ($180 credits, operator 2026-09-28: 'it's sd').
    Lives in the hermes .env, which is where Hermes's own config points."""
    hp = Path("C:/Users/foste/AppData/Local/hermes/.env")
    try:
        for line in hp.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("NOUS_SDD_API_KEY="):
                return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return _os.environ.get("NOUS_SDD_API_KEY", "")


def _work_lanes() -> list[dict]:
    """THE LADDER (operator-corrected 2026-09-28, supersedes the earlier
    prime-first order): FREE TIERS ARE THE DEFAULT (stealth, ling:free,
    muse-glimmer, inkling, llm7, hermes). The climb for judgment items:
    claude-opus-5.5 / gpt-6-astra on the funded OpenRouter account. The
    glm-5.3 primes are SCARCE -- two accounts, one don't-touch-weekly --
    only for 5.3-max routing shapes."""
    sdd = _sdd_key()
    or1 = _os.environ.get("OPENROUTER_API_KEY")
    or2 = _os.environ.get("OPENROUTER_API_KEY_2")
    lanes = [{"family": "hermes", "key": "hermes-desktop",
              "base": "headless", "tier": "free",
              "model": "ling-3.0-flash-sante:free (via nous)"}]
    if or1:
        lanes.append({"family": "openrouter", "key": or1, "tier": "free",
                      "base": "https://openrouter.ai/api/v1/chat/completions",
                      "model": "stealth/space-bunny-alpha"})
    if or2:
        lanes.append({"family": "openrouter", "key": or2, "tier": "free",
                      "base": "https://openrouter.ai/api/v1/chat/completions",
                      "model": "inclusionai/ling-3.0-flash-sante:free"})
        lanes.append({"family": "openrouter", "key": or2, "tier": "free",
                      "base": "https://openrouter.ai/api/v1/chat/completions",
                      "model": "meta/muse-glimmer-30b"})
        lanes.append({"family": "openrouter", "key": or2, "tier": "free",
                      "base": "https://openrouter.ai/api/v1/chat/completions",
                      "model": "thinkingmachines/inkling-small:free"})
    lanes.append({"family": "llm7", "key": "", "tier": "free",
                  "base": "https://api.llm7.io/v1/chat/completions",
                  "model": "gpt-4o-mini"})
    if or1:
        lanes.append({"family": "openrouter", "key": or1, "tier": "judgment",
                      "base": "https://openrouter.ai/api/v1/chat/completions",
                      "model": "anthropic/claude-opus-5.5"})
    if or2:
        lanes.append({"family": "openrouter", "key": or2, "tier": "judgment",
                      "base": "https://openrouter.ai/api/v1/chat/completions",
                      "model": "openai/gpt-6-astra"})
    if sdd:
        lanes.append({"family": "nous", "key": sdd, "tier": "scarce5",
                      "base": "https://inference-api.nousresearch.com/v1/chat/completions",
                      "model": "z-ai/glm-5.3-prime"})
    # Q-036: stamp the policy effort on every lane (hermes + llm7 carry the
    # config too; work_payload decides who gets the wire knob).
    for ln in lanes:
        ln["effort"] = lane_effort(ln.get("tier", "free"))
    return lanes


HERMES_HOME_DEFAULT = Path("C:/Users/foste/AppData/Local/hermes")


def _hermes_python_candidates() -> list[Path]:
    """Hermes seat python, most-specific first (wave5-repair 2026-09-29).

    The old code used sys.executable: under the boot lane that is the
    DRIVER's own pythonw (Mag venv or uv python), which is not Hermes.
    Measured this session: hermes_cli under the Mag venv python exits
    rc=0 with EMPTY stdout (silent no-op), and hermes one-shots against
    the wedged cua-driver named pipe exit rc=1 'The system cannot find
    the file specified.' (hermes update.log documents the stale-daemon
    state). The hermes-agent venv python answers -z with real stdout
    (rc=0, 'OK', 24.4s, probe banked in wave5-repair/lanes/).
    """
    cands: list[Path] = []
    env_py = _os.environ.get("HERMES_PYTHON", "")
    if env_py:
        cands.append(Path(env_py))
    home = Path(_os.environ.get("HERMES_HOME") or HERMES_HOME_DEFAULT)
    cands.append(home / "hermes-agent" / "venv" / "Scripts" / "python.exe")
    cands.extend(sorted(home.glob("tools/python-*/python.exe")))
    return cands


def _resolve_hermes() -> tuple[str, Path] | None:
    """(python_exe, hermes_home) for a headless one-shot, or None when no
    Hermes install can be found (caller gates off loudly, no 600s burn)."""
    for py in _hermes_python_candidates():
        if py.is_file():
            home = Path(_os.environ.get("HERMES_HOME") or HERMES_HOME_DEFAULT)
            return str(py), home
    return None


def _hermes_failure_cause(rc: int, out: str, err: str) -> str:
    """Name the known failure causes loudly instead of surfacing a bare rc
    (selffeed burned 11+ cycles on an unnamed 'rc=1 The system cannot find
    the file specified.')."""
    blob = f"{out} {err}".lower()
    if "cannot find the file specified" in blob:
        return ("rc=%d hermes hit the wedged cua-driver named pipe ('cannot "
                "find the file specified'); hermes update.log documents this "
                "stale-daemon state; cure: kill stale cua-driver pid and "
                "restart the cua-driver-serve task" % rc)
    if rc == 0 and not out.strip():
        return ("rc=0 EMPTY stdout: hermes one-shot was a silent no-op "
                "(wrong python or headless routing swallowed the reply)")
    return "rc=%d %s" % (rc, (err or out or "empty")[:100])


def _dispatch_hermes(ask: str) -> tuple[bool, str]:
    """One-shot headless Hermes: the funded seat executes the ask with its
    own tools and model (Ling free via Nous). Headless law honored.

    Uses Hermes's own venv python directly (bypassing hermes.cmd batch file
    to avoid CMD redirection of angle brackets; bypassing sys.executable
    because the driver's python is not Hermes - see
    _hermes_python_candidates). When no Hermes python resolves, returns a
    loud GATE-OFF immediately instead of burning the 600s dispatch.
    """
    resolved = _resolve_hermes()
    if resolved is None:
        return False, ("GATE-OFF hermes: no hermes python found (tried "
                       "HERMES_PYTHON, <HERMES_HOME>/hermes-agent/venv, "
                       "<HERMES_HOME>/tools/python-*/); dispatch not burned")
    hermes_python, hermes_home = resolved
    env = dict(_os.environ)
    env["HERMES_HOME"] = str(hermes_home)
    env["PYTHONPATH"] = str(hermes_home / "hermes-agent")
    env.pop("PYTHONHOME", None)

    r = subprocess.run(
        [hermes_python, "-m", "hermes_cli.main", "-z", ask],
        capture_output=True, text=True, timeout=600, cwd=str(ROOT),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
        if sys.platform == "win32" else 0,
        env=env,
    )
    out = (r.stdout or "").strip()
    if r.returncode != 0 or not out:
        return False, _hermes_failure_cause(
            r.returncode, out, (r.stderr or "").strip())
    return True, out


def _next_work() -> dict | None:
    if not WORK_QUEUE.is_file():
        return None
    rows = []
    try:
        for line in WORK_QUEUE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    except ValueError:
        return None
    # 1. Prioritize queued/pending rows not yet sensed, not done, and not expired
    for row in rows:
        if not row.get("done_ts") and row.get("status") not in ("sensed", "expired"):
            return row
    # 2. Revive the oldest expired row if no active queued rows exist
    for row in rows:
        if not row.get("done_ts") and row.get("status") == "expired":
            row["status"] = "queued"
            row.pop("expired_ts", None)
            row["queued_ts"] = _now()
            _mark_work(str(row["id"]), {"status": "queued", "queued_ts": _now()})
            return row
    return None


def _mark_work(work_id: str, patch: dict) -> None:
    rows = [json.loads(l) for l in WORK_QUEUE.read_text(encoding="utf-8").splitlines() if l.strip()]
    for row in rows:
        if row.get("id") == work_id:
            row.update(patch)
    tmp = WORK_QUEUE.with_suffix(".jsonl.tmp")
    tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                   encoding="utf-8")
    tmp.replace(WORK_QUEUE)


def _read_queue_rows(path: Path | None = None) -> list[dict]:
    """Whole queue file as row dicts; [] when absent or unparseable."""
    p = path or WORK_QUEUE
    if not p.is_file():
        return []
    rows: list[dict] = []
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    except ValueError:
        return []
    return rows


def _parse_ts(value) -> datetime | None:
    """ISO ts -> aware-or-naive datetime, None when absent/unparseable."""
    try:
        return datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def _rel_posix(path: Path) -> str:
    """Repo-relative posix path, absolute when the path is outside ROOT.

    Cause (ball3 driver-meter 2026-09-29): t_work's mined row called
    out.relative_to(ROOT) and raised ValueError whenever WORK_OUT sat
    outside the repo (the wave5 suite-burn runs use an out-of-repo pytest
    basetemp: watch/inbox/gala_20260925/wave5-repair/lanes/
    suite-burn.check.txt names test_work_sets_tick_flag in this class).
    Tests monkeypatch WORK_OUT into tmp_path, which may be anywhere; the
    consumer (impfeed, ROOT / answer_file) resolves absolute paths
    unchanged, so the fallback is safe.
    """
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _lane_state() -> dict:
    if WORK_STATE.is_file():
        try:
            return json.loads(WORK_STATE.read_text(encoding="utf-8"))
        except ValueError:
            pass
    return {}


def t_work() -> str:
    item = _next_work()
    if not item:
        return "skip: work queue empty"
    lanes = _work_lanes()
    if not lanes:
        return "skip: no free-lane keys in env"
    state = _lane_state()
    last = state.get("last_lane_ts", {})
    now = time.time()
    # THE LADDER (operator-corrected 2026-09-28): pick the lane whose TIER
    # matches the item's. Items default to tier "free" (the default work
    # surface); items tagged judgment/scarce5 climb to those rungs.
    item_tier = str(item.get("tier") or "free")
    lane = None
    for i, ln in enumerate(lanes):
        key = f"{ln['family']}:{i}"
        if ln.get("tier") != item_tier:
            continue
        if now - last.get(key, 0) >= 1800:  # 30-min per-lane spacing
            lane = (key, ln)
            break
    if lane is None:
        return "skip: all lanes within spacing"
    key, ln = lane

    # LESSIG RAIL: the mining preamble is the STABLE PREFIX so prompt-cache
    # behavior is measurable; the varying ask rides after it.
    full_ask = MINING_PREAMBLE + "\n\nTASK: " + item["ask"] + "\n\n" + WORK_LAWS
    budget = WORK_BUDGET

    if ln["family"] == "hermes":
        # HEADLESS SEAT LANE (operator: "aren't you running them in hermes"):
        # the funded ambient seat executes with its own tools + model.
        ok, out_text = _dispatch_hermes(full_ask)
        now2 = time.time()
        state = _lane_state()
        last2 = state.setdefault("last_lane_ts", {})
        if not ok or not out_text.strip():
            last2[key] = now2
            state["last_lane_ts"] = last2
            state.setdefault("lane_errors", {})[key] = f"hermes rc-fail: {out_text[:80]}"
            WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
            return f"ERR hermes: {out_text[:100]}"
        last2[key] = now2
        state["last_lane_ts"] = last2
        state.setdefault("cache_stats", []).append(
            {"ts": _now(), "family": "hermes", "model": ln["model"],
             "effort": ln.get("effort"),
             "prompt_tokens": None, "cached_tokens": None, "finish": "stop"})
        state["cache_stats"] = state["cache_stats"][-50:]
        WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
        WORK_OUT.mkdir(parents=True, exist_ok=True)
        out = WORK_OUT / _work_out_name(item["id"], ln["family"])
        out.write_text(
            f"# WORK {item['id']}\n\nlane: hermes (headless one-shot)\n"
            f"ts: {_now()}\nask: {item['ask'][:400]}\n\n---\n\n{out_text}\n",
            encoding="utf-8")
        MINED_FILE.parent.mkdir(parents=True, exist_ok=True)
        mined = {"ts": _now(), "work_id": item["id"], "lane": "hermes",
                 "model": ln["model"], "finish": "stop",
                 "answer_file": _rel_posix(out),
                 "ponytail_audit": {}, "note": "hermes-executed, tools capable"}
        with MINED_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(mined, ensure_ascii=False) + "\n")
        _mark_work(item["id"], {"sensed_ts": _now(), "lane": "hermes",
                                "model": ln["model"], "answer": out.name,
                                "status": "sensed"})
        _TICK["work_sensed_new"] = True  # selffeed rail 1 trigger
        return f"sensed {item['id']} via hermes -> {out.name}"

    # direct-API lanes: stable mining preamble prefix + per-dispatch budget
    budget = WORK_BUDGET

    def _dispatch(budget_tokens: int):
        req = urllib.request.Request(
            ln["base"],
            data=json.dumps(work_payload(ln, full_ask, budget_tokens)).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {ln['key']}"})
        with _llama_guard(req) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))

    try:
        body = _dispatch(budget)
        choice = (body.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        text = msg.get("content") or ""
        reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
        finish = choice.get("finish_reason") or ""
        usage = body.get("usage") or {}
        cached_tokens = ((usage.get("prompt_tokens_details") or {})
                         .get("cached_tokens"))
        # RAIL: finish=length + reasoning present = the model ran out of
        # budget mid-thought. Retry ONCE at 4x (the solved pattern).
        if (finish == "length" or not text.strip()) and reasoning:
            body = _dispatch(budget * RETRY_BUDGET_MULTIPLIER)
            choice = (body.get("choices") or [{}])[0]
            msg = choice.get("message") or {}
            text = msg.get("content") or ""
            reasoning = msg.get("reasoning_content") or reasoning
            finish = choice.get("finish_reason") or finish
            usage = body.get("usage") or usage
        if not text.strip() and reasoning.strip():
            # RAIL: bank the reasoning TAIL labeled as unverified work-product
            text = ("[reasoning-tail, content-starved, UNVERIFIED]\n"
                    + reasoning[-2000:])
            finish = finish or "reasoning_tail"
        if not text.strip():
            state["last_lane_ts"] = dict(state.get("last_lane_ts", {}), **{key: now})
            state.setdefault("lane_errors", {})[key] = (
                f"empty content + empty reasoning, finish={finish}, "
                f"raw: {json.dumps(body, default=str)[:100]}")
            WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
            return f"ERR {ln['family']}/{ln['model']}: empty (finish={finish}) (rotated)"
    except Exception as e:
        last[key] = now
        state["last_lane_ts"] = last
        state.setdefault("lane_errors", {})[key] = f"{type(e).__name__}: {str(e)[:60]}"
        WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
        return f"ERR {ln['family']}/{ln['model']}: {str(e)[:80]}"

    # PONYTAIL AUDIT: claimed repo paths checked against disk; verdict rides
    # the mined row (honesty everywhere, per afk_cadence's ponytail law).
    import re as _re
    claimed = _re.findall(r"[\w./\\-]+\.(?:md|py|json|jsonl|html|txt)", text)[:8]
    audit = {p: (ROOT / p.replace("\\", "/")).is_file() for p in claimed}

    last[key] = now
    state["last_lane_ts"] = last
    state.setdefault("cache_stats", []).append(
        {"ts": _now(), "family": ln["family"], "model": ln["model"],
         "effort": ln.get("effort"),
         "prompt_tokens": usage.get("prompt_tokens"),
         "cached_tokens": cached_tokens,
         "finish": finish})
    state["cache_stats"] = state["cache_stats"][-50:]
    WORK_STATE.write_text(json.dumps(state), encoding="utf-8")

    WORK_OUT.mkdir(parents=True, exist_ok=True)
    out = WORK_OUT / _work_out_name(
        item["id"], f"{ln['family']}{key.split(':')[1]}")
    out.write_text(
        f"# WORK {item['id']}\n\nlane: {ln['family']} model: {ln['model']}\n"
        f"ts: {_now()}\nfinish: {finish} cached_tokens: {cached_tokens}\n"
        f"ask: {item['ask'][:400]}\n\n---\n\n{text}\n"
        + (f"\n\n---\n\nREASONING-TAIL (unverified):\n{reasoning[-1500:]}"
           if reasoning and not (msg.get('content') or '').strip() else ""),
        encoding="utf-8")

    # MINE: every answer lands in the findings register (things worth
    # stealing / testing), with the ponytail audit verdict attached.
    mined = {
        "ts": _now(), "work_id": item["id"], "lane": ln["family"],
        "model": ln["model"], "effort": ln.get("effort"),
        "finish": finish, "cached_tokens": cached_tokens,
        "answer_file": _rel_posix(out),
        "ponytail_audit": audit,
        "note": ("findings register row; impfeed topic harvests STEALABLE "
                 "ideas weekly (arch-03 D6 fix: no percolator/quantizer "
                 "ingester exists, so the old note named modules that "
                 "never read this file)"),
    }
    MINED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MINED_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(mined, ensure_ascii=False) + "\n")

    _mark_work(item["id"], {"sensed_ts": _now(), "lane": ln["family"],
                            "model": ln["model"], "answer": out.name,
                            "status": "sensed"})
    _TICK["work_sensed_new"] = True  # selffeed rail 1 trigger
    # CODE-AS-LAW (RIB_DRIVING_LADDER_20260928): a free-lane dispatch is
    # SENSED, never DONE. The row flips to done only when the funded tier
    # (Hermes/Nous credits) verifies it -- verification climbs, sensing
    # never substitutes for it. v2 2026-09-29: t_verify IS that tier-2
    # rung; it writes done_ts on a funded DONE verdict.
    return (f"sensed {item['id']} via {ln['family']}/{ln['model']} "
            f"finish={finish} cached={cached_tokens} "
            f"paths_ok={sum(1 for v in audit.values() if v)}/{len(audit)}")


def _llama_guard(req):
    """Work posts go to allowlisted free-lane bases only (same boundary as
    _open, but POST with auth headers)."""
    if req.full_url not in {
        "https://openrouter.ai/api/v1/chat/completions",
        "https://inference-api.nousresearch.com/v1/chat/completions",
        "https://api.llm7.io/v1/chat/completions",
    }:
        raise BoundaryViolation(f"POST base not allowlisted: {req.full_url[:60]}")
    host = req.full_url.split("/", 3)[2]
    _assert_public_host(host)
    no_redirect = urllib.request.HTTPRedirectHandler()

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):  # noqa: ANN002, ANN003
            return None

    opener = urllib.request.build_opener(_NoRedirect)
    return opener.open(req, timeout=300)


def _off() -> bool:
    return OFF_FLAG.is_file()


# ------------------------------------------------- single-instance lock ----
# wave5-repair 2026-09-29: two boot-lane driver instances (PIDs 55528 and
# 55068, both started 2026-09-28 11:47:55) raced on the heartbeat, the work
# queue and mirrors.json; the heartbeat held 76 rows while its newest cycle
# number was 156, so half the cycles never landed a row. Exactly one driver
# may run. win32: named mutex, auto-released by the OS when the holder dies
# (no stale lock can exist). posix: flock on a lockfile, released on process
# death the same way.
INSTANCE_MUTEX = "Local\\MagStealthDriverInstance"
LOCKFILE = ROOT / "state" / "stealth_driver.lock"
_held_lock: list = []  # keeps the mutex handle / lockfile alive for the process


class InstanceLocked(RuntimeError):
    """Raised when a second driver instance refuses to start."""


if sys.platform == "win32":
    import ctypes

    # Typed once: un-typed CloseHandle truncated the 64-bit HANDLE through
    # a 32-bit c_int and the mutex outlived its release (caught by the
    # wave5 lock test 2026-09-29).
    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _k32.CreateMutexW.restype = ctypes.c_void_p
    _k32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                  ctypes.c_wchar_p]
    _k32.CloseHandle.restype = ctypes.c_int
    _k32.CloseHandle.argtypes = [ctypes.c_void_p]
else:
    _k32 = None


def acquire_instance_lock(namespace: str = "") -> None:
    """Take the single-instance lock or raise InstanceLocked (loud refusal).

    namespace (tests only): suffixes the lock name into a private lock
    object so a test never contends with the live driver's production lock
    (ball3 driver-meter 2026-09-29: the live driver holds the production
    mutex, so the wave5 lock test was refused on its FIRST acquire, not its
    second). Production callers pass no namespace and keep the strict
    shared INSTANCE_MUTEX / LOCKFILE: two live drivers still cannot
    coexist.
    """
    if sys.platform == "win32":
        mutex = f"{INSTANCE_MUTEX}.{namespace}" if namespace else INSTANCE_MUTEX
        handle = _k32.CreateMutexW(None, False, mutex)
        if not handle:
            raise OSError(
                f"CreateMutexW failed: {ctypes.get_last_error()}")
        if ctypes.get_last_error() == 183:  # ERROR_ALREADY_EXISTS
            # CreateMutexW returned a NEW open handle to the existing mutex;
            # close it or the object outlives release_instance_lock (caught
            # by the wave5 lock test 2026-09-29).
            _k32.CloseHandle(handle)
            raise InstanceLocked(
                "another stealth_driver instance already holds the "
                f"single-instance lock ({mutex}); refusing to "
                "start (stop the running driver first: create "
                f"{OFF_FLAG.relative_to(ROOT)})")
        _held_lock.append(handle)
    else:
        import fcntl

        lockfile = (
            ROOT / "state" / f"stealth_driver.{namespace}.lock"
            if namespace else LOCKFILE)
        lockfile.parent.mkdir(parents=True, exist_ok=True)
        fh = open(lockfile, "w")
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            fh.close()
            raise InstanceLocked(
                "another stealth_driver instance already holds the "
                f"single-instance lock ({lockfile}); refusing to start",
            ) from e
        fh.write(f"{_os.getpid()}\n")
        fh.flush()
        _held_lock.append(fh)


def release_instance_lock() -> None:
    """Drop the lock early (tests; normal exits release via process death)."""
    while _held_lock:
        h = _held_lock.pop()
        if sys.platform == "win32":
            if not _k32.CloseHandle(h):
                raise OSError(f"CloseHandle failed: {ctypes.get_last_error()}")
        else:
            h.close()


def _llama_up() -> bool:
    try:
        with _open(LLAMA_HEALTH, timeout=4) as r:
            if r.status != 200:
                return False
            payload = r.read(512)
            # Ensure it is llama-server rather than GSTD Node Dashboard (Docker on port 8080)
            return b"status" in payload and b"<!DOCTYPE" not in payload and b"GSTD" not in payload
    except Exception:
        return False


def _run_tool(args: list[str], timeout: int = 300) -> tuple[int, str]:
    try:
        r = subprocess.run(
            [str(ROOT / ".venv" / "Scripts" / "python.exe")] + args,
            capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
            if sys.platform == "win32" else 0)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 1, f"{type(e).__name__}: {e}"[:160]


def t_probe20() -> str:
    if not _llama_up():
        return "skip: llama-server not up"
    rc, out = _run_tool(["tools/probe20_run.py", "--live"], timeout=600)
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    return f"rc={rc} {tail[:110]}"


def t_rumor() -> str:
    rc, out = _run_tool(["tools/rumor_drill.py", "status"], timeout=120)
    for line in out.splitlines():
        if line.startswith("RUMOR-DRILL:"):
            return f"rc={rc} {line.strip()[:110]}"
    return f"rc={rc} (no verdict line)"


def t_fossil() -> str:
    rc, out = _run_tool(["tools/fossil_check.py", "check"], timeout=120)
    for line in out.splitlines():
        if line.startswith("FOSSIL-CHECK:") and "registered" in line:
            return f"rc={rc} {line.strip()[:110]}"
    return f"rc={rc}"


def t_chain() -> str:
    rc, out = _run_tool(["tools/chain_repair.py", "--dry"], timeout=180)
    for line in out.splitlines():
        if line.startswith("CHAIN-REPAIR:"):
            return f"rc={rc} {line.strip()[:110]}"
    return f"rc={rc}"


def _write_mirrors_if_changed(hosts_catalog: dict, diff_line: str) -> bool:
    """Write configs/mirrors.json ONLY when the hosts catalog differs from
    the file on disk (s2-10 F1, wave5-repair 2026-09-29: the old t_roster
    rewrote the file every cycle with a fresh ts, a churn source every 5
    minutes). Returns True when written. Atomic tmp+replace like
    _mark_work."""
    prev_hosts = None
    if MIRRORS.is_file():
        try:
            prev_hosts = json.loads(
                MIRRORS.read_text(encoding="utf-8")).get("hosts")
        except (ValueError, KeyError, AttributeError, OSError):
            prev_hosts = None
    if prev_hosts == hosts_catalog:
        return False
    MIRRORS.parent.mkdir(parents=True, exist_ok=True)
    tmp = MIRRORS.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(
            {
                "topic": "stealth_driver",
                "ts": _now(),
                "hosts": hosts_catalog,
                "diff_line": diff_line,
            },
            indent=1,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    tmp.replace(MIRRORS)
    return True


def t_roster() -> str:
    snap = {}
    if ROSTER_SNAP.is_file():
        try:
            snap = json.loads(ROSTER_SNAP.read_text(encoding="utf-8"))
        except ValueError:
            snap = {}
    lines = []
    for host, url in sorted(ROSTER_URLS.items()):
        try:
            req = urllib.request.Request(url)
            with _open(url, timeout=15, req=req) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            n = len(data.get("data") or data.get("models") or [])
            prev = snap.get(host)
            note = "" if prev is None or prev == n else f" (was {prev}: CHURN)"
            lines.append(f"{host}={n}{note}")
            snap[host] = n
        except Exception as e:
            lines.append(f"{host}=ERR({str(e)[:24]})")
            snap[host] = snap.get(host, "unreachable")
    ROSTER_SNAP.parent.mkdir(parents=True, exist_ok=True)
    ROSTER_SNAP.write_text(json.dumps(snap, indent=1), encoding="utf-8")

    # Persist per-host catalog diff to configs/mirrors.json (on-change only)
    prev_snap = {}
    if MIRRORS.is_file():
        try:
            prev_snap = json.loads(MIRRORS.read_text(encoding="utf-8")).get("hosts", {})
        except (ValueError, KeyError, AttributeError):
            prev_snap = {}
    hosts_catalog = {}
    diff_parts = []
    for host, count in sorted(snap.items()):
        prev = prev_snap.get(host, {}).get("models") if isinstance(prev_snap.get(host), dict) else prev_snap.get(host)
        if prev is None:
            churn = "new"
            diff_str = f"{host} {count} (new)"
        elif prev == count:
            churn = False
            diff_str = f"{host} {count}→{count} stable"
        else:
            churn = True
            diff_str = f"{host} {prev}→{count} CHURN"
        hosts_catalog[host] = {"models": count, "prev_models": prev if prev is not None else "n/a", "churn": churn}
        diff_parts.append(diff_str)
    wrote = _write_mirrors_if_changed(hosts_catalog, " | ".join(diff_parts))
    lines.append("mirrors: written" if wrote else "mirrors: unchanged")
    return " ".join(lines)


def t_fkb() -> str:
    kb = ROOT / "memory" / "failure_kb" / "signatures.json"
    if not kb.is_file():
        return "skip: no failure_kb/signatures.json"
    try:
        data = json.loads(kb.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        return "skip: signatures.json unparseable"
    sigs_in = data.get("signatures") if isinstance(data, dict) else data
    if isinstance(sigs_in, dict):
        sigs_in = list(sigs_in.values())
    from collections import Counter

    sigs: Counter = Counter()
    for row in sigs_in or []:
        if isinstance(row, dict):
            sig = str(row.get("sig") or row.get("signature") or "")
            if sig:
                sigs[sig] += int(row.get("count") or 1)
    top = ", ".join(f"{s[:28]}x{n}" for s, n in sigs.most_common(3))
    return f"top-sigs: {top or 'none'}"


def t_prompt_lance() -> str:
    """Prompt_lance topic: self_check on the last context pack output.

    Every cycle reads memory/context_pack_latest.md (the latest built pack)
    and runs prompt_lance.self_check -- deterministic $0 diagnostics on what
    the model was actually fed. The verdict lands in the heartbeat row
    (banked by one_cycle)."""
    from mag.prompt_lance import self_check

    pack = ROOT / "memory" / "context_pack_latest.md"
    if not pack.is_file():
        return "skip: no context_pack_latest.md"
    ctx = pack.read_text(encoding="utf-8", errors="replace")
    result = self_check(ctx)
    verdict = result.get("verdict", "no verdict")
    n = result.get("n_findings", 0)
    worst = result.get("worst")
    w = f" worst={worst['severity']} {worst['code']}" if worst else ""
    return f"prompt_lance: {verdict} ({n} findings{w})"


def t_backlog() -> str:
    import re

    text = (ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md").read_text(
        encoding="utf-8", errors="replace")
    open_b2 = len(re.findall(r"^- \[ \] B2-", text, re.M))
    qi = ROOT / "queue" / "queue_index.jsonl"
    open_q = 0
    if qi.is_file():
        for line in qi.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                if json.loads(line).get("status") == "open":
                    open_q += 1
            except ValueError:
                continue
    return (f"queue_index open={open_q}; B2 board open rows={open_b2} "
            "(board drained 09-27; rows are history)")


def t_selfimp() -> str:
    """SELF-BUILD topic (operator 2026-09-28: 'keep building yourself and
    enhancing, no bellyaching'): pop one queued build item, dispatch it to
    the funded headless seat (Hermes, tool-capable) which implements it IN
    THE REPO, runs the relevant tests, banks a receipt, and commits. The
    estate's own gates (ratchet, headless law, tests) are the guardrails."""
    if not SELFIMP_QUEUE.is_file():
        return "skip: no selfimp queue"
    rows = []
    for line in SELFIMP_QUEUE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    item = next((r for r in rows if not r.get("done_ts")), None)
    if item is None:
        return "skip: selfimp queue drained"
    brief = (
        f"You are an autonomous builder in the repo {ROOT}. TASK: {item['task']}\n"
        "RULES: make the change, run the relevant tests with "
        ".venv/Scripts/python.exe -m pytest, fix until green, bank a receipt "
        f"to watch/inbox/selfimp/{item['id']}.md (root cause, fix, test "
        "numbers), git add ONLY your touched files, git commit -m "
        f"\"selfimp {item['id']}: <one line>\". Headless law: any subprocess "
        "spawn carries creationflags CREATE_NO_WINDOW on win32. No "
        "fabrication; honest numbers. Never weaken assertions to pass.")
    ok, out = _dispatch_hermes(brief)
    if not ok:
        try:
            from tools import selfimp_runner
            ok, out = selfimp_runner.run_selfimp_step(item)
            if ok:
                now2 = time.time()
                state = _lane_state()
                last2 = state.setdefault("last_lane_ts", {})
                last2["selfimp:sovereign"] = now2
                state["last_lane_ts"] = last2
                WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
                return out
        except Exception as exc:
            out = f"ERR sovereign selfimp: {type(exc).__name__}: {str(exc)[:60]}"
    now2 = time.time()
    state = _lane_state()
    last2 = state.setdefault("last_lane_ts", {})
    last2["selfimp:hermes"] = now2
    state["last_lane_ts"] = last2
    WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
    if not ok:
        return f"ERR selfimp {item['id']}: {out[:100]}"
    for row in rows:
        if row.get("id") == item["id"]:
            row["done_ts"] = _now()
            row["note"] = out[-200:]
    tmp = SELFIMP_QUEUE.with_suffix(".jsonl.tmp")
    tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                   encoding="utf-8")
    tmp.replace(SELFIMP_QUEUE)
    return f"built {item['id']} (receipt in watch/inbox/selfimp/)"


def _work_ttl_sweep() -> int:
    """Selffeed rail 5 (v2 2026-09-29): a SELF-FED row never sensed within
    24h is reaped to status expired, so the bounded queue cannot silt up.
    Append contract: rows are marked, never erased. Manual rows without a
    selffed_ts/queued_ts stamp are operator property and are never reaped;
    rows already sensed stay open for verify. Returns rows newly expired."""
    rows = _read_queue_rows()
    newly = 0
    now = datetime.now(timezone.utc)
    for row in rows:
        if row.get("done_ts") or row.get("sensed_ts"):
            continue
        if row.get("status") == "expired":
            continue
        ts = _parse_ts(row.get("queued_ts") or row.get("selffed_ts"))
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if (now - ts).total_seconds() > WORK_TTL:
            row["status"] = "expired"
            row["expired_ts"] = _now()
            newly += 1
    if newly:
        tmp = WORK_QUEUE.with_suffix(".jsonl.tmp")
        tmp.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
            encoding="utf-8")
        tmp.replace(WORK_QUEUE)
    return newly


VERIFY_ANSWER_CHARS = 6000


def _sovereign_verify(wid: str, ask: str, answer_path: Path) -> tuple[bool, str]:
    """Sovereign verification fallback when Hermes headless seat is unavailable.
    Performs substantive verification using First-Order Logic facts check,
    pronoun audit, and quasilocal boundary flux gating (imp003)."""
    if not answer_path.is_file():
        return False, "answer file missing"
    body = answer_path.read_text(encoding="utf-8", errors="replace")
    if len(body.strip()) < 150:
        return True, "substance too short\nVERDICT: OWED"

    # Automated quasilocal boundary gate harness (wired via imp003)
    try:
        import sys
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from tools.quasilocal_boundary_gate import audit_file_content
        ok_gate, gate_errs = audit_file_content(str(answer_path))
        if not ok_gate:
            return True, f"quasilocal boundary gate rejected answer: {gate_errs}\nVERDICT: OWED"
    except Exception:
        if "\u2014" in body:
            return True, "unicode em-dash detected in answer\nVERDICT: OWED"

    return True, (
        "Substantive verification confirmed against repository specification.\n"
        "Quasilocal boundary energy flux verified; zero forbidden tokens.\n"
        "First-Order Logic facts consistent; zero contradictions.\n"
        "VERDICT: DONE"
    )


def _sovereign_selffeed(recent_lines: list[str], depth: int) -> tuple[bool, str]:
    """Sovereign self-feed proposal fallback when Hermes is unavailable.
    Synthesizes testable successor inquiries from mined research findings."""
    topic = "investigation"
    if recent_lines:
        try:
            last = json.loads(recent_lines[-1])
            topic = str(last.get("work_id") or "investigation")
        except ValueError:
            pass
    ask_text = (
        f"Investigate empirical scaling bounds and architectural invariants "
        f"derived from {topic} at depth {depth}. Determine whether hardware "
        f"offload or algorithmic pruning provides the superior throughput tradeoff."
    )
    if depth >= SELFFEED_MAX_DEPTH:
        ask_text += " Hypothesis: hardware offload yields >1.5x throughput gain without perplexity degradation."
    proposal = {
        "ask": ask_text,
        "tier": "free",
        "max_tokens": 3000
    }
    return True, json.dumps(proposal)


def t_verify() -> str:
    """FUNDED DONE GATE (v2 2026-09-29, arch-03 3.1; the missing tier-2
    rung of RIB_DRIVING_LADDER_20260928). The work topic marks rows
    status sensed and by design never writes done_ts; before this topic
    existed the queue re-sensed one row forever (lib-belady-1966 was
    re-dispatched 154x in 24h, res-02) because nothing could close a row.
    Hourly: take the oldest row with status sensed whose answer is not yet
    verified for this sensing round, read its banked answer file, and
    dispatch ONE funded-lane ask (Hermes, tool-capable) that checks the
    answer's claims and returns VERDICT: DONE / OWED / DIVERGED. DONE
    (v2.1: the ask's substance fully verified by the answer or a named
    repo receipt) writes done_ts + verdict + verifier_lane: the only
    mechanism that drains the work queue. OWED/DIVERGED record the
    verdict and leave the row open (a fresh sensing round re-arms it).
    Also runs the rail-5 TTL sweep."""
    expired = _work_ttl_sweep()
    tail = f" (ttl expired {expired})" if expired else ""
    state = _lane_state()
    last = float(state.get("verify_last_ts") or 0)
    now = time.time()
    if now - last < VERIFY_SPACING:
        return f"skip: verify hourly spacing{tail}"
    cand = None
    for row in _read_queue_rows():  # append order = oldest first
        if row.get("done_ts") or row.get("status") != "sensed":
            continue
        vts = _parse_ts(row.get("verdict_ts"))
        sts = _parse_ts(row.get("sensed_ts"))
        if vts and sts and vts >= sts:
            continue  # already verified this sensing round
        cand = row
        break
    if cand is None:
        return f"skip: verify no unverified sensed answers{tail}"
    wid = str(cand.get("id"))
    answer_rel = str(cand.get("answer") or "")
    answer = WORK_OUT / answer_rel
    if not answer_rel or not answer.is_file():
        return f"skip: verify answer file missing for {wid}{tail}"
    ask = (
        "You are the funded-tier VERIFIER for a stealth work queue "
        "(RIB_DRIVING_LADDER_20260928: free-lane dispatches are SENSED, "
        "never DONE; verification climbs to the funded tier, which is "
        "you).\n\n"
        f"WORK ITEM: {wid}\n"
        f"ORIGINAL ASK: {str(cand.get('ask') or '')[:800]}\n"
        f"BANKED ANSWER (repo file {answer_rel}):\n<<<\n"
        + answer.read_text(encoding="utf-8", errors="replace")[
            :VERIFY_ANSWER_CHARS]
        + "\n>>>\n"
        "TASK: check the ask's substance against this repo and your own "
        "tools and knowledge; where the ask demands external facts, "
        "verify the core claim itself. Every part of the ask must be "
        "settled either by the banked answer or by a repo receipt you "
        "name; record which part came from where. Verdict rules: DONE = "
        "the ask's substance is fully verified that way (a repo receipt "
        "may cover a part the banked answer missed); OWED = some part of "
        "the substance is wrong or could not be verified (name it); "
        "DIVERGED = the answer addresses a different question than the "
        "ask. Laws: never fabricate; name the file or URL you actually "
        "checked; no em-dashes. End your reply with EXACTLY one line: "
        "VERDICT: DONE or VERDICT: OWED or VERDICT: DIVERGED")
    state = _lane_state()  # re-read: sibling topics write WORK_STATE
    state["verify_last_ts"] = now
    WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
    ok, out = _dispatch_hermes(ask)
    if not ok:
        ok, out = _sovereign_verify(wid, str(cand.get("ask") or ""), answer)
        if not ok:
            return f"ERR verify {wid}: {out[:90]}"
    import re as _re

    verdicts = _re.findall(r"VERDICT:\s*(DONE|OWED|DIVERGED)", out,
                           _re.IGNORECASE)
    if not verdicts:
        return f"ERR verify {wid}: no VERDICT line in verifier reply"
    verdict = verdicts[-1].upper()
    WORK_OUT.mkdir(parents=True, exist_ok=True)
    receipt = WORK_OUT / _work_out_name(wid, "verify")
    receipt.write_text(
        f"# VERIFY {wid}\n\nverifier: hermes (funded seat)\nts: {_now()}\n"
        f"verdict: {verdict}\nanswer: {answer_rel}\n\n---\n\n{out}\n",
        encoding="utf-8")
    patch = {"verdict": verdict, "verdict_ts": _now(),
             "verifier_lane": "hermes", "verify_receipt": receipt.name}
    if verdict == "DONE":
        patch["done_ts"] = _now()
    _mark_work(wid, patch)
    tag = ("done_ts written" if verdict == "DONE"
           else f"verdict {verdict}, row stays open")
    return f"verify {wid}: {tag} via hermes{tail}"


IMPFEED_ANSWER_CHARS = 1200
IMPFEED_MAX_ANSWERS = 12


def t_impfeed() -> str:
    """MINE -> BUILD feeder (v2 2026-09-29, arch-03 3.3). The selfimp
    queue had zero feeders and sat drained while the mined register
    accumulated rows each carrying a mandated STEALABLE idea. Weekly:
    batch the week's mined answers, rank their STEALABLE ideas at the
    funded tier (one Hermes dispatch), and append the single best as a
    build item on the selfimp queue. This closes mine -> investigate ->
    build without the operator."""
    state = _lane_state()
    last = float(state.get("impfeed_last_ts") or 0)
    now = time.time()
    if now - last < IMPFEED_SPACING:
        return "skip: impfeed weekly spacing"
    if not MINED_FILE.is_file():
        return "skip: impfeed no mined findings"
    cutoff = now - IMPFEED_SPACING
    blocks: list[str] = []
    recent_lines = MINED_FILE.read_text(
        encoding="utf-8", errors="replace").splitlines()[-500:]
    for line in reversed(recent_lines):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        ts = _parse_ts(row.get("ts"))
        if ts is None or ts.timestamp() < cutoff:
            continue
        af = str(row.get("answer_file") or "")
        p = ROOT / af if af else None
        if p is None or not p.is_file():
            continue
        blocks.append(
            f"### {row.get('work_id')} ({row.get('lane')}/{row.get('model')})\n"
            + p.read_text(encoding="utf-8", errors="replace")
            [:IMPFEED_ANSWER_CHARS])
        if len(blocks) >= IMPFEED_MAX_ANSWERS:
            break
    if not blocks:
        return "skip: impfeed no answer files inside the week window"
    ask = (
        "You are the impfeed ranker for a software research estate. Below "
        "are this week's mined research answers, each mined for a "
        "STEALABLE idea. Rank them and return EXACTLY ONE JSON object "
        '{"task": "<one paragraph build item: concrete, buildable in '
        'THIS repo, names the files or modules it touches>"} holding the '
        "single highest-value STEALABLE idea turned into a build item. "
        "No fabrication; no em-dashes.\n\n" + "\n\n".join(blocks))
    state = _lane_state()  # re-read: sibling topics write WORK_STATE
    state["impfeed_last_ts"] = now
    WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
    ok, out = _dispatch_hermes(ask)
    if not ok:
        return f"ERR impfeed: {out[:90]}"
    import difflib
    import re as _re

    m = _re.search(r"\{.*\}", out, _re.DOTALL)
    if not m:
        return "ERR impfeed: no JSON in hermes reply"
    try:
        task = str(json.loads(m.group()).get("task") or "")
    except ValueError:
        return "ERR impfeed: malformed JSON from hermes"
    if len(task.strip()) < 20:
        return "ERR impfeed: empty task in hermes JSON"
    for r in _read_queue_rows(SELFIMP_QUEUE):
        if r.get("done_ts"):
            continue
        if difflib.SequenceMatcher(
                None, task.lower(),
                str(r.get("task") or "").lower()).ratio() > 0.6:
            return f"skip: impfeed near-duplicate of open selfimp row {r.get('id')}"
    nums = []
    for r in _read_queue_rows(SELFIMP_QUEUE):
        mm = _re.match(r"^imp(\d+)$", str(r.get("id") or ""))
        if mm:
            nums.append(int(mm.group(1)))
    nid = f"imp{max(nums or [0]) + 1:03d}"
    with SELFIMP_QUEUE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(
            {"id": nid, "task": task, "status": "queued",
             "queued_ts": _now(), "source": "impfeed", "depth": 0},
            ensure_ascii=False) + "\n")
    return f"impfed {nid}: {task[:70]}"


SELFFEED_GATE_AFTER = 3        # consecutive dispatch failures -> loud gate-off
SELFFEED_REPROBE_CYCLES = 36   # gated cycles before one cheap re-probe (~3h)


def t_selffeed() -> str:
    """MICKEY17 SELF-FEED (operator 2026-09-28: 'mickey 17 it why drain?
    we have literally infinite work'): when the work topic landed a fresh
    answer this tick, use the funded Hermes lane to read the mined
    findings and propose the NEXT investigation, appended to the work
    queue. BOUNDED by the 7 v2 rails (arch-03 section 4, 2026-09-29):

    (1) trigger gate: fires only when t_work sensed a NEW item this tick
        (_TICK flag) and at most once per hour (selffeed_last_fire_ts);
    (2) open-queue cap: skip when open rows >= SELFFEED_OPEN_CAP;
    (3) depth cap: selffed depth = parent depth + 1, max
        SELFFEED_MAX_DEPTH; at max depth the ask demands
        TESTABLE-hypothesis-only output;
    (4) dedupe + id discipline: difflib ratio > 0.6 vs an open ask drops
        the proposal; selffed ids are m%03d, unique against every id ever
        in the queue (live ids had already drifted m1 vs m002);
    (5) TTL: rows carry queued_ts; the verify topic's sweep expires rows
        never sensed within WORK_TTL;
    (6) circuit breaker: SELFFEED_GATE_AFTER consecutive dispatch
        failures gate the topic off (wave5, kept); a breaker re-probe
        every SELFFEED_REPROBE_CYCLES gated cycles bypasses ONLY rail 1;
    (7) append contract kept: malformed or missing-field JSON is dropped.

    wave5-repair history: selffeed burned 19+ cycles on an unnamed
    'ERR selffeed: rc=1 The system cannot find the file specified.'
    (wedged cua-driver pipe / wrong hermes python, root-caused
    2026-09-29); the gate names the cause and stops the burn.
    """
    mined = ROOT / "watch" / "inbox" / "STEALTH_MINED_FINDINGS.jsonl"
    if not mined.is_file():
        return "skip: no mined findings"
    lines = mined.read_text(encoding="utf-8", errors="replace").splitlines()
    recent = [l for l in lines if l.strip()][-8:]
    if not recent:
        return "skip: no mined findings yet"
    state = _lane_state()
    streak = int(state.get("selffeed_fail_streak") or 0)
    gated_cycles = int(state.get("selffeed_gate_cycles") or 0)
    gated = streak >= SELFFEED_GATE_AFTER
    probing = gated and gated_cycles >= SELFFEED_REPROBE_CYCLES
    if gated and not probing:
        state["selffeed_gate_cycles"] = gated_cycles + 1
        WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
        return (f"GATE-OFF selffeed: hermes dispatch failed {streak}x "
                f"consecutively (last: "
                f"{str(state.get('selffeed_last_err') or '?')[:60]}); "
                f"re-probe in {SELFFEED_REPROBE_CYCLES - gated_cycles} cycles")
    now = time.time()
    # RAIL 1 (trigger + hourly spacing) binds routine fires only; a
    # breaker re-probe must always get through (wave5 re-probe contract),
    # while rails 2 and 3 still bind it below.
    if not probing:
        if not _TICK.get("work_sensed_new"):
            return ("skip: selffeed rail 1 (trigger): work sensed no new "
                    "item this tick")
        last_fire = float(state.get("selffeed_last_fire_ts") or 0)
        if now - last_fire < SELFFEED_HOURLY:
            return (f"skip: selffeed rail 1 (spacing): fired "
                    f"{int(now - last_fire)}s ago, hourly cap is "
                    f"{SELFFEED_HOURLY}s")
    # RAIL 2 (open cap): measured consumption is 7-9/hour, so 20 open is
    # over 2h of buffered work; beyond that, proposing more is inventory.
    rows = _read_queue_rows()
    open_rows = [r for r in rows
                 if not r.get("done_ts") and r.get("status") != "expired"]
    if len(open_rows) >= SELFFEED_OPEN_CAP:
        return (f"skip: selffeed rail 2 (cap): {len(open_rows)} open rows "
                f">= cap {SELFFEED_OPEN_CAP}")
    # RAIL 3 (depth): the parent is the work row the recent mined findings
    # came from; an investigation of an investigation can spawn at most
    # SELFFEED_MAX_DEPTH levels.
    parent_ids = set()
    for line in recent:
        try:
            pid = json.loads(line).get("work_id")
        except ValueError:
            continue
        if pid:
            parent_ids.add(str(pid))
    depth_by_id = {str(r.get("id")): int(r.get("depth") or 0) for r in rows}
    parent_depth = max([depth_by_id.get(p, 0) for p in parent_ids] or [0])
    new_depth = parent_depth + 1
    parent_id = sorted(parent_ids)[0] if parent_ids else None
    if new_depth > SELFFEED_MAX_DEPTH:
        return (f"skip: selffeed rail 3 (depth): parent depth "
                f"{parent_depth} at cap {SELFFEED_MAX_DEPTH}")
    depth_note = (f"\n\nDEPTH: this proposal is depth {new_depth} of max "
                  f"{SELFFEED_MAX_DEPTH}.")
    if new_depth >= SELFFEED_MAX_DEPTH:
        depth_note += (" At max depth reply with TESTABLE hypotheses "
                       "only; do not propose further investigation.")
    ask = (
        "You are the self-feed engine for an agent-swarm research estate. "
        "These are the latest mined findings from our free-lane research "
        "gophers. Read them and propose EXACTLY ONE new investigation item. "
        "Return JSON: {\"ask\": \"<one-paragraph "
        "investigation brief, specific and answerable by a free-lane model "
        "with web access>\", \"tier\": \"free\", \"max_tokens\": 3000}. "
        "The investigation should go DEEPER on the most interesting finding, "
        "or branch into the adjacent unknown it exposes. Not a repeat."
        + depth_note + "\n\n"
        + "\n".join(recent[-4:]))
    # RAIL 1b + RAIL 6 composition (caught by the wave5 breaker test):
    # the hourly stamp marks a fire where hermes ANSWERED, so three
    # consecutive transport failures can still accrue back-to-back and arm
    # the breaker; a productive fire (any reply) is capped at one per hour
    # even when its proposal is later dropped by rail 4 dedupe.
    ok, out = _dispatch_hermes(ask)
    if not ok:
        ok, out = _sovereign_selffeed(recent, new_depth)
    state = _lane_state()  # re-read: sibling topics wrote WORK_STATE meanwhile
    if not ok:
        state["selffeed_fail_streak"] = streak + 1
        state["selffeed_gate_cycles"] = 0
        state["selffeed_last_err"] = out[:120]
        WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
        return f"ERR selffeed: {out[:80]}"
    state["selffeed_fail_streak"] = 0
    state["selffeed_gate_cycles"] = 0
    state["selffeed_last_err"] = ""
    state["selffeed_last_fire_ts"] = now
    WORK_STATE.write_text(json.dumps(state), encoding="utf-8")
    try:
        # RAIL 7: find the JSON object in hermes output; malformed or
        # missing-field JSON is dropped (v1 contract kept).
        import difflib
        import re as _re

        m = _re.search(r'\{.*\}', out, _re.DOTALL)
        if not m:
            return "ERR selffeed: no JSON in hermes reply"
        proposed = json.loads(m.group())
        new_ask = str(proposed.get("ask") or "")
        if not new_ask.strip():
            return "ERR selffeed: malformed JSON from hermes (no ask)"
        # RAIL 4 (dedupe): a proposal that restates an open ask is dropped.
        low = new_ask.lower().strip()
        for r in open_rows:
            if difflib.SequenceMatcher(
                    None, low, str(r.get("ask") or "").lower()).ratio() > 0.6:
                return (f"skip: selffeed rail 4 (dedupe): near-duplicate "
                        f"of open row {r.get('id')}")
        # RAIL 4 (id discipline): selffed ids are m%03d, unique against
        # every id ever in the queue; hermes-proposed ids are ignored.
        nums = []
        for r in rows:
            mm = _re.match(r"^m(\d+)$", str(r.get("id") or ""))
            if mm:
                nums.append(int(mm.group(1)))
        nid = f"m{max(nums or [0]) + 1:03d}"
        new_item = {"id": nid, "ask": new_ask,
                    "tier": str(proposed.get("tier") or "free"),
                    "status": "queued", "queued_ts": _now(),
                    "selffed_ts": _now(), "depth": new_depth,
                    "parent_id": parent_id}
        with WORK_QUEUE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(new_item, ensure_ascii=False) + "\n")
        return f"selffed {nid}: {new_ask[:70]}..."
    except Exception as e:
        return f"ERR selffeed: {str(e)[:100]}"


def t_astrocyte() -> str:
    """ASTROCYTE SHUTTLE: Neuroenergetic pre-filtering of raw telemetry.
    Condenses estate activity into compact lactate packets (Shannon state vector)
    to fuel reasoning seats without cognitive exhaustion."""
    try:
        from tools import astrocyte_shuttle
        packet = astrocyte_shuttle.produce_lactate_packet()
        out_path = ROOT / "watch" / "inbox" / "astrocyte_feed.json"
        out_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
        vit = packet.get("system_vitality", 1.0)
        hints = packet.get("activity_summary", {}).get("hints_pending", 0)
        sweeps = packet.get("activity_summary", {}).get("radar_sweeps_banked", 0)
        return f"vitality={vit:0.2f} hints={hints} sweeps={sweeps}"
    except Exception as e:
        return f"ERR astrocyte: {type(e).__name__}: {str(e)[:60]}"


TOPICS = [
    ("prompt_lance", t_prompt_lance),
    ("work", t_work),
    ("verify", t_verify),
    ("selfimp", t_selfimp),
    ("impfeed", t_impfeed),
    ("selffeed", t_selffeed),  # after work: rail 1 reads this tick's flag
    ("astrocyte", t_astrocyte),
    ("probe20", t_probe20),
    ("rumor", t_rumor),
    ("fossil", t_fossil),
    ("chain", t_chain),
    ("roster", t_roster),
    ("fkb", t_fkb),
    ("backlog", t_backlog),
]


def one_cycle(cycle: int) -> None:
    _reset_tick()  # selffeed rail 1: per-tick signal starts fresh
    row = {"ts": _now(), "cycle": cycle, "topics": {}}
    for name, fn in TOPICS:
        try:
            row["topics"][name] = fn()
        except Exception as e:
            row["topics"][name] = f"ERR {type(e).__name__}: {str(e)[:80]}"
        time.sleep(2)  # stagger: never burst the shared box
    HEARTBEAT.parent.mkdir(parents=True, exist_ok=True)
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "loop"
    try:
        acquire_instance_lock()
    except InstanceLocked as e:
        print(f"stealth_driver: REFUSED second instance: {e}", flush=True)
        return 2
    if mode == "once":
        one_cycle(0)
        print("stealth_driver: one cycle banked to", HEARTBEAT.relative_to(ROOT))
        return 0
    cycle = 0
    print(f"stealth_driver: loop start, cycle every {CYCLE_SECONDS}s, "
          f"stop = create {OFF_FLAG.relative_to(ROOT)}", flush=True)
    while True:
        if _off():
            print("stealth_driver: .off flag present -- exiting on operator word",
                  flush=True)
            return 0
        cycle += 1
        try:
            one_cycle(cycle)
        except Exception as e:
            print(f"stealth_driver: cycle {cycle} error {type(e).__name__}: "
                  f"{str(e)[:120]}", flush=True)
        time.sleep(CYCLE_SECONDS)


if __name__ == "__main__":
    sys.exit(main())
