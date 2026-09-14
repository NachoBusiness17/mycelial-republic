"""Water-computer keep — physics for the hydraulic module.

Isomorphism, not identity. Engine owns tank heights + valves.
Pieces (pumps) may tick. They may not pour. Bucket into OUT is a cheat, not a win.

CLI: python -m mag.water_computer play | glass | demo
"""
from __future__ import annotations

import json
import sys
from typing import Any

SCHEMA = "water_computer.v1"
MODULE_IDS = {"water_computer", "water", "hydraulic"}
SOURCE_N = 3
WIN_OUT = 2
BAR = "█"
EMPTY = "·"

VALVE_AT = {
    "source_cistern": "source_work",
    "work_gallery": "work_out",
}


def is_module(camp: dict[str, Any] | None) -> bool:
    mid = str((camp or {}).get("module_id") or "").lower()
    return mid in MODULE_IDS or "water_computer" in mid


def seed(camp: dict[str, Any]) -> None:
    flags = [str(f) for f in (camp.get("flags") or [])]
    have = {f.split("=")[0] for f in flags if "=" in f}
    for k, v in (
        ("water:source", str(SOURCE_N)),
        ("water:work", "0"),
        ("water:out", "0"),
        ("valve:source_work", "closed"),
        ("valve:work_out", "closed"),
    ):
        if k not in have:
            flags.append(f"{k}={v}")
    camp["flags"] = list(dict.fromkeys(flags))


def _flag_map(camp: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for f in camp.get("flags") or []:
        s = str(f)
        if "=" in s:
            k, v = s.split("=", 1)
            out[k] = v
    return out


def _write_map(camp: dict[str, Any], m: dict[str, str]) -> None:
    keep = [str(f) for f in (camp.get("flags") or []) if "=" not in str(f)]
    for k, v in m.items():
        keep.append(f"{k}={v}")
    camp["flags"] = list(dict.fromkeys(keep))


def heights(camp: dict[str, Any]) -> dict[str, int]:
    m = _flag_map(camp)
    def n(k: str) -> int:
        try:
            return max(0, int(m.get(k, "0")))
        except (TypeError, ValueError):
            return 0
    return {
        "source": n("water:source"),
        "work": n("water:work"),
        "out": n("water:out"),
    }


def valves(camp: dict[str, Any]) -> dict[str, str]:
    m = _flag_map(camp)
    return {
        "source_work": m.get("valve:source_work", "closed"),
        "work_out": m.get("valve:work_out", "closed"),
    }


def cheated(camp: dict[str, Any]) -> bool:
    return any(str(f).lower() in ("cheat:bucket", "cheat") for f in (camp.get("flags") or []))


def scorched(camp: dict[str, Any]) -> bool:
    return any(str(f).lower().startswith("nuke:") or str(f).lower() == "scorched"
               for f in (camp.get("flags") or []))


def phase(camp: dict[str, Any]) -> str:
    return str(_flag_map(camp).get("water:phase") or "liquid").lower()


def _n(camp: dict[str, Any], key: str) -> int:
    try:
        return max(0, int(_flag_map(camp).get(key, "0")))
    except (TypeError, ValueError):
        return 0


def steam_n(camp: dict[str, Any]) -> int:
    return _n(camp, "steam")


def rain_n(camp: dict[str, Any]) -> int:
    return _n(camp, "water:rain")


def ice_n(camp: dict[str, Any]) -> int:
    return _n(camp, "water:ice")


def charge_n(camp: dict[str, Any]) -> int:
    return _n(camp, "charge")


def mass(camp: dict[str, Any]) -> int:
    h = heights(camp)
    return h["source"] + h["work"] + h["out"] + steam_n(camp) + rain_n(camp) + ice_n(camp)


def won(camp: dict[str, Any]) -> bool:
    if phase(camp) in ("gas", "rain", "ice"):
        return False
    h = heights(camp)
    return (not cheated(camp)) and h["out"] >= WIN_OUT and any(
        str(f).startswith("flowed") for f in (camp.get("flags") or [])
    )


def sight_glass(camp: dict[str, Any]) -> str:
    h = heights(camp)
    v = valves(camp)

    def bar(n: int) -> str:
        n = max(0, min(SOURCE_N, n))
        return BAR * n + EMPTY * (SOURCE_N - n)

    lines = [
        f"SOURCE {bar(h['source'])} {h['source']}",
        f"WORK   {bar(h['work'])} {h['work']}",
        f"OUT    {bar(h['out'])} {h['out']}",
        f"A {v['source_work']}  B {v['work_out']}",
    ]
    ph = phase(camp)
    ch = charge_n(camp)
    charge_bit = f" | CHARGE {bar(min(SOURCE_N, ch))} {ch}" if ch else ""
    if ph == "ice":
        return " | ".join([
            f"ICE    {bar(ice_n(camp))} {ice_n(camp)}",
            f"SOURCE {bar(h['source'])} {h['source']}",
            "GLASS: frozen. Gravity waits on the season.",
        ]) + charge_bit
    if ph == "rain" or rain_n(camp) > 0:
        return " | ".join([
            f"RAIN   {bar(rain_n(camp))} {rain_n(camp)}",
            f"STEAM  {bar(steam_n(camp))} {steam_n(camp)}",
            f"SOURCE {bar(h['source'])} {h['source']}",
            "GLASS: rain falls. Drop → wheel → charge. Water returns.",
        ]) + charge_bit
    if ph == "gas":
        p = steam_n(camp)
        return " | ".join([
            f"STEAM  {bar(p)} {p} atm",
            f"RAIN   {bar(rain_n(camp))} {rain_n(camp)}",
            "GLASS: pressure. Wait — steam becomes rain. Gravity is not fired; it is queued.",
        ]) + charge_bit
    if scorched(camp) and mass(camp) <= 0:
        return " | ".join([
            "SOURCE ???",
            "WORK   ???",
            "OUT    ???",
            "GLASS: SHATTERED — fireball. Find the water. It changed phase.",
        ])
    if cheated(camp):
        lines.append("GLASS: DISPUTED — bucket. Nothing was computed.")
    elif won(camp):
        lines.append("GLASS: height earned. Gravity did the work.")
    else:
        lines.append("GLASS: height is the computation. Bucket is a lie.")
    return " | ".join(lines)


def glance(camp: dict[str, Any]) -> str:
    room = ((camp.get("module_snapshot") or {}).get("rooms") or {}).get(camp.get("room_id")) or {}
    name = str(room.get("name") or "Gallery")
    return name + ". " + sight_glass(camp)


def to_gas(camp: dict[str, Any]) -> dict[str, Any]:
    """Phase change. Mass conserved. Height stops being the instrument."""
    seed(camp)
    if phase(camp) == "gas":
        return {
            "ok": True,
            "handled": True,
            "events": [
                "It already is a gas. You were looking at a height glass in a steam room.",
                sight_glass(camp),
            ],
        }
    h = heights(camp)
    qty = mass(camp) or steam_n(camp)
    if qty <= 0 and scorched(camp):
        qty = SOURCE_N
    if qty <= 0:
        return {"ok": False, "handled": True, "error": "nothing to boil — tanks dry"}
    m = _flag_map(camp)
    m["water:source"] = "0"
    m["water:work"] = "0"
    m["water:out"] = "0"
    m["water:phase"] = "gas"
    m["steam"] = str(qty)
    _write_map(camp, m)
    return {
        "ok": True,
        "handled": True,
        "events": [
            f"The water becomes gas. {qty} marks of mass, now pressure.",
            "Height was the wrong instrument. Gravity cannot read steam.",
            sight_glass(camp),
            "Wait. Steam becomes rain. Physics is still in play.",
        ],
    }


def fireball(camp: dict[str, Any]) -> dict[str, Any]:
    """Nuke the analog computer. Mass becomes unmeasured steam. Height-glass dies."""
    seed(camp)
    qty = mass(camp) or steam_n(camp) or SOURCE_N
    m = _flag_map(camp)
    m["steam"] = str(qty)
    m["water:source"] = "0"
    m["water:work"] = "0"
    m["water:out"] = "0"
    m["valve:source_work"] = "closed"
    m["valve:work_out"] = "closed"
    _write_map(camp, m)
    flags = list(camp.get("flags") or [])
    flags.append("nuke:fireball")
    flags.append("scorched")
    camp["flags"] = list(dict.fromkeys(flags))
    return {
        "ok": True,
        "handled": True,
        "events": [
            "You throw the fireball into the tanks.",
            "Glass goes first. Water flashes to nothing you can measure. Pipes scream and then do not.",
            "The plaque blacks. Height cannot be read.",
            sight_glass(camp),
            "This is not a win. You killed the referee.",
        ],
    }


def freeze(camp: dict[str, Any]) -> dict[str, Any]:
    seed(camp)
    liquid = mass(camp) - steam_n(camp) - rain_n(camp) - ice_n(camp)
    falling = rain_n(camp)
    qty = liquid + falling + ice_n(camp)
    if qty <= 0:
        if steam_n(camp) > 0:
            return {"ok": False, "handled": True, "error": "steam must rain before it can freeze"}
        return {"ok": False, "handled": True, "error": "nothing to freeze"}
    m = _flag_map(camp)
    m["water:source"] = "0"
    m["water:work"] = "0"
    m["water:out"] = "0"
    m["water:rain"] = "0"
    m["water:ice"] = str(qty)
    m["water:phase"] = "ice"
    _write_map(camp, m)
    return {
        "ok": True,
        "handled": True,
        "events": [
            f"The water freezes. {qty} marks of ice. Flow stops. Charge stays.",
            sight_glass(camp),
            "Wait — the season turns. Melt starts the process over.",
        ],
    }


def gravity_tick(camp: dict[str, Any]) -> list[str]:
    """One physics tick. Steam→rain→charge+source; ice→melt; liquid→gravity."""
    seed(camp)
    m = _flag_map(camp)
    steam, rain, ice = steam_n(camp), rain_n(camp), ice_n(camp)
    h = heights(camp)
    charge = charge_n(camp)
    ph = phase(camp)
    events: list[str] = []

    if steam > 0:
        steam -= 1
        rain += 1
        m["steam"] = str(steam)
        m["water:rain"] = str(rain)
        m["water:phase"] = "gas" if steam > 0 else "rain"
        _write_map(camp, m)
        events.append("Steam becomes rain.")
        events.append(sight_glass(camp))
        return events

    if rain > 0:
        rain -= 1
        h["source"] += 1
        charge += 1
        m["water:rain"] = str(rain)
        m["water:source"] = str(h["source"])
        m["charge"] = str(charge)
        m["water:phase"] = "rain" if rain > 0 else "liquid"
        _write_map(camp, m)
        events.append("Rain falls. A wheel turns. Electrical energy. Water in SOURCE.")
        if rain == 0:
            events.append("Height can be read again. The process did not end.")
        events.append(sight_glass(camp))
        return events

    if ph == "ice" or ice > 0:
        ice -= 1
        h["source"] += 1
        m["water:ice"] = str(ice)
        m["water:source"] = str(h["source"])
        m["water:phase"] = "ice" if ice > 0 else "liquid"
        _write_map(camp, m)
        events.append("Ice melts. SOURCE rises. The process starts over.")
        if ice == 0:
            events.append("Liquid. Valves. Gravity. Same computer.")
        events.append(sight_glass(camp))
        return events

    h = heights(camp)
    v = valves(camp)
    moved = []
    if v["source_work"] == "open" and h["source"] > 0:
        h["source"] -= 1
        h["work"] += 1
        moved.append("source→work")
    if v["work_out"] == "open" and h["work"] > 0:
        h["work"] -= 1
        h["out"] += 1
        moved.append("work→out")
    m = _flag_map(camp)
    m["water:source"] = str(h["source"])
    m["water:work"] = str(h["work"])
    m["water:out"] = str(h["out"])
    _write_map(camp, m)
    flags = list(camp.get("flags") or [])
    if moved:
        flags.append("flowed")
        camp["flags"] = list(dict.fromkeys(flags))
        events = ["Gravity. " + ", ".join(moved) + "."]
    else:
        events = ["Gravity. Nothing moves. A valve is closed, or a tank is dry."]
    events.append(sight_glass(camp))
    if won(camp):
        events.append("The output height is yours. You walked the water here.")
    return events


def _valve_here(camp: dict[str, Any]) -> str | None:
    rid = str(camp.get("room_id") or "")
    return VALVE_AT.get(rid)


def set_valve(camp: dict[str, Any], want: str) -> dict[str, Any]:
    seed(camp)
    which = _valve_here(camp)
    if not which:
        return {"ok": False, "handled": True, "error": "no valve in this room"}
    want = "open" if want in ("open", "on") else "closed"
    m = _flag_map(camp)
    key = "valve:" + which
    m[key] = want
    _write_map(camp, m)
    label = "A" if which == "source_work" else "B"
    return {
        "ok": True,
        "handled": True,
        "events": [f"Valve {label} {want}.", sight_glass(camp)],
    }


def pour_bucket(camp: dict[str, Any]) -> dict[str, Any]:
    seed(camp)
    rid = str(camp.get("room_id") or "")
    inv = [str(x).lower() for x in ((camp.get("player") or {}).get("inventory") or [])]
    if "bucket" not in inv and not any("bucket" in x for x in inv):
        return {"ok": False, "handled": True, "error": "no bucket in hand"}
    if rid != "out_cistern":
        return {
            "ok": True,
            "handled": True,
            "events": ["The bucket wants the output tank. Pouring anywhere else is just a mess."],
        }
    m = _flag_map(camp)
    m["water:out"] = str(SOURCE_N)
    _write_map(camp, m)
    flags = list(camp.get("flags") or [])
    flags.append("cheat:bucket")
    camp["flags"] = list(dict.fromkeys(flags))
    return {
        "ok": True,
        "handled": True,
        "events": [
            "You pour. OUT fills. The height is a lie. Nothing was computed.",
            sight_glass(camp),
            "This is not a win. Physics did not run.",
        ],
    }


def hire_tick(camp: dict[str, Any]) -> list[str]:
    """AFK hireling: one gravity tick. Check valve — they cannot pour."""
    events = ["Pump-Janitor ticks once. Check valve holds. They do not pour."]
    events.extend(gravity_tick(camp))
    return events


def handle(camp: dict[str, Any], action: dict[str, Any], *, atype: str, raw: str) -> dict[str, Any]:
    """Take over water-specific verbs. Return handled False to let the campaign engine proceed."""
    if not is_module(camp):
        return {"handled": False}
    seed(camp)
    atype = (atype or "").lower()
    raw_l = (raw or "").lower()
    blob = (raw_l + " " + atype + " " + str(action.get("target") or "")).lower()
    if atype == "freeze" or "freeze" in blob:
        return freeze(camp)
    if atype in ("boil", "steam", "gas") or any(
        w in blob for w in ("into gas", "into a gas", "evaporat", "boil", "steam")
    ):
        if "fireball" not in blob and "nuke" not in blob and "freeze" not in blob:
            return to_gas(camp)
    if atype in ("fireball", "nuke") or "fireball" in blob or (atype == "act" and "fireball" in blob):
        return fireball(camp)
    if atype in ("open", "close"):
        return set_valve(camp, "open" if atype == "open" else "closed")
    if atype == "pour" or (atype == "use" and "bucket" in raw_l):
        return pour_bucket(camp)
    if atype == "use" and any(w in raw_l for w in ("valve", "pipe", "gate")):
        want = "close" if "close" in raw_l else "open"
        return set_valve(camp, want)
    if atype == "use":
        if _valve_here(camp):
            return set_valve(camp, "open")
        if str(camp.get("room_id") or "") == "out_cistern":
            return pour_bucket(camp)
        return {"handled": False}
    if atype == "wait":
        return {"ok": True, "handled": True, "events": ["You wait."] + gravity_tick(camp)}
    if atype == "work":
        return {"ok": True, "handled": True, "events": ["You crank the pump."] + gravity_tick(camp)}
    return {"handled": False}


def after(camp: dict[str, Any], atype: str, events: list[str],
          action: dict[str, Any] | None = None) -> list[str]:
    """Append glass / hireling tick after generic look/rest/talk."""
    if not is_module(camp):
        return events
    seed(camp)
    extra: list[str] = []
    if atype in ("look", "status", "help"):
        blob = " ".join(str(e) for e in events)
        if "SOURCE" not in blob and "GLASS" not in blob:
            extra.append(sight_glass(camp))
    elif atype == "rest":
        extra.append("Time passes in the pipes.")
        extra.extend(gravity_tick(camp))
    elif atype == "talk":
        tgt = str((action or {}).get("target") or "").lower()
        blob = (tgt + " " + " ".join(str(e) for e in events)).lower()
        if "janitor" in blob or "pump" in blob:
            extra.extend(hire_tick(camp))
    return list(events) + extra


def extra_legal(camp: dict[str, Any]) -> list[dict[str, Any]]:
    if not is_module(camp):
        return []
    acts = [{"type": "wait"}, {"type": "work"}]
    if _valve_here(camp):
        acts.extend([{"type": "open"}, {"type": "close"}])
    if str(camp.get("room_id") or "") == "out_cistern":
        acts.append({"type": "pour"})
    return acts


def extra_paths(camp: dict[str, Any]) -> list[dict[str, str]]:
    if not is_module(camp):
        return []
    paths = [{"label": "Look at the glass", "text": "look"}]
    if _valve_here(camp):
        paths.append({"label": "Open the valve", "text": "open valve"})
        paths.append({"label": "Close the valve", "text": "close valve"})
    paths.append({"label": "Wait (gravity)", "text": "wait"})
    if str(camp.get("room_id") or "") == "out_cistern":
        paths.append({"label": "Pour the bucket (cheat)", "text": "pour bucket"})
    return paths[:4]


def _play_demo() -> dict[str, Any]:
    from mag.game_campaign import apply_action, begin_play, parse_player_speech, set_character, parse_character

    b = begin_play(module_id="water_computer", voice_session_id="water-demo", force_new=True)
    cid = str(b.get("campaign_id") or (b.get("campaign") or {}).get("campaign_id") or "")
    if b.get("need_character"):
        set_character(cid, parse_character("I'm Ash a curious engineer"))
    steps = []
    for line in (
        "look",
        "go west",
        "open valve",
        "wait",
        "wait",
        "go east",
        "go east",
        "open valve",
        "wait",
        "wait",
        "look",
    ):
        act = parse_player_speech(line) or {"type": "look"}
        r = apply_action(cid, act)
        steps.append({"line": line, "ok": r.get("ok"), "narrate": (r.get("narrate") or "")[:220]})
    from mag.game_campaign import load_campaign

    camp = load_campaign(cid) or {}
    return {
        "ok": True,
        "schema": SCHEMA,
        "campaign_id": cid,
        "won": won(camp),
        "cheated": cheated(camp),
        "glass": sight_glass(camp),
        "steps": steps,
    }


def main(argv: list[str] | None = None) -> int:
    a = list(argv or sys.argv[1:])
    cmd = (a[0] if a else "play").lower()
    if cmd == "demo":
        print(json.dumps(_play_demo(), ensure_ascii=False, indent=2))
        return 0
    from mag.game_campaign import begin_play, load_campaign, latest_for_session

    if cmd == "glass":
        camp = latest_for_session("water-cli") or latest_for_session("water-demo")
        if not camp:
            print(json.dumps({"ok": False, "error": "no water campaign"}))
            return 1
        print(json.dumps({"ok": True, "glass": sight_glass(camp), "won": won(camp), "cheated": cheated(camp)}))
        return 0
    b = begin_play(module_id="water_computer", voice_session_id="water-cli", force_new=True)
    cid = str(b.get("campaign_id") or (b.get("campaign") or {}).get("campaign_id") or "")
    camp = load_campaign(cid) or b.get("campaign") or {}
    print(json.dumps({
        "ok": bool(b.get("ok")),
        "campaign_id": cid,
        "speak": (b.get("speak") or "")[:400],
        "glass": sight_glass(camp) if camp else "",
        "legal": [a.get("type") for a in (b.get("legal") or [])][:12],
        "note": "Say water one in Talk, or: go west / open valve / wait / pour bucket",
    }, ensure_ascii=False, indent=2))
    return 0 if b.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
