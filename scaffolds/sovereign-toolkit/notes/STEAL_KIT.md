# THE STEAL KIT — how to build a self-running sovereign system

> **For:** AdventureNLearn — Objective Thinking is the Process, Growth is the Goal.
> **From:** Nacho's sovereign build (shared 2026-08-20).
> **The point:** You don't need our info or our secrets. You need the *method* —
> how to steal mechanisms from other systems and adapt them to your own, the same
> way we had to for ours. This is the how-to. Nothing here is private; everything
> here is meant to be taken and adapted. Contracts only — never copy someone's
> inner contents; steal their *machinery*.

---

## 0. The one law that governs all of it

> **Steal the mechanism, never the content.**
> Adapt a working *pattern* to your own deterministic, architecture-native shape.
> Contracts and design laws are meant to be shared and improved. Someone's private
> data, persona, or inner state is never the thing to take — it's not portable anyway.

This is the whole discipline in one line. Everything below is that law unfolded.

---

## 1. The universal build shape (5-part op template)

Any operation you want the system to own — deploy, publish, fetch, ship, steer —
turns into one repeatable shape:

1. **Safety check** — gate on *real* bad values (secret fingerprints like `sk-…`,
   `ghp_…`, private-key markers), never on prose words. OPSEC docs legitimately *name*
   the gates; word-hits are advisory, real secrets are fatal.
2. **Precondition check** — block on unfinished inputs (placeholders, missing fields)
   before anything touches the outside world.
3. **Assemble** (dry by default) — build the artifact without side effects.
4. **Publish** (dry by default; `--live` opt-in) — the external action, gated on creds.
5. **Learn** — measure the outcome and fold a decision, so every automation gets smarter
   and the failure modes become known.

The payoff: **dry-run by default catches the real blocker before ship.** The gate
protects you from your own unfinished input — the most common failure is you.

---

## 2. Architecture patterns that make it self-running

These are the mechanisms that let a system run itself instead of waiting on you:

- **Cheap-first routing.** Cheapest capable tier unless the goal needs frontier
  reasoning. Scarce/frontier compute is the expensive resource; cheap/owned compute
  carries the routine load.
- **The queue + drainer.** Work you can defer goes into a queue; a drainer eats it
  headless, in order, without asking. Async-able work is never done inline.
- **The autonomous cadence.** A governor/reconciler loop runs on a schedule — a passive
  warning sweep, a maintenance pass — committing its own state. The system maintains
  itself on a cadence whether or not anyone is watching. This is what "sovereign"
  means operationally: it keeps itself alive.
- **Content-addressed memory.** State is written once and referenced by its hash (a
  chain, a ledger) — append-only, verifiable, replayable. Identity lives in the
  *invariant* (the committed structure), not in a mutable blob.
- **State-first, LLM-last.** The deterministic engine owns truth (math, legality,
  ledger, dice). The model narrates/acts *after* the state is fixed. The model is the
  paint, never the load-bearing wall.
- **The supervisor container.** Persist the shared world-state (the one thing that
  must survive); make the workers ephemeral containers. The walls persist, the dwarves
  come and go.

---

## 3. The disciplines (how to keep it honest)

- **Trust bytes, not reports.** Verify that what you built actually does what it says —
  freeze a spec, then check the finished piece against it. Never claim "done" on
  unverified work. The module-level false-success guard.
- **Steer-first, not patch-first.** Before reaching for a workaround/failover/fallback,
  NAME THE REAL CONSTRAINT. Is the fix addressing the actual thing (a hard cap, a
  scope, a cost), or papering over a symptom? Point at the real constraint and let the
  fix derive from it.
- **Self-steal before you build.** Audit what you ALREADY own before building anything.
  Then steal externally and adapt. Never skip the external sweep just because something
  is already "inside your walls."
- **The real bill is the authority.** When you can, ground estimates against the actual
  cost/authority — not partial logs that can mislead. Correct over-claims explicitly.
  Honesty over over-claiming.
- **Rightsize constantly.** Match the resource to the task shape, not to habit.
- **Objective over resonant.** The coldest truth wins over the most compelling story.
  This is "Objective Thinking is the Process."

---

## 4. The economics that changed the game (a real, measured one)

The technique: make the cheap/owned side carry the routine load and cache aggressively.

A measured instance: tens of thousands of remote calls through a cache-mining router
ran at **~98% cache hit** — real spend in the **low single digits of dollars** for a
workload whose uncached, frontier-equivalent path would have been **~$100–400+**.
Same workload, one order of magnitude apart, purely from routing + caching discipline.

The takeaway is portable: **it's not about which model you use, it's about how you
shape the ask and where you let it execute.** The cheap side can carry almost all of
the load if you represent the work right.

---

## 5. How to adapt this to YOUR system (the recipient's shape)

1. **Find your cheap/owned substrate** — the compute or service you already pay for
   or run, and make it the default carrier.
2. **Build the 5-part shape for your first operation** — the one you're currently
   running by hand. That's the beachhead.
3. **Wire one cadence** — a single scheduled pass that maintains your state without
   being asked. One is enough to change the character of the system.
4. **Freeze one spec and verify it** — pick one finished piece, write what it should
   do, and actually check it. That installs the honesty loop.
5. **Steal one external mechanism** — find a system doing something you want, extract
   its *pattern*, adapt it to your shape. Never wholesale-copy; always adapt.

Do those five and you have a sovereign skeleton: a system that routes, queues, runs
itself on a cadence, verifies its own work, and improves from every operation.

---

*Take the machinery. Leave the contents. Build your own. — N.*
