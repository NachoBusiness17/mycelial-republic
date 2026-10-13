"""East/West ractor pairing on the DOE thorn kit + inroads play (RS pattern:
file separately, then compose per ti-yong)."""
from __future__ import annotations

import ipaddress, json, os, socket, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ROOT  # noqa: E402

OUT = ROOT / "memory" / "runs" / "elder_asks" / "RS_EASTWEST_THORN_20260920"
OBJECTS = [ROOT / "watch" / "inbox" / "THORN_KIT_20260920.md",
           ROOT / "memory" / "research_packs" / "INROADS_PLAY_SELF_STEAL_20260920.md"]
_API_URL = "https://api.deepseek.com/chat/completions"

WEST = ("You are the WEST lens (DC, the contract table). For every demand, claim, and "
        "open question in the object: (a) the missing contractual instrument, (b) the "
        "cheapest enforcement mechanism, (c) the repeal condition. Byte-level: verify the "
        "object's own citations and receipts where they can be checked internally; flag "
        "any number or claim lacking a row. Every falsifier must carry a threshold, a "
        "named runner, and an INCONCLUSIVE state so a null cannot masquerade as a pass. "
        "Addressed deltas only — numbered, terse, no prose ornaments.")

EAST = ("You are the EAST lens (AC, the walk). Read the object for what the "
        "falsifier-first lens skips: 正名 rectification of names (what is named that "
        "cannot testify; what testifies but is unnamed); 慎独 the scheduled walk (what "
        "needs a daily walk, not just a verify()); 知行合一 knowledge-action unity (what "
        "is known but not practiced); 和而不同 harmony without uniformity (where "
        "uniformity masquerades as harmony; the stranger is the 不同 the channel was dug "
        "for); the seed that waits a season (patience distinguished from excuse — write "
        "the season down). Terse, concrete, name the naming lags. Then the walk: what "
        "should be walked daily that is not.")

COMPOSE = ("You are the COMPOSE step (ti-yong 体用): a gate that refuses is function 用; a "
           "gate that logs is ritual 礼. Neither lens alone has the whole gate — the West "
           "table without the East walk is enforcement with no memory of why; the East "
           "walk without the West table is reverence with no refusal. From the two "
           "testimonies produce: (1) the binding rulings — what refuses, what logs, what "
           "walks, what waits; (2) the single composed order of operations for the next "
           "seven days; (3) one line on what must never be merged. Keep both banks "
           "distinct in the record.")


def _validated_api_url() -> str:
    parts = urllib.parse.urlsplit(_API_URL)
    if parts.scheme != "https" or parts.hostname != "api.deepseek.com":
        raise ValueError("unsanctioned API URL")
    for info in socket.getaddrinfo(parts.hostname, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            raise ValueError(f"blocked range: {ip}")
    return _API_URL


def ds(system: str, user: str) -> dict:
    from models.providers import get_provider, provider_keys
    keys = provider_keys(get_provider("deepseek") or {})
    if not keys:
        return {"ok": False, "error": "no key"}
    payload = {"model": "deepseek-chat", "temperature": 0.3, "max_tokens": 1100,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}]}
    req = urllib.request.Request(
        _validated_api_url(), data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {keys[0]}"},
        method="POST")
    for attempt in (0, 1):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read().decode("utf-8"))
            return {"ok": True, "text": ((data.get("choices") or [{}])[0].get("message", {})
                                         .get("content") or "").strip()}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(15); continue
            return {"ok": False, "error": f"HTTP {e.code}"}
        except Exception as e:  # noqa: BLE001
            if attempt == 0:
                time.sleep(5); continue
            return {"ok": False, "error": str(e)[:200]}
    return {"ok": False, "error": "429 x2"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    obj = "\n\n===\n\n".join(p.read_text(encoding="utf-8", errors="replace")[:9000] for p in OBJECTS)
    for name, sysmsg in (("WEST", WEST), ("EAST", EAST)):
        r = ds(sysmsg, f"OBJECT (two documents):\n\"\"\"\n{obj}\n\"\"\"\n\nTestify.")
        p = OUT / f"RS_{name}_THORN.md"
        if r["ok"]:
            p.write_text(f"# RS_{name}_THORN — view_through({name})\n\n{r['text']}\n", encoding="utf-8")
            print(f"[{name}] ok {len(r['text'])} chars", flush=True)
        else:
            print(f"[{name}] FAIL {r['error']}", flush=True)
            return
        time.sleep(1.0)
    west = (OUT / "RS_WEST_THORN.md").read_text(encoding="utf-8")
    east = (OUT / "RS_EAST_THORN.md").read_text(encoding="utf-8")
    r = ds(COMPOSE, f"WEST TESTIMONY:\n{west}\n\nEAST TESTIMONY:\n{east}\n\nCompose.")
    if r["ok"]:
        (OUT / "RS_COMPOSE_EAST_WEST.md").write_text(
            f"# RS_COMPOSE_EAST_WEST — thorn kit + inroads play\n\n{r['text']}\n", encoding="utf-8")
        print(f"[compose] ok {len(r['text'])} chars", flush=True)
    else:
        print(f"[compose] FAIL {r['error']}", flush=True)


if __name__ == "__main__":
    main()
