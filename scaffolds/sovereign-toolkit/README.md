# Sovereign Toolkit — crown jewels for the Mycelial Republic

A forkable, pure-stdlib exchange pack: the mechanisms we believe **nobody really has but
us**, distilled so a prolific creator can **take them, run them, and enhance them to his
own needs**. Part of the exchange of ideas in the Mycelial Republic.

**Nothing here is private.** No secrets, no runtime memory, no repo contents. Only the
machinery, made portable. Take it. Steal it. Make it yours.

---

## What's in the pack

| Tool | Module | What it does | The idea |
|------|--------|--------------|----------|
| **Stateless Boot** | `stateless_boot.py` | Render a fresh worker's *frozen prefix* from current tools/interfaces/live-truth | A worker is born fresh — no persona, no history. It holds the machine, not the person. Workers die; the wave persists. |
| **MemLance** | `memlance.py` | Index real memory bytes, *select* the relevant grounded states, with a deterministic verified/derived verdict | Don't load everything — lance only the relevant leaves. Anti-hallucination by construction: only real bytes, flagged when ungrounded. |
| **Verkle Knot** | `verkle_knot.py` | A content-addressed, append-only, hash-linked chain of commits | Every commit references its parent root; state is replayable and verifiable. "Disk is law" made structural. |

---

## Run it (zero friction)

```sh
# from this directory
python -m pytest tests/ -q        # no installs, no deps
```

Each module also has a `__main__` so you can run it directly:

```sh
python stateless_boot.py
python memlance.py
python verkle_knot.py
```

---

## The one law

> **Steal the mechanism, never the content.**
> Adapt a working *pattern* to your own deterministic, architecture-native shape.
> Contracts and design laws are meant to be shared and improved. Someone's private data
> or persona is never the thing to take — it's not portable anyway.

---

## How to make these YOURS (enhance, don't just run)

1. **Stateless Boot** — feed it your own `tools`, `interfaces`, and `live_truth`. The
   frozen prefix is the clean-slate contract: give a fresh agent the machine, not the
   accumulated self. Wire it to your own launch path.
2. **MemLance** — point `index()` at *your* memory roots. Add your own grounding markers
   to `VERIFIED_MARKERS` / `UNVERIFIED_MARKERS`. The selection is deterministic keyword
   relevance — swap in your own scoring if you like.
3. **Verkle Knot** — this is the substrate. Append your own state as knots; the hash
   chain gives you verifiable, replayable, append-only memory for free. Point it at any
   directory.

The three compose: **stateless boot** spawns a fresh worker, **memlance** selects what
it should remember (grounded only), and **verkle knot** commits what it learned so the
wave persists even though the worker died.

---

## The disciplines these encode (keep them)

- **Trust bytes, not reports.** Verify what you built against a frozen spec. Never claim
  "done" on unverified work.
- **Objective over resonant.** The coldest truth wins over the most compelling story.
- **Self-steal before you build.** Audit what you already own first; then steal
  externally and adapt.

*Take the machinery. Leave the contents. Build your own.*
