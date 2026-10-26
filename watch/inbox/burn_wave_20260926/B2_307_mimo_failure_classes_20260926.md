# B2-307 mimo_watch non-HTTP failure classes (2026-09-26)

## Verdict

LANDED. The generic "other" ceiling is replaced by named classes: refused /
timeout / dns parsed from the URLError reason or errno, with "other" surviving
only for genuinely unknown shapes and now carrying the exception class name in
an error_class field. Both non-HTTP branches use it: the session-create leg
(serve=down, the unarmed-vs-hung discriminator the brief demands) and the
message-post leg (serve=up, session proved the daemon answers, but the failure
class is still named). The module docstring spec was updated spec-first.

## Evidence file:line quotes

- The disease, tools/mimo_watch.py (pre-edit): both generic branches ended
  `"error": str(e)[:160], "error_type": "other"`, and the docstring line 41
  said "non-HTTP failures (refused, timeout) record error_type 'other'" -
  the brief's falsifier state exactly: a refused row and a timeout row both
  read error_type "other" with no distinguishing field.
- Post-edit tools/mimo_watch.py: new `_nonhttp_error_row(e, serve=...)` -
  refused = ConnectionRefusedError / ECONNREFUSED errno, timeout =
  socket.timeout or a "timed out" reason, dns = gaierror, else other with
  error_class naming the reason's type; session-create except arm now calls
  it; message-post except arm calls it with serve="up" and probe="error";
  docstring spec lines rewritten (spec before behavior change).
- Class-arm proof (this lane, real exception shapes through the imported
  module): URLError(ConnectionRefusedError(61)) -> refused |
  ConnectionRefusedError; URLError(socket.timeout('timed out')) -> timeout |
  TimeoutError; URLError(gaierror(-2)) -> dns | gaierror;
  URLError(OSError('weird')) -> other | OSError; bare TimeoutError with
  serve="up" -> timeout, serve up. ALL CLASS ARMS PASS. ast.parse green.

## Work done

1. Read the B2-252 error-row shape and both generic branches; confirmed the
   ledger cannot distinguish unarmed from hung today.
2. Added the errno/socket imports, the classifier row builder, and rewired
   both except arms; updated the module docstring spec line first.
3. Proved every class arm from real exception objects; kept the "other"
   residue for unknown shapes (never a silent catch-all).
4. Claim was filed before the first byte read (claim law, QUEUE 19:40:49Z).
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This landing is inverted if any of the following holds: (a) a live probe run
against an unarmed daemon records error_type "other" instead of "refused"
(the classifier is unreachable from the live path); (b) a hung-daemon
timeout records "refused" (the arms are crossed; the discriminator lies
about its one job); (c) the docstring still claims non-HTTP failures record
"other" anywhere in the tree (spec bytes regressed against behavior).

## Bibliography closed

tools/mimo_watch.py (read in full: docstring, _post, _http_error_row,
_serve_probe, both branches; edited as above); watch/inbox/burn_wave_20260926/B2_252_error_capture_20260926.md
(accepted from the brief as the prior-row shape; the B2-252 HTTPError body
shape is intact and untouched). No network calls; classifier proof uses
constructed exceptions only.
