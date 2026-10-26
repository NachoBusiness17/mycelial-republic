# SEED-RIB format v0 (2026-09-26, burn brief B2-180)

Operator want: merge the seed concept with the warmed RIB into a directory
that lets agents recreate our structure for kilobytes. This is format spec v0;
the generator and rebuild verifier are tools/seed_rib.py (schema seed_rib.v0).
Pointers fused here: watch/inbox/ESSENTIALS_RESTORE.md (what a cold machine
actually boots from), TWO_MACHINE_SYNC_20260919.md warmed-RIB section (the
portable unit is the warmed RIB, ~4,000 files under 0.1 GB; everything else is
debris or ore), the seed/ directory + MANIFEST.sha256 + SEED_VERSION (prior
art, file-list shape), memory/law/registry.json (the law registry a seed must
carry or point at).

## 1. The seed document

One JSON file, schema `seed_rib.v0`:

```json
{
  "schema": "seed_rib.v0",
  "created_ts": "YYYY-MM-DDTHH:MM:SSZ",
  "source_root": "<repo root name>",
  "inline_max_bytes": 8192,
  "entries": [
    {"path": "memory/law/registry.json", "role": "registry",
     "bytes": 51234, "sha256": "<hex>",
     "carrier": "inline|pointer",
     "content_b64": "<base64, inline only>"}
  ],
  "law_refs": ["LAW-1", "LAW-3", "..."]
}
```

- `path`: repo-relative, forward slashes, never `..`, never absolute. A seed
  that carries an absolute or escaping path is void (a seed is a portable
  root, not a machine snapshot).
- `role`: one of `law` (memory/law/*, registry.json), `doctrine` (docs/
  constitution/compass class), `boot` (AGENTS.md, BOOT docs, handoffs),
  `receipt` (watch/inbox evidence), `ledger` (append-only jsonl state),
  `pointer` (a named reference to a surface that must be fetched, not
  carried). Roles drive generation rules and consumer expectations; they are
  metadata, not enforcement.
- `sha256`: over the exact source bytes, lowercase hex. This is the seal;
  the rebuild verifier hash-compares rebuilt bytes against it.
- `carrier`: `inline` when the seed carries the bytes (`content_b64`, files
  up to `inline_max_bytes`, default 8192), `pointer` when it carries only the
  seal (size + sha256) and the file must come from a named source (the
  estate, the Drive mirror, the essentials pack). Pointers are how the seed
  stays under the size bar; a pointer is a promise with a hash, never a
  hand-wave.

## 2. Generation rules (estate -> seed)

- `build`: walk an explicit file list or subtree globs; classify roles by
  path; inline small files, seal large ones; emit law_refs parsed from
  memory/law/registry.json ids when that file is in scope. Fail-closed: a
  listed file that vanished between listing and sealing is a hard error,
  never a silent skip.
- Budget: the whole-fleet seed targets < 100KB. That budget is met by
  inlining only the boot kernel (laws, registry heads, doctrine, handoff
  pointers) and pointing at everything heavy (ledgers, corpora, packs). The
  warmed-RIB census (TWO_MACHINE_SYNC: ~4,000 files) is the pointer
  universe; the inline set is the kilobyte kernel.

## 3. Rebuild verifier (seed -> structure -> hash-compare)

- `verify`: recreates every inline entry under a target root with the exact
  sealed bytes, then hash-compares: rebuilt bytes sha256 == entry seal.
  Recreates pointer entries as zero-byte stubs named `<path>.SEED_POINTER`
  carrying the seal in text, so the structure is visible and nothing fake is
  written. Exit 0 only when every inline entry matches and every pointer
  entry is either resolvable against an explicit `--source` root (hash
  checked) or reported UNRESOLVED by name. The verifier never invents bytes
  for a pointer: an unresolved pointer is named, not filled.
- `--source <root>`: when given, pointer entries are hash-checked against
  the live estate; a seal mismatch is a hard fail (the seed and the world
  disagree, someone moved bytes without re-sealing).

## 4. Law files

A seed that includes memory/law/ surfaces MUST carry or reference
memory/law/registry.json: it is the machine-checkable law registry (LAW-N
ids with tier, trigger, guardrail). law_refs records which ids the seed
attests; the verifier checks ids it can see locally and names the rest
owed. A seed without a law surface declares `law_refs: []` honestly rather
than pointing at nothing.

## 5. Dogfood (this box, 2026-09-26)

tools/seed_rib.py built a seed from the real memory/law doctrine subtree
(9 law md files + registry pointer surface) and verified a rebuild into a
temp root: every inline file hash-matched its seal, pointer entries named,
seed weighed kilobytes, not megabytes. Numbers in the receipt
watch/inbox/burn_wave_20260926/B2_180_seed_rib_v0_20260926.md.

## Falsifier (format-level)

A seed is void if: (a) the verifier reports PASS while any inline entry's
rebuilt hash differs from its seal; (b) a pointer entry gets synthetic
content instead of a named stub; (c) the seed carries an absolute or
escaping path; (d) a whole-fleet seed exceeds the 100KB budget without
naming the overflow; (e) law_refs claims ids that registry.json does not
hold.

## v0.1 amendment (2026-09-26, card seedrib revision): the directory carrier

The seed_rib.v0 SEMANTICS (inline/pointer carriers, seals, law_refs,
never-invent law) also re-home onto a real directory, and the directory is
now the preferred carrier; the JSON stays a build product. Landed tree:
watch/inbox/seed_rib_20260926/seed-rib/ (43 files, battery
check_seed_rib.py beside it). Carrier mapping:

- A file PRESENT in the tree = the INLINE carrier: raw bytes, sealed by the
  tree's own MANIFEST.sha256 (verify_seal.py exit 0 proves every carried
  byte; the pack's own contract, no new machinery).
- A row in POINTERS.sha256 with no file = the POINTER carrier: path + bytes
  + sha256 + named source (seed-3.2.0.zip entry, fleet-repo path, or a
  named-value row for git HEAD / verkle tip / the essentials pack). Fetch,
  hash-check, lay down; never invent bytes (same law as 97-99 above).
- kernel/law.heads.json carries law_refs (registry ids attested + per
  law-file seals); section 4 above applies unchanged.
- Payload efficiency: raw directory bytes carry raw bytes (no 4/3 base64
  tax); the JSON carrier spends ~126KB base64 to carry the same ~95KB
  kernel. The JSON remains what rib/seed_rib.py builds and verifies
  (compat invocation + enforced expectation recorded in the tree's
  SEED_RIB.md; default flags select nothing, selection must be explicit).
- Budget law unchanged: whole tree < 100,000 bytes; the build prints a
  measured L1-L5 REDUCTION REPORT so the overflow path is mechanical.
