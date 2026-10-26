# THE CHUNKED CAMPAIGN — Astra in resumable asks (2026-09-09)

> **[AUDIT-TYPED]** status: STAGED · operator: "send it to Astra — it will
> probably fail eventually, so chunk it into smaller asks that build, like
> our Bernays driving" · the steal: durable execution (Google AX / Temporal)
> applied to the conversation — execution = durable state + resumable actor
> + interruption + replay · each ask = one RIB segment: compact,
> self-contained, resumable from any death · the failure mode (usage walls,
> context limits) becomes PAUSE, not loss.

## THE CHUNKING LAW

One ask per paste. Each paste = **RIB-so-far** (the campaign state, ≤150
words, written by Astra itself at the end of the previous chunk) + **one
new deliverable** + **the price**. Astra ends every chunk by writing its
own carry-forward blob. We transport the blob. Session death, usage walls,
model swaps — none of it kills the campaign; the next chunk resumes from
the blob. This is Bernays driving: small steering inputs, continuous
direction, cumulative without any single mega-ask.

## THE CAMPAIGN SEQUENCE (seven chunks)

**CHUNK 0 — THE SEED (calibration).** Paste: who we are (the verified-hobby
paragraph), the one-paragraph architecture (constitution-as-cache, epistemic
bus, materialized belief, durable executor, referee, receipt spine), and
the commission: "State in your own words what this system is FOR — one
paragraph. We fold disagreements into the design; we do not fold
misunderstandings." → Output: Astra's purpose-statement. CALIBRATION GATE:
if its restatement is wrong, the campaign pauses and we fix the seed.

**CHUNK 1 — THE RACE (F-COMM-1 pre-registered).** Paste: RIB + the four
conditions (cold / warm-typed / warm-free / desk) + the sham-task rule.
Ask: "Design the experiment to be immune to our self-deception: outcomes,
decision rules, sample floor, and the pre-registered program-ender." →
Output: the locked protocol.

**CHUNK 2 — THE CUPS (deletion semantics).** Paste: RIB + the three stores
(AUDIT/BELIEF/HEAD). Ask: "Spec the garbage collector: what BELIEF forgets,
what AUDIT keeps forever, the tombstone receipt fields, and the collector
schedule. Name the first way the GC gets gamed." → Output: deletion spec
v1.

**CHUNK 3 — THE REFEREE (liveness without sovereignty).** Paste: RIB +
the veto-only circuit-breaker pattern. Ask: "Design the smallest referee
that survives the operator sleeping: veto list, tripwires, liveness rules,
and its first failure mode." → Output: referee spec v1.

**CHUNK 4 — THE EVENT LAYER v2 (costimulation + staking + CCIR).** Paste:
RIB + the seven emissions + the price-vector principle. Ask: "Spec the
layer: schema, promotion gates, gaming defenses, and the price of each
epistemic verb." → Output: event layer spec v1.

**CHUNK 5 — THE MIGRATION HARNESS (constitution tuple).** Paste: RIB + the
(C, M, tokenizer, template, mapper, judge-pack) tuple + duty-spec gates.
Ask: "Design the migration harness: the conformance suite, the shadow
epoch, and what happens when the envelope cannot be preserved." → Output:
migration spec v1.

**CHUNK 6 — THE INTEGRATION (the route plan).** Paste: RIB + everything.
Ask: "Assemble the full system design document: the diagram, the build
order, the kill conditions per component, and the one thing you would cut."
→ Output: the deep system design doc, delivered as the campaign's summit.

**CHUNK 7 (standing) — THE RED TEAM.** The doc handed to a DIFFERENT model
family to attack. Findings fold back as chunk amendments.

## THE CAMP-STATE BLOB (the carry-forward format)

Each chunk ends with Astra writing:

```text
CAMP STATE v{n}
decided: [one line per locked decision]
open: [one line per unresolved question]
next: [the single most important open item]
```

We carry the blob verbatim into the next paste. The blob is the campaign's
RIB: compact, attributed (model + date), and honest about what is not yet
decided.

## RULES

1. One deliverable per chunk. If Astra exceeds scope, we fold the excess
   into the blob as "offered, not locked."
2. Every chunk's output is pinned to the campaign card the day it lands.
3. Usage walls are routing information: the chunk that died is the chunk
   to re-send first (durable execution semantics — interruption ≠ loss).
4. The red team (chunk 7) uses a different model family than chunks 0-6.
5. No chunk may add an organ the four-condition experiment has not
   justified — the wave-three stop rule, carried.
