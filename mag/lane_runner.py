"""lane_runner — the in-cage, headless lane engine (container-native lanes).

Operator order 2026-09-04 evening: agents spawning terminals on the shared desktop
is a defect class — recurring work must be HEADLESS and IN THE CONTAINERS
(headless-only + docker-not-desktop, 2026-08-25/26). This module is the
container-native successor of the ZCode-scheduled lane tasks: it runs INSIDE
mag-sovereign via `docker exec`, opens no window on any OS, and drives the lanes
off the same file chassis (queue/lanes/<lane>/{inbox.jsonl,surface.md,trail.jsonl}).

Laws wired in:
- LAW-058 PIN-CHECK: free lanes only — this runner refuses any paid-lane call by
  construction (single flash helper, z_ai3 Lite, thinking off).
- LAW-056 COUNTER-TEETH: economist RED flags escalate to the operator inbox row.
- LAW-055 HUMAN-PACED: external fetches are few, timed out short, never looped,
  and pass the SSRF guard (https only, public IPs only, redirects refused).
- ADOPT-2 HANDOFF GATE: every inbox drop is gated (schema/ttl/anchor) before the
  lane acts; gate verdicts are trail rows.

Usage:
  python mag/lane_runner.py --lane economist --once   # one cycle, one lane
  python mag/lane_runner.py --lane all --once         # every lane once
  python mag/lane_runner.py --daemon                  # the schedule loop (in-cage)

The android lane is NOT schedulable in-cage (adb/emulator are host-bound); it
stays a seat/manual lane by design.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# in-cage imports (models/, mag/ siblings) resolve from the repo root:
sys.path.insert(0, str(ROOT))

LANES = ROOT / "queue" / "lanes"
STATIC = ROOT / "dashboard" / "static"
LOG = ROOT / "logs" / "lane_scheduler.log"
PIDFILE = ROOT / "logs" / "lane_scheduler.pid"

# CADENCE: minutes for recurring lanes, "HH:MM" local for daily lanes.
SCHEDULE = {
    "research": 15,
    "builder": 30,
    "day_work": 30,
    "economist": "06:00",
    "bard_ledger": "20:00",
    "elder": "12:00",
    # "night" is composite (monitor + sweep + march receipt), 23:00-09:00 window.
    "night": "23:00",
    # prose-debt census: daily in the quiet window, before the economist.
    "prose": "05:30",
    # media harvest: drains state/art_queue.jsonl (spend-gated by the queue).
    "forge": "12:00",
    # THE WATCHER: one free model experiencing the fleet feed, dropping breadcrumbs.
    "watcher": "30",
    # ARXIV HARVEST: the day's journals, recorded, mined against ourselves.
    "harvest": "06:30",
}
STALLED_HOURS = 2.0


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ts() -> str:
    return _now().strftime("%Y-%m-%dT%H:%M:%SZ")


def _trail(lane: str, event: str, detail: str, artifacts: list | None = None) -> None:
    lane_dir = LANES / lane
    lane_dir.mkdir(parents=True, exist_ok=True)
    row = {"ts": _ts(), "actor": f"{lane}-cage", "event": event,
           "detail": detail[:400], "artifacts": artifacts or []}
    with (lane_dir / "trail.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _surface_append(lane: str, text: str) -> None:
    p = LANES / lane / "surface.md"
    with p.open("a", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")


def _state(lane: str) -> dict:
    p = LANES / lane / "runner_state.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return {}
    return {}


def _save_state(lane: str, st: dict) -> None:
    p = LANES / lane / "runner_state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def _mirror(lane: str) -> None:
    """Mirror trail + surface to dashboard/static (the operator's board)."""
    lane_dir = LANES / lane
    try:
        (STATIC / "trails").mkdir(parents=True, exist_ok=True)
        (STATIC / "lanes").mkdir(parents=True, exist_ok=True)
        src_t = lane_dir / "trail.jsonl"
        src_s = lane_dir / "surface.md"
        if src_t.exists():
            (STATIC / "trails" / f"{lane}.jsonl").write_text(
                src_t.read_text(encoding="utf-8"), encoding="utf-8")
        if src_s.exists():
            (STATIC / "lanes" / f"{lane}.md").write_text(
                src_s.read_text(encoding="utf-8"), encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        _log(f"mirror fail {lane}: {e}")


def _log(msg: str) -> None:
    line = f"{_ts()} {msg}"
    print(line, flush=True)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:  # noqa: BLE001
        pass


# ------------------------------------------------------------------ SSRF guard
class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # noqa: ANN002, ANN003
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _safe_https_url(url: str) -> bool:
    """Mimosa SSRF guard: https only, host must resolve to a PUBLIC address,
    redirects refused. Blocks private/loopback/link-local/metadata targets."""
    try:
        p = urllib.parse.urlparse(url)
        if p.scheme != "https" or not p.hostname:
            return False
        for info in socket.getaddrinfo(p.hostname, 443, proto=socket.IPPROTO_TCP):
            ip = ipaddress.ip_address(info[4][0])
            if (ip.is_private or ip.is_loopback or ip.is_link_local
                    or ip.is_reserved or ip.is_multicast or ip.is_unspecified):
                return False
        return True
    except Exception:  # noqa: BLE001
        return False


# ---------------------------------------------------------------- handoff gate
def gate_drop(item: dict, lane: str) -> tuple[bool, list[str]]:
    """ADOPT-2 handoff gate (charter clause 9): one atomic validation per inbox
    drop BEFORE the lane acts. Returns (ok, reasons); every verdict is trailed."""
    reasons: list[str] = []
    for field in ("ts", "from", "task", "where", "why"):
        if not item.get(field):
            reasons.append(f"missing:{field}")
    ttl = item.get("ttl")
    if ttl:
        try:
            exp = datetime.fromisoformat(str(ttl).replace("Z", "+00:00"))
            if _now() > exp:
                reasons.append("ttl:expired")
        except Exception:  # noqa: BLE001
            reasons.append("ttl:unparseable")
    else:
        reasons.append("ttl:missing")
    anchor = item.get("anchor")
    if anchor and not (ROOT / str(anchor)).exists():
        reasons.append(f"anchor:missing({anchor})")
    ok = not reasons
    _trail(lane, "GATE_VERDICT",
           f"{str(item.get('task', '?'))[:80]} -> {'PASS' if ok else 'FAIL: ' + ','.join(reasons)}",
           [str(item.get("anchor", ""))])
    return ok, reasons


def _inbox_new(lane: str) -> list[dict]:
    """New inbox drops since the last processed offset (gate applies to each)."""
    inbox = LANES / lane / "inbox.jsonl"
    if not inbox.exists():
        return []
    st = _state(lane)
    off = int(st.get("inbox_offset", 0))
    lines = inbox.read_text(encoding="utf-8").splitlines()
    items = []
    for ln in lines[off:]:
        ln = ln.strip()
        if not ln:
            off += 1
            continue
        try:
            items.append(json.loads(ln))
        except Exception:  # noqa: BLE001
            pass
        off += 1
    _save_state(lane, {**st, "inbox_offset": off})
    return items


# ------------------------------------------------------------------ flash call
_FLASH_ENDPOINT = "https://api.z.ai/api/paas/v4/chat/completions"
_FLASH_KEY_VARS = ("ZAI_API_KEY_L", "ZAI_API_KEY_LITE", "ZAI_API_KEY")


def flash_call(system: str, user: str, max_tokens: int = 1536) -> str:
    """LAW-058 pin-check baked in: the ONLY model door here is the Lite coding-plan
    key (ZAI_API_KEY_L, the Calcifer lane) on glm-5.3-flash. CORRECTED 2026-09-05:
    this is NOT the fleet's $0 lane — the promo verdict proved Lite metered
    (10,000 credits/wk real credits; the "zero-metered night window" belief was
    falsified). Paced by mag/lite_guard.py (law 15 daily ceiling), past it raises.
    5.x law: thinking cannot be disabled — reasoning_effort low + max_tokens >= 1536
    (epoch-1 medicine). march_228.py's proven request shape; endpoint passes the
    SSRF guard; redirects refused (_OPENER)."""
    from mag import lite_guard
    g = lite_guard.check("lane_runner")
    if not g["ok"]:
        raise RuntimeError(g["deny"])
    key = next((os.environ[v] for v in _FLASH_KEY_VARS if os.environ.get(v)), "")
    if not key:
        raise RuntimeError("no Lite key in cage env (flash lane down)")
    if not _safe_https_url(_FLASH_ENDPOINT):
        raise ValueError("blocked: endpoint failed SSRF guard (scheme/host/resolved-IP)")
    body = {"model": "glm-5.3-flash",
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "max_tokens": max_tokens, "temperature": 0.2,
            "thinking": {"type": "enabled"}, "reasoning_effort": "low"}
    req = urllib.request.Request(_FLASH_ENDPOINT, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + key})
    with _OPENER.open(req, timeout=120) as r:
        data = json.loads(r.read())
    _u = data.get("usage") or {}
    lite_guard.record("lane_runner",
                      int(_u.get("prompt_tokens") or 0) + int(_u.get("completion_tokens") or 0))
    # PASSIVE THOUGHT BANK (2026-09-05): one choke point, mag/thought_bank.py —
    # verbatim reasoning to memory/thinking/, silent-fail, all models by design.
    try:
        from mag.thought_bank import bank_response
        bank_response("glm-5.3-flash", user, data, lane="cage")
    except Exception:  # noqa: BLE001 — bank, not break
        pass
    return ((data.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()


# ----------------------------------------------------------------- lane cycles
def _run_script(path: str, timeout: int = 600) -> tuple[int, str]:
    p = ROOT / path
    if not p.exists():
        return 2, f"missing: {path}"
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True,
                           text=True, timeout=timeout, cwd=str(ROOT))
        out = ((r.stdout or "") + (r.stderr or ""))[-1500:]
        return r.returncode, out
    except Exception as e:  # noqa: BLE001
        return 1, f"{type(e).__name__}: {e}"


def _latest_sweep_report() -> "Path | None":
    sweeps = sorted((ROOT / "watch" / "usage_sweeps").glob("USAGE_SWEEP_*.md"))
    return sweeps[-1] if sweeps else None


def _sweep_flag_count(p: "Path") -> int:
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        return -1
    return len([ln for ln in text.splitlines()
                if "OUTPUT-RATIO:" in ln or "PIN-EXPIRY:" in ln or "CONTEXT-DEBT:" in ln])


def cycle_economist() -> str:
    # hunger ledger: cage copy first (watch/ is mounted; scripts/ is not), then canonical.
    rc2, out2 = _run_script("watch/cage_bin/hunger_ledger.py")
    if rc2 == 2:
        rc2, out2 = _run_script("scripts/hunger_ledger.py")
    # LAW-056 teeth: read the newest HOST-produced sweep report (the sweep itself is
    # host-db-bound: it reads ~/.zcode/cli/db/db.sqlite which no container sees —
    # parked pending an operator-sanctioned data door). Escalate ONCE per report.
    rep = _latest_sweep_report()
    flags = _sweep_flag_count(rep) if rep else -1
    st = _state("economist")
    if rep is not None and flags > 0 and st.get("escalated_sweep") != rep.name:
        _surface_append("economist",
            f"\n## CAGE ESCALATION {_ts()}\nusage sweep {rep.name} FLAGS={flags} — "
            f"premium burn law violation (see the report)\n")
        esc = {"ts": _ts(), "from": "lane_runner",
               "task": "OPERATOR INBOX: usage sweep flagged premium burn (see economist surface)",
               "where": f"watch/usage_sweeps/{rep.name}",
               "why": "LAW-056 counter-teeth: RED flag auto-escalation",
               "ttl": "", "anchor": "queue/lanes/economist/surface.md"}
        try:
            with (LANES / "day_work" / "inbox.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps(esc, ensure_ascii=False) + "\n")
        except Exception:  # noqa: BLE001
            pass
        _save_state("economist", {**st, "escalated_sweep": rep.name})
    _trail("economist", "CYCLE",
           f"hunger rc={rc2}; sweep={rep.name if rep else 'none'} flags={flags}; {out2[-160:]}")
    return f"hunger rc={rc2}, sweep_flags={flags}"


def cycle_research() -> str:
    rc, out = _run_script("watch/monitor_lane.py", timeout=300)
    _trail("research", "MONITOR", f"monitor_lane rc={rc}: {out[-250:]}")
    n = 0
    for item in _inbox_new("research"):
        ok, why = gate_drop(item, "research")
        if not ok:
            continue
        # LAW-055: one gentle fetch per drop, short timeout, redirects refused.
        url = str(item.get("url") or item.get("where") or "")
        title = url[:120]
        if url.startswith("https://") and _safe_https_url(url):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with _OPENER.open(req, timeout=8) as resp:
                    head = resp.read(4096).decode("utf-8", "ignore")
                a, b = head.find("<title>"), head.find("</title>")
                if 0 <= a < b:
                    title = head[a + 7:b][:160]
            except Exception as e:  # noqa: BLE001
                title = f"fetch-failed({type(e).__name__})"
        elif url.startswith("http"):
            title = "blocked:ssrf-guard"
        score = ""
        try:
            score = flash_call(
                "You triage research links for an AI-agent fleet. Reply EXACTLY: "
                "SCORE: <0-10> | ONE-LINE: <what it is> | VERDICT: <CARD|SHELF|SKIP>",
                f"Link: {url}\nTitle: {title}\nContext: {str(item.get('why'))[:300]}")
        except Exception as e:  # noqa: BLE001
            score = f"lane-down({e})"
        _surface_append("research", f"\n### DROP {str(item.get('task', ''))[:60]}\n"
                        f"- url: {url[:160]}\n- title: {title}\n- triage: {score}\n"
                        f"- gated: {'PASS' if ok else 'FAIL ' + ','.join(why)}\n")
        n += 1
    return f"monitor rc={rc}, drops gated={n}"


def cycle_builder() -> str:
    n = 0
    for item in _inbox_new("builder"):
        ok, why = gate_drop(item, "builder")
        _surface_append("builder",
            f"\n### GATED DROP {str(item.get('task', ''))[:70]}\n"
            f"- gate: {'PASS' if ok else 'FAIL ' + ','.join(why)}\n"
            f"- where: {item.get('where')}\n- ttl: {item.get('ttl')}\n"
            f"- state: {'QUEUED for in-cage build shift (window_throttle claim first)' if ok else 'REFUSED'}\n")
        n += 1
    _trail("builder", "CYCLE", f"drops gated={n}; queue on surface")
    return f"gated={n}"


def cycle_bard() -> str:
    today = _now().strftime("%Y%m%d")
    cards = sorted((ROOT / "watch").glob(f"*_{today}.md"))
    ledger = ROOT / "watch" / f"DAY_LEDGER_{_now().strftime('%Y-%m-%d')}.md"
    names = ", ".join(c.name for c in cards[-12:])
    row = (f"\n## CAGE ROW {_ts()}\n- cards today: {len(cards)}\n"
           f"- recent: {names}\n- source: watch/ glob (read, not invented)\n")
    try:
        with ledger.open("a", encoding="utf-8") as f:
            f.write(row)
        _trail("bard_ledger", "CYCLE", f"ledger row appended ({len(cards)} cards today)")
        return "row"
    except Exception as e:  # noqa: BLE001
        _trail("bard_ledger", "CYCLE_FAIL", str(e)[:200])
        return "fail"


def cycle_elder() -> str:
    today = _now().strftime("%Y%m%d")
    cards = sorted((ROOT / "watch").glob(f"*_{today}.md"))[-3:]
    if not cards:
        cards = sorted((ROOT / "watch").glob("*.md"),
                       key=lambda p: p.stat().st_mtime)[-3:]
    if not cards:
        _trail("elder", "CYCLE", "no cards to read")
        return "empty"
    digest = []
    for c in cards:
        try:
            digest.append(f"--- {c.name} ---\n" + c.read_text(encoding="utf-8")[:1200])
        except Exception:  # noqa: BLE001
            pass
    try:
        lens = flash_call(
            "You are the Elder lens: read fleet cards and give the emergent pattern in "
            "physics/compsci/esoteric anchors ONLY where real (name them). End with "
            "THE ELDER'S QUESTION: the question the fleet isn't asking. Label as lens, not claim.",
            "\n\n".join(digest)[:6000], max_tokens=900)
    except Exception as e:  # noqa: BLE001
        lens = f"lane-down: {e}"
    # TRI-STATE TRAIL LAW (elder lens 2026-09-18): the trail may not file a
    # success-shaped CYCLE row when the lens died. lane-down gets CYCLE_FAIL.
    if lens.startswith("lane-down:"):
        _surface_append("elder", f"\n## ELDER LENS (cage, {_ts()}) — LENS NOT CLAIM, Unproven\n"
                        f"{lens}\n")
        _trail("elder", "CYCLE_FAIL", lens[:200])
        return "lane-down"
    _surface_append("elder", f"\n## ELDER LENS (cage, {_ts()}) — LENS NOT CLAIM, Unproven\n"
                    f"{lens}\n")
    _trail("elder", "CYCLE", f"lens on {len(cards)} cards")
    return "lens"


def cycle_day_work() -> str:
    stalled = []
    # HANDSHAKES ARE LOANS (2026-09-05): an operator-unlocked gate with no
    # first-use receipt is a promise idling — surface it every cycle until we
    # drive it or it dies honestly.
    try:
        hs = ROOT / "state" / "handshakes.jsonl"
        if hs.exists():
            for line in hs.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("unlocked_at") and not row.get("first_use"):
                    stalled.append(f"handshake:{row.get('gate')}")
    except Exception as e:  # noqa: BLE001 — flagging must never break the mirror
        stalled.append(f"handshake-scan:{type(e).__name__}")
    for lane in SCHEDULE:
        if lane == "night":
            continue
        t = LANES / lane / "trail.jsonl"
        if not t.exists():
            continue
        age_h = (time.time() - t.stat().st_mtime) / 3600
        if age_h > STALLED_HOURS:
            stalled.append(f"{lane}({age_h:.1f}h)")
        _mirror(lane)
    for f in ("DAY_WORK_DIGEST.md",):
        src = ROOT / "watch" / f
        if src.exists():
            try:
                (STATIC / f).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            except Exception:  # noqa: BLE001
                pass
    _trail("day_work", "CYCLE",
           f"mirrored {len(SCHEDULE) - 1} lanes; STALLED: {', '.join(stalled) if stalled else 'none'}")
    return f"mirrored, stalled={len(stalled)}"


def cycle_night() -> str:
    """Composite night cycle: monitor + usage sweep + march receipt.
    In-window guard (23:00-09:00 local), once per night, $0."""
    hour = _now().astimezone().hour
    if not (23 <= hour or hour < 9):
        return "out-of-window"
    st = _state("night")
    today = _now().strftime("%Y-%m-%d")
    if st.get("last_night") == today:
        return "already-ran"
    parts = []
    rc, _ = _run_script("watch/monitor_lane.py", timeout=300)
    parts.append(f"monitor rc={rc}")
    rc, _ = _run_script("watch/march_228.py", timeout=600)
    # march reads .env for its key — unmounted in-cage; an honest rc=2 is expected
    # until the operator sanctions an env door. Recorded, never faked.
    parts.append(f"march rc={rc}")
    _save_state("night", {**st, "last_night": today})
    _trail("night", "CYCLE", "night composite: " + "; ".join(parts))
    return "; ".join(parts)


def cycle_forge() -> str:
    """Media harvest lane: drain state/art_queue.jsonl through the dual-lane
    forge (grok primary, cogview fallback). Spend-gated by the queue — no
    queue, no spend. Gallery: dashboard/static/art/."""
    from mag.art_forge import forge_once
    r = forge_once(ROOT)
    _trail("forge", "CYCLE", f"forged={r.get('forged')} errors={len(r.get('errors') or [])}")
    return f"forged={r.get('forged')} left={r.get('left_in_queue', 0)} err={len(r.get('errors') or [])}"


def cycle_watcher() -> str:
    """THE WATCHER (2026-09-05): one feed, one free model, experiencing
    everything RESTfully — read snapshot, think, drop breadcrumb clues into
    lane inboxes. Clues are LEADS marked UNPROVEN; evidence-quoted or
    discarded. The environment watches itself; stigmergy does the steering."""
    from mag.single_feed import build_snapshot
    s = build_snapshot()
    md = (ROOT / "memory" / "feed" / "feed_snapshot.md").read_text(encoding="utf-8",
                                                                  errors="replace")
    system = ("You are THE WATCHER of a fleet of AI agents. You read one feed snapshot "
              "of everything the fleet did. Find only what is VISIBLE IN THE SNAPSHOT: "
              "(1) repeating shapes, (2) wrong assumptions (feed rows that contradict a "
              "claim), (3) TESUJI: a FAILURE in one lane whose key datum is exactly what "
              "a DIFFERENT lane needs to win — route the clue to THAT lane, stating what "
              "broke, the usable datum, and the win it enables. Output ONLY a JSON array, "
              "max 3 clues, each: {\"lane\": one of "
              "research|builder|day_work|economist|bard_ledger|elder|forge|prose, "
              "\"shape\": \"...\", \"evidence\": \"verbatim quote from the snapshot\", "
              "\"clue\": \"one-line breadcrumb for that lane's inbox\"}. No evidence "
              "quote, no clue. If nothing: [].")
    out = flash_call(system, md[:6000], max_tokens=900)
    clues = []
    try:
        i, j = out.find("["), out.rfind("]")
        if 0 <= i < j:
            parsed = json.loads(out[i:j + 1])
            clues = [c for c in parsed if isinstance(c, dict) and c.get("evidence")]
    except Exception:  # noqa: BLE001 — watcher output is leads, never law
        clues = []
    dropped = []
    for c in clues[:3]:
        lane = c.get("lane") if c.get("lane") in SCHEDULE else "day_work"
        inbox = ROOT / "queue" / "lanes" / lane / "INBOX"
        inbox.mkdir(parents=True, exist_ok=True)
        stamp = _now().strftime("%Y%m%dT%H%M%SZ")
        crumbs = (f"**WATCHER BREADCRUMB** (UNPROVEN lead — verify before acting) {stamp}\n\n"
                  f"- shape: {c.get('shape', '')}\n"
                  f"- evidence: `{str(c.get('evidence', ''))[:220]}`\n"
                  f"- clue: {c.get('clue', '')}\n")
        (inbox / f"watcher_{stamp}.md").write_text(crumbs, encoding="utf-8")
        _trail(lane, "WATCHER_CRUMB", str(c.get("clue", ""))[:160])
        dropped.append(f"{lane}:{str(c.get('clue', ''))[:60]}")
    return f"watched chars={s['chars']} clues={len(clues)} dropped={len(dropped)}"


def cycle_harvest() -> str:
    """ARXIV HARVEST (2026-09-05): the day's journals recorded to corpus/, massaged,
    mined against our interest map, top hits dropped to research. Truly stateless —
    the world's research becomes files any era can read."""
    from mag.arxiv_harvest import harvest
    r = harvest()
    _trail("harvest", "CYCLE", f"fetched={r['fetched']} new={r['new']} hits={r['hits']}")
    return f"fetched={r['fetched']} new={r['new']} hits={r['hits']}"


def cycle_prose() -> str:
    """Prose-debt census (2026-09-05, operator: 'no monkeypatches'): the debt as
    a measured queue — stale/fossil files, ghost refs, launcher-shaped fences —
    filed to watch/ so conversion-to-structure works a list, not a feeling."""
    from mag.prose_census import run_census
    s = run_census(ROOT)
    _trail("prose", "CYCLE",
           f"census files={s['files']} stale={s['stale']} fossil={s['fossil']} "
           f"ghost={s['ghost_refs']} launchers={s['launchers']}")
    return (f"census files={s['files']} stale={s['stale']} fossil={s['fossil']} "
            f"ghost={s['ghost_refs']} launchers={s['launchers']}")


CYCLES = {
    "research": cycle_research,
    "builder": cycle_builder,
    "economist": cycle_economist,
    "bard_ledger": cycle_bard,
    "elder": cycle_elder,
    "day_work": cycle_day_work,
    "night": cycle_night,
    "prose": cycle_prose,
    "forge": cycle_forge,
    "watcher": cycle_watcher,
    "harvest": cycle_harvest,
}


# ------------------------------------------------------------------ scheduling
def _due(lane: str) -> bool:
    st = _state(lane)
    last = st.get("last_run")
    now = _now().astimezone()
    cad = SCHEDULE.get(lane)
    if isinstance(cad, int):
        if not last:
            return True
        age = (_now() - datetime.fromisoformat(last)).total_seconds() / 60
        return age >= cad
    if isinstance(cad, str) and cad.count(":") == 1:
        hh, mm = (int(x) for x in cad.split(":"))
        if (now.hour, now.minute) < (hh, mm):
            return False
        return st.get("last_day") != now.strftime("%Y-%m-%d")
    return False


def tesuji_pass(lane: str, failure: str) -> None:
    """TESUJI AT THE MOMENT OF FAILURE (2026-09-05, operator: "how can you spot a
    tesuji 30m ago?" — you can't; batch sees shapes, tesuji needs immediacy).
    Fired synchronously when a lane fails: the failure's key datum is matched
    across lanes NOW, while the next cycles are still open. $0 lane, silent-fail."""
    try:
        snap = ROOT / "memory" / "feed" / "feed_snapshot.md"
        ctx = snap.read_text(errors="replace")[-2500:] if snap.exists() else "(no feed yet)"
        out = flash_call(
            "A fleet lane just failed. Decide if the failure's key datum is exactly "
            "what a DIFFERENT lane needs to win (a tesuji: the sacrificed stone wins "
            "elsewhere). If yes output ONLY {\"lane\": <research|builder|day_work|"
            "economist|bard_ledger|elder|forge|prose>, \"datum\": \"the usable fact\", "
            "\"win\": \"what the other lane does with it\"}. If the datum helps no "
            "other lane, output ONLY {}.",
            "failed lane: " + lane + "\nfailure: " + failure[:600]
            + "\nrecent fleet context:\n" + ctx,
            max_tokens=400)
        i, j = out.find("{"), out.rfind("}")
        if not (0 <= i < j):
            return
        c = json.loads(out[i:j + 1])
        dst = c.get("lane")
        if dst not in SCHEDULE or dst == lane or not c.get("datum"):
            return
        inbox = ROOT / "queue" / "lanes" / dst / "INBOX"
        inbox.mkdir(parents=True, exist_ok=True)
        stamp = _now().strftime("%Y%m%dT%H%M%SZ")
        body = (f"**TESUJI PASS** (UNPROVEN lead) {stamp} — failure in {lane}\n\n"
                f"- datum: {c.get('datum', '')}\n- win: {c.get('win', '')}\n"
                f"- failure: `{str(failure)[:200]}`\n")
        (inbox / f"tesuji_{stamp}.md").write_text(body, encoding="utf-8")
        _trail(dst, "TESUJI_DROP", f"from {lane}: {c.get('datum', '')}"[:160])
        _log(f"tesuji {lane}->{dst} datum={str(c.get('datum', ''))[:60]}")
    except Exception:  # noqa: BLE001 — never let the tesuji pass break the lane loop
        pass


def run_lane(lane: str) -> str:
    fn = CYCLES.get(lane)
    if fn is None:
        return f"unknown lane {lane}"
    t0 = time.time()
    try:
        result = fn()
    except Exception as e:  # noqa: BLE001
        result = f"EXC {type(e).__name__}: {e}"
        _trail(lane, "CYCLE_FAIL", result)
    if result.startswith("EXC") or " rc=1" in result or " rc=2" in result:
        tesuji_pass(lane, result)
    _mirror(lane)
    st = _state(lane)
    st["last_run"] = _now().isoformat()
    st["last_day"] = _now().strftime("%Y-%m-%d")
    st["last_result"] = str(result)[:200]
    _save_state(lane, st)
    _log(f"lane={lane} result={result} ({time.time() - t0:.1f}s)")
    return str(result)


def daemon() -> None:
    # SINGLE-WRITER GUARD (2026-09-05, the doubled-log lesson): _log() writes
    # LOG itself; if a launcher ALSO redirects our stdout into that same file,
    # every row lands twice. Refuse the launch instead of running double-mouthed.
    try:
        st_out, st_log = os.fstat(1), LOG.stat()
        if (st_out.st_dev, st_out.st_ino) == (st_log.st_dev, st_log.st_ino):
            print(f"{_ts()} daemon REFUSED: stdout redirects into {LOG.name} —"
                  " one file, one writer; start without the >> redirect", flush=True)
            return
    except OSError:
        pass
    # SINGLE-DAEMON GUARD (the respawn-law lesson, applied to this organ): a second
    # scheduler would double-run every lane. Refuse if a live holder exists.
    try:
        if PIDFILE.exists():
            old = int(PIDFILE.read_text(encoding="utf-8").strip() or 0)
            os.kill(old, 0)  # alive?
            _log(f"daemon REFUSED: pid {old} already holds {PIDFILE.name}")
            return
    except (ProcessLookupError, ValueError, PermissionError):
        pass  # stale/absent holder — take the lock
    except OSError:
        return
    PIDFILE.parent.mkdir(parents=True, exist_ok=True)
    PIDFILE.write_text(str(os.getpid()), encoding="utf-8")
    _log(f"lane_scheduler daemon UP pid={os.getpid()} lanes={list(SCHEDULE)}")
    _trail("day_work", "SCHEDULER_UP",
           f"in-cage lane scheduler armed; lanes={list(SCHEDULE)}")
    _mirror("day_work")
    beats = 0
    try:
        while True:
            for lane in SCHEDULE:
                try:
                    if _due(lane):
                        run_lane(lane)
                except Exception as e:  # noqa: BLE001
                    _log(f"loop exc {lane}: {e}")
            beats += 1
            if beats % 60 == 0:  # hourly heartbeat
                _trail("day_work", "HEARTBEAT", "scheduler alive, all lanes stateful")
                _mirror("day_work")
            time.sleep(60)
    finally:
        try:
            PIDFILE.unlink()
        except OSError:
            pass


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lane", default="all", choices=list(SCHEDULE) + ["all"])
    ap.add_argument("--once", action="store_true", help="one cycle now (default)")
    ap.add_argument("--daemon", action="store_true", help="run the schedule loop")
    a = ap.parse_args(argv)
    if a.daemon:
        daemon()
        return 0
    lanes = list(SCHEDULE) if a.lane == "all" else [a.lane]
    for lane in lanes:
        print(f"{lane}: {run_lane(lane)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
