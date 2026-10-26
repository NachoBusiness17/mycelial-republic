"""build_seed — assemble the shippable method package (seed/) and seal it.
2026-09-25, operator's ends: "what I want people to have is the method, not my version of it."
The seed = the laws + the engines (method as runnable code) + first boot + handoff, sealed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "seed"

STAMP = """

---

*Stamped 2026-09-25 by the falsifier run: a card of FACTS built from these laws scored 1/12
on held-out questions — the laws transfer as LAWS, not as pre-computed answers. This page is
the law, not the memory. The memory regrows from the record engines below.*
"""

FIRST_BOOT = """# FIRST BOOT — for a stranger holding this seed

You are holding a method, not a product. It is small on purpose. Here is your first hour.

1. **Read THE_METHOD.md** (one page, 11 laws). You will violate some of them in your first
   week. That is what the meters are for.
2. **Run the smith chart on nothing:** `python engines/estate_smith_chart.py` — it will tell
   you honestly that you have no records yet. That is your zero state. Gamma = 1 is normal.
3. **Declare your keys** in one JSON manifest (one manifest, one loader — copy the shape from
   engines/key_law.py). Never let a key name be guessed twice.
4. **Index what you have.** The spine pattern (engines/estate_atlas.py) walks your files and
   writes one JSONL line per file. That index is the map. It regenerates — it is never
   hand-maintained.
5. **Start one record.** Markdown, append-only, receipted: who, when, where, evidence. A claim
   not in a record didn't happen.
6. **Schedule the cooker.** Every free lane you have (any provider with a free tier) gets a
   reset time in engines/cooker.py, and an hourly task fires work at each refill. Your
   compute burns by default, not by willpower.
7. **Answer the daily question:** did the meters move? If a meter can't move, you built prose,
   not a meter. Delete it and build the meter.

The goal is not to reproduce the original estate. It is to grow YOUR estate under THESE laws.
The laws are the method; everything else is your version of it.
"""

HANDOFF = """# HANDOFF — what this seed is

This seed exists because of a measured result: on 2026-09-24/25 an attempt to ship this
estate as a page of pre-computed answers FAILED a held-out test (1/12) — the knowledge does
not transfer as facts. What transfers is the method: the laws (THE_METHOD.md), the engines
(engines/ — the method as runnable code), and the discipline (FIRST_BOOT.md).

The estate this came from: 63GB, 1.2M files, 3 years of human+AI operation, distilled here
to a handful of files. The stranger-continuation bar (G7): a stranger boots this seed and
continues without the original operator. That is the pass condition of this package.

Open-append records, hash-sealed freezes, loud-failing audits, meters over prose, the
operator's hand on transmit/delete/spend — the laws carry their own reasons. The seed is
small so that nothing in it is exempt from being read.
"""

ENGINES = [
    "mag/key_law.py", "mag/lite_guard.py", "mag/cooker.py", "mag/claritas.py",
    "mag/phone_relay.py", "mag/librarian_catalog.py", "tools/stealth_sweep.py",
    "tools/task_wall.py", "tools/estate_atlas.py", "tools/estate_smith_chart.py",
    "tools/model_bakeoff.py", "tools/build_seed.py",
]


def main() -> None:
    SEED.mkdir(exist_ok=True)
    (SEED / "engines").mkdir(exist_ok=True)

    card = (ROOT / "watch/inbox/method_card_exp/CARD_V1.md").read_text(encoding="utf-8")
    (SEED / "THE_METHOD.md").write_text(card + STAMP, encoding="utf-8")

    copied = []
    for src in ENGINES:
        p = ROOT / src
        if p.is_file():
            (SEED / "engines" / p.name).write_bytes(p.read_bytes())
            copied.append(p.name)

    (SEED / "FIRST_BOOT.md").write_text(FIRST_BOOT, encoding="utf-8")
    (SEED / "HANDOFF.md").write_text(HANDOFF, encoding="utf-8")

    lines = []
    for f in sorted(SEED.rglob("*")):
        if f.is_file() and f.name != "MANIFEST.sha256":
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            lines.append(f"{h}  {f.relative_to(SEED).as_posix()}")
    (SEED / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"SEED BUILT: {len(copied)} engines, {len(lines)} files sealed")


if __name__ == "__main__":
    main()
