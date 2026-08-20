"""Campaign engine — state/legal actions first; LLM narrates after.

Schema: mag_game_campaign.v1
Law: engine owns truth; character ask + save check; traits fire tables (CK-lite).
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
from datetime import datetime, timezone
from pathlib import Path
import hashlib
from typing import Any
from uuid import uuid4

from config import ROOT

SCHEMA = "mag_game_campaign.v1"
CAMP_DIR = ROOT / "memory" / "working" / "game_campaigns"
MODULES_DIR = ROOT / "memory" / "game_modules"
CHAR_DIR = ROOT / "memory" / "working" / "game_characters"

_ARCHETYPES = {
    "fighter": {"hp": 12, "hp_max": 12, "ac": 14, "attack_bonus": 4, "damage": "1d8+2"},
    "rogue": {"hp": 10, "hp_max": 10, "ac": 13, "attack_bonus": 5, "damage": "1d6+3"},
    "wizard": {"hp": 8, "hp_max": 8, "ac": 12, "attack_bonus": 3, "damage": "1d10"},
    "cleric": {"hp": 10, "hp_max": 10, "ac": 14, "attack_bonus": 3, "damage": "1d6+1"},
}
_TRAITS = ["greedy", "brave", "craven", "curious", "hotheaded", "cautious", "kind", "cynical"]


def _pals(camp: dict[str, Any]) -> list[dict[str, Any]]:
    return [p for p in (camp.get("pals") or []) if isinstance(p, dict)]


def _pal(camp: dict[str, Any], name: str) -> dict[str, Any] | None:
    n = (name or "").lower()
    for p in _pals(camp):
        if str(p.get("name") or "").lower() == n:
            return p
    return None


def _set_pal(camp: dict[str, Any], pal: dict[str, Any]) -> None:
    name = str(pal.get("name") or "").lower()
    rest = [p for p in _pals(camp) if str(p.get("name") or "").lower() != name]
    if str(pal.get("station") or "") != "fled":
        rest.append(pal)
    camp["pals"] = rest


def _cut_merchant(camp: dict[str, Any], pl: dict[str, Any]) -> str:
    """Palworld catch + XCOM panic. One station. Dice, not a script. He never opens the crate."""
    from mag.game_dice import roll_dice
    flags = list(camp.get("flags") or [])
    if "freed_merchant" in flags:
        return "The rope already fell."
    flags.append("freed_merchant")
    flags.append("freed_merchant_opportunity")
    enc = camp.get("encounter") or {}
    fighting = False
    try:
        fighting = bool(isinstance(enc, dict) and enc.get("name") and int(enc.get("hp") or 0) > 0)
    except (TypeError, ValueError):
        fighting = False
    traits = [str(x).lower() for x in (pl.get("traits") or [])]
    dc = 12
    if fighting:
        dc += 4
    if "kind" in traits:
        dc -= 2
    if "talked_merchant" in flags:
        dc -= 1
    if "brave" in traits:
        dc -= 1
    if "greedy" in traits:
        dc += 1
    roll = int(roll_dice("1d20").get("total") or 10)
    pal = {
        "name": "merchant",
        "race": "human",
        "job": "merchant",
        "traits": ["craven", "cynical"],
        "hp": 6,
        "hp_max": 6,
        "station": "cover",
    }
    if fighting and roll >= dc + 5:
        pal["station"] = "fight"
        pal["traits"] = ["cynical"]
        line = "The rope falls. He snatches a goblin spear. His hands shake. He still will not touch the crate."
    elif roll >= dc:
        pal["station"] = "cover" if fighting else "follow"
        if fighting:
            line = "The rope falls. He crawls behind the crate. Cover. He will not fight. He will not open it."
        else:
            line = "The rope falls. He walks. He still will not open that box."
    elif fighting:
        pal["station"] = "fled"
        flags.append("merchant_fled")
        line = "The rope falls. He runs. Goblins still hold the floor. The crate keeps its wax."
    else:
        pal["station"] = "follow"
        line = "The rope falls. He walks. He still will not open that box."
    camp["flags"] = list(dict.fromkeys(flags))
    _set_pal(camp, pal)
    enc = camp.get("encounter")
    if isinstance(enc, dict) and enc.get("units"):
        for u in enc.get("units") or []:
            if str(u.get("station") or "") == "captive":
                u["station"] = "idle"
                u["job"] = "idle"
                u["aware"] = True
        if fighting:
            _alert_camp(enc)
    try:
        from mag.party_subchain import append as _ps
        _ps(seat="table", ok=True, move="merchant pal " + str(pal.get("station")), kind="pal")
    except Exception:
        pass
    return line


def _pal_in_fight(camp: dict[str, Any], enc: dict[str, Any], events: list[str], pl: dict[str, Any]) -> None:
    """XCOM squad: pal acts from their station. Panic can break cover."""
    pal = _pal(camp, "merchant")
    if not pal:
        return
    from mag.game_dice import roll_dice
    station = str(pal.get("station") or "")
    traits = [str(x).lower() for x in (pal.get("traits") or [])]
    php = int(pl.get("hp") or 0)
    pmax = int(pl.get("hp_max") or 10) or 10
    if station == "cover":
        events.append("The merchant stays behind the crate.")
        if "craven" in traits and php * 2 <= pmax:
            if int(roll_dice("1d20").get("total") or 10) < 10:
                pal["station"] = "fled"
                camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + ["merchant_fled"]))
                _set_pal(camp, pal)
                events.append("He breaks. He is gone.")
        return
    if station == "fight" and enc and int(enc.get("hp") or 0) > 0:
        dmg = int(roll_dice("1d4").get("total") or 1)
        unit = _pick_unit(enc) if enc.get("units") else None
        if unit:
            dead = _hurt_unit(enc, unit, dmg)
            if dead or int(enc.get("hp") or 0) <= 0:
                events.append("His spear drops the " + str(unit.get("name")) + ".")
            else:
                events.append("His spear finds the " + str(unit.get("name")) + ".")
        else:
            enc["hp"] = max(0, int(enc.get("hp") or 0) - dmg)
            if enc["hp"] <= 0:
                events.append("His spear drops one. They fall. The crate is still waxed.")
            else:
                events.append("His spear finds one.")
        if "craven" in (pal.get("traits") or []) and int(roll_dice("1d20").get("total") or 10) < 8:
            pal["station"] = "cover"
            pal["traits"] = ["craven", "cynical"]
            _set_pal(camp, pal)
            events.append("He ducks back behind the crate.")



def _task_ahead(camp: dict[str, Any]) -> str:
    flags = " ".join(str(f) for f in (camp.get("flags") or [])).lower()
    if "talked_merchant" in flags or "freed_merchant" in flags:
        return "crate"
    return "captive"


_STATION_LINE = {
    "crate": "at the crate",
    "captive": "at the rope",
    "mouth": "at the way out",
    "dice": "dice by the pillars",
    "sleep": "asleep on a claw-mark",
    "idle": "where the rope was",
}


def _sync_band(enc: dict[str, Any]) -> dict[str, Any]:
    units = [u for u in (enc.get("units") or []) if int(u.get("hp") or 0) > 0]
    enc["units"] = units
    enc["hp"] = sum(int(u.get("hp") or 0) for u in units)
    if units:
        enc["hp_max"] = max(int(enc.get("hp_max") or 0), sum(int(u.get("hp_max") or 0) for u in units))
    if not units:
        enc["hp"] = 0
    init = [x for x in (enc.get("init") or []) if x == "you" or x == "merchant" or any(str(u.get("name")) == x for u in units)]
    if init:
        enc["init"] = init
        enc["whose"] = int(enc.get("whose") or 0) % len(init)
    return enc


def _roll_init(camp: dict[str, Any], enc: dict[str, Any]) -> None:
    from mag.game_dice import roll_dice
    order: list[tuple[str, int]] = []
    pl = camp.get("player") or {}
    traits = [str(x).lower() for x in (pl.get("traits") or [])]
    you = int(roll_dice("1d20").get("total") or 10)
    if "cautious" in traits:
        you += 2
    if "hotheaded" in traits:
        you -= 1
    if str(pl.get("archetype") or "").lower() == "rogue":
        you += 3
    order.append(("you", you))
    pal = _pal(camp, "merchant")
    if pal and str(pal.get("station") or "") == "fight":
        order.append(("merchant", int(roll_dice("1d20").get("total") or 8)))
    for u in enc.get("units") or []:
        bonus = 4 if u.get("aware") else -4
        order.append((str(u.get("name")), int(roll_dice("1d20").get("total") or 10) + bonus))
    order.sort(key=lambda x: -x[1])
    enc["init"] = [n for n, _ in order]
    enc["whose"] = 0


def _ensure_band(camp: dict[str, Any]) -> dict[str, Any] | None:
    enc = camp.get("encounter")
    if not isinstance(enc, dict) or int(enc.get("hp") or 0) <= 0:
        return enc if isinstance(enc, dict) else None
    if enc.get("units"):
        _sync_band(enc)
        if not enc.get("init"):
            _roll_init(camp, enc)
        camp["encounter"] = enc
        return enc
    from mag.game_dice import roll_dice
    n = max(3, min(5, 2 + int(roll_dice("1d3").get("total") or 2)))
    ahead = _task_ahead(camp)
    jobs = [ahead]
    for j in ("captive", "crate", "mouth", "dice", "sleep"):
        if j not in jobs:
            jobs.append(j)
        if len(jobs) >= n:
            break
    names = {
        "crate": "crate-guard",
        "captive": "rope-guard",
        "mouth": "mouth-guard",
        "dice": "dice-goblin",
        "sleep": "sleeper",
    }
    units = []
    for i, st in enumerate(jobs[:n]):
        aware = st not in ("dice", "sleep")
        units.append({
            "id": "g" + str(i + 1),
            "name": names.get(st, "goblin"),
            "race": "goblin",
            "job": st,
            "station": st,
            "hp": 3 if st == "sleep" else 4,
            "hp_max": 3 if st == "sleep" else 4,
            "ac": 15 if aware else 12,
            "attack_bonus": 4 if aware else 1,
            "damage": "1d6+2" if aware else "1d4",
            "speed": 10 if aware else 4,
            "ct": 0,
            "aware": aware,
        })
    enc["units"] = units
    _roll_init(camp, enc)
    _sync_band(enc)
    camp["encounter"] = enc
    return enc


def _camp_look(camp: dict[str, Any]) -> str:
    enc = _ensure_band(camp)
    if not enc or int(enc.get("hp") or 0) <= 0:
        return ""
    units = enc.get("units") or []
    n = len(units)
    bits = [str(n) + (" goblins." if n != 1 else " goblin.")]
    for u in units:
        bits.append("One " + _STATION_LINE.get(str(u.get("station") or ""), "in the dark") + ".")
    return " ".join(bits)


def _pick_unit(enc: dict[str, Any], target: str = "") -> dict[str, Any] | None:
    units = [u for u in (enc.get("units") or []) if int(u.get("hp") or 0) > 0]
    if not units:
        return None
    t = (target or "").lower()
    for u in units:
        blob = " ".join([str(u.get("name") or ""), str(u.get("station") or ""), str(u.get("job") or "")]).lower()
        if t and t in blob:
            return u
    aware = [u for u in units if u.get("aware")]
    return (aware or units)[0]


def _hurt_unit(enc: dict[str, Any], unit: dict[str, Any], dmg: int) -> bool:
    unit["hp"] = max(0, int(unit.get("hp") or 0) - int(dmg))
    dead = int(unit["hp"]) <= 0
    _sync_band(enc)
    return dead


def _goblin_strike(camp: dict[str, Any], unit: dict[str, Any], pl: dict[str, Any], events: list[str]) -> None:
    from mag.game_dice import roll_dice
    if not unit.get("aware"):
        unit["aware"] = True
        unit["ac"] = 15
        unit["speed"] = 10
        events.append("The " + str(unit.get("name")) + " wakes.")
        return
    hit = roll_dice("1d20+" + str(int(unit.get("attack_bonus") or 0)))
    if int(hit.get("total") or 0) >= int(pl.get("ac") or 10):
        fdmg = roll_dice(str(unit.get("damage") or "1d6"))
        dealt = int(fdmg.get("total") or 1)
        pmax = int(pl.get("hp_max") or pl.get("hp") or 10)
        pl["hp"] = max(0, int(pl.get("hp") or 0) - dealt)
        if pl["hp"] <= 0:
            camp["status"] = "defeated"
            events.append("The " + str(unit.get("name")) + " drops you.")
        else:
            events.append("The " + str(unit.get("name")) + " hits. " + _wound_look(int(pl["hp"]), pmax, "you"))
    else:
        events.append("The " + str(unit.get("name")) + " misses.")


def _resolve_ticks(camp: dict[str, Any], events: list[str], pl: dict[str, Any]) -> None:
    enc = camp.get("encounter")
    if not isinstance(enc, dict) or int(enc.get("hp") or 0) <= 0:
        return
    init = [x for x in (enc.get("init") or ["you"]) if x]
    if not init:
        return
    try:
        you_i = init.index("you")
    except ValueError:
        you_i = 0
    enc["whose"] = (you_i + 1) % len(init)
    for _ in range(len(init)):
        enc = camp.get("encounter")
        if not isinstance(enc, dict) or int(enc.get("hp") or 0) <= 0:
            return
        init = [x for x in (enc.get("init") or ["you"]) if x]
        if not init:
            return
        whose = int(enc.get("whose") or 0) % len(init)
        who = init[whose]
        if who == "you":
            return
        if who == "merchant":
            _pal_in_fight(camp, enc, events, pl)
        else:
            unit = next((u for u in (enc.get("units") or []) if str(u.get("name")) == who and int(u.get("hp") or 0) > 0), None)
            if unit:
                _goblin_strike(camp, unit, pl, events)
                if camp.get("status") == "defeated":
                    return
        init = [x for x in ((camp.get("encounter") or {}).get("init") or init) if x]
        if not init:
            return
        enc = camp.get("encounter") or enc
        enc["whose"] = (int(enc.get("whose") or 0) + 1) % len(init)


def _sneak_to(camp: dict[str, Any], pl: dict[str, Any]) -> tuple[bool, str]:
    from mag.game_dice import roll_dice
    enc = _ensure_band(camp)
    flags = list(camp.get("flags") or [])
    if "near:merchant" in flags:
        return True, "You are already at the rope."
    traits = [str(x).lower() for x in (pl.get("traits") or [])]
    arch = str(pl.get("archetype") or "").lower()
    dc = 10
    units = (enc or {}).get("units") or []
    if any(u.get("station") == "captive" and u.get("aware") for u in units):
        dc += 2
    if any(u.get("station") == "mouth" and u.get("aware") for u in units):
        dc += 1
    if enc and enc.get("alert"):
        dc += 4
    dc += min(3, max(0, int((enc or {}).get("rope_tug") or 0) - 1))
    dc -= sum(1 for u in units if not u.get("aware"))
    if arch == "rogue":
        dc -= 3
    if "cautious" in traits:
        dc -= 2
    if "craven" in traits:
        dc -= 1
    if "hotheaded" in traits:
        dc += 2
    roll = int(roll_dice("1d20").get("total") or 10)
    if roll >= dc:
        camp["flags"] = list(dict.fromkeys(flags + ["near:merchant"]))
        return True, "You reach the rope. The camp does not look up."
    _alert_camp(enc)
    return False, "A goblin hisses. The camp knows you."



_JOB_LINES = {
    "captive": [
        "The rope-guard tugs the knot.",
        "The rope-guard works the knot.",
        "The knot bites. He does not look up.",
    ],
    "crate": [
        "The crate-guard does not touch the wax.",
        "The crate-guard shifts his weight. The seal holds.",
        "He looks at the crate. He does not open it.",
    ],
    "mouth": [
        "The mouth-guard watches the way you came.",
        "The mouth-guard spits into the dark.",
        "The way out is still his.",
    ],
    "dice": [
        "Dice click. They are not looking.",
        "A curse at the bones. Still not looking.",
        "The dice go still. Then again.",
    ],
    "sleep": [
        "A goblin snores on a claw-mark.",
        "The sleeper rolls. The claw-mark stays.",
        "Wet leather breath. Still asleep.",
    ],
    "idle": [
        "He stares at the empty ring.",
        "He has nothing to hold.",
        "The rope is gone. He is still here.",
    ],
}


def _job_say(st: str, enc: dict[str, Any]) -> str:
    opts = _JOB_LINES.get(st) or []
    if not opts:
        return ""
    if st == "captive":
        i = min(len(opts) - 1, max(0, int(enc.get("rope_tug") or 1) - 1))
        return opts[i]
    tick = int(enc.get("tick") or 1)
    return opts[(tick - 1) % len(opts)]


def _alert_camp(enc: dict[str, Any] | None) -> None:
    if not isinstance(enc, dict):
        return
    enc["alert"] = True
    for u in enc.get("units") or []:
        u["aware"] = True
        u["ac"] = 15
        u["speed"] = 10


def _camp_tick(camp: dict[str, Any], events: list[str], speak: bool = True) -> None:
    """Infocom CLOCKER. One job in the light. Never the same line twice running."""
    enc = _ensure_band(camp)
    if not enc or int(enc.get("hp") or 0) <= 0:
        return
    if enc.get("alert"):
        return
    enc["tick"] = int(enc.get("tick") or 0) + 1
    units = enc.get("units") or []
    for u in units:
        if str(u.get("station") or "") == "captive":
            enc["rope_tug"] = int(enc.get("rope_tug") or 0) + 1
    n = len(units)
    if not n:
        return
    last = enc.get("last_tick_line")
    idx = (int(enc.get("tick") or 1) - 1) % n
    line = ""
    for off in range(n):
        u = units[(idx + off) % n]
        cand = _job_say(str(u.get("station") or ""), enc)
        if cand and cand != last:
            line = cand
            break
    if not line:
        line = _job_say(str(units[idx].get("station") or ""), enc)
    enc["last_tick_line"] = line
    if speak and line:
        events.append(line)



def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _cid() -> str:
    return "gc-" + uuid4().hex[:10]


def list_modules() -> list[dict[str, Any]]:
    out = []
    if not MODULES_DIR.is_dir():
        return out
    for p in MODULES_DIR.glob("*.json"):
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
            out.append(
                {
                    "module_id": m.get("module_id") or p.stem,
                    "title": m.get("title"),
                    "aliases": m.get("aliases") or [],
                    "path": str(p.relative_to(ROOT)).replace("\\", "/"),
                }
            )
        except Exception:
            continue
    return out


def resolve_module(name: str) -> dict[str, Any] | None:
    q = (name or "classic").strip().lower()
    for p in MODULES_DIR.glob("*.json"):
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        mid = str(m.get("module_id") or "").lower()
        aliases = [str(a).lower() for a in (m.get("aliases") or [])]
        title = str(m.get("title") or "").lower()
        if q == mid or q in aliases or any(q in a or a in q for a in aliases) or q in title:
            return m
    classic = MODULES_DIR / "dnd_classic_stub.v1.json"
    if classic.is_file():
        return json.loads(classic.read_text(encoding="utf-8"))
    return None


def _path(campaign_id: str) -> Path:
    return CAMP_DIR / f"{campaign_id}.json"


def load_campaign(campaign_id: str) -> dict[str, Any] | None:
    p = _path(campaign_id)
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_campaign(camp: dict[str, Any]) -> Path:
    CAMP_DIR.mkdir(parents=True, exist_ok=True)
    camp["updated"] = _utc()
    p = _path(str(camp["campaign_id"]))
    p.write_text(json.dumps(camp, indent=2, default=str), encoding="utf-8")
    return p


def latest_for_session(session_id: str) -> dict[str, Any] | None:
    if not CAMP_DIR.is_dir() or not session_id:
        return None
    best, best_ts = None, ""
    for p in CAMP_DIR.glob("gc-*.json"):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(c.get("voice_session_id") or "") != session_id:
            continue
        if c.get("status") not in ("active", "awaiting_character", "paused"):
            continue
        ts = str(c.get("updated") or c.get("ts") or "")
        if ts >= best_ts:
            best_ts, best = ts, c
    return best


def latest_any() -> dict[str, Any] | None:
    """Most recently updated live campaign, session-agnostic. Desk mounts this, not a void."""
    if not CAMP_DIR.is_dir():
        return None
    best, best_ts = None, ""
    for pth in CAMP_DIR.glob("gc-*.json"):
        try:
            c = json.loads(pth.read_text(encoding="utf-8"))
        except Exception:
            continue
        if c.get("status") not in ("active", "awaiting_character", "paused"):
            continue
        ts = str(c.get("updated") or c.get("ts") or "")
        try:
            mtime = str(pth.stat().st_mtime)
        except OSError:
            mtime = ""
        key = ts or mtime
        if key >= str(best_ts):
            best_ts, best = key, c
    return best


def parse_character(text: str) -> dict[str, Any] | None:
    """Parse 'I'm Ash a greedy fighter' or 'random classic'."""
    t = (text or "").strip()
    if not t:
        return None
    low = t.lower()
    if re.search(r"\b(random|classic character|surprise me)\b", low):
        arch = random.choice(list(_ARCHETYPES.keys()))
        traits = random.sample(_TRAITS, 2)
        name = random.choice(["Ash", "Brynn", "Corin", "Dax", "Elra", "Fenn"])
        base = dict(_ARCHETYPES[arch])
        return {
            "name": name,
            "archetype": arch,
            **base,
            "traits": traits,
            "inventory": ["torch", "rations"],
        }
    # name patterns
    name = None
    m = re.search(
        r"\b(?:i(?:'m| am)|call me|name(?:'s| is)|play as)\s+([A-Za-z][A-Za-z'-]{1,20})",
        t,
        re.I,
    )
    if m:
        name = m.group(1)
    # Tavern Brawler (5e feat kit) — preferred for brawl dogfood
    # Do not treat leading word "tavern" as character name.
    if re.search(r"\btavern\s*brawler\b", low):
        from mag.game_brawl import tavern_brawler_sheet

        bad_names = {
            "tavern",
            "brawler",
            "the",
            "a",
            "an",
            "with",
            "fighter",
            "adventurer",
        }
        nm = name if name and name.lower() not in bad_names else "Ash"
        # "I'm Brynn a tavern brawler"
        m_nm = re.search(
            r"\b(?:i(?:'m| am)|call me|name(?:'s| is)|play as)\s+([A-Za-z][A-Za-z'-]{1,20})",
            t,
            re.I,
        )
        if m_nm and m_nm.group(1).lower() not in bad_names:
            nm = m_nm.group(1)
        traits_tb = [tr for tr in _TRAITS if tr in low] or ["hotheaded", "brave"]
        sheet = tavern_brawler_sheet(nm, traits=traits_tb[:3])
        # pick up gear words into inventory
        inv = list(sheet.get("inventory") or [])
        if re.search(r"\b(axe|hatchet)\b", low) and "axe" not in inv:
            inv.append("axe")
        if re.search(r"\b(mug|ale|tankard)\b", low) and "mug" not in inv:
            inv.append("mug of ale")
        sheet["inventory"] = inv
        return {k: v for k, v in sheet.items() if k not in ("id", "is_player", "faction", "ai")}
    if not name:
        m2 = re.match(r"^([A-Za-z][A-Za-z'-]{1,20})\b", t)
        if m2 and m2.group(1).lower() not in (
            "the",
            "go",
            "i",
            "a",
            "an",
            "tavern",
            "play",
        ):
            name = m2.group(1)

    arch = "fighter"
    for a in _ARCHETYPES:
        if a in low:
            arch = a
            break
    if "rogue" in low or "thief" in low:
        arch = "rogue"
    if "mage" in low or "wizard" in low:
        arch = "wizard"
    if "cleric" in low or "priest" in low:
        arch = "cleric"
    traits = [tr for tr in _TRAITS if tr in low]
    if not traits:
        traits = ["brave"]
    if not name and not re.search(r"\b(fighter|rogue|wizard|cleric|greedy|brave|tavern)\b", low):
        return None
    if not name:
        name = "Adventurer"
    base = dict(_ARCHETYPES[arch])
    return {
        "name": name[:40],
        "archetype": arch,
        **base,
        "traits": traits[:3],
        "inventory": ["torch", "rations"],
    }


def begin_play(
    *,
    module_id: str = "classic",
    voice_session_id: str = "",
    force_new: bool = False,
) -> dict[str, Any]:
    """Save check → resume or await character / start."""
    if not force_new and voice_session_id:
        existing = latest_for_session(voice_session_id)
        if existing and existing.get("status") in ("active", "paused"):
            if existing.get("status") == "paused":
                existing["status"] = "active"
                save_campaign(existing)
            return {
                "ok": True,
                "resumed": True,
                "campaign": existing,
                "speak": (
                    f"Resuming {existing.get('module_title')}: "
                    f"{(existing.get('player') or {}).get('name')} "
                    f"in {_room(existing).get('name')}. "
                    f"HP {(existing.get('player') or {}).get('hp')}/"
                    f"{(existing.get('player') or {}).get('hp_max')}. "
                    f"Say an action: go north, attack, look, help…"
                ),
                "legal": list_legal_actions(existing),
                "scene_context": scene_context(existing),
            }
        if existing and existing.get("status") == "awaiting_character":
            starter = ((existing.get("module_snapshot") or {}).get("player_start") or {})
            if starter.get("name"):
                seated = set_character(str(existing.get("campaign_id")), dict(starter))
                camp2 = load_campaign(str(existing.get("campaign_id"))) or existing
                return {
                    "ok": True,
                    "resumed": False,
                    "need_character": False,
                    "campaign_id": camp2.get("campaign_id"),
                    "campaign": camp2,
                    "speak": seated.get("speak") or (
                        f"Starting {camp2.get('module_title')}. "
                        f"You are {starter.get('name')} the {starter.get('archetype')}."
                    ),
                    "legal": list_legal_actions(camp2),
                    "scene_context": scene_context(camp2),
                }
            return {
                "ok": True,
                "need_character": True,
                "campaign_id": existing.get("campaign_id"),
                "speak": (
                    "Campaign ready. Who are you? "
                    "Say e.g. I'm Ash a greedy fighter — or random classic."
                ),
            }

    mod = resolve_module(module_id)
    if not mod:
        return {"ok": False, "error": "no module", "modules": list_modules()}

    cid = _cid()
    camp = {
        "schema": SCHEMA,
        "campaign_id": cid,
        "ts": _utc(),
        "voice_session_id": voice_session_id or "",
        "module_id": mod.get("module_id"),
        "module_title": mod.get("title"),
        "status": "awaiting_character",
        "room_id": mod.get("start_room"),
        "player": None,
        "encounter": None,
        "flags": [],
        "storyteller": {"threat_budget": 2, "days_since_crisis": 0},
        "log": [{"ts": _utc(), "type": "init", "text": f"Module {mod.get('title')} loaded"}],
        "module_snapshot": {
            "rooms": mod.get("rooms") or {},
            "event_tables": mod.get("event_tables") or {},
            "license_note": mod.get("license_note"),
            "player_start": mod.get("player_start") or {},
        },
    }
    save_campaign(camp)
    starter = mod.get("player_start") or {}
    if starter.get("name"):
        seated = set_character(cid, dict(starter))
        camp2 = load_campaign(cid) or camp
        return {
            "ok": True,
            "resumed": False,
            "need_character": False,
            "campaign_id": cid,
            "campaign": camp2,
            "speak": seated.get("speak") or (
                f"Starting {mod.get('title')}. "
                f"You are {starter.get('name')} the {starter.get('archetype')} "
                f"in {_room(camp2).get('name')}."
            ),
            "legal": list_legal_actions(camp2),
            "scene_context": scene_context(camp2),
        }
    return {
        "ok": True,
        "resumed": False,
        "need_character": True,
        "campaign_id": cid,
        "campaign": camp,
        "speak": (
            f"Starting {mod.get('title')}. Who are you playing? "
            "Name and class/vibe — or say random classic."
        ),
    }


def set_character(campaign_id: str, player: dict[str, Any]) -> dict[str, Any]:
    camp = load_campaign(campaign_id)
    if not camp:
        return {"ok": False, "error": "missing campaign"}
    camp["player"] = player
    camp["status"] = "active"
    start = camp.get("room_id")
    rooms = (camp.get("module_snapshot") or {}).get("rooms") or {}
    room = rooms.get(start) or {}
    enc = room.get("encounter")
    if enc:
        camp["encounter"] = dict(enc)
    camp["log"] = list(camp.get("log") or []) + [
        {
            "ts": _utc(),
            "type": "character",
            "text": f"{player.get('name')} the {player.get('archetype')} "
            f"({', '.join(player.get('traits') or [])}) enters the road.",
        }
    ]
    # persist character sheet
    try:
        CHAR_DIR.mkdir(parents=True, exist_ok=True)
        cp = CHAR_DIR / f"{re.sub(r'[^a-z0-9]+', '-', str(player.get('name') or 'x').lower())}.json"
        cp.write_text(
            json.dumps({"player": player, "campaign_id": campaign_id, "ts": _utc()}, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass
    save_campaign(camp)
    sc = scene_context(camp)
    speak = f"Playing {player.get('name')} the {player.get('archetype')}. " + _narrate_room(camp)
    try:
        from mag.game_passage import narrate_passage, room_meta_from_camp

        pas = narrate_passage(
            sc,
            room_meta=room_meta_from_camp(camp),
            full=True,
            use_llm=True,
            last_action="arrive",
        )
        if pas.get("text"):
            speak = f"Playing {player.get('name')} the {player.get('archetype')}.\n\n" + str(
                pas["text"]
            )
    except Exception:
        pass
    return {
        "ok": True,
        "campaign": camp,
        "speak": speak,
        "legal": list_legal_actions(camp),
        "scene_context": sc,
    }


def _room(camp: dict[str, Any]) -> dict[str, Any]:
    rid = camp.get("room_id")
    return (camp.get("module_snapshot") or {}).get("rooms", {}).get(rid) or {}




def _rashomon_voice(who: str) -> str:
    """FILE voice from the tavern bar-fight seed. Engine_truth stays the ledger."""
    from config import ROOT as _R
    path = _R / "memory" / "narrative_corpus" / "rashomon" / "tavern_bar_fight_party.v1.md"
    if not path.is_file():
        return ""
    body = path.read_text(encoding="utf-8", errors="replace")
    key = "## Perspective: " + who
    if key not in body:
        return ""
    rest = body.split(key, 1)[1]
    rest = rest.split("\n", 1)[1] if "\n" in rest else rest
    chunk = rest.split("## Perspective:", 1)[0].strip()
    return " ".join(chunk.split())[:360]


def _donjon_sense(camp: dict[str, Any]) -> str:
    """Donjon constraint: one sensory atom, hashed to the room, no new geography."""
    try:
        from mag.narrative_engine import SENSORY_TABLES
    except Exception:
        return ""
    room = _room(camp)
    tags = [str(x).lower() for x in (room.get("tags") or [])]
    if "tavern" in tags or "hub" in tags or room.get("area_tag") == "hub":
        return ""
    rid = str(camp.get("room_id") or room.get("id") or "room")
    kind = "sight"
    rows = list(SENSORY_TABLES.get(kind) or SENSORY_TABLES.get("sight") or [])
    if not rows:
        return ""
    i = int(hashlib.sha256(("donjon:" + rid + ":" + kind).encode()).hexdigest()[:8], 16) % len(rows)
    return str(rows[i])



def _adjacent_memory(keys: list[str]) -> list[str]:
    """Single recall surface: verkle_lance.trace. Themes only — session_ids are theater."""
    lines: list[str] = []
    try:
        from mag.verkle_lance import trace
    except Exception:
        return lines
    for key in keys:
        try:
            r = trace(str(key), limit=4)
        except Exception:
            continue
        if not r.get("found"):
            continue
        for m in r.get("matches") or []:
            theme = str(m.get("theme") or "")
            low = theme.lower()
            if not theme or "steal_pack" in low or "rib_bus_" in low:
                continue
            if theme not in lines:
                lines.append(theme)
            if len(lines) >= 6:
                return lines
    return lines


def _rib_babel_speech() -> str:
    """Plain speech from memory/rib_bus/babelfish-turtles.json. No hashes, no filenames."""
    path = ROOT / "memory" / "rib_bus" / "babelfish-turtles.json"
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    for rec in (data.get("ribs") or {}).values():
        inv = str(rec.get("invariant") or "").strip()
        if not inv:
            continue
        body = inv.split(":", 1)[-1].strip() if ":" in inv[:90] else inv
        body = re.sub(r"\([^)]*self_loop[^)]*\)", "", body)
        body = re.sub(r"\bfish_ear\b", "fish", body)
        body = re.sub(r"\s+\.", ".", body)
        return " ".join(body.split())
    return ""


def _player_signal(text: str, *, source: str) -> str:
    """percolator.partition: SIGNAL vs THEATER vs NOISE. steal_pack / rib_bus_ never narrate."""
    raw = (text or "").strip()
    if not raw:
        return ""
    kept: list[str] = []
    try:
        from mag.percolator import partition
        part = partition(raw, source=source)
        for row in part.get("signal") or []:
            sent = str(row.get("sentence") or "").strip()
            low = sent.lower()
            if not sent or "steal_pack" in low or "rib_bus_" in low:
                continue
            kept.append(sent)
    except Exception:
        kept = []
    if not kept:
        kept = [
            s.strip()
            for s in re.split(r"(?<=[.!?])\s+", raw)
            if s.strip() and "steal_pack" not in s.lower() and "rib_bus_" not in s.lower()
        ]
    return " ".join(kept).strip()



def _trial_from_lance(goal: str) -> str:
    """ghost_memlance.select: the quest is naming the grounded tool. Two strokes, then wait."""
    try:
        from mag.ghost_memlance import select
        picked = select(goal, k=6)
    except Exception:
        return ""
    strokes: list[str] = []
    for s in picked.get("selected") or []:
        if not s.get("verified"):
            continue
        raw = str(s.get("excerpt") or "")
        # drop markdown chrome; keep operator bytes
        keep: list[str] = []
        for ln in raw.splitlines():
            t = ln.strip()
            if not t or t.startswith("#") or t.startswith("**Schema") or t.startswith("**Scope"):
                continue
            t = re.sub(r"^\*\*[^*]+\*\*:\s*", "", t)
            t = t.strip("\"'")
            if t:
                keep.append(t)
        body = " ".join(keep)
        body = _player_signal(body, source="memlance") or body
        body = " ".join(body.split())
        if len(body) < 24:
            continue
        # first sentence only — Positronick: two strokes
        sent = re.split(r"(?<=[.!?])\s+", body)[0].strip()
        if sent and sent not in strokes:
            strokes.append(sent.rstrip(".") + ".")
        if len(strokes) >= 2:
            break
    if not strokes:
        return ""
    return " ".join(strokes) + " What do you do?"


def _invariant_talk(target: str, camp: dict[str, Any]) -> list[str] | None:
    """If the target is an invariant-NPC, voice the principle they embody (the doctrine made flesh).
    Returns narration events, or None if the target isn't one."""
    try:
        from mag import invariant_npcs
        per = invariant_npcs.resolve(target)
        if not per:
            return None
        room = _room(camp)
        scene = f"{room.get('name')}. {room.get('desc')}".strip()
        r = invariant_npcs.talk(per["name"], scene=scene, history=camp.get("log") or [])
        text = r.get("reply") or per.get("soul") or ""
        return [str(text).strip() or str(per.get("soul") or per["name"])]
    except Exception:
        return None


def _talk_calcifer(camp: dict[str, Any]) -> str:
    """One fire elemental. Mira lantern hearth only. Never play-text doctrine."""
    room = _room(camp)
    rid = str(camp.get("room_id") or room.get("id") or "").lower()
    if "lantern" not in rid and "tavern" not in rid:
        return ""
    line = "The hearth pops. You named him Calcifer."
    return _player_signal(line, source="calcifer") or line


def _look_at(camp: dict[str, Any], noun: str) -> str:
    """Examine one thing in the room. Bytes already on the lantern, not a new throne."""
    room = _room(camp)
    n = (noun or "").strip().lower()
    if n.startswith(("the ", "a ", "an ")):
        n = n.split(" ", 1)[-1]
    desc = str(room.get("desc") or "")
    hooks = [str(h) for h in (room.get("hooks") or [])]
    if n in ("calcifer",):
        rid = str(camp.get("room_id") or room.get("id") or "").lower()
        if "lantern" in rid or "tavern" in rid:
            return "The hearth. You named him Calcifer."
        return "He is in Mira's hearth. Not here."
    if n in ("fire", "hearth", "flame"):
        rid = str(camp.get("room_id") or room.get("id") or "").lower()
        if "lantern" in rid or "tavern" in rid:
            return "The hearth. You named him Calcifer."
        return "A fire. Ordinary."
    if n in ("goblin", "goblins", "band", "camp", "them", "guards"):
        return _camp_look(camp) or "No camp here."
    if n in ("dice", "dice-goblin"):
        return "Bone dice. They are not looking at you."
    if n in ("sleeper",):
        return "Asleep on a claw-mark. Breath like wet leather."
    if n in ("rope-guard", "crate-guard", "mouth-guard"):
        enc = camp.get("encounter") if isinstance(camp.get("encounter"), dict) else {}
        u = _pick_unit(enc, n)
        if u:
            return "One " + _STATION_LINE.get(str(u.get("station") or ""), "in the dark") + "."
        return _camp_look(camp) or "No camp here."
    if n in ("stubs", "stub"):
        return "Blackened nubs in the rock. The fire is gone. Something small still uses this dark."
    if n in ("hand", "hands", "inventory", "bag", "bags", "pocket", "pockets"):
        inv = [str(x) for x in ((camp.get("player") or {}).get("inventory") or []) if x]
        if not inv:
            return "Empty hands."
        return "In hand: " + ", ".join(inv) + "."
    if n in ("mug", "tankard", "glass"):
        return "The same mug. Mira polishes it like a debt she can finish."
    if "stranger" in n:
        return (
            "The stranger did not stand when the mug broke. "
            "Broth still steaming. Three windows in three mouths. "
            "Keep smoke is a rumor they will not settle."
        )
    if n in ("barkeep", "mira", "bartender"):
        return (
            "Mira polishes the mug like a debt she can finish. "
            "Keep politics does not pour ale."
        )
    if n in ("door", "road"):
        return "Door to the road. The weather is on the other side of it."
    if n in ("stairs", "rooms"):
        return "Stairs up to rooms. The boards remember wet wool."
    if n in ("cart", "wagon", "tracks"):
        hit = next((h for h in hooks if "cart" in h.lower() or "track" in h.lower()), "")
        return hit or "Mixed tracks. An overturned cart. Blood, no bodies."
    if n in ("gate", "gates", "gatehouse"):
        return desc or "Iron-bound gates. The keep is the building that appeared."
    if n in ("raven", "ravens"):
        return "Raven calls. They already know the chimney is wrong."
    if n in ("chimney", "keep", "smoke", "weather"):
        hit = next((h for h in hooks if "chimney" in h.lower() or h.lower().startswith("rumor")), "")
        if hit.lower().startswith("rumor"):
            hit = hit.split(":", 1)[-1].strip()
        return hit or "The keep chimney. Wrong smoke for this weather."
    if n in ("chair", "table", "tables", "rings"):
        return "Sticky tables. Wet rings. Someone has been mapping them and will not look up."
    if n in ("torch", "rations", "coins"):
        return "You are carrying that."
    if n in ("merchant", "captive", "prisoner"):
        hit = next((h for h in hooks if any(w in h.lower() for w in ("merchant", "captive", "prisoner"))), "")
        body = hit.split(":", 1)[-1].strip() if hit else ""
        return body or "A captive merchant, still bound. The keep's business did not end at the gate."
    if n in ("rope",):
        blob = " ".join([str(room.get("name") or ""), str(room.get("desc") or ""), " ".join(hooks)]).lower()
        if "captive" in blob or "merchant" in blob or "rope" in blob:
            return (
                "The rope has worn a ring in his wrist. "
                "Cut it and he walks. He still will not open the box."
            )
        return "No rope here."
    if n in ("crate", "chest", "seal", "box", "puzzle-box", "puzzlebox", "puzzle"):
        blob = " ".join([str(room.get("name") or ""), str(room.get("desc") or ""), " ".join(hooks)]).lower()
        if not re.search(r"\b(crate|chest|seal|box|ward)\b", blob):
            return "The box is not in this room."
        hit = next((h for h in hooks if any(w in h.lower() for w in ("crate", "seal", "chest", "box"))), "")
        body = hit.split(":", 1)[-1].strip() if hit else ""
        opened = any(str(f).startswith("temple:") or str(f).startswith("shared:") or str(f).startswith("slain:") for f in (camp.get("flags") or []))
        if not opened:
            if n == "seal":
                return "The keep's mark in the wax. A name you have not spoken."
            return (
                "Wood, wax, the keep's mark. "
                "A closed thing remembers the tool that was missing when it was shut."
            )
        return body or "The box is open. The ward has a name now."
    if n:
        try:
            from mag.verkle_lance import trace
            trace(n, limit=2)
        except Exception:
            pass
        for h in hooks:
            if n in h.lower():
                return h
        if n in desc.lower():
            for sent in re.split(r"(?<=[.!?])\s+", desc):
                if n in sent.lower():
                    return sent
            return desc
    return "Nothing called " + noun + " stands out."


def _hook_body(s: str) -> str:
    t = str(s or "").strip()
    if not t:
        return ""
    if t.lower().startswith(("rumor", "quest", "hook")) and ":" in t[:28]:
        t = t.split(":", 1)[-1].strip()
    elif ":" in t[:28]:
        head, rest = t.split(":", 1)
        if head.strip().replace(" ", "").isalpha() and len(head.strip()) < 24:
            t = rest.strip()
    return t


def _lookables(room: dict[str, Any]) -> list[str]:
    blob = " ".join([
        str(room.get("name") or ""),
        str(room.get("desc") or ""),
        " ".join(str(h) for h in (room.get("hooks") or [])),
        " ".join(str(x) for x in (room.get("loot") or [])),
    ]).lower()
    nouns = (
        "crate", "seal", "merchant", "captive", "torch", "fire",
        "cart", "gate", "mug", "stranger", "chest", "tracks",
    )
    out: list[str] = []
    for n in nouns:
        if n in blob and n not in out:
            out.append(n)
    return out[:6]


def _takeables(camp: dict[str, Any]) -> list[str]:
    room = _room(camp)
    inv = [str(x).lower() for x in ((camp.get("player") or {}).get("inventory") or [])]
    loot = [str(x) for x in (room.get("loot") or [])]
    out: list[str] = []
    for x in loot:
        if x and x.lower() not in inv and x.lower() not in [o.lower() for o in out]:
            out.append(x)
    blob = " ".join([str(room.get("desc") or ""), " ".join(str(h) for h in (room.get("hooks") or []))]).lower()
    if "crate" in blob and "crate" not in inv and "crate" not in [o.lower() for o in out]:
        out.append("crate")
    return out[:4]


def story_so_far(camp: dict[str, Any]) -> str:
    """Legend of the run. Start near the end. The sim already happened."""
    if not camp:
        return ""
    pl = camp.get("player") or {}
    who = str(pl.get("name") or "You")
    room = _room(camp)
    here = str(room.get("name") or camp.get("room_id") or "somewhere")
    rid = str(camp.get("room_id") or "")
    flags = [str(x) for x in (camp.get("flags") or []) if x]
    log = list(camp.get("log") or [])
    blob = " ".join(
        [rid, here, " ".join(flags)]
        + [str(e.get("text") or "") for e in log[-80:]]
        + [str(e.get("type") or "") for e in log[-80:]]
    ).lower()
    color = str((camp.get("storyteller") or {}).get("color") or "").strip()

    # Vonnegut: start at the end of what already happened.
    now = []
    if "claw" in rid or "claw" in here.lower() or "hall" in here.lower():
        if "goblin" in blob:
            now.append("The goblin band is already down. That is not the story.")
        now.append("The keep is a temple. The crate is a puzzle box. The story is who comes out when you open it.")
    elif "keep" in rid or "gate" in rid:
        now.append("The keep is the building that appeared. The chimney still lies about the weather.")
    elif "lantern" in rid or "tavern" in here.lower():
        now.append("The lantern is still a hub. The road north is the call.")
    else:
        now.append(f"Now: {here}.")

    path = []
    if any(w in blob for w in ("lantern", "tavern", "mira")):
        path.append("the Guttered Lantern")
    if any(w in blob for w in ("road", "cart", "tracks")):
        path.append("the road with the overturned cart")
    if any(w in blob for w in ("keep_gate", "gatehouse", "courtyard")):
        path.append("the keep gate")
    if any(w in blob for w in ("cellar", "cave", "fork")):
        path.append("the caves")
    if any(w in blob for w in ("claw", "hall")):
        path.append("the claw-marked hall")
    walked = ""
    if path:
        walked = f"{who} walked {', then '.join(path)}. "

    calc = ""
    if "calcifer" in blob or "torch" in blob:
        calc = "The fire came with them — Calcifer, same flame as the lantern, still arguing with the damp. "

    want = ""
    if "merchant" in blob or "captive" in blob:
        want = "The merchant wants a name spoken and a rope cut. The crate wants to go up. "
    if "chimney" in blob or "wrong smoke" in blob:
        want += "The keep still wants its lie believed. "

    legend = (walked + " ".join(now) + " " + calc + want).strip()
    if color and color.lower() not in legend.lower():
        legend = legend + " " + color[:280]
    return " ".join(legend.split())


def _craft_narrate(camp: dict[str, Any], events: list[str]) -> str:
    """Author corpus through Mag DM voice. Engine bytes stay truth. No new throne."""
    room = _room(camp)
    pl = camp.get("player") or {}
    try:
        from mag.corpus_query import inspire_for_scene
        from mag.game_dm_voice import _narrator_from_pack
        pack = (inspire_for_scene(
            story=" ".join(str(e) for e in (events or [])[-5:]),
            room=str(room.get("name") or room.get("id") or ""),
            flags=list(camp.get("flags") or [])[-8:],
            events_tail=list(events or [])[-5:],
        ) or {}).get("pack") or {}
        line = _narrator_from_pack(
            pack,
            status=str(camp.get("status") or "active"),
            player_name=str(pl.get("name") or "Adventurer"),
            absurd=False,
            your_turn=True,
            events=list(events or []),
        )
        return " ".join(str(line or "").split())[:420]
    except Exception:
        return ""


def _llm_room_beat(camp: dict[str, Any]) -> str:
    """Creative DM beat via game_dm_llm (emergent, Memento-flavored). Returns text or None on
    failure so the deterministic narration is the safe fallback."""
    try:
        from mag import game_dm_llm
        from mag import game_saga
        room = _room(camp)
        scene = f"{room.get('name')}. {room.get('desc')}".strip()
        root = str((camp.get("world_root") or ""))[:16]
        cid = str(camp.get("campaign_id") or camp.get("id") or "default")
        history = list(camp.get("log") or [])
        saga = game_saga.recall(cid)
        if saga.get("text"):
            history = [saga["text"]] + history
        res = game_dm_llm.dm_narrate(scene, world_root=root, action="look", history=history)
        if res.get("ok") and res.get("text"):
            text = str(res["text"]).strip()
            # record a named saga beat so the running gag recurs + builds (Boatmurdered law)
            game_saga.add(cid, _saga_name(room), f"in the {room.get('name')}: {scene}"[:200])
            return text
    except Exception:
        pass
    return ""


def _saga_name(room: dict[str, Any]) -> str:
    """The named thing the world will remember — a room's recurring character or a specific absurdity."""
    people = [str(p) for p in (room.get("hooks") or []) if str(p).strip().lower().startswith(
        ("barkeep", "stranger", "merchant", "goblin", "calcifer"))]
    if people:
        return people[0].split(":", 1)[0].strip()
    for known in ("elephant", "the mug", "the torch", "the fire", "the crate"):
        if any(known in str(h).lower() for h in (room.get("hooks") or [])):
            return known
    return str(room.get("name") or "the tavern")


def _narrate_room(camp: dict[str, Any]) -> str:
    """This beat. Objects first. People want. Soft craft echo. No census."""
    # Creative DM (MAG_CAMPAIGN_LLM, default ON): emergent LLM narration via game_dm_llm,
    # deterministic fallback if it fails. Set MAG_CAMPAIGN_LLM=0 for the pure $0 engine.
    if os.environ.get("MAG_CAMPAIGN_LLM", "1") not in ("0", "false", "no"):
        beat = _llm_room_beat(camp)
        if beat:
            return beat
    room = _room(camp)
    name = str(room.get("name") or "?")
    desc = str(room.get("desc") or "").strip()
    paras: list[str] = []
    lead = desc if desc and desc.lower().startswith(name.lower()) else (
        f"{name}. {desc}" if desc else f"{name}."
    )
    paras.append(lead if lead[-1:] in ".!?" else lead + ".")

    people = people_in_room(camp)
    hooks = [str(h).strip() for h in (room.get("hooks") or []) if str(h).strip()]
    rumor = ""
    used = set()
    for h in hooks:
        low = h.lower()
        if low.startswith("quest"):
            continue
        if low.startswith("rumor"):
            rumor = _hook_body(h)
            continue
        body = _hook_body(h)
        if not body:
            continue
        for ppl in people:
            if ppl.lower() in h.lower():
                used.add(ppl.lower())
        words = body.replace(".", "").split()
        # Inform: skip when_closed labels; weave verbs only
        if len(words) <= 6 and not any(
            w.lower() in ("is", "are", "has", "holds", "wants", "lies", "sits", "burns", "waits")
            for w in words
        ):
            continue
        if body[-1] not in ".!?":
            body += "."
        paras.append(body)
        for p in people:
            if p.lower() in h.lower():
                used.add(p.lower())

    leftover = [p for p in people if p.lower() not in used]
    if leftover:
        if len(leftover) == 1:
            paras.append(f"{leftover[0]} is here, and wants something.")
        else:
            paras.append(", ".join(leftover[:-1]) + f", and {leftover[-1]} are here.")

    if rumor and rumor.lower() not in " ".join(paras).lower():
        paras.append(rumor if rumor[-1:] in ".!?" else rumor + ".")

    enc = camp.get("encounter")
    if enc and int(enc.get("hp") or 0) > 0:
        paras.append(
            f"{enc.get('name')} still holds the floor. They want you gone more than they want to talk."
        )
    elif enc and int(enc.get("hp") or 0) <= 0:
        nm = str(enc.get("name") or "the fight")
        if nm.lower() not in " ".join(paras).lower():
            paras.append(f"{nm} is down. The stone has not cooled.")

    sense = _donjon_sense(camp)
    if sense and sense.lower() not in " ".join(paras).lower():
        paras.append(sense if sense[-1:] in ".!?" else sense + ".")

    try:
        from mag.chasm_state import recall
        mem = recall(str(camp.get("campaign_id") or ""), str(camp.get("room_id") or ""), limit=2)
        for m in mem or []:
            line = " ".join(str(m).split())
            low = line.lower()
            if not line:
                continue
            if low.startswith("this place remembers") or "`idle`" in low:
                continue
            if re.search(r"\d{4}-\d{2}-\d{2}T", line):
                continue
            if "`" in line:
                continue
            if any(line[:40] in p for p in paras):
                continue
            paras.append(line[:160] if line[-1:] in ".!?" else line[:160] + ".")
            break
    except Exception:
        pass

    exits = room.get("exits") or {}
    if isinstance(exits, dict) and exits:
        rooms = (camp.get("module_snapshot") or {}).get("rooms") or {}
        named = []
        for d, dest_id in exits.items():
            dest = rooms.get(str(dest_id) or "") or {}
            dname = str(dest.get("name") or dest_id or d)
            named.append(f"{d} toward {dname}")
        pass
    return " ".join(p.strip() for p in paras if p and p.strip())



def scene_context(camp: dict[str, Any]) -> dict[str, Any]:
    """TinyStories-regime input for narrator — no dig/desk sludge."""
    room = _room(camp)
    pl = camp.get("player") or {}
    return {
        "room_name": room.get("name"),
        "room_desc": room.get("desc"),
        "hook": (room.get("hooks") or [None])[0],
        "hooks": list(room.get("hooks") or []),
        "exits": list((room.get("exits") or {}).keys()),
        "encounter": camp.get("encounter"),
        "player": {
            "name": pl.get("name"),
            "archetype": pl.get("archetype"),
            "hp": pl.get("hp"),
            "hp_max": pl.get("hp_max"),
            "traits": pl.get("traits"),
        },
        "flags": (camp.get("flags") or [])[-8:],
        "log_tail": [e.get("text") for e in (camp.get("log") or [])[-3:]],
        "legal": list_legal_actions(camp),
    }


def _examine_verbs(camp: dict[str, Any]) -> str:
    """Command/verb reference for the current room — the grounded 'how do I play' answer."""
    room = _room(camp)
    lookables = _lookables(room)
    takeables = _takeables(camp)
    people = people_in_room(camp)
    exits = list((room.get("exits") or {}).keys())
    L = ["— COMMANDS · verbs you can use right now —"]
    if lookables:
        L.append("  look <object>    : study  " + ", ".join(str(x) for x in lookables))
    if people:
        L.append("  talk <person>    : speak  " + ", ".join(people))
    if takeables:
        L.append("  take <item>      : take   " + ", ".join(str(x) for x in takeables))
    if exits:
        L.append("  move <direction> : go     " + ", ".join(exits))
    L.append("  use <object>     : interact with a feature (torch / crate / box / seal)")
    L.append("  examine          : this reference · examine <object> : study one thing closer")
    L.append("  try <verb> <obj> : attempt a complex action — the dice decide, the world reacts")
    L.append("  look / rest / rumor / drink / work")
    return "\n".join(L)


def _verbs_for_object(camp: dict[str, Any], noun: str) -> str:
    """Suggest verbs that work on one examined object (the 'try' hook)."""
    return (f"On the {noun}, you could: examine <it>, use {noun}, or try <verb> {noun}. "
            f"Look close first — the right verb may be hiding in its description.")


def _try_action(
    camp: dict[str, Any], pl: dict[str, Any], action: dict[str, Any], *, raw: str = ""
) -> str:
    """Complex interaction: roll the dice, decide success/fail, narrate the consequence
    (via the creative DM), and subtly hint a good next move to finish the task."""
    from mag.game_dice import roll_dice

    text = (raw or str(action.get("raw") or action.get("text") or "")).strip()
    rest = re.sub(r"^(try|try to|attempt|attempt to)\s+", "", text, flags=re.I).strip()
    words = rest.split()
    verb = words[0].lower() if words else "force"
    target = " ".join(words[1:]).strip() or str(action.get("target") or "the door")
    room = _room(camp)
    bonus = int(pl.get("attack_bonus") or 2)
    roll = int(roll_dice("1d20", seed=None).get("total") or 1) + bonus
    dc = 12
    ok = roll >= dc
    try:
        from mag import game_dm_llm
        scene = f"{room.get('name')}. {room.get('desc')}".strip()
        prompt = (f"The player attempts to {verb} the {target}. "
                  f"Roll {roll} vs difficulty {dc} — {'SUCCESS' if ok else 'FAILURE'}. "
                  f"Narrate the consequence, then subtly hint a good next move to finish the task.")
        res = game_dm_llm.dm_narrate(scene, action=prompt)
        if res.get("ok") and res.get("text"):
            return str(res["text"]).strip()
    except Exception:
        pass
    if ok:
        camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + [f"handled:{target.lower()[:20]}"]))
        return (
            f"The {target} gives. Something you had not named yet was the tool."
        )
    return (
        f"The {target} keeps its secret. The crate is still waxed. The tool is not in your hand."
    )


def _next_paths(camp: dict[str, Any], events: list[str], action: dict[str, Any] | None = None) -> list[dict[str, str]]:
    """3-4 clickable paths from this beat and this room. Type anything else."""
    beat = " ".join(str(e) for e in (events or [])).lower()
    raw = str((action or {}).get("raw") or (action or {}).get("text") or "").lower()
    blob = beat + " " + raw
    room = _room(camp)
    rid = str(camp.get("room_id") or room.get("id") or "").lower()
    people = [str(x).lower() for x in people_in_room(camp)]
    enc = camp.get("encounter") or {}
    exits = room.get("exits") or {}
    exit_names = list(exits.keys()) if isinstance(exits, dict) else list(exits or [])
    flags = [str(f).lower() for f in (camp.get("flags") or [])]
    hooks = " ".join(str(h) for h in (room.get("hooks") or [])).lower()
    room_blob = " ".join([str(room.get("name") or ""), str(room.get("desc") or ""), hooks]).lower()
    paths: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(label: str, text: str) -> None:
        t = (text or "").strip()
        if not t or t.lower() in seen or len(paths) >= 4:
            return
        seen.add(t.lower())
        paths.append({"label": label, "text": t})

    fighting = False
    try:
        fighting = bool(isinstance(enc, dict) and enc.get("name") and int(enc.get("hp") or 0) > 0)
    except (TypeError, ValueError):
        fighting = False
    if any(w in blob for w in ("rope", "cut", "loose", "wrist", "bound")) and "freed_merchant" not in flags:
        if (not fighting) or ("near:merchant" in flags):
            add("Cut him loose", "take rope")
    if any(w in blob or w in room_blob for w in ("crate", "box", "seal", "wax")):
        if not fighting:
            add("Look at the crate", "look crate")
    if fighting:
        _ensure_band(camp)
        enc = camp.get("encounter") or enc
        alert = bool(isinstance(enc, dict) and enc.get("alert"))
        if not alert:
            add("Listen", "listen")
        unit = _pick_unit(enc) if isinstance(enc, dict) else None
        if unit:
            add("Attack the " + str(unit.get("name")), "attack " + str(unit.get("name")))
        else:
            add("Fight " + str(enc.get("name")), "attack")
        if alert:
            add("Wait", "wait")
        elif "near:merchant" in flags and "freed_merchant" not in flags:
            add("Talk to the merchant", "talk to merchant")
        elif "freed_merchant" not in flags:
            add("Sneak to the captive", "sneak to merchant")
        add("Get out", "flee")
    pal = _pal(camp, "merchant")
    if pal and str(pal.get("station") or "") == "cover":
        add("Tell him to fight", "talk to merchant fight")
    if pal and str(pal.get("station") or "") == "fight":
        add("Talk to the merchant", "talk to merchant")
    if "merchant" in people and "talk to merchant" not in seen and not pal:
        if "merchant" not in blob:
            if not (fighting and isinstance(enc, dict) and enc.get("alert") and "near:merchant" not in flags):
                add("Talk to the merchant", "talk to merchant")
    if any(n in people for n in ("barkeep", "mira")):
        add("Talk to Mira", "talk to mira")
        add("Look at the fire", "look fire")
    if "stranger" in people and "stranger" not in blob:
        add("Talk to the stranger", "talk to stranger")
    if "stubs" in room_blob or "cellar" in rid:
        add("Look at the stubs", "look stubs")
        if "deeper" in [str(e).lower() for e in exit_names]:
            add("Go deeper", "go deeper")
        if "up" in [str(e).lower() for e in exit_names]:
            add("Go up", "go up")
    for d in exit_names:
        dl = str(d).lower()
        add("Go " + dl, "go " + dl)
    add("Look around", "look")
    add("Check your hands", "look hand")
    return paths[:4]


def list_legal_actions(camp: dict[str, Any]) -> list[dict[str, Any]]:
    room = _room(camp)
    acts: list[dict[str, Any]] = []
    enc = camp.get("encounter")
    if enc and int(enc.get("hp") or 0) > 0:
        acts.append({"type": "attack"})
        acts.append({"type": "flee"})
    for name in people_in_room(camp):
        acts.append({"type": "talk", "target": name})
    for noun in _lookables(room):
        acts.append({"type": "look", "target": noun})
    for item in _takeables(camp):
        acts.append({"type": "take", "item": item})
    for direction in room.get("exits") or {}:
        acts.append({"type": "move", "direction": direction})
    acts.append({"type": "work"})
    acts.append({"type": "look"})
    acts.append({"type": "rest"})
    tags = [str(t).lower() for t in (room.get("tags") or [])]
    if "tavern" in tags or "hub" in tags or room.get("area_tag") == "hub":
        acts.extend([{"type": "rumor"}, {"type": "drink"}])
    if room.get("area_tag") in ("road", "woods") or "road" in str(room.get("id") or ""):
        acts.append({"type": "seek_fight"})
    acts.append({"type": "examine"})  # command/verb reference (how to play, grounded)
    acts.append({"type": "try"})      # complex interaction: roll -> consequence -> hint
    return acts



def people_in_room(camp: dict[str, Any]) -> list[str]:
    """Names you can talk to. Same bytes wave._room_who already paints."""
    room = _room(camp)
    names: list[str] = []
    enc = camp.get("encounter")
    if isinstance(enc, dict) and enc.get("name") and int(enc.get("hp") or 0) > 0 and not enc.get("units"):
        names.append(str(enc.get("name")))
    for h in room.get("hooks") or []:
        s = str(h).strip()
        if not s:
            continue
        low = s.lower()
        if low.startswith("rumor") or low.startswith("quest"):
            continue
        name = ""
        if low.startswith("barkeep"):
            name = "barkeep"
        elif "stranger" in low:
            name = "stranger"
        elif low.startswith("merchant") or low.startswith("captive"):
            name = "merchant"
        elif "goblin" in low:
            name = "goblin"
        elif ":" in s[:28]:
            name = s.split(":", 1)[0].strip()
            if name.lower() in ("rumor", "quest", "hook"):
                continue
        if not name:
            continue
        if any(x.lower() == name.lower() for x in names):
            continue
        names.append(name)
    blob = " ".join([
        str(room.get("name") or ""),
        str(room.get("desc") or ""),
        " ".join(str(x) for x in (room.get("tags") or [])),
        " ".join(str(h) for h in (room.get("hooks") or [])),
    ]).lower()
    rid = str(camp.get("room_id") or room.get("id") or "").lower()
    if ("lantern" in rid or "tavern" in rid) and any(w in blob for w in ("fire", "hearth")):
        if "calcifer" not in [n.lower() for n in names]:
            names.append("Calcifer")
    flags = [str(f).lower() for f in (camp.get("flags") or [])]
    if "merchant_fled" in flags:
        names = [n for n in names if "merchant" not in n.lower()]
    for pal in _pals(camp):
        if str(pal.get("station") or "") == "fled":
            continue
        nm = str(pal.get("name") or "").strip()
        if nm and not any(nm.lower() == x.lower() for x in names):
            names.append(nm)
    return names


def _talk_target(raw: str, people: list[str], explicit: str = "") -> str:
    if (explicit or "").strip():
        e = explicit.strip()
        for p in people:
            if p.lower() == e.lower() or e.lower() in p.lower() or p.lower() in e.lower():
                return p
        return e
    blob = (raw or "").strip().lower()
    for p in people:
        if p.lower() in blob:
            return p
    aliases = (("mira", "barkeep"), ("bartender", "barkeep"))
    for a, canon in aliases:
        if re.search(rf"\\b{a}\\b", blob):
            for p in people:
                if p.lower() == canon:
                    return p
            return canon
    m = re.search(
        r"\\b(?:talk|speak|say|ask)\\s+(?:to\\s+|with\\s+)?(?:the\\s+)?([a-z][\\w'-]*)",
        blob,
    )
    if m:
        cand = m.group(1)
        if cand not in ("to", "the", "a", "an", "me", "you"):
            return cand
    return ""


def _hook_for_person(room: dict[str, Any], name: str) -> str:
    for h in room.get("hooks") or []:
        if name.lower() in str(h).lower():
            return str(h).strip()
    return ""


def _talk_events(camp: dict[str, Any], pl: dict[str, Any], action: dict[str, Any]) -> list[str]:
    """Address the person in the room. Hooks are their lines. No rumor dump."""
    raw = str(action.get("raw") or "").strip()
    room = _room(camp)
    people = people_in_room(camp)
    you = str(pl.get("name") or "").strip()
    target = _talk_target(raw, people, str(action.get("target") or ""))
    events: list[str] = []
    low_raw = raw.lower().strip()
    commandish = (
        low_raw in ("talk", "speak", "say", "ask")
        or low_raw.startswith(("talk to ", "speak to ", "say to ", "ask ", "talk with ", "speak with "))
        or bool(re.search(r"\b(wink|nod|wave)\s+at\b", low_raw))
    )
    if not raw:
        events.append("You speak into the room.")
    if target and you and target.lower() == you.lower():
        events.append("That's you.")
        if people:
            events.append("Here: " + ", ".join(people) + ".")
        return events
    if not target:
        names = {x.lower() for x in people}
        if "barkeep" in names and any(
            w in low_raw for w in ("polish", "mug", "tankard", "glass", "why", "mira")
        ):
            target = "barkeep"
        elif "stranger" in names and any(
            w in low_raw for w in ("hunt", "mark", "bad guy", "failed", "party", "adventur")
        ):
            target = "stranger"
        elif "barkeep" in names and any(
            w in low_raw for w in ("howdy", "hello", "hey", "hi", "hiya", "greetings")
        ):
            target = "barkeep"
        elif len(people) == 1:
            target = people[0]
        elif people:
            events.append("Talk to whom? " + ", ".join(people) + ".")
            return events
        else:
            rid = str(camp.get("room_id") or "").lower()
            if "lantern" in rid or "tavern" in rid:
                events.append(_talk_calcifer(camp) or "The hearth pops. No one answers.")
            else:
                events.append("No one answers.")
            return events
    tlow = target.lower()
    if "calcifer" in tlow:
        events.append(_talk_calcifer(camp) or "He is in Mira's hearth. Not here.")
        return events
    if tlow in ("fire", "hearth", "torch", "flame"):
        rid = str(camp.get("room_id") or "").lower()
        if "lantern" in rid or "tavern" in rid:
            events.append(_talk_calcifer(camp) or "A fire elemental lives in this hearth. You named him Calcifer. He is not every flame.")
        else:
            events.append("A fire. Ordinary. Not the elemental from the lantern.")
        return events
    tlow_inv = target.lower()
    skip_inv = any(n in tlow_inv for n in ("mira", "barkeep", "merchant", "stranger", "calcifer", "goblin"))
    if not skip_inv:
        # Invariant-NPCs (the doctrine personified): talking to one IS interacting with an invariant.
        inv_events = _invariant_talk(target, camp)
        if inv_events:
            events.extend(inv_events)
            return events
    here = any(
        p.lower() == target.lower() or target.lower() in p.lower() or p.lower() in target.lower()
        for p in people
    )
    tlow_early = target.lower()
    aliases = {"mira": "barkeep", "bartender": "barkeep", "captive": "merchant"}
    want = aliases.get(tlow_early, tlow_early)
    here = here or any(want in p.lower() or p.lower() in want for p in people)
    local = ("merchant", "barkeep", "mira", "stranger", "goblin")
    if any(n in tlow_early for n in local) and not here:
        if people:
            events.append("No " + target + " here. Here: " + ", ".join(people) + ".")
        else:
            events.append("No " + target + " here.")
        return events
    if people and not here:
        events.append("No " + target + " here. Here: " + ", ".join(people) + ".")
        return events
    if "merchant" in tlow or "captive" in tlow:
        flags = list(camp.get("flags") or [])
        enc = camp.get("encounter")
        live = isinstance(enc, dict) and int(enc.get("hp") or 0) > 0
        if live and "near:merchant" not in flags:
            if isinstance(enc, dict) and enc.get("alert"):
                events.append("They are looking. You cannot reach the rope.")
                return events
            ok, line = _sneak_to(camp, pl)
            events.append(line)
            if not ok:
                enc = _ensure_band(camp) or {}
                guard = next((u for u in (enc.get("units") or []) if u.get("station") in ("captive", "mouth") and u.get("aware")), None)
                if guard:
                    _goblin_strike(camp, guard, pl, events)
                enc = camp.get("encounter") or enc
                if isinstance(enc, dict) and enc.get("init") and "you" in enc["init"]:
                    enc["whose"] = enc["init"].index("you")
                return events
        pal = _pal(camp, "merchant")
        if pal and str(pal.get("station") or "") == "cover" and any(
            w in low_raw for w in ("fight", "help", "stand", "spear")
        ):
            from mag.game_dice import roll_dice
            if int(roll_dice("1d20").get("total") or 10) >= 12:
                pal["station"] = "fight"
                pal["traits"] = ["cynical"]
                _set_pal(camp, pal)
                events.append("He takes a spear. His hands shake. He still will not touch the crate.")
            else:
                pal["station"] = "fled"
                camp["flags"] = list(dict.fromkeys(flags + ["merchant_fled"]))
                _set_pal(camp, pal)
                events.append("He shakes his head and runs.")
            return events
        if pal and str(pal.get("station") or "") == "fight":
            events.append("He keeps the spear. He still will not open that box.")
            return events
        if pal and str(pal.get("station") or "") == "cover":
            events.append("He is behind the crate. Cover. He will not open it.")
            return events
        if "merchant_fled" in flags:
            events.append("He already ran.")
            return events
        if "freed_merchant" in flags:
            events.append(
                "He rubs the ring in his wrist. "
                "'I walk. I still will not open that box.'"
            )
        elif "talked_merchant" in flags:
            events.append(
                "He will not look at the crate. "
                "'The rope is a kindness. The seal is a name you have not spoken. "
                "Those are the only two doors left.'"
            )
        else:
            tug = int((camp.get("encounter") or {}).get("rope_tug") or 0)
            if tug >= 2:
                events.append("The knot is worse. His hand is darker.")
            events.append(
                "The merchant's mouth is dry. The rope has worn a ring in his wrist. "
                "'Cut me loose and I will walk. I will not open that box. "
                "We shut it because we did not have the tool. Opening it is how you find the tool.'"
            )
            camp["flags"] = list(dict.fromkeys(flags + ["talked_merchant"]))
        return events
    if tlow in ("barkeep", "mira") or "barkeep" in tlow:
        flags = list(camp.get("flags") or [])
        if any(w in raw.lower() for w in ("polish", "mug", "tankard", "glass", "why")):
            events.append(
                "Mira the barkeep does not look up. "
                "'Because if I stop, I start counting chairs I do not own and debts I do. "
                "Mug is honest work. Keep smoke is not my department.'"
            )
            return events
        if "talked_mira" in flags:
            events.append("Mira polishes. 'Keep smoke is not my department.'")
        else:
            events.append(
                "Mira the barkeep does not look up. "
                "'First drink is free if you come back breathing. Mug is honest work.'"
            )
            camp["flags"] = list(dict.fromkeys(flags + ["talked_mira"]))
        return events
    if tlow == "stranger" or "stranger" in tlow:
        if any(w in raw.lower() for w in ("hunt", "mark", "bad guy", "failed", "party", "adventur")):
            events.append(
                "A regular snorts. 'Party came back empty-handed. "
                "Heat like that finds a stranger's stool real quick.'"
            )
            camp["flags"] = list(
                dict.fromkeys(list(camp.get("flags") or []) + ["failed_hunt_rumor"])
            )
            return events
        voice = _rashomon_voice("stranger")
        if voice:
            events.append("The stranger does not look up. " + voice)
            return events
        hook = _hook_for_person(room, "stranger")
        if hook:
            events.append(hook)
            return events
    hook = _hook_for_person(room, target)
    if hook:
        events.append(hook)
        return events
    events.append(target + " does not answer cleanly. The room heard you.")
    return events


def _pick_weighted(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None
    total = sum(int(r.get("w") or 1) for r in rows)
    x = random.randint(1, max(1, total))
    acc = 0
    for r in rows:
        acc += int(r.get("w") or 1)
        if x <= acc:
            return r
    return rows[-1]


def _fire_rest_events(camp: dict[str, Any]) -> list[str]:
    """CK/Rim-lite: tables + traits produce comedy."""
    events: list[str] = []
    tables = (camp.get("module_snapshot") or {}).get("event_tables") or {}
    pl = camp.get("player") or {}
    traits = [str(t).lower() for t in (pl.get("traits") or [])]
    st = camp.get("storyteller") or {}
    st["days_since_crisis"] = int(st.get("days_since_crisis") or 0) + 1

    row = _pick_weighted(list(tables.get("rest_safe") or []))
    if row:
        events.append(str(row.get("text") or ""))
        if row.get("lose") and row["lose"] in (pl.get("inventory") or []):
            pl["inventory"] = [i for i in pl.get("inventory") or [] if i != row["lose"]]
            events.append(f"(Lost {row['lose']}.)")
        if row.get("id") == "omen" and "craven" in traits:
            events.append("Your craven streak whispers: turn back.")
        if row.get("id") == "thief" and "greedy" in traits:
            events.append("As a greedy soul, the missing ration stings extra.")

    # merchant debt comedy if flag pending
    if "freed_merchant_opportunity" in (camp.get("flags") or []) and "greedy" in traits:
        row2 = _pick_weighted(list(tables.get("greedy_merchant") or []))
        if row2:
            events.append(str(row2.get("text") or ""))
            if row2.get("flag"):
                camp["flags"] = list(camp.get("flags") or []) + [str(row2["flag"])]
            camp["flags"] = [f for f in camp["flags"] if f != "freed_merchant_opportunity"]

    # storyteller crisis if budget and long calm
    budget = int(st.get("threat_budget") or 0)
    if budget > 0 and int(st.get("days_since_crisis") or 0) >= 2 and random.random() < 0.35:
        events.append("Distant horns — the keep's troubles don't sleep when you do.")
        st["days_since_crisis"] = 0
        st["threat_budget"] = budget - 1

    camp["storyteller"] = st
    camp["player"] = pl
    return [e for e in events if e]


def _act_events(camp: dict[str, Any], action: dict[str, Any]) -> list[str]:
    """cast/summon/call: collide verb with room bytes + lance.trace. FILE speech, never empty."""
    raw = str(action.get("raw") or "").strip()
    verb = str(action.get("verb") or "").strip().lower()
    target = str(action.get("target") or "").strip().lower()
    blob = (raw + " " + verb + " " + target).lower()
    room = _room(camp)
    desc = str(room.get("desc") or "")
    hooks = [str(h) for h in (room.get("hooks") or [])]
    room_blob = " ".join(
        [str(room.get("name") or ""), desc, " ".join(hooks)]
    ).lower()
    try:
        from mag.fish_ear import decompile
        decompile(raw or (verb + " " + target))
    except Exception:
        pass
    found: dict[str, bool] = {}
    try:
        from mag.verkle_lance import trace
        for k in ("fireball", "familiar", "babel", "calcifer", "percolat"):
            try:
                found[k] = bool((trace(k, limit=3) or {}).get("found"))
            except Exception:
                found[k] = False
    except Exception:
        pass
    parts: list[str] = []
    if "fireball" in blob or (verb == "cast" and "familiar" not in blob):
        if any(w in room_blob for w in ("torch", "fire", "flame", "hearth")):
            parts.append(
                "The torch pops — Calcifer, same fire as the lantern. It answers the cast."
            )
        dice_h = next((h for h in hooks if "dice" in h.lower()), "")
        if dice_h:
            parts.append(dice_h)
        if "gate" in room_blob and desc:
            parts.append(desc.split(".")[0].strip().rstrip(".") + ".")
        if not found.get("fireball"):
            parts.append("The chain has no fireball knot. The room still moves.")
    if "familiar" in blob or verb in ("summon", "call"):
        if found.get("babel") or found.get("familiar"):
            rib = _rib_babel_speech()
            origin_what = ""
            try:
                from mag.fish_ear import originate
                origin_what = str(((originate() or {}).get("origin") or {}).get("what") or "")
            except Exception:
                pass
            parts.append(
                "The liquid familiar answers as translation in a body of work — "
                "the babel fish, not a pet on the floor."
            )
            if rib:
                parts.append(rib)
            elif origin_what:
                parts.append(origin_what)
            camp["flags"] = list(
                dict.fromkeys(list(camp.get("flags") or []) + ["liquid_familiar"])
            )
        else:
            if any(w in room_blob for w in ("torch", "fire", "flame")):
                parts.append("The torch pops. No familiar stands on the floor.")
            elif hooks:
                parts.append(hooks[0])
    if not parts:
        try:
            from mag.swarm_emerge import detect
            detect()
        except Exception:
            pass
        parts.append(desc[:220] if desc else "The room hears you.")
        if hooks:
            parts.append(hooks[0])
    speech = _player_signal(" ".join(p for p in parts if p), source="keep_gate_act")
    if not speech:
        speech = (hooks[0] if hooks else desc[:180]) or "The room answers."
    return [speech]



def _wound_look(hp: int, hp_max: int, who: str = "they") -> str:
    """HP is the body. 10 full, 5 beaten, 3 needs a doctor, 1 badly wounded still moving."""
    hp = int(hp or 0)
    mx = max(1, int(hp_max or 10))
    you = who == "you"
    if hp <= 0:
        return "You fall." if you else "They drop."
    n = 10.0 * hp / mx
    if n >= 9.5:
        return "You look unhurt." if you else "They look unhurt."
    if n >= 5:
        return "You've taken a beating." if you else "They've taken a beating."
    if n >= 3:
        return "You're hurt. You need a doctor." if you else "They're hurt. They need a doctor."
    return (
        "You're badly wounded. You can still move. You need help."
        if you
        else "They're badly wounded. They can still move. They need help."
    )


def _glance(camp: dict[str, Any]) -> str:
    """Place remembers deeds, not glances. One beat. Flags prime the next door."""
    room = _room(camp)
    name = str(room.get("name") or "Here")
    rid = str(camp.get("room_id") or room.get("id") or "").lower()
    tags = [str(x).lower() for x in (room.get("tags") or [])]
    flags = [str(f).lower() for f in (camp.get("flags") or [])]
    crate_open = any("crate" in f or f.startswith("handled:") for f in flags)
    here = " ".join(people_in_room(camp)).lower()
    if "tavern" in tags or "hub" in tags or "lantern" in rid:
        if crate_open and "crate" in (str(room.get("desc") or "") + here).lower():
            return name + " is the same. Wax on the crate is broken. Mira will not look at it."
        if "talked_merchant" in flags and "merchant" in here:
            return name + " is the same. Rope and seal still wait. The fire argues with the damp."
        if "talked_mira" in flags:
            return name + " is the same. The dwarf's mug was honest work. North is the keep."
        return name + " is the same. Mira the dwarf at the bar. A fire elemental argues with the damp."
    if "road" in rid or "road" in name.lower():
        return name + " is the same. Overturned cart. Keep smoke too black."
    if "gate" in rid:
        return name + " is the same. Empty post. Dice on the table. A hatch goes down."
    if "court" in rid:
        return name + " is the same. Well rope cut halfway. Barracks barred. West is the great hall."
    if "hall" in rid or "claw" in rid:
        here = " ".join(people_in_room(camp)).lower()
        enc = camp.get("encounter")
        if isinstance(enc, dict) and int(enc.get("hp") or 0) > 0:
            _ensure_band(camp)
            camp_line = _camp_look(camp)
            crate = " The crate keeps its wax."
            if camp_line:
                return camp_line + crate
            body = _wound_look(int(enc.get("hp") or 0), int(enc.get("hp_max") or 10), "they")
            if "freed_merchant" in flags:
                return name + " is the same. " + body + " The rope fell." + crate
            return name + " is the same. " + body + crate
        if "freed_merchant" in flags:
            return name + " is the same. The rope fell. The crate keeps its wax."
        if "talked_merchant" in flags and "merchant" in here:
            return name + " is the same. Rope and seal still wait. The crate keeps its wax."
        return name + " is the same. A captive by the fire. A crate with the keep's seal."
    if "cellar" in rid:
        return "The same cave. Cold. Chatter still deeper."
    if "fork" in rid:
        return name + " is the same. Noise echoes. Two mouths: left and right."
    enc = camp.get("encounter")
    if isinstance(enc, dict) and int(enc.get("hp") or 0) > 0:
        body = _wound_look(int(enc.get("hp") or 0), int(enc.get("hp_max") or 10), "they")
        return name + " is the same. " + body
    people = [p for p in people_in_room(camp) if p]
    if people:
        return name + " is the same. " + people[0] + " is here."
    return name + " is the same."


def apply_action(campaign_id: str, action: dict[str, Any] | None) -> dict[str, Any]:
    from mag.game_dice import roll_dice

    camp = load_campaign(campaign_id)
    if not camp:
        return {"ok": False, "error": "missing campaign"}
    if camp.get("status") == "awaiting_character":
        return {"ok": False, "error": "need character first", "need_character": True}
    if camp.get("status") != "active":
        return {"ok": False, "error": f"campaign {camp.get('status')}"}

    action = action or {}
    atype = str(action.get("type") or "").lower().strip()
    raw = str(action.get("raw") or action.get("text") or "").strip()
    legal = list_legal_actions(camp)
    events: list[str] = []
    pl = camp.get("player") or {}

    if atype in ("look", "status"):
        noun = str(action.get("item") or action.get("target") or "").strip()
        if noun:
            events.append(_look_at(camp, noun))
        else:
            camp_line = _camp_look(camp)
            events.append(camp_line or _glance(camp))
        enc = camp.get("encounter")
        if isinstance(enc, dict) and (enc.get("units") or []) and not enc.get("alert"):
            _camp_tick(camp, events, speak=False)
    elif atype in ("listen", "wait"):
        enc = _ensure_band(camp)
        live = isinstance(enc, dict) and int((enc or {}).get("hp") or 0) > 0
        if atype == "listen":
            if not live:
                events.append("The room holds its breath. Nothing answers.")
            elif enc.get("alert"):
                events.append("Steel. Breath. They are all looking.")
            else:
                bits: list[str] = []
                has_rope = False
                for u in enc.get("units") or []:
                    st = str(u.get("station") or "")
                    if st == "captive":
                        has_rope = True
                    if u.get("aware"):
                        continue
                    if st == "dice":
                        bits.append("Dice.")
                    elif st == "sleep":
                        bits.append("A snore.")
                if has_rope:
                    bits.append("The rope creaks.")
                events.append(" ".join(bits) if bits else "The camp is quiet in the wrong way.")
                if int(enc.get("rope_tug") or 0) >= 2:
                    events.append("The knot has been worked.")
                _camp_tick(camp, events, speak=False)
        else:
            if live and enc.get("alert"):
                events.append("You wait. They do not.")
                _resolve_ticks(camp, events, pl)
            elif live:
                events.append("You wait.")
                _camp_tick(camp, events, speak=True)
            else:
                events.append("Time passes.")
    elif atype == "use":
        room = _room(camp)
        tags = [str(x).lower() for x in (room.get("tags") or [])]
        if "tavern" in tags or "hub" in tags:
            events.append(
                "The torch dips toward a sticky chair. Mira does not look up. "
                "'Hearth only. You want a fire, take the road north toward the keep.'"
            )
            camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + ["hearth_only"]))
        else:
            events.append("Nothing here takes the torch kindly.")
    elif atype == "take":
        noun = str(action.get("item") or "").strip().lower()
        room = _room(camp)
        blob = " ".join([
            str(room.get("name") or ""),
            str(room.get("desc") or ""),
            " ".join(str(h) for h in (room.get("hooks") or [])),
            " ".join(str(x) for x in (room.get("loot") or [])),
        ]).lower()
        loot = list(room.get("loot") or [])
        inv = list(pl.get("inventory") or [])
        scenery = {
            "stubs", "stub", "stairs", "stair", "cave", "air", "chatter",
            "mouth", "hatch", "rock", "wall", "dark", "cold", "fire",
            "hearth", "keep", "smoke", "weather", "door", "road",
        }
        if not noun:
            events.append("Take what?")
        elif noun in scenery or any(noun == s or noun.endswith("s") and noun[:-1] in scenery for s in scenery):
            events.append("That stays in the room. It does not come free.")
        elif "rope" in noun and ("captive" in blob or "merchant" in blob):
            live = isinstance(camp.get("encounter"), dict) and int((camp.get("encounter") or {}).get("hp") or 0) > 0
            enc_now = camp.get("encounter") if isinstance(camp.get("encounter"), dict) else {}
            if live and enc_now.get("alert") and "near:merchant" not in list(camp.get("flags") or []):
                events.append("They are looking. You cannot reach the rope.")
            elif live and "near:merchant" not in list(camp.get("flags") or []):
                ok, line = _sneak_to(camp, pl)
                events.append(line)
                if not ok:
                    enc = _ensure_band(camp) or {}
                    guard = next((u for u in (enc.get("units") or []) if u.get("station") in ("captive", "mouth") and u.get("aware")), None)
                    if guard:
                        _goblin_strike(camp, guard, pl, events)
                    enc = camp.get("encounter") or enc
                    if isinstance(enc, dict) and enc.get("init") and "you" in enc["init"]:
                        enc["whose"] = enc["init"].index("you")
                else:
                    events.append(_cut_merchant(camp, pl))
            else:
                events.append(_cut_merchant(camp, pl))
        elif any(noun in str(i).lower() for i in inv):
            events.append(f"Already carrying {noun}.")
        elif any(noun in str(x).lower() for x in loot):
            item = next((x for x in loot if noun in str(x).lower()), noun.replace(" ", "_"))
            if item not in inv:
                inv.append(item)
                pl["inventory"] = inv
            if "rope" in noun:
                events.append(_cut_merchant(camp, pl))
            elif any(w in noun for w in ("crate", "seal", "chest", "bounty")):
                events.append(
                    "The crate is a calling card. Wax still holds. "
                    "We shut it because we did not have the tool."
                )
                _work_events(camp, action)
                enc_now = camp.get("encounter")
                if isinstance(enc_now, dict) and int(enc_now.get("hp") or 0) > 0:
                    events.append("Goblins still hold the floor.")
            else:
                events.append(f"You take the {noun}. It sits in the hand, unnamed until used.")
        else:
            events.append(f"No {noun} here to take.")
    elif atype == "talk":
        # Address the named person. Their hook is the line. HP lives on the bar.
        events.extend(_talk_events(camp, pl, action))
    elif atype == "rumor":
        tables = (camp.get("module_snapshot") or {}).get("event_tables") or {}
        rows = list(tables.get("tavern_rumor") or [])
        if not rows:
            events.append("No one is talking. The fire pops once, unhelpfully.")
        else:
            row = _pick_weighted(rows) or {}
            events.append(str(row.get("text") or "A rumor dissolves before it lands."))
            if row.get("flag"):
                camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + [str(row["flag"])]))
    elif atype == "drink":
        tables = (camp.get("module_snapshot") or {}).get("event_tables") or {}
        rows = list(tables.get("tavern_drink") or [])
        row = _pick_weighted(rows) if rows else {}
        events.append(str((row or {}).get("text") or "You drink. It is a liquid."))
        # tiny heal in hub
        pl["hp"] = min(int(pl.get("hp_max") or 10), int(pl.get("hp") or 0) + 1)
        events.append(f"HP {pl['hp']}/{pl.get('hp_max')}.")
    elif atype == "seek_fight":
        tables = (camp.get("module_snapshot") or {}).get("event_tables") or {}
        room = _room(camp)
        tag = str(room.get("area_tag") or "road")
        key = "random_woods" if tag == "woods" else "random_road"
        if tag == "hub":
            events.append(
                "The barkeep clears their throat: 'Not in the Lantern.' "
                "Take the road if you want a fair fight."
            )
        else:
            rows = list(tables.get(key) or tables.get("random_road") or [])
            row = _pick_weighted(rows) if rows else {}
            events.append(str((row or {}).get("text") or "Nothing answers your bloodlust."))
            enc = (row or {}).get("encounter")
            if enc:
                camp["encounter"] = dict(enc)
    elif atype == "examine":
        # examine (no target) -> the command/verb reference; examine <object> -> study it
        noun = str(action.get("item") or action.get("target") or "").strip()
        if noun:
            events.append(_look_at(camp, noun))
            events.append(_verbs_for_object(camp, noun))
        else:
            events.append(_examine_verbs(camp))
    elif atype == "try" or (raw and re.match(r"^(try|attempt)", raw, re.I)):
        events.append(_try_action(camp, pl, action, raw=raw))
    elif atype == "freeze":
        try:
            from mag.game_freeze import freeze_campaign

            fr = freeze_campaign(str(campaign_id))
            if fr.get("ok"):
                events.append(fr.get("speak") or f"Frozen `{fr.get('freeze_id')}`.")
            else:
                events.append(str(fr.get("error") or "freeze failed"))
        except Exception as exc:
            events.append(f"Freeze failed: {exc}"[:200])
    elif atype == "help":
        tips = ", ".join(
            a.get("type", "")
            + (f" {a['direction']}" if a.get("direction") else "")
            for a in legal[:10]
        )
        # Socratic: try freeze L0/L1 help if available
        try:
            from mag.game_freeze import freeze_campaign, format_socratic_help, load_freeze

            st = camp.get("storyteller") or {}
            fid = st.get("freeze_id")
            frz = load_freeze(str(fid)) if fid else None
            if not frz:
                fr = freeze_campaign(str(campaign_id))
                frz = fr.get("freeze") if fr.get("ok") else None
            if frz:
                events.append(format_socratic_help(frz))
            else:
                events.append(f"You can: {tips}. Or say inventory, rest, freeze state.")
        except Exception:
            events.append(f"You can: {tips}. Or say inventory, rest, freeze state.")
    elif atype == "inventory":
        inv = pl.get("inventory") or []
        events.append(
            f"{pl.get('name') or 'You'} carries: {', '.join(inv) if inv else 'nothing much'}."
        )
        events.append(f"HP {pl.get('hp')}/{pl.get('hp_max')}.")
    elif atype == "move":
        direction = str(action.get("direction") or "").lower()
        exits = _room(camp).get("exits") or {}
        if direction not in exits:
            # fuzzy
            for k in exits:
                if k.startswith(direction) or direction in k:
                    direction = k
                    break
        if direction not in exits:
            return {"ok": False, "error": f"can't go {direction}", "legal": legal}
        if camp.get("encounter") and int((camp["encounter"] or {}).get("hp") or 0) > 0:
            dmg = roll_dice("1d4")
            pl["hp"] = max(0, int(pl.get("hp") or 0) - int(dmg["total"]))
            events.append(f"Leaving under fire — take {dmg['total']}! HP {pl['hp']}.")
            if pl["hp"] <= 0:
                camp["status"] = "defeated"
                camp["player"] = pl
                events.append("You fall. Say start classic for a new run.")
                save_campaign(camp)
                return {"ok": True, "events": events, "narrate": " ".join(events), "status": "defeated"}
        camp["room_id"] = exits[direction]
        camp["encounter"] = None
        room = _room(camp)
        for fl in room.get("flags_on_enter") or []:
            camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + [fl]))
        enc = room.get("encounter")
        if enc:
            camp["encounter"] = dict(enc)
            rid = str(room.get("id") or camp.get("room_id") or "").lower()
            if "claw" in rid or "hall" in rid:
                _ensure_band(camp)
                events.append("You enter the hall. " + (_camp_look(camp) or "Goblins hold the floor.") + " The crate keeps its wax.")
            else:
                events.append(
                    "You enter "
                    + str(room.get("name") or "the room")
                    + ". Something holds the floor."
                )
        else:
            # game_entry.walk shape (stone 2), geography from the module not BUILDINGS.
            hook = str((room.get("hooks") or [""])[0] or "")
            name = str(room.get("name") or "somewhere")
            low_n = name.lower()
            if any(w in low_n for w in ("cave", "hall", "fork", "cellar", "tunnel", "pit", "road", "gate", "court", "lantern", "tavern")):
                line = "You walk " + direction + " into " + name + "."
            else:
                line = "You walk " + direction + " to " + name + "."
            if hook:
                line = line + " " + str(hook).split(":", 1)[-1].strip()
            events.append(line)
    elif atype == "sneak":
        ok, line = _sneak_to(camp, pl)
        events.append(line)
        if not ok:
            enc = _ensure_band(camp) or {}
            guard = next((u for u in (enc.get("units") or []) if u.get("station") in ("captive", "mouth") and u.get("aware")), None)
            if guard:
                _goblin_strike(camp, guard, pl, events)
            enc = camp.get("encounter") or enc
            if isinstance(enc, dict) and enc.get("init") and "you" in enc["init"]:
                enc["whose"] = enc["init"].index("you")
        else:
            events.append("He is close enough to hear you whisper.")
    elif atype == "attack":
        enc = camp.get("encounter")
        if not enc or int(enc.get("hp") or 0) <= 0:
            return {"ok": False, "error": "nothing to attack", "legal": legal}
        enc = _ensure_band(camp) or enc
        camp["flags"] = [f for f in (camp.get("flags") or []) if f != "near:merchant"]
        traits = [str(t).lower() for t in (pl.get("traits") or [])]
        bonus = int(pl.get("attack_bonus") or 0)
        if "hotheaded" in traits:
            bonus += 1
        if "craven" in traits:
            events.append("Fear nags. You strike anyway.")
        target = str(action.get("target") or action.get("item") or "").strip()
        unit = _pick_unit(enc, target)
        hit = roll_dice(f"1d20+{bonus}")
        ac = int((unit or enc).get("ac") or 10)
        enc_max = int(enc.get("hp_max") or enc.get("hp") or 10)
        if hit["total"] >= ac:
            dmg = roll_dice(str(pl.get("damage") or "1d6"))
            dealt = int(dmg["total"])
            if unit:
                dead = _hurt_unit(enc, unit, dealt)
                if dead:
                    events.append("The " + str(unit.get("name")) + " drops.")
                    enc = camp.get("encounter") or enc
                else:
                    events.append("The " + str(unit.get("name")) + " takes the blow. " + _wound_look(int(unit.get("hp") or 0), int(unit.get("hp_max") or 4), "they"))
                enc["hp"] = int((camp.get("encounter") or enc).get("hp") or 0)
            else:
                enc["hp"] = max(0, int(enc.get("hp") or 0) - dealt)
            if enc["hp"] <= 0:
                events.append("They drop. The crate is still waxed.")
                droom = str(enc.get("dungeon_room") or "")
                if droom:
                    try:
                        from mag import dungeon_dev
                        dungeon_dev.conquer(droom, knot=f"slain:{enc.get('name')}", publish=True)
                    except Exception:
                        pass
                for fl in _room(camp).get("flags_on_clear") or []:
                    camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + [fl]))
                camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + ([f"slain:{droom}"] if droom else [])))
                camp["encounter"] = None
            elif not unit:
                bits = []
                if dealt >= (enc_max / 2):
                    bits.append("The blow takes half of them.")
                bits.append(_wound_look(int(enc["hp"]), enc_max, "they"))
                events.append(" ".join(bits))
        else:
            if unit:
                events.append("You miss the " + str(unit.get("name")) + ".")
            else:
                events.append("You miss. " + _wound_look(int(enc.get("hp") or 0), enc_max, "they"))
        enc = camp.get("encounter")
        if enc and int(enc.get("hp") or 0) > 0:
            _resolve_ticks(camp, events, pl)
            enc = camp.get("encounter")
            if enc and int(enc.get("hp") or 0) <= 0:
                events.append("They drop. The crate is still waxed.")
                camp["encounter"] = None
                enc = None
        if enc and int(enc.get("hp") or 0) > 0 and not (enc.get("units") or []):
            fhit = roll_dice(f"1d20+{int(enc.get('attack_bonus') or 0)}")
            if fhit["total"] >= int(pl.get("ac") or 10):
                fdmg = roll_dice(str(enc.get("damage") or "1d6"))
                dealt = int(fdmg["total"])
                pmax = int(pl.get("hp_max") or pl.get("hp") or 10)
                pl["hp"] = max(0, int(pl.get("hp") or 0) - dealt)
                if pl["hp"] <= 0:
                    camp["status"] = "defeated"
                    events.append("You fall.")
                else:
                    bits = ["They hit back."]
                    if dealt >= (pmax / 2):
                        bits.append("The blow takes half of you.")
                    bits.append(_wound_look(int(pl["hp"]), pmax, "you"))
                    events.append(" ".join(bits))
    elif atype == "flee":
        exits = list((_room(camp).get("exits") or {}).keys())
        if not exits:
            return {"ok": False, "error": "nowhere to flee"}
        return apply_action(campaign_id, {"type": "move", "direction": exits[0]})
    elif atype == "rest":
        if camp.get("encounter") and int((camp["encounter"] or {}).get("hp") or 0) > 0:
            return {"ok": False, "error": "They still hold the floor.", "legal": legal}
        before = int(pl.get("hp") or 0)
        mx = int(pl.get("hp_max") or 10)
        pl["hp"] = mx
        if before > 0 and (10.0 * before / max(1, mx)) < 3:
            events.append("Help finds you. You rest. You look unhurt.")
        elif before > 0 and (10.0 * before / max(1, mx)) < 9.5:
            events.append("You rest. You look unhurt.")
        else:
            events.append("You rest. The fire argues with the damp.")
        events.extend(_fire_rest_events(camp))
    elif atype == "act":
        events.extend(_act_events(camp, action))
    elif atype in ("work", "share", "file"):
        events.extend(_work_events(camp, action))
    else:
        return {"ok": False, "error": f"illegal action {atype}", "legal": legal}

    camp["player"] = pl
    color = _craft_narrate(camp, events)
    # color lives on storyteller for the passage, not in the spoken beat
    camp["log"] = list(camp.get("log") or []) + [
        {"ts": _utc(), "type": atype, "text": e} for e in events
    ]
    save_campaign(camp)

    # session stats for DM dogfood / Fast-Slow metrics
    st = dict(camp.get("storyteller") or {})
    st["turn_n"] = int(st.get("turn_n") or 0) + 1
    st["fast_turns"] = int(st.get("fast_turns") or 0) + 1  # engine apply = fast path
    if color:
        st["color"] = color
        st["slow_turns"] = int(st.get("slow_turns") or 0) + 1
        st["ds_called"] = False
        st["craft"] = True
    st["saga"] = story_so_far({**camp, "storyteller": st})
    camp["storyteller"] = st
    save_campaign(camp)

    # Foundation: play is a world change. Castle (table) proposes; world core commits.
    try:
        from mag import game_world, game_world_render
        rid = str(camp.get("room_id") or "")
        pln = str((pl.get("name") or "adventurer")).lower().replace(" ", "-") or "adventurer"
        game_world.set_state(
            "table.campaign",
            {
                "campaign_id": campaign_id,
                "room_id": rid,
                "status": camp.get("status"),
                "turn": st.get("turn_n"),
                "action": atype,
            },
            source="table",
        )
        room = _room(camp)
        game_world.set_state(
            f"table.room.{rid or 'void'}",
            {
                "name": room.get("name"),
                "desc": (room.get("desc") or "")[:240],
                "hooks": list(room.get("hooks") or [])[:6],
            },
            source="table",
        )
        if atype == "move":
            game_world_render.walk(
                player=pln,
                direction=str(action.get("direction") or "forward"),
                region="guttered-lantern",
            )
    except Exception:
        pass

    try:
        from mag.chasm_state import persist as _chasm_persist
        _chasm_persist(camp, events=events, action=atype)
    except Exception:
        pass

    try:
        from mag.training_events import emit

        emit(
            "game_turn",
            join={
                "campaign_id": campaign_id,
                "module_id": str(camp.get("module_id") or ""),
                "world_family": "tabletop-dnd",
                "voice_session_id": str(camp.get("voice_session_id") or ""),
            },
            input_data={"action": atype, "direction": action.get("direction") or ""},
            action={
                "room": camp.get("room_id"),
                "fast_path": True,
                "ds_called": False,
            },
            outcome={
                "status": camp.get("status"),
                "events_n": len(events),
                "turn_n": st.get("turn_n"),
                "has_encounter": bool(
                    camp.get("encounter") and int((camp.get("encounter") or {}).get("hp") or 0) > 0
                ),
            },
            pattern_tags=["game", "tabletop-dnd", atype, "fast_path", "dogfood_dm"],
            tier_max="T2",
            exportable=False,
        )
    except Exception:
        pass

    return {
        "ok": True,
        "schema": SCHEMA,
        "campaign_id": campaign_id,
        "events": events,
        "narrate": " ".join(events).strip(),
        "legal": list_legal_actions(camp),
        "choices": _next_paths(camp, events, action),
        "scene_context": scene_context(camp),
        "status": camp.get("status"),
        "player": camp.get("player"),
        "fast_path": True,
        "ds_called": False,
        "metrics": {
            "turn_n": st.get("turn_n"),
            "fast_turns": st.get("fast_turns"),
            "slow_turns": st.get("slow_turns") or 0,
        },
    }



# dungeon_dev rooms wearing MUD armor. Play slays them. Conquer folds the knot.
_TEMPLE_BEASTS = {
    "emulator-core": {
        "name": "Temple Guardian",
        "kind": "construct",
        "want": "the engine room stays sealed",
        "ac": 14,
        "attack_bonus": 3,
        "damage": "1d6",
    },
    "rib-as-mod": {
        "name": "Puzzle-Box Ward",
        "kind": "puzzle",
        "want": "the lid stays shut",
        "ac": 12,
        "attack_bonus": 2,
        "damage": "1d4",
    },
    "warm-prefix": {
        "name": "Troll Army",
        "kind": "horde",
        "want": "to eat the treasury and the warming",
        "ac": 11,
        "attack_bonus": 2,
        "damage": "1d6",
    },
    "vram-lattice": {
        "name": "Necromancer",
        "kind": "undead",
        "want": "the memlands as a private grave",
        "ac": 13,
        "attack_bonus": 4,
        "damage": "1d8",
    },
    "arrival-compiler": {
        "name": "Lich of Arrival",
        "kind": "undead",
        "want": "to write its own RIB and never die",
        "ac": 15,
        "attack_bonus": 4,
        "damage": "1d8",
    },
    "hologram-visor": {
        "name": "Dragon of the Eye",
        "kind": "dragon",
        "want": "the hologram as a hoard, not a well",
        "ac": 16,
        "attack_bonus": 5,
        "damage": "1d10",
    },
}


def _beast_for_room(room_id: str, hp: int = 3) -> dict[str, Any]:
    spec = dict(_TEMPLE_BEASTS.get(str(room_id) or "") or {
        "name": "Temple Warden",
        "kind": "ward",
        "want": "the inner door stays shut",
        "ac": 12,
        "attack_bonus": 2,
        "damage": "1d6",
    })
    h = max(1, int(hp or 3))
    spec.update({
        "hp": h,
        "hp_max": h,
        "dungeon_room": str(room_id or ""),
        "temple": True,
    })
    return spec


def _work_events(camp: dict[str, Any], action: dict[str, Any] | None = None) -> list[str]:
    """Puzzle box / temple. Opening a ward spawns a beast. Share throws one worker. Slay conquers."""
    events: list[str] = []
    try:
        from mag import dungeon_dev
        st = dungeon_dev.dungeon_state() or {}
        ip = list(st.get("in_progress") or [])
        room = ip[0] if ip else None
        spec = next((r for r in dungeon_dev.ROOMS if r.get("room") == room), None) if room else None
        if not room:
            gen = dungeon_dev.generate_room() or {}
            room = gen.get("room")
            if not room:
                events.append("The temple is mapped. The puzzle box is empty. Share what you already carry.")
                return events
            spec = next((r for r in dungeon_dev.ROOMS if r.get("room") == room), None)
        hp = int((spec or {}).get("hp") or 3)
        beast = _beast_for_room(str(room), hp=hp)
        enc = camp.get("encounter")
        live = isinstance(enc, dict) and int(enc.get("hp") or 0) > 0
        if live and not enc.get("temple"):
            events.append(
                f"{enc.get('name')} still holds the floor. The puzzle box can wait."
            )
            return events
        if not live:
            camp["encounter"] = beast
            events.append(
                f"The crate is a puzzle box. The keep is a temple. "
                f"A ward opens: the {beast['name']} wants {beast.get('want')}."
            )
        else:
            events.append(f"The {enc.get('name')} is still the ward. Hit it. Share it. Slay it.")
            beast = dict(enc)
            room = str(enc.get("dungeon_room") or room)
        asg = dungeon_dev.assign_workers(str(room), n=1, enqueue=True) or {}
        if asg.get("ok"):
            events.append(
                "A worker takes the blow with you. If the beast drops, the knot is for everyone."
            )
        else:
            events.append("The temple filed the blow. The swarm did not pick up the sword.")
        camp["flags"] = list(dict.fromkeys(list(camp.get("flags") or []) + [f"temple:{room}"]))
        try:
            from mag.party_subchain import append as _ps
            _ps(seat="table", ok=True, move=f"slay {beast.get('name')} / {room}", kind="play_as_work")
        except Exception:
            try:
                from mag.steer import emit as _steer
                _steer("play-as-work", "table", f"slay {room}", steer_back=False)
            except Exception:
                pass
    except Exception as e:
        events.append("The puzzle box jams. " + str(e)[:140])
    return events


def parse_player_speech(text: str) -> dict[str, Any] | None:
    t = (text or "").strip().lower()
    if not t:
        return None
    if re.match(r"^(try|attempt)\b", t):
        return {"type": "try", "raw": (text or "").strip()[:240]}
    # single-letter exits (voice-friendly)
    if t in ("n", "north"):
        return {"type": "move", "direction": "north"}
    if t in ("s", "south"):
        return {"type": "move", "direction": "south"}
    if t in ("e", "east"):
        return {"type": "move", "direction": "east"}
    if t in ("w", "west"):
        return {"type": "move", "direction": "west"}
    if t in ("u", "up"):
        return {"type": "move", "direction": "up"}
    if t in ("d", "down"):
        return {"type": "move", "direction": "down"}
    if re.search(r"\b(share|bounty|file work|file the take|throw workers|assign workers|open the (box|temple|ward))\b", t) or t in ("share", "work", "file", "bounty", "open"):
        return {"type": "work", "raw": (text or "").strip()[:240]}
    if re.search(r"\b(slay|kill|fight|stab|hit|attack|strike)\b", t) or t in ("attack", "strike"):
        m = re.search(r"\b(?:slay|kill|fight|stab|hit|attack|strike)\s+(?:the |a |an )?(.+)$", t)
        out = {"type": "attack"}
        if m:
            out["target"] = (m.group(1) or "").strip()[:80]
        return out
    if re.search(r"\b(freeze state|freeze game|game freeze|dump state|save freeze)\b", t):
        return {"type": "freeze"}
    if re.search(r"\b(help|what can i do|options|commands|legal)\b", t):
        return {"type": "help"}
    if re.search(r"\b(inventory|inv|what do i (have|carry)|gear|pack)\b", t):
        return {"type": "inventory"}
    if re.search(
        r"\b(rumor|rumours|rumors|gossip|news|what('s| is) the (word|news)|ask (the )?barkeep)\b",
        t,
    ):
        return {"type": "rumor"}
    if re.search(r"\b(drink|ale|beer|broth|buy a drink|order a)\b", t):
        return {"type": "drink"}
    if re.search(
        r"\b(leave (the )?(tavern|inn|bar)|go (outside|out)|hit the road|leave for the road)\b",
        t,
    ):
        return {"type": "move", "direction": "out"}
    if t in ("wait", "z") or re.match(r"^wait\b", t):
        return {"type": "wait"}
    if re.search(r"\b(listen|hear|eavesdrop)\b", t):
        return {"type": "listen"}
    if re.search(r"\b(sneak|creep|steal up|stalk|hide)\b", t):
        return {"type": "sneak", "target": "merchant", "raw": (text or "").strip()[:240]}
    if re.search(r"\b(cut|free|untie|loose)\b", t) and re.search(r"\b(rope|him|merchant|captive|loose)\b", t):
        return {"type": "take", "item": "rope"}
    if re.search(r"\b(take|grab|get|pick up|pick)\b", t):
        m = re.search(r"\b(?:take|grab|get|pick up|pick)\s+(?:the |a |an )?(.+)$", t)
        return {"type": "take", "item": ((m.group(1) if m else "").strip()[:80])}
    if re.search(r"\b(wink|nod|wave)\s+at\b", t):
        m = re.search(r"\b(?:wink|nod|wave)\s+at\s+(?:the\s+)?(.+)$", t)
        who = ((m.group(1) if m else "").strip()[:80])
        return {"type": "talk", "raw": (text or "").strip()[:240], "target": who or "calcifer"}
    if t in ("talk", "speak", "say") or re.match(r"^(talk|speak|say)\s+", t):
        out = {"type": "talk", "raw": (text or "").strip()[:240]}
        m = re.search(r"^(?:talk|speak|say)\s+(?:to\s+|with\s+)?(?:the\s+)?([a-z][\w'-]*)", t)
        if m and m.group(1) not in ("to", "the", "a", "an"):
            out["target"] = m.group(1)
        return out
    if re.search(r"\b(howdy|hiya|greetings)\b", t):
        return {"type": "talk", "raw": (text or "").strip()[:240]}
    if re.search(r"\b(burn|set fire|on fire|light the|torch the|set the .+ on fire)\b", t):
        return {"type": "use", "raw": (text or "").strip()[:240], "item": "fire"}
    if re.search(r"\b(look|where am i|describe|status|what do i see|examine|search|peer)\b", t):
        m = re.search(r"\b(?:look|examine|inspect|peer)\s+(?:at |the |a |an )?(.+)$", t)
        item = (m.group(1).strip()[:80] if m else "")
        if item and item not in ("around", "here", "room"):
            return {"type": "look", "item": item}
        return {"type": "look"}
    # In-world talk / ask NPC (must not fall through to curveball bathroom fails)
    if re.search(
        r"\b("
        r"why (are|is|do|does)|what (are|is|do|does)|who (are|is)|"
        r"how (are|is|do|does|come)|tell me|ask |talk to|speak to|say to|"
        r"polishing|barkeep|mira|hey |hello|howdy|hiya|good (eve|day|night)|"
        r"what('s| is) (that|this|the)"
        r")\b",
        t,
    ):
        out = {"type": "talk", "raw": (text or "").strip()[:240]}
        m = re.search(
            r"\b(?:talk|speak|say|ask)\s+(?:to\s+|with\s+)?(?:the\s+)?([a-z][\w'-]*)",
            t,
        )
        if m:
            cand = m.group(1)
            if cand not in ("to", "the", "a", "an", "me", "you"):
                out["target"] = cand
        return out
    if re.search(r"\b(rest|heal|camp|sleep)\b", t):
        return {"type": "rest"}
    if re.search(r"\b(attack|hit|fight|strike|kill|swing|stab|slash)\b", t):
        return {"type": "attack"}
    if re.search(r"\b(flee|run away|retreat)\b", t) and not re.search(r"\brun into\b", t):
        return {"type": "flee"}
    for d in (
        "north",
        "south",
        "east",
        "west",
        "up",
        "down",
        "left",
        "right",
        "deeper",
        "back",
        "out",
        "tavern",
    ):
        if re.search(rf"\b(go |move |head |walk |run )?(to )?{d}\b", t) or t.strip() == d:
            return {"type": "move", "direction": d}
    if re.search(r"\b(enter|gate|to the keep|inside|through the (gate|door))\b", t):
        return {"type": "move", "direction": "north"}
    if re.search(r"\b(fight (a |some )?|go (fight|hunt)|find (a )?monster|random fight)\b", t):
        return {"type": "seek_fight"}
    m_act = re.search(r"\b(cast|summon|call)\s+(?:the\s+|a\s+|an\s+)?(.+)$", t)
    if m_act:
        return {
            "type": "act",
            "raw": (text or "").strip()[:240],
            "verb": m_act.group(1),
            "target": (m_act.group(2) or "").strip()[:80],
        }
    return None


def seal_session(
    *,
    session_id: str = "",
    campaign_id: str = "",
    tldr: str = "",
) -> dict[str, Any]:
    """DM post-game notes — FILE session card for train/exploit review."""
    camp = load_campaign(campaign_id) if campaign_id else None
    if not camp and session_id:
        camp = latest_for_session(session_id)
    if not camp:
        return {"ok": False, "error": "no campaign to seal"}
    st = camp.get("storyteller") or {}
    turn_n = int(st.get("turn_n") or len(camp.get("log") or []))
    fast_n = int(st.get("fast_turns") or turn_n)
    slow_n = int(st.get("slow_turns") or 0)
    card = {
        "schema": "mag_game_session_seal.v1",
        "ts": _utc(),
        "campaign_id": camp.get("campaign_id"),
        "voice_session_id": camp.get("voice_session_id") or session_id,
        "module_id": camp.get("module_id"),
        "module_title": camp.get("module_title"),
        "room_id": camp.get("room_id"),
        "status": camp.get("status"),
        "player": camp.get("player"),
        "flags": camp.get("flags"),
        "metrics": {
            "turn_n": turn_n,
            "fast_turns": fast_n,
            "slow_turns": slow_n,
            "local_only_pct": round(100.0 * fast_n / max(1, fast_n + slow_n), 1),
        },
        "log_tail": (camp.get("log") or [])[-12:],
        "tldr": (tldr or "")[:500]
        or f"Sealed at {camp.get('room_id')} after ~{turn_n} turns.",
        "dogfood_dm": True,
        "transfer_checklist": [
            "default_local_engine",
            "pack_then_guest",
            "confirm_before_write",
            "file_outcomes",
            "hub_return",
        ],
    }
    out_dir = ROOT / "memory" / "working" / "game_sessions"
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"seal_{camp.get('campaign_id')}_{_utc()[:19].replace(':', '')}.json"
    path = out_dir / fname
    path.write_text(json.dumps(card, indent=2, default=str), encoding="utf-8")
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    try:
        from mag.training_events import emit

        emit(
            "game_turn",
            join={"campaign_id": str(camp.get("campaign_id")), "kind": "seal"},
            action={"seal": True, "path": rel},
            outcome=card["metrics"],
            pattern_tags=["game", "seal", "dogfood_dm", "dm_transfer"],
            tier_max="T1",
            exportable=False,
        )
    except Exception:
        pass
    speak = (
        f"Session sealed ({rel}). "
        f"Turns {turn_n}; fast {fast_n}; slow/guest {slow_n}; "
        f"local-only ~{card['metrics']['local_only_pct']}%. "
        f"DM drill: name which Mag seat fired. See docs/ref/DM_MAG_TRANSFER.md"
    )
    return {"ok": True, "path": rel, "card": card, "speak": speak, "narrate": speak}


def handle_game(body: dict[str, Any] | None = None) -> dict[str, Any]:
    body = body or {}
    action = str(body.get("action") or "status").strip().lower()
    sid = str(body.get("session_id") or "")
    if action in ("modules", "list_modules"):
        return {"ok": True, "modules": list_modules()}
    if action in ("seal", "seal_session", "end_session"):
        return seal_session(
            session_id=sid,
            campaign_id=str(body.get("campaign_id") or ""),
            tldr=str(body.get("tldr") or body.get("text") or ""),
        )
    if action in ("start", "new", "classic", "play"):
        return begin_play(
            module_id=str(body.get("module") or body.get("module_id") or "classic"),
            voice_session_id=sid,
            force_new=bool(body.get("force_new") or action == "new"),
        )
    if action in ("character", "set_character"):
        cid = str(body.get("campaign_id") or "")
        if not cid:
            c = latest_for_session(sid)
            cid = str((c or {}).get("campaign_id") or "")
        player = body.get("player") if isinstance(body.get("player"), dict) else parse_character(
            str(body.get("text") or "")
        )
        if not player:
            return {"ok": False, "error": "could not parse character", "need_character": True}
        return set_character(cid, player)
    if action in ("state", "status"):
        c = load_campaign(str(body.get("campaign_id") or "")) or latest_for_session(sid)
        if not c:
            return {"ok": False, "error": "no campaign"}
        return {
            "ok": True,
            "campaign_id": c.get("campaign_id"),
            "status": c.get("status"),
            "scene_context": scene_context(c) if c.get("player") else None,
            "speak": _narrate_room(c) if c.get("player") else "Need character.",
            "legal": list_legal_actions(c) if c.get("player") else [],
        }
    if action in ("act", "apply", "do"):
        c = load_campaign(str(body.get("campaign_id") or "")) or latest_for_session(sid)
        if not c:
            return {"ok": False, "error": "no campaign"}
        act = body.get("move") or body.get("act")
        if isinstance(act, str):
            act = parse_player_speech(act) or {"type": act}
        if not act and body.get("text"):
            act = parse_player_speech(str(body.get("text")))
        return apply_action(str(c["campaign_id"]), act if isinstance(act, dict) else {})
    return {"ok": False, "error": f"unknown action {action}"}
