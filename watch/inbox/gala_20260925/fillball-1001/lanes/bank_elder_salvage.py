"""Bank the elder-lens salvage row + trail row (fill-elder-salvage, gala fillball-1001).

The falsifier organ per the card's own terms is queue/lanes/elder/inbox.jsonl
(watch/inbox/ractor50/skills.md section 2.2). Manifest law: inbox = compact
pointers; the lens's actionable core (pattern + question + clock) rides in the
row, the full text lives in the receipt. Write path: python json.dumps, never
heredoc.
"""
import json
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).isoformat()

inbox_row = {
    "ts": NOW,
    "from": "seat-salvage-fillball-1001",
    "kind": "lens-pointer",
    "priority": "high",
    "item": (
        "ELDER LENS salvage bank: one lens distilled from "
        "watch/inbox/48h_synth/STORY.md (the 48h-synthesis window narrative, "
        "read whole), executing the elder-lens card's own salvage clause "
        "(watch/inbox/ractor50/skills.md section 2.2) inside its ~10-02 "
        "falsifier clock; card resurrects by its own terms."
    ),
    "pattern": (
        "Every win in the 48h window converted a one-shot into a cadence "
        "(standing drain verb, perishable suite green, tapestry bake, daily "
        "mine cron with slug law, 24x7 burn churn, fail-closed gate) and every "
        "corpse died of having no live loop (untracked fold overwritten, "
        "Roblox venue question never asked, compaction never fired); meanwhile "
        "the estate's oldest cadence (this lane's noon cycle) spent 12 days "
        "firing daily into honest 429 death rows (surface.md 09-20..10-01, "
        "runner_state last_result lane-down) and nothing answered until an "
        "outside register's clock forced this salvage. A cadence that files "
        "its own death is still a cadence: the cadence layer has no liveness "
        "meter and no answerer-obligation."
    ),
    "question": (
        "What evidence would show, for every cadence the estate runs (tapestry "
        "bake, mine cron, burn churn, census patrol, this inbox, every schtask), "
        "who is OBLIGED to answer its death rows, and which fresh cadences "
        "would survive that audit?"
    ),
    "falsifier": (
        "A lens is dead if no organ acts on its question within one week: "
        "clock started at banking, closes 2026-10-09T04:05:56Z; the question "
        "ledger answer-rate (watch/inbox/SELF_STEAL_DEEP_20260918.md) is the "
        "meter."
    ),
    "purpose": (
        "Give the elder lane its first live intake since Sep 4 and put the "
        "cadence-answerability question where an organ can act on it before "
        "the one-week clock closes."
    ),
    "card": "watch/inbox/fillball/elder-salvage.md",
    "anchors": (
        "watch/inbox/48h_synth/STORY.md; watch/inbox/ractor50/skills.md:98-112; "
        "queue/lanes/elder/surface.md:293-327; queue/lanes/elder/runner_state.json"
    ),
    "ttl": "2026-10-09",
}

trail_row = {
    "ts": NOW,
    "actor": "seat-salvage-fillball-1001",
    "event": "LENS_BANKED",
    "detail": (
        "elder-lens salvage clause executed inside its ~10-02 falsifier clock: "
        "one lens distilled from watch/inbox/48h_synth/STORY.md banked to "
        "inbox.jsonl (was 0 bytes, mtime Sep 4); card intake line widened to "
        "accept gala synthesis outputs (watch/inbox/ractor50/skills.md section "
        "2.2 terms); question filed to SELF_STEAL_DEEP_20260918; new one-week "
        "question clock closes 2026-10-09T04:05:56Z"
    ),
    "artifacts": [
        "queue/lanes/elder/inbox.jsonl",
        "watch/inbox/fillball/elder-salvage.md",
        ".agents/skills/elder-lens/SKILL.md",
        "watch/inbox/SELF_STEAL_DEEP_20260918.md",
    ],
}


def append_jsonl(path: str, row: dict) -> None:
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=True) + "\n")


append_jsonl("queue/lanes/elder/inbox.jsonl", inbox_row)
append_jsonl("queue/lanes/elder/trail.jsonl", trail_row)
print("banked:", NOW)
print("inbox_bytes:", __import__("os").path.getsize("queue/lanes/elder/inbox.jsonl"))
