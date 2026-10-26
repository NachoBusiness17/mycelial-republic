# SP1_gate_exit_contract (anthropic/claude-opus-5.5, turn 1, channel: reasoning (content channel empty))

I need to carefully count through the workflow_gate.py file line by line to pin the exact line numbers for the spec document, starting from the shebang and module docstring at the top.

Continuing through the docstring, I trace the gate's purpose — born from an operator order to stop manual workflow pings and instead gate submissions automatically — then catalog the seven checks (G1 through G7) and the scenario mode requiring one scenario card per gate, each minted from a real registry FAIL row so future gate changes re-prove themselves.

Writing check definitions...

Adding more gate checks...

Now I'm defining the G6 stamp regex, following the same pattern as the freshness gate's case-insensitive label-colon-date format, so a receipt reference without a matching dated line counts as a soft finding rather than a hard gate failure.

I'm extending the judge-independence logic: since the subagent facade only exposes the session model, independence has to be declared explicitly via a `judge-model:` stamp naming the cross-family model used when firing a workflow with a fresh-reader judge seat. I'm writing a regex to detect that stamp, so G3 steering without it triggers the soft-warn tied to the B2-60 finding, leaving the exit contract unchanged.

Now I'm building the `run_checks` function that runs all seven gate checks over the script text and assembles result rows, with special handling so the G6 soft-false case gets flagged with a reason without being counted among the hard failures.

Finishing the soft-reason assignment, then I'm adding a helper to split rows into failed and warned id lists based on the ok/soft flags, and starting a function to index registry rows by timestamp and digest while tolerating malformed lines.

Writing validation logic...

Still validating expected_verdict fields...

Now I'm writing the run_scenarios function that loads all scenario card files, validates them as a read-only check without writing any rows, and collects failures for each card against the known gate registry.

Still checking expected exit codes...

I also want to verify the pass_control fixture runs clean through all seven gates, flagging it as a failure if anything fails or warns, then printing a final summary if any failures occurred overall.

Now I'm setting up the main entry point with argparse, defining the "check" command and options for specifying a script path or validating a scenario directory read-only.

Still writing gate logic...

Finishing the file writing logic, then verifying my hand count of the return statements and exit call against the pasted code block — both counts line up, confirming the control flow checks out.

So code wins on specificity there. I also notice that an empty scenarios directory and a missing directory both produce empty glob results, hitting the same exit-1 path, but an individual unreadable card JSON doesn't trigger exit 1 — it just gets counted as a failure, leading to exit 2 instead. That's a meaningful gap: D2's table correctly lists "unreadable script, empty card dir" under exit 1, but someone generalizing that "could-not-evaluate always means exit 1" would be wrong for an unreadable individual card.

Beyond that, I'm realizing there are several uncaught-exception paths that also terminate with exit 1 via the Python interpreter itself rather than explicit exit calls — a non-UTF-8 script file raises UnicodeDecodeError, which isn't caught by the existing OSError handler, so it crashes out; similarly a registry write failure after the verdict is already printed would still crash with exit 1. These interpreter-level exits are stdlib behavior I haven't fully verified but are worth flagging as a distinct category from the intentional exit codes.

So the real contract for callers should be: treat anything that isn't exit 0 or exit 2 as "could not evaluate" and block, since exit 1 can come from multiple sources including crashes, not just the two explicit sites. I also want to check whether `--script` and `--no-register` flags get silently ignored when `--scenarios` is passed, since that precedence matters for interpreting behavior.

Now I'm realizing exit code 2 is genuinely ambiguous — argparse itself exits with code 2 on invalid or missing arguments, which collides directly with the refutable-violation exit code. The way to disambiguate is checking stdout for a "workflow_gate FAIL" header: if it's absent, exit 2 means a usage error from argparse rather than an actual violation, and that distinction needs to be explicit in the caller contract.

I'm also noting some minor edge cases: `--help`/`-h` exits 0 with no evaluation at all, argparse's default prefix-matching could allow abbreviated flags like `--scen`, and an empty string passed to `--scenarios` is falsy so it silently falls back to the script path. Additionally, `SCENARIO_DIR_DEFAULT` is defined but never actually used as a default, so the spec shouldn't claim there's a default scenarios directory.

The digest computation reads the file in text mode with UTF-8 encoding, which means Python's universal newline translation normalizes CRLF to LF before hashing -- so the digest isn't simply sha256 of the raw file bytes, and a CRLF checkout would hash identically to an LF one, differing from what `git hash-object` would produce. This behavior is unverified in the corpus, and I should also flag that UTF-8 decoding doesn't strip a BOM if present.

The timestamp is UTC at second resolution in ISO format, captured after checks complete, and the row also records the name (from args or script basename), the verbatim script path argument (explaining path drift between rows 41-45), the pass/fail verdict, and the detailed checks list including soft-check reasons -- all serialized as one JSON line per append, with directories created as needed.

I also notice the registry's "desc" field for G6 has drifted over time (earlier rows say "durable receipt landing in watch/inbox" while later ones add "with a dated stamp"), since desc is copied from CHECKS at run time rather than fixed -- meaning verifiers can't compare desc text across rows. I need to pin down exactly which row introduced the change, checking timestamps around row 9-10.

Now I'm going through the registry rows one by one, tracking which test runs (tree-doctrine-dig, mickey17-v2, the-gala, etc.) produced FAIL vs PASS verdicts and their timestamps, to map out the soft-row pattern.

Continuing through the run log, tree-doctrine-dig passes soft checks across several timestamps, then game-mechanics fails once before passing with G3/G6 soft, followed by a string of passes for ractor-panel and ractor v2 tests, and multiple frontier runs logged through the early morning into evening.

Cross-checking against D2's FAIL rows (1,3,5,10,12,16,18,20,26,36,39 — eleven total), my count matches, and row 18's scenario-g1-fixture aligns too. Row 27 has both G3 and G6 soft, matching D2's note about the missing exit-0 stamp, and I notice rows 26 and 27 share the same digest (f72e86015), which seems significant.

Actually this reveals something important: same script digest but different verdicts means the gate logic itself must have changed between 22:18:50 and 22:19:57 — row 26 has G3 failing hard while row 27 treats it as soft. The registry doesn't pin which gate version produced a verdict, so a result is really a function of both the script digest and whatever gate code was active at that moment. I see the same pattern with digest d2a6783b55be across rows 13, 19, and 22-25: the first two pass cleanly, but starting at row 22 G3 goes soft, suggesting the gate was updated (likely with B2-206) in between. The key finding is that digest pins the script but not the gate version used to evaluate it.

I also notice the seatlaw temp files around row 36-39 relate to the --no-register flag added later, and the help text names seat_law_gate as a hook caller for in-flight content checks, but it doesn't quote that caller's actual exit-1 branch — similarly, the freshness_gate comment references a different caller entirely. So no caller's exit-1 logic is directly evidenced anywhere, meaning that residue gap remains unresolved.

Now I'm checking the stdout format for the gate output: a header line with pass/fail status, digest, and script path, followed by indented rows marking WARN/ok/FAIL status with ids and descriptions, plus an optional reason for warnings and a trailer line when a registered check fails.

I'm also tracing scenario mode line numbers and an important nuance about G6: soft WARN only applies if the base check already passed and some date is missing, but a completely missing receipt is always a hard FAIL, not soft.

Same logic holds for G3 — missing steering entirely is a hard fail, not soft, confirming this with the row examples. On exit codes, -h always exits 0 via argparse, and in full scenario runs, if all cards pass and the control is either clean or simply absent from the test fixture, the run still exits 0 — the control being absent gets silently skipped rather than treated as a failure. That's worth flagging since the docstring claims the all-pass control must pass clean, but the actual code just skips it if missing, so the code's behavior should be documented as the real finding. I'm also noting that in scenario mode, the control is marked as failing if any card gets a soft WARN.

Looking closer, I see that a card declaring expected exit_code 1 can never actually match, since the only exit codes run_scenarios can produce are 0 or 2 — so cards with exit_code 1 are structurally guaranteed to fail validation. That's another real bug worth capturing: validate_card allows a value the runner can never produce.

Now I'm mapping out the full exit-code matrix across code paths — argparse errors, help flag, empty scenarios, red/green scenario outcomes — tracking which exit code and row count each path produces.

I continue through the remaining paths: read errors, decode errors, the --no-register flag variants, and the main tail success/failure cases, noting exit codes and whether a row gets appended, including the uncaught OSError case during registry append where the row count is ambiguous.

I also check the scenario-crash scenario—where the card JSON is a list instead of a dict, where the scenario input might be a directory instead of a file, and where a decode error could occur during reading—to see which paths produce errors versus falling through to normal validation. I note the important caveat that stdout can print "PASS" while the exit code is still 1, so callers must rely on exit code rather than printed output.

Thinking about exit code semantics, I'm flagging that exit 2 is overloaded—covering both usage errors and refutable violations—while exit 1 covers both crashes and could-not-evaluate cases, and exit 0 covers both successful no-violation runs and help/no-op invocations like `-h`. This contradicts an earlier claim that exit 2 is the "only hard block" signal, since the contract leaves disambiguation to stdout header presence rather than exit code alone, even though the "exit 2 only for hard blocks" invariant might still technically hold for usage errors.

For exit 1, the caller must treat it as a hard stop: don't submit, don't treat it as a warning, fix the underlying environment issue (path, encoding, card directory) and re-run — since no row exists, there's no ledger fact to act on either way.


