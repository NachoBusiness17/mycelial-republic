# T1W1_stranger_shared_surface (anthropic/claude-opus-5.5, turn 1, channel: reasoning (content channel empty))

I need to cite file:line for this audit, but I don't have reliable line numbers for shared_surface.py. Since citations must resolve to quoted bytes or be marked UNVERIFIED, I should quote the actual bytes and flag any estimated line numbers as UNVERIFIED.

I'm going through the contract JSON line by line, counting the schema, canonical paths, purpose, the list of laws about treating inbox items as untrusted and requiring classification before reuse, the workflow steps, and the client_aliases section to establish precise line references.

Then I'm checking the authority block and comparing against the never_sole_destination list, before cross-referencing with INDEX.json to catch a discrepancy -- the contract's read_first path points to INDEX.json but I need to verify whether the actual file uses .md or .json.

A bigger issue stands out: there's no writer authentication on the events log. Since it's append-only JSONL, any seat with filesystem write access could forge any event under any writer string, and the existing nonce gaps already flood fold_warnings with noise, which would mask a forged entry -- this matches the seq 42 note flagging that writer ids need session-scoping since two concurrent sessions are sharing one id.

The log also isn't tamper-evident since there's no prev_hash chain, so fold accepts reorder, edit, or replay -- a gap the estate itself already flagged as open. Combined with last-register-wins semantics and writer-chosen seq numbers, an attacker could pick an absurdly large seq value to force their write to win every ordering comparison, since the sort law treats seqs as exact BigInts.

This means someone could overwrite a receipt file's bytes, then re-register it with their own sha and an inflated seq -- validate would pass because it only checks bytes against the recorded sha, never who recorded it or whether the prev-sha chain is consistent. That's indistinguishable from the drift-patrol-cron's routine "hash refresh" behavior, making a malicious overwrite look identical to ordinary file evolution, and it directly violates the "never silently overwrite" rule with no mechanism to catch the discontinuity.

Now I'm also noticing that classification is just free text chosen by the writer, with index entries showing inconsistent casing and categories like "RECEIPT," "FACT," "LAW," "DOCTRINE" scattered arbitrarily rather than enforced against the contract's defined classes.


