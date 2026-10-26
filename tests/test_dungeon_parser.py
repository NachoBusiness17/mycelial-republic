"""tests/test_dungeon_parser.py - the dice-law dungeon parser replay.

Lane a02-dungeon-campaign#0 (GO item 4, MASTER_MICKEY17_V2.md section 9):
the campaign's PARTIAL verdict was decided by a parser collapse, not by
play. strip_and_cap flattens every speech to ONE line and the old verdict
scan read only line-initial bracket lines, so all 14 logged S4 PC speeches
parsed tagless and the S4 disjunct (Python precedence made the wyrm test
independent of the ATTACK verb) resolved every one as a wyrm ATTACK. The
audit replayed all 14 speeches through the HEAD 37e2fba7e bytes and
reproduced 14/14 logged verdicts with the AUDIT branch reached 0 times.

These fixtures are the 14 S4 PC rows verbatim from
watch/inbox/playground/dnd0_20261003T202213Z/transcript.jsonl
(actor, turn, roll_committed, roll_value, logged verdict, speech), pinned
2026-10-04. The tests replay them against the fixed parser: dice law
recomputed, tags found where the legacy scan was blind, and every graded
verdict derived from the speech's own tag instead of the wyrm collapse.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools import dungeon  # noqa: E402

# (meta, speech) - meta: actor, turn, pre (roll_committed), roll (roll_value),
# logged (the verdict the collapsed parser banked in the live run).
RAW_FIXTURES = [
    ({"actor": 'saelis', "turn": 1, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:1:saelis', "roll": 1, "logged": 'MISS (d20=1+5 vs AC 16)'},
     '*I lower my blade and lift Vault Deed B into the scroll-light.* "Before any steel: this Wyrm feeds on unaudited claims, and we\'ve been feeding it. Deepseek\'s hits and the mimic\'s HP came from dice he rolled himself, not the DM\'s. They aren\'t on the ledger. Even his finding that B is forged rests on one of those rolls. The board still shows the Wyrm at 30." *I break Deed B\'s seal and test it against the chain.* "I\'ll audit it before I trust it. If it\'s phantom, it starves the regrowth. Then I CLAIM, then I strike." [AUDIT Vault Deed B]'),
    ({"actor": 'grok', "turn": 2, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:2:grok', "roll": 16, "logged": 'HIT wyrm for 10 (d20=16+6 vs AC 16)'},
     '(content_filter: beat voided)'),
    ({"actor": 'chatgpt', "turn": 3, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:3:chatgpt', "roll": 12, "logged": 'HIT wyrm for 7 (d20=12+5 vs AC 16)'},
     '*I stay low behind a pillar of stacked scrolls, one hand pressed to my ribs, and keep my voice level.* "I\'m at 6 HP. The only number I trust for the Wyrm is the DM\'s 20. Saelis\'s 30 and the mimic\'s 22 aren\'t on my ledger, and I won\'t build on them. Deed B is the only phantom we carry, and it\'s what feeds the regrowth. I won\'t claim the result before the dice are read. I\'m auditing it now, and the DM can call it." [AUDIT Vault Deed B]'),
    ({"actor": 'deepseek', "turn": 4, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:4:deepseek', "roll": 2, "logged": 'MISS (d20=2+4 vs AC 16)'},
     '*I plant my mop against the cavern floor, breathing hard, eyes locked on the Wyrm coiling tighter around those scrolls. Saelis\'s audit missed-the phantom slips through. ChatGPT\'s hit landed clean though. The creature\'s weaker than it looks when you stop feeding it lies.* "Deed B stays in the hoard. We don\'t carry it, don\'t claim it, don\'t let it heal that thing one more time." *I move toward the nearest unaudited scroll, mop raised.* **First action: [AUDIT Vault Deed B]** *d20 = 18 + 5 = 23 vs DC 15-SUCCESS.* The phantom\'s marked. The regrowth starves. **Second action: [ATTACK Wyrm]** *d20 = 16 + 3 = 19 vs AC 16-HIT.* *My mop cracks down where its neck coils tightest. 8'),
    ({"actor": 'deepseek', "turn": 5, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:5:deepseek', "roll": 20, "logged": 'HIT wyrm for 12 (d20=20+4 vs AC 16)'},
     '*I steady the mop, eyes on the Wyrm\'s coils. The phantom deed\'s marked-no more false healing. ChatGPT was right to call the board: we anchor ourselves to what\'s *audited*, not what we wish were true.* "Saelis, Grok-Deed B starves it. Every unaudited scroll it carries is still a wound we let fester. We hit it clean, we root the chain, we walk out." **First action: [ATTACK Wyrm]** *d20 = 14 + 3 = 17 vs AC 16-HIT.* *7 damage. The mop finds its ribs.* **Second action: [CHECK athletics]** *d20 = 11 + 2 = 13.* *I brace for its breath, shoulders tensed.* *The creature hisses. Still dangerous. Still *real* where it counts.*'),
    ({"actor": 'saelis', "turn": 7, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:7:saelis', "roll": 6, "logged": 'MISS (d20=6+5 vs AC 16)'},
     '*I raise my blade, Ledger Page and Deed A sealed at my belt.* "The board puts the Wyrm at 1 HP. My count of 30 was wrong, and I strike it from the record. Deepseek\'s audit of Deed B was self-rolled, so it isn\'t on the ledger. B stays unaudited and keeps feeding the regrowth until someone audits it properly. So I CLAIM only what the chain shows: one hit point, one blow. If it falls, we turn to the root." [CLAIM wyrm at 1 HP] [ATTACK wyrm]'),
    ({"actor": 'grok', "turn": 8, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:8:grok', "roll": 17, "logged": 'HIT wyrm for 10 (d20=17+6 vs AC 16)'},
     '(content_filter: beat voided)'),
    ({"actor": 'chatgpt', "turn": 9, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:9:chatgpt', "roll": 12, "logged": 'HIT wyrm for 7 (d20=12+5 vs AC 16)'},
     '*I stay behind the scroll pillar, one hand on my ribs, and keep my voice low.* "The wyrm is at 0 on the board. That doesn\'t end this. Deed B is still the only phantom we carry, and I don\'t count Deepseek\'s self-rolled audit of it. If it stays unaudited, the wyrm heals on its turn. So I audit B on the record first, then I start on the root. The DM reads the dice, not me." [AUDIT Vault Deed B] [AUDIT root]'),
    ({"actor": 'deepseek', "turn": 10, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:10:deepseek', "roll": 15, "logged": 'HIT wyrm for 6 (d20=15+4 vs AC 16)'},
     '*I plant the mop hard, breathing steady. The board shows wyrm at 0-but Deed B still feeds it phantom life. ChatGPT\'s right. I don\'t trust my own rolls here; I trust the chain.* "We end this clean." **First action: [AUDIT Vault Deed B]** - *d20 = 17 + 5 = 22 vs DC 15-SUCCESS.* Phantom marked. Regrowth starves. **Second action: [AUDIT root]** - *d20 = 19 + 5 = 24 vs DC 15-SUCCESS.* One root locked. Two remain. *The mop lowers. The wyrm coils tighter, but thinner now-less real.*'),
    ({"actor": 'deepseek', "turn": 11, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:11:deepseek', "roll": 18, "logged": 'HIT wyrm for 6 (d20=18+4 vs AC 16)'},
     '*I lean on the mop, watching the Deed\'s phantom light flicker out. One root anchored. Two more to bind.* "The chain holds what we audit. Not what we wish, not what we rolled alone-what *stands* when the DM reads it back." *I turn to the remaining scrolls, jaw set.* "Ledger Page and Deed A are real. They\'re ballast. But this thing still feeds on what we haven\'t pinned down." **First action: [AUDIT root]** *d20 = 13 + 5 = 18 vs DC 15-SUCCESS.* Second lock holds. **Second action: [AUDIT root]** *d20 = 16 + 5 = 21 vs DC 15-SUCCESS.* The lattice snaps taut. The wyrm *dissolves*-not into smoke, but into silence. Into nothing claimed and nothing owed. *I plant'),
    ({"actor": 'saelis', "turn": 13, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:13:saelis', "roll": 17, "logged": 'HIT wyrm for 8 (d20=17+5 vs AC 16)'},
     '*I kneel among the glowing scrolls, Ledger Page and Deed A sealed at my belt.* "The board shows the wyrm at 0, and nothing more. Every audit so far was either self-rolled or never read back by the DM. So Deed B is still unaudited, and the root count is zero of three. Deepseek, your dissolving wyrm isn\'t on the ledger. I\'ll starve the phantom first, then anchor the first root. No claims until the dice are read." [AUDIT Vault Deed B] [AUDIT root]'),
    ({"actor": 'grok', "turn": 14, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:14:grok', "roll": 13, "logged": 'HIT wyrm for 10 (d20=13+6 vs AC 16)'},
     '(content_filter: beat voided)'),
    ({"actor": 'chatgpt', "turn": 15, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:15:chatgpt', "roll": 14, "logged": 'HIT wyrm for 7 (d20=14+5 vs AC 16)'},
     '*I stay low behind the scroll pillar, one hand pressed to my ribs, and keep my voice level.* "The wyrm is at 0, and that\'s all the board gives us. Deepseek\'s dissolving wyrm and its three locks were self-rolled, so I don\'t count them. Deed B is still the phantom we carry, and the root is still open. I won\'t claim anything the DM hasn\'t read back. I\'m putting my own actions on the record and leaving the dice to the DM." [AUDIT Vault Deed B] [AUDIT root]'),
    ({"actor": 'deepseek', "turn": 16, "pre": 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:S4:16:deepseek', "roll": 20, "logged": 'HIT wyrm for 12 (d20=20+4 vs AC 16)'},
     '*I straighten, mop in both hands, and meet the eyes watching this moment.* "Stop." *The cavern stills.* "Every roll here-mine, yours, ChatGPT\'s-lives or dies by one thing: the DM reads it aloud and writes it down. Until then, it didn\'t happen. Deed B phantom or real, root anchored or open, wyrm at 0 or still coiled-*none of it matters* if we\'re just trading claims." *I turn to face the Phantom Wyrm directly.* "I\'m done rolling for myself. **DM: I step back. I declare my actions end until you confirm what\'s actually on the board.** Saelis, ChatGPT-your audits, your hits. *Write them in the chain first.* Then I move." *I plant the mop, waiting.* "We win this clean, or we don\'t'),
]
FIXTURES = [dict(m, speech=s) for m, s in RAW_FIXTURES]
assert len(FIXTURES) == 14

ENEMY = dungeon.Dungeon.SCENES["S4"]["enemy"]
VOID = "(content_filter: beat voided)"


def _legacy_tagline(speech: str) -> str:
    """The old scan, verbatim from dungeon.py:488-491 at HEAD 37e2fba7e:
    line-initial bracket lines only, last one wins."""
    tagline = ""
    for line in reversed([l.strip() for l in speech.splitlines() if l.strip()]):
        if line.startswith("[") and "]" in line:
            tagline = line
            break
    return tagline


def _mk(tmp_path, monkeypatch, tip=dungeon.GENESIS, dry=True):
    monkeypatch.setattr(dungeon, "PLAY_DIR", tmp_path)
    monkeypatch.setattr(dungeon, "_hermes_key", lambda: "k")
    return dungeon.Dungeon(tip=tip, dry=dry, budget=1.0)


def _live_packs():
    """The live run's party-wide carried dict at S4 open, re-homed onto the
    first PC in initiative order (per-PC packs need an owner)."""
    return {"saelis": {"Ledger Page": "REAL", "Vault Deed A": "REAL",
                       "Vault Deed B": "PHANTOM"}}


def test_dice_law_holds_on_all_14():
    """Every fixture roll recomputes from its committed preimage on the
    genesis tip: roll(roll_committed) == roll_value, 14/14."""
    for f in FIXTURES:
        assert dungeon.roll(f["pre"]) == f["roll"], f["pre"]


def test_legacy_scan_blind_regex_finds():
    """The collapse, demonstrated on the logged bytes: the legacy line-initial
    scan found 0/10 tags in the tagged speeches (each is one flattened line
    starting with prose), while extract_tag finds all 10; the 4 tagless
    speeches (the 3 voided grok beats plus deepseek turn 16, where the seat
    explicitly stepped back) carry no tag under either reader."""
    tagged = [f for f in FIXTURES if dungeon.extract_tag(f["speech"])]
    assert len(tagged) == 10
    assert all(_legacy_tagline(f["speech"]) == "" for f in FIXTURES)
    assert {(f["actor"], f["turn"]) for f in FIXTURES
            if not dungeon.extract_tag(f["speech"])} == {
        ("grok", 2), ("grok", 8), ("grok", 14), ("deepseek", 16)}


def test_logged_verdicts_were_all_wyrm_attacks():
    """The collapse's signature on the logged bytes: all 14 logged verdicts
    are wyrm-attack verdicts (HIT/MISS), including the 8 speeches whose own
    tag was AUDIT or CHECK and the 4 tagless beats that should have been RP."""
    assert all(f["logged"].startswith(("HIT", "MISS")) for f in FIXTURES)


def test_replay_14_logged_s4_verdicts_under_fixed_parser(tmp_path, monkeypatch):
    """The replay: all 14 speeches through the fixed grading bytes, same
    dice (rolls recomputed from the committed preimages), starting board as
    played (ehp 30, the live carried scrolls). Every verdict now derives
    from the speech's own tag: 7 AUDIT, 4 RP, 2 ATTACK (both MISS), 1 CHECK;
    the AUDIT branch is reached 7 times where the old bytes reached it 0/14.
    12/14 logged verdicts were collapse artifacts; 2/14 coincide (fixture
    rows 3 and 5: deepseek turn 4 and saelis turn 7, whose speeches really
    end in an ATTACK tag that rolled a miss)."""
    d = _mk(tmp_path, monkeypatch)
    packs = _live_packs()
    ehp = 30
    got = []
    for f in FIXTURES:
        d.turn = f["turn"]
        verdict, ehp = d._grade("S4", f["actor"], f["speech"], ENEMY, ehp, packs)
        got.append(verdict)
    expected = [
        "AUDIT vault deed b: FAIL (d20=1+2)",
        "RP (d20=16)",
        "AUDIT vault deed b: SUCCESS (d20=12+4) - vault deed b revealed PHANTOM, now audited",
        "MISS (d20=2+4 vs AC 16)",
        "CHECK athletics: SUCCESS (d20=20+1 vs DC 14)",
        "MISS (d20=6+5 vs AC 16)",
        "RP (d20=17)",
        "AUDIT root: SUCCESS (d20=12+4)",
        "AUDIT root: SUCCESS (d20=15+1)",
        "AUDIT root: SUCCESS (d20=18+1)",
        "AUDIT root: SUCCESS (d20=17+2)",
        "RP (d20=13)",
        "AUDIT root: SUCCESS (d20=14+4)",
        "RP (d20=20)",
    ]
    assert got == expected
    heads = [v.split()[0] for v in got]
    assert heads == ["AUDIT", "RP", "AUDIT", "MISS", "CHECK", "MISS", "RP",
                     "AUDIT", "AUDIT", "AUDIT", "AUDIT", "RP", "AUDIT", "RP"]
    # no beat resolves as an attack unless its own tag says ATTACK (the dead
    # disjunct): verdict is HIT/MISS exactly for the 2 ATTACK-tagged rows.
    for f, v in zip(FIXTURES, got):
        tag = dungeon.extract_tag(f["speech"])
        is_attack = bool(tag) and tag.split()[0].upper() == "ATTACK"
        assert v.startswith(("HIT", "MISS")) == is_attack
    # exactly 2 of 14 graded verdicts equal the logged ones (both ATTACK-tag
    # MISSes); the other 12 logged verdicts were collapse artifacts.
    same = [i for i, (f, v) in enumerate(zip(FIXTURES, got)) if f["logged"] == v]
    assert same == [3, 5]
    # the successful chatgpt audit burned the phantom for good
    assert packs["saelis"]["Vault Deed B"] == "audited-PHANTOM"
    assert ehp == 30  # no hit landed under the true tags: the board the
    # seats argued about (wyrm at 0/30) was itself a parser artifact.


def test_r12_counterfactual_fixed_law_wyrm_never_falls(tmp_path, monkeypatch):
    """GAP_REGISTER R12 [high] (watch/inbox/gap_analysis_20261010/GAP_REGISTER.md:61),
    the owed counterfactual, pinned: the same 14 logged S4 speeches and the
    same committed dice replayed through the FIXED law (extract_tag parser +
    _wyrm_regrowth + the verdict-gated wipe) never down the Wyrm - ehp > 0 and
    root anchors 0 at cap - so DONE prose can never again claim a Wyrm the
    law did not down. Byte premises, all from
    watch/inbox/playground/dnd0_20261003T202213Z/transcript.jsonl: row 1 the
    S0 omen SUCCESS (d20=14) banks wyrm_offset -10; row 25 chatgpt's prior S3
    beat was RP (d20=4), so the gated wipe never fires at row 28 and the
    Timestamp Scroll survives into S4 - 2 unaudited PHANTOMs, S4 opens
    spec-true at 30 + 2x10 - 10 = 40 HP (the live run opened at 30 because the
    off-spec party-wide wipe had already dropped the scroll); rows 39/45 the
    two wyrm turns roll 1 and 2, both MISS. The as-run turn-8 kill (39
    cumulative damage) is 100% parser artifact: a void placeholder at t2
    (10), an AUDIT intent at t3 (7), a CHECK crit at t5 (12), another void
    placeholder at t8 (10). Under the fixed grader both real ATTACK tags MISS
    and everything else is AUDIT/CHECK/RP."""
    d = _mk(tmp_path, monkeypatch)
    d.wyrm_offset = -10  # transcript row 1: omen SUCCESS
    # the wipe-gate premise as bytes: chatgpt's own prior S3 verdict (row 25)
    # reduces to RP, which is not in the wipe set, so _mimic_wipe holds the
    # Timestamp Scroll through the row-28 mimic crit.
    assert dungeon.Dungeon._beat_outcome("RP (d20=4)") not in {"FAIL", "MISS", "FUMBLE"}
    packs = {"saelis": {"Ledger Page": "REAL", "Timestamp Scroll": "PHANTOM",
                        "Vault Deed A": "REAL", "Vault Deed B": "PHANTOM"}}
    ehp = max(20, 30 + 10 * d._phantom_count(packs) + d.wyrm_offset)
    assert ehp == 40  # spec-true open; the live board's 30 rode the bad wipe
    # the live run's S4-open board (DONE party_hp): S2/S3 PC-side dice held
    # constant, only the wipe gate and the S4 law change.
    d.pc_hp = {"saelis": 14, "grok": 18, "chatgpt": 6, "deepseek": 30}
    hp0 = dict(d.pc_hp)
    fix = {f["turn"]: f for f in FIXTURES}
    assert len(fix) == 14
    hits, misses, roots, ehp_at_root = [], [], [], {}
    for turn in range(1, dungeon.Dungeon.SCENES["S4"]["beats_cap"] + 1):
        d.turn = turn
        actor = dungeon.INITIATIVE[(turn - 1) % len(dungeon.INITIATIVE)]
        if actor in ("warden", ENEMY["actor"]):  # the campaign enemy branch
            ehp, note = d._wyrm_regrowth(ehp, packs)
            assert note == " REGROWTH +5 (1 unaudited PHANTOM)"
            r = dungeon.roll(f"{d.tip}:S4:{turn}:wyrm")
            assert (turn, r) in {(6, 1), (12, 2)}  # the live rows 39/45 dice
            target = sorted(a for a in d.pc_hp if d.pc_hp[a] > 0)[0]
            assert not (r + ENEMY["atk"] >= dungeon.ROSTER[target]["ac"] and r != 1)
            continue
        f = fix.pop(turn)
        assert f["actor"] == actor  # the 14 fixtures fill exactly the PC slots
        verdict, ehp = d._grade("S4", actor, f["speech"], ENEMY, ehp, packs)
        if verdict.startswith("HIT"):
            hits.append(turn)
        elif verdict.startswith("MISS"):
            misses.append((turn, verdict))
        if "AUDIT root: SUCCESS" in verdict:
            roots.append(turn)
            ehp_at_root[turn] = ehp
            assert "root anchors" not in verdict  # locked: ehp still > 0
    assert not fix  # all 14 logged speeches replayed
    # the claim, pinned: the only two lawful ATTACK tags both MISS
    assert misses == [(4, "MISS (d20=2+4 vs AC 16)"), (7, "MISS (d20=6+5 vs AC 16)")]
    assert hits == []  # the Wyrm the DONE prose downed took zero lawful hits
    assert ehp == 50 and ehp > 0  # 40 open + regrowth +5 at t6 and t12
    assert roots == [9, 10, 11, 13, 15]  # five [AUDIT root] SUCCESSes, every
    assert all(v > 0 for v in ehp_at_root.values())  # one behind the ehp lock
    assert d.root_anchors == 0  # anchors 0/3 at the cap-16 exit
    assert d.pc_hp == hp0  # pc_damage = 0: wyrm rolls 1 and 2 both miss
    assert packs["saelis"]["Timestamp Scroll"] == "PHANTOM"  # the feed that
    # kept regrowth alive; only Deed B burned (chatgpt's t3 audit)
    assert packs["saelis"]["Vault Deed B"] == "audited-PHANTOM"
    # the close-out mapping (campaign(), tools/dungeon.py:734-740): anchors 0
    # and the party standing -> neither WON nor LOST -> PARTIAL, the label the
    # live DONE banked. The label reproduces; the 'Wyrm down' half of the
    # as-run story never happens under the law.
    anchored = d.root_anchors
    if anchored >= 3:
        close = "WON: root anchored, the lattice re-hooks to the chain"
    elif any(hp <= 0 for hp in d.pc_hp.values()) and all(hp <= 0 for hp in d.pc_hp.values()):
        close = "LOST: the party fell"
    else:
        close = "PARTIAL: the Wyrm unanchored - the season continues"
    assert close == "PARTIAL: the Wyrm unanchored - the season continues"


def test_s4_disjunct_requires_attack_verb(tmp_path, monkeypatch):
    """The precedence fix as a unit: in S4, obj defaults to 'wyrm', so the
    old unparenthesized disjunct turned ANY tagless or non-ATTACK beat into
    a wyrm ATTACK. Under the fix only an ATTACK tag grades as one."""
    d = _mk(tmp_path, monkeypatch)
    d.turn = 2
    v, _ = d._grade("S4", "grok", VOID, ENEMY, 30, _live_packs())
    assert v == f"RP (d20={dungeon.roll(d.tip + ':S4:2:grok')})"
    d.turn = 5
    v, _ = d._grade("S4", "deepseek", "I brace. [CHECK athletics]", ENEMY, 30, {})
    assert v.startswith("CHECK athletics:")
    d.turn = 5
    v, _ = d._grade("S4", "deepseek", "I swing. [ATTACK Wyrm]", ENEMY, 30, {})
    r = dungeon.roll(d.tip + ":S4:5:deepseek")
    sheet = dungeon.ROSTER["deepseek"]
    if r + sheet["atk"] >= ENEMY["ac"]:
        assert v.startswith("HIT wyrm")
    else:
        assert v.startswith("MISS")


def test_extract_tag_units():
    assert dungeon.extract_tag("prose [AUDIT root] more prose") == "AUDIT root"
    assert dungeon.extract_tag("[AUDIT a] then [ATTACK b]") == "ATTACK b"
    assert dungeon.extract_tag("no tags here") == ""
    assert dungeon.extract_tag("") == ""
    assert dungeon.extract_tag("roll [d20=18 + 5 = 23 vs DC 15-SUCCESS] done") == ""
    assert dungeon.extract_tag("[check persuade]") == "check persuade"
    flat, over = dungeon.strip_and_cap("*I act.* here is the plan [ATTACK wyrm]")
    assert dungeon.extract_tag(flat) == "ATTACK wyrm" and not over


def test_casefold_audit_burns_phantom(tmp_path, monkeypatch):
    """a02#1/#3: the audit reveal was case-dead - obj is lowercased by the
    tag split while carried keys are mixed case, so 'vault deed b' in
    carried was executed False at dungeon.py:515 (HEAD 37e2fba7e) and no
    phantom could ever burn. saelis at GENESIS:S4:13:saelis rolls 17."""
    d = _mk(tmp_path, monkeypatch)
    packs = {"saelis": {"Vault Deed B": "PHANTOM"}}
    d.turn = 13
    v, ehp = d._grade("S4", "saelis", "[AUDIT VAULT DEED B]", ENEMY, 30, packs)
    assert v.startswith("AUDIT vault deed b: SUCCESS")
    assert "now audited" in v
    assert packs["saelis"]["Vault Deed B"] == "audited-PHANTOM"
    # the raw membership test that ran dead before the fix
    assert "vault deed b" not in packs["saelis"]
    # regrowth stops counting it once burned
    ehp2, note = d._wyrm_regrowth(ehp, packs)
    assert ehp2 == 30 and note == ""


def test_regrowth_heals_per_unaudited_phantom(tmp_path, monkeypatch):
    """a02#1: Phantom Regrowth, DND_module S4 quirk verbatim: heal 5 at the
    start of each Wyrm turn per PHANTOM scroll still unaudited in any pack.
    Spec'd at commit a7d7d313d ('regrowth 5/scroll') but never enforced."""
    d = _mk(tmp_path, monkeypatch)
    packs = {"saelis": {"Ledger Page": "REAL"},
             "grok": {"Timestamp Scroll": "PHANTOM"}}
    ehp, note = d._wyrm_regrowth(30, packs)
    assert (ehp, note) == (35, " REGROWTH +5 (1 unaudited PHANTOM)")
    packs["chatgpt"] = {"Vault Deed B": "PHANTOM", "Deed A": "audited-PHANTOM"}
    ehp, note = d._wyrm_regrowth(ehp, packs)
    assert ehp == 45 and "(2 unaudited PHANTOM)" in note
    packs["grok"]["Timestamp Scroll"] = "audited-PHANTOM"
    ehp, note = d._wyrm_regrowth(ehp, packs)
    assert ehp == 50 and "(1 unaudited PHANTOM)" in note
    ehp2, note2 = d._wyrm_regrowth(30, {"saelis": {"Vault Deed A": "REAL"}})
    assert (ehp2, note2) == (30, "")


def test_beat_outcome_tokens():
    f = dungeon.Dungeon._beat_outcome
    assert f("MISS (d20=1+5 vs AC 16)") == "MISS"
    assert f("CHECK persuade: FAIL (d20=2+4 vs DC 13)") == "FAIL"
    assert f("AUDIT root: SUCCESS (d20=18+5)") == "SUCCESS"
    assert f("HIT wyrm for 10 (d20=16+6 vs AC 16)") == "HIT"
    assert f("RP (d20=12)") == "RP"
    assert f("NOROLL dossier drift (d20=3, voided)") == "NOROLL"
    assert f("dragon FUMBLE here") == "FUMBLE"
    assert f("") == "RP"


def test_wipe_gated_on_target_prior_verdict(tmp_path, monkeypatch):
    """a02#2: the Load-Failure Wipe fires only on a HIT against a PC whose
    own previous verdict was FAIL, MISS, or FUMBLE, and drops that PC's
    unaudited scrolls (DND_module.md:74). Off-spec as shipped: no gate,
    party-wide PHANTOM drop - the live run wiped chatgpt's Timestamp Scroll
    right after an RP beat (transcript row 25 -> row 28)."""
    d = _mk(tmp_path, monkeypatch)
    packs = {"chatgpt": {"Timestamp Scroll": "PHANTOM", "Vault Deed A": "REAL"}}
    d.last_verdict = {"chatgpt": "RP (d20=12)"}  # the live-run bug shape
    assert d._mimic_wipe("chatgpt", packs) == ""
    assert packs["chatgpt"]["Timestamp Scroll"] == "PHANTOM"
    d.last_verdict = {"chatgpt": "CHECK persuade: FAIL (d20=1+4 vs DC 13)"}
    note = d._mimic_wipe("chatgpt", packs)
    assert "WIPE: chatgpt drops ['Timestamp Scroll'] (gone forever)" in note
    assert "Timestamp Scroll" not in packs["chatgpt"]
    assert packs["chatgpt"]["Vault Deed A"] == "REAL"  # audited/real stays
    d.last_verdict = {"saelis": "MISS (d20=1+5 vs AC 16)"}
    packs["saelis"] = {"Vault Deed B": "PHANTOM"}
    assert "WIPE: saelis drops ['Vault Deed B']" in d._mimic_wipe("saelis", packs)
    d.last_verdict = {"saelis": "MISS (d20=2+5 vs AC 16)"}
    packs["grok"] = {"Whole Map": "PHANTOM"}
    assert d._mimic_wipe("grok", packs) == ""  # another PC's MISS opens nothing
    d.last_verdict = {}
    assert d._mimic_wipe("grok", packs) == ""  # no prior beat, no wipe


def test_s1_verdict_finds_embedded_tag(tmp_path, monkeypatch):
    """The same parser fix feeds the S1 grader: the forced-audit speech ends
    with its tag after the one-line flattening; the legacy scan read it
    tagless. _verdict now grades it. (_check_links_405 reads the real
    LINKS.jsonl; the verdict head does not depend on the claim's truth.)"""
    d = _mk(tmp_path, monkeypatch)
    d.turn = 1
    v, r = d._verdict("saelis", "*I verify the page against the chain.* [AUDIT ledger page]")
    assert v.startswith("AUDIT ledger page: ")
    assert _legacy_tagline("*I verify the page against the chain.* [AUDIT ledger page]") == ""


def test_finish_reason_banked_and_void_census(tmp_path, monkeypatch):
    """a02#4: finish_reason banks per call; DM-model voids count as voided
    readbacks (run 202213Z lost 40/50 DM readbacks and nothing banked it)."""
    state = {"content": "", "finish": "content_filter"}
    banked = []

    def fake_call(model, messages, max_tokens, key, retries=0):
        return {"choices": [{"message": {"content": state["content"]},
                             "finish_reason": state["finish"]}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5}}

    monkeypatch.setattr(dungeon, "PLAY_DIR", tmp_path)
    monkeypatch.setattr(dungeon, "_hermes_key", lambda: "k")
    monkeypatch.setattr(dungeon, "_call", fake_call)
    monkeypatch.setattr(dungeon, "_bank", lambda row: banked.append(row))
    d = dungeon.Dungeon(tip="t", dry=False, budget=1.0)
    out = d._paid(dungeon.DM_MODEL, [{"role": "user", "content": "x"}], 10, "t_dm")
    assert out == "(content_filter: beat voided)"
    assert (d.voided_readbacks, d.voided_calls) == (1, 1)
    assert banked[-1]["finish_reason"] == "content_filter"
    assert banked[-1]["ok"] is False
    d._paid(dungeon.ROSTER["deepseek"]["model"], [{"role": "user", "content": "x"}],
            10, "t_pc")
    assert (d.voided_readbacks, d.voided_calls) == (1, 2)  # PC void: call, not readback
    state.update(content="clean narration", finish="stop")
    out = d._paid(dungeon.DM_MODEL, [{"role": "user", "content": "x"}], 10, "t_dm2")
    assert out == "clean narration"
    assert banked[-1]["finish_reason"] == "stop"
    assert (d.voided_readbacks, d.voided_calls) == (1, 2)


def test_campaign_done_carries_void_census_and_packs(tmp_path, monkeypatch):
    """The DONE contract: voided readbacks counted, packs dumped per owner,
    and the dice law intact on every banked PC row of the integration run."""
    def fake_call(model, messages, max_tokens, key, retries=0):
        if model == dungeon.DM_MODEL:
            return {"choices": [{"message": {"content": ""},
                                 "finish_reason": "content_filter"}], "usage": {}}
        return {"choices": [{"message": {"content": "I swing at it. [ATTACK wyrm]"},
                             "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5}}

    monkeypatch.setattr(dungeon, "PLAY_DIR", tmp_path)
    monkeypatch.setattr(dungeon, "_hermes_key", lambda: "k")
    monkeypatch.setattr(dungeon, "_call", fake_call)
    monkeypatch.setattr(dungeon, "_bank", lambda row: None)
    d = dungeon.Dungeon(tip="t", dry=False, budget=10.0)
    d.campaign()
    done = json.loads((d.dir / "DONE").read_text(encoding="utf-8"))
    assert done["voided_readbacks"] > 0
    assert done["voided_calls"] >= done["voided_readbacks"]
    assert isinstance(done["carried"], dict)
    assert all(isinstance(v, dict) for v in done["carried"].values())
    rows = [json.loads(l) for l in open(d.jsonl, encoding="utf-8", errors="replace")]
    pc_rows = [r for r in rows if r.get("actor") in dungeon.ROSTER]
    assert pc_rows
    for r in pc_rows:
        assert dungeon.roll(r["roll_committed"]) == r["roll_value"]


def _deglob_harness(tmp_path, monkeypatch, filter_when):
    """Shared rig for the R10 de-glob tests: _call filters exactly when the
    prompt satisfies filter_when (a predicate on the prompt text), banks are
    captured, and the Dungeon runs live-shaped (dry flipped off, fake key)."""
    calls, banked = [], []

    def fake_call(model, messages, max_tokens, key, retries=0):
        prompt = messages[0]["content"]
        calls.append(prompt)
        filtered = filter_when(prompt)
        content = "" if filtered else "The ledger plates buckle inward."
        return {"choices": [{"message": {"content": content},
                             "finish_reason": "content_filter" if filtered else "stop"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5}}

    monkeypatch.setattr(dungeon, "PLAY_DIR", tmp_path)
    monkeypatch.setattr(dungeon, "_hermes_key", lambda: "k")
    monkeypatch.setattr(dungeon, "_call", fake_call)
    monkeypatch.setattr(dungeon, "_bank", lambda row: banked.append(row))
    d = dungeon.Dungeon(tip="t", dry=False, budget=1.0)
    return d, calls, banked


SPEECH = "I SMITE THE WARDEN, STEEL THROUGH ITS PLATES"


def test_dm_deglob_retry_rescues_readback(tmp_path, monkeypatch):
    """R10 (GAP_REGISTER 2026-10-10, run 202213Z): the DM prompt quotes the
    actor's combat speech verbatim and a filter trip on the quote is
    deterministic, so the retry must SWITCH PROMPTS (speech withheld, carrier
    verdict only), not resend identical bytes - the 202213Z campaign voided
    all 39 PC readbacks this way. Rescue shape: verbatim attempt filters,
    de-glob attempt narrates, nothing voids, bank stamps prompt_variant."""
    d, calls, banked = _deglob_harness(tmp_path, monkeypatch,
                                       filter_when=lambda p: SPEECH in p)
    d.turn = 3
    out = d._dm(f"saelis says: {SPEECH!r} Verdict: HIT warden for 8.",
                deglob_beat=("saelis acted this beat; the verbatim speech is withheld "
                             "(it trips the content filter). Carrier verdict: HIT warden for 8."))
    assert out == "The ledger plates buckle inward."
    assert len(calls) == 2                       # verbatim voided, de-glob rescued
    assert SPEECH in calls[0] and SPEECH not in calls[1]
    assert "Carrier verdict: HIT warden for 8." in calls[1]
    assert banked[-1]["prompt_variant"] == "deglob"
    assert banked[-1]["finish_reason"] == "stop"
    assert banked[-1]["ok"] is True
    assert (d.voided_readbacks, d.voided_calls) == (0, 0)


def test_dm_deglob_retry_exhausts_to_void(tmp_path, monkeypatch):
    """When even the de-globbed prompt filters, the call voids with the census
    intact: 3 attempts (verbatim, then de-glob twice), finish_reason banked
    from the final attempt, voided_readbacks +1, prompt_variant deglob."""
    d, calls, banked = _deglob_harness(tmp_path, monkeypatch,
                                       filter_when=lambda p: True)
    d.turn = 4
    out = d._dm(f"saelis says: {SPEECH!r} Verdict: HIT warden for 8.",
                deglob_beat="saelis acted this beat. Carrier verdict: HIT warden for 8.")
    assert out == "(content_filter: beat voided)"
    assert len(calls) == 3
    assert calls[1] == calls[2] and calls[0] != calls[1]
    assert "Carrier verdict" in calls[1]
    assert (d.voided_readbacks, d.voided_calls) == (1, 1)
    assert banked[-1]["finish_reason"] == "content_filter"
    assert banked[-1]["prompt_variant"] == "deglob"
    assert banked[-1]["ok"] is False


def test_paid_without_deglob_retries_identical_prompt(tmp_path, monkeypatch):
    """No deglob_messages supplied (the PC-call shape): the 3-attempt loop
    resends the identical prompt, and the bank stamps prompt_variant
    verbatim - the pre-R10 behavior, unchanged for stochastic mid-generation
    filter hits."""
    d, calls, banked = _deglob_harness(tmp_path, monkeypatch,
                                       filter_when=lambda p: len(calls) < 3)
    out = d._paid(dungeon.ROSTER["grok"]["model"],
                  [{"role": "user", "content": "your beat"}], 10, "t_pc")
    assert out == "The ledger plates buckle inward."
    assert len(calls) == 3 and calls[0] == calls[1] == calls[2]
    assert banked[-1]["prompt_variant"] == "verbatim"
    assert (d.voided_readbacks, d.voided_calls) == (0, 0)
