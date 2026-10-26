# THE_LENSING: frontier judgment on the route (MC6 paid ask)

Status: ok. Metered cost: $0.2130. Seconds: 130.1. Usage: {"prompt_tokens": 619, "completion_tokens": 10524, "total_tokens": 11143, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 3792, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.212956, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}. Finish: stop.
Prompt sha256: b8e9f52faae6b4fdc8e2797a222c8a66884d6b63ac10f46c98e7edd74fef5c7e (1510B).
Full return below, verbatim. Em-dash count in return body: 0.

---

# Parity Deep Cuts: Build Instructions for Q14, Q15, and Q16

**Scope note:** I don't have V2CTX.md. Everything below is built from the three question statements plus public behaviour of the four runtimes. File names, the determinism law's exact wording, and the rule_parity.py internals are assumed. Adjust names to match the estate.

**Tags:**
- **[public]** means a documented runtime or language fact.
- **[inference]** means my design judgement.

---

## Q14: The Minimal Flock Parity Harness

### Ground facts that shape the design

- **[public]** Godot 4 `Vector2` uses 32-bit float components in standard builds. `real_t` is float32 unless the engine is compiled with `precision=double`. Scalar GDScript `float` is 64-bit.
- **[public]** Roblox `Vector3` components are float32. Plain Luau numbers are doubles. JS numbers are doubles. numpy defaults to float64.
- **[public]** ECMAScript leaves `Math.sin`, `Math.atan2` and similar functions implementation-approximated. Across platforms libm is not guaranteed correctly rounded either. `+ - * / sqrt` are IEEE-exact in all four runtimes.
- **[public]** Godot's JSON parser returns numbers as floats. Any integer above 2^53 is silently corrupted on read. This bites Q16 too.
- **[inference]** Boids are chaotic. Two implementations that differ by one ulp at tick 0 diverge visibly within tens to hundreds of ticks. A trajectory-level compare with fixed tolerance will produce false failures, so the harness must not compare free-running trajectories as its primary law.

### Which pair first: GDScript ↔ numpy

**[inference]** Pair GDScript with numpy first, for three reasons:

1. **Infrastructure already exists.** The rule_parity.py pattern already has a Python driver and a headless Godot runner (`godot --headless --script runner.gd`). Both ends of this pair are proven.
2. **It forces the hardest problem early.** Godot is float32 and numpy is float64, so this pair makes the precision policy explicit on day one. JS↔Luau would hide that behind a shared double type.
3. **numpy is the natural oracle.** It is vectorised and easy to instrument, so it can play the role of reference implementation.

Pairing order:

| Order | Pair | Runner |
|---|---|---|
| 1 | GDScript ↔ numpy | Existing headless Godot + Python |
| 2 | JS ↔ numpy | `node runner.js` |
| 3 | Luau ↔ numpy | Open-source `luau` CLI with a pure-table Vector3 shim |

For step 3: the shim must round to float32 via `string.pack("f")`/`string.unpack`, or the harness will not model Roblox's real Vector3.

Every implementation pairs against numpy, never against each other. That gives N−1 harnesses instead of N(N−1)/2.

### Seeded-frame format (`flockframe/1`)

```json
{
  "format": "flockframe/1",
  "constants_hash": "sha256:…",
  "consts": {"FLEE_RADIUS": "0x41a00000", "...": "..."},
  "dt": "0x3c888889",
  "boids": [
    {"id": 0, "pos": ["0x42c80000","0x43160000"], "vel": ["0x3f800000","0x00000000"],
     "rand": ["0x3e99999a","0x3f19999a"]}
  ],
  "threats": [{"pos": ["0x42f00000","0x43160000"]}]
}
```

Rules:

- **[inference] All floats travel as float32 bit patterns in hex strings.** This removes decimal-parse differences and the JSON 2^53 problem. Each runtime needs a decoder:
  - Python: `struct.unpack('<f', bytes.fromhex(...))`
  - GDScript: `PackedByteArray` plus `decode_float`
  - JS: `DataView.getFloat32`
  - Luau: `string.unpack("<f", ...)`
- **[inference] Randomness is injected, not generated.** Each boid carries its pre-drawn random values for the tick. Porting four RNGs to bit-identical output is its own project, so defer it. Harmonise RNGs later, if ever, as a separate harness.
- **[inference] Constants ride in the frame.** The frame also carries `constants_hash`. A runner whose compiled-in constants hash differs refuses to run with exit code 3. This is the Q15 link: constant drift becomes a harness error, not a mysterious position diff.

The output frame has the same shape plus a `decisions` block per boid:

- neighbour id set (sorted)
- `fleeing` bool
- which rule branches fired

### The position-compare law

**[inference] The law is teacher-forced single-step comparison.** Each tick, both implementations receive the same canonical input frame and produce one output. Next tick's input is the reference's output, quantised to float32, not each implementation's own output. Chaos cannot amplify because error never compounds across ticks.

Within one step, apply two tiers.

**Tier D (discrete decisions) must match exactly.** This covers neighbour sets, the flee flag, and branch flags. This is where real bugs live: wrong radius, `<` vs `<=`, a squared-vs-unsquared distance.

The one sanctioned exception is the threshold band. If `|d² − R²| ≤ 8·ulp32(R²)` for a pair, that pair's membership is excluded from the exact check and logged as `edge`.

**Tier C (continuous state) must match within tolerance.** Per component:

`|a − b| ≤ 4·ulp32(max(|a|,|b|)) + 1e-6·dt`

The ulp term absorbs float32 rounding-order differences. The small absolute term absorbs near-zero cancellation. If the flock uses transcendentals (heading via atan2, for example), widen that component only to 16 ulp. Document it in a `TOLERANCE_EXCEPTIONS` table keyed by field name.

**Exact-hash comparison is reserved for self-parity and for a future fixed-point flock.** It is not the cross-language law. If the estate's determinism law demands bit-identity across the flock twins, only one path gets there: port the flock to fixed-point integers, as the water engine presumably already is. Float boids across four runtimes will not be bit-identical. That is a decision to escalate, not a harness setting.

A free-running trajectory test is kept only as a smoke test:

- 60 ticks
- a loose centroid and spread comparison (flock-level statistics)
- no per-boid positions

It catches "flock explodes in one implementation" without false chaos failures.

### Tests that prove the harness is faithful

1. **Codec round-trip.** In each runtime, decode then re-encode every frame in a corpus including NaN, ±0, subnormals, ±inf, and max float32. Output bytes must be identical to input. This proves the transport is lossless.
2. **Self-parity.** Run numpy against numpy through the full harness, including subprocess and serialisation. The result must be exact-hash equal over 1000 frames. Do the same for GDScript against itself (two separate Godot processes). This proves the harness adds no noise.
3. **Known-answer frames.** Hand-computed 2- and 3-boid cases with outputs derived on paper. One is a symmetric pair that must have zero net lateral force. One is a single boid at exactly `FLEE_RADIUS + 1 ulp` from a threat, which must not flee. Both implementations must hit the known answer, not just agree with each other.
4. **Mutation sensitivity (the key falsifier).** A script applies each mutant to one implementation only. The harness must go red for every mutant:
   - `FLEE_RADIUS` += 1.0
   - swap `<` for `<=` on the neighbour test
   - drop the `dt` factor on one force
   - negate one separation component
   - use a stale velocity (read-after-write ordering)
5. **Anti-sensitivity.** A mutant that perturbs one position by 1 ulp32 must stay green. Together, tests 4 and 5 bound the harness's resolution from both sides.
6. **Hash-guard.** A runner with a mismatched `constants_hash` must exit 3, not produce output.

**Build size [inference]:** roughly 400 lines. That breaks down as a Python driver around 150, a GDScript runner around 120, a codec per language around 30 each, and the mutant list.

---

## Q15: Single Source of Truth for Shared Constants

### Design

**[public]** Three Godot 4 facts drive the choice:

- A script with `class_name` exposes its `const`s globally at parse time, as `FlockConstants.FLEE_RADIUS`.
- Those consts are usable inside other `const` expressions.
- Autoload singletons are nodes created at runtime. Their members are not constants, cannot appear in `const` expressions, and are subject to autoload-order and `@tool`-script availability issues.

**[inference] Verdict: a generated `class_name` const file, guarded by tests.** Not an autoload.

- **Autoload** is the right tool for mutable runtime state or live-tuning overrides. It is the wrong tool for invariants.
- **Test-pinning alone** detects drift but does not prevent it. Use it as the transition guard and the permanent backstop.
- **Generation wins because of Q14.** The flock exists in four languages. A GDScript-only singleton fixes one tree and leaves three copies drifting.

Structure:

```
tuning/flock.toml               # the ONE human-edited source
tools/gen_constants.py          # emits all four + a content hash
godot/gen/flock_constants.gd    # class_name FlockConstants; const FLEE_RADIUS := 20.0 ...
roblox/gen/FlockConstants.lua
web/gen/flockConstants.js
py/gen/flock_constants.py
```

Each generated file:

- starts with a `# GENERATED - DO NOT EDIT` header
- carries the `CONSTANTS_HASH` consumed by the Q14 frame guard
- is emitted as float32-exact values (e.g. `20.0` is exact; for `0.1` emit the float32-rounded decimal), so every language starts from the same bits

The generated GDScript file must depend on nothing. As a leaf, it cannot participate in `class_name` cyclic-reference problems.

**[inference] If live tuning is wanted,** add a separate `TuningOverrides` autoload that reads a `.tres` in debug builds only. Game code reads `TuningOverrides.flee_radius()`, which falls back to `FlockConstants.FLEE_RADIUS`. Parity tests always run with overrides disabled.

### Migration that never breaks a running game

**Step 0: decide before merging (human decision, not mechanical).** Are `flock.gd` FLEE_RADIUS and `fish_brain.gd` FLEE_RADIUS the same concept?

- If fish_brain's is the brain's panic-trigger radius and flock's is the steering-avoidance radius, they are two constants that collided on a name. The fix is to rename them, e.g. `FLEE_STEER_RADIUS` and `FLEE_TRIGGER_RADIUS`, not unify them.
- If they are the same concept, decide whether 20.0 or 14.0 is canonical by playtest. Do not simply let the later lane win.

The migration then proceeds in behaviour-preserving steps. The unification or rename in Step 3 is the only commit that changes gameplay.

| Step | Commit | Behaviour change |
|---|---|---|
| 1 | Pin test asserts current reality: `flock.gd`=20.0, `fish_brain.gd`=14.0. The drift is documented, not hidden. | none |
| 2 | Add toml + generator + generated files, containing both current values under distinct names. CI regen-diff check goes live. | none |
| 3 | In each script, replace the literal with an alias: `const FLEE_RADIUS = FlockConstants.FLEE_STEER_RADIUS`. Call sites are untouched because the local name survives. | none |
| 4 | The deliberate commit: unify or rename per Step 0, update the pin test in the same commit, and attach playtest notes. | intended only |
| 5 | Add lint (below) and remove the local aliases at leisure. | none |

Each step is independently revertible. Saved games and scenes do not store consts, so there is no data migration.

### Guards and falsifiers

- **Regen-diff (CI).** Run `gen_constants.py --check`, which regenerates to temp and byte-compares.
  - *Falsifier:* edit `flock.toml` without regenerating. CI must fail.
- **Literal lint (CI).** Fail on any declaration of a registered constant name outside `gen/` that assigns a literal:
  `rg -n '^\s*const\s+(FLEE_\w+|NEIGHBOR_\w+|…)\s*(:\s*\w+)?\s*:?=\s*-?[0-9]' --glob '!**/gen/**'`
  - *Falsifier:* re-add `const FLEE_RADIUS = 14.0` to `fish_brain.gd`. The lint must fail.
- **Runtime pin.** A GdUnit or headless test asserts `FishBrain.FLEE_RADIUS == FlockConstants.<name>` for every alias.
  - *Falsifier:* mutate the alias target. The test must fail.
- **Cross-language.** The Q14 `constants_hash` guard.
  - *Falsifier:* regenerate only the JS file. The harness must exit 3 for that runner.

---

## Q16: Integer-Domain Policy for the Twin Engines

### Ground facts

- **[public]** GDScript `int` is signed 64-bit and wraps silently on overflow. There is no trap, not even in debug.
- **[public]** Python `int` is unbounded. But numpy `int64` array arithmetic wraps silently too. If the Python twin mixes numpy arrays and scalars, it already has two overflow semantics internally. Audit which one the water engine uses.
- **[public]** Integer division semantics differ:
  - GDScript `int / int` truncates toward zero; Python `//` floors. They diverge for negative operands: `-7/2` gives −3 vs −4.
  - `%` diverges likewise, truncated vs floored.
  - This is a second divergence class, independent of overflow, and should ship in the same policy.
- **[public]** `struct.pack('<q', x)` raises `struct.error` when x is outside int64. If the state hash packs ints this way, the Python twin is a free overflow detector.

### Policy

**[inference]** The determinism law, taken as "identical inputs yield identical state hashes in both twins", implies five rules.

**Rule 1: Domain, not saturation, is the primary defence.** Define `INT_DOMAIN` limits in the Q15 generated constants, for example `VOLUME_MAX`, `CROSS_SECTION_MAX`, and `CELL_COUNT_MAX`. Choose them so every intermediate provably fits in int64.

Board load validates inputs against these limits. Both twins reject out-of-domain boards with the same error code before tick 0. Out-of-domain behaviour must match in outcome (identical rejection), not in value.

**Rule 2: Rewrite overflow-prone formulas to be exact.** Replace `volume * DEPTH_SCALE / cs` with the decomposition:

```
q = volume // cs;  r = volume % cs          # volume >= 0, cs > 0 asserted
depth = q * DEPTH_SCALE + (r * DEPTH_SCALE) // cs
```

This is mathematically identical to `floor(volume*1000/cs)` for non-negative operands. It needs only `cs * DEPTH_SCALE < 2^63` and `depth < 2^63`, both far looser than `volume * 1000 < 2^63`. Exact beats saturating, because saturation changes answers that the domain says are legal.

**Rule 3: Saturation only for accumulators that can legally grow unbounded,** such as cumulative inflow counters. Use one shared helper pair, `sat_add` and `sat_mul`, implemented identically in both twins.

- The GDScript version pre-checks: `a > 0 and b > INT64_MAX - a`, and similar for `sat_mul`, with the `INT64_MIN` case handled explicitly.
- The Python version clamps to `[-2^63, 2^63-1]`.
- Saturation is sticky and hashed. Both twins must saturate on the same tick to the same value.

**Rule 4: Division and modulo only through `fdiv` and `fmod` helpers** with defined (floored) semantics, or assert non-negative operands. Bare `/` and `%` on ints in engine code are banned by lint in GDScript. In Python, bare `/` on engine ints is banned outright, since it produces a float.

**Rule 5: Where divergence is acceptable vs must-match.**
- **Must-match:** every value that feeds back into the simulation or into the state hash.
- **May diverge:**
  - render-only derived floats, such as depth-to-colour shading
  - debug and telemetry strings
  - performance counters
- **Enforcement:** anything allowed to diverge must be structurally excluded from the hash. Keep it in a separate struct, not a comment.

### Overflow test family

All tests run both twins through the rule_parity.py runner. Big ints travel as decimal strings in the JSON, because of the Godot 2^53 parse issue above.

1. **Domain edges.** `VOLUME_MAX` must be accepted with equal hashes. `VOLUME_MAX + 1` must be rejected identically. Repeat for each domain constant.
2. **Naive-overflow witness.** Use `volume` with `volume*1000 > 2^63` but `volume ≤ VOLUME_MAX`, and `cs = 1000`. Both twins must produce the exact depth. Also run the old naive formula in GDScript and assert that it differs, which proves the test actually exercises the overflow region.
3. **Extremes.** Check `cs = 1`, `cs = CROSS_SECTION_MAX`, `volume = 0`, and `cs = 0` (defined rejection).
4. **Sign cases.** Negative operands reaching `fdiv`/`fmod` must give equal results in both twins. Bare-operator lint must fail on a planted `a / b`.
5. **Saturation timing.** A stress board drives an accumulator to `INT64_MAX` over N ticks. Both twins must saturate on the same tick, and hashes must match every tick after.
6. **Property fuzz.** Hypothesis generates boards within the domain, biased toward powers of two, ±1 around them, and domain maxima. Compare per-tick hashes, and let shrinking produce minimal repros.
7. **Detector canary.** The Python state hash packs with `'<q'`. A planted unbounded intermediate in the Python twin must raise `struct.error`, not hash silently.

**Policy falsifier:** revert the depth formula to the naive product, in either twin. Tests 2 and 6 must go red. If they stay green, the stress boards never reach the overflow region and the family is testing nothing.

---

## Cross-Links

- **Q15's constants hash** is Q14's frame guard.
- **Q16's domain limits** live in Q15's generated file.
- **Q14's codec rules** (hex bits, big ints as strings) are the same transport discipline Q16 needs.
- **Build order:** Q15 generator, then Q16 policy plus tests on the existing water harness, then Q14 flock harness using both.