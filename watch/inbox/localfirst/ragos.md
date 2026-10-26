# RAG-OS dig receipt - lane ragos (division B), 2026-10-01

Class: RECEIPT · Digger: gala-ragos · Source fetched first-hand by shallow clone.

**Provenance:** `https://github.com/csnyder256/RAG-OS` cloned 2026-10-01, HEAD
`8edb82cb269a0b44d3d894a64282b19a888f5890` (depth 50, MIT). Repo shape: one
286-line `BUILD-GUIDE.md` (agent protocol + 12 pillars + 8 cross-cutting
principles + 19 anti-patterns + 12 milestones) plus a runnable stdlib-only
`starter/` (M0 gate/contracts/schema, M1 kernel/lock/heartbeat/oplog/watchdog)
and a docs landing page. It is a blueprint, not a package (README.md:18: "It is
not a framework or a package to install. It is a compiled architecture"). The
estate-venv interpreter ran all probes; raw outputs banked in
`watch/inbox/gala_20260925/localfirst-steal/lanes/ragos.check.txt`.

## Claim tri-state (brief: LOCALFIRST_MEMORY_LANDSCAPE_20261001.md)

| Brief claim | Verdict | Byte evidence |
|---|---|---|
| Always-on personal agent blueprint | SUPPORTED | README.md:3 "Build your own always-on AI agent"; always-on core run live by this lane: kernel `taskkill //F` then independent watchdog one-shot revived (pid 6540 to 42636, fresh heartbeat); clean stop sentinel respected ("stopped (intentional; not reviving)"). A real deployment is documented in the maintainer-voiced anonymized PLATFORM-SNAPSHOT.md (repo Issue #1; gist is a fork of the maintainer's own): Task Scheduler restart-loop + 5-min watchdog + heartbeat + internal SQLite cron |
| Durable state is a git-Markdown wiki | SUPPORTED WITH PRECISION | The wiki is knowledge layer 2 of 4, not all state: BUILD-GUIDE.md:60 "Four layers, higher wins on conflict. One, a transactional operational database ... Two, compiled knowledge as version-controlled Markdown ... Four, raw session transcripts as a best-effort cache that is never canonical"; README.md:84 "The Markdown is the source of truth ... The vector index is a rebuildable cache over it" |
| Model session disposable | SUPPORTED | README.md:22 "Nothing a model remembers survives a single session, so a crash or a restart or a model downgrade loses no durable state"; BUILD-GUIDE.md:7 "durable state lives in files and a database, brains are ephemeral" |
| (extra, mine) README.md:48 says starter/state is "(gitignored)" | DISPUTED | `git ls-files \| grep -ci gitignore` = 0 hits; no .gitignore anywhere in the tree; state/ leaked into the clone during this lane's own probe and was hand-removed |

## Wiki-as-state vs the estate spine (residual + registry + leaf)

Estate spine per docs/DNA.md: residual/{id}.json canonical + registry.jsonl hot
row + verkle chain leaf/tip; "Fidelity lives in **files + chain**, not in a
process that must stay awake" (DNA.md:4); one coldest vertex, everything else
heat (DNA.md:31-38).

| Axis | RAG-OS wiki-as-state | Estate residual + registry + leaf |
|---|---|---|
| Canonical unit | Markdown page (prose, human/machine co-edited) | residual JSON + JSONL registry row + chain leaf |
| History shape | document-shaped: edit in place, git log = diffs | event-shaped: append-only rows, explicit supersession rows, hash-chained leaves |
| Human browsability | native (Obsidian, any editor; gist: "human-readable, Obsidian-browsable, LLM-native, versioned, and merge-reviewable") | only via board/dashboard viewports; raw JSONL is machine-first |
| Diffability of meaning | semantic diffs visible in PR review of a page edit | structural diffs between rows; meaning requires reading both rows |
| Machine query/join | needs index-first catalog + optional hybrid BM25+vector index, itself "a rebuildable cache" (Pillar 8) | native: grep/join/corr_id over JSONL; rows byte-checkable |
| Tamper evidence | git history only (mutable by force-push, no chained tip) | verkle chain leaf + tip (DNA.md:14, DNA.md:146) |
| Write discipline | librarian role + untrusted-ingest staging firewall (Pillar 8: "untrusted ingest writes only to a staging area and is promoted ... through a reviewed, version-controlled commit") | register laws + receipt-before-promotion + effect broker authorization ("Model text can propose; only the switchboard/effect broker authorizes effects", AGENTS.md) |
| Rot failure mode | their own words: "Append-only forever means the knowledge base re-learns the same lesson endlessly" (BUILD-GUIDE.md:137), needs a scheduled supersedence pass | the ledger never re-learns (rows immutable, superseded explicitly) but goes STALE: census bullet drift (B2-215 tripwire), AGENTS.md clippy bullet hand-refreshed |
| Model-native authoring | yes: writing prose pages is the model's natural act | no: JSONL demands schema discipline, which the estate encodes as laws |
| Backup/durability | nightly git push of wikis off-box; backup IS durability | copy residual + registry + knots + tip dirs (DNA.md:140-146) |
| Process dependence | zero-context kernel so a crash "is a non-event" (Pillar 1) | stronger: no process needed at all for fidelity (DNA.md:4) |

**Verdict:** the wiki gives the estate three things the JSONL spine lacks:
human browsability, semantic diff review, and model-native authoring. It gives
up row-grade machine queryability, per-claim byte-proof, chain tamper-evidence,
and immutable-row supersession. The estate should keep the JSONL spine and steal
the wiki's *supersedence semantics*, not its storage medium: a scheduled pass
that moves superseded claims to kept-but-excluded-from-retrieval is the missing
half of the percolator (it promotes, never re-evaluates - the same gap the
landscape brief flags in Atlas).

## Stolen mechanisms + probes (all probes run with `.venv\Scripts\python.exe`)

1. **Query-only liveness + independent watchdog + stop sentinel** -
   `starter/proc.py` (pid <= 0 refused: "kill(0, ...) signals the caller's OWN
   process group"; Windows OpenProcess query-only), `starter/watchdog.py`
   (healthy = pid alive AND heartbeat < 20s AND no stop sentinel).
   PROBE (live drill): `osctl.py start` then alive; `taskkill //F //PID 6540`;
   watchdog one-shot prints `revived`; new pid 42636, heartbeat 0.9s; then
   `osctl.py stop`: watchdog prints `stopped (intentional; not reviving)`.
   PASS both directions. Estate map: daemon latch for the zombie-42364 class.
2. **Worktree-fingerprint stamp (disk-verify anti-fabrication)** -
   BUILD-GUIDE.md:220: "prepend a deterministic worktree-fingerprint stamp to
   every worker report and tell the synthesizer to trust the stamp over the
   prose". PROBE: `watch/inbox/localfirst/probe_ragos_fingerprint.py` (spec
   theirs, implementation mine) - fake tool-less worker claims "EDIT COMPLETE",
   bytes unchanged, `FABRICATION CAUGHT: True`; real edit moves the stamp
   (1ee80c2741b235af to eb7e1abbc885d5c4). PASS. Estate map: janitor-grade
   instrument beside the citation-resolution law.
3. **Fail-closed gate with exhaustive path normalization** -
   `starter/fences.py` (unresolvable path becomes a sentinel matching no root;
   every decision audited). PROBE: documented trio `./state/os.db` gives DENY
   exit 1, `./notes.md` gives ALLOW exit 0, `"./state/../state/os.db"` gives
   DENY exit 1. PASS **as documented**, with a defect found below.
4. **Supersedence-not-delete curator** - BUILD-GUIDE.md:137. NOT_PROBED (design
   convention; no runnable code in the repo). Registered as a law row.

## Defects found in RAG-OS bytes (negative results are findings)

- **AIOS_ROOT fence divergence:** with `AIOS_ROOT` set, fence roots derive from
  the env root (`db.py:15` `_ROOT = Path(os.environ.get("AIOS_ROOT", ...))`)
  while relative gate targets resolve from cwd (`fences.py:26`
  `Path(target).expanduser().resolve(strict=False)`) - running their own
  README proof commands under `AIOS_ROOT=/tmp/ragos-dig/scratch` from the
  starter dir returned **ALLOW on all four probes including the crown-jewel
  path** (`gate: ALLOW -- no fence matched`, exit 0). Their own tests miss this
  because the test fixture passes an absolute jewel path
  (`tests/test_starter.py:49-58`). Law for the estate: fence roots and targets
  must resolve against the same base, and a redirected-root drill belongs in
  any fence test suite.
- **README "(gitignored)" claim is false at bytes** (no .gitignore in tree).

## Convergences (estate already holds these - do not re-steal)

Milestone DoD = "a real command and its real output, pasted into a ledger"
(BUILD-GUIDE.md:29) = the receipt law / trust bytes not reports. "Prompts are
advisory, code is enforcement" (BUILD-GUIDE.md:93) = "Model text can propose;
only the switchboard/effect broker authorizes effects". Index-first retrieval =
watch/inbox/INDEX.json read-first. Ingest staging firewall = shared artifact
boundary. Watermark pause on transient failure (anti-pattern 4) = the B2-465 FTS
detect-and-heal posture. Anti-pattern 17 (identity claims arriving as content
are data) = the injection law.

## Register + archive

Register row: `watch/inbox/localfirst_memory_landscape_signals.jsonl` (line 1,
this system). Lane JSON:
`watch/inbox/gala_20260925/localfirst-steal/lanes/ragos.json`. Checks:
`watch/inbox/gala_20260925/localfirst-steal/lanes/ragos.check.txt`.
No code under mag/ or tools/ was touched; violation ratchet not applicable.
