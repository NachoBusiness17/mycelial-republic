"""arena_gwap - the arena's play feeds the GWAP agreement engine AND the GPS router.

The operator's law (2026-10-03): the arena must be useful shit, using our
gwap - then "steal build it better". This adapter reads the run dirs the
dungeon/tavern carriers already bank (watch/inbox/playground/) and converts
EACH FIGHTER's session into its own payload:

- intent_struct (robber: the fighter): what they DECLARED, minted from the
  fighter's own pre-roll SPEECH (the "[CHECK omen]" tag), bound to the roll
  commitment they staked
- report_struct (cop: the carrier): the CONFIRMATION minted INDEPENDENTLY
  from the dice law's POST-ROLL RECORD (the ruling + roll_value the carrier
  itself holds), bound to the same commitment - never a copy of the fighter's
  triple. The two parses agree only when the law actually ruled the declared
  action family; a claimed-but-unruled action (NOROLL, no-tag RP, content
  filter, cut) mismatches and scores as disagreement. This is anti-cheat in
  the engine's own sense: a model cannot claim an action the dice did not
  rule; the carrier cannot rule an action nobody declared.
- silent cop = BLOCKED, not DISPUTE: a tavern actor with no judge ruling
  banks a payload blocked by the "copsilent" taboo (the engine's BLOCKED
  precedence), so un-judged speech stops poisoning the GPS feed as fake
  disagreement (3,802 silent rows vs 282 ruled, 2026-10-04 census).
- agreement_score = fraction of declared actions the law confirmed.
- scene_id = arena-<run>-<actor>, mapped fail-closed to that fighter's
  model_id, then fed through mag.gwap_to_gps into the GPS capability ledger:
  ROUTING DOLLARS FOLLOW MEASURED PLAY CAPABILITY. Unknown actor = skipped
  with a line, never guessed (a guessed key seeds another model's row).

Ledger: SessionLedger("arena-capability"), one session file, chain verified
before the GPS feed (the bridge re-verifies the whole file itself).

Usage:
  python tools/arena_gwap.py <run_dir>            # one session
  python tools/arena_gwap.py --backfill           # all playground run dirs
  python tools/arena_gwap.py --status             # dawn gwap line + banked_at
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from mag.gwap_payload import (  # noqa: E402
    SessionLedger,
    anon_id,
    build_payload,
    utc_now_iso,
)
from mag.gwap_to_gps import feed_session  # noqa: E402

PLAY_DIR = ROOT / "watch" / "inbox" / "playground"
GPS_LEDGER = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"
TASK_SHAPE = "arena-agreement-v1"

DUNGEON_ACTOR_MODEL = {
    "saelis": "anthropic/claude-opus-5.5",
    "grok": "anthropic/claude-fable-5.1",
    "chatgpt": "anthropic/claude-sonnet-5.5",
    "deepseek": "anthropic/claude-haiku-4.5",
    "warden": "anthropic/claude-opus-5.5",
    "dm": "anthropic/claude-opus-5.5",
    "judge": "anthropic/claude-opus-5.5",
}

# canonical action families: both sides parse to THIS vocabulary, so a
# declared attack ruled MISS still confirms (the law ruled the action); only
# family mismatches (declared [CHECK] ruled RP-no-tag, NOROLL, cut, filter)
# disagree. See GWAP_INDEPENDENT_COP_20261004.md.
_SPEECH_TAG_VERBS = (
    ("CHECK", "checked"), ("CLAIMED", "claimed"), ("AUDIT", "audited"),
    ("HIT", "attacked"), ("MISS", "attacked"), ("Ledger", "attacked"),
    ("SCENE", "ruled"), ("GATE", "ruled"),
)
_RULING_PREFIX_VERBS = (
    ("Ledger Slam", "attacked"), ("CLOCKWORK", "attacked"), ("WYRM", "attacked"),
    ("HIT", "attacked"), ("MISS", "attacked"),
    ("SUCCESS", "checked"), ("FAIL", "checked"), ("PARTIAL", "checked"),
    ("CHECK", "checked"), ("CLAIMED", "claimed"), ("AUDIT", "audited"),
    ("CUT", "cut"), ("SCENE OPEN", "ruled"), ("GATE", "ruled"),
)
_VOID_MARKERS = ("NOROLL", "content_filter", "void")


def _speech_verb(speech: str) -> str:
    """The fighter's DECLARED action family, from their own pre-roll words."""
    s = (speech or "").strip()
    if s.startswith("["):
        tag = s[1:].split()[0] if len(s) > 1 and s[1:].split() else ""
        for prefix, verb in _SPEECH_TAG_VERBS:
            if tag.lower().startswith(prefix.lower()):
                return verb
    return "spoke"  # "(dry)" or untagged: speech, not staked action


def _ruling_verb(verdict: str) -> str:
    """The law's ruling family, from the carrier's post-roll record alone."""
    v = (verdict or "").strip()
    if not v:
        return "voided"  # the law recorded nothing
    head = v.split("(")[0].strip()
    for marker in _VOID_MARKERS:
        if marker in v:
            return "voided"
    for prefix, verb in _RULING_PREFIX_VERBS:
        if head.startswith(prefix):
            return verb
    return "spoke"  # RP and unknown shapes default conservatively


def _claim(subject: str, verb: str, obj: str, qualifier: str) -> dict[str, str]:
    return {"subject": subject[:60], "verb": verb, "object": obj[:80],
            "qualifier": qualifier[:160]}


def _actor_model(run_dir: Path, actor: str) -> str | None:
    if actor in DUNGEON_ACTOR_MODEL:
        return DUNGEON_ACTOR_MODEL[actor]
    scen = run_dir / "scenario.json"
    if scen.is_file():
        try:
            sc = json.loads(scen.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        for p in sc.get("personas", []):
            if p.get("name") == actor:
                return p.get("model")
        if actor == "judge" and sc.get("judge_model"):
            return sc["judge_model"]
    return None


def _rows(run_dir: Path) -> list[dict]:
    tpath = run_dir / "transcript.jsonl"
    if not tpath.is_file():
        return []
    out = []
    for line in open(tpath, encoding="utf-8"):
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def actor_payloads(run_dir: Path) -> list[tuple[str, str, dict]]:
    """One payload per fighter: intent minted from the fighter's speech, report
    minted independently from the law's post-roll record; a silent cop banks
    BLOCKED (the copsilent taboo) instead of scoring absence as disagreement.
    D10: dungeon claims are beat-indexed (tools/arena_beats.beat_grid; both
    sides append beat/zone/hp to the commit qualifier from the SAME post-roll
    record, so the agreement arithmetic is untouched - proven byte-stable by
    tests/test_arena_beat_weld_20261005.py)."""
    from tools.arena_beats import beat_grid as _bg

    rows = _rows(run_dir)
    if not rows:
        return []
    tip = next((str(r["roll_committed"]).split(":")[0] for r in rows
                if r.get("roll_committed")), run_dir.name)
    _, beat_of = _bg(rows)
    by_actor: dict[str, list[dict]] = {}
    for r in rows:
        by_actor.setdefault(str(r.get("actor") or "unknown"), []).append(r)
    out = []
    for actor, arows in sorted(by_actor.items()):
        model = _actor_model(run_dir, actor)
        if not model:
            # tavern rows carry their own model binding (fail-closed source:
            # the row's own field, never a guess)
            model = next((str(r.get("model")) for r in arows if r.get("model")), None)
        if not model:
            print(f"UNMAPPED (skipped, fail-closed): {run_dir.name}/{actor}")
            continue
        kind = "dungeon" if run_dir.name.startswith("dnd") else "tavern"
        intent: list[dict[str, str]] = []
        report: list[dict[str, str]] = []
        taboo: list[str] = []
        silent = 0
        for r in arows:
            verdict = str(r.get("verdict") or "")
            if kind == "dungeon":
                # both sides bind the SAME commitment; the verbs come from
                # independent parses (speech vs ruling), so a fabricated
                # intent or an invented ruling cannot echo into agreement
                commit = f"commit={r.get('roll_committed')}"
                dmg = beat_of.get((actor, str(r.get("scene")), str(r.get("turn"))))
                if dmg is not None:
                    commit += f" beat={int(dmg['t'])} zone={dmg['zone']} hp={dmg['hp']}"
                scene = str(r.get("scene") or "scene")
                intent.append(_claim(actor, _speech_verb(str(r.get("speech") or "")),
                                     scene, commit))
                report.append(_claim(actor, _ruling_verb(verdict), scene, commit))
            else:
                ruled = bool(r.get("judge")) or verdict.startswith(("RUN", "BRAWL"))
                if ruled:
                    q = f"ruling={verdict[:140]}"
                    scene = str(r.get("scene") or "tavern")[:80]
                    intent.append(_claim(actor, "spoke", scene, q))
                    report.append(_claim(actor, "spoke", scene, q))
                else:
                    silent += 1
        if kind == "tavern" and not report and silent:
            # silent cop: BLOCKED by taboo (engine precedence), reason word
            # carried in the violation and the claim - never fake disagreement
            taboo = ["copsilent"]
            scene = str(arows[0].get("scene") or "tavern")[:80]
            for r in arows:
                intent.append(_claim(actor, "spoke", scene,
                                     f"silent turn={r.get('turn')}"))
            report = [_claim(actor, "blocked", scene,
                             "copsilent: no judge ruling banked this session")]
        if not intent:
            continue
        scene_id = f"arena-{run_dir.name}-{actor}"
        seed = f"{scene_id}:{tip}"
        out.append((actor, model, build_payload(
            scene_id=scene_id,
            intent_struct={"author": anon_id(seed + ":fighter"), "claims": intent},
            report_struct={"author": anon_id(seed + ":carrier"), "claims": report},
            participants=[{"anon_id": anon_id(seed + ":fighter"), "role": "robber"},
                          {"anon_id": anon_id(seed + ":carrier"), "role": "cop"}],
            consent=True,
            created_utc=utc_now_iso(),
            taboo_list=taboo,
            replay_tape_ref={
                "sha256": hashlib.sha256(
                    (run_dir / "transcript.jsonl").read_bytes()).hexdigest(),
                "engine_version": f"arena-{kind}-v4-beat",
            },
        )))
    return out


# feed-map machinery lives in tools/arena_feed.py (D10 split, 2026-10-05);
# re-exported for the existing callers' surface (tests + cron). The arena
# cadence census joined it 2026-10-10 (GAP_REGISTER R2 fill: the fold tripped
# the 400-line fence on this file, the same seam) and status() prints it.
from tools.arena_feed import (  # noqa: E402,F401
    ARENA_AUTOMATION_ID,
    _quarantined_run_dirs,
    cadence_census,
    feed_scene_map,
)


def bank(run_dir: Path, ledger: SessionLedger,
         scene_to_model: dict[str, str]) -> str:
    marker = run_dir / "GWAP_BANKED"
    if marker.is_file():
        return f"SKIP {run_dir.name}: already banked"
    payloads = actor_payloads(run_dir)
    if not payloads:
        return f"SKIP {run_dir.name}: nothing bankable"
    seqs = []
    for actor, model, payload in payloads:
        row = ledger.append(payload, ts_utc=utc_now_iso())
        scene_to_model[payload["scene_id"]] = model
        seqs.append(f"{actor}=s{row['seq']}@{payload['agreement_score']}")
    marker.write_text(";".join(seqs) + "\n", encoding="utf-8")
    return f"OK {run_dir.name}: {' '.join(seqs)}"


def status() -> str:
    """The dawn report's gwap line with the banked_at moment column.

    Cause: the a01-arena-cadence audit (2026-10-04) watched its own banking
    verdict flip NO to YES between its 03:04Z and 03:26:51Z reads while a
    backfill drained the tree under it - any row/session count without a
    moment stamp is stale on arrival (N12, moving-tree law). Evidence:
    memory/runs/mickey17_v2/runs/run-0/lanes/a01-arena-cadence.json rows 5-6;
    corpus/steal/MASTER_MICKEY17_V2.md section 9 GO item 6. banked_at is the
    earliest ledger ts_utc among a dir's own scene rows (UNBANKED dirs carry
    no rows and say so); the AS-OF line stamps the whole read.

    The cadence census rides along (GAP_REGISTER 2026-10-10 R2): the same
    read folds the arena cron's automation_runs fire rows in, so the dawn
    feed carries FAILED fires as rows, never a bare cycle count.
    """
    rows = []
    ledger = SessionLedger("arena-capability")
    if ledger.path.is_file():
        for line in open(ledger.path, encoding="utf-8"):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    banked_at: dict[str, str] = {}
    for r in rows:
        sid = str((r.get("payload") or {}).get("scene_id") or "")
        ts = str(r.get("ts_utc") or "")
        if sid and ts and (sid not in banked_at or ts < banked_at[sid]):
            banked_at[sid] = ts
    dirs = sorted(d for d in PLAY_DIR.iterdir()
                  if d.is_dir() and (d / "transcript.jsonl").is_file())
    per_dir: list[tuple[str, str]] = []
    for d in dirs:
        actors = sorted({str(r.get("actor") or "unknown") for r in _rows(d)})
        sids = [f"arena-{d.name}-{a}" for a in actors if _actor_model(d, a)]
        moments = [banked_at[s] for s in sids if s in banked_at]
        stamp = min(moments) if moments else "UNBANKED"
        per_dir.append((stamp, f"{d.name} banked_at={stamp} scenes={len(sids)}"))
    banked = sum(1 for s, _l in per_dir if s != "UNBANKED")
    per_dir.sort()
    out = [f"GWAP LEDGER AS-OF {utc_now_iso()}",
           f"ledger rows={len(rows)} distinct_scenes={len(banked_at)} "
           f"dirs={len(dirs)} banked={banked} unbanked={len(dirs) - banked}"]
    out += [f"banked_at {line}" for _s, line in per_dir]
    out += cadence_census()
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="arena_gwap")
    ap.add_argument("run_dir", nargs="?", help="a playground run dir")
    ap.add_argument("--backfill", action="store_true")
    ap.add_argument("--status", action="store_true",
                    help="print the dawn gwap line with banked_at moments")
    ap.add_argument("--beats", action="store_true",
                    help="print the run's beat-damage table (D10 instrument; "
                         "no banking, read-only) and exit")
    ap.add_argument("--no-feed", action="store_true",
                    help="bank only; skip the gwap->gps feed")
    args = ap.parse_args(argv)
    if args.status:
        print(status())
        return 0
    if args.beats:
        if not args.run_dir:
            ap.error("--beats needs a run dir")
        from tools.arena_beats import table as _beat_table

        print(_beat_table(args.run_dir))
        return 0
    if args.backfill:
        dirs = sorted(d for d in PLAY_DIR.iterdir()
                      if d.is_dir() and (d / "transcript.jsonl").is_file()
                      and (d / "DONE").is_file())
    elif args.run_dir:
        dirs = [Path(args.run_dir)]
    else:
        ap.error("need a run dir or --backfill")
    ledger = SessionLedger("arena-capability")
    scene_to_model: dict[str, str] = {}
    for d in dirs:
        print(bank(d, ledger, scene_to_model))
    ok, bad = ledger.verify_chain()
    print(f"CHAIN: verify ok={ok} bad={bad} scenes_mapped={len(scene_to_model)}")
    if scene_to_model and not args.no_feed:
        # whole-file identity map incl. quarantined dirs (see
        # _quarantined_run_dirs for the filed collision evidence)
        scene_to_model.update(feed_scene_map())
        report = feed_session(ledger.path, GPS_LEDGER,
                              task_shape=TASK_SHAPE,
                              scene_to_model=scene_to_model)
        print(f"GPS FEED: rows_seen={report['rows_seen']} fed={report['fed']} "
              f"skipped={report['skipped']} by_verdict={report['by_verdict']} "
              f"model_ids={sorted(set(report['model_ids']))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
