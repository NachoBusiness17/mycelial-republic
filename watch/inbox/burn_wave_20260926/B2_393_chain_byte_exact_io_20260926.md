# B2-393 receipt: chain writers must write bytes, not text (2026-09-26, lane SW-03)

## Verdict

LANDED. All four named chain write sites are byte-exact now: mag/verkle_knot.py _rewrite_chain writes via write_bytes, mag/verkle_knot.py:741 append opens with newline="", and both flag scripts (mag/_flag_dangling_264d0ba3.py, mag/_flag_dangling_20260925.py) write via write_bytes; any rerun of them keeps LF as LF on Windows. The no-CR tripwire is live in chain_guard.check(): a chain carrying any CR byte returns state "crlf_rewrite", ok False, with an alarm naming the B2-83/B2-393 repair path. The falsifier witness is pinned as a test: the OLD write_text shape still reproduces the CRLF rewrite on a copy (5/8 rows -> 2 CRLF), proving the hazard was real and the conversion load-bearing. 5/5 tests pass; the live chain is byte-clean today (0 CR bytes, 7,760 lines).

## Evidence file:line quotes

- mag/verkle_knot.py:431 (pre-fix): "CHAIN.write_text(\"\\n\".join(lines) + (\"\\n\" if lines else \"\"), encoding=\"utf-8\")" (text mode, Windows newline translation on).
- mag/verkle_knot.py:738-739 (pre-fix): "with CHAIN.open(\"a\", encoding=\"utf-8\") as fh: fh.write(json.dumps(chain_row, ensure_ascii=False) + \"\\n\")" (append in text mode).
- mag/_flag_dangling_264d0ba3.py:81 and mag/_flag_dangling_20260925.py:90 (pre-fix): identical write_text shapes.
- watch/inbox/burn_wave_20260926/B2_83_flag_restore_20260926.md (the live proof this brief stands on): text-mode write rewrote the LF chain to CRLF while content verify stayed green; only a raw-byte diff caught it.
- Live bytes (this lane): memory/biography/verkle_chain.jsonl contains 0 CR bytes across 7,760 LF-terminated lines (clean before the fix; the fix protects future writes).

## Work done

- mag/verkle_knot.py _rewrite_chain: write_text -> write_bytes of the UTF-8 encoding (fix comment carries the B2-83 receipt and the law).
- mag/verkle_knot.py chain append: open("a", encoding="utf-8", newline="") so the appended \n is never translated.
- mag/_flag_dangling_264d0ba3.py and mag/_flag_dangling_20260925.py: write_text -> write_bytes (both named by the brief as rerun hazards).
- mag/chain_guard.py check(): new no-CR tripwire reading the chain bytes (b"\\r" presence), reported as crlf_bytes in every check output and an early-return alarm state "crlf_rewrite" (ok False) whose alarm text names the text-mode writer and the B2-83/B2-393 re-derive path; fires before the marker logic so the damage shape is never masked by a healthy canary.
- tests/test_chain_byte_exact_io.py (new, 5 tests): _rewrite_chain LF-only round-trip; converted flag-script shape LF-only; the OLD write_text shape reproduces CRLF on Windows (the falsifier witness, platform-skipped where translation does not exist); chain_guard trips crlf_rewrite on a CRLF chain; chain_guard unmarked/green on an LF chain.

## Falsifier

The brief's falsifier, both halves executable: (a) rerunning the flag-script write shape on a copy of an LF chain under the OLD code reproduced the CRLF rewrite (preserved as test_old_write_text_shape_reproduces_the_crlf_rewrite, the witness that the fix is load-bearing), (b) under the NEW code the same shapes keep LF byte-exact (tests 1-2), and (c) any future text-mode chain writer is caught by the chain_guard crlf_rewrite alarm on the first check after the damage. Residual: the two flag scripts are one-off instruments; if a third copy of that write shape is ever pasted elsewhere it is outside this pin until chain_guard's tripwire sees its damage.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_83_flag_restore_20260926.md (the live proof; read via the brief and the chain_guard comment)
- mag/verkle_knot.py (_rewrite_chain 407-434, append branch 738-745)
- mag/_flag_dangling_264d0ba3.py, mag/_flag_dangling_20260925.py (write sites converted)
- mag/chain_guard.py (check(), no-CR tripwire added; standing "regression" state on the live chain is the pre-existing dangling-row condition, untouched)
- memory/biography/verkle_chain.jsonl (live byte check: 0 CR)
- tests/test_chain_byte_exact_io.py (new)
