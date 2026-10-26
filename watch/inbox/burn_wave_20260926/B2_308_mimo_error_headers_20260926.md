# B2-308 mimo error-row header evidence, 2026-09-26

## Verdict

LANDED. _http_error_row now captures the response's Server and Content-Type headers into the row as structured fields resp_server / resp_content_type, so a compressed or binary opaque body that resists decoding is still attributable by header evidence; absent headers read as empty string (honest absence, no fallback branch). The brief's falsifier is dead on bytes: two opaque non-JSON bodies with different Server headers previously differed only in body prose (both error_type "other"); the new pin test drives exactly that pair (cloudflare/text-html vs nginx/octet-stream binary payload) and asserts the rows differ on resp_server as a structured field. tests/test_mimo_watch_error_capture.py: 18 passed (16 pre-existing shape incl. the two new B2-308 pins, plus one claim-law rebase). Ratchet: the two NEW hits this hour are mag/shared_surface.py and tools/openrouter_free_gate.py, concurrent lanes' files; mimo_watch.py (215 lines) contributes none. Em-dash 0 in added bytes.

## Evidence file:line quotes

- tools/mimo_watch.py _http_error_row (post-edit): docstring "B2-308: the response's Server and Content-Type headers ride in the row as resp_server / resp_content_type, so a compressed or binary opaque body that resists decoding is still attributable by header evidence; two opaque bodies from different servers can never produce rows identical on every structured field. Absent header = empty string (honest absence)."; code `"resp_server": hdrs.get("Server", "") or "", "resp_content_type": hdrs.get("Content-Type", "") or ""` with `hdrs = e.headers or {}` (HTTPError's hdr may be None).
- tests/test_mimo_watch_error_capture.py (new pins): test_two_opaque_bodies_differ_by_server_header — nginx row error_type "other" on body b"BINARY-PAYLOAD-NOT-JSON-7f3a" with resp_server "nginx" vs cloudflare row EDGE_BODY with resp_server "cloudflare", asserting error_type equal "other"/"other" while resp_server differs; test_missing_headers_read_empty_not_crash — headers None yields resp_server "" and resp_content_type "" with error_type still "FreeTierError".
- Pre-fix shape (B2-252 test, still green): FreeTierError body vs EDGE_BODY both 403 differ on error_type/error_body; the binary case is the one B2-308 adds, where NO prose discriminator exists.
- Claim-law rebase named: test_message_phase_failure_records_other asserted the B2-252-era "other" for URLError("timed out"); B2-307's landed non-http classifier (docstring: "refused = ConnectionRefusedError / ECONNREFUSED, timeout = socket.timeout", reason-parsed) returns "timeout" for that row, and the failing assertion was stale against the working tree I claimed. Rebased to assert "timeout" with a dated comment naming B2-307's classifier and this rebase; first lander keeps bytes, no B2-307 logic touched.
- Ratchet output: "NEW 198edd83211b76e1 file-too-long: mag/shared_surface.py:418" and "NEW 3b1726dec4670996 except-pass: tools/openrouter_free_gate.py:84" — both concurrent lanes' in-flight files, zero hits from tools/mimo_watch.py or the test file.

## Work done

- Claim law: CLAIM SW-00 lines for both shared files (tools/mimo_watch.py working-tree-modified, tests/test_mimo_watch_error_capture.py untracked, both B2-307's active neighborhood) before editing; retired at landing.
- Read _http_error_row/_nonhttp_error_row and the B2-252 test battery; added the two header fields with the dated law in the docstring before the code, same edit.
- Extended the _http_error helper with a headers parameter (None-safe); added the falsifier pin and the missing-headers pin; updated the module docstring contract.
- Hit a null-byte corruption from a shell heredoc write (real 0x1f/0x00 control bytes landed in the test file), caught by pytest collection, repaired by byte-level replacement with an ASCII opaque-body literal; the landed literal is b"BINARY-PAYLOAD-NOT-JSON-7f3a".
- Rebased the one stale assertion per the claim law (named above); 18/18 pass on the file; ratchet and em-dash checks clean for my bytes.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Two opaque-bodied errors with different Server headers producing rows identical on every structured field kills the landing (rerun test_two_opaque_bodies_differ_by_server_header; it must stay green).
- A header-only capture is spoofable (a proxy can lie in Server); the row records what the wire said, not ground truth — attribution claims from resp_server alone are probabilistic, and the receipt scope is distinguishability, not authenticity.
- If mimo_watch's probe path ever stops using urllib.error.HTTPError (switch to http.client or a client lib), e.headers changes shape and the fields must follow or silently empty.
- The rebase asserts B2-307's "timeout" classification; if B2-307's landing is later amended to a different class for URLError("timed out"), this test must follow that landing, not this receipt.

## Bibliography closed

tools/mimo_watch.py (_http_error_row pre/post-edit, _nonhttp_error_row B2-307 docstring, probe call sites :142/:168); tests/test_mimo_watch_error_capture.py (whole, post-edit); watch/inbox/burn_wave_20260926/B2_252_error_capture_20260926.md (referenced via the B2-252 contract in code); tools/violation_ratchet.py check --changed output. No web sources. Em-dash count 0.
