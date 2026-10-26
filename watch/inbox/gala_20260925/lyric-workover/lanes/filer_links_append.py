# estate-filer: append tonight's GALA lyric-workover LINKS rows to memory/corpus/LINKS.jsonl
# law: sequential single-writer append only; dedupe by src against existing rows first;
#      whole-ledger re-parse after append; ASCII only, no em/en dashes (ensure_ascii=True).
import collections
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
LINKS = ROOT / "memory/corpus/LINKS.jsonl"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ROWS = [
    {
        "ts": TS,
        "id": "GALA-lyric-workover-archaeology",
        "kind": "gala",
        "slug": "lyric-workover",
        "src": "watch/inbox/gala_20260925/lyric-workover/lanes/archaeology.json",
        "author": "gala lane archaeology (lyric-workover, division B)",
        "title": "repetition-is-the-content law",
        "load_bearing": [
            "repetition-is-the-content law: The canon's hooks repeat 30-144x and sing about repetition itself, so the rewrite must mark which of its 14 lines are the loop rather than writing 14 through-composed lines.",
            "one-word-mutation reversal law: The canon never announces a turn: its reversals are a single swapped word inside an otherwise identical repeated line (feel/look in Over And Over, would/wouldn't in Heartbeats).",
            "objects-carry-stakes law: Stakes are never named as emotions: grief is a phone call and coffee, doom is a car and a bottle, obsession is a burning home; each beat gets one object staged flat.",
            "count-as-clock law: The canon measures time by counting, never by explaining: one-two-three-four, ten days, hour after hour, one more time.",
            "loop-ready exit-line law: Exit lines are 1-4 words and are placed where the loop restarts, so the ending is a beginning (go slow; work is never over; Downtown).",
            "never-explains law: Across 24 fetched lyric sheets, zero tracks state a thesis in the hook, resolve the plot, or name abstract emotions; the form shows a feeling and makes you do it.",
            "density-band law: The canon holds one story beat per 3.5-4 unique lines (Heartbeats: 4 beats in ~16 unique lines; Someone Great: the call beat in 8), so the riddle's 4 beats in 14 lines is inside the band and the form can hold the thriller minus its connective tissue.",
        ],
        "decision_changed": "lyric-workover rewrite form: the 14-line riddle rewrite must obey the canon's measured grammar (I/you present tense, 4-8 word single-clause lines, hook as instruction or count at 1-4 words per line, reversal delivered as ONE mutated word inside an otherwise identical repeated line, exit line 1-4 words and loop-ready, clock and stakes staged as objects never stated, one beat per 3.5-4 lines, no thesis anywhere) instead of prose-thriller conventions",
        "lane": "gala-20260925/lyric-workover/B",
        "note": "24 Genius lyric pages fetched live (22 in-folder canon tracks + 2 ask-named tracks verified absent from the folder); grammar + compression study watch/inbox/music/lyric-archaeology.md; honest gaps carried in the lane JSON: the operator's 14-line riddle text was NOT found on disk (searched watch/inbox, memory, state, queue, all gala folders), so the study measures against the ask's own riddle spec; Phoenix not in the folder's 51-artist taxonomy and 'dance with trouble' unresolvable to any track; no code under mag/ or tools/ touched so the violation ratchet was not run (not owed); check archaeology_check.py exit 0, FAILURES 0 (lanes/archaeology.check.txt)",
    },
    {
        "ts": TS,
        "id": "GALA-lyric-workover-jung",
        "kind": "gala",
        "slug": "lyric-workover",
        "src": "watch/inbox/gala_20260925/lyric-workover/lanes/jung.json",
        "author": "gala lane jung (lyric-workover, division B)",
        "title": "the 6 cutter packs' LYRICS blocks superseded by the archetype-workover rewrites; the doctrine-as-liturgy lyric approach is ruled out: doctrine enters songs as symbol only",
        "load_bearing": [
            "all 6 cutter cuts rewritten as ~3:00 archetype thrillers (Persona, Hero, Trickster, Shadow, each with its shadow) in the operator's riddle structure, doctrine as symbol only",
            "Suno paste rule: source style string + the archetype-workover lyric sheet, style strings and DNA numbers unchanged",
            "81/81 byte checks pass (lanes/jung.check.txt, PYEXIT=0)",
        ],
        "decision_changed": "The 6 cutter packs keep their style strings, DNA numbers, and triangulations; their LYRICS blocks are superseded by the archetype-workover rewrites (Suno paste: source style string + this file's lyric sheet, ~3:00 render target). The doctrine-as-liturgy lyric approach is ruled out: doctrine enters songs as symbol only.",
        "lane": "gala-20260925/lyric-workover/B",
        "note": "rows empty per division B (decision-change lane); artifact watch/inbox/gala_20260925/lyric-workover/archetype-workover.md; style strings and DNA unchanged; checks: check_jung.py exit 0, 81 PASS (lanes/jung.check.txt)",
    },
    {
        "ts": TS,
        "id": "GALA-lyric-workover-bernays",
        "kind": "gala",
        "slug": "lyric-workover",
        "src": "watch/inbox/gala_20260925/lyric-workover/lanes/bernays.json",
        "author": "gala lane bernays (lyric-workover, division B)",
        "title": "render supersession: the dialogue-hook sheets in bernays-workover.md are the paste-ready lyrics for any Suno render of the six music-ractor packs, superseding the opinion-hook LYRICS blocks (style strings, BPM targets, DNA numbers and the ffprobe acceptance gate unchanged)",
        "load_bearing": [
            "every hook is now two-line dialogue (handoff or refusal: play the tape / it was / nice copy / same fire / since you last asked / I'm keeping it)",
            "verses are ticking clocks, every noun is an object with stakes, system words banished from all lyric blocks (byte-checked, ban-scan exit 1 = no match)",
            "each cut carries the engineered want + crowd reaction; style strings and DNA left with the source packs",
        ],
        "decision_changed": "Render supersession: for the six music-ractor packs (TRUST BYTES, GREEN IS A MOMENT, THE SMIRK KEY, ONE BUG MANY JACKETS, GREEN IS PERISHABLE, THE CASINO), the paste-ready lyrics for any Suno render are now the dialogue-hook sheets in bernays-workover.md, superseding the opinion-hook LYRICS blocks in watch/inbox/music/cutter-disco_cuts.md and cutter-electro_cuts.md; style strings, BPM targets, DNA numbers and the ffprobe acceptance gate are unchanged.",
        "lane": "gala-20260925/lyric-workover/B",
        "note": "rows empty per division B (decision-change lane); receipt watch/inbox/gala_20260925/lyric-workover/lanes/bernays-workover.md 22387 bytes verified on disk at filing; checks: finish-line byte battery exit 0 + json.tool parse ok (lanes/bernays.check.txt); violation_ratchet NOT RUN and not owed (no code under mag/ or tools/ touched, watch/inbox records only)",
    },
]

# validation: ASCII only, no em/en dashes anywhere in the filed text
for r in ROWS:
    fields = [r["id"], r["kind"], r["slug"], r["src"], r["author"], r["title"],
              r["decision_changed"], r["lane"], r["note"]] + r["load_bearing"]
    for v in fields:
        v.encode("ascii")  # raises UnicodeEncodeError on any non-ascii byte
        assert "\u2013" not in v and "\u2014" not in v, f"dash law hit in {r['id']}"

# dedupe by src and id against existing rows, whole-ledger parse baseline
raw = LINKS.read_text(encoding="utf-8")
lines = [l for l in raw.splitlines() if l.strip()]
assert len(lines) == 231, f"pre-append ledger line count {len(lines)} != 231"
ledger = [json.loads(l) for l in lines]
existing_srcs = {r.get("src") for r in ledger}
existing_ids = {r.get("id") for r in ledger}
for r in ROWS:
    assert r["src"] not in existing_srcs, f"dedupe hit on src: {r['src']}"
    assert r["id"] not in existing_ids, f"dedupe hit on id: {r['id']}"

# sequential single-writer append
with LINKS.open("a", encoding="utf-8", newline="\n") as f:
    for r in ROWS:
        f.write(json.dumps(r, ensure_ascii=True) + "\n")

# whole-ledger re-parse after append
lines2 = [l for l in LINKS.read_text(encoding="utf-8").splitlines() if l.strip()]
assert len(lines2) == 234, f"post-append line count {len(lines2)} != 234"
parsed = [json.loads(l) for l in lines2]
assert len(parsed) == len(lines2), "post-append parse lost a line"
# Fix (2026-10-01, this filer): the original strict assertion here was
# len(set(srcs2)) == len(srcs2) for ALL rows and failed post-append even though
# the append itself was clean: the baseline ledger already carried 60 rows with
# src=None (verified against git HEAD:memory/corpus/LINKS.jsonl at 231 lines,
# same 60 src-less rows), so global src uniqueness is not a ledger invariant.
# The house law is dedupe-by-src of the appended batch against existing rows
# (asserted above) plus batch-internal uniqueness and each appended src exactly
# once in the post-append ledger; that is what this check now enforces.
appended_srcs = [r["src"] for r in ROWS]
assert len(set(appended_srcs)) == len(appended_srcs), "appended batch has a duplicate src"
post_counts = collections.Counter(p.get("src") for p in parsed)
for s in appended_srcs:
    assert post_counts.get(s) == 1, f"appended src not exactly once after append: {s}"

print(f"OK: 3 rows appended, ledger {len(lines)} -> {len(lines2)}, whole-ledger re-parse OK, TS={TS}")
for r in ROWS:
    print("  +", r["id"], "->", r["src"])
