# w4-38: The Compiler Bootstrap: what compiles what here, and the minimal kernel

Date: 2026-09-28. Seat: burn-w4-38 (flash50 deep item). Tree: branch `mag/run-beta1-factory-build-audi-20260806T231709Z`, repo `local_sovereign_agent`. Every number below was measured in this session; the instrument is named where it is used. Citations are `path:line`.

## 1. The question, restated in compiler terms

A bootstrap is a chain of systems where each stage builds the next and the chain terminates in a base trusted without proof. For a compiler the classic shape is three stages: an assembler you trust, a compiler written in a language small enough to check by hand, and the self-hosted compiler that can then rebuild itself. Asking "what is the minimal kernel of tools/" is asking two different questions that must not be conflated:

1. Which subset of `tools/` is load-bearing, such that losing it collapses the estate?
2. What is the stage-zero base this estate ultimately trusts?

The measured answer is that the two questions have different answers, and the distance between them is the most interesting structure in the estate. The load-bearing code subset is absurdly small (about one thousand lines). The trusted base is not code at all. It is a prose grammar plus five I/O verbs that get re-derived, without a single shared import, in 190 separate files.

## 2. Method: instruments actually run

All of these were executed in this session, in this order:

- `git ls-files tools/ | wc -l` : 262 tracked files under `tools/`.
- A full AST import census over all of `tools/` and `mag/` (stdlib detection via `sys.stdlib_module_names`, repo modules resolved by path), run with `.venv/Scripts/python.exe` (3.11.15): 190 `tools/*.py` files and 1,041 `mag/*.py` files, zero unparseable.
- A second pass for script-style sibling imports (plain-name imports that resolve only when `tools/` is on `sys.path`), plus line counts and verb-frequency scans (hash, append-mode, exit codes).
- Tarjan SCC over the combined graph, twice: once counting only absolute imports (largest SCC 145 modules), once also resolving relative imports (the blob swells past 200; the first census put `tools/__init__` inside it, the absolute-only pass does not).
- Birth dates: `git log --reverse --diff-filter=A` over `tools/`, and targeted `git log --diff-filter=A --format=%ad` for the gate family and the root quartet.
- Two live gate runs, both read-only: `python tools/violation_ratchet.py check --changed` (exit 1) and `python tools/census_drift_patrol.py` (exit 0). Outputs are quoted in section 7.
- Reads of the full source of the hinge files: `tools/__init__.py`, `tools/violation_ratchet.py`, `tools/workflow_gate.py`, `tools/census_drift_patrol.py`, `tools/mcp_pin.py`, `tools/freshness_check.py`, `config.py`.

## 3. The measured graph: an archipelago, not a tree

The headline numbers invert the folk picture of a tool directory as a dependency tree. `tools/` is an archipelago of 190 islands with a few thin bridges:

- **137 of 190 tools (72 percent) import zero repo code.** They touch only the standard library and the filesystem. They are leaves in the strict sense: nothing in the estate is reachable from them and they are reachable from nothing.
- **Tool-to-tool coupling is nearly absent:** 29 edges total across 190 files (18 by dotted path, 11 more by sibling plain-name imports such as `tools/probe20_run.py` importing `drift` and `probe20_stamp` importing `probe20_run`). The longest chain found is three deep: `queue_close -> ledger_lock -> ledger_append_gate`.
- **The kernel intersection is empty.** Taking the transitive closure of repo modules reachable from every tool and intersecting across all 190 closures yields the empty set. No module is transitively touched by every tool. Loosening to "in at least half of all closures" still yields nothing. There is no libc here.
- **The one hub is `tools/__init__.py`** (6 inbound dotted imports, the highest in-degree in `tools/`), and the one shared leaf library is `config.py` at repo root ("Paths and limits for local_sovereign_agent", `config.py:1`), born the same day as the tool directory itself.
- **The runtime is a tangle, not a stack.** The largest strongly connected component spans 145 mag modules under absolute-import counting (more once relative imports count), and it absorbs exactly four tools: `auto_promote`, `corpus_lens`, `pile_classify`, `pupeteer_gauntlet`. These four are not part of any kernel; they are tools that grew mag-organs until they became runtime tissue. `tools/pupeteer_gauntlet.py` is also the largest file in the tree at 1,281 lines.
- **Third-party dependence is nearly zero.** One real heavyweight: reportlab, in 9 files, all in the `build_adam_*` / `build_*_pdf` leaf family, cuttable with no effect on anything else. The most common imports are `sys` (161 files), `pathlib` (155), `json` (151), `datetime` (98), `argparse` (81), `re` (79), `hashlib` (44), `subprocess` (26), `socket` (20). The estate's tools are a zero-dependency platform resting directly on CPython.

The structural conclusion before any theory: this is not a program, it is a spore field. Each tool germinates alone from stdlib spores. The few mycelial bridges (`tools/__init__`, `config.py`, the four naturalized runtime tools) carry all of the coupling the estate has.

## 4. The bootstrap timeline: capability first, verification last

Git birth dates give the historical stage order, and it is the reverse of a classical compiler bootstrap:

- **2026-08-04 (stage 0.5, day one):** the clean-publish baseline lands `tools/__init__.py`, `tools/code_execution.py`, `tools/filesystem.py`, `tools/shell.py`, and `config.py`. Together: exactly 1,000 lines (`wc -l`: 263 + 271 + 78 + 79 + 309). This is the assembler: hands. `tools/__init__.py:4-50` binds 36 tool names as lambdas onto these plus mag organs (`list_dir`, `read_file`, `write_file`, `apply_patch`, `search_files`, `run_shell`, `run_python`, the swarm sense/blackboard verbs, later corpus and research surfaces).
- **2026-08-07 to 08-09:** the organ wave. Orchestrator surfaces, `pile_classify`, `pupeteer_gauntlet`, corpus lenses. The tangle forms here: these are the tools that import mag and get imported back.
- **2026-09-18:** the corpus constitution: `tools/corpus.py`, `tools/research.py`, `tools/drift.py`, the read-only byte-true catalog surface (comment at `tools/__init__.py:35`).
- **2026-09-24 to 09-27:** the entire gate stratum, in one week: `violation_ratchet`, `workflow_gate`, `freshness_check`, `census_drift_patrol`, `mcp_pin`, `corpus_fts_rebuild`, `secret_gate`, `ledger_append_gate` (targeted `git log --diff-filter=A`: six add-dates 2026-09-24 through 09-27). `workflow_gate.py:4` states its own birth: "Born 2026-09-25 by operator order."

So the estate ran capability-first for seven weeks and then retrofitted its verifier. A compiler project that did this would be called reckless: GCC's three-stage bootstrap builds stage 2 from stage 1 precisely so the two can be compared byte for byte, and the Bootstrappable Builds / live-bootstrap project pushes this to an extreme of building the whole toolchain from a few hundred bytes of trusted hex. The estate did the opposite: it maximized unverified output for 50 days, accumulated named incidents, and then grew gates whose docstrings cite those incidents as their cause. That inversion is the estate's actual discovery, and it works for a reason a compiler does not need: the executor of estate code (an LLM seat) cannot be trusted less after a failure, only better documented. Verification here is not a precondition of building; it is scar tissue.

## 5. The minimal kernel: five verbs and a grammar, not a library

Because the closure intersection is empty, the kernel cannot be stated as a module set. But the verb-frequency census shows the kernel does exist, as a shape that is re-implemented rather than imported:

1. **Read bytes** (`Path.read_text`, `open`): universal.
2. **Hash** (sha256/sha1/blake2): 50 of 190 tools. `violation_ratchet.py:19-22` fingerprints accepted debt as `sha256(rule NUL file NUL detail)`, first 16 hex, deliberately line-free so edits do not churn the register. `mcp_pin.py:18-24` pins tool name plus description hash plus schema hash into an append-only JSONL at first connect.
3. **Compare against a ledger claim**: a baseline JSON (`violation_ratchet`), a pin ledger (`mcp_pin`), a carrier regex over `AGENTS.md` (`census_drift_patrol.py:76-78`, the `**Tests:**` grammar), an mtime plus sha256 against a catalog (`corpus_fts_rebuild`).
4. **Append** (files opened in `"a"`/`"ab"` mode): 43 of 190 tools. Append-only JSONL is the universal state form: pins (`state/mcp_pins.jsonl`), registry rows (`memory/workflows/REGISTRY.jsonl`, `workflow_gate.py:42`), ledgers, receipts. Nothing rewrites; everything grows; history is the data structure.
5. **Fail closed by exit code**: the 0/1/2 contract. 0 pass, 1 finding, 2 the gate itself is broken and must never be read as a pass. Documented verbatim at `violation_ratchet.py:28` ("1 = new violations found, 2 = gate itself broken"), `census_drift_patrol.py:30-32` ("2 = cannot verify", "a git failure is exit 2, never a guess and never a pass", lines 26-28), and `freshness_check.py:58-60` (git failure: "refusing to guess (exit 2)"). Only 3 files spell a literal `exit(2)` (`freshness_check`, `probe20_run`, `secret_gate`); the contract usually travels as main returning a code, so the literal count understates it. What the contract encodes is epistemic: unknown is a third value, distinct from both yes and no, and it must be loud.

Around the five verbs sits one piece of pure convention, costing zero lines of code: the receipt grammar (a dated path in `watch/inbox/`, numbers named with instrument and moment). This is enforced culturally through `AGENTS.md` and the ribs, and semi-mechanically by `workflow_gate.py:70-94`, where a receipt mention without a `YYYY-MM-DD` stamp is a soft WARN.

The theory name for this is worse-is-better (Gabriel's New Jersey style) applied to kernels: instead of factoring the trust primitives into one audited shared module, the estate lets every tool carry its own tiny copy of the same five idioms. The cost is 190 near-duplicate preambles. The benefit is visible in the census: delete any single module in the repo and at most a handful of tools break. There is no single point of code coupling anywhere in `tools/` except the file that gives agents hands. Spores do not share organs, so no organ's death is contagious.

## 6. Trusting trust: the seat is the compiler, prose is the binary

The estate's deepest bootstrap fact is that the thing compiling its source is not CPython. It is the LLM seat, and the source language is `AGENTS.md` plus the ribs. Thompson's "Reflections on Trusting Trust" (1984) showed that a compromised compiler can propagate its compromise to every binary it builds, including a new compiler, invisibly, because nobody re-checks the compiler against its source. The estate has a live, benign instance of exactly this attack surface, and it measured it:

- The `**Tests:**` bullet in `AGENTS.md` carried a hand-copied "1,341 tests / 264 files" headline for 12 days while the real suite grew 31 files, because seats kept copying the claim from seats. A prose number that is copied forward without re-derivation is Thompson's self-replicating payload with the malice removed. `census_drift_patrol.py:4-8` names this disease as its reason to exist.
- The countermeasure is a recompilation pass: the patrol never trusts the carrier. It re-derives growth from git commits and on-disk bytes, fails closed on unparseable claims, and rejects a future-dated census as a "fabrication smell" (`census_drift_patrol.py:26-28`). This is the estate's analog of the stage-2-versus-stage-3 comparison: recompute the binary from source and diff.
- The same pattern, generalized: `mcp_pin.py:10-14` ("a tool server (or anything between us and it) can rewrite a description to smuggle new instructions... A hash pin turns that from invisible to loud") is Thompson applied to tool descriptions; the ratchet's fingerprints applied to debt claims; `freshness_check.py:11` ("STALE when its last commit is older than STALE_DAYS while the repo itself has heartbeat") applied to doctrine itself. The estate's trust model is: every claim is a binary, every binary gets a hash, every hash gets an expiry. Trust is per-claim, byte-derived, and decays.

One honest asymmetry: the true stage-zero anchor, the `.venv` CPython 3.11.15 interpreter itself, is hash-pinned nowhere that I found in this session's reading. The estate verifies its claims down to the byte but inherits its interpreter on faith. That is the one link in the chain with no recompilation pass, and it is worth naming as the residual trusting-trust exposure.

## 7. The fixed point, and gates as scar tissue

Two live runs today show the verifier stratum is not decorative:

```
RATCHET check: scope=20 changed files; hits=16; registered=13; NEW=3
  NEW 84291bf5f2af246b file-too-long: mag/corpus_gap_research.py:663 (over 400 lines)
  NEW 42b721c740d1abda file-too-long: mag/corpus_selfsteal.py:460 (over 400 lines)
  NEW 2c7e16bf178da9d0 shell-true: tools/fossil_check.py:73
RATCHET: FAIL ... RATCHET_EXIT=1

CENSUS-PATROL: ok - census 2026-09-27 (2303 collected / 352 files)
  grew: 2026-09-28 tests/test_silentpass_batch2.py (+ 4 more)
  disk candidate files: 369
CENSUS-PATROL: ok ... PATROL_EXIT=0
```

The ratchet failing loudly on the working tree of the very audit that is praising it is the strongest bootstrap evidence available: a kernel that reports its own state honestly, including its own unfinished debt, is a kernel. And the patrol passing with a named instrument lag (disk 369 vs carrier 352, "instrument lag: disk counts pytest-named candidates, carrier counts item-bearing files") shows the census-denominator law (B2-216) running as designed: name the instrument, moment, and delta.

Two structural observations close the loop:

- **The gates are subject to their own law.** `census_drift_patrol.py:40-51` records that the file had to split its self-test (B2-248) and its byte-gatherers (B2-365) into sibling modules to stay under the ratchet's 400-line bar. The verifier obeys the ratchet it enforces. That is the fixed point a bootstrap aims at: the system's rules apply to the rule-makers, and the history of compliance is itself an append-only receipt.
- **Each gate is the fossil of a named incident, not a design decision.** The patrol exists because of the 12-day stale headline; `violation_ratchet.py:10-17` exists because a prune reaped 25 mimosa claims (B2-95); `workflow_gate.py:4` exists because of an operator order; the ephemeral-overlay and static-no-shadow machinery in `tools/__init__.py:52-108` and the shape-collapse defense in `tools/__init__.py:133-173` each cite a specific run's failure (the 2026-08-06 `run_shell` loop, 25k rows; the 2026-08-03 12h sovereign run, bug 2). Verification here has no origin in design review. It is secreted by failure, one gate per wound. The gate stratum is the estate's immune memory, and like immune memory it is the youngest and fastest-growing tissue.

## 8. The rebuild thought experiment

If the estate were wiped down to its git history and had to be rebuilt, the dependency graph says the true minimal kernel is:

- CPython plus stdlib (trusted, unpinned: the one act of faith),
- `config.py` plus the 2026-08-04 quartet (`tools/__init__.py`, `filesystem.py`, `shell.py`, `code_execution.py`): 1,000 lines total, giving an agent hands and paths,
- the receipt grammar as prose convention (zero LOC, carried in `AGENTS.md` and ribs).

Everything else is regrowth. The 72 percent leaf fraction is the deep antifragility property: leaves are cheap because leaves share nothing. The expensive-to-rebuild part is the 145-module mag tangle, and notably the four tools trapped inside it. A refactor worth naming for the estate: the tangle's four naturalized tools are the seed crystal of any future decomposition; they mark exactly where tool-land and runtime-land fused. And if only one stratum could be kept, it should be the six gate files (none over 500 lines): without them the prose carrier decays at the measured rate of hand-copying, which the 09-26 disease pegged at 31 files of drift in 12 days. Capability regrows from spores; honesty does not regenerate without the recompilation passes.

## 9. Not run, not verified (OWED)

- The `.venv` interpreter provenance is unpinned (stated above); I did not hunt outside the repo for a pin.
- The sibling-import scan is heuristic; the 29 tool-to-tool edges are a lower bound.
- `workflow_gate` scenario mode and `corpus_fts_rebuild --check --deep` were not executed this session; the two live runs were ratchet and patrol only.
- Census #1 counted `models` as a top-level import in some tools; repo root has no `models.py` and greps for `import models` / `from models import` under `tools/` return nothing, so those entries are subproject-local resolution artifacts of my classifier, not root glue. `config.py` is the only verified root-glue module.
- The exact size of the runtime SCC depends on whether relative imports are counted (145 vs 200+); both numbers are mine, the honest claim is a range.

## 10. Register

Primary sources read in full this session: `tools/__init__.py` (263 lines), `tools/violation_ratchet.py` (head), `tools/workflow_gate.py` (head), `tools/census_drift_patrol.py` (head), `tools/mcp_pin.py` (head), `tools/freshness_check.py` (head), `config.py` (head). Literature engaged: Thompson, "Reflections on Trusting Trust" (CACM 27:8, 1984); the GCC three-stage bootstrap and the Bootstrappable Builds / live-bootstrap chain as the verifier-first pole; Gabriel, "Worse Is Better" as the no-shared-kernel pole; Forth's dictionary-from-primitives as the spore model's nearest cousin.
