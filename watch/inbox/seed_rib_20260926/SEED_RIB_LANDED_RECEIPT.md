# SEED-RIB v0.1 landed (receipt, 2026-09-26, card seedrib revision)

The surviving candidate seedrib-two's proof tree is now a LANDED, durable
seed directory. Home chosen per the judge's option list: the shared inbox
(alongside SEED_RIB_CURRENT_20260926.json), the estate's durable write root
for every client per AGENTS.md; no git branch was created (the tree is
working-tree durable like every inbox artifact, and committing is the
operator's call).

## What landed (all under watch/inbox/seed_rib_20260926/)

- seed-rib/ : the tree itself. 43 files, 96,507 bytes on disk (cap 100,000;
  margin 3,493). Battery 14/14 exit 0 (raw: check.out).
- build_seed_rib.py : the build (rebuilds the tree from live estate + frozen
  zip; prints the measured REDUCTION REPORT). Raw: build.out.
- check_seed_rib.py : the battery C1..C10 (C4b named-value pointer rows,
  C9 compat invocation enforcement, C10 reduction-report re-derivation).
- derivation.json : 43 rows, source + method per carried file.
- coldseat_seed_rib.py + coldseat_prompt.txt + coldseat_*_run2.out +
  coldseat_*_20260927T*.out : the cold-seat falsifier harness, the exact
  prompt bytes (7 tree files in SEED_RIB.md join order), and raw cold-agent
  answers.

## Battery (ran on the landed tree this revision, raw check.out)

C1 budget 43/96,507 PASS; C2 verify_seal 42/42 exit 0 PASS; C3a/C3b closure
+ carried identity 0 mismatch PASS; C4 35/35 hash rows PASS; C4b git HEAD +
branch vs live git PASS, verkle tip + index vs memory/warm_state.json PASS,
essentials pack vs watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc
(1,706,469,664 B, sha256 82a4efed7745...) PASS; C5 no carried state PASS;
C6 kernel 5,9xx B vs 9,700 cap PASS (load.order 832 B vs amended cap 1,100);
C7 law_refs 12 of 12 PASS; C8 grep-level kernel answers PASS; C9 compat
invocation reproduced exactly (9 entries, 9 inline, 21,473 B, law_refs 12,
verify 9/9 hash-matched) PASS; C10 reduction report matches recomputation
PASS. 14/14.

## Cold-seat falsifier (administered this revision)

Three administrations, two genuinely cold local Ollama models (gemma:2b the
janitor scut tier; qwen2.5:3b-instruct), prompt assembled mechanically from
the 7 tree files the SEED_RIB.md join prescribes, zero context outside the
directory. Graded transcripts coldseat_run2.out / coldseat_run3.out; raw
model answers beside them. Run 1 graded under the initial key set (two of
its FAILs were key artifacts: a backtick splitting "bare `python`", and a
correct kernel-order answer to Q2 that the first key set did not accept;
key sets now name both forms the tree documents). Run 1's raw files were
overwritten before per-run stamps existed (harness wart, fixed).

Distribution, stated honestly: qwen2.5:3b answered all four questions
correctly in substance on every run (one sample omitted the concrete
interpreter string, naming the law instead: "this repo's interpreter, never
bare python on PATH"). gemma:2b answered all four correctly in 2 of 3
samples; its third sample kept the thesis, the never-bare-python half and
the filing location, but pointed at load.order.md without naming the first
files and garbled the accompaniment. Verdict: the join transmits the kernel
to kilobyte-class cold agents; the 2b tier is flaky on specifics, the 3b
tier is reliable. Gate met at 3b; recorded, not smoothed.

## Canonical doc amendments (same change)

- watch/inbox/SEED_RIB_FORMAT_v0_20260926.md: v0.1 amendment note, the
  directory carrier (file present + MANIFEST.sha256 = inline; POINTERS
  row = pointer; kernel/law.heads.json = law_refs; JSON stays a build
  product).
- watch/inbox/SEED_RIB_HANDOFF_KERNEL_20260926.md: TOC amendment log,
  load.order cap 600 -> 1,100 (dated, reasoned: full 64-hex seals for 7
  rows cost ~450 B; measured content 832 B); kernel total ceiling stays
  <= 9,700 binding; section-7 pointers ride as POINTERS.sha256.

## Honest caveats (records, not blockers)

- The candidate's compat claim "9 entries, 23,595 B, law_refs 11" is NOT
  reproducible: its selection was never recorded; the recorded selection
  today reads 9 entries / 21,473 B / law_refs 12 (the registry gained its
  12th id in the working tree between the candidate run and this revision).
  The number now lives in SEED_RIB.md with the exact command and is
  enforced by C9, so it can never silently rot again.
- memory/warm_state.json stores chain.verkle_root TRUNCATED by its writer
  (19 chars + "..."); the pointer row faithfully carries what the source
  holds; C4b compares row to source, so a future full-length root will
  fail the battery until the seed rebuilds (intended freshness semantics).
- The essentials pack row seals the dated non-VAULT pack
  (ESSENTIALS_PACK_20260926.tar.gz.enc, 1.7 GB); the battery re-hashes it
  per run (~15 s).
- The Mimosa hook drops .mimosa/hook-state files into the cwd of
  subprocesses run inside the tree; build and battery exclude .mimosa/ by
  name (named, not silent).

## INDEX registration

Register events appended via scripts/index_fold_host.mjs add for this
directory's artifacts (receipt, scripts, derivation, raw outputs, and the
tree's MANIFEST.sha256 + SEED_RIB.md + SEED_VERSION as the bounded tree
row); INDEX.json re-folded by the same command;
python -m mag.shared_surface validate run after (result in the final).
