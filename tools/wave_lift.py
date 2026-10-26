"""WAVE LIFT — the estate's own 50-wide executor. Hardy by design.

Operator law, 2026-09-22: width must not live inside any harness. ZCode updates
cannot break what lives in the estate. This bridge seeds N lanes into the mag
orchestrator queue across MULTIPLE providers (the estate's clarke_wave ran
ds40+glm20 concurrently — multi-provider means no single rate limit strangles
the wave), watches them with Mickey-17 semantics (a failed lane is re-seeded,
K attempts, then tombstoned — never silently carried), and lands receipts in a
durable write root (watch/inbox/wave_lift_<stamp>/, per the fifty_wide board
law). Findings JSON at the end feeds tools/kv50_smith_chart.py directly.

Usage (repo root):
  .venv/Scripts/python.exe tools/wave_lift.py --spec lanes.json --tag kv50
  lanes.json = [{"id": "...", "prompt": "...", "provider": "deepseek|grok|glm|ollama"(optional)}]
  --wide N        seed at most N lanes (default: all in spec)
  --attempts K    re-seeds per lane before tombstone (default 2)
  --deadline S    max seconds to wait (default 5400)
  --rotate        round-robin providers across lanes (default: deepseek,grok,glm,ollama)

Update-hardy contract: depends only on mag.orchestrator (queue + drainer) and
files. No ZCode internals. Any harness, any version, any seat can drive it.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROVIDER_CYCLE = ["deepseek", "grok", "glm", "ollama", "mimo"]  # mimo: free-window surge hull (ends ~09-28), per MIMO_FREE_WINDOW_20260922.md
TERMINAL = {"done", "failed", "killed", "timeout", "died"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    ap = argparse.ArgumentParser(prog="wave-lift")
    ap.add_argument("--spec", help="JSON file: [{'id','prompt','provider'?}]")
    ap.add_argument("--resume-root", help="existing wave_lift root name: re-watch its original seeds, no new enqueues")
    ap.add_argument("--wide", type=int, default=0)
    ap.add_argument("--attempts", type=int, default=2)
    ap.add_argument("--deadline", type=int, default=5400)
    ap.add_argument("--tag", default="wave-lift")
    args = ap.parse_args()

    from mag import orchestrator as orch

    index = ROOT / "watch" / "inbox" / "index_events.jsonl"
    lanes = []
    prompt_map = {}
    if args.resume_root:
        if args.spec:
            _spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
            _ls = _spec.get("lanes") if isinstance(_spec, dict) else _spec
            prompt_map = {l["id"]: l for l in (_ls or [])}
        root = ROOT / "watch" / "inbox" / args.resume_root
        state = {}
        qids = {}
        seeds = json.loads((root / "00_seeds.json").read_text(encoding="utf-8"))["lanes"]
        for lid, s in seeds.items():
            s["status"] = "queued"
            s["attempts"] = 1
            state[lid] = s
            if s.get("queue_id"):
                qids[lid] = s["queue_id"]
        print(f"[wave] resume {args.resume_root}: re-watching {len(state)} original seeds (no new enqueues)")
    else:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        # accept either a bare lane array or an object wrapping one ({tag, doctrine, lanes})
        lanes = spec.get("lanes") if isinstance(spec, dict) else spec
        lanes = lanes or []
        if args.wide:
            lanes = lanes[: args.wide]
        if not lanes:
            print("[wave] empty spec")
            return 2
        root = ROOT / "watch" / "inbox" / f"wave_lift_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        root.mkdir(parents=True, exist_ok=True)

    def seal(name: str, payload: dict) -> None:
        import hashlib

        p = root / name
        p.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        sha = hashlib.sha256(p.read_bytes()).hexdigest().upper()
        line = json.dumps(
            {
                "seq": int(datetime.now(timezone.utc).timestamp() * 1e6),
                "ts": now(),
                "op": "register",
                "file": f"/board/inbox/wave_lift_{root.name.split('_', 2)[2]}/{name}",
                "sha256": sha,
                "class": "RECEIPT",
                "purpose": f"wave lift {args.tag}: {name}",
            },
            ensure_ascii=False,
        )
        with index.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    if not args.resume_root:
        # fresh wave: reset state; resume mode already loaded it above
        state: dict[str, dict] = {}
        qids: dict[str, str] = {}
    cycle = PROVIDER_CYCLE.copy()

    if args.resume_root:
        # resume path already loaded state/qids; nothing to seed
        seal("live_status.json", {"checked_at": now(), "resumed": True, "lanes": state})
    else:
        # --- seed (Mickey 17: every lane is expendable and replaceable) ---
        for i, lane in enumerate(lanes):
            lid = lane.get("id") or f"lane-{i}"
            provider = lane.get("provider") or cycle[i % len(cycle)]
            goal = f"[wave:{args.tag}:{lid}] {lane.get('prompt', '').strip()}"
            r = orch.enqueue(goal, provider=provider, tag=f"{args.tag}:{lid}", priority=1)
            state[lid] = {"lane": lid, "provider": provider, "attempts": 1, "status": "queued", "queue_id": r.get("queue_id"), "error": r.get("error")}
            if r.get("queue_id"):
                qids[lid] = r["queue_id"]
        seal("00_seeds.json", {"tag": args.tag, "seeded_at": now(), "lanes": state})
        print(f"[wave] seeded {len(state)} lanes under tag '{args.tag}' -> {root.name}")

    # --- watch + re-seed (the wave breathes across providers) ---
    # Mickey-17 correction, dash25 wave: a queue entry MISSING from a listing is not
    # a dead lane — listings truncate and entries age out. Only explicit terminal
    # failure statuses re-seed; missing status just waits, and a lane is only
    # tombstoned when the listing has missed it 30 consecutive polls.
    deadline = time.time() + args.deadline
    misses = {lid: 0 for lid in state}
    while time.time() < deadline:
        time.sleep(20)
        queue = orch.list_queue(limit=500)
        byqid = {q.get("queue_id"): q for q in queue}
        pending = False
        for lid, st in state.items():
            if st["status"] in TERMINAL:
                continue
            q = byqid.get(qids.get(lid, ""))
            status = (q or {}).get("status")
            if status is None:
                misses[lid] = misses.get(lid, 0) + 1
                if misses[lid] > 30:
                    st["status"] = "tombstoned:missing"
                    print(f"[wave] {lid}: tombstoned after {misses[lid]} missed listings")
                else:
                    pending = True
                continue
            misses[lid] = 0
            if status in ("queued", "running"):
                pending = True
                st["status"] = status
                continue
            if status in ("done",):
                st["status"] = "done"
                st["detail"] = str((q or {}).get("detail", ""))[:2000]
                continue
            if status in ("failed", "timeout", "killed", "died"):
                src = prompt_map.get(lid) or (dict((l["id"], l) for l in lanes).get(lid) if lanes else None)
                if src is None:
                    st["status"] = "tombstoned:no-prompt"
                    print(f"[wave] {lid}: tombstoned (resume mode has no prompt to re-seed)")
                    continue
                if st["attempts"] < args.attempts:
                    provider = cycle[(cycle.index(st["provider"]) + 1) % len(cycle)]
                    goal = f"[wave:{args.tag}:{lid}:r{st['attempts'] + 1}] {src['prompt'].strip()}"
                    r = orch.enqueue(goal, provider=provider, tag=f"{args.tag}:{lid}", priority=1)
                    st["attempts"] += 1
                    st["provider"] = provider
                    st["status"] = "queued"
                    st["queue_id"] = r.get("queue_id")
                    if r.get("queue_id"):
                        qids[lid] = r["queue_id"]
                    pending = True
                    print(f"[wave] {lid}: {status} -> re-seeded on {provider} (attempt {st['attempts']})")
                else:
                    st["status"] = f"tombstoned:{status}"
                    st["detail"] = str((q or {}).get("detail", ""))[:500]
                    print(f"[wave] {lid}: tombstoned after {st['attempts']} attempts")
        seal("live_status.json", {"checked_at": now(), "lanes": state})
        if not pending:
            break

    # --- land the findings ---
    done = [l for l, s in state.items() if s["status"] == "done"]
    seal("99_final.json", {"finished_at": now(), "done": len(done), "lanes": state})
    findings = [
        {"lane": l, "finding": state[l].get("detail", ""), "sources": [], "evidence": state[l].get("detail", "")[:200], "steal_action": "", "confidence": "medium", "converges_with": ""}
        for l in state
        if state[l]["status"] == "done"
    ]
    fj = ROOT / f"wave_findings_{args.tag}.json"
    fj.write_text(json.dumps(findings, indent=2), encoding="utf-8")
    print(f"[wave] done={len(done)}/{len(state)} · findings: {fj.name} (pipe into tools/kv50_smith_chart.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
