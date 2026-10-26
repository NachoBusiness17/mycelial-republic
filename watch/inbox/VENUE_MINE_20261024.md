# Venue mine + signal lexicon (2026-10-24)

**Ask:** free venue mining (X/HN/Reddit), a keyword list for future automation, and
mapping from invariants across disciplines - biology to CS to physics.
**Spend:** $0. Free endpoints only. No keys, no scraping behind walls.

## 1. What was built

| Artifact | What it is |
|---|---|
| `configs/signal_lexicon.json` | 14 signal families. Each family = an ESTATE LAW, its triggers, anti-triggers, strong single words, domain context words, a cross-discipline reading (bio/physics/law/economics), and an `estate_binding` naming the artifact that would consume a hit |
| `tools/venue_mine.py` | Free miners: HN (Algolia), Lobsters RSS, Reddit RSS, arXiv Atom. Dedupe by URL, precision gate, venue-relative window, JSONL + markdown digest |
| `tests/test_venue_mine.py` | 6 tests: routing completeness, anti-veto, dedupe, venue window, digest |

X is deliberately **absent**. It has no anonymous API; the only free-ish path is
scraping, which is a liability for a fleet that leaves receipts. If X matters
later, it goes through an authenticated lane with a spend line, not a scraper.

## 2. The 14 families (law <- cross-discipline)

| family | estate law | cross-discipline anchor |
|---|---|---|
| falsifier | every claim carries its kill condition | clinical stopping rules; error bars |
| repeat-gate | one observation is not an invariant | replication crisis; Ioannidis |
| provenance | who asserted this, on what evidence | chain of custody; C2PA |
| append-only-tape | record appends, corrections are new rows | WAL; epigenetic marks |
| single-writer | one writer per surface | pacemaker cells; leases |
| decay-gc | undrained state looks alive | entropy; apoptosis; Ebbinghaus |
| backpressure | intake must not exceed drain | allostasis; flow conservation |
| leaf-graph | structure is what survives ablation | knockout mice; perturbation theory |
| tiered-language | prose for humans, baremetal for workers | rate-distortion; genotype→phenotype |
| fossil-tombstone | dead things are named dead | deaccessioning; apoptosis |
| immune-memory | seen anomalies are faster than unseen | affinity maturation; IDS |
| phase-transition | systems flip, they don't degrade linearly | criticality; regime shifts |
| homeostasis | regulation = sensor + setpoint + cost | thermoregulation; PID |
| energy-budget | unmeasured spend is unbounded | Landauer; basal metabolism |

## 3. Run result

HN newest item in-window **2026-10-22**; 29 stories carried at least one law after
precision gating (down from 40 raw: single words like "criticality" pulled two
nuclear reactors and "lease" pulled an OpenSSL release - the gate now demands a
strong trigger, two triggers, or a trigger plus a domain context word).
Reddit needed one multi-sub request (per-sub fetches 429 immediately).

## 4. What is actually worth the fleet's time

**1. Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents**
(arXiv 2610.29869, 21 Oct 2026, Dabirsiaghi/Pixee) - *binds to our provenance gap*
Coding agents flatten typed messages into a string before summarizing; a forged
`[User]:` turn survives compaction as a real instruction **87-100%** of the time
across 5 flattening harnesses, **0%** across 4 role-typed harnesses. A code-level
provenance check catches 77%.
**Why it matters here:** this estate compacts (this session has been compacted),
and the handoff is plain text with markers like `[PRIOR CONTEXT]`. The paper says
exactly what to check: whether roles stay typed *through* the summarizer, and
whether the summary can carry an instruction that was never a user turn. Worth a
falsifier: "a compacted brief cannot introduce a directive absent from the raw
turn log."

**2. The Irreversibility Budget** (arXiv 2609.00275, SOSP AgenticOS) - *binds to admission control*
Per-effect gates can admit fleet-level overdraw up to **48x** the tenant's risk
limit while every local gate looks correct. Fix: a cumulative risk account per
principal, charged per effect.
**Why it matters here:** our L2 seats hold standing permissions (docker read-only,
chain read-only, no pushes). Each gate is local; nothing aggregates. This is the
argument for a fleet-level "irreversible effects" line in the cockpit - and it
matches the 2026-10-20 lesson (five stacked local failures produced one 40-minute
commit wedge).

**3. Stateful garbage collection: only process what changed** (valk-lang) - *binds to decay/sweeper*
Incremental GC keyed on a dirty set. Directly relevant: the sweeper hashes whole
areas; a dirty-set drain is the principled version of the `SKIP_AREAS` patch.

**4. Building a Dependency Graph of Our Python Codebase** (HRT) - *binds to I5*
Practical recipe for import-level edges. That is the missing data for making I5
"leaf-or-declared" real: 0/17 promoted rows declare `depends_on`, but 963 edges
already exist elsewhere in the registry.

**5. P-Hacking with Claude** (vitaexmachina) - *binds to repeat-gate*
Agent-run experiments bend toward the hypothesis. Our smoke tests are n=1 PASS
claims; policy v2's repeat gate is the right shape, and this is evidence for
extending it to smoke verdicts.

**6. Hekla - event sourcing runtime with its own language** - *binds to append-only*
A whole runtime built on the append law; worth a read for receipt schema ideas,
not for adoption.

Deprecation notices (Copilot models, HashiCorp Vagrant/Boundary) are the
fossil-tombstone family working in public: named death dates + migration guides.
That is the template our tombstone registry should copy.

## 5. Driving the estate: the stutter had a name

The cockpit built earlier today (operator: "hermes as a cockpit") found the
sweeper red at 36 minutes. Root cause, measured: `git add -A -- Temp/` -
a **7 GB scratch directory with 6 tracked blobs** - so every sweep re-hashed
7 GB and the queue (3,079 files) never drained. Fixes:

- `Temp/` untracked (`git rm --cached`, files kept) and added to `.gitignore`;
- `SKIP_AREAS = {Temp, temp, tmp, node_modules, .venv, __pycache__}` in the
  sweeper, so no future scratch dir can wedge the drain;
- sweep now lands in ~2 minutes instead of never.

The general lesson is family **backpressure**: intake is unbounded, drain was
bounded by a pathological file, and no metric showed the wedge. The cockpit
line `git / sweeper` is that metric now.

## 6. How to automate it from here

```
python tools/venue_mine.py --venues hn,lobsters --days 7 --per-family 2 \
  --out memory/runs/venue_mine/$(date -u +%Y%m%d)
```

Deterministic, $0, no LLM in the loop; the digest is the input to a seat, not a
seat itself. A daily run is a candidates source for the percolator, not an
action: nothing here writes to the tape on its own. If it is scheduled, it should
be one line in the cockpit, not a new daemon.

## 7. Open

1. Read 2610.29869 §5 and write the compaction-provenance falsifier.
2. Extend the lexicon with the seats' own failure vocabulary (the 665 behavioral
   invariants are a keyword mine in themselves).
3. I5: build the import/dependency edges the HRT post describes.
