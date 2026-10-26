"""percolator — raw signal in; noise/theater stripped; repeatables compiled to invariants;
novel signal explored + folded. Applied EVERYWHERE (training-signal detection, X-tabs, intake).

Operator (2026-08-11): "raw signal invariant stripped of noise and theater. anything that can be
repeated is compiled into invariants anything novel explored and folded" + "for training signal
detection and false positives do this everywhere" + "put the noise in a noise file".

THE PIPELINE (deterministic, $0 — no LLM, module functions only):
  percolate(text) ->
    split into sentences
    classify each: SIGNAL vs THEATER vs NOISE (lexicon scoring, no hallucination)
    noise/theater sentences -> NOISE FILE (memory/ghost/noise/<domain>.jsonl)
    clean signal -> canonical fingerprint (hash of the signal sentences)
    if that canonical has been seen before  -> REPEAT  -> compile to INVARIANT (fold via fact_bus +
      invariant registry, dedupe by content hash). Recurrence = stable truth worth compiling.
    if it is NOVEL (first time)            -> NOVEL   -> log to the EXPLORE queue (deep research /
      steal / synthesis / frontier assistance) so it gets explored and folded.
  inaccessible / blocked input            -> INTAKE REGISTER (memory/ghost/intake/register.jsonl)
      status 'open', to look into later (inference/steering assistance when deep in training).
  false positives (a detected training signal that is actually noise) -> filtered + counted, so the
      lexicon/registry learns and the FP rate drops. Honesty: a false positive is logged, never
      carried forward as truth.
  --candidates (fillball-1001, 2026-10-01; GAP_REGISTER rank 6): mine digests
      (watch/inbox/frontier_olm_*/percolator_candidates.jsonl) ingest into the REVIEW PASS
      (memory/percolator/candidates.jsonl) as candidates, promoted=False. The promote gate
      stays alpha-budget: ingestion never compiles invariants or explore rows; promotion
      happens only through the standing percolate() path on reviewed signal.

COUNT LAWS (Z15, 2026-09-29, S15 diagnosis — the top invariant read 232,214 self-reinforcements
= 79.8% of all events; configs/mates.yaml: "the percolator's memorization is an exploit played
by the loop on itself"; receipt watch/inbox/hydrology/Z15_PERCOLATOR_FIX.md):
  1. HALF-LIFE DECAY — count halves every half_life_days without reinforcement (applied at
     increment time + by maintenance(); config configs/percolator.json, default 30 days).
  2. HEAL-MERGE TAKES MAX, NOT SUM — idempotent: healing N times from the same seal never
     inflates a count (SUM re-added the sealed count on every heal event = triple-counting).
  3. SELF-EMISSION CAP — an invariant reinforced by the same source within the same cycle
     (UTC day) counts ONCE per cycle, not once per repetition. The exploit: pro_library.fire
     logs a "[steer] …" behavioral event per fire, operator_inbox percolates every behavioral
     event, so each fire re-incremented the very invariant that told seats to fire it.

INVARIANT CASCADE (CP-1 port, 2026-10-03, gala build-it-all lane cascade-port): the promote
gate compiled invariants but never re-evaluated dependents when a parent moved. The gap was
confirmed at data level by the localfirst-steal atlas lane (watch/inbox/localfirst/atlas.md
section 3: 639 registry rows, zero dependency fields of any kind). The port, per that spec's
section 4, adds:
  1. depends_on edges on registry rows - DECLARED via declare_depends_on() at fold time,
     MINED via mine_depends_on() (16-hex hash citations + substring derivations, deterministic
     + $0, applies additive-only with a pre-edit backup);
  2. cascade() - BFS over REVERSE dependency edges (dependents first, visited-set cycle
     guard, max_depth 10 / max_nodes 5000, shallowest-first: the Atlas RippleEngine shape),
     emitting PROPOSALS to the review pass (memory/percolator/cascade_queue.jsonl, status
     pending, promoted False) plus a chained receipt (memory/percolator/cascades.jsonl,
     schema invariant_cascade.v1, cascade_id = sha256(prev|origin|proposals)[:16]).
  PROPOSALS, NEVER MUTATIONS: cascade() never edits invariants.json - every route
  (refresh when the parent premise holds, escalate when it broke: removed/superseded/expired)
  is a pending review row. This port deliberately does NOT auto-apply the atlas spec's
  REFRESH bucket: Atlas's own unwired AUTO_APPLY (atlas.md defect 2.1) is the anti-pattern
  named and avoided, and the same alpha-budget discipline as the --candidates ingest holds.

Schema: percolator.v1 · cascade rows: invariant_cascade.v1 · deterministic + $0 · deps: stdlib only (config file is JSON, not yaml)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "percolator.v1"
NOISE_DIR = ROOT / "memory" / "ghost" / "noise"
INTAKE_DIR = ROOT / "memory" / "ghost" / "intake"
INVARIANT_REGISTRY = ROOT / "memory" / "percolator" / "invariants.json"
SEALS_DIR = ROOT / "memory" / "seals"
EXPLORE_QUEUE = ROOT / "memory" / "percolator" / "explore.jsonl"
# --candidates review pass (fillball-1001, 2026-10-01; GAP_REGISTER rank 6 a02-r2):
# mine digests (watch/inbox/frontier_olm_*/percolator_candidates.jsonl) had ZERO
# consumers (grep mag/ tools/ tests/ = 0 hits). Ingest lands rows HERE, status
# "candidate", promoted=False. THE PROMOTE GATE STAYS ALPHA-BUDGET: this path never
# writes invariants.json or explore.jsonl; a candidate is promoted to an invariant
# only by the standing percolate() path on reviewed signal, never by ingestion.
CANDIDATES_REVIEW = ROOT / "memory" / "percolator" / "candidates.jsonl"

# ── count laws config (Z15, 2026-09-29) ───────────────────────────────────────
# JSON (not yaml) on purpose: this module's contract is stdlib-only. The file is
# OPTIONAL — every key has an in-code default, so a missing/corrupt file degrades
# to the documented defaults, never to a crash.
PERCOLATOR_CFG = ROOT / "configs" / "percolator.json"
_CFG_DEFAULTS: dict[str, Any] = {
    "half_life_days": 30.0,       # law 1: count halves every 30 days without reinforcement
    "cycle": "utc-day",           # law 3 cycle clock: one UTC day = one cycle
    "self_emission_cap": True,    # law 3: same source, same cycle counts once
}
_cfg_cache: dict[str, Any] = {"mtime": None, "data": dict(_CFG_DEFAULTS)}


def _cfg() -> dict[str, Any]:
    """Load count-law config (mtime-cached; defaults on any read/parse failure)."""
    try:
        m = PERCOLATOR_CFG.stat().st_mtime
        if _cfg_cache["mtime"] != m:
            data = json.loads(PERCOLATOR_CFG.read_text(encoding="utf-8"))
            merged = dict(_CFG_DEFAULTS)
            if isinstance(data, dict):
                for k, v in _CFG_DEFAULTS.items():
                    if k in data and data[k] is not None:
                        merged[k] = data[k]
            _cfg_cache.update(mtime=m, data=merged)
        return dict(_cfg_cache["data"])
    except Exception:
        return dict(_CFG_DEFAULTS)

# ── signal lexicon (deterministic scoring, no hallucination) ──────────────────
SIGNAL_HINTS = (
    "system prompt", "you are", "available tools", "guidelines", "tools:",
    "invariant", "architecture", "swarm", "flock", "rib", "procedure", "mechanism",
    "we built", "we made", "how to", "the map precedes", "intended paths", "consensus",
    "agent", "steer", "fold", "verkle", "training signal", "false positive", "noise",
    # moderation-field register (wrongthink invariant map, 2026-09-10): a flag receipt is
    # the platform's sensor firing — refusals/filters/blocks are repeatable field signal.
    "refusal", "content filter", "moderation", "flagged", "shadow cell", "denial",
    "temp block", "reach limit", "unsafe content", "boundary is data",
)
THEATER_HINTS = (
    "thrilled", "excited", "excitedly", "announcement", "breaking", "🚀", "🔥",
    "huge", "massive", "historic", "game-changer", "revolutionary", "unprecedented",
    "amazing", "incredible", "so excited", "to the moon", "check this out",
    "steal_pack", "rib_bus_", "session_id",
)
NOISE_HINTS = (
    "reposted", "retweet", "thread", "follow me", "follow @", "like and share",
    "subscribed", "verified", "sponsored", "advertisement", "sign up", "subscribe",
    "giveaway", "win a", "click the link", "dm me", "replies", "reply to",
)
MIN_SIGNAL_LEN = 3  # a 'sentence' shorter than this is not signal

_SENT_RE = re.compile(r"[^.!?\n]+[.!?]?")
_TOKEN_RE = re.compile(r"[a-z0-9_]+")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_ts(ts: Any) -> datetime | None:
    """Parse an ISO timestamp from the registry (naive treated as UTC; bad -> None)."""
    if not isinstance(ts, str) or not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _cycle_key(now: datetime | None = None) -> str:
    """Law 3 cycle clock: one UTC day = one cycle (config 'cycle': 'utc-day')."""
    return (now or datetime.now(timezone.utc)).date().isoformat()


def _decay_count(count: int, elapsed_days: float, *, half_life_days: float | None = None) -> int:
    """Law 1 (Z15, 2026-09-29): count halves every half_life_days without reinforcement.

    Elapsed time is quantized to WHOLE cycles (UTC days — the law's clock, law 3): decay
    lands per-cycle, so two observations minutes apart decay nothing and two landed a day
    apart decay exactly one day's worth. floor at 1 — an observed invariant never decays to
    0 by time alone (only the false-positive path removes truth claims).
    Pure function; tests hit this directly.
    """
    if half_life_days is None:
        half_life_days = float(_cfg()["half_life_days"])
    whole_cycles = float(int(elapsed_days))  # sub-cycle remainder never decays
    if whole_cycles <= 0 or half_life_days <= 0:
        return int(count)
    return max(1, int(count * (0.5 ** (whole_cycles / half_life_days))))


def _canonical_hex(signal_sentences: list[str]) -> str:
    norm = " ".join(s.strip().lower() for s in signal_sentences if s.strip())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16] if norm else ""


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_RE.findall(text or "") if s.strip()]


def _classify(sentence: str) -> dict[str, Any]:
    low = sentence.lower()
    toks = set(_TOKEN_RE.findall(low))
    signal = sum(1 for h in SIGNAL_HINTS if h in low)
    theater = sum(1 for h in THEATER_HINTS if h in low)
    noise = sum(1 for h in NOISE_HINTS if h in low)
    kind = "signal"
    if noise > 0 and noise >= signal:
        kind = "noise"
    elif theater > 0 and theater >= signal:
        kind = "theater"
    return {"sentence": sentence, "signal": signal, "theater": theater,
            "noise": noise, "kind": kind}


def partition(text: str, *, source: str = "") -> dict[str, Any]:
    """Split raw text into signal / theater / noise sentence classes. Deterministic + $0."""
    signal_s, theater_s, noise_s = [], [], []
    for s in _sentences(text):
        c = _classify(s)
        if len(_TOKEN_RE.findall(c["sentence"].lower())) < MIN_SIGNAL_LEN:
            noise_s.append(c)
            continue
        {"signal": signal_s, "theater": theater_s, "noise": noise_s}[c["kind"]].append(c)
    return {"source": source, "signal": signal_s, "theater": theater_s, "noise": noise_s,
            "n_signal": len(signal_s), "n_theater": len(theater_s), "n_noise": len(noise_s)}


def _append_jsonl(path: Path, entry: dict[str, Any]) -> None:
    """Append one row. The explore queue is also rewritten by fuel_feed.clarify,
    so both sides take the same advisory lock (2026-10-24)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path == EXPLORE_QUEUE:
        from mag.queue_lock import queue_lock
        with queue_lock(path):
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _read_jsonl(path: Path, tail: int = 200) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[-tail:]:
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return out


def _newest_seal_registry() -> Path | None:
    """Newest seal snapshot of the invariant registry, or None (seal dir names are UTC-sortable)."""
    try:
        cands = sorted(SEALS_DIR.glob("*/memory/percolator/invariants.json"))
        return cands[-1] if cands else None
    except OSError:
        return None


def _load_registry() -> dict[str, Any]:
    reg = None
    try:
        if INVARIANT_REGISTRY.is_file():
            reg = json.loads(INVARIANT_REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        reg = None
    seal_path = _newest_seal_registry()
    if seal_path is not None:
        try:
            seal = json.loads(seal_path.read_text(encoding="utf-8"))
        except Exception:
            seal = None
        if isinstance(seal, dict):
            seal_gens = seal.get("invariants") or {}
            live_gens = (reg.get("invariants") or {}) if isinstance(reg, dict) else {}
            # GAP-2 (2026-09-06, seat sealcheck; Astra gap v2 ANSWER.md "recovery presented as
            # conservation"): the heal trigger is a PER-GENERATION ID DIFF against the newest
            # seal — ANY sealed generation missing from live heals. The old >50%-by-count gate
            # could not detect partial loss: deleting ONE sealed generation left a silently
            # "healthy" load. The count gate is kept only as a redundant fast-path pre-check
            # (the ID diff subsumes it); it is never the sole trigger.
            missing = [k for k in seal_gens if k not in live_gens]
            shrank = len(live_gens) * 2 < len(seal_gens)
            if reg is None or missing or shrank:
                try:  # AUTO-HEAL (registry-wipe amnesia 2026-09-06 + partial loss 2026-09-06):
                    # merge newest seal — never start empty, never silently stay partial.
                    merged = dict(seal_gens)
                    if INVARIANT_REGISTRY.is_file():
                        try:
                            live = json.loads(INVARIANT_REGISTRY.read_text(encoding="utf-8"))
                            for k, v in (live.get("invariants") or {}).items():
                                if k in merged:
                                    # Z15 (2026-09-29, S15 diagnosis "heal-merge SUMS counts
                                    # (triple-counting)"): shared count merges take MAX, not SUM.
                                    # MAX is IDEMPOTENT — healing N times from the same seal
                                    # yields the same count every time; SUM re-added the sealed
                                    # count on every heal event (heal.log 2026-09-06..09-26:
                                    # repeated 57/72/109/216-gen heals riding the same seal),
                                    # which is one of the two pumps behind the 232,214 top count.
                                    merged[k]["count"] = max(merged[k].get("count", 0),
                                                              v.get("count", 0))
                                    if (v.get("last_seen") or "") > (merged[k].get("last_seen") or ""):
                                        # carry the cap ledger (law 3) from the fresher side
                                        merged[k]["last_seen"] = v.get("last_seen")
                                        merged[k]["decay_as_of"] = v.get("decay_as_of")
                                        if isinstance(v.get("cycle_hits"), dict):
                                            merged[k]["cycle_hits"] = v.get("cycle_hits")
                                    else:
                                        merged[k]["last_seen"] = max(merged[k].get("last_seen") or "",
                                                                     v.get("last_seen") or "")
                                else:
                                    merged[k] = v
                            seal["false_positives"] = max(seal.get("false_positives", 0),
                                                          live.get("false_positives", 0))
                        except Exception:
                            pass
                    reg = {"invariants": merged, "false_positives": seal.get("false_positives", 0)}
                    _append_jsonl(INVARIANT_REGISTRY.parent / "heal.log",
                                  {"ts": _now(),
                                   "heal": f"auto-healed {len(merged)} generations from {seal_path.parents[2]}"})
                except Exception:
                    reg = None
    if reg is None:
        reg = {"invariants": {}, "false_positives": 0}
    reg.setdefault("invariants", {})
    reg.setdefault("false_positives", 0)
    return reg


def _save_registry(reg: dict[str, Any]) -> None:
    INVARIANT_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    tmp = INVARIANT_REGISTRY.with_name(f"{INVARIANT_REGISTRY.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    try:  # LAW-065 DEMO (2026-09-07, seat gatekeep): receipt the destructive replace.
        # Warn-only era — the receipt is appended, the save is never blocked. Sole demo
        # call site; fleet-wide requirement is operator law, not this build's call.
        from mag.destructive_receipt import record as _receipt
        _receipt(str(INVARIANT_REGISTRY), actor="percolator",
                 reason="atomic registry save (temp+os.replace) — LAW-065 demo call site")
    except Exception:
        pass  # the instrument must never break the writer
    os.replace(tmp, INVARIANT_REGISTRY)  # atomic: empty-file-from-crash is now impossible


def append_noise(items: list[dict[str, Any]], *, domain: str = "general") -> dict[str, Any]:
    """Write the stripped noise/theater to a per-domain noise file (jsonl)."""
    path = NOISE_DIR / f"{domain}.jsonl"
    for it in items:
        _append_jsonl(path, {"ts": _now(), "kind": it["kind"], "sentence": it["sentence"]})
    return {"ok": True, "schema": SCHEMA, "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "n": len(items)}


def noise_log(domain: str = "general", *, tail: int = 200) -> dict[str, Any]:
    path = NOISE_DIR / f"{domain}.jsonl"
    rows = _read_jsonl(path, tail)
    return {"ok": True, "schema": SCHEMA, "domain": domain, "n": len(rows), "rows": rows}


def intake_register(target: str, *, reason_blocked: str, why_useful: str,
                    source: str = "x-tabs", domain: str = "general") -> dict[str, Any]:
    """When input is INACCESSIBLE, log it to the intake register for later (inference/steering)."""
    rec = {"id": hashlib.sha256(f"{target}\x1f{_now()}".encode("utf-8")).hexdigest()[:16],
           "ts": _now(), "target": target, "source": source, "domain": domain,
           "reason_blocked": reason_blocked, "why_useful": why_useful, "status": "open"}
    _append_jsonl(INTAKE_DIR / "register.jsonl", rec)
    return {"ok": True, "schema": SCHEMA, "intake": rec,
            "path": str((INTAKE_DIR / "register.jsonl").relative_to(ROOT)).replace("\\", "/")}


def open_intake(*, tail: int = 200) -> dict[str, Any]:
    rows = [r for r in _read_jsonl(INTAKE_DIR / "register.jsonl", tail) if r.get("status") == "open"]
    return {"ok": True, "schema": SCHEMA, "n_open": len(rows), "rows": rows}


def false_positive(signal_sentence: str, *, reason: str = "detected signal is actually noise",
                   domain: str = "general") -> dict[str, Any]:
    """Filter a FALSE POSITIVE training signal: log it (never carried as truth) + count it."""
    reg = _load_registry()
    reg["false_positives"] = reg.get("false_positives", 0) + 1
    _save_registry(reg)
    _append_jsonl(NOISE_DIR / f"{domain}.fp.jsonl",
                  {"ts": _now(), "sentence": signal_sentence, "reason": reason})
    return {"ok": True, "schema": SCHEMA, "false_positives_total": reg["false_positives"],
            "path": str((NOISE_DIR / f"{domain}.fp.jsonl").relative_to(ROOT)).replace("\\", "/")}


def _compile_invariant(signal_sentences: list[str], canonical: str, *, domain: str,
                       source: str = "") -> dict[str, Any]:
    reg = _load_registry()
    now_dt = datetime.now(timezone.utc)
    now = now_dt.isoformat().replace("+00:00", "Z")
    cycle = _cycle_key(now_dt)
    src = (source or "")[:60]
    inv = reg["invariants"].get(canonical)
    if inv:
        hits = inv.get("cycle_hits") if isinstance(inv.get("cycle_hits"), dict) else {}
        capped = bool(_cfg()["self_emission_cap"]) and hits.get(src) == cycle
        if capped:
            # law 3 (Z15, 2026-09-29): same source, same cycle = ONE count per cycle, not one
            # per repetition. The observation still refreshes last_seen/decay_as_of (the
            # invariant is demonstrably still alive — decay measures ABSENCE), it just cannot
            # pump its own count inside a single cycle.
            pass
        else:
            # law 1 (Z15): decay the stored count over the interval since the last observation
            # baseline (decay_as_of, falling back to last_seen for pre-Z15 rows), THEN +1 for
            # this reinforcement. Long absence floors at 1 then re-counts from there.
            baseline = _parse_ts(inv.get("decay_as_of")) or _parse_ts(inv.get("last_seen"))
            if baseline is not None:
                elapsed_days = (now_dt - baseline).total_seconds() / 86400.0
                inv["count"] = _decay_count(int(inv.get("count", 1)), elapsed_days) + 1
            else:
                inv["count"] = int(inv.get("count", 0)) + 1
        inv["last_seen"] = now
        inv["decay_as_of"] = now
        # per-source cycle ledger, pruned to the current cycle (bounded: one entry per source
        # that hit THIS cycle — an A/B/A alternation within a day still counts each source once)
        inv["cycle_hits"] = {s: c for s, c in hits.items() if c == cycle}
        inv["cycle_hits"][src] = cycle
        _save_registry(reg)
        return {"status": "repeat", "invariant": inv["text"], "count": inv["count"],
                "canonical": canonical, "compiled": True, "capped": capped}
    text = " ".join(s.strip() for s in signal_sentences if s.strip())
    reg["invariants"][canonical] = {"text": text, "count": 1, "first_seen": now,
                                    "domain": domain, "last_seen": now, "decay_as_of": now,
                                    "cycle_hits": {src: cycle}}
    _save_registry(reg)
    try:
        from mag import fact_bus
        # fold=False (2026-08-16, sacred-cow fix): a percolator SIGNAL does not need a full
        # verkle session-knot append (append_verkle_knot -> _rewrite_chain uses
        # incremental O(n log n) prefix roots over the whole chain).
        # The fact still lands in the fact STORE + the invariant registry (real data); only the
        # expensive session-knot verkle rewrite is skipped. The spine (verkle_knot) is untouched.
        fb = fact_bus.publish_fact(text[:400], who="percolator", what="compiled_invariant",
                                   when=_now(), domain=domain, fold=False)
    except Exception:
        fb = {}
    return {"status": "novel", "invariant": text, "count": 1, "canonical": canonical,
            "compiled": True, "fact_bus": fb}


def percolate(text: str, *, source: str = "", domain: str = "general",
              fold: bool = True) -> dict[str, Any]:
    """The full percolator. Raw signal -> noise file + invariants (repeat) / explore (novel)."""
    p = partition(text, source=source)
    # 1) strip noise + theater to the noise file
    stripped = p["theater"] + p["noise"]
    noise_res = append_noise(stripped, domain=domain) if stripped else {"ok": True, "n": 0}
    # 2) the clean signal
    signal_sentences = [s["sentence"] for s in p["signal"]]
    canonical = _canonical_hex(signal_sentences)
    if not signal_sentences:
        return {"ok": True, "schema": SCHEMA, "source": source, "verdict": "no_signal",
                "noise": noise_res, "n_signal": 0, "n_stripped": len(stripped)}
    # 3) repeat (compile to invariant) vs novel (explore + fold)
    res = _compile_invariant(signal_sentences, canonical, domain=domain, source=source)
    if res["status"] == "novel":
        # Probe chatter is instrumentation, not a task (2026-10-24 census: 1,492 of
        # 2,388 open rows carried a probe_* domain; four ractors independently named
        # that inflation as the load-bearing defect, and sixteen existing readers
        # were consuming it). The row still lands - the queue is append-only - but
        # it lands as status="probe" so it never counts as open work.
        row_status = "probe" if str(domain).startswith("probe_") else "open"
        _append_jsonl(EXPLORE_QUEUE, {"ts": _now(), "source": source, "domain": domain,
                                      "signal": res["invariant"][:600], "canonical": canonical,
                                      "status": row_status})
    return {"ok": True, "schema": SCHEMA, "source": source, "domain": domain,
            "verdict": res["status"], "n_signal": len(signal_sentences),
            "n_stripped": len(stripped), "canonical": canonical, "signal": res["invariant"],
            "count": res["count"], "capped": res.get("capped", False), "noise": noise_res,
            "explore": res["status"] == "novel",
            "explore_queue": str(EXPLORE_QUEUE.relative_to(ROOT)).replace("\\", "/")}


def percolate_signal(text: str, *, pattern: str = "route_decision", source: str = "",
                     domain: str = "general", emit_event: bool = True) -> dict[str, Any]:
    """APPLY THE PERCOLATOR EVERYWHERE (training-signal detection + false positives).

    Drop-in for any loop that ingests free-text signal (operator messages, behavioral signals,
    research findings). It: (1) strips noise/theater to the noise file, (2) filters false
    positives (a detected signal that is actually noise -> noise .fp file + counted, NEVER carried
    as truth), (3) compiles repeatable signal into an invariant, (4) queues novel signal for
    exploration, and (5) optionally emits a training event (mag.training_events.emit) so the
    signal is captured in the training feed. Deterministic + $0, safe to call from any loop.
    """
    p = percolate(text, source=source or pattern, domain=domain)
    verdict = p.get("verdict", "no_signal")
    fp = False
    if verdict == "no_signal" and text and len(text.strip()) >= MIN_SIGNAL_LEN:
        # text with no detected signal in a signal-bearing path = likely false positive
        fp_res = false_positive(text[:200], reason="no_signal_in_signal_path", domain=domain)
        fp = True
        p["false_positive"] = fp_res
    evt = {}
    if emit_event:
        try:
            from mag import training_events
            evt = training_events.emit(
                pattern if pattern in training_events.VALID_PATTERNS else "route_decision",
                input_data={"source": source or pattern, "text": text[:500]},
                outcome={"verdict": verdict, "stripped": p.get("n_stripped", 0),
                         "signal": p.get("n_signal", 0), "false_positive": fp},
                pattern_tags=["percolator"])
        except Exception as e:
            evt = {"error": str(e)[:120]}
    p["false_positive"] = fp
    p["training_event"] = evt
    return p


# ── --candidates: mine ingest into the review pass (fillball-1001, 2026-10-01) ─
# GAP_REGISTER rank 6 (a02-r2): the olm mine's percolator_candidates.jsonl rows had
# zero consumers and never reached any percolator surface. The fix is a READ PATH
# only: rows land in the review pass (CANDIDATES_REVIEW) as candidates with
# promoted=False. Auto-promotion is forbidden here (the lane contract: the promote
# gate stays alpha-budget) - only percolate() on reviewed signal compiles invariants.

def _expand_candidate_paths(args: list[str]) -> tuple[list[Path], list[str]]:
    """Expand explicit paths or glob patterns (cwd first, then ROOT-anchored).

    Returns (sorted existing files, patterns that matched nothing). Duplicate files
    from overlapping patterns are collapsed so one row is never ingested twice.
    """
    files: dict[str, Path] = {}
    unmatched: list[str] = []
    for arg in args or []:
        hits = [p for p in (Path(arg),) if p.is_file()]
        if not hits:
            import glob as _glob
            hits = [Path(p) for p in sorted(_glob.glob(arg))]
        if not hits and not os.path.isabs(arg):
            import glob as _glob
            hits = [Path(p) for p in sorted(_glob.glob(str(ROOT / arg)))]
        if not hits:
            unmatched.append(arg)
            continue
        for p in hits:
            # store the RESOLVED path: relative glob hits must relativize against
            # ROOT for the review row's "file" field (forward-slash, repo-relative)
            # - a native-separator or absolute leak would break rerun dedupe keys.
            rp = p.resolve()
            files[str(rp)] = rp
    return [files[k] for k in sorted(files)], unmatched


def _candidate_key(review_row: dict[str, Any]) -> tuple[str, int, str]:
    return (str(review_row.get("file") or ""), int(review_row.get("row") or 0),
            str(review_row.get("canonical") or ""))


def ingest_candidates(paths: list[str | Path], *, domain: str = "frontier_mine") -> dict[str, Any]:
    """Ingest mine percolator_candidates.jsonl rows into the REVIEW PASS as candidates.

    Per row: the claim text runs through the standard partition() classifier (noise
    and theater sentences still strip to the domain noise file), and the surviving
    signal is filed in CANDIDATES_REVIEW with status "candidate", promoted=False,
    plus the row's source_url / estate_map / probe (and area / card_path when the
    mine emitted them). A rerun over the same file is IDEMPOTENT: the (file, row,
    canonical) key is deduped against the review file already on disk.

    PROMOTION IS NEVER DONE HERE: this function does not touch INVARIANT_REGISTRY or
    EXPLORE_QUEUE. A candidate reaches invariants.json only through the standing
    percolate() path when the reviewed signal is re-fired for real - the promote
    gate stays alpha-budget, ingestion only makes the rows reviewable.
    """
    files, unmatched = _expand_candidate_paths([str(p) for p in (paths or [])])
    if not files:
        return {"ok": False, "schema": SCHEMA, "n_files": 0, "n_rows": 0,
                "unmatched": unmatched,
                "error": f"no candidates files matched: {unmatched or paths}"}
    seen = {_candidate_key(r) for r in _read_jsonl(CANDIDATES_REVIEW, tail=100_000)}
    n_rows = n_candidate = n_no_signal = n_dupe = n_stripped = 0
    per_file: list[dict[str, Any]] = []
    for path in files:
        rel = str(path.relative_to(ROOT)).replace("\\", "/") if _within(path, ROOT) else str(path)
        f_rows = n_f_new = n_f_dupe = 0
        for i, line in enumerate(_iter_jsonl_lines(path)):
            raw = line.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if not isinstance(row, dict):
                continue
            f_rows += 1
            text = str(row.get("claim") or "").strip()
            if not text:
                n_no_signal += 1
                continue
            source = str(row.get("source_url") or "")[:300]
            p = partition(text, source=source)
            signal_sentences = [s["sentence"] for s in p["signal"]]
            canonical = _canonical_hex(signal_sentences)
            entry = {"ts": _now(), "status": "candidate", "promoted": False,
                     "domain": domain, "file": rel, "row": i,
                     "source": source, "claim": text[:600],
                     "canonical": canonical,
                     "n_signal": len(signal_sentences),
                     "signal": " ".join(signal_sentences)[:600],
                     "estate_map": str(row.get("estate_map") or "")[:400],
                     "probe": str(row.get("probe") or "")[:400]}
            if row.get("area"):
                entry["area"] = str(row["area"])[:120]
            if row.get("card_path"):
                entry["card_path"] = str(row["card_path"])[:300]
            key = _candidate_key(entry)
            if key in seen:
                n_dupe += 1
                n_f_dupe += 1
                continue
            # dedupe gates EVERY disk write: a rerun re-partitions (pure) but must
            # not re-strip noise to the noise file before it hits the dedupe skip
            # (caught live: an idempotence rerun doubled frontier_mine.jsonl).
            seen.add(key)
            stripped = p["theater"] + p["noise"]
            n_stripped += len(stripped)
            if stripped:
                append_noise(stripped, domain=domain)
            _append_jsonl(CANDIDATES_REVIEW, entry)
            n_candidate += 1
            n_f_new += 1
        n_rows += f_rows
        per_file.append({"file": rel, "rows": f_rows, "new": n_f_new, "dupe": n_f_dupe})
    return {"ok": True, "schema": SCHEMA, "domain": domain,
            "n_files": len(files), "files": per_file, "unmatched": unmatched,
            "n_rows": n_rows, "n_candidate": n_candidate, "n_no_signal": n_no_signal,
            "n_dupe": n_dupe, "n_stripped_sentences": n_stripped,
            "n_promoted": 0,
            "promote_gate": "alpha-budget: ingestion never compiles invariants; "
                            "promotion happens only via percolate() on reviewed signal",
            "review_pass": str(CANDIDATES_REVIEW.relative_to(ROOT)).replace("\\", "/")}


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _iter_jsonl_lines(path: Path):
    """Yield raw lines of a jsonl file (whole file, no tail truncation - mine
    candidate files are digests, bounded small; a silently dropped row would be
    a zero-ingestion relapse)."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                yield line
    except OSError:
        return


def _top_rows(invs: dict[str, Any], n: int = 5) -> list[dict[str, Any]]:
    return [{"canonical": k, "count": v.get("count", 0), "text": (v.get("text") or "")[:60]}
            for k, v in sorted(invs.items(), key=lambda kv: -int(kv[1].get("count", 0)))[:n]]


def maintenance(*, dry: bool = True) -> dict[str, Any]:
    """Z15 backfill (2026-09-29): enforce the three count laws on STORED counts.

    Laws 1+3 apply prospectively in _compile_invariant; this pass repairs the historical
    damage already sitting in invariants.json (the 232,214 exploit count among them):

      cap   count <- min(count, distinct cycles observed): without per-hit source history
            the strongest PROVABLE bound on a cycle-deduped count is the number of UTC days
            in [first_seen, last_seen] (inclusive). Conservative: an invariant legitimately
            reinforced by several DISTINCT sources in one day can exceed it — accepted, the
            alternative is keeping a provably self-inflated number.
      decay count <- half-life decay from the observation baseline (decay_as_of, falling back
            to last_seen) to now; floor 1. decay_as_of is stamped on apply so a rerun decays
            only the fresh interval, never compounds.

    dry=True reports only (no disk write, deliberately NOT via _load_registry so a pending
    auto-heal can never surprise-write during a dry run). dry=False backs up the registry
    next to it (invariants.json.bak-z15-<date>) before the atomic replace.
    """
    try:
        original_raw = INVARIANT_REGISTRY.read_text(encoding="utf-8")
        reg = json.loads(original_raw)
    except Exception as e:
        return {"ok": False, "error": f"cannot read registry: {e}", "dry": dry}
    if not isinstance(reg, dict):
        reg = {"invariants": {}}
    invs = reg.setdefault("invariants", {})
    now_dt = datetime.now(timezone.utc)
    now = now_dt.isoformat().replace("+00:00", "Z")
    cap_on = bool(_cfg()["self_emission_cap"])
    top_before = _top_rows(invs)
    changed = 0
    total_before = sum(int(v.get("count", 0)) for v in invs.values())
    for inv in invs.values():
        old = int(inv.get("count", 1))
        count = old
        fs, ls = _parse_ts(inv.get("first_seen")), _parse_ts(inv.get("last_seen"))
        if cap_on and fs is not None and ls is not None:
            observed_days = max(1, (ls.date() - fs.date()).days + 1)
            count = min(count, observed_days)
        baseline = _parse_ts(inv.get("decay_as_of")) or ls
        if baseline is not None:
            count = _decay_count(count, (now_dt - baseline).total_seconds() / 86400.0)
        count = max(1, count)
        if count != old:
            inv["count"] = count
            changed += 1
        inv["decay_as_of"] = now
    backup = None
    if not dry:
        backup = INVARIANT_REGISTRY.with_name(f"{INVARIANT_REGISTRY.name}.bak-z15-{now_dt:%Y%m%d}")
        try:
            backup.write_text(original_raw, encoding="utf-8")  # PRE-EDIT bytes, not the result
        except Exception:
            backup = None  # the atomic save still proceeds; the pre-edit file stays on disk
        _save_registry(reg)
    return {"ok": True, "dry": dry, "n_invariants": len(invs), "n_changed": changed,
            "total_count_before": total_before,
            "total_count_after": sum(int(v.get("count", 0)) for v in invs.values()),
            "top_before": top_before, "top_after": _top_rows(invs), "backup": backup,
            "half_life_days": _cfg()["half_life_days"], "ts": now}


# ── invariant cascade (CP-1, gala build-it-all lane cascade-port, 2026-10-03) ─
# Port of the localfirst-steal atlas lane's cascade ledger spec (watch/inbox/
# localfirst/atlas.md section 4) onto the percolator registry. THE GAP: invariants
# carried no dependency field and the promote gate never re-evaluated dependents
# when a parent moved.
#
# LAWS (atlas.md section 4.3, kept; one ask-level override):
#   PROPOSALS, NEVER MUTATIONS - cascade() reads INVARIANT_REGISTRY and writes only
#   the review pass (CASCADE_QUEUE) + the receipt ledger (CASCADES_LEDGER). The
#   atlas spec auto-applies its REFRESH bucket; this port does NOT: every route is
#   a pending proposal for the review pass (same alpha-budget discipline as the
#   --candidates ingest above), because Atlas's unwired AUTO_APPLY (its defect 2.1)
#   is the named anti-pattern.
#   BFS over REVERSE edges (dependents first), visited-set cycle guard, max_depth
#   10 / max_nodes 5000 defaults, shallowest-first order (Atlas RippleEngine
#   analyze_impact shape - all that terminates).
#   Edge schema (atlas.md section 4.1): {"kind": "invariant", "key": "<16-hex>"}
#   for invariant-to-invariant edges. The spec's fact-kind edges (census, file-sha,
#   law-status, queue-state, receipt-exists) are the unbuilt half: no instruments
#   are wired here, so traversal uses invariant edges only. Honest gap, on record.
CASCADE_QUEUE = ROOT / "memory" / "percolator" / "cascade_queue.jsonl"
CASCADES_LEDGER = ROOT / "memory" / "percolator" / "cascades.jsonl"
CASCADE_SCHEMA = "invariant_cascade.v1"
MIN_EDGE_TEXT_LEN = 12  # substring edges below this length are degenerate noise
_ESCALATE_KINDS = ("removed", "superseded", "expired")
_HEX16_RE = re.compile(r"\b[0-9a-f]{16}\b")


def _invariant_parents(row: dict[str, Any]) -> list[str]:
    """Invariant-kind parent keys of one registry row (missing kind reads as 'invariant')."""
    deps = row.get("depends_on") if isinstance(row, dict) else None
    if not isinstance(deps, list):
        return []
    return [str(e["key"]) for e in deps
            if isinstance(e, dict) and e.get("key")
            and str(e.get("kind") or "invariant") == "invariant"]


def declare_depends_on(canonical: str, parents: list[Any], *, apply: bool = True) -> dict[str, Any]:
    """DECLARED mode (atlas spec 4.1): a lane names which invariants its row depends on.

    Fold-time declaration: merges invariant-kind edges into the row's depends_on,
    deduped by key. All-or-nothing per call: any invalid parent (unknown key,
    self-edge, empty) rejects the whole declaration before a single append. The
    write goes through the sanctioned atomic registry writer only.
    """
    reg = _load_registry()
    invs = reg["invariants"]
    if canonical not in invs:
        return {"ok": False, "error": f"unknown invariant: {canonical}"}
    row = invs[canonical]
    have = {e.get("key") for e in (row.get("depends_on") or []) if isinstance(e, dict)}
    staged: list[dict[str, str]] = []
    for p in parents or []:
        key = str(p.get("key") if isinstance(p, dict) else p or "")
        if not key:
            return {"ok": False, "error": "empty parent key", "canonical": canonical}
        if key == canonical:
            return {"ok": False, "error": "self-dependency rejected", "canonical": canonical}
        if key not in invs:
            return {"ok": False, "error": f"unknown parent invariant: {key}", "canonical": canonical}
        if key not in have:
            have.add(key)
            staged.append({"kind": "invariant", "key": key})
    if apply and staged:
        row.setdefault("depends_on", []).extend(staged)
        _save_registry(reg)
    return {"ok": True, "canonical": canonical, "added": [e["key"] for e in staged],
            "depends_on": row.get("depends_on") or [], "applied": bool(apply and staged)}


def mine_depends_on(*, apply: bool = False) -> dict[str, Any]:
    """MINED mode (atlas spec 4.1): deterministic retroactive dependency edges, $0.

    Two byte-level miners over row text, no judgment calls:
      (a) HASH CITATION - a row whose text cites another row's 16-hex canonical
          key depends on it (atlas spec: invariant-to-invariant edges only where
          one invariant cites another by hash);
      (b) SUBSTRING DERIVATION - a row whose text byte-contains another row's text
          (>= MIN_EDGE_TEXT_LEN chars) depends on it: the container's compiled
          signal includes the child's sentence, so the container's premise
          presupposes the child's.

    apply=False reports only. apply=True adds the depends_on key to EVERY row
    (empty list where no edge was found), merges (never removes) existing edges,
    backs up the registry to invariants.json.bak-cascade-<date> with the PRE-EDIT
    bytes, and saves through the atomic writer. Counts, text, timestamps untouched.
    """
    try:
        raw = INVARIANT_REGISTRY.read_text(encoding="utf-8")
        reg = json.loads(raw)
    except Exception as e:
        return {"ok": False, "error": f"cannot read registry: {e}"}
    invs = reg.get("invariants") or {}
    keys = set(invs)
    mined: dict[str, list[dict[str, str]]] = {}
    for k, v in invs.items():
        text = v.get("text") or ""
        cites = {t for t in _HEX16_RE.findall(text) if t in keys and t != k}
        subs = {other for other, ov in invs.items()
                if other != k and len((ov.get("text") or "").strip()) >= MIN_EDGE_TEXT_LEN
                and (ov.get("text") or "").strip() in text}
        parents = sorted(cites | subs)
        if parents:
            mined[k] = [{"kind": "invariant", "key": p} for p in parents]
    res: dict[str, Any] = {"ok": True, "n_invariants": len(invs),
                           "n_rows_with_edges": len(mined),
                           "n_edges": sum(len(v) for v in mined.values()),
                           "edges": {k: [e["key"] for e in v] for k, v in sorted(mined.items())},
                           "mode": "apply" if apply else "report"}
    if apply:
        now_dt = datetime.now(timezone.utc)
        added = 0
        for k, edges in mined.items():
            row = invs[k]
            have = {e.get("key") for e in (row.get("depends_on") or []) if isinstance(e, dict)}
            new = [e for e in edges if e["key"] not in have]
            if new:
                row.setdefault("depends_on", []).extend(new)
                added += len(new)
        for row in invs.values():  # every row carries the key, edge-free or not
            row.setdefault("depends_on", [])
        backup: Any = None
        try:
            backup = INVARIANT_REGISTRY.with_name(
                f"{INVARIANT_REGISTRY.name}.bak-cascade-{now_dt:%Y%m%d}")
            backup.write_text(raw, encoding="utf-8")  # PRE-EDIT bytes, not the result
        except Exception:
            backup = None  # the atomic save still proceeds; the pre-edit file stays on disk
        _save_registry(reg)
        res.update(added_edges=added, backup=backup)
    return res


def cascade(origin: str, *, change: dict[str, Any] | None = None, max_depth: int = 10,
            max_nodes: int = 5000, write: bool = True) -> dict[str, Any]:
    """Re-evaluate dependents when a parent invariant changes: emit PROPOSALS, never mutations.

    BFS from origin over reverse depends_on edges (dependents first, visited-set
    cycle guard, shallowest-first, max_depth/max_nodes caps). One route per
    cascade, from the origin change: escalate (premise broke: origin absent from
    the registry, or change kind in removed/superseded/expired) or refresh
    (premise holds: parent moved, dependents re-evaluate against its new state).
    Every visited dependent yields a proposal row in the review pass
    (CASCADE_QUEUE, status pending, promoted False); the receipt ledger
    (CASCADES_LEDGER) chains cascade_id = sha256(prev|origin|proposals)[:16] so
    any edited history breaks the walk (detection only, no signature - the verkle
    fold is the external-anchor half, per the atlas spec's own honesty note).

    write=False is pure compute: no queue row, no ledger row, no registry write.
    INVARIANT_REGISTRY is NEVER written by this function in any mode.
    """
    if not origin or not isinstance(origin, str):
        return {"ok": False, "error": "origin key required"}
    reg = _load_registry()
    invs = reg.get("invariants") or {}
    change = dict(change or {})
    kind = str(change.get("kind") or ("removed" if origin not in invs else "changed"))
    broke = origin not in invs or kind in _ESCALATE_KINDS
    route = "escalate" if broke else "refresh"
    rev: dict[str, list[str]] = {}
    for k, v in invs.items():
        for p in _invariant_parents(v):
            rev.setdefault(p, []).append(k)
    for lst in rev.values():
        lst.sort()  # deterministic BFS order: registry-key sorted per level
    parent_count = int(invs[origin].get("count", 0)) if origin in invs else None
    rationale = (f"parent invariant {origin} is {kind}: dependent premise needs review"
                 if broke else
                 f"parent invariant {origin} changed ({kind}): re-evaluation proposed, no auto-edit")
    proposals: list[dict[str, Any]] = []
    depths: list[int] = []
    truncated = False
    visited = {origin}
    q: deque[tuple[str, int]] = deque([(origin, 0)])
    while q and not truncated:
        node, d = q.popleft()
        if d >= max_depth:
            continue
        for child in rev.get(node, []):
            if len(visited) >= max_nodes:
                truncated = True
                break
            if child in visited:
                continue
            visited.add(child)
            depths.append(d + 1)
            proposals.append({"key": child, "depth": d + 1, "route": route,
                              "components": {"change_kind": kind,
                                             "parent_present": origin in invs,
                                             "parent_count": parent_count,
                                             "old": change.get("old"), "new": change.get("new")},
                              "rationale": rationale})
            q.append((child, d + 1))
    now = _now()
    prev = ""
    for r in _read_jsonl(CASCADES_LEDGER, tail=1):
        prev = str(r.get("cascade_id") or "")
    payload = json.dumps(proposals, sort_keys=True, ensure_ascii=False)
    cascade_id = hashlib.sha256(f"{prev}|{origin}|{payload}".encode("utf-8")).hexdigest()[:16]
    routes = {"refresh": 0, "escalate": 0}
    for p in proposals:
        routes[p["route"]] += 1
    res: dict[str, Any] = {"ok": True, "schema": CASCADE_SCHEMA, "origin": origin,
                           "change": change, "kind": kind, "route": route,
                           "impacted": len(proposals), "depths": depths,
                           "truncated": truncated, "routes": routes,
                           "proposals": proposals, "cascade_id": cascade_id,
                           "prev_cascade_id": prev, "write": write,
                           "cascade_queue": str(CASCADE_QUEUE.relative_to(ROOT)).replace("\\", "/"),
                           "cascades_ledger": str(CASCADES_LEDGER.relative_to(ROOT)).replace("\\", "/")}
    if write:
        for p in proposals:
            _append_jsonl(CASCADE_QUEUE, {"schema": CASCADE_SCHEMA, "ts": now,
                          "status": "pending", "promoted": False, "cascade_id": cascade_id,
                          "origin": origin, "change_kind": kind, "key": p["key"],
                          "depth": p["depth"], "route": p["route"],
                          "components": p["components"], "rationale": p["rationale"]})
        _append_jsonl(CASCADES_LEDGER, {"schema": CASCADE_SCHEMA, "ts": now,
                        "cascade_id": cascade_id, "prev_cascade_id": prev,
                        "origin": {"key": origin, "kind": kind,
                                   "old": change.get("old"), "new": change.get("new")},
                        "impacted": len(proposals), "depths": depths,
                        "proposals": proposals, "routes": routes, "truncated": truncated})
    return res


def status() -> dict[str, Any]:
    reg = _load_registry()
    return {"ok": True, "schema": SCHEMA,
            "contract": "percolate(text) -> noise file + invariant(repeat) / explore(novel); "
                        "percolate_signal(text) for training-signal detection + false positives",
            "n_invariants": len(reg.get("invariants") or {}),
            "false_positives": reg.get("false_positives", 0),
            "count_laws": {"half_life_days": _cfg()["half_life_days"],
                           "cycle": _cfg()["cycle"],
                           "self_emission_cap": _cfg()["self_emission_cap"]},
            "noise_dir": str(NOISE_DIR.relative_to(ROOT)).replace("\\", "/"),
            "intake": str((INTAKE_DIR / "register.jsonl").relative_to(ROOT)).replace("\\", "/"),
            "candidates_review": str(CANDIDATES_REVIEW.relative_to(ROOT)).replace("\\", "/"),
            "cascade_queue": str(CASCADE_QUEUE.relative_to(ROOT)).replace("\\", "/"),
            "cascades_ledger": str(CASCADES_LEDGER.relative_to(ROOT)).replace("\\", "/"),
            "cost": "deterministic + $0 (stdlib only)"}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="percolator")
    ap.add_argument("text", nargs="?", help="raw signal to percolate")
    ap.add_argument("--source", default="manual")
    ap.add_argument("--domain", default="general")
    ap.add_argument("--noise-log", action="store_true")
    ap.add_argument("--intake", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--maintenance", action="store_true",
                    help="Z15 backfill: self-emission cap + half-life decay on stored counts")
    ap.add_argument("--dry", action="store_true",
                    help="with --maintenance or --cascade: report only, no write")
    ap.add_argument("--apply", action="store_true",
                    help="with --maintenance or --mine-depends-on: write the repair/backfill")
    ap.add_argument("--candidates", nargs="+", metavar="PATH_OR_GLOB",
                    help="ingest mine percolator_candidates.jsonl rows into the review pass "
                         "(memory/percolator/candidates.jsonl) as candidates, NEVER auto-promoted "
                         "(the promote gate stays alpha-budget); globs expand, e.g. "
                         "watch/inbox/frontier_olm_*/percolator_candidates.jsonl")
    ap.add_argument("--cascade", metavar="KEY",
                    help="fire the invariant cascade from KEY over reverse depends_on edges "
                         "(CP-1 port); proposals land in memory/percolator/cascade_queue.jsonl "
                         "(status pending) and the receipt in memory/percolator/cascades.jsonl; "
                         "invariants.json is NEVER edited; use --dry for compute-only")
    ap.add_argument("--change-kind", default=None,
                    help="with --cascade: change kind (removed/superseded/expired escalate; "
                         "anything else refresh-proposes)")
    ap.add_argument("--old", default=None, help="with --cascade: old value for the change record")
    ap.add_argument("--new", default=None, help="with --cascade: new value for the change record")
    ap.add_argument("--mine-depends-on", action="store_true",
                    help="mine invariant-to-invariant dependency edges (16-hex hash citations "
                         "+ substring derivations) and report; with --apply, back up the "
                         "registry and add the depends_on key to every row (additive only)")
    a = ap.parse_args()
    if a.status:
        print(json.dumps(status(), indent=2, default=str))
    elif a.maintenance:
        if a.dry and a.apply:
            ap.error("--dry and --apply are mutually exclusive")
        print(json.dumps(maintenance(dry=not a.apply), indent=2, default=str))
    elif a.cascade:
        chg: dict[str, Any] = {}
        if a.change_kind:
            chg["kind"] = a.change_kind
        if a.old is not None:
            chg["old"] = int(a.old) if str(a.old).lstrip("-").isdigit() else a.old
        if a.new is not None:
            chg["new"] = int(a.new) if str(a.new).lstrip("-").isdigit() else a.new
        print(json.dumps(cascade(a.cascade, change=chg or None, write=not a.dry),
                         indent=2, default=str))
    elif a.mine_depends_on:
        print(json.dumps(mine_depends_on(apply=a.apply), indent=2, default=str))
    elif a.candidates:
        print(json.dumps(ingest_candidates(a.candidates), indent=2, default=str))
    elif a.noise_log:
        print(json.dumps(noise_log(a.domain), indent=2, default=str))
    elif a.intake:
        print(json.dumps(open_intake(), indent=2, default=str))
    elif a.text:
        print(json.dumps(percolate(a.text, source=a.source, domain=a.domain), indent=2, default=str))
