# TOUR — what the estate does, and what carries it here

The seed came from a 63GB / 1.2M-file estate: three years of one human operating a
fleet of AI seats in Docker containers, remembering itself in a hash-chained record.
A tour of what it actually DOES, and where each capability lives for you:

| estate capability | carries into the seed as |
|---|---|
| keys declared once, audited daily, loud on drift | engines/key_law.py + configs/keys.json |
| every outbound call through one guarded door | engines/lite_guard.py |
| free compute burned on refills, unattended | engines/cooker.py (+ MORNING_LOOP.md) |
| the free-model wall scored daily | engines/stealth_sweep.py |
| cheap-model chores run as a standing wall | engines/task_wall.py + configs/chores.json |
| the health meter: gamma = 1 - delivered/claimed | engines/estate_smith_chart.py |
| the file index that regenerates, never hand-maintained | engines/spine_walk.py + engines/estate_atlas.py |
| approvals from a phone, fail-closed | engines/phone_relay.py |
| model prompts distilled from leaked frontier system prompts | engines/claritas.py |
| catalog + canon integrity checks | engines/librarian_catalog.py |
| decisions fought across independent seats | SALON.md |
| what data may leave the disk | DATA_TIERS.md |
| boot order for a fresh seat | FIRST_BOOT.md + AGENTS.md |
| the founding constitution's fork equality, handoff law | THE_METHOD.md (the 11 laws) |

What the seed deliberately does NOT carry: the estate's history (63GB of records —
you grow your own), its games and artifacts (built, yours to visit), its personal
workload (the chores were the author's; configs/chores.json is yours). The cache
is the author's; the cache MINER is what ships.
