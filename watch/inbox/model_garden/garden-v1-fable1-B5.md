# garden-v1-B5 (anthropic/claude-fable-5.1 @ nous, turn 1, channel: reasoning (content channel empty))

I'm going through the source file line by line to map out its structure, noting the header comment, spec description, and the HMAC-SHA256 envelope details.

Still writing constants and setting up the restrictive word grammar...

Now I'm defining exception classes for verification failures and steering refusals, plus a NamedTuple for admitted results, and starting a function to locate the seal home directory using an environment variable.

I'm now adding helper functions for default paths (keyfile, seen directory, mode path) and a resolve_mode function that validates an explicit mode argument against allowed values or falls back to checking an environment variable.

Still tracing the logging function... it writes a row of data to the LOG file, creating parent directories as needed and catching any write failures to report to stderr. Then I'm looking at the key-handling functions, starting with `write_keyfile`, which resolves the path and ensures its parent directory exists before writing the key.

Continuing through this function: it validates the key length against `MIN_KEY_BITS`, raising an error if too short, then branches on the `force` flag -- either overwriting atomically via a temp file and `os.replace`, or refusing to overwrite an existing file by using `os.open` with exclusive creation and raising a `VerifyError` if the file already exists. After writing, it returns the computed key ID. Next I'm starting to trace `_checked_key`.

Still writing file loading logic...

Then I continue into the `canonical` function, which builds a canonical byte representation of an environment dict by iterating over expected fields, validating each is present, and handling special formatting for version/timestamp fields.

I also sketch out `compute_mac` and the start of a `seal` function that validates the payload is a string before proceeding to construct the sealed output with a key, optional nonce, and timestamp.

Filling in the rest of seal...

Now I'm adding a helper that rejects duplicate keys when parsing JSON objects, and starting a parse_envelope function that uses this hook to safely decode the JSON text.

Now I'm defining a classify function that normalizes text to NFC, uppercases it, replaces punctuation with spaces, and checks whether it matches restrictive words to return either "restrictive" or "permit". I'm also starting to define a FileNonceSt class next.

Still writing nonce check logic...

Writing verify function logic...

Still tracing verification logic...

Continuing the logic, I see that in enforce mode, an unsealed permit word gets refused with an error pointing the user to seal it first, while in warn mode it logs a warning and still admits the text as "unverified-warn". Then the code moves into defining a new `admit_text` function with its own parameters and docstring.

Now I'm thinking adversarially about defects: the nonce check happens after MAC and timestamp verification, so an attacker can't burn nonces without a valid MAC, which seems fine. I'm also considering warn mode behavior—whether a forged envelope that fails verification but carries a permit-like payload could slip through `_gate` since the fallback treats the raw JSON text as an unclassified string.

The bigger concern is that the default mode is warn, which means a missing sentinel lets unsealed permit words pass through unchecked—effectively a no-op gate for permits in production unless explicitly tightened. I'm also noting that the `MAG_STEER_SEAL_MODE` environment variable can override the sentinel, which is another avenue worth flagging.

This is a total bypass: anyone who can set env vars for the harness process can relocate the seal home and mint valid seals with their own key, completely subverting the trust boundary - this seems grounded in the actual code reading env variables directly. I should also check the freshness check, which uses a 300-second window comparing timestamps.

The nonce marker gets evicted after 600 seconds based on mtime, but since `now` is injectable through the admit_text function, if a caller freezes `now` while real time advances past the eviction point, a replay could slip through after the marker is gone - though this seems like a test-only edge case rather than a practical exploit. There's also the future-dating issue: since the freshness check uses absolute difference, a timestamp set 300 seconds in the future is still accepted, effectively extending the valid window to 600 real seconds from now, which widens the replay surface more than the nominal 300-second freshness window suggests.

So there's a real sub-second window where a future-dated envelope can slip past eviction and get replayed, since the grace period plus the skew tolerance add up to exactly the eviction age. Filesystem mtime truncation (like FAT's 2-second granularity) could widen that gap further, though NTFS wouldn't have that issue. I think this is worth flagging as a genuine edge case, grounded at lines 302 and 343, with a fix being to evict at 3x the window or reject timestamps too far in the future.

Separately, I'm noticing that in warn mode at line 378, `_gate` returns the raw envelope JSON as the steer text rather than unwrapping it — so a forged envelope with a bad MAC still gets its whole JSON blob treated as the operative steer words. Not a security hole exactly, but a functional oddity, since unwrapping an unverified payload would arguably be worse than leaving it as-is.

Checking the nonce handling: it's lowercased and matched against an 8-128 hex regex, which looks fine, though the marker directory scan via glob happens on every call, giving O(n) overhead — minor but worth flagging. The `verify()` function's blanket exception-to-False catch is fine since canonical parsing already validates fields like timestamp. And I confirm that in the restrictive path, a forged envelope carrying "STOP" is still honored — that's the documented interrupt-law tradeoff, meaning attackers can inject STOP in either mode, which is accepted behavior rather than a defect.

Now looking at `admit()`'s strict path: calling `parse_envelope(text)` raises `VerifyError` on a non-envelope file before it ever reaches `_gate`, so a plain-text "STOP" directive file gets rejected with an exception instead of being honored as restrictive — unlike `admit_text`, where "STOP" is honored directly. This seems to contradict the safe-fail interrupt law, since a plain STOP file through `admit(path)` never reaches the restrictive check in `_gate`. I'm weighing whether this is an intentional strict design choice per the docstring or an actual violation of the module's own safety law.

A possible fix: catch `VerifyError` from `parse_envelope` and fall back to `env=None`, letting `_gate` classify the raw text — "STOP" would then be honored as restrictive, "GO" would still require enforcement. That seems safer and more consistent with the stated law, but I'm second-guessing whether the strictness is deliberate and whether an adversarial reading of the docstring would treat this "fix" as itself a bypass.

Turning to the environment override variables MAG_STEER_SEAL_HOME and MAG_STEER_SEAL_MODE — these look like the worst issue so far. Then there's the audit log living inside ROOT where the agent itself can write, letting it tamper with its own record even though keys are stored outside ROOT; the message truncation and included exception reason are minor but still worth flagging. I'm now looking at how `load_keys` behaves on posix permission checks.

On POSIX, `write_keyfile` writes the temp file with default umask permissions (typically 0644), then replaces the keyfile — but `load_keys` immediately rejects anything not matching 0o077 restrictive permissions, meaning the write path produces a file its own loader would refuse. That's a real self-inconsistency, though since Windows is the actual production target, it ranks lower in priority.

Looking at other candidates: the injectable `now` parameter in `admit_text` seems too speculative to count as a real issue, and the nonce recording flow after MAC/timestamp verification appears sound since payload return always follows a clean check. A more interesting case is in `_gate` — what happens when verification fails due to nonce reuse on a genuine, already-seen "STOP" envelope.

In warn mode though, replay of a genuine permit-payload envelope just falls through to the permit path with a warning, which is expected behavior. I'm also checking `classify`'s punctuation normalization (punctuation becomes spaces, so "STOP!!!" still reads as restrictive), confirming `resolve_mode` only evaluates on the permit path per call, and noting that `_try_parse_envelope` returning None on a broken envelope causes it to fall through as unsealed text.

I keep going through smaller checks: canonical() uses consistent JSON serialization across seal and verify, key_id is just a public hash prefix so not sensitive, nonce eviction can't be abused for DoS since attackers can't forge valid MACs, and seal() properly errors on keyfiles with multiple keys. Now I'm ready to rank the findings, starting with the environment variable overrides for MAG_STEER_SEAL_HOME and MAG_STEER_SEAL_MODE that could let anyone controlling the environment escape the intended root boundary.

The process environment can relocate the key/seen state or downgrade enforce mode to warn, which I can trace to mag/steer_seal.py around lines 71-72 and 90-92. Given the citation format only allows a single line or range, I'll cite 71-72 as the primary evidence and fold the mode-related behavior into the claim description rather than adding a second citation.

Second issue: admit(path) throws VerifyError before the gate check on any non-JSON file, so a plain-text STOP directive gets blocked, which contradicts the interrupt law (lines 17-19/51), evidenced at line 399. The fix is to catch VerifyError around parse_envelope and set env=None so _gate can classify the raw text properly -- this matters especially on Windows where the posix keyfile issue doesn't apply, so I'm ranking this second.

Now I'm moving on to look at a third issue involving future-dated entries.

Envelope lifetime equals eviction age exactly: timestamps up to now+300 are accepted as valid, staying fresh until ts+300=now+600, but the marker gets evicted when mtime falls below time.time()-600. Because of int() truncation on now_v combined with float mtime comparisons, there's a sub-second replay window around real time now+600, and it's even wider on filesystems with coarse mtime granularity (evidence at line 343 vs 302) -- the fix is to reject timestamps with skew beyond roughly 30 seconds, or alternatively evict at 3x the freshness window. I'm also weighing this against a fourth candidate: the audit log sitting inside ROOT while the keyfile sits outside it, making the audit log agent-writable -- trying to judge which flaw is more damaging, since the replay window requires a genuine future-dated envelope to exploit.

The log being inside ROOT is a real integrity gap but it doesn't actually change any gate decisions, whereas the replay window is a genuine correctness bug in the anti-replay logic, so I'd rank it third overall. I'm also reconsidering the POSIX keyfile mode issue -- write_keyfile generates a keyfile that load_keys then rejects on POSIX systems, making the whole thing unusable until a chmod -- but since production runs on Windows, that's less relevant. I'll commit to the replay math as the answer, framing it precisely: int(time.time()) versus the float st_mtime, occurring in the one-second window [now+600, now+601), under NTFS mtime resolution on Windows. The arithmetic is deterministic, so this should hold, but I want to verify that eviction only fires inside check_and_record, which only runs after a passing MAC and freshness check.

Tracing through the actual exploit sequence: a replayed envelope at real time now+600 would pass the MAC check and freshness check (since 600-300=300, not greater than 300), then hit check_and_record where it checks if the marker exists. The marker was created at the original real time (mtime ≈ now + f), and eviction only happens if another verify call ran after the cutoff passed -- meaning another valid envelope arrived at a real time greater than now+f+600. But the replay attempt itself can't evict its own marker before claiming it, since the exclusive-create fails first while the marker still exists, and eviction only happens after that. So the actual requirement is a separate, prior valid envelope verified within the narrow window (now+f+600, now+601) to evict the marker first.

This window is quite narrow, and coarse mtime resolution on some filesystems (like FAT's 2-second granularity) would widen it slightly, though the nonce file's content (which stores the verify clock) is irrelevant since eviction uses mtime, not content. Given the instruction against speculation, I need to be precise about this rather than just plausible. I'm now weighing whether this replay-window issue is the strongest finding to report, or whether the audit log being writable inside ROOT -- combined with `_log_event` silently swallowing all exceptions -- is a cleaner, more clearly grounded issue to flag instead, since it undermines the entire purpose of having a tamper-evident receipt.

Comparing candidates by actual damage potential: the replay window is tiny and the POSIX keyfile issue is platform-specific, so I'm leaning toward the log-in-ROOT problem as the primary finding. But there's also the production default warning around line 102, where a missing sentinel seems to silently let a security gate pass through unchecked.


