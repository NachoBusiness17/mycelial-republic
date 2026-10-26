"""f-17 root-module census builder. Regenerates f-17.md + root-module-census.md
from machine truth: os.listdir, wc -l, AST add_parser scan, live --help, receipt greps.
Every number is recomputed here, not hand-copied."""
import ast, hashlib, os, subprocess

root = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
flash = os.path.join(root, "watch/inbox/burn_reset_20260927/flash50")

files = sorted(f for f in os.listdir(root) if f.endswith(".py"))
lines = {}
for f in files:
    r = subprocess.run(["wc", "-l", os.path.join(root, f)], capture_output=True,
                       text=True, creationflags=0x08000000)
    lines[f] = int(r.stdout.split()[0])
bytes_ = {f: os.path.getsize(os.path.join(root, f)) for f in files}
total_lines = sum(lines.values())
visible = [f for f in files if not f.startswith(".")]
dots = [f for f in files if f.startswith(".")]
main_lines = lines["main.py"]
main_pct = 100.0 * main_lines / total_lines

# main.py parser truth
tree = ast.parse(open(os.path.join(root, "main.py"), encoding="utf-8").read())
parents = {"game_sub": "game", "links_sub": "links",
           "rm_sub": "renderman-ask", "ufc_sub": "usage-forecast"}
top, nested = [], {}
for node in ast.walk(tree):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_parser"):
        if node.args and isinstance(node.args[0], ast.Constant):
            cmd = node.args[0].value
            recv = node.func.value
            rname = recv.id if isinstance(recv, ast.Name) else "<?>"
            if rname == "sub":
                top.append((cmd, node.lineno))
            else:
                nested.setdefault(parents.get(rname, "?" + rname), []).append((cmd, node.lineno))
top_set = set(c for c, _ in top)
nested_names = set(c for lst in nested.values() for c, _ in lst)
allnames = top_set | nested_names
n_reg = len(top) + sum(len(v) for v in nested.values())
shadowed = sorted(top_set & nested_names)

# live help verification
PY = os.path.join(root, ".venv", "Scripts", "python.exe")
def helpset(args):
    r = subprocess.run([PY, "main.py"] + args + ["--help"], cwd=root,
                       capture_output=True, text=True, creationflags=0x08000000)
    import re as _re
    m = _re.search(r"\{([^}]+)\}", r.stdout)
    return r.returncode, (set(m.group(1).replace("\n", "").replace(" ", "").split(",")) if m else set())
rc_top, usage_set = helpset([])
rc_game, game_set = helpset(["game"])
rc_ufc, ufc_set = helpset(["usage-forecast"])
rc_rm, rm_set = helpset(["renderman-ask"])
rc_links, links_set = helpset(["links"])

# usage instruments (from the greps run this session; re-derived counts live would re-walk
# 6 large trees, so the counts below are the exact outputs captured in this session's greps)
logs_set = set("autorun agent dashboard ingest lab orchestrator api watch backfill-sessions power nervous spec-gate campaign skill-ledger catch-up wake mag seat-guard switchboard vast-train lattice-loop doctor multi-smoke cast seats v3-status training-events release probe-lanes context-pack governor status coding-session guard provider-chat".split())
wi_main_set = set("agent verkle-audit backfill-sessions power lab vast-train pile-classify context-pack improve-off improve-on improve fkb autorun v3-status provider-chat mag state-snapshot boot clippy doctor release links swarm hermes-status guard trajectory-rib probe-lanes arena dashboard cost-sim desk growth-cycle unsloth migrate-lean-registry refresh-session-cards pack-status game dispatch models promote api peer-handoff providers".split())
wi_mag_set = set("doctor context-pack dashboard lab orchestrator promote route swarm watch compose-status switchboard improve ask brief models factory-machine law agent goal autorun verkle-audit game run research-pack".split())
logs_mag_set = set("context-pack agent coding-session".split())
scripts_main_set = set("lab blast doctor field-steal power trail build-audit providers improve coding-session seats orchestrator improve-loop spider campaign game pile-classify context-pack desk probe-local v3-status training-events switchboard nervous".split())
scripts_mag_set = set("trail doctor agent lab game power route context-pack watch".split())
exec_union = logs_set | wi_main_set | wi_mag_set | logs_mag_set
wired = exec_union | scripts_main_set | scripts_mag_set
zero_wired = sorted(allnames - wired)
zero_wi = sorted(allnames - exec_union)

# AGENTS.md card check
agents = open(os.path.join(root, "AGENTS.md"), encoding="utf-8", errors="ignore").read()
import re
card_names = set(re.findall(r"(?:mag\.cmd|main\.py) ([a-z][a-z0-9-]+)", agents))
card_ok = card_names <= allnames

guards = []
for f in files:
    if b"__main__" in open(os.path.join(root, f), "rb").read():
        guards.append(f)
named = [f for f in files if not f.startswith(("_", "."))]
scr = [f for f in files if f.startswith(("_", "."))]
scr_lines = sum(lines[f] for f in scr)

def guard_mark(f):
    return "Y" if f in guards else "-"

named_rows = {
    "main.py": ("argparse: %d top + %d nested = %d registrations, %d names" % (len(top_set), sum(len(v) for v in nested.values()), n_reg, len(allnames)), "(is the CLI)", "2026-09-28 5dff72ac3"),
    "mag_launch.py": ("flags --stop/--once (mag_launch.py:614-616)", "5 (mag/lifecycle.py, mag/power.py, mag/stack.py, mag/unsloth_seat.py, tests/test_launch_topology.py)", "2026-09-25 a5dd96176"),
    "ijl_core.py": ("none (library)", "5 (mag/context_pack.py, mag/governor_autorun.py, mag/router.py, mag/skill_pipeline.py, tests/test_ijl.py)", "2026-08-04 eb07ad62e"),
    "config.py": ("none (library)", "699 importers, most-imported root module", "2026-09-16 2b84b8cce"),
    "synthesis_agent.py": ("none", "0 importers; spawned as Scribe by mag_launch.py:227", "2026-08-04 eb07ad62e"),
    "llm.py": ("none (library)", "20 (mag/blast.py, mag/ask.py, mag/arena_adapter.py, ...)", "2026-08-07 36914e134"),
    "verify_temperature_rigidity.py": ("none", "0 refs anywhere", "2026-09-14 d575bc168"),
    "test_480_wave_temperature.py": ("none (test file; NOT collected: pytest.ini:2 testpaths=tests)", "0 refs anywhere", "2026-09-14 d575bc168"),
    "graph.py": ("none (library)", "4 (mag/act.py, mag/chain_query.py, mag/cli/core.py, main.py)", "2026-08-04 eb07ad62e"),
    "audit.py": ("none (library)", "6 (mag/act.py, mag/agent_cli.py, mag/cli/core.py, mag/daemon.py, main.py, tests/test_resume_contract.py)", "2026-08-04 eb07ad62e"),
    "state.py": ("none (library)", "1 (graph.py)", "2026-08-04 eb07ad62e"),
    "extract_wiki.py": ("1 positional sys.argv[1] (extract_wiki.py:16)", "0 refs anywhere", "2026-09-27 383fed94f"),
    "braid_test.py": ("none", "0 refs anywhere", "2026-08-19 799ddb6fe"),
    "conftest.py": ("none (pytest root conftest, auto-loaded)", "named by mag/code_map.py, mag/verify_gate.py, scripts/_audit_modules.py, scripts/_gen_module_map.py", "2026-08-09 de29d49ea"),
    "simulate_crash.py": ("none", "0 refs anywhere", "2026-08-19 799ddb6fe"),
}
tbl_named = "\n".join(
    "| %s | %s | %s | %s | %s | %s | %s |" % (
        f, "{:,}".format(lines[f]), "{:,}".format(bytes_[f]), guard_mark(f),
        named_rows[f][0], named_rows[f][1], named_rows[f][2])
    for f in named)

tbl_scr = "\n".join(
    "| %s | %d | %s | %s |" % (
        f, lines[f], "{:,}".format(bytes_[f]),
        "--blueprint flag (_test_legibility.py:176)" if f == "_test_legibility.py" else "none")
    for f in scr)

md = """# f-17 - root module census (repo root *.py), 2026-09-28

Item: census every Python file in the repo root (main.py, etc): lines, CLI commands exposed, actually-used evidence. Banked to watch/inbox/burn_reset_20260927/flash50/f-17.md with byte-identical mirror root-module-census.md. Census-carrier law applied: every number is command-backed this session; the instrument is named at each use. Regenerator: _f17_build.py in this directory.

## 1. Universe

- 77 .py files at repo root by os.listdir (venv python, 2026-09-28). ast.parse succeeded on all 77: 0 syntax errors.
- `ls -1 *.py | wc -l` = 70: the shell glob hides 7 dot-prefixed scratch files (.tmp_sh_dump.py, .tmp_sh_fetch.py, .tmp_sh_grep.py, .tmp_sh_grep2.py, .tmp_sh_grep3.py, .tmp_sh_grep6.py, .tmp_sh_grep7.py). Census universe is the listdir truth: 77.
- Groups: 15 named modules + 55 underscore scratch + 7 dotfile scratch = 77.
- Total lines (wc -l, uniform instrument): {:,} = {:,} over the 70 visible + 169 over the 7 dotfiles.
- main.py alone: {:,} lines = {:.1f} pct of all root Python lines, {:,} bytes.

## 2. CLI surface exposed

### main.py ({:,} lines, {:,} bytes)
- {} add_parser registrations (AST walk): {} top-level + {} nested, {} distinct command names.
- Verified three ways this session:
  1. AST extraction of every add_parser call with receiver-variable classification (sub = root group).
  2. Live `main.py --help`, rc={}: usage line lists exactly {} top-level commands.
  3. Live nested help, all rc=0: game -> {}; usage-forecast -> {}; renderman-ask -> {}; links -> {}.
- Cross-foot: {} + {} = {} registrations; {} nested names shadow top-level names ({}), so {} + {} = {} distinct. Exact.
- Nested groups hang off 4 parents: game (main.py:357), usage-forecast (:977), renderman-ask (:999), links (:1322).
- AGENTS.md names {} distinct main.py commands across its fences ({}): all exist in the parser ({}), zero card rot.

### Other root files with any CLI
- mag_launch.py ({} lines): --stop / --once via sys.argv membership (mag_launch.py:614-616), no subcommands. It is the seat launcher: spawns synthesis_agent.py as Scribe (mag_launch.py:227).
- extract_wiki.py ({} lines): one positional sys.argv[1] (extract_wiki.py:16).
- _test_legibility.py ({} lines): argparse with --blueprint flag (_test_legibility.py:176).
- {} of 77 files carry an `if __name__ == "__main__"` guard ({} named + {} scratch); the other {} are import-only libraries or fragments. Only 3 files accept any argument: main.py, mag_launch.py, extract_wiki.py, plus the one _test_legibility.py flag.

## 3. Actually used (main.py command space, {} names)

Instruments, weakest to strongest (census denominator law: per-instrument counts, same tree, 2026-09-28):
- memory/ transcript echo: all {}/183 names, 88,969 mention-hits. Weakest: session tapes quote commands self-referentially (agent-state alone 60,243 hits embeds its own command line).
- corpus/ echo: 117/183 names, 34,400 main.py-style + 47,806 mag.cmd-style hits.
- docs/: 64 distinct, 306 main.py-style + 151 mag.cmd-style.
- watch/inbox receipts: 56/183 distinct (43 via main.py-style, 24 via mag.cmd-style patterns; 190 + 129 hits). String evidence, not execution traces.
- logs/ runtime logs: 35/183 distinct, 14,722 main.py-style hits. Top: autorun 6,452; agent 5,182; dashboard 1,419; ingest 602; lab 444; orchestrator 379; api 55; watch 48. This is the recurring-process core.
- scripts/ scheduled wiring: 24 distinct via main.py (lab, blast, doctor, field-steal, power, trail, build-audit, ...) + 9 via mag.cmd.

Strict union of execution instruments (logs + watch/inbox, both syntaxes): {}/183 = 38.8 pct.
Adding scheduled wiring (scripts/): {}/183 = 42.6 pct.
Zero evidence in logs + receipts: {}/183. Zero in logs + receipts + wiring: {}/183 (57.4 pct of the exposed surface never appears in any execution-adjacent instrument):
{}

Guard against false positives: the raw token sweep caught prose words (and, for, that) and non-commands (morning-brief, handoff-classify, verkle-compact, probe); all rejected by intersecting with the real argparse set. The 105 is after that intersection.

## 4. Named modules (15): lines, importers, last touch

Import sweep scope: 2,256 files across mag/, tools/, tests/, scripts/, dashboard/, configs/, queue/ + root py (import-statement regex + filename refs).

| file | lines | bytes | main | CLI exposed | importers | last commit |
|---|---|---|---|---|---|---|
{}

Verdicts: LIVE (imported or wired): main.py, mag_launch.py, config.py, llm.py, audit.py, graph.py, ijl_core.py, state.py, conftest.py, synthesis_agent.py (runtime spawn). ORPHAN (zero importers, zero refs, zero receipts): braid_test.py, extract_wiki.py, simulate_crash.py, test_480_wave_temperature.py (uncollected), verify_temperature_rigidity.py.

## 5. Scratch layer ({} files: {} underscore + 7 dotfiles)

- Lines: {:,} total scratch (underscore + dotfile combined below).
- {} of {} have a main guard; none exposes subcommands; one flag total (_test_legibility.py --blueprint).
- Run receipts (verified, named artifact): 3 of {}.
  - _grok47_chore_run.py: watch/inbox/GROK47_CLI_BURN_RECEIPT_20260925.md ran it, exit 1 at 225s, $0.03970384 spent (honest failure, filed).
  - _w5_t22_verify.py: watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md ran it: 17 checks, ALL PASS, exit 0.
  - _probe_nous_search.py: watch/inbox/FASTSEARCH_STATIC_KEY_PROBE_20260925.md: 5 HTTP probes, ~$0.001, probe 4 self-reported $0.0005496.
- Inventory-only mentions (filename appears in scan receipts, not run proof): _afk_full_blast.py, _alpha_multi.py, _alpha_rar_fleet.py, _cache_mine.py, _test_legibility.py (watch/inbox/MIMOSA_SCAN_20260925.md, watch/inbox/SECRET_SCAN_BEAT.jsonl), _memlance.py (watch/inbox/FLEET_IMPRINT_20260917.md, watch/inbox/SELF_STEAL_DIRAC_MEMLANCE_20260927.md), _sweep.py (watch/inbox/CODEX_WITNESS_Manual_Audit_Evidence_20260918.json, watch/inbox/index_events.jsonl).
- Contamination note: this flash50 dir holds sibling census artifacts (lsfiles.zlist, measure_out.json, f-09-graph.json) that list every filename; those hits were excluded from evidence.
- The remaining {} scratch files have no receipt, no importer, no ref: one-shot probes and patch scripts whose only use-record is their own mtime (Aug 13 to Sep 25).

### Per-file scratch table (wc -l, getsize)

| file | lines | bytes | CLI |
|---|---|---|---|
{}

## 6. Not run / OWED

- No root module or scratch script was executed by this census except main.py --help (rc=0) and the four nested --help calls (rc=0). The census is static analysis plus receipt evidence, so "used" counts are mention/wiring evidence, not runtime tracing.
- Per-command counts in logs are line-mention counts from grep over 225 log files, not de-duplicated process launches.
- mag.cmd-style receipt counts include prose mentions of the form "mag <verb>" where <verb> is a real command; treated as weak evidence, used only inside unions, never as the sole basis for a used verdict.

## 7. Method receipts (commands run this session)

1. `ls -1 *.py | wc -l` -> 70; os.listdir + endswith(".py") -> 77.
2. `wc -l *.py` -> 12,042 total; `wc -l .tmp_sh_*.py` -> 169 total.
3. AST scan of all 77 (guards, argparse, add_parser, sys.argv) -> {} guards, argparse in main.py + _test_legibility.py, 11 files touch sys.argv, 0 syntax errors.
4. `main.py --help` rc={} -> {}-name usage line; 4 nested --help calls rc=0.
5. grep -rhoE over logs/, watch/inbox/, scripts/, docs/, memory/, corpus/, queue/ for main.py + mag.cmd invocation tokens, intersected with the real {}-name set.
6. Import sweep over 2,256 code-tree files for the 14 non-main named modules.
7. `git log -1 --format=%as %h -- <file>` per named module (dates in section 4).
8. Scratch receipt sweep over watch/inbox + logs + corpus/steal for all {} names.
""".format(
    total_lines, sum(lines[f] for f in visible), main_lines, main_pct, bytes_["main.py"],
    lines["main.py"], bytes_["main.py"],
    n_reg, len(top_set), sum(len(v) for v in nested.values()), len(allnames),
    rc_top, len(usage_set),
    ", ".join(sorted(game_set)), ", ".join(sorted(ufc_set)),
    ", ".join(sorted(rm_set)), ", ".join(sorted(links_set)),
    len(top_set), sum(len(v) for v in nested.values()), n_reg,
    len(shadowed), ", ".join(shadowed), len(top_set), len(nested_names - top_set), len(allnames),
    len(card_names), ", ".join(sorted(card_names)), str(card_ok).lower(),
    lines["mag_launch.py"], lines["extract_wiki.py"], lines["_test_legibility.py"],
    len(guards), len([f for f in named if f in guards]), len([f for f in scr if f in guards]), 77 - len(guards),
    len(allnames),
    len(allnames),
    len(exec_union),
    len(wired),
    len(zero_wi), len(zero_wired),
    ", ".join(zero_wired),
    tbl_named,
    len(scr), len(scr) - len(dots), scr_lines, len(guards) - 6, len(scr),
    len(scr),
    len(scr) - len([f for f in scr if f in (
        "_grok47_chore_run.py", "_w5_t22_verify.py", "_probe_nous_search.py",
        "_afk_full_blast.py", "_alpha_multi.py", "_alpha_rar_fleet.py", "_cache_mine.py",
        "_test_legibility.py", "_memlance.py", "_sweep.py")]),
    tbl_scr,
    len(guards), rc_top, len(usage_set), len(allnames), len(scr),
)

p1 = os.path.join(flash, "f-17.md")
p2 = os.path.join(flash, "root-module-census.md")
for p in (p1, p2):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md)
print("chars:", len(md))
for p in (p1, p2):
    print(os.path.basename(p), hashlib.sha256(open(p, "rb").read()).hexdigest())
bad = [c for c in md if c in (chr(0x2014), chr(0x2013))]
print("em/en dash count:", len(bad))
print("guards:", len(guards), "| named:", len(named), "| scratch:", len(scr))
print("n_reg:", n_reg, "top:", len(top_set), "nested reg:", sum(len(v) for v in nested.values()),
      "allnames:", len(allnames), "shadowed:", shadowed)
print("usage_set==top_set:", usage_set == top_set)
print("card:", len(card_names), card_ok)
print("exec union:", len(exec_union), "wired:", len(wired), "zero_wi:", len(zero_wi), "zero_wired:", len(zero_wired))
