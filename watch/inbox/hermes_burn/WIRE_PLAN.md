# WIRE_PLAN (anthropic/claude-opus-5.5, turn 1, channel: reasoning (content channel empty))

I need to cite file:line for this, but I don't have exact line numbers handed to me, so I'll count carefully and mark approximate line numbers where needed, quoting exact bytes for accuracy.

Looking at the six files in evidence—chan.py, game_mud.py, tavern.py, dungeon.py, hermes_burn.py, kabuki_cast.json—I notice workflow_gate.py, the gap register, and the ractor red-team aren't actually included, so I'll need to mark those UNVERIFIED and instead look for a genuine defect visible in what I do have, like a potential thread-filtering mismatch in chan.py's `thread()` function.

Going deeper, I spot a real gap: game_mud's `claim()` calls `survey()` fresh rather than consulting a prior survey despite its docstring implying one exists, meaning the party could get re-surveyed with different results. There's also a convergence artifact in `_statements` where any sentence over 12 characters counts as a statement, so witnesses echoing the room's prose back would falsely appear to "converge" on a shared core. In tavern.py, `bar_round` checks budget before each persona call but `judge_round` doesn't enforce the same check, so the judge call could exceed budget unchecked.

Looking at dungeon.py, `ROSTER[actor]["bolts"] -= 1` mutates a module-level global that persists across Dungeon instances within the same process, which is a minor but real statefulness bug. The budget check correctly raises before spending occurs, and file-not-found errors in `_check_links_405` are properly caught as OSError. I'm now examining the `_verdict` AUDIT logic checking whether a scroll's name appears in the object.

The substring matching has an edge case where "ledger page" could match other scroll iterations, but since Ledger Page is first in the list it's effectively harmless. The `_tail` function assumes all rows have an actor field, which holds true in this case, and `hermes_burn` opens the .env file redundantly per name but that's just inefficient, not buggy.

Looking at `chan`'s `_wake_run`, cost is uncontrolled through docker openclaw, and `wake` spawns a daemon thread without any deduplication, so overlapping wake calls could stack up. I also notice kabuki_cast assigns all actors to a free model under account "sdd" that isn't listed in hermes_burn's PRICING table — since `_fire_ask` raises a ValueError for unrecognized models and `tavern._paid` does a raw dictionary lookup that would throw a KeyError, kabuki's faces can't actually use hermes_burn's billing rails without hitting an error. That's a real wiring gap, and on top of that the hermes_burn endpoint is locked to a specific host that may not even serve these free models.

There's also the tier_note mapping a persona to a SKU with a ":batch" suffix that also isn't in PRICING, so that mapping is broken too. Separately, I'm checking consistency around em-dash usage — some docstrings use them, and game_mud prose contains them as well, so I need to be careful not to reproduce em-dashes verbatim if I quote that text, since my own output should avoid them.

Looking at the chan catalog logic, party seats (kabuki stage names) aren't in PLAYER_SEATS, so a partychat thread wouldn't appear in the catalog unless the OP seat is "operator" or "primer" — that's a useful finding for how thread visibility works.

Also noting seat names get sanitized and lowercased, posts cap at 8000 chars, and glue code could use chan's private append method to directly write thread_open events rather than going through post(). For mapping chan threads onto game_mud rooms, since ROOMS is a fixed dict, I'm considering whether new rooms could be registered at runtime by inserting into that dict directly.

Functions like go and survey all look up rooms by key in ROOMS, so glue could inject a new room entry at runtime, but exits need to point to existing rooms and ROOMS isn't persisted, meaning glue has to rebuild it from room.jsonl on import. The claim verb is complicated since survey() calls into game_dm which isn't verified, and claim() doesn't pass seats the way survey does, so for the party chat glue probably needs to bypass claim and build its own deterministic overlap check directly over the thread's posts instead.

I also need to flag that game_mud's state persistence relies on functions not in evidence, and that the save function swallows exceptions silently, which risks claims vanishing without any error. Beyond that, workflow_gate.py and the ractor red-team references are both unverified and need their own adapter work and documentation lookup before the spec can treat them as solid.

So for chat posts I'll use the tavern _call + _bank + PRICING pattern with the endpoint fence, while rival builds go through run_ask with full evidence preflight, landed-skip, refusal terminal, and atomic claim. I'm now untangling the system-prompt assembly: kabuki persona needs to merge with the hermes_burn LAWS block, but face_for isn't in evidence so I'll treat that as unverified and lean on calling hermes_burn._system_for(model) directly and prepending the persona rather than guessing at an unverified face system.

Since I can't import the laws text as a standalone variable, I'll extract it by splitting _system_for's output at the "ESTATE LAWS" marker and taking everything after, with a fallback if the marker's missing — a bit hacky but avoids duplicating content. For the gap register, since it's not in evidence I need to name a concrete falsifier row rather than leave it unverified, and I'm leaning toward flagging the kabuki/PRICING mismatch as the candidate gap, though that's really what this glue work is meant to resolve, so I should look for a better first candidate.

I'm considering tavern.judge_round, which seems to bypass the budget cap since bar_round checks spend against budget but judge_round calls the paid path unconditionally — a concrete, testable law breach, though I need to verify dry mode and monkeypatched spend tracking actually gate it properly. Another candidate is the dungeon ROSTER bolts bug, where global mutation means a second Dungeon instance in the same process inherits depleted bolts from the first — an easy reproducible defect worth flagging too.

Mapping out the six threads for cost surfacing: chan is free, game_mud is deterministic and free if we skip survey, tavern handles posting turns, dungeon's dice roll gives free deterministic turn order, hermes_burn covers rival builds, and kabuki's face config is free. For the party scenario with six actors across three rounds (eighteen posts total), I'm sketching a tier mapping assigning haiku as the cheap default model for most actors.

I'm keeping everyone on haiku for regular posts since fable-5.1 is pricey and only reserved for ARAGOTO at commission tier 2+. Estimating costs per post with roughly 9k input tokens and 400 output tokens, haiku runs about $0.011 each, totaling roughly $0.20 for all eighteen posts, and I'm now working out the rival build costs on sonnet using the tavern.py file as evidence.

Estimating the sonnet revision call at roughly $0.086 each (worst case doubling to $0.20 per call with revisions), two calls totaling $0.40, plus an opus red-team pass at about $0.14, giving an expected $0.74 per thread with a hard cap of $1.50 -- and the workflow_gate cost remains unverified pending whether it invokes models at all.

If the operator's hourly cadence means one thread per hour, that's 24 threads a day, roughly $17.76 expected with a $36 cap, which would burn through the noted ~70+ hermes credits in just 2-4 days. All of this rests on pricing assumptions captured from an October probe rather than actual measured tokens, so I should flag that the real falsifier is summing usage.jsonl by thread id prefix rather than trusting these estimates. The tavern's 500 max_tokens cap for posts seems fine as-is. Now I want to tally up line numbers for the key items.

I'm counting through chan.py line by line — it starts with a module docstring describing the engine as casual, owning posts and the CLI interface, then moves into imports (hashlib, json, re, threading, uuid, datetime, pathlib, typing), followed by schema and root/room constants, and then into the Grok TUI section defining hidden event types like post_tool_use, pre, user, stop, and start.

Continuing down, I'm tracking the player seats and primer threads constants, then the KEEP_OP prompt block which frames the scenario as "being the Primer" with instructions and example quote-reply actions like glass, fireball, and do-not, followed by the start of the CHAN_SYSTEM prompt describing the Anonymous persona rules for /keep/ — reading the thread, quoting properly, no lecturing, and references to thought crime and transgression.

Then I'm reviewing the helper functions: room_path for building paths, _now for timestamps, slugify for cleaning strings into slugs, paint_tool for some formatted output, trip_id for generating identifiers, and is_play_post which validates whether a record is a legitimate play post by checking its type, event, thread, and text content. Finally I see the start of a _load function.

Now I'm continuing _load — reading lines from a file, parsing each as a record, and filtering only valid play posts into a list — followed by _append which writes a new record to disk, _number which adds sequential numbering to records, and _is_player_thread which checks if a thread involves player seats.

I'm then defining seed_keep, which checks if a thread already has posts and if not appends a "thread_open" keep-alive record, returning whether it created one. After that I'm starting catalog(), which seeds keep-alive posts, groups records by slug, and builds a list of threads with numbered posts, last bump times, and reply counts.

Still defining functions...

Still writing fallback logic...

Now I'm scanning through game_mud.py line by line, tracing the docstring that explains the MUD's design philosophy—how the tabletop mechanic works with shared scenes, agreed vs. unique statements, and the world map structure covering rooms like World-Memory, Gear, and the Observatory.

Below the docstring I'm tracking the main game loop commands (look, go, survey, claim, inv, map) and the reuse logic for routing novel content through the game world, then moving into the imports and setup—config loading with a fallback, stdout reconfiguration wrapped in a try/except, and the schema constant defining the save version and player/claimed state fields.

Now I'm building out the ROOMS dictionary, defining each room's World-Memory with its role, a multi-line question prompt, and a prose description block containing atmospheric text like roots and a faint hum rising from below.

Given how long this line-by-line enumeration is getting, I decide to adopt a consistent citation method instead: count lines precisely where I can, mark approximate counts with a tilde, and treat quoted bytes as the real anchor so citations can resolve even without exact line numbers.

Still counting lines...

Setting up the run directory structure...

If budget is exceeded, I log a budget cap verdict and bail out. Otherwise I'm building the persona's act-duty instructions based on temper versus effective threshold, assembling system and user prompts with secrets, tells, room context, and transcript, then calling the model to generate the persona's tavern line.

Now I'm defining judge_round, which builds a judge prompt from the transcript and round number, requests a JSON score response, and parses the result.

This actually looks like a real defect: the docstring promises id format TAVERN_<run>_r<round>_<actor>, but the code drops the run identifier, generating TAVERN_r{rnd}_{p['name']} instead. Since every tavern run reuses identical ids, hermes_burn._bank's doubled_key_check will flag (id, turn=1) collisions across different runs as if they were re-fires, which is a strong candidate for a genuine first bug.

Now I'm weighing whether to lead with this id collision or the judge budget bypass as my primary falsifier candidate — both live in the tavern code, but the id collision is a clean docstring-vs-code divergence with a deterministic test: monkeypatch the call, run two separate Run instances, and assert the banked ids come out distinct. I'll lean toward the budget bypass as the main row since it involves money, and treat the id collision as a glue-law fix, while still considering rival guard placements inside the paid-check logic.

Scanning through dungeon.py's opening section — docstring describing the gladiatorial arena laws (dice law, golden vectors, quirks, hard caps, call banking), then into the imports.

Still writing the game setup...

I'm now scanning the docstring for hermes_burn, noting its contract rules around per-ask evidence, output locations, usage logging format, and the carrier-patch laws like "landed beats force" and "refused is terminal."

Continuing down, I see the actual code starting: imports for argparse, ipaddress, json, socket, sys, time, and urllib modules, plus datetime and pathlib, followed by root path setup and internal imports from mag.inference_budget and tools.

Writing instance guard logic...

Finishing the API call logic with retry handling and a timeout sleep before raising an error, then writing the evidence-reading function that loads file contents with a size cap and tracks missing files.

Now I'm defining a function to log usage rows to a ledger file, deduplicating keys before appending. Then I start building the system prompt for a model, importing a "face_for" helper and assembling deterministic estate-law text to append to it.

I'm now scanning further down for the ask-running logic and pricing checks, then moving to inspect the kabuki_cast.json structure—its schema, fallback model, default account, and actor list starting with an entry named ARAGOTO.

Continuing to count through the actors array, I see entries for WAKA, ONSEI, and TACHIYAKU, each with their own model, account, max_words, persona, and tier_note fields defining their behavior.

Now I'm scanning game_mud for key functions like claim, survey, and act, trying to estimate line numbers for rooms, directions, and the world setup so I can figure out roughly where each major section falls in the file.

Moving on to designing tools/partychat.py, I'm sketching the constants it needs: a schema version tag, paths to the cast config and run inbox folder, and a mapping from free-tier models to their priced SKU equivalents, with Haiku as the default and a special case for higher-tier ARAGOTO models, plus separate SKUs for the builder and red-team roles.

I'm setting word SKU isn't in the pricing table), and opening a new thread from a gap record with required fields like id, title, file, and falsifier.

For opening the thread, I'm slugifying the gap id into a channel name and appending a thread_open row tagged with the operator seat so it registers as a player thread in the catalog, including gap_id, partychat flag, and room metadata -- making sure the operation is idempotent if the thread slug already exists.

-to-token caps and a per-thread budget, then outlining the core functions: loading the cast roster and resolving each actor's priced SKU (failing closed if a
