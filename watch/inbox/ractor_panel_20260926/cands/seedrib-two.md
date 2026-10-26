# SEED-RIB merge design: candidate two (card seedrib, 2026-09-26)

Work: the B2-150..153 SEED-RIB merge, a generative directory under 100KB that
agents rebuild the fleet from. Everything below was measured in this lane; the
proof tree was built, verified 9/9, then deleted per the no-pseudo-state law
(B2-180 precedent). Rebuild evidence: `_seedrib_two_build.py` +
`_seedrib_two_check.py` + `_seedrib_two_derivation.json` in this directory.

## Approach

The directory IS the seed. The filed seed_rib.v0 (B2-180) carries inline bytes
as base64 inside one JSON and pays a 4/3 tax: SEED_RIB_CURRENT_20260926.json
spends 42,727 bytes to carry 31,328 bytes of payload. The merge keeps the
seed_rib.v0 SEMANTICS (inline/pointer carriers, seals, law_refs, never-invent
law) but re-homes them onto a real directory of raw files, sealed by the
public pack's own contract (MANIFEST.sha256 + verify_seal.py, shipped in
seed-3.2.0 and byte-carried here):

- a file PRESENT in the tree = the inline carrier (raw bytes, MANIFEST-sealed)
- a row in POINTERS.sha256 with no file = the pointer carrier (path + bytes +
  sha256 + named source; fetch, hash-check, lay down; never invent bytes)
- kernel/law.heads.json = law_refs (registry ids attested + per-law-file seals)

Generative law: LAW bytes are carried sealed and static; STATE is never
carried. Every state surface regenerates at rebuild time by a carried engine
or a kernel section carrying its own as-of stamp (the B2-300 stale-trap fix).
A cold agent instantiating the directory holds the fleet KERNEL; the UNIVERSE
(~4,000 files / 0.1 GB warmed RIB, TWO_MACHINE_SYNC_20260919.md) is
deliberately left out as sealed pointers and rehydrates from named sources
(git HEAD row, essentials pack row, per-file fleet-repo rows). No file in the
instantiated tree requires anything beyond the directory.

Source-of-bytes decision: the merge builds from the FROZEN public pack bytes
(watch/inbox/seed-3.2.0.zip, 53 entries, sha256 e9f4603a4484dafb3d79103aef63c
678774ec508f9cd573677e91f83bc78f87e, verified against INDEX.json row [952] by
sha256sum this lane), NOT the repo seed/ tree: state/CURRENT.md records that
tree as drifted mid-3.3.0-cook (verify_seal exit 1, DRIFT TRUST_BYTES_LAW.md,
55/56) and it holds 4 unshipped files (STACK.md, templates/*, byte-diffed
this lane: 50 of 53 zip entries byte-identical on disk, CHANGELOG/MANIFEST/
SEED_VERSION drifted).

## Moves with estate paths

### M1. Re-home the carrier: JSON-base64 in, sealed directory out
Touches: watch/inbox/SEED_RIB_FORMAT_v0_20260926.md (B2-180 format),
tools/seed_rib.py, seed-3.2.0 MANIFEST.sha256 + verify_seal.py contract.
The merged artifact is a 43-file directory measured at 94,789 bytes on disk
(margin 5,211 under the 100,000B budget). Payload efficiency vs the JSON
carrier: 94,789B of tree buys 94,789B of kernel; the v0 JSON would spend
~126KB base64 carrying the same bytes. seed_rib.py rides inside the tree
(rib/seed_rib.py, byte-identical to tools/seed_rib.py) and still works: this
lane ran it FROM the tree, build exit 0 (9 entries, 23,595B seed) and verify
exit 0 (9/9 inline hash-matched) against a temp rebuild root. The JSON stays
a build product, not the carrier.

### M2. The kernel cut of the pack: 31 of 53 zip entries carried frozen
Touches: watch/inbox/seed-3.2.0.zip. Carried byte-frozen (C3b: 0 mismatches):
20 law/boot docs (THE_METHOD 3,093B, FIRST_BOOT 2,085B, TRUST_BYTES_LAW,
BUILD_DISCIPLINE_LAWS, SHARED_SURFACE_LAW, ARTIFACT_LEDGER_LAW,
STATE_BRIEF_CONTRACT, BOOT_BUDGET_CARD, CAPABILITY_GATE_LEDGER, SALON,
MORNING_LOOP, DATA_TIERS, ZERO_CONTEXT_DELEGATION, ACCOUNTS, TOUR, HANDOFF,
SETUP, VSCODE, CHANGELOG, LICENSE) + the 172B thin AGENTS.md boot card + the
4 configs (laws-as-config: law_registry.json 7,200B, mode_budgets 3,301B,
keys.json, chores.json) + 5 generator engines (seed_init 2,461B,
spine_walk 6,841B, cooker 6,840B, key_law 4,619B, keys 1,153B) +
verify_seal.py (712B, the kernel self-test).

### M3. Handoff kernel instantiated: kernel/ sections generated from live surfaces
Touches: memories/session/next-window-handoff.md, AGENTS.md, state/
START_BRIEF.md, state/CURRENT.md, memory/law/registry.json,
memory/warm_state.json, mag.cmd context-pack. Seven sections, 5,908B total
(cap 9,700): env.law (641B, AGENTS.md Python-env slice), load.order (730B,
AGENTS.md load table + full live sha256 seals + the one command row),
thesis.card (1,488B, context-pack L0b rendered live this lane and sliced at
the UPDATE marker), state.now (820B, START_BRIEF running/queued/health +
CURRENT owed head, stamped, never hand-carried), filing.law (554B, handoff
procedure step 5 + residual-on-disk standing line), tier.law (253B, T0/T1
standing lines + L2 tags), law.heads.json (1,435B, 11 law_refs ids
byte-parsed from the registry, all 11 exist in registry.json, plus seals for
registry + every memory/law/*.md).

### M4. Deliberately left out, sealed not silent
Touches: POINTERS.sha256 (4,526B, 38 rows) and the universe it bounds.
20 zip rows (hashed from the frozen zip): 11 running-fleet engines
(process_supervisor 30,324B, estate_smith_chart 14,100B, estate_atlas
11,498B, flight_recorder 15,176B, task_wall 13,189B, lite_guard 11,628B,
phone_relay 11,179B, model_bakeoff 8,220B, librarian_catalog 7,816B,
stealth_sweep 7,683B, claritas 2,945B; 133KB total, the budget killer if
carried); 7 organ templates (SKILLS, ACTIVITY_TRAIL, CAMPAIGN_EVIDENCE,
COST_LEDGER_TEMPLATE, LOOP_GAP_TEMPLATE, TRAINING_EVENT_TEMPLATE,
TRAINING_SPINE_LAW); tests/ (test_seed_laws.py imports phone_relay, a
left-out engine: carrying the test without the engine ships a red suite, so
it rides as a pointer and verify_seal.py is the kernel self-test).
15 fleet-repo rows (hashed live): AGENTS.md full, the load-order files
(FRAMEWORK_LOAD, COMPASS, SCIENCE_MAP, DIRECTION_ARTIFACT, PROJECT_PROPOSAL,
OPERATOR_CARD), docs/DNA.md, memory/law/registry.json, tools/seed_mcp.py,
configs/lanes.yaml, configs/version_roadmap.yaml, and the three SEED_RIB
estate docs. 3 named-value rows: git HEAD + branch (universe root),
verkle tip + chain index (from memory/warm_state.json), essentials pack
(seal lives with the pack, watch/inbox/ESSENTIALS_RESTORE.md).

### M5. What each carried file regenerates (the spec table)
- verify_seal.py + MANIFEST.sha256 regenerate the seal audit: exit 0 proves
  every carried byte (ran: 42/42 verified, 0 drifted, 0 missing).
- engines/seed_init.py regenerates the estate skeleton (records/, logs/,
  watch/inbox/, configs/, doc copies) for the grow path.
- engines/spine_walk.py regenerates the estate index (JSONL per-file map);
  the kernel boot runs it on the seed itself as the honest zero state.
- engines/key_law.py + keys.py + configs/keys.json regenerate the
  key-declaration audit (.env law, fails loud on live-undeclared).
- engines/cooker.py + configs/chores.json + mode_budgets.json regenerate the
  free-lane burn schedule.
- configs/law_registry.json regenerates the 13-law method registry
  (laws-as-config, the B2-153 delta nobody ships).
- rib/seed_rib.py regenerates the seed_rib.v0 JSON (build) and proves
  rebuilds byte-exact (verify) from the directory itself.
- kernel/env.law, load.order, tier.law, filing.law regenerate the rebuilt
  fleet's AGENTS.md surfaces (env law, load table, ladder, filing law);
  thesis.card + state.now regenerate the cold seat's first read, stamped at
  build time.
- The 20 law/boot docs regenerate the law surface of any grown estate
  (seed_init copies them); SEED_VERSION + SEED_RIB.md carry merge identity,
  the carrier law, the cold-join procedure, and the budget levers
  (L1 VSCODE 1.4KB, L2 TOUR+SALON 3.2KB, L3 MORNING_LOOP 1.2KB, L4 ACCOUNTS
  1.6KB, L5 kernel-cap floor), the named reduction path if a future build
  exceeds 100KB.

## Falsifier

Ran in this lane (commands + output; battery = `_seedrib_two_check.py`):
- C1 budget: 43 files, 94,789 bytes on disk vs the 100,000B cap. PASS
  (margin 5,211B; reduction levers L1-L5 named in SEED_RIB.md).
- C2 the pack's own verifier inside the tree:
  `.venv/Scripts/python.exe <tree>/verify_seal.py` exit 0,
  "42/42 verified, 0 drifted, 0 missing". PASS.
- C3 derivation closure: 43 tree files == 43 derivation rows (symmetric
  difference empty); carried-frozen and carried-from-repo files byte-compared
  against their sources: 0 mismatches. PASS. This is the kill-arm answer: no
  file in the instantiated tree is underivable from the directory; every row
  names source + method (carried-frozen / carried-from-repo / extracted /
  regenerated / generated / authored).
- C4 pointer honesty: 35 hash rows of POINTERS.sha256 re-hashed against their
  named sources (zip entries and repo files): 0 bad. PASS.
- C5 state absence: no records/, no ledgers, no *.jsonl in the tree. PASS.
- C6 kernel caps: 7 sections, 5,908B total vs 9,700B cap. PASS (one dated
  amendment: load.order 600 to 1,100, because full 64-hex seals for 7 rows
  cost ~450B alone; the kernel total cap still holds with 3.8KB spare).
- C7 law_refs: 11 ids attested, all 11 present in memory/law/registry.json
  (byte-parsed). PASS.
- C8 cold-kernel acceptance (B2-300's test, grep level): the four kernel
  answers present in the directory alone (venv law, FRAMEWORK_LOAD load
  path, watch/inbox filing law, standing thesis). PASS.
- Compat: rib/seed_rib.py run FROM the tree built a seed_rib.v0 JSON
  (9 entries, 23,595B) and re-verified it into a temp root, 9/9 inline
  hash-matched, exit 0. PASS.

Standing kill conditions for the design (the judge's arms):
(a) a rebuilt tree over 100KB with no named lever (levers exist and are
measured; L1-L4 alone free 7.4KB); (b) any file in the instantiated tree
whose derivation row cannot name an in-directory source or generator (C3
closes this; the LEFT-OUT list is explicitly NOT instantiated); (c) a
pointer row whose seal disagrees with its source (C4 re-runnable); (d) a
state section hand-carried or older than the seed build stamp (build stamp
is generated, not hand-edited; C5 pins no-state-in-tree); (e) law_refs
naming ids the registry does not hold (C7).

## Owed

1. Cold-seat administration of C8: a genuinely cold agent reading only the
   directory and answering the four kernel questions unaided. Grep-level
   presence ran; the cold-seat run needs a second seat (same honest gap
   B2-229 filed for its audit seed).
2. Universe rehydration drill: fetch one POINTERS row from the Drive mirror
   or a clone and lay it down hash-checked. Not run: no second machine in
   this lane.
3. seed_rib.v0 format amendment: SEED_RIB_FORMAT_v0_20260926.md needs a v0.1
   note recognizing the directory carrier (present+MANIFEST = inline,
   POINTERS row = pointer). SEED_RIB.md carries the interim law; the format
   doc is the canonical home.
4. 3.3.0 re-merge: the disk seed/ tree (STACK.md, templates/, seal hygiene
   per its CHANGELOG) is mid-cook and drifted; re-merge against its sealed
   zip when the repack ships.
5. load.order cap amendment (600 to 1,100, dated 2026-09-26, this lane)
   should be folded into the B2-300 TOC doc alongside the kernel-total cap
   law.
6. The proof tree was deleted after measurement (no pseudo-state); the
   landed seed needs a durable home (seed/ on a new branch, or the watch
   inbox alongside SEED_RIB_CURRENT) and an INDEX.json row when the operator
   picks it up.
