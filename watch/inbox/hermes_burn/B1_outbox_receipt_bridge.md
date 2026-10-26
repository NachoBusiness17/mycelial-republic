# B1_outbox_receipt_bridge (anthropic/claude-opus-5.5, turn 1)

# OUTBOX-to-inbox Receipt Bridge: Design and Landable Spec

**Deliverable:** one patch spec covering two files, a new config file, and a new test file. A seat can apply it as written.

**Falsifier:** section 5.

**Citation convention:** every claim cites `file:line` and quotes the bytes.
- Line numbers for `tools/dispatch_landing_join.py` and `mag/seat_dispatch.py` were hand-counted from the evidence paste. They are not re-read from disk. Re-anchor on the quoted bytes if they drift.
- Lines in `server/server.py` and `mag/orchestrator.py` were not counted. Those are cited by quoted bytes and marked UNVERIFIED-line.

---

## 0. Grounding

<measurement>

**Reported finding:** "PROVEN-LANDED 4 / CLAIMED-DONE-NO-RECEIPT 238 / FAILED 73 / OPEN 2, exit 1".
- Source: `watch/inbox/fix_everything_20261001.md`, Wave 3, row "Q33 dispatch-vs-landing join".
- Instrument: `tools/dispatch_landing_join.py`, default args.
- Moment: 2026-10-01, Wave 3. No clock time is stated in the receipt.
- Context: "6,267 files, 317 seat-dispatch rows", read-only.

**I did not re-run it.** The figure is reported, not re-measured by this spec.

</measurement>

<facts>

| # | Byte fact | Cite |
|---|---|---|
| F1 | OUTBOX is deliberately excluded from evidence: `queue/handoff/<seat>/OUTBOX/<id>.md is NOT evidence: seat_dispatch writes it itself` | `tools/dispatch_landing_join.py:25-26` |
| F2 | The dispatcher writes OUTBOX after finalizing the ledger, and swallows write failures: `fin = _finalize(task_id, ok=ok, detail=detail)` (246), `(outbox / f"{task_id}.md").write_text(` (261), `except Exception:  # noqa: BLE001` / `pass` (264-265) | `mag/seat_dispatch.py:246,261,264-265` |
| F3 | The OUTBOX status line format: `f"# {seat} dispatch {task_id}\n\n- queued: {_utc()}\n- status: {'done' if ok else 'failed'}\n\n"
