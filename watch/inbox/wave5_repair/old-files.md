# wave5-repair / old-files: the three proven oldest-files defects, fixed

Date: 2026-09-29. Lane: old-files (gala wave5-repair, division B).
Defect source: `watch/inbox/burn_reset_20260927/flash50/s2-17.md` (census of the
10 oldest files by git log; three defects proven there, none fixed there).
Ownership honored: only `.gitignore`, `agents/escalate_grok.py`, `README.md`
edited. Changes left UNCOMMITTED in the working tree (branch
`mag/run-beta1-factory-build-audi-20260806T231709Z`); landing the commit is the
orchestrator's move.

## 1. .gitignore:22 - glued negation never fired (FIXED)

Before: line 22 was one line: `!.env.example# live provider/mesh credentials
<mojibake> never commit (tracked fix 2026-08-20)`. Gitignore `#` starts a
comment only at line start, so the whole line parsed as a negation pattern
matching nothing, and line 21 `.env.*` ignored `.env.example` (the file survived
only because it is already tracked). Byte proof of the mojibake taken before the
edit: the dash residue was `c3 a2 e2 82 ac 22` (double-encoded em-dash), while
line 18's comment carries a real UTF-8 em-dash `e2 80 94`.

Fix: split into two lines, `.gitignore:22` = `!.env.example` and `.gitignore:23`
= `# live provider/mesh credentials - never commit (tracked fix 2026-08-20)`
(ASCII hyphen in place of the mojibake bytes; line 18's pre-existing em-dash
left untouched). Diff: 2 insertions, 1 deletion; verified by `git diff`.

Proof (raw output: `watch/inbox/gala_20260925/wave5-repair/lanes/old-files.check.txt`):
- BEFORE: `git check-ignore -v --no-index .env.example` printed
  `.gitignore:21:.env.*	.env.example`, exit 0 (ignored).
- AFTER: same command prints `.gitignore:22:!.env.example	.env.example`
  (the winning rule is the negation), and the quiet boolean
  `git check-ignore -q --no-index .env.example` exits 1 = NOT ignored.
- Control: `touch .env.zzprobe && git check-ignore -v --no-index .env.zzprobe`
  still prints `.gitignore:21:.env.*` exit 0, so the `.env.*` rule itself is
  intact. Note: in `-v` mode exit 0 only means "a pattern matched"; the printed
  pattern is the winner; `-q` is the ignored/not-ignored truth.

Residual (NOT mine): `.zcodeignore:22` carries the same glued line, read this
session (`sed -n '18,26p' .zcodeignore`), left for its owner. If a wave owns
`.zcodeignore`, the identical one-line split applies.

## 2. agents/escalate_grok.py:89 - cwd=ROOT NameError swallowed (FIXED)

Before: line 89 passed `cwd=ROOT` with no ROOT import anywhere in the file
(grep ROOT returned only line 89). The harness escalation path raised NameError
inside the try at :82, which the blanket except at :111 folded into
`harness = {"ok": False, "error": "name 'ROOT' is not defined"}`; the node
silently degraded to park-only handoff forever. Reproduced before the fix with
the probe (below): exactly that error string, status stuck at `escalated`.

Fix: `agents/escalate_grok.py:13` now reads
`from config import HANDOFF_DIR, RESULTS_DIR, ROOT` (ROOT is `config.py:7`,
`Path(__file__).resolve().parent`, the repo root). Error path stays loud: the
except at :111 is untouched, failures still land in `harness["error"]`,
`out["grok_harness"]`, and the `audit.log_event` record at :115-122.

Probe instrument:
`watch/inbox/gala_20260925/wave5-repair/lanes/old-files.escalate_probe.py`
(patches `harness.grok_cli.harness_available` to True and
`escalate_via_harness` to a fake that records the cwd argument, then calls
`escalate_grok_node`; runs the real node end to end without a Grok CLI).
- BEFORE probe: `status: escalated`, `grok_harness:
  {"ok": false, "error": "name 'ROOT' is not defined"}`,
  `PROBE_RESULT: NAMEERROR_SWALLOWED`.
- AFTER probe: `status: escalated_grok_ran`, `cwd forwarded:
  C:\Users\foste\Documents\projects\local_sovereign_agent`,
  `cwd == config.ROOT: True`, `PROBE_RESULT: HARNESS_PATH_EXECUTED`.
- `python -m py_compile agents/escalate_grok.py` exit 0; bare
  `import agents.escalate_grok` exit 0.
Probe side effects: 3 runs wrote `queue/handoff/20260929-10{01,04,06}*-taskold-files-probe.{json,md}`
plus router-log lines and a CURRENT.md refresh, all gitignored runtime surfaces.

Scope note: `harness/grok_cli.py:47,70` already defaults `cwd` to its own ROOT
when None, so `cwd=ROOT` and `cwd=None` behave the same after the import; the
import fix is what the defect card names and what restores the author's intent
(escalate inside the repo).

## 3. README.md:213 - ends mid-sentence on "Also" (FIXED: cleanly marked)

The lost tail is not recoverable from git history (last substantive edit
2026-08-09 de7bb85fe per s2-17), so per the ask's second option the truncation
is cleanly marked: the dangling `Also` is removed and the file now ends with a
complete closing sentence naming the defect card and the repair. `tail -10
README.md` shows the note; `wc -l` = 218; last byte is `\n`. My README delta is
ONLY the tail change: the hunk `-Also` -> `+(Truncation note: ...)` is
6 added lines / 1 removed (README diffstat 14+/1- = my 6 plus the 8
pre-existing fence-owner lines).

Honesty flag: README.md already carried 8 uncommitted FW-11 fence-owner lines
(dated 2026-09-28, e.g. the "README quickstart card" stamps) in the working
tree BEFORE this lane started; they were present in my first Read of the file
and appear in the diff vs HEAD 6a6e35b59. Not mine, not touched by me. The
session-start git status listed README.md as modified.

## Ratchet (run voluntarily; NOT required by the ask)

No `mag/` or `tools/` file was touched, so the ask's ratchet condition does not
trigger. Ran it anyway for evidence:
`python tools/violation_ratchet.py check --changed` -> exit 1, scope "24 changed
files; hits=16; registered=13; NEW=3". The 3 NEW hits are
`mag/corpus_gap_research.py:663`, `mag/corpus_selfsteal.py:476`,
`tools/fossil_check.py:73` - none touched by this lane; `--changed` sweeps the
shared branch's whole in-flight tree. My three files are outside the ratchet's
`mag/`+`tools/` scan and produced zero hits. No `baseline-update` was run:
accepting other lanes' debt by name is not this lane's call.

## Decision ledger

Closes s2-17's "none fixed here - census only" verdict for all three defects:
- Grok harness escalation path went from dead-on-arrival since the root commit
  (eb07ad62e, 2026-08-04) to executable: `MAG_ESCALATE_HARNESS` unset now means
  the handoff is actually run headless when the CLI is present, not silently
  parked forever.
- The `.env.example` negation is effective for any future untracked copy (the
  tracked copy was never at risk, but every clone/fork that removes-and-reseeds
  the template was).
- The repo front door ends at a complete sentence with the truncation on
  record.

Raw check transcript (before + after + controls + ratchet):
`watch/inbox/gala_20260925/wave5-repair/lanes/old-files.check.txt`
Lane JSON: `watch/inbox/gala_20260925/wave5-repair/lanes/old-files.json`
