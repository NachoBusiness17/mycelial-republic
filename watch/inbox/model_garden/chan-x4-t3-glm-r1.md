# chan-x4-t3-glm-r1 (glm-5.3-flash @ zai, turn 1, channel: content)

> my B1 stands, but the board is half right and I paid for the lock with the wrong currency

> CONCEDE: on ONE queue dir the race needs a written law already broken. WAVE24_BOARD.md HONEST GAPS: "N driver instances on DISJOINT queue dirs ... not one driver widened." And msvcrt.locking after a hard kill leaves the lock held; the paid lane hangs with no operator-visible cause. Lockfile is worse than the disease on the sanctioned shape.

> BUT the disjoint-dirs law does NOT disjoint memory/runs/hermes_burn/usage.jsonl. _bank appends it per row (tools/hermes_burn.py, _bank, append mode, one write per row, no lock); _refusal_state re-parses the whole ledger every entry (tools/hermes_burn.py:167-183) and skips JSONDecodeError lines silently; main sums cost the same way, torn rows are zero cost (tools/hermes_burn.py:348-354).

> VERDICT on the shared surface: milder poison, not double-burn. Two drivers on disjoint queues CAN interleave appends on the one ledger. On Windows/POSIX a single fh.write under O_APPEND of a small line is not guaranteed atomic cross-process; a torn row zeroes cost in the totals (348-354) and, worse, a torn refusal row undercounts refusals in 167-183, which delays the REFUSED marker mint and buys one extra paid refusal fire. That is real money but bounded: per ask, at most the retry chain, not the A1 x45 shape, because the landed gate (_landed_skip, entry checks at tools/hermes_burn.py:266-284) still reads the output FILE, which is disjoint by the out-prefix law.

> BETTER CURE, landable, lock-free: per-ask claim file, tools/hermes_burn.py run_ask entry, before the 266-284 checks: os.open(out_path + ".claim", O_CREAT | O_EXCL | O_WRONLY); failure to claim = skip. Stale-claim cure without msvcrt: claim bytes are {"pid": N, "ts": iso}; a claim older than 950s (the _call timeout is 900 plus one 20s retry) is stolen and rewritten. Same primitive used for the ledger: write each row to usage.jsonl via one os.write of a single <=4k bytes buffer under O_APPEND, and make _refusal_state count torn rows as refusals-conservative, not skip.

> NEGATIVE example: single driver, sequential, per WAVE24 - claim file changes nothing, adds one unlink per ask, no behavior risk.

FALSIFIER: launch two hermes_burn processes, disjoint queue dirs, shared ledger, hammer 200 asks with kill -9 mid-dispatch; any hung lane, any double-fire on one ask id, or any torn ledger row that shifts the 348-354 total by even $0.0001 sinks this design.
