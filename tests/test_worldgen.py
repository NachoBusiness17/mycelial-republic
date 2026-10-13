"""Worldgen port tests — mag/worldgen.py vs roblox/src/shared/Worldgen.luau
+ roblox/src/server/ZoneGate.luau.

Mission contract (W5, watch/inbox/last_mile_20260930/W5_WORLDGEN.md):
  - same UserId produces the same sphere assignment (determinism),
  - allied zones open (+VirtueMark), opposed zones refuse,
  - the alliance table resolves (kinship law 4: opposition outranks kin).

Golden anchors (UserId -> sphere; seed -> beast name) were computed once
from this port and baked in: they pin the xorshift32 stream so future
refactors cannot silently drift the per-soul draw. The data mirrors
(SPHERES/ALIGNMENT/ALLIES/OPPOSED/REGION_SPHERES/DWARVEN) are asserted
against the structural laws of the generated Luau artifacts (130 spheres,
symmetric opposition, grounded rows), not hand-copied constants.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mag.worldgen as wg  # noqa: E402
from mag.worldgen import (  # noqa: E402
    ALLIES,
    ALIGNMENT,
    DWARVEN,
    OPPOSED,
    REGION_SPHERES,
    SPHERES,
    Beast,
    SeedRng,
    Soul,
    Worldgen,
    ZoneGate,
    gate_attr,
)

SPHERE_SET = set(SPHERES)


# --------------------------------------------------------------------------
# SeedRng — bit-exact xorshift32 (shared/SeedRng.luau)
# --------------------------------------------------------------------------
class TestSeedRng:
    def test_seed_wrap_and_zero_guard(self):
        # SeedRng.new: seed % 2147483647, 0 -> 1 (xorshift32 must not start at 0)
        r = SeedRng(2147483647)  # 2147483647 * 7919 later wraps; here: 2147483647 % 2147483647 == 0
        assert r.seed == 1

    def test_stream_is_deterministic_and_in_unit_range(self):
        a = SeedRng(123456)
        b = SeedRng(123456)
        sa = [a.next() for _ in range(50)]
        sb = [b.next() for _ in range(50)]
        assert sa == sb
        assert all(0.0 <= x < 1.0 for x in sa)

    def test_int_bounds(self):
        r = SeedRng(7)
        for _ in range(500):
            v = r.int(1, 130)
            assert 1 <= v <= 130

    def test_pick_from_list(self):
        r = SeedRng(9)
        assert r.pick(["only"]) == "only"


# --------------------------------------------------------------------------
# Sphere assignment — one sphere per soul, deterministic from the UserId
# (ZoneGate.ensureSphere: SeedRng(UserId * 7919).int(1, 130))
# --------------------------------------------------------------------------
GOLDEN_SPHERES = {
    1: "LOYALTY",
    42: "VICTORY",
    123456: "DANCE",
    999999999: "PREGNANCY",
    2147483647: "AGRICULTURE",  # 2147483647 * 7919 % 2147483647 == 0 -> seed 1
}


class TestSphereAssignment:
    def test_golden_user_ids(self):
        for uid, sphere in GOLDEN_SPHERES.items():
            assert ZoneGate().ensure_sphere(Soul(uid)) == sphere

    def test_same_user_id_same_sphere(self):
        # fresh soul, fresh gate, twice: the draw is re-derivable, no store
        for uid in (1, 42, 123456, 4242424):
            first = ZoneGate().ensure_sphere(Soul(uid))
            second = ZoneGate().ensure_sphere(Soul(uid))
            assert first == second
            assert first in SPHERE_SET

    def test_sphere_attribute_is_set_and_honored(self):
        soul = Soul(123456)
        drawn = ZoneGate().ensure_sphere(soul)
        assert soul.attributes["Sphere"] == drawn
        # a pre-set attribute is authoritative: no re-draw (the Luau cached path)
        preset = Soul(1, {"Sphere": "WAR"})
        assert ZoneGate().ensure_sphere(preset) == "WAR"
        assert preset.attributes["Sphere"] == "WAR"

    def test_all_spheres_reachable(self):
        # the draw spreads across the whole 130, not a corner
        seen = {ZoneGate().ensure_sphere(Soul(i)) for i in range(5000)}
        assert seen == SPHERE_SET


# --------------------------------------------------------------------------
# The alliance table resolves — kinship law 4 (opposition outranks kin)
# (Worldgen.zoneAlliance / sphereAlignment)
# --------------------------------------------------------------------------
class TestAllianceTable:
    def test_opposed_symmetric(self):
        w = Worldgen()
        assert w.zone_alliance("BLIGHT", "CHARITY") == "opposed"
        assert w.zone_alliance("CHARITY", "BLIGHT") == "opposed"

    def test_allied_symmetric(self):
        w = Worldgen()
        assert w.zone_alliance("NATURE", "ANIMALS") == "allied"
        assert w.zone_alliance("ANIMALS", "NATURE") == "allied"

    def test_independent(self):
        w = Worldgen()
        assert w.zone_alliance("ART", "WAR") == "independent"
        assert w.zone_alliance("ART", "ART") == "independent"  # empty kin rows are facts

    def test_opposition_outranks_kinship(self):
        # law 4 precedence: a pair that would land in both still reads opposed
        # (structural: every aligned sphere's opposed set is exactly the other class)
        good = {s for s, a in ALIGNMENT.items() if a == "good"}
        evil = {s for s, a in ALIGNMENT.items() if a == "evil"}
        assert good and evil and not (good & evil)
        for g in good:
            assert set(OPPOSED[g]) == evil
        for e in evil:
            assert set(OPPOSED[e]) == good

    def test_alignment_lookup(self):
        w = Worldgen()
        assert w.sphere_alignment("MERCY") == "good"
        assert w.sphere_alignment("CHAOS") == "evil"
        assert w.sphere_alignment("ART") == "unaligned"

    def test_generated_tables_shape(self):
        assert len(SPHERES) == 130
        assert len(set(SPHERES)) == 130
        assert set(ALLIES) == SPHERE_SET
        assert set(OPPOSED) == SPHERE_SET
        assert set(ALIGNMENT) <= SPHERE_SET
        # every kin value grounded in the 130
        for table in (ALLIES, OPPOSED):
            for values in table.values():
                assert set(values) <= SPHERE_SET
        # region rows grounded, 11 regions, NONE empty (a fact)
        assert len(REGION_SPHERES) == 11
        for row in REGION_SPHERES.values():
            assert set(row) <= SPHERE_SET
        assert REGION_SPHERES["NONE"] == []
        # dwarven lexicon: 130 words, 50 adjective / 80 noun (ArtifactLore pools)
        assert len(DWARVEN) == 130
        assert sum(1 for x in DWARVEN if x.pos == "adjective") == 50
        assert sum(1 for x in DWARVEN if x.pos == "noun") == 80

    def test_sourced_regions_never_oppose(self):
        # the ZoneGate.luau header's fact: every sourced region row is
        # unaligned spheres, so "opposed" is unreachable through the sourced
        # table — the lock branch only fires through the injectable seam.
        w = Worldgen()
        aligned = set(ALIGNMENT)
        for row in REGION_SPHERES.values():
            for region_sphere in row:
                assert region_sphere not in aligned
                for soul_sphere in aligned:
                    assert w.zone_alliance(soul_sphere, region_sphere) != "opposed"


# --------------------------------------------------------------------------
# allianceFor — verdict over a region's whole sphere row
# --------------------------------------------------------------------------
class TestAllianceFor:
    def test_allied_region(self):
        gate = ZoneGate()
        # FOREST = ANIMALS, NATURE, PLANTS, RIVERS, TREES; NATURE allies with ANIMALS
        assert gate.alliance_for("NATURE", "FOREST") == "allied"

    def test_independent_region(self):
        gate = ZoneGate()
        assert gate.alliance_for("ART", "FOREST") == "independent"  # ART holds no kin
        assert gate.alliance_for("NATURE", "NONE") == "independent"  # empty row is a fact

    def test_unknown_region_is_independent(self):
        gate = ZoneGate()
        assert gate.alliance_for("BLIGHT", "ATLANTIS") == "independent"

    def test_opposed_through_the_seam(self):
        # the Luau header names this seam: an aligned region row is the thing
        # that grows the lock. The sourced table has none, so the port's
        # injectable region_spheres is how the branch is reachable at all.
        gate = ZoneGate(region_spheres={"TEST_HEAVEN": ["CHARITY"], "TEST_PIT": ["BLIGHT"]})
        assert gate.alliance_for("BLIGHT", "TEST_HEAVEN") == "opposed"
        assert gate.alliance_for("CHARITY", "TEST_PIT") == "opposed"

    def test_opposition_outranks_allies_in_a_row(self):
        # a row holding both kin and foe must read opposed (first opposed decides)
        gate = ZoneGate(region_spheres={"MIXED": ["ANIMALS", "CHARITY"]})
        assert gate.alliance_for("BLIGHT", "MIXED") == "opposed"


# --------------------------------------------------------------------------
# portalGate — allied opens (+VirtueMark), opposed refuses, clock rate-limits
# --------------------------------------------------------------------------
class TestPortalGate:
    @staticmethod
    def _gate(clock=None, region_spheres=None):
        gate = ZoneGate(clock=clock, **({"region_spheres": region_spheres} if region_spheres else {}))
        gate.init({"Whispering Woods": "FOREST", "Shining City": "TEST_HEAVEN"})
        return gate

    def test_unjoined_zone_always_open(self):
        gate = self._gate()
        soul = Soul(1, {"Sphere": "BLIGHT"})
        assert gate.portal_gate(soul, "The Endless Stair") is True  # no join, no gate
        assert "VirtueMarks" not in soul.attributes
        assert gate.ledger == []

    def test_allied_zone_opens_and_awards_one_mark_per_buff_window(self):
        now = {"t": 1000}
        gate = self._gate(clock=lambda: now["t"])
        soul = Soul(1, {"Sphere": "NATURE"})
        assert gate.portal_gate(soul, "Whispering Woods") is True
        assert soul.attributes["VirtueMarks"] == 1
        # within BUFF_SECONDS: still open, no second mark
        now["t"] = 1000 + ZoneGate.BUFF_SECONDS - 1
        assert gate.portal_gate(soul, "Whispering Woods") is True
        assert soul.attributes["VirtueMarks"] == 1
        # past the window: exactly one more
        now["t"] = 1000 + ZoneGate.BUFF_SECONDS
        assert gate.portal_gate(soul, "Whispering Woods") is True
        assert soul.attributes["VirtueMarks"] == 2
        # the ledger carries the welcome line, once per award
        welcomes = [e for e in gate.ledger if "welcomes a NATURE soul" in e[1]]
        assert len(welcomes) == 2
        assert all(e[0] == "Basecamp" and e[2] is True for e in welcomes)

    def test_marks_are_per_zone(self):
        now = {"t": 1000}
        gate = self._gate(clock=lambda: now["t"])
        gate.init({"Woods A": "FOREST", "Woods B": "FOREST"})
        soul = Soul(1, {"Sphere": "NATURE"})
        assert gate.portal_gate(soul, "Woods A") is True
        assert gate.portal_gate(soul, "Woods B") is True  # different zone, own window
        assert soul.attributes["VirtueMarks"] == 2

    def test_opposed_zone_refuses(self):
        now = {"t": 1000}
        gate = self._gate(clock=lambda: now["t"],
                          region_spheres={**REGION_SPHERES, "TEST_HEAVEN": ["CHARITY"]})
        soul = Soul(1, {"Sphere": "BLIGHT"})
        assert gate.portal_gate(soul, "Shining City") is False
        assert "VirtueMarks" not in soul.attributes
        refusals = [e for e in gate.ledger if "refuses you" in e[1]]
        assert len(refusals) == 1
        assert refusals[0][0] == "Basecamp" and refusals[0][2] is False
        assert "BLIGHT" in refusals[0][1] and "Shining City" in refusals[0][1]
        # refusal is rate-limited to one ledger line per REFUSAL_SECONDS
        now["t"] = 1000 + ZoneGate.REFUSAL_SECONDS - 1
        assert gate.portal_gate(soul, "Shining City") is False
        assert len([e for e in gate.ledger if "refuses you" in e[1]]) == 1
        now["t"] = 1000 + ZoneGate.REFUSAL_SECONDS
        assert gate.portal_gate(soul, "Shining City") is False
        assert len([e for e in gate.ledger if "refuses you" in e[1]]) == 2

    def test_independent_zone_opens_with_no_effect(self):
        gate = self._gate()
        soul = Soul(1, {"Sphere": "ART"})
        assert gate.portal_gate(soul, "Whispering Woods") is True
        assert "VirtueMarks" not in soul.attributes
        assert gate.ledger == []  # a negative is a fact: no line, no mark

    def test_seeded_soul_walks_the_gate_deterministically(self):
        # end to end: the UserId draw decides the verdict, same every time
        now = {"t": 1000}
        for _ in range(3):
            gate = self._gate(clock=lambda: now["t"])
            soul = Soul(123456)  # golden: DANCE (holds no kin) -> independent
            assert gate.portal_gate(soul, "Whispering Woods") is True
            assert "VirtueMarks" not in soul.attributes


# --------------------------------------------------------------------------
# attach / gateAttr — the t46 replicated verdict + t67 authored join
# --------------------------------------------------------------------------
class TestAttachAndGateAttr:
    def test_gate_attr_sanitizes(self):
        assert gate_attr("Scorching Sands!") == "Gate_Scorching_Sands_"
        assert gate_attr("a_b-c") == "Gate_a_b_c"  # underscore survives on both sides
        assert re.fullmatch(r"Gate_[A-Za-z0-9_]+", gate_attr("weird #zone %x%"))

    def test_attach_stamps_every_joined_zone(self):
        gate = ZoneGate(region_spheres={**REGION_SPHERES, "TEST_HEAVEN": ["CHARITY"]})
        gate.init({"Woods": "FOREST", "City": "TEST_HEAVEN"}, souls=[])
        soul = Soul(1, {"Sphere": "NATURE"})
        gate.attach(soul)
        assert soul.attributes["Gate_Woods"] == "allied"
        assert soul.attributes["Gate_City"] == "independent"  # NATURE vs CHARITY: no kin, no foe
        # a soul pre-seeded with an aligned sphere gets the lock verdict stamped too
        doomed = Soul(2, {"Sphere": "BLIGHT"})
        gate.attach(doomed)
        assert doomed.attributes["Gate_Woods"] == "independent"
        assert doomed.attributes["Gate_City"] == "opposed"

    def test_climb_zone_gets_no_attribute(self):
        gate = ZoneGate()
        gate.init({"Woods": "FOREST"})
        soul = Soul(1)
        gate.attach(soul)
        assert "Gate_Endless_Stair" not in soul.attributes

    def test_external_recorder_receives_ledger_events(self):
        seen = []
        # clock must read past BUFF_SECONDS for the FIRST award (last-buff defaults to 0)
        gate = ZoneGate(clock=lambda: 1000, record=lambda s, place, msg, pos: seen.append((s.user_id, place, pos)))
        gate.init({"Woods": "FOREST"})
        soul = Soul(1, {"Sphere": "NATURE"})
        gate.portal_gate(soul, "Woods")
        assert seen == [(1, "Basecamp", True)]


# --------------------------------------------------------------------------
# Ages — boss kills move the world (Worldgen.ageText)
# --------------------------------------------------------------------------
class TestAges:
    @staticmethod
    def _age(kills: int) -> str:
        w = Worldgen()
        for i in range(kills):
            w.note_boss_kill(f"megabeast {i}")
        return w.age_text()

    def test_progression_and_ordinals(self):
        assert self._age(0) == "The Age of Myth"
        assert self._age(9) == "The Age of Myth"
        assert self._age(10) == "The Age of Heroes"
        assert self._age(19) == "The Age of Heroes"
        assert self._age(20) == "The Age of Legends"
        assert self._age(30) == "the Second Age of Myth"
        assert self._age(50) == "the Second Age of Legends"  # stage 5 -> cycle 1, AGES[2]
        assert self._age(60) == "the Third Age of Myth"      # stage 6 -> cycle 2
        assert self._age(90) == "the Fourth Age of Myth"

    def test_ordinal_caps_at_seventh(self):
        # cycle > len(ORDINALS)-1 clamps to "Seventh" (Luau: min(cycle+1, #ORDINALS))
        assert self._age(7 * 30) == "the Seventh Age of Myth"
        assert self._age(21 * 30) == "the Seventh Age of Myth"

    def test_kill_count_and_log(self):
        w = Worldgen()
        assert w.kill_count() == 0 and w.kill_log == []
        w.note_boss_kill("Grimtal")
        w.note_boss_kill("Vuthrax")
        assert w.kill_count() == 2
        assert w.kill_log == ["Grimtal", "Vuthrax"]


# --------------------------------------------------------------------------
# Forgotten beasts — named from the dwarven lexicon, kinship rows attached
# (Worldgen.forgottenBeast / kinshipLine)
# --------------------------------------------------------------------------
class TestForgottenBeasts:
    def test_golden_beasts(self):
        b = Worldgen().forgotten_beast(SeedRng(42))
        assert b.name == 'alak nicat, "the Ace chain of THUNDER"'
        assert b.sphere == "THUNDER"
        b2 = Worldgen().forgotten_beast(SeedRng(2026))
        assert b2.name == 'ilas nil, "the Absolute hammer of VOLCANOS"'
        assert b2.sphere == "VOLCANOS"

    def test_same_seed_same_beast(self):
        w = Worldgen()
        assert w.forgotten_beast(SeedRng(77)).name == w.forgotten_beast(SeedRng(77)).name

    def test_beast_carries_kinship_rows(self):
        b = Worldgen().forgotten_beast(SeedRng(42))
        assert b.allies == ALLIES["THUNDER"]
        assert b.opposed == OPPOSED["THUNDER"]
        assert w_kinship(b) == "Kin: LIGHT and LIGHTNING. Foes: none."

    def test_kinship_line_negative_is_a_fact(self):
        # VOLCANOS holds no kin and no foes: both halves read "none"
        b = Beast(name="x", sphere="VOLCANOS",
                  allies=list(ALLIES["VOLCANOS"]), opposed=list(OPPOSED["VOLCANOS"]))
        assert w_kinship(b) == "Kin: none. Foes: none."

    def test_forgotten_name_matches_beast(self):
        w = Worldgen()
        assert w.forgotten_name(SeedRng(5)) == w.forgotten_beast(SeedRng(5)).name

    def test_beast_name_shape(self):
        # '%s, "the %s of %s"' — dwarven compound, titled gloss, sourced sphere
        # (dw words carry DF diacritics; glosses may hyphenate: "Awe-inspiring")
        for seed in range(20):
            b = Worldgen().forgotten_beast(SeedRng(seed))
            assert re.fullmatch(r'[^\W\d_]+ [^\W\d_]+, "the [A-Z]\S+ [a-z]\S* of [A-Z]+"', b.name), b.name
            assert b.sphere in SPHERE_SET


def w_kinship(beast: Beast) -> str:
    return Worldgen().kinship_line(beast)
