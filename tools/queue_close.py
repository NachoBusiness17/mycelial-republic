#!/usr/bin/env python3
r"""queue_close -- the queue-owner close verb (LINKS-328's missing drain half).

FORCED BY queue-field pass c (watch/inbox/BURN_queue-field_20260927_c.md, 2026-09-27):
the janitor roam triaged 42 of 50 rows but NOTHING in the fleet can close a row
(repo-wide grep found zero closure verbs; visor reads the index read-only), so
completed upstream work (HELP_WANTED briefs RESOLVED, scanner v3 landed) leaves
rows like Q-044/Q-045 open forever. This is that verb.

Shape note (2026-09-27): the security hook refused every variable-path receipt
join (five normalize-and-validate constructions); the landed form is therefore
STRICTER than the original design: close evidence is resolved exclusively from
the RECEIPT_BINDINGS table below, whose values are literal repo-relative paths.
A generic --receipt mode is owed to a future window that lands a hook-passing
validator; until then the verb cannot be pointed at any file not registered
here, which is the most conservative possible confinement.

Contract (exit 0/2/3):
  --id Q-XXX
    * the row id must have a RECEIPT_BINDINGS entry and that receipt must
      BYTE-EXIST on disk: no binding, no close (no close without evidence,
      the falsifier's own law);
    * the row must exist and be open (closing a superseded/closed row refuses);
    * the rewrite happens under the single-writer lockfile queue/queue_index.lock
      (LedgerLock, stale-break 600s), temp-then-replace, json.dumps canonical rows;
      never a hand edit;
    * the closed row keeps every original field and gains: status="closed",
      closed_ts, closed_by, close_receipt, close_note.
  Exit 0 closed; 2 refused (unbound id, missing receipt, missing row, or row
  not open); 3 lock held fresh.

Pre-registered falsifier (pass c, verbatim intent): within one janitor cycle
Q-044, Q-045, Q-029 flip to closed on already-existing receipts with zero new
work; closed-row count >= 3; every closed row's receipt byte-exists.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "queue" / "queue_index.jsonl"
LOCK = REPO / "queue" / "queue_index.lock"

# Close evidence registry: row id -> literal repo-relative receipt path.
# Adding an entry is an Edit to this table (hook-scanned); nothing runtime
# can introduce or alter a receipt path.
RECEIPT_BINDINGS: dict[str, str] = {
    "Q-044": "memory/frontier/help_wanted/resolved/research_A.md",
    "Q-045": "memory/frontier/help_wanted/resolved/research_B.md",
    "Q-029": "watch/inbox/CORPUS_MAP_SALON_20260918.md",
    "Q-046": "watch/inbox/HELPWANTED_C_VERDICT_20260926.md",
    "Q-030": "watch/inbox/burn_wave_20260926/B2_102_fts5_wiring_20260926.md",
    # Z9 queue sweep 2026-09-29/30 (watch/inbox/hydrology/Z9_QUEUE_SWEEP.md):
    # the 09-28 burn_reset fan-out executed most rows but nothing flipped
    # the index; these bindings let the verb drain them on the receipts.
    "Q-001": "watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md",
    "Q-002": "watch/inbox/burn_reset_20260927/queue/Q-002.md",
    "Q-003": "watch/inbox/burn_reset_20260927/queue/Q-003.md",
    "Q-007": "watch/inbox/burn_reset_20260927/queue/Q-007.md",
    "Q-008": "watch/inbox/burn_reset_20260927/queue/Q-008.md",
    "Q-009": "watch/inbox/burn_reset_20260927/queue/Q-009.md",
    "Q-010": "watch/inbox/burn_reset_20260927/queue/Q-010.md",
    "Q-011": "watch/inbox/burn_reset_20260927/queue/Q-011.md",
    "Q-020": "watch/inbox/burn_reset_20260927/queue/Q-020.md",
    "Q-021": "watch/inbox/burn_reset_20260927/queue/Q-021.md",
    "Q-022": "watch/inbox/burn_reset_20260927/queue/Q-022.md",
    "Q-023": "watch/inbox/burn_reset_20260927/queue/Q-023.md",
    "Q-024": "watch/inbox/burn_reset_20260927/queue/Q-024.md",
    "Q-026": "watch/inbox/burn_reset_20260927/queue/Q-026.md",
    "Q-027": "watch/inbox/burn_reset_20260927/queue/Q-027.md",
    "Q-028": "watch/inbox/burn_reset_20260927/queue/Q-028.md",
    "Q-031": "watch/inbox/burn_reset_20260927/queue/Q-031.md",
    "Q-032": "watch/inbox/ROBLOX_LANE_DEATH_20260929.md",
    "Q-033": "watch/inbox/burn_reset_20260927/queue/Q-033.md",
    "Q-034": "watch/inbox/burn_reset_20260927/queue/Q-034.md",
    "Q-035": "configs/mirrors.json",
    "Q-036": "watch/inbox/burn_reset_20260927/queue/Q-036.md",
    "Q-037": "watch/inbox/ROBLOX_LANE_DEATH_20260929.md",
    "Q-038": "watch/inbox/ROBLOX_LANE_DEATH_20260929.md",
    "Q-039": "watch/inbox/ROBLOX_LANE_DEATH_20260929.md",
    "Q-040": "watch/inbox/ROBLOX_LANE_DEATH_20260929.md",
    "Q-041": "watch/inbox/burn_reset_20260927/queue/Q-041.md",
    "Q-042": "watch/inbox/ROBLOX_LANE_DEATH_20260929.md",
    "Q-043": "watch/inbox/burn_reset_20260927/queue/Q-043.md",
    "Q-048": "watch/inbox/burn_reset_20260927/queue/Q-048.md",
    "Q-049": "watch/inbox/burn_reset_20260927/queue/Q-050.md",
    "Q-050": "watch/inbox/burn_reset_20260927/queue/Q-050.md",
    # queue-truth lane 2026-10-04 (mickey17_v2 GO item 7, a14 row a14-queue-truth#0):
    # the WO-12 flip sweep (watch/inbox/wave5_repair/queue-closes.md) verified both
    # receipts by dir-listing and flipped the todo boxes on 2026-09-29 but never
    # appended here (grep 'Q-005|Q-025' in that file = 0 hits, checked 2026-10-04),
    # so todo and index disagreed since 2026-09-29. Bindings let the verb drain
    # them on the receipts; the todo citation paths queue/Q-005.md and
    # queue/Q-025.md were dead (no such file) and were fixed same lane.
    "Q-005": "watch/inbox/burn_reset_20260927/queue/Q-005.md",
    "Q-025": "watch/inbox/burn_reset_20260927/queue/Q-025.md",
}

RECEIPT_NOTES: dict[str, str] = {
    "Q-044": "upstream RESOLVED by gopher t13a 2026-09-26; drop-candidate pointer closed on the resolved artifact",
    "Q-045": "upstream RESOLVED by gopher t13b 2026-09-26; queue-owner close on the resolved artifact",
    "Q-029": "scanner v3 landed by other hands (inline v3 walk 2026-09-18, mag/catalog_scan.py v3 per B2-76, catalog rebuilt 489,548 rows per B2-186); closed on the salon receipt",
    "Q-046": "brief 3 RESOLVED 2026-09-26 by gopher t13c (stack row found+pruned, no pipe record confirmed twice); closed on the verdict receipt (triage 2026-09-27)",
    "Q-030": "FTS5 decision made and WIRED 2026-09-26 (B2-102: catalog_fts.sqlite live, 4.5s->2.5ms); freshness budget landed as the B2-465 daily rebuild task; closed on the wiring receipt (triage 2026-09-27)",
    # Z9 sweep notes (2026-09-29/30): each names instrument + moment + evidence.
    "Q-001": "STALE-superseded: compaction PARKED by funded elder consult 2026-09-29 (watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md) with 4 named re-raise conditions; commit 4b77c3d01 records the operator ruling that the Q-001 operator-GO ask DISSOLVES into the parking; plan-only half already banked by burn_reset Q-001 receipt (247 folded / 790 kept at plan time)",
    "Q-002": "DONE by burn_reset 2026-09-28 receipt: tools/auto_promote.py + tests/test_auto_promote.py landed, wired into mag/improve.py, configs/improve.yaml promote.auto block; byte-verified this sweep (files exist)",
    "Q-003": "DONE by burn_reset 2026-09-28 receipt: tools/session_cards.py built, human-session cards generated; byte-verified this sweep (14 .card.json in memory/biography/cards/, mtime 2026-09-28)",
    "Q-007": "DONE by burn_reset 2026-09-28 receipt: 11 new chord/refusal/rope rows anchor-verified and banked as Q_007_rows.jsonl (validator included); residual sister-repo append to mycelial-republic mirror_train.jsonl spawned in Z9_QUEUE_SWEEP.md (outside this repo's write roots)",
    "Q-008": "DONE by burn_reset 2026-09-28 receipt: spider _check_fkb_repeat root-caused (double flat count bar + [:5] rank slice, severity ignored), thresholds fixed with test_spider_detects_fkb_repeat; severity tiers byte-verified in mag/spider.py this sweep",
    "Q-009": "DONE by burn_reset 2026-09-28 receipt: comms_trail consumption_signal wired into every router branch (_comms_lane_boost, heavy + remote), stale retirement line in mag/cleanup_steal.py named; byte-verified in mag/router.py this sweep",
    "Q-010": "DONE by burn_reset 2026-09-28 receipt + commit a30976c4b: tools/derived_dag.py landed read-only over all four hash families; index byte-verified this sweep (memory/derived/derived_dag_index.json, 30.7MB, 2026-09-28)",
    "Q-011": "DONE by burn_reset 2026-09-28 receipt: huang.v1 gate landed in mag/frontier_salon.py (why + single-seat baseline required pre-dispatch, shaped refusal, audit echo, CLI split); byte-verified this sweep",
    "Q-020": "DONE by burn_reset 2026-09-28 receipts: all five FW-01..05 legs receipted (202/202 harness trio after two re-lands, referee chain 28 passed of 81-family, grounding row-122 verify, VOID executed by operator cross-sign 2026-09-27, sampler closure receipt); per-leg receipts alongside",
    "Q-021": "DONE by burn_reset 2026-09-28 receipt: all nine FW-06..14 census-debt items executed with per-item receipts",
    "Q-022": "DONE by burn_reset 2026-09-28 receipt: all four FW-15..18 tide items executed (amendment row, gemma leg repair, dashboard surface, 3-strike clock; note: operator model later minted TWO-STRIKE bail law, 4f3030294); honest gaps declared in receipt",
    "Q-023": "DONE by burn_reset 2026-09-28 receipt: FW-19..21 patrol debt executed (event paths, fold self-heal verify, inbox validate delta)",
    "Q-024": "DONE by burn_reset 2026-09-28 receipt: all five FW-22..26 X radar steals executed with artifacts",
    "Q-026": "DONE by burn_reset 2026-09-28 receipt: FW-32..36 wave stones receipted (FW-36 stubs by design, falsifier battery correctly not authored inside a stub); out-of-scope set declared in receipt",
    "Q-027": "DONE by burn_reset 2026-09-28 receipt: all six FW-37..42 game-estate items landed with per-item artifacts (FW38..42 files alongside)",
    "Q-028": "DONE by burn_reset 2026-09-28 receipt: 6 of 8 fleet-wart items executed/landed, 2 verified already absorbed (Q-001 plan-only, Q-002 done), 1 superseded-by-tombstone with supersession banked",
    "Q-031": "DONE by burn_reset 2026-09-28 receipt: tags v2 owner column live in catalog/tags.jsonl (spec-first in mag/catalog_tags.py, byte-verified this sweep) + held-out 50-question eval executed (accuracy@1 0.48, accuracy@10 0.76, results JSON with sha-pinned catalog); mining correctly not started",
    "Q-032": "STALE-superseded: Roblox lane dead per operator 2026-09-29 (watch/inbox/ROBLOX_LANE_DEATH_20260929.md); the receipt itself cites the Q_032 flock battery 37/37 as archived code, Godot is primary",
    "Q-033": "DONE by burn_reset 2026-09-28 receipt: comparative audit executed (same prompt across free lanes with reasoning traces + drift verdict: muse-glimmer-30b first, ling-flash-vl second, honest OWED marking); $0",
    "Q-034": "DONE by burn_reset 2026-09-28 receipt: first video-input burn executed on one corpus mp4 with raw provider JSON banked; OWED section empty (none blocking)",
    "Q-035": "DONE by evidence: configs/mirrors.json carries the per-host catalog diff (groq/llm7/openrouter counts + churn flags + diff_line), written on-change by tools/stealth_driver.py _write_mirrors_if_changed on every driver cycle; byte-refreshed 2026-09-30T07:51Z this sweep window",
    "Q-036": "DONE by burn_reset 2026-09-28 receipt: LANE_EFFORT_POLICY (free=low, judgment=max, scarce5=max, unknown fails closed to low) wired into stealth-driver dispatch payloads + heartbeat observability + test_stealth_driver_effort_dial.py (byte-verified this sweep); nous passthrough live-verify declared OWED, non-blocking (config-only)",
    "Q-037": "STALE-superseded: named CLOSED by operator Roblox lane death 2026-09-29 (watch/inbox/ROBLOX_LANE_DEATH_20260929.md): chat remotes + swarm shooting + Wing Chun input were verified WIRED by burn_reset Q-037 receipt before the death; lane archived",
    "Q-038": "STALE-superseded: Studio publish moot after operator Roblox lane death 2026-09-29 (watch/inbox/ROBLOX_LANE_DEATH_20260929.md); the surviving server publish landed separately 2026-09-29 as watch/inbox/hydrology/Y5_SERVER_PUBLISH.md (server/ to the-mountain, vendored physics, never pushed)",
    "Q-039": "STALE-superseded: named CLOSED by operator Roblox lane death 2026-09-29 (watch/inbox/ROBLOX_LANE_DEATH_20260929.md); no public gateway host owed for a dead lane",
    "Q-040": "STALE-superseded: named CLOSED by operator Roblox lane death 2026-09-29 (watch/inbox/ROBLOX_LANE_DEATH_20260929.md); v1.1 polish (FOV kick, cooldown chips, mobile bindings) had already landed via burn_reset Q-040 receipt; lane archived",
    "Q-041": "DONE by burn_reset 2026-09-28 receipt (leaderstats page landed, committed place kept fresh) and mooted-and-archived with the Roblox lane death 2026-09-29; work executed before the death",
    "Q-042": "STALE-superseded: named CLOSED by operator Roblox lane death 2026-09-29 (watch/inbox/ROBLOX_LANE_DEATH_20260929.md); pet orb had already landed via burn_reset Q-042 receipt (luau-lsp clean, rojo build, byte checks); lane archived",
    "Q-043": "DONE by burn_reset 2026-09-28 receipt: all three games-polish items landed (GnomeCode SectionStream.luau streamed sections, Trove loop ownership, cooldown chips; sectionstream battery 12/12); Roblox lane archived 2026-09-29 with the code kept",
    "Q-048": "DONE by burn_reset 2026-09-28 receipt: quantized lattice fold design doc banked (ghost_memlance schema + thought_quantizer + state_quantizer read in full, read-side proof via context_pack._quantized_laws, staleness check armed); design ask, no code owed",
    "Q-049": "STALE-consumed: vacuous telemetry row (roam verdict: not work, keep as signal); the signal was consumed by the Q-050 audit which ruled route=ledger-artifact (keep demoted, September slice straddles the bar) and audit=starved; closed on the audit receipt",
    "Q-050": "DONE by burn_reset 2026-09-28 receipt: all 3 task_ids byte-verified in cost_ledger (all actual.calls 0, agent_churn, purged 2026-08-10), one-word verdicts banked (audit: starved; route: ledger-artifact); HELP_WANTED brief 7 closed by memory/frontier/analysis/audit_gap_diagnosis.md (byte-verified this sweep)",
    # queue-truth lane notes 2026-10-04 (mickey17_v2 GO item 7): each names the
    # cause of the index/todo disagreement and the evidence it was closed on.
    "Q-005": "DONE by burn_reset 2026-09-28 receipt: 127 attention.md pings triaged (every one the shape 'Session record ready (first)'), writer named at mag/biography.py:509-515; habit line NOT re-seeded (operator ruling on the ritual not given); todo box flipped 2026-09-29 WO-12 but that flip sweep never appended to this index (grep 'Q-005' in watch/inbox/wave5_repair/queue-closes.md = 0 hits), so todo and index disagreed since 2026-09-29; closed by queue-truth-a14 mickey17_v2 GO item 7",
    "Q-025": "DONE by burn_reset 2026-09-28 receipt: all five FW-27..31 operator gate packets executed as packets (FW27_publish_manifest.md, FW28_blind_hour.md, FW29_cube_assembly.md, FW30_discord_runbook.md, FW31_sep20_demo.md under watch/inbox/fifty_wide_20260917/, all five byte-exist 2026-10-04); todo box flipped 2026-09-29 WO-12 but that flip sweep never appended to this index (grep 'Q-025' in watch/inbox/wave5_repair/queue-closes.md = 0 hits), so todo and index disagreed since 2026-09-29; closed by queue-truth-a14 mickey17_v2 GO item 7",
}

sys.path.insert(0, str(REPO))
from tools.ledger_lock import LedgerLock, LockHeldError  # noqa: E402


def _now_z() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def close_row(row_id: str, by: str) -> int:
    receipt_rel = RECEIPT_BINDINGS.get(row_id)
    if receipt_rel is None:
        bound = ", ".join(sorted(RECEIPT_BINDINGS))
        print(f"REFUSE no receipt binding for {row_id} (bound: {bound})",
              file=sys.stderr)
        return 2
    receipt_path = REPO.joinpath(*receipt_rel.split("/"))
    if not receipt_path.is_file():
        print(f"REFUSE bound receipt does not byte-exist: {receipt_path}",
              file=sys.stderr)
        return 2

    rows: list[dict] = []
    target: dict | None = None
    with INDEX.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if str(r.get("id")) == row_id:
                target = r
            rows.append(r)
    if target is None:
        print(f"REFUSE no such row id: {row_id}", file=sys.stderr)
        return 2
    if target.get("status") != "open":
        print(f"REFUSE row {row_id} status is {target.get('status')!r}, not open",
              file=sys.stderr)
        return 2

    target["status"] = "closed"
    target["closed_ts"] = _now_z()
    target["closed_by"] = by
    target["close_receipt"] = receipt_rel
    note = RECEIPT_NOTES.get(row_id)
    if note:
        target["close_note"] = note

    lock = LedgerLock(str(LOCK))
    try:
        lock.acquire()
    except LockHeldError as e:
        print(f"REFUSE lock held: {e}", file=sys.stderr)
        return 3
    try:
        tmp = str(INDEX) + ".close.tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, str(INDEX))
    finally:
        lock.release()
    print(f"OK closed {row_id} on receipt {target['close_receipt']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="queue_close",
        description="queue-owner close verb (receipt-bindings-gated)")
    ap.add_argument("--id", required=True,
                    help="row id with a RECEIPT_BINDINGS entry, e.g. Q-044")
    ap.add_argument("--by", default="queue-owner",
                    help="who closes (default: queue-owner)")
    args = ap.parse_args(argv)
    return close_row(args.id, args.by)


if __name__ == "__main__":
    sys.exit(main())
