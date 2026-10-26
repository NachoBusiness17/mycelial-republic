# garden-v1-B1 (anthropic/claude-fable-5.1 @ nous, turn 1, channel: reasoning (content channel empty))

I'm counting through the source file line by line, starting from the docstring, to pin down exact line numbers for the sections I need to reference.

Continuing with the retry policy, I'm noting that after one retry failures are terminal and batches continue regardless. The carrier-patch laws from the 2026-10-01 receipts show a costly day of re-fire theater, so I'm codifying that landed outputs block re-burning unless a revision explicitly rides turn2_only, and that a stale force flag previously burned the same ask dozens of times after it had already landed.

Past that, I'm adding that two provider refusals for a single ask now mint a permanent REFUSED marker the carrier skips forever, since refusal-retry loops burned certain asks dozens of times before this. I'm also writing an evidence preflight rule requiring every evidence path to exist on disk with its rendered bytes actually present in the outgoing message, failing closed if no evidence exists at all, since one case fired fourteen paid calls whose material never reached the model.

Next I'm documenting the endpoint fence pattern reused from the SSRF rulings: a fixed https URL on exactly one host, asserted per call, with the resolved IP checked to refuse private/loopback/link-local/reserved/multicast addresses so DNS or hosts-file tricks can't redirect the tool internally. The script closes out with exit codes and starts the actual module with imports.

Adding pricing data for more models...

Still writing parsing logic...

Still writing the request/retry logic...

Still writing helper function...

I'm now adding a function to append usage rows to a log file as JSON lines, and starting to define a system prompt builder that pulls in persona/law configuration from the claritas module.

Still writing the estate-law block...

Then I'm defining a `_refusal_state` helper that reads a usage log file to count prior refusals and capture the last snippet, returning both for later use.

Still writing refusal marker logic...

Still writing skip-detection logic...

Now I'm defining a helper that asserts evidence paths referenced in metadata actually appear in the rendered message body, guarding against an empty evidence block slipping past the duel stager by verifying each bank/draw_id/material_path entry exists and matches what's actually being sent.

Still writing the preflight check...

Still tracing refusal logic...

For turn 2, I check for a revision file and reset the conversation to only the original prompt plus the revision content, avoiding any stale context from turn 1. I also handle dry-run mode by just logging placeholders, and add a shortcut for skipping turn 1 entirely when "turn2_only" is set.

Then I move to the actual API call: I verify the evidence is embedded in the message body, invoke the model, and pull out usage stats to calculate cost based on prompt and completion token pricing. I extract the response content and set up a channel variable to track where the content came from, preparing to handle the case where content comes back empty.

If content is still missing, I fall back to checking the reasoning field, and if that's empty too, I check for a refusal message—logging it to the bank with details like the ask id, token counts, and cost if the model refused to respond.

Still writing error handling...

Still writing file handling logic...

After finishing the revision append logic and computing total cost, I'm now setting up the main entry point with argument parsing for the queue path and dry-run flag.

Writing the ask directory loop...

After the loop, it tallies total spend from the USAGE log file and prints a summary line before returning a failure code if any asks failed. Now I need to double check my line counts for the docstrings of `_landed_skip` and `_assert_evidence_in_body`, recounting them directly from source to be safe.

The docstring explains a real incident: A1_steer_antiforgery got re-fired 45 times (~$20.53) after its deliverable had already landed, because a stale force flag in its ask.json (never cleaned up, from early morning) kept bypassing the skip logic on every 45-second driver cycle. The flag-hygiene fix only prevented this for new entries going forward, so since every retry funnels through run_ask, this entry check becomes the single choke point for both cycle-boundary retries and other triggers like empty content or provider refusals.

Now I'm also noting a related gap: only a pending revision tied to turn2_only can reopen an already-landed ask (the normal revision case), and the old gate at entry also let through revision flags lacking turn2_only — which is the same kind of hole. Then I'm moving to another docstring for a validation check that fails closed before any API call if evidence material is missing — flagging an incident where 14 paid calls went out despite the actual evidence bytes never reaching the model (every response complained the evidence block was empty), and four separate asks were sent with an empty evidence list because the staging process pulled from the wrong draw in the ask bank.

I note the fix requires every evidence path to exist on disk and its rendered content to actually appear in the message body, otherwise the ask fails closed just like an evidence-less fire would. Last I look at a helper that reads refusal-ledger state for an ask id, documenting that refusals should be treated as data rather than something to blindly retry — referencing an earlier incident where the driver kept retrying refused asks dozens of times over two hours instead of recognizing the refusal.

Now I'm moving into ranking the actual defects by damage, starting with a turn-2 revision loop issue: the "landed" skip logic returns None under certain revision-pending conditions, but the turn-2 append path doesn't seem to consult that state before writing out.

Second issue I'm flagging: the transport retry logic retries on any HTTPError, including 4xx codes like insufficient credits, bad request, and unauthorized, not just the 5xx cases where a retry would actually make sense.

Another unpatched spot: the empty-response case at lines 334-335 pays tokens but never banks a row, so there's no terminal marker and the cycle refires unbounded, same disease as the refusal loop but without the fix applied there. The right patch is to bank an "empty": True row into terminal state alongside refusals. Now I'm weighing whether this is worse than the revision re-fire case.

Looking at the public-endpoint check, I notice a TOCTOU gap: it resolves DNS once to validate, then urlopen resolves again separately, so DNS rebinding could slip past the guard and reach internal hosts — the docstring's safety claim only really covers hosts-file tampering, not this. I also spot `_hermes_key` reading `.env` fresh each loop, where a missing file raises a generic FileNotFoundError instead of the cleaner SystemExit path, though that's a minor issue by comparison.

In `main`'s cost reporting, the OK/FAIL print always evaluates truthy since `row.get('ok')` defaults oddly, so skipped asks get counted as passing — another minor cosmetic bug. The ledger-summing step also calls `.get("cost_usd", 0)` on JSON lines that might not even be dicts (like a stray list), which would throw an uncaught AttributeError.

More concerning is that `meta["id"]` gets used directly to build the output path, so an id containing `..` or path separators could escape `OUT_DIR` entirely — a real path traversal risk if asks are staged by less-trusted tooling rather than purely operator-authored. I'm now looking at the preflight probe logic, which truncates text to the first 400 characters for inspection.

I'm also noting that refusal costs get banked but empty responses don't, and transport errors after billing silently go unbanked. On the retry side, `_call` retries HTTP 4xx errors like 400 (invalid request) and 402 (insufficient credits), both of which are pointless since retrying won't fix them — it just wastes 20 seconds. The more serious issue is unbanked burn when a transport failure happens after the provider has already started processing, which I want to fold into the billing analysis.

Now moving to the first real finding: the revision/turn2_only logic re-fires turn 2 every cycle after it's landed, because nothing ever consumes revision.md. This means the "landed beats force" gate keeps reopening the ask indefinitely, and each cycle appends a paid REVISION block for no reason. The evidence is at tools/hermes_burn.py:211-214 for the reopening and 349-351 for the appending without consumption — I'll cite both locations together in one line.

Next I'm looking at the empty-response path around lines 320-335: a paid call returns usage but nothing gets banked and no terminal state is reached, so the ask fires unbounded every cycle just like the refusal loop but without any fix, undercounting the ledger. The fix would be to bank a row marking it empty with its cost, and extend the refusal-state check to count empty rows toward the terminal marker threshold.

Then I need to pick between the DNS TOCTOU issue and the unbanked transport failure with its 900-second timeout — the timeout path seems more damaging since a hung provider can stall a single ask for up to 30 minutes with retries and sleep delays, and if the provider already billed for that first attempt...

Actually I should be careful here — the code fact I can verify is that there's no bank call in the failure path of the call function, but whether the provider actually billed is speculation I can't ground. I should phrase it more precisely: a request that times out or returns a 5xx after the provider has already consumed it banks no row, and the retry just re-sends the same body with neither attempt ever recorded. As for the DNS TOCTOU angle, that's grounded in the code — there's a getaddrinfo call and then a separate resolution inside urlopen — but the docstring's claim that DNS re-pointing can't reach internal surfaces looks false based on that.

The actual fix would be to resolve once and open the TLS socket directly to the vetted IP, setting server_hostname so certificate validation still works against the original hostname — more involved than a one-liner but closes the gap cleanly.


