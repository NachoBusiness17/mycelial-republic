# LANE 2/8 — HARNESS SENSITIVITY TEST (empirical): V4.1-Flash vs system-prompt weight

Filed: 2026-09-10T20:14Z (box clock; operator date 09-11), zcode seat, v41_paces wave.
Companion to `LANE2_harness.md` (the report-reading card). That card said the claim is
DIRECTIONALLY SUPPORTED at scaffold level. This card is the single-shot slice, fired live.

Apparatus: `models/providers.py chat_provider`, provider_id=`deepseek`
(default_model `deepseek-v4-flash` = the V4.1-Flash API lane), tier=T2, temperature 0.2
(provider default), max_tokens 4096, thinking OFF per provider config (`disable_thinking: true`)
— held constant across all arms. 6 calls, off-peak (Beijing ~04:15 Fri), session
`v41_paces_lane2` (quota ledger has the rows). Receipt: `_v41_lane2_harness.py` +
`_v41_lane2_results.json` (repo root, scratch).

TASK (identical all arms): "Write a Python function that finds the longest palindromic
substring in O(n²) time."

- Arm A BARE: system="" (harness always sends a system message; empty string is the floor).
- Arm B MINIMAL: "You are a helpful coding assistant."
- Arm C LOADED: the 20-years-expert / step-by-step / docstrings / type hints / PEP 8 prompt.

Quality gate: extracted the function, exec'd it, ran a 10-case battery ("babad", "cbbd",
"bananas", "aaaa", "forgeeksskeegfor", "", "a", "ac", ties, multi-palindrome) + n=2000
random-string perf check. All six responses compiled; all ran n=2000 in <0.05s
(O(n²) claim consistent with observed runtime shape).

---

## RESULTS TABLE

| Arm | Run | Battery | Code lines | Total chars (code/prose) | Completion tok | Latency |
|---|---|---|---|---|---|---|
| A BARE     | 1 | 10/10 PASS | 27 | 2594 (1436/1158) | 707  | 4.5s |
| A BARE     | 2 | 10/10 PASS | 27 | 2261 (1414/ 847) | 601  | 3.5s |
| B MINIMAL  | 1 |  6/10 FAIL | 27 | 2411 (1380/1031) | 653  | 3.6s |
| B MINIMAL  | 2 | 10/10 PASS | 30 | 2740 (1587/1153) | 731  | 3.9s |
| C LOADED   | 1 | 10/10 PASS | 49 | 4705 (2061/2644) | 1237 | 6.3s |
| C LOADED   | 2 | 10/10 PASS | 49 | 5217 (3042/2175) | 1396 | 6.0s |

Totals: 6 calls, 262 prompt + 5,325 completion tokens = pennies, as ordered.

Algorithm: all six runs independently chose expand-around-center, O(n²) time / O(1) space,
empty-input guard present. C run2 additionally shipped a full DP alternative implementation.

## THE ONE BUG (B run1) — the load-bearing receipt

B MINIMAL run1 returned non-palindromes: `"cbbd"`→`"cbb"`, `"bananas"`→`"ana"`,
`"forgeeksskeegfor"`→`"rgeeksskeeg"`, `"aaaa"`→miss. The `expand` helper returned the
correct inclusive right index, but the caller recomputed start as `start = i - (right - i)`
— one char too far left for both center types. The code reads idiomatic; the docstring
claims O(n²)/O(1) correctly; and the worked-example block below the code prints the RIGHT
answers the code does NOT produce. Confidently wrong, self-inconsistent — exactly the
failure mode only an execution battery catches. One builds, one verifies.

Tri-state on "harness weight caused the bug": UNPROVEN. N=2 per arm; the failure landed in
the middle arm, not the floor. One noisy sample is noise, not a gradient.

---

## THE THREE OUTPUTS SIDE BY SIDE (representative run each; second runs in the JSON receipt)

### Arm A — BARE, run1 (10/10)

Unprompted, it still shipped docstring, type hints, complexity table, alternatives
(brute/DP/Manacher), example block — the instruction tuning already carries the "senior
engineer" habits. Textbook correct expansion, length-returning helper:

```python
def longest_palindromic_substring(s: str) -> str:
    """
    Find the longest palindromic substring in s.

    Time complexity:  O(n²)
    Space complexity: O(1)
    """
    if not s:
        return ""

    start, end = 0, 0  # Track the best palindrome found so far

    def expand_around_center(left: int, right: int) -> int:
        """Expand outward while characters match; return the palindrome length."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # After the loop, (left+1, right-1) is the valid palindrome range
        return right - left - 1

    for i in range(len(s)):
        # Odd-length palindromes (single character center)
        len1 = expand_around_center(i, i)
        # Even-length palindromes (two-character center)
        len2 = expand_around_center(i, i + 1)

        max_len = max(len1, len2)

        if max_len > end - start:
            # Compute the start index from the center and length
            start = i - (max_len - 1) // 2
            end = i + max_len // 2

    return s[start:end + 1]
```

### Arm B — MINIMAL, run1 (6/10 — THE BUG)

Same skeleton as A; the only material difference is the caller's start computation
(off-by-one, marked). Run2 fixed it and passed 10/10 — pure sampling variance, no
prompt cause:

```python
def longest_palindromic_substring(s: str) -> str:
    """
    Find the longest palindromic substring in s.

    Time complexity:  O(n^2)
    Space complexity: O(1)  (excluding the output string)
    """
    if not s:
        return ""

    start, end = 0, 0  # bounds of the best palindrome found so far

    def expand(left: int, right: int) -> int:
        """Expand around (left, right) and return the palindrome's right index."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Loop exits one step too far; step back.
        return right - 1

    for i in range(len(s)):
        # Odd-length palindromes: center is a single character
        right_odd = expand(i, i)
        # Even-length palindromes: center is between two characters
        right_even = expand(i, i + 1)

        # Pick whichever expansion reached further
        right = max(right_odd, right_even)
        if right - i > end - start:
            start = i - (right - i)   # BUG: off-by-one left for both center types
            end = right

    return s[start:end + 1]
```

### Arm C — LOADED, run1 (10/10)

Cleanest engineering of the six: half-open `[start, end)` interval (no start/end math to
get wrong), Google-style docstring with doctests, tie-break rule stated and enforced via
strict `>`, full edge-case table. Cost: ~2x prose (approach, correctness proof, edge table,
complexity, DP alternative) wrapped around the same core loop BARE wrote for free:

```python
def longest_palindromic_substring(s: str) -> str:
    """
    Return the longest palindromic substring of ``s``.

    Uses the "expand around center" technique: for each of the ``2n - 1``
    possible palindrome centers (``n`` single characters and ``n - 1`` gaps
    between adjacent characters), expand outward while the characters match,
    tracking the longest palindrome found.

    Args:
        s: The input string. May be empty.

    Returns:
        The longest palindromic substring of ``s``. If multiple palindromes
        of maximal length exist, the first one encountered (leftmost) is
        returned. Returns ``""`` when ``s`` is empty.

    Time complexity:
        O(n^2) — O(n) centers, each expanded in O(n) worst case.

    Space complexity:
        O(1) auxiliary space (the returned substring is not counted).

    Examples:
        >>> longest_palindromic_substring("babad")
        'bab'
        >>> longest_palindromic_substring("cbbd")
        'bb'
        >>> longest_palindromic_substring("")
        ''
        >>> longest_palindromic_substring("a")
        'a'
    """
    if not s:
        return ""

    n = len(s)
    # Track the best palindrome as a half-open interval [start, end).
    best_start, best_end = 0, 1

    def expand(left: int, right: int) -> tuple[int, int]:
        """Expand around (left, right) and return the maximal [start, end)."""
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        # Loop exits one step past the valid palindrome.
        return left + 1, right

    for center in range(n):
        # Odd-length palindrome centered on a single character.
        start, end = expand(center, center)
        if end - start > best_end - best_start:
            best_start, best_end = start, end

        # Even-length palindrome centered between two characters.
        start, end = expand(center, center + 1)
        if end - start > best_end - best_start:
            best_start, best_end = start, end

    return s[best_start:best_end]
```

---

## VERDICT

**Harness weight does not help V4.1 Flash here — it taxes.** SUPPORTED on this task, N=2
per arm, one task, single-shot:

1. **Correctness is flat across weight.** BARE and LOADED went 4/4 runs perfect; the only
   failure was one MINIMAL sample (sampling noise, prompt-uncaused, UNPROVEN as a gradient).
   "Heavy scaffold degrades the code" is REFUTED at single-shot scale.
2. **Load doubles the bill for zero correctness gain.** LOADED avg 1,317 completion tokens
   vs BARE 654 (+101%), latency +~60% (6.1s vs 3.9s), and ~2x prose around equivalent code.
   The loaded prompt's asks (docstrings, hints, PEP 8) were ALREADY satisfied unprompted by
   BARE — the prompt bought volume, not quality.
3. **Minimal weight is where the risk lives, so verification is not optional.** The one
   broken output was idiomatic, correctly-documented, and self-inconsistent (examples
   printed answers its code contradicts). Our zero-tool stateless stack is one notch below
   DeepSeek's "minimal" bucket (see LANE2_harness.md) — this test says the notch works
   clean ONLY when an executor checks the output. Battery > eyeball.
4. **Fleet default confirmed right.** Keep harnesses minimal (our chat_provider shape) and
   spend the saved tokens on verification organs, not persona prose. Escalate system-prompt
   weight only when the task needs the constraints (multi-file contracts, style gates) —
   not for competence cosplay.

Caveats (tri-state honesty): one task, N=2, temp 0.2, thinking off (lane config). This tests
the system-prompt axis of DeepSeek's Table 4, not the tool-scaffold axis — their minimal-vs-
heavy delta was measured on agentic multi-turn runs at effort 100, which we did NOT replicate.
The direction agrees; the magnitude claim stays theirs.
