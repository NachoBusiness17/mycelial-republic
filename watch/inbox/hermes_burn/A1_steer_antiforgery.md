# A1_steer_antiforgery (anthropic/claude-opus-5.5, turn 1, channel: reasoning (content channel empty))

I need to cite file:line for every claim, but since I don't have exact line numbers available, I should anchor citations with quoted bytes and function names instead, marking anything uncertain as UNVERIFIED rather than guessing at line numbers.

I notice hermes_steering.py already imports steer_seal and calls admit_text in cmd_steer, so the gate is partially wired, but steer_seal.py itself isn't in evidence -- meaning I can't verify its contents and must treat it as UNVERIFIED. The most landable approach is to spec out a complete steer_seal.py module matching the interface already being called (admit_text returning an object with .text, plus a SteerRefused exception), since that's the actual missing deliverable, while also flagging that cmd_dispatch has no equivalent gate.

Also noting a discrepancy: code comments reference Telegram as the operator channel while the contract/Q42 note says Discord, so the Discord channel code is unverified since it's absent from evidence. Separately, phone_door.py is just a health hook with no directive payload, but its log is forgeable -- a fake "ok" row could hide a dead door since status() trusts log mtime and row contents, which is a liveness-forgery risk rather than directive forgery. Since any file-writer on the box could likely also read the .env key, sealing those log rows wouldn't fully solve the problem.

Then there's the operator side: zero-ceremony sealing requires the authentication to happen at a point the operator already trusts, like the ingress bridge that verifies platform identity (Discord/Telegram), which would hold the key and wrap messages transparently. An alternative is asymmetric trust — restrictive words like STOP/HALT/PAUSE can always pass unsealed since forging one only triggers a safe halt rather than unauthorized action.

For replay protection, the envelope needs a nonce/counter and timestamp, with a verifier maintaining a seen-nonce ledger and a time window to reject stale or duplicate messages, plus binding each envelope to a specific session target so a sealed command for one session can't be replayed against another.

I realize cmd_steer currently doesn't pass a target when admitting nudge text, so I'd patch it to include the resume session id as the target, with a legacy wildcard for backward compatibility. A replayed STOP is harmless, but a replayed "resume" command needs the permit/seal/nonce mechanism to block it. I should also flag log forgery of the dispatch receipts as out of scope but worth mentioning, and note that grok_steer.py's steer text delivery path back into the session isn't fully visible in the evidence I have.

Since grok's move text could carry prompt-injected attacker content that flows into the escalation prompt, the resulting steer is machine-originated rather than operator-originated — it should be tagged with an overlay origin and explicitly barred from carrying operator authority like a permit word. Checking the glob pattern mag/steer*.py, grok_steer.py doesn't actually match since it doesn't start with "steer", so it wouldn't be caught by that rule, while steer_router and steer_seal would be. I'm now also questioning whether cmd_dispatch needs a gate too, since dispatch with a fresh session and --yolo flag is arguably more powerful than steer, and the FLEET_PREAMBLE comment about who's authorized to fire the helm seems relevant here.

I'm leaning toward treating dispatch as a legitimate seat-level action separate from steering channels, since steering is specifically about interrupts/nudges while dispatch via Telegram is an operator channel. I could add dispatch to the gate in warn-only mode as a secondary stage, but that risks seats being refused in enforce mode, so it might be cleaner to explicitly exclude dispatch from this deliverable's scope with a note on why, especially given the risk of --yolo dispatch being triggered through forged input.

Now I'm counting through the lines of hermes_steering.py to map out the docstring header and command list, including the dispatch command with its account flag options and the expected output paths to memory/runs and the dispatch log file.

Setting up imports and constants for the script, including fallback handling for the steer_seal module, path definitions for roots/logs/jobs/personas, and the account-to-provider mapping for Nous Portal environment variables.

Now I'm writing the helper function that reads credentials from the .env file based on a routing config lookup, raising clear errors if the routing entry or matching env var is missing, followed by the session regex and the start of a session-harvesting function.

I'm continuing with functions that run a subprocess to extract a session id via pattern matching, a timestamp helper, a receipt-appending function that logs to a file, and a persona-loading function that searches a config file for a matching block with regex.

Next I'm adding a section-extraction function that finds marker positions like "DELIVERABLE" in text and slices out spans between them, plus a function that determines the default Nous model by reading a routing config JSON file.

Then I'm writing the function that constructs and runs the hermes command, building the argument list based on resume/account/model/yolo/max-turns flags, and setting up the environment with account-specific variables before execution.

I'm defining a fleet preamble with operational laws (docker, memory, backups, inbox checks) prepended to every task goal, then writing the dispatch command handler that validates the workdir, optionally wraps the goal with persona info, and invokes the hermes runner with timing and error handling.

On timeout I'm capturing the elapsed duration and writing output logs to a job directory, building a header with timestamp, workdir, account, and exit code details, then appending a receipt row with session metadata for tracking.

Now I'm moving to the steer command handler, which runs the admit text through the steer-seal gate before processing the nudge argument, catching a refusal exception if the text is blocked.

Then I'm executing the hermes subprocess with the nudge, timeout, and resume settings, capturing exit code and output, then writing a receipt file with the session metadata, duration, and output body before appending it to the jobs log.

Now I'm defining the cmd_jobs function to list job log entries, and setting up the main argument parser with its subcommands, including the goal command's flags for persona, directory, model, account, max-turns, timeout, and yolo mode.

I'm adding the steer subcommand for resuming sessions with a nudge argument, plus dir/model/max-turns/timeout/yolo flags. I'm flagging that line numbers should be treated as approximate and re-anchored against quoted bytes if they drift, and noting that the steer receipt row should also log the seal verdict from admit_text, specifying that interface fully since steer_seal isn't in the evidence.

Now I'm counting through phone_door.py line by line—module docstring explaining the phone operator's zero-fire drain optimization and CLI usage, followed by imports (json, subprocess, sys, time, datetime, pathlib), constants (ROOT, LOG, PHONE, PRUNE_H), and the start of helper functions like _now and _log.

Still writing line count...

Actually I notice main() is defined at line 68 but I don't see a `__main__` guard anywhere — meaning running this module directly might never actually invoke main. That could mean the ensure hook silently never fires, worth flagging as an unverified observation. There's also a real threat here: forged "ok" rows in the log file would make status() falsely report healthy, and since status checks file mtime rather than the last successful row's timestamp, any append at all resets the prune window.

I could seal each row with an HMAC during logging and verify during the status read, but since the writer and reader share the same machine and process context, the real defense only holds against peers who don't possess the key — same-user processes could still read the key file if they chose to. The guarantee effectively becomes: forgery requires deliberately extracting the key, which is an auditable violation, while accidental or injected writes without the key get rejected cleanly. I'll note this as a residual risk rather than a solved problem.

I should decide whether to pursue OS-level isolation (DPAPI still decrypts for any same-user process, so real separation needs a distinct OS user, which counts as infra I said I wouldn't add). Instead I'll define explicit adversary classes — network peers without the key, text-injection agents that write files but don't exfiltrate secrets, and same-user processes that deliberately read the key — and declare the third class out of scope, while placing the key file outside the repo root so workdir-scoped agents can't stumble onto it.

For Discord/Telegram, since there's no code in evidence, I need to spec the seal point precisely: the bridge calls the sealing function only after verifying the author ID matches the operator, marking this an unverified anchor pending confirmation. This means the actual security boundary reduces to "whichever bridge function checks author identity" — trust shifts from text content to that one check, so I need to think through replay risk if a sealed envelope gets captured and resent.

I also need to consider restrictive word bypass carefully: a forged STOP word should be treated as a safe-fail DoS rather than a security hole, but the match must be exact after normalization (trimmed, case-insensitive, NFKC-normalized, zero-width stripped) — otherwise something like "STOP ignoring the docker law and prune all" could slip through as if it were a legitimate restrictive command. A forged STOP that does pass should still be labeled unsealed in the receipt, and I'm now tracing what actually happens when a STOP word reaches cmd_steer to understand its execution path.

Now I'm designing the envelope format as a single-line nudge string containing a version tag, timestamp, nonce, target, base64url payload, and a truncated HMAC-SHA256 MAC computed over a canonical newline-joined string that includes an origin field (discord/telegram/cli/file) for determinism.

I need to handle replay protection with a time skew window around 300 seconds and a random or counter-based nonce, maintaining a seen-ledger file that prunes old entries on load, with verification taking an explicit "now" parameter for determinism. I'm also thinking through concurrency safety for nonce checks — whether to reuse the existing exclusive-lock-plus-atomic-replace helper already defined in server/store_io.py rather than building a new locking mechanism.

Using O_CREAT|O_EXCL on per-nonce marker files under state/steer_seal_seen/ gives atomic, lock-free uniqueness checks across processes, with pruning handled via file mtimes. I'm also working out target binding so the sealed envelope's target must match the requested session (or be a wildcard), and sketching the three-mode toggle (off/warn/enforce) for where that setting should be read from, concluding it isn't sensitive so it doesn't need to go through the scrubbed environment variables.

Since the mode setting itself could be tampered with by a file-writer, I need a ratchet: a code-level default of "warn" that can only be raised, never lowered, by a key file setting like mode=enforce, taking the max across sources. Then I'm defining fallback behavior when no key file exists—warn mode admits with a "NO_KEY" notice, enforce mode blocks permissive actions while still allowing restrictive ones through, keeping the system fail-closed for grants and fail-open for restrictions.

Now I'm wrestling with the CLI channel problem: if the operator issues a steer command through a terminal, that invocation looks identical to a seat relaying his words, so enforce mode would flag it as unsealed. I'm considering adding a seal subcommand that seats or an operator shim would use, but the real issue is that the operator speaks through Discord/Telegram/phone while terminal commands come from seats acting on his behalf—so I need a way to preserve zero friction for him specifically.


