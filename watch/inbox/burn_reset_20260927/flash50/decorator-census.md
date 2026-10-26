# s2-24: decorator census - mag/ + tools/

Date: 2026-09-28. Snapshot: branch `mag/run-beta1-factory-build-audi-20260806T231709Z`, HEAD `f576b0ec9` (read at scan time).

Scope: every decorator expression on every function, method, and class in
every .py file under `mag/` and `tools/` (recursive), extracted with
Python `ast` from source bytes. All numbers below come from the scanner
run recorded in the Receipt section.

## Method

- interpreter: `.venv/Scripts/python.exe` (3.11.15)
- scanner: `watch/inbox/burn_reset_20260927/flash50/_s2_24_scan.py`
  (AST walk, bytes in, no shell spawn except three `git` reads with
  CREATE_NO_WINDOW on win32)
- run command: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_s2_24_scan.py`
- files found: mag 1037 + tools 190 = 1227 .py; parsed OK 1227; parse failures 0
- live-tree drift note: an earlier probe glob in this same session read
  mag 1036 + tools 190 = 1226; one mag file landed between the two commands
  (sibling lanes are active). Census numbers are the scanner moment.
- untracked .py in scope (git ls-files): 4: mag/corpus_gap_repack.py, mag/corpus_gap_research.py, mag/corpus_selfsteal_prove.py, tools/prompt_compiler.py
- decorator expressions collected by ast: 270
- independent recount: physical lines whose stripped form starts with `@`: 276
  (difference 6; explained in Limits)
- docs corpus scanned for custom-decorator mentions: 509 files, 4843683 bytes

## Totals

- unique decorator names: 22
- decorated functions incl. methods (decorator-to-def rows, a def with N decorators counts N times): 132 (of which methods: 37)
- decorated classes (same counting rule): 138
- every class-decoration row is dataclasses: `@dataclass` 130 + `@_dc` 8
  (a module-level alias of `dataclasses.dataclass`) = 138
- total defs in scope: 11374 functions + 258 classes
- files containing at least one decorator: 84 of 1227 parsed
- call form vs bare form: 107 `@x(...)` / 163 bare `@x`
- rows by kind: stdlib 8, custom 6, builtin 3, third-party 3, unresolved 2

Tree shape (files per second-level dir, top 12): mag/cli 3, mag/tests 2, mag/__init__.py 1, mag/_bench_free_shelf.py 1, mag/_cache_ab_probe.py 1, mag/_codex_seat.py 1, mag/_comb_tokens.py 1, mag/_compare_chain_sources.py 1, mag/_conc_test_slot.py 1, mag/_consensus_witness.py 1, mag/_deep_research_verkle_dedupe.py 1, mag/_demo_eyes_receipt.py 1

## Table: every unique decorator name (sorted by function uses)

| decorator | kind | origin / def site | funcs | methods | classes | files | call-form |
|---|---|---|---:|---:|---:|---:|---:|
| `@app.get` | unresolved |  | 25 | 0 | 0 | 1 | 25 |
| `@route` | custom | mag/api_gateway.py:104 | 14 | 0 | 0 | 1 | 14 |
| `@app.post` | unresolved |  | 13 | 0 | 0 | 1 | 13 |
| `@property` | builtin | builtins | 12 | 12 | 0 | 8 | 0 |
| `@family` | custom | tools/duty_fuzz.py:202 | 10 | 0 | 0 | 1 | 10 |
| `@staticmethod` | builtin | builtins | 10 | 10 | 0 | 8 | 0 |
| `@_register` | custom | tools/local_bench.py:67 | 9 | 0 | 0 | 1 | 9 |
| `@_verifier` | custom | tools/local_bench.py:77 | 9 | 0 | 0 | 1 | 9 |
| `@app_commands.command` | third-party | discord.app_commands.command | 5 | 5 | 0 | 1 | 5 |
| `@app_commands.describe` | third-party | discord.app_commands.describe | 5 | 5 | 0 | 1 | 5 |
| `@classmethod` | builtin | builtins | 5 | 5 | 0 | 4 | 0 |
| `@contextlib.contextmanager` | stdlib | contextlib.contextmanager | 5 | 0 | 0 | 5 | 0 |
| `@lru_cache` | stdlib | functools.lru_cache | 3 | 0 | 0 | 3 | 3 |
| `@_state_locked` | custom | mag/agent_state.py:111 | 1 | 0 | 0 | 1 | 0 |
| `@app.api_route` | third-party | fastapi.FastAPI.api_route | 1 | 0 | 0 | 1 | 1 |
| `@asynccontextmanager` | stdlib | contextlib.asynccontextmanager | 1 | 0 | 0 | 1 | 0 |
| `@contextmanager` | stdlib | contextlib.contextmanager | 1 | 0 | 0 | 1 | 0 |
| `@functools.lru_cache` | stdlib | functools.lru_cache | 1 | 0 | 0 | 1 | 1 |
| `@functools.wraps` | stdlib | functools.wraps | 1 | 0 | 0 | 1 | 1 |
| `@gw.route` | custom | mag/api_gateway.py:104 | 1 | 0 | 0 | 1 | 1 |
| `@_dc` | stdlib | dataclasses.dataclass | 0 | 0 | 8 | 4 | 0 |
| `@dataclass` | stdlib | dataclasses.dataclass | 0 | 0 | 130 | 61 | 10 |

## Stdlib and third-party decorators (what they do)

Standard-library rows state standard Python semantics; discord.py and
FastAPI rows state their framework behavior; anything still unknown stays
with its own module docs rather than guessed.

| decorator | origin module | funcs | what it does |
|---|---|---:|---|
| `@property` | builtins | 12 | builtin: computed attribute getter |
| `@staticmethod` | builtins | 10 | builtin: method that receives no implicit self/cls |
| `@app_commands.command` | discord.app_commands.command | 5 | discord.py: registers the coroutine as a Discord application (slash) command |
| `@app_commands.describe` | discord.app_commands.describe | 5 | discord.py: attaches human-readable parameter descriptions to an app command |
| `@classmethod` | builtins | 5 | builtin: method that receives cls instead of self |
| `@contextlib.contextmanager` | contextlib.contextmanager | 5 | stdlib: turns a generator function into a with-statement factory |
| `@lru_cache` | functools.lru_cache | 3 | stdlib: memoizes function results in an LRU cache |
| `@app.api_route` | fastapi.FastAPI.api_route | 1 | FastAPI: registers the handler for an HTTP method + path (same family as @app.get/@app.post) |
| `@asynccontextmanager` | contextlib.asynccontextmanager | 1 | stdlib: async version of contextmanager (async with support) |
| `@contextmanager` | contextlib.contextmanager | 1 | stdlib: turns a generator function into a with-statement factory |
| `@functools.lru_cache` | functools.lru_cache | 1 | stdlib: memoizes function results in an LRU cache |
| `@functools.wraps` | functools.wraps | 1 | stdlib: copies __name__/__doc__/__module__ onto wrapper functions inside decorator bodies |
| `@_dc` | dataclasses.dataclass | 0 | stdlib alias: module-level `name = dataclass` assignment; generates __init__/__repr__/__eq__ from class annotations |
| `@dataclass` | dataclasses.dataclass | 0 | stdlib: generates __init__/__repr__/__eq__ from class annotations |

## Custom decorators (defined inside mag/ or tools/)

Custom decorator names: 6. Documentation rubric: **documented** = has a docstring at the definition AND >=1 mention of its name in `docs/` or a root `*.md`; **docstring-only** = docstring, no doc-tree mention; **undocumented** = neither. Mixed rows (one of the two signals) state their exact evidence in the block. Result: 2 documented / 0 docstring-only / 3 undocumented. Override applied after reading, see blocks: the two "documented" rows earn their doc-tree signal from the common English word "route" in prose, so their true grade is docstring-only.

### `@route`

- def site(s): mag/api_gateway.py:104
- decorator is a function
- docstring at def: yes: "Decorator factory registering ``fn`` for ``method`` + ``path``. ``path`` may contain ``{name}`` segments captured as path params, e.g. ``/it"
- doc-tree mentions: 102 file(s); example: docs/ARCHITECTURE.md
- what it does (read at def site, mag/api_gateway.py:104-117): decorator factory; the returned closure stores `fn` in `_ROUTES[method][path]` and returns it unchanged; `{name}` path segments become captured params; registering the same (method, path) twice silently overwrites
- uses: 14 function(s) (0 methods), 0 class(es), across 1 file(s); count 14 (14 call-form)
- first use sites: mag/api_gateway.py:188, mag/api_gateway.py:194, mag/api_gateway.py:227
- verdict (refined after read): docstring-only. The 102 name matches are the common English word "route" in prose (first hit docs/ARCHITECTURE.md), not documentation of this decorator; `git grep -c "api_gateway" -- docs | wc -l` reads 0 files. Documented at the def site only.

### `@family`

- def site(s): tools/duty_fuzz.py:202
- decorator is a function
- docstring at def: no
- what it does (read at def site, tools/duty_fuzz.py:202-206): decorator factory; appends `{"name", "duties", "fn"}` to the module-level `FAMILIES` list and returns the scenario-builder unchanged; no docstring
- doc-tree mentions: 36 file(s); example: docs/archive/ZEITGEIST.md
- uses: 10 function(s) (0 methods), 0 class(es), across 1 file(s); count 10 (10 call-form)
- first use sites: tools/duty_fuzz.py:210, tools/duty_fuzz.py:235, tools/duty_fuzz.py:261
- verdict: undocumented. The 36 "family" matches are the common English word in prose, and `git grep -c "duty_fuzz" -- docs | wc -l` reads 0 files; the def has no docstring.

### `@_register`

- def site(s): tools/local_bench.py:67
- decorator is a function
- what it does (read at def site, tools/local_bench.py:67-71): decorator factory; stores `fn` in the module `TASKS` dict under `name` (prompt-builder registry) and returns it unchanged; no docstring
- docstring at def: no
- doc-tree mentions: 0 file(s)
- uses: 9 function(s) (0 methods), 0 class(es), across 1 file(s); count 9 (9 call-form)
- first use sites: tools/local_bench.py:93, tools/local_bench.py:107, tools/local_bench.py:120
- verdict: undocumented (no docstring; `git grep -c "local_bench" -- docs | wc -l` reads 0 files)

### `@_verifier`

- def site(s): tools/local_bench.py:77
- decorator is a function
- what it does (read at def site, tools/local_bench.py:77-81): decorator factory; stores `fn` in the module `_VERIFIERS` dict under `name` (verify-fn registry) and returns it unchanged; no docstring
- docstring at def: no
- doc-tree mentions: 0 file(s)
- uses: 9 function(s) (0 methods), 0 class(es), across 1 file(s); count 9 (9 call-form)
- first use sites: tools/local_bench.py:100, tools/local_bench.py:114, tools/local_bench.py:127
- verdict: undocumented (no docstring; `git grep -c "local_bench" -- docs | wc -l` reads 0 files)

### `@_state_locked`

- def site(s): mag/agent_state.py:111
- decorator is a function
- what it does (read at def site, mag/agent_state.py:111-117): wraps `fn` so every call runs under `agent_state_lock()` (a lock-file acquire loop with timeout, released via unlink in `finally`); `functools.wraps` preserves the wrapped function's metadata; no docstring
- docstring at def: no
- doc-tree mentions: 0 file(s)
- uses: 1 function(s) (0 methods), 0 class(es), across 1 file(s); count 1 (0 call-form)
- first use sites: mag/agent_state.py:281
- verdict: undocumented by name. Host module note: `git grep -c "agent_state" -- docs | wc -l` reads 14 files, but none mention this decorator's name and the def has no docstring.

### `@gw.route`

Same def as `@route` (attribute access `gw.route` on the imported module object, first use mag/mcp_http.py:33); the scanner lists it as its own row because the syntactic name differs.

- def site(s): mag/api_gateway.py:104
- decorator is a function
- docstring at def: yes: "Decorator factory registering ``fn`` for ``method`` + ``path``. ``path`` may contain ``{name}`` segments captured as path params, e.g. ``/it"
- doc-tree mentions: 102 file(s); example: docs/ARCHITECTURE.md
- uses: 1 function(s) (0 methods), 0 class(es), across 1 file(s); count 1 (1 call-form)
- first use sites: mag/mcp_http.py:33
- verdict (refined after read): docstring-only, same as `@route` (the 102 matches are the word "route" in prose).

## Unresolved or special rows

- `@app.get` (unresolved): 25 use(s) in 1 file(s); first: mag/ghost.py:1845
- `@app.post` (unresolved): 13 use(s) in 1 file(s); first: mag/ghost.py:1887
- Hand-resolution (read, not inferred): `app` is a function-local
  `app = FastAPI(title="Ghost Daemon", ...)` at mag/ghost.py:1841 and
  `from fastapi import FastAPI` sits at mag/ghost.py:1695 inside the same
  function. The scanner's alias pass only walks module-level assignments,
  so this pair reads unresolved; they are `fastapi.FastAPI.get` and
  `fastapi.FastAPI.post`, i.e. FastAPI HTTP route registration for 38 ghost
  daemon endpoints (25 GET + 13 POST). With them reclassified third-party,
  the kind tally reads: stdlib 8, custom 6 rows / 5 unique defs, builtin 3,
  third-party 5, unresolved 0.

## Limits

- Static ast scan: decorators attached dynamically (getattr, a decorator
  registry dict, decorator lib apply(), manual wrapper assignment) do not
  appear; only syntactic `@` applications count.
- Names bound by `from x import *` cannot be resolved; files with star
  imports: 0.
- The regex recount counts any physical line starting with `@` including
  ones inside string literals or comments and multi-line decorator-call
  arg lines never start with @; the ast count is the census number, the
  regex number is a second instrument for the same tree.
- A def with several decorators contributes one row-hit per decorator,
  so per-kind sums exceed distinct decorated defs; distinct-decorator
  def counts are not separately reported (row sums are the ask's unit:
  how many functions use each decorator).
- docs mention check is name-based (`\bname\b`) over docs/ + root *.md:
  short generic names can match prose (overcount); example file given
  per custom decorator so a human can spot-check.
- Aliases (module-level `name = decorator` assignments) resolved up to
  5 hops; deeper alias chains would show as unresolved.
- Class decorators are reported in their own column; the ask's headline
  unit is functions, which for this census includes methods (methods
  also broken out).
- parse failures: none

## External spot checks (separate commands, run after the scanner)

- Regex-vs-ast diff instrument (same 1227-file set): the 6 `@`-lines ast
  does not count are all inside strings, verified by reading them:
  mag/steal_first.py:215 and :311 are `@steal_first(...)` usage examples
  inside the StealFirstMiddleware class docstring; mag/x_control_surface.py:6
  is a module banner line starting with `@`; tools/seed_v2.py:738, :743,
  :752 are `@app.get(...)` lines inside embedded example code in a string.
  270 ast + 6 string lines = 276 regex lines.
- git grep occurrence-line counts vs ast table (tracked files only; the
  scan set had 4 untracked files, none named below):
  `@staticmethod` 10 = 10; `@property` 12 = 12; `@app.post` 13 = 13;
  `@_register` 9 = 9; `@_verifier` 9 = 9; `@family` 10 = 10; `@route(` 14 = 14;
  `gw.route` 1 = 1; `@app.get` 28 = 25 ast + 3 seed_v2.py docstring lines
  (:738 :743 :752); `@dataclass` 131 = 130 ast + 1 comment line
  (mag/riddler.py:84, "# A default @dataclass (eq=True) is UNHASHABLE...").
- Custom-decorator host modules in docs/ (`git grep -c <module> -- docs | wc -l`):
  api_gateway 0, duty_fuzz 0, local_bench 0, agent_state 14, ghost.py 4.
  No docs file documents any of the five custom decorators by name.
- Custom def sites read this session: mag/api_gateway.py:104-117,
  tools/duty_fuzz.py:202-206, tools/local_bench.py:61-81,
  mag/agent_state.py:111-117, mag/ghost.py:1835-1874 + :1695.

## Receipt

- instrument: `watch/inbox/burn_reset_20260927/flash50/_s2_24_scan.py`
- raw aggregates: `watch/inbox/burn_reset_20260927/flash50/_s2_24_decorators.json`
- twins: `decorator-census.md` and `s2-24.md` in the same directory,
  byte-identical (hash recorded in the commit message)

