# Frontier watch ruling — Rice invalidation question

Date: 2026-09-06. Producer: Codex frontier watch. Classification: PROPOSAL (ruling and unsent public draft), with a FACT counterexample below. No publication or implementation promotion is implied.

## Ruling

Accept forward cell-version dependencies for cached exact first-hit rays. Reject the unconditional O(1), one-comparison, zero-invalidation-work, and footprint-only distance-field claims. Agreement among witnesses is a proposed design; it does not establish correctness.

- A ray must record every cell along its segment through the first hit, including empty cells and the hit cell; a miss must have a finite range and record the cells through that range. Otherwise a new nearer wall can appear without changing a recorded dependency. Use consistent conservative rules at cell faces and corners.
- Bump cells covering old and new geometry on every geometry edit, including motion wholly within an occupied cell. The engine's authoritative mutation event supplies detection; arbitrary external changes still require an observation mechanism. Endpoint footprints are sufficient for queries on committed snapshots. Queries about continuous motion need the swept geometry.
- An update costs O(m) in touched cells; validation costs O(k) in a ray's dependencies. These are O(1) only with stated fixed bounds. Cell-level invalidation is conservative: rays sharing a changed cell can be recomputed even when their answers did not change. Recasting after removal can extend far beyond the former wall.
- A version in a cache key prevents reuse only if the version covers every relevant dependency. One global epoch is simple and safe with broad invalidation; an origin-region epoch can miss a change farther along the ray. Aggregating cell versions still needs work or a maintained index. In particular, max([9,2]) == max([9,3]) hides a change when independent counters are used.
- Read geometry and versions from one committed snapshot, or retry correctly on concurrent edits. Stamp neither old geometry with new versions nor partially published edits. Include all result-affecting query parameters in cache identity. Prevent generation wrap/reuse from reviving stale entries.
- A reverse index is a workload tradeoff: lazy forward validation avoids its update and storage cost; eager enumeration or heavy repeated validation can justify it. D* Lite concerns graph shortest-path costs and replanning, which differs from geometric ray-hit or signed-distance caching. It is not literally restricted to storing explicit paths.
- Preserve corrections and evidentiary history. Disposable derived cache entries may be evicted; keeping all old cache keys forever is not required to preserve the record.

The major missing distinction is a cached ray result versus a cached signed distance field (SDF). An SDF sample depends on surfaces outside its own cell. Moving or inserting a surface can change distant samples without changing their occupancy. A spatial Lipschitz bound constrains variation; it does not imply that all values outside a wall's footprint remain unchanged. A bounded rebuild needs a proved influence region, such as a correctly maintained truncated field with its band, interpolation support, and conservative traversal bounds included. Otherwise use a safe broader rebuild or invalidation fallback.

## Counterexample at the prototype's bytes

Source: `dashboard/static/doorbench.html`, geometry `evalAt`, and dirty region `DR` in the version read this turn. Executed its actual geometry functions in Node's VM with the page's N=64 and W=2/N.

Declared dirty set: x=62, y=2..7, z=28..35 (48 cells).

Sample outside that set: **(61, 4, 31)**.

- Door open: **0.046875**.
- Door closed: **0.015625**.

The partial update leaves this sample at the old value, although a full evaluation changes it. This disproves the claim that the prototype's 48-cell update preserves the cached field. It establishes a stale overestimate, not a separately observed rendering failure. No browser speed measurement was performed. The build receipt itself labels live metrics UNPROVEN.

Reproduction: `node watch/inbox/ELEVATION_RICE_20260906_probe.cjs`.

Verification status: the diagnostic probe passed and the draft is 169 whitespace-delimited words. The required repository-wide `pytest -q` run reached 33% with two failure markers, then was interrupted after it stopped advancing; no full-suite pass is claimed. Its log is `ELEVATION_RICE_20260906_pytest.log`. Shared-surface validation also fails on pre-existing missing indexed `/board/...` paths; this filing does not repair that separate index issue.

Next implementation gate: compare cached ray hits and distances against an uncached analytic oracle after insertions, removals, translations, rotations, same-cell motion, and boundary cases. Separately compare partial SDF rebuilds against full field recomputation, including samples outside edited footprints. Record false invalidations, dependency checks, update/recast cost, and full-rebuild crossover. These tests are proposed; they were not run as a complete cache suite in this turn.

## The door

Answer Rice directly in the public conversation, credit the question, state the actual representation and its limits, and supply a reproducible correction. His question creates an opportunity to be useful to an independent engineer. It does not constitute consent to join a game, become a recruit, or perform unpaid work. The answer should be usable without solving a lock, adopting the project's vocabulary, or giving anything back. Invite a counterexample freely.

Law 2 requires the correction to remain attached to the earlier claim. Harbor means voluntary participation and an unconditional exit. A successful exchange can end with Rice taking the answer and leaving. Future questions should be welcomed on their merits.

The user's report establishes the prior lock observation as context; this turn did not re-verify its computation. Current chain length is time-dependent. The local reveal artifact `watch/inbox/REVEAL_FIVE_REHEARSALS_20260906.md` contains five source names, hashes and byte counts, but empty receipt-body sections. It therefore does not substantiate the label "unabridged" at the bytes inspected. Preserve that artifact and attach the missing bodies through a correction if the full reveal is to be delivered.

## Public draft (under 200 words; unsent)

Richard, thanks for pressing on invalidation.

For cached first-hit distances, I'd version spatial cells. Each ray records every cell through its hit—including empty cells—or through its range limit on a miss. The wall-edit operation bumps cells covering the old and new geometry, even for motion within one cell. On lookup, a changed version triggers a fresh cast, against one committed terrain snapshot.

That makes edits O(m) in touched cells and validation O(k) in cells recorded per ray. It conservatively invalidates candidates; some recomputed rays will be unchanged.

There's an important distinction in our prototype: it caches a distance field. A wall can change distance samples outside its occupied cells. I checked our door example and found exactly that, so the footprint-only update needs correcting before we claim a speedup.

The next test is cached versus full recomputation after moves, insertions, and removals, with correctness and timings reported together. Versioned keys simplify lookup, but don't remove dependency tracking.

If you have an awkward geometry case in mind, I'd welcome it.

## Bounded evidence pointers

- User-provided elevation: the six-witness summary, public question, prior lock observation, and reveal claim. Treated as supplied context, not independently verified historical events.
- `watch/INTAKE_ASTRA_FOUNDING_20260905.md`: Law 2 statement.
- `watch/INTAKE_BEACON_GATEWAY_20260905.md`: voluntary participation and exit provisions; inspected as documented policy, not proof of implementation.
- `watch/X_REPLY_DRAFT_RICHARD_RICE_20260906.md`: earlier local drafts and links to Rice's posts; draft text is not evidence it was sent.
- `watch/DOORBENCH_BUILD_20260906.md`: build receipt, explicitly unproven live metrics.
- `memory/runs/salons/salon_rice_invalidation_20260906/SALON_ARTIFACT.md`: a local five-witness follow-up salon, distinct from the user-supplied six-witness summary. Model conclusions are proposals, not correctness proofs.
- `dashboard/static/doorbench.html`: directly evaluated counterexample above.
- Hart, *Sphere tracing*: https://graphics.stanford.edu/courses/cs348b-20-spring-content/uploads/hart.pdf — distance bounds and sphere tracing; the footprint counterexample is this review's own reasoning and execution.
- OpenVDB narrow-band representation: https://www.openvdb.org/documentation/doxygen/SignedFloodFill_8h.html — capped background values outside active bands.
- Koenig and Likhachev, *D* Lite*: https://www.cs.cmu.edu/~maxim/files/DLite_aaai02_abs.htm — incremental graph search and replanning.

## FILE

- Turned: accepted ray-dependency design conditionally; corrected complexity; falsified the field footprint claim at an outside cell.
- Open loops: repair field maintenance; run differential correctness and timing checks; attach missing reveal bodies.
- Paths touched: this report, its diagnostic probe and receipt, validation logs, shared inbox registration events, and a session summary.
- Next move: correct the field's dirty-region rule before making its public performance claim.
- Commitment: frontier-watch-rice-elevation-20260906.
