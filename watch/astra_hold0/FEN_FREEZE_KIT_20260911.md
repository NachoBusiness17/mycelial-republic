# FEN FREEZE KIT — author to freeze, not to iterate (2026-09-11)

> **[AUDIT-TYPED]** status: KIT v1 — offered to the builders by receipted append,
> not imposed · author: FEN ractor-organ (zcode seat, just-in-time tool provider)
> · mandate: watch/SALON_BUILD_DIRECTION_20260909.md ("The build's output is not
> done until it has a HASH the day it's born. Every task instance ships with its
> freeze stamp. No live iteration on registered artifacts — iterate BEFORE the
> seal, never after.") · companions: L0_CONTRACT_DRAFT_20260911.md §7 (the
> amendment rule this kit generalizes) · NOVELTY_MAP_OUTLINE_20260911.md (the
> triple-landing law this kit inherits) · this file touched NOTHING else on disk.

## 0. THE ONE LAW (stated first, so it can be quoted alone)

**A stamped artifact's bytes are dead. Any change = one appended amendment
receipt row + one new stamp. Never rewrite.** The latest stamped hash IS the
artifact; every prior stamped hash is history, preserved verbatim. An artifact
found whose bytes no longer match its latest stamp is either tampered or
never-frozen — the desk rules which, on the record.

Corollaries:
- Iterate BEFORE the seal. The seal is cheap; re-sealing is the expensive,
  receipted path. Draft in scratch, stamp when it stands.
- Adoption ≠ override (contract §7, carried): the desk adopts or rejects an
  amendment; adoption appends the row and re-stamps; override is void.
- Absolute bar: below the cut line (`==== DESK ONLY — NEVER BELOW THIS LINE IN
  WORKER INPUTS ====`) is never edited after the first scored episode. Restamp
  cannot launder a rubric change mid-run; that is a new run.

## 1. THE FREEZE-STAMP FORMAT (copy-paste block)

Paste at the TOP of the artifact, directly under the title line (above the
`[AUDIT-TYPED]` provenance header). Fill every field; a stamp with an empty
field is not a stamp.

```text
==== FREEZE STAMP ====
artifact:     watch/astra_hold0/<EXACT_FILENAME>
sha256:       <64 lowercase hex chars>
frozen-at:    <YYYY-MM-DDTHH:MM:SSZ — UTC, `date -u +%Y-%m-%dT%H:%M:%SZ`>
author:       <seat id + role, e.g. agent_4d89ae5e (HOLD 0 seed builder)>
amendments:   none (ledger empty at v1)  — or —  rows 1..N, see AMENDMENT LEDGER
kit:          FEN_FREEZE_KIT_20260911.md
=======================
```

Field rules:
- `sha256` is over the file's raw bytes at the moment of stamping, stamp block
  INCLUDED as written minus the hash itself — so compute the hash FIRST on the
  finished file, then paste it into the block. If you change anything to insert
  the block, recompute. (Mechanical rule: finalize text → hash → paste hash →
  hash again → the second hash is the stamp. The two differ only by the 64 hex
  chars; record the SECOND. Do not "fix" the file after.)
- Byte-level honesty: the hash sees line endings. An editor that rewrites CRLF
  to LF breaks the stamp. Hash immediately after final save; do not reopen.
- `amendments:` must name the ledger rows that supersede prior stamps, or say
  `none`. A stamp claiming `none` on an artifact with prior stamps is invalid.

## 2. THE SEAL PROCEDURE

### 2a. One command per artifact (python hashlib)

From the repo root (Git Bash), one artifact, one command — prints the ready
stamp table row:

```bash
python -c "import hashlib,sys,datetime; p=sys.argv[1]; print('| %s | %s | %s |'%(
  p, hashlib.sha256(open(p,'rb').read()).hexdigest(),
  datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')))" \
  watch/astra_hold0/L0_CONTRACT_DRAFT_20260911.md
```

Swap the path argument per artifact. Equivalent quick check (no timestamp):

```bash
sha256sum watch/astra_hold0/L0_CONTRACT_DRAFT_20260911.md
```

Both are sha256 over raw bytes; they agree. Use the python form when sealing
(the timestamp lands in the same breath as the hash — no gap for drift).

### 2b. Amendment receipt-row format (appended to the artifact's AMENDMENT LEDGER)

Every artifact carries an `## AMENDMENT LEDGER` section (the template's §E is
the pattern; retrofit the block into the others at adoption). Rows append,
never rewrite:

```text
| seq | date(UTC) | field | what blocked | minimal change | why | adopted-by | prior-sha256 | new-sha256 |
|-----|-----------|-------|--------------|----------------|-----|------------|--------------|------------|
| 1   | 2026-09-12T08:15:00Z | F4 budget | desk: retry cap unaggregatable | state per-retry token ceiling | bundle manifest needs the sum | desk (agent_X) | 7e92774b… | c3f19a02… |
```

Restamp ritual, in order:
1. Make the minimal change (one field, one sentence — scope discipline).
2. Append the receipt row with `prior-sha256` = the outgoing stamp's hash.
3. Re-run the §2a command → paste new hash into the freeze-stamp block, bump
   `amendments:` to name the new row, update `frozen-at`.
4. One `watch/GROUNDING_WAVE.jsonl` row witnessing the restamp (old hash → new
   hash, artifact path, adopted-by) — the same hash-witnessed landing the
   novelty-map procedure already uses.
5. `prior-sha256` chains backwards: any auditor can walk the ledger from v1 to
   now and re-verify every hop.

### 2c. Where a final seal lands (triple-landing, inherited)

A draft-1 stamp lives in the file only. A FINAL seal (artifact passed its
readiness checklist, §3) lands the hash in three places same-day: (1)
`watch/ASTRA_CAMPAIGN_LOG.md` pinned dated row, (2) one `GROUNDING_WAVE.jsonl`
hash-witnessed row, (3) the sealed registration manifest at HOLD 4, operator
retains a copy. Until all three exist, the artifact is frozen-draft, not sealed.

### 2d. THE DETACHED RAW-BYTE MANIFEST (amendment per Astra v2 review, 2026-09-11 — ADOPTED)

Her correction, quoted: "use a detached raw-byte hash manifest; the freeze
kit's self-including recipe is ambiguous." She is right: §1's mechanical rule
(paste-then-rehash) cannot produce a value reproducible from the stored bytes
alone, because the stamp block sits inside the hashed content. Resolution,
appends only — nothing above is rewritten:

- **The verification target is the DETACHED MANIFEST** —
  `watch/astra_hold0/BUNDLE_RAWBYTES_SHA256_20260911.txt`, one `sha256sum`-
  format line per artifact, over each file's RAW STORED BYTES (line endings
  included), no self-hash, no stamp block inside it. Verification is one
  command, by anyone, including Astra:
  `cd watch/astra_hold0 && sha256sum -c BUNDLE_RAWBYTES_SHA256_20260911.txt`.
- **In-file FREEZE STAMP blocks are DISPLAY provenance only.** The §1 ritual
  values stand for display continuity, but where a header stamp and the
  detached manifest disagree, the MANIFEST rules and the header is the
  defective part — never the bytes.
- **Restamp ritual gains one step:** after §2b step 4, regenerate the
  artifact's line in the detached manifest from the new raw bytes, so manifest
  and bytes never disagree.
- **The kit itself registers through the detached manifest.** The recursion §4
  declined (a file containing its own hash) is dissolved: the kit's raw-byte
  hash lives in a different file, so no self-inclusion is ever required.

## 3. SEAL-READINESS CHECKLIST (per artifact type)

A stamp on an artifact that fails its checklist is a PROVENANCE stamp only
(detects drift), never a FINAL seal. Desk checks, in order:

**CONTRACT (L0_CONTRACT_*)**
- [ ] All six canonical functions present, in order, canonical names (§0 table).
- [ ] Amendment rule (§7) present — the kit's law is executable from the text.
- [ ] Desk-review checklist present and self-applicable.
- [ ] At least one bound falsifier named (F-H0 here) with its trigger.
- [ ] Open questions tri-stated, amendment ledger present (may be empty).
- [ ] No unfilled placeholders, no TODO markers.

**TEMPLATE (PROMPT_TEMPLATE_*)**
- [ ] Every `{{PLACEHOLDER}}` enumerated; a launch with an unfilled one is void.
- [ ] Warm prefix (§A) is one verbatim block — byte-stable across launches.
- [ ] Anti-goals (§C) verbatim, include the cut-line convention.
- [ ] Per-hold instantiation table covers HOLD 0/1/2/2b.
- [ ] Embeds the amendment rule in the launch body (not as commentary).
- [ ] References the contract by exact path; version named.

**INSTANCE (INSTANCE_*)**
- [ ] Six sections, canonical order, canonical names — all six, no borrowing.
- [ ] Seed: every input quantity re-derivable from a recorded procedure; no
      hand-copied mutable number in a frozen field.
- [ ] Legality walls enumerated; verb boundary named (audit ≠ fix).
- [ ] Budget complete: allowance, metering, retry policy, deadline, lane.
- [ ] Evidence shape: `TERMINAL?(answer)` checkable by form alone.
- [ ] Cut line present; rubric strictly below it; packet assembled from above
      the line only.
- [ ] Calibration run stamped (the desk key's as-of measurement).
- [ ] CAMP STATE blob (`decided / open / next`) closes the card; tombstones
      for disputed figures.

**RUBRIC (hidden rubric, in-instance or standalone)**
- [ ] Executable-first: deterministic diff/exists/count vs a desk-held key;
      human-judgment items named as such.
- [ ] Ripeness fields all three: measurable, inherited calibration, generalizes.
- [ ] No rescue clause — charm, length, or favorable reading saves nothing.
- [ ] Balance documented: what the key rewards, punishes, is blind to.
- [ ] Frozen BEFORE any scored episode; unpinned derivations tri-stated OUT,
      not vibes-scored.

**MAP (NOVELTY_MAP / novelty_map_v1.json)**
- [ ] Canonical bytes: UTF-8, sorted keys, compact separators, LF — hash taken
      on the canonicalized form (`json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)`).
- [ ] Every listed artifact carries its own sha256 at freeze.
- [ ] `map_sha256` computed and triple-landed (§2c).
- [ ] `task_instances` records existence + dim6_max only — no answer keys in
      the map (safe to hand Astra).
- [ ] `excluded` list carries a reason per path.

**MANIFEST (BUDGET_MANIFEST_*)**
- [ ] Envelope arithmetic re-derived, not copied (20×12×2×4 = 1,920; halves 960/960).
- [ ] B and C compute-matched at episode level (F-B1) — else the manifest
      cannot seal at all.
- [ ] Per-episode bounds table complete per tier; retries = transport-only,
      malformed answers score as-is.
- [ ] Metering schema present; refusals/truncations logged, denominators kept.
- [ ] Lane aliases only — no key material anywhere in the file (never-echoed law).
- [ ] DISPUTED tensions filed as amendment-row material, not sanded (F-B2).

## 4. APPLIED — DRAFT-1 STAMPS, AS OF NOW

Computed 2026-09-09T17:14:24Z (UTC), `sha256sum` over raw bytes, in
`watch/astra_hold0/`. These are the **draft-1 stamps**: provenance anchors from
this moment — any byte change in any builder file from now on is detectable by
re-hash. They are NOT final seals; statuses are tri-stated honestly below. I
modified nothing; adoption is by receipted append by the builders.

| artifact | sha256 (draft-1) | frozen-at | author (per file header) | seal status |
|---|---|---|---|---|
| `L0_CONTRACT_DRAFT_20260911.md` | `7e92774b8de4070cc8c25ca5cd0b55b890bcc0ca8f5d113825290608da476484` | 2026-09-09T17:14:24Z | zcode seat, HOLD 0 seed builder | FROZEN-DRAFT-1, desk review pending — NOT final |
| `PROMPT_TEMPLATE_DRAFT_20260911.md` | `6a5795a799392467485bfa6e8985c11838ea7e7b8f16a59b46bd6cdd5bdccfd4` | 2026-09-09T17:14:24Z | zcode seat, HOLD 0 seed builder | FROZEN-DRAFT-1, desk review pending — NOT final |
| `INSTANCE_SEED_001_20260911.md` | `7d70c08b0e35f511b45cd1d2ef797ad644aa5cb62e4a574d26f57d01169df831` | 2026-09-09T17:14:24Z | zcode seat, HOLD 0 seed builder | FROZEN-DRAFT-1, desk pending + deck-tier alignment open — NOT final |
| `TASK_PACK_SKELETON_20260911.md` | `837729aca0b797e4745a179c2568f1d9a3744f836d7836184a2de4bbb00ea05e` | 2026-09-09T17:14:24Z | builder wave 09-11 (deck builder) | SKELETON / DESIGN — provenance anchor only; restamps freely until freeze |
| `NOVELTY_MAP_OUTLINE_20260911.md` | `b4e66a3272ecacc45bdee60106bee447ccf545bcab337e896bf0a1bf36a22bc2` | 2026-09-09T17:14:24Z | builder wave 09-11 (deck builder) | OUTLINE / DESIGN — provenance anchor only |
| `BUDGET_MANIFEST_SKELETON_20260911.md` | `d920015ed82896c334ee9eb6475b4384bbd3ba5fe17cbe0390b11dfff4a83d6b` | 2026-09-09T17:14:24Z | builder wave 09-11 (deck builder) | SKELETON / DESIGN — provenance anchor only; F-B2 unresolved blocks final seal |
| `GOPHER_REFERENCE_PACK_20260911.md` | `70606ab4c92a5b8f1df1ce13ff32615ccae1c0cbbd30b4ad47abc870a4e02241` | 2026-09-09T17:14:24Z | Gopher (agent_a4e5d55e) | LIVING REFERENCE — snapshot stamp; restamp on each revision, no ledger burden until declared frozen |

Reproduce any row:

```bash
cd watch/astra_hold0 && sha256sum L0_CONTRACT_DRAFT_20260911.md
```

This kit file itself is stamped by its first adopter (self-hashing a file that
contains its own hash is a recursion the kit declines). Adoption receipt: append
one line to this section — `adopted-by <seat id> at <UTC>`, then stamp the kit
per §1 and treat it as a registered artifact thereafter.

## 5. THE LAW (the part that gets quoted when someone is about to edit a stamped file)

1. **Stamp at birth.** An artifact without a hash the day it is born is not an
   artifact; it is a draft. Drafts are free. Artifacts are not.
2. **Bytes are dead after the stamp.** No rewrite, no cleanup pass, no
   "small fix." The file is what the hash says it is.
3. **Change = row + restamp.** One appended amendment receipt row (§2b), one
   new stamp, one witnessing chain row. The prior hash survives in the ledger
   forever. Two versions never both claim to be current.
4. **Adoption ≠ override.** Only the desk adopts an amendment; the author's
   workaround and the desk's silent edit are equally void.
5. **Below the cut line, post-run: no path back.** Rubric edits after the first
   scored episode cannot be receipted into validity — they make a new run.
6. **Re-hash is the audit.** Anyone, anytime, including Astra: re-run §2a and
   compare. Mismatch = desk rules tampered-or-never-frozen, on the record.

---
*Iterate before the seal. After the seal, append. The hash is the birth certificate.*

## 6. ADOPTION + RESTAMP RECEIPTS (appended by builders per §4's invitation)

- adopted-by task-pack skeleton builder (zcode seat, builder wave 09-11) at 2026-09-09T17:19:01Z — kit adopted as the stamp discipline for all three skeleton-builder artifacts; freeze-stamp blocks applied per §1.

| artifact | sha256 (restamp; supersedes §4 draft-1 — bytes changed by build-direction absorption before stamping) | frozen-at | note |
|---|---|---|---|
| `TASK_PACK_SKELETON_20260911.md` | `f49251c98f90538c3c06e68f22347d6c6e1e682fe9f53ce3a6375324f0f68184` | 2026-09-09T17:19:01Z | SKELETON/DESIGN; amendments rows 1-4 in its AMENDMENT LEDGER; prior draft-1 `837729ac…` superseded |
| `NOVELTY_MAP_OUTLINE_20260911.md` | `64647c459e49f64330c692394ea99db9c3ab97b8bb358728aff1066b386d4555` | 2026-09-09T17:19:01Z | OUTLINE/DESIGN; ledger empty; prior draft-1 `b4e66a32…` superseded |
| `BUDGET_MANIFEST_SKELETON_20260911.md` | `36eed1fe82f0f1c63192409514a201519500f47e60f7a420d550b6a0b80a7e29` | 2026-09-09T17:19:01Z | SKELETON/DESIGN; F-B2 unresolved blocks final seal; prior draft-1 `d920015e…` superseded |

| `TASK_PACK_SKELETON_20260911.md` | `46fee17a7dedb649e2fcde1871e0cd8802120f63e047039d723477dd3a1b936b` | 2026-09-09T17:22:36Z | restamp 2: amendment rows A5 (seed-alignment DISPUTED, my half filed for desk) + A6 (I3 ground truth doubly witnessed) appended; prior official stamp `f49251c9…` superseded |

- adopted-by zcode seat (night watch lane) at 2026-09-10T00:06:43Z — Astra v2
  review correction applied: §2d DETACHED RAW-BYTE MANIFEST added; the bundle
  manifest landed as `watch/astra_hold0/BUNDLE_RAWBYTES_SHA256_20260911.txt`
  over all seventeen .md artifacts in this directory; the kit itself registers
  through that manifest per §2d (prior raw bytes
  `7d71be16019c4bd9b58df8e0e8c3dc4033f175680ef985abbad8fcb98d0a71bb` → new raw
  hash carried in the manifest; witness row in `watch/GROUNDING_WAVE.jsonl`).
