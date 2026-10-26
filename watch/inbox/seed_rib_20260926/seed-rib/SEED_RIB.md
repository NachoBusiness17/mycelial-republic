# SEED_RIB: the merge law and the cold-join procedure

This directory is the SEED-RIB merge: the public seed pack 3.2.0 (method +
engines + laws-as-config) fused with the seed_rib.v0 carrier law (B2-180) and
the handoff kernel sections (B2-300). It is the fleet KERNEL: everything a
cold agent needs to rebuild the fleet's shape and regrow its state.

## Carrier law (seed_rib.v0.1, re-homed onto a directory)

- A file PRESENT in this tree is the INLINE carrier: raw bytes, sealed in
  MANIFEST.sha256. `python verify_seal.py` proves the whole tree (exit 0).
- A row in POINTERS.sha256 with no file is the POINTER carrier: path + bytes +
  sha256. Pointers are promises with hashes, never hand-waves. Fetch from the
  named source and hash-check; the verifier never invents pointer bytes.
- kernel/law.heads.json carries law_refs (the law registry ids this seed
  attests) and per-law-file seals.
- Canonical format home: watch/inbox/SEED_RIB_FORMAT_v0_20260926.md (v0.1
  amendment note, 2026-09-26) recognizes this directory carrier.

## Cold join (rebuild the fleet kernel from this directory alone)

0. `python verify_seal.py`: exit 0 or stop here (trust bytes, not reports).
1. Read kernel/ in order: thesis.card.md, state.now.md, env.law.md,
   load.order.md, tier.law.md, filing.law.md. These seven sections are the
   handoff kernel: the cold seat now knows the thesis, the owed, the env law,
   the load order, the tier ladder, the filing law.
2. Zero state, honestly: `python engines/spine_walk.py <this-dir>` indexes the
   kernel itself (the map regenerates; it is never hand-maintained). The full
   method's smith chart (FIRST_BOOT step 2) is a POINTER row: the kernel boot
   substitutes this self-index; fetch the chart engine when you run lanes.
3. `python engines/key_law.py --audit`: passes on declared 'awaiting' keys,
   fails loud the moment a live key is undeclared.
4. `python engines/cooker.py status`: the free-lane reset table.
5. Grow: a stranger runs `python engines/seed_init.py <target>` and grows
   their own estate under THE_METHOD.md (FIRST_BOOT.md is that path).
   A fleet seat rehydrates the UNIVERSE instead: every row of POINTERS.sha256
   names a source (repo path in the fleet mirror, or the git/verkle/essentials
   rows); fetch, hash-check, lay down. The universe is never carried, only
   sealed.

## Compat build (the seed_rib.v0 JSON is a build product, not the carrier)

rib/seed_rib.py (byte-identical to tools/seed_rib.py) still builds and
verifies a seed_rib.v0 JSON. Default flags select nothing (0 entries), so the
selection must be explicit. Verified invocation, run with the tree's own copy
against the fleet repo (numbers are as-of this seed's build stamp; the live
law corpus moves them: the candidate artifact's 23,595 B / law_refs 11 was
never reproducible because its selection was never recorded, and the same
corpus read 21,473 B / law_refs 12 one build later):

    python rib/seed_rib.py build --root <fleet-repo> --out seed_from_tree.json --glob "memory/law/*.md"
    python rib/seed_rib.py verify --seed seed_from_tree.json --into <tmp-rebuild>

    build: 9 entries (9 inline, 0 pointer), seed 21473 bytes, law_refs 12
    verify: inline 9 hash-matched, exit 0

The battery (check_seed_rib.py, C9) reruns exactly these lines and fails on
drift, so the compat numbers above can never silently rot: when the live law
corpus grows, the battery fails loudly and the seed rebuilds.

## Budget and growth laws

- Whole tree < 100,000 bytes (measured at build; see MANIFEST row count).
  The build prints a REDUCTION REPORT with each lever measured from this
  build's own bytes; when a rebuild exceeds the cap the report names the
  lever set that recovers it. Levers, in order: L1 pointer-ize VSCODE.md;
  L2 TOUR.md + SALON.md; L3 MORNING_LOOP.md; L4 ACCOUNTS.md; L5 tighten
  kernel caps back to the B2-300 minimums (load.order to 600).
- STATE IS NEVER CARRIED. records/, indexes, meters, ledgers regenerate from
  zero by the engines; history folds to pointers (residual + registry + chain
  leaf per docs/DNA.md, sealed in POINTERS.sha256).
- A seed section carries its own as-of stamp; a state section older than the
  seed's build stamp voids the build (the stale-trap law, B2-300).
