# riblive1-U3-r1-deepseek (deepseek-chat @ deepseek, turn 1, channel: content)

L1: Decorative verdict kills selector on rel_delta_pct alone
CLAIM: The kill condition for F-W5 is fixed at rel_delta_pct < 3, computed as 100 * mean_abs_dlp / mean(|lp_A|) over shared token positions. A selector whose ordering moves the field less than 3 percent relative to the conditioned-run logprob scale is declared DECORATIVE and killed.
STEAL: Before running probe, add a row to watch/inbox documenting rel_delta_pct's denominator (mean_abs_logprob_scale) so a reader cannot confuse the 3 percent threshold with a raw logprob delta; cite the formula line.
FALSIFIER: A probe row where rel_delta_pct < 3 but top1_churn_rate is high (say > 0.5) and shared_positions is small, proving the metric is dominated by token misalignment rather than logprob agreement.
SOURCE: mag/preload_selector.py "verdict = ("DECORATIVE" if rel_pct < 3.0 else"
LEVERAGE: high

L2: Heat normalization is within-source, not cross-source
CLAIM: tesuji blocks normalize heat by token count and tape blocks normalize heat by duration_ms, each against that source's own max, so a tape block can score heat 1.0 with zero tokens. The 0.2 heat weight therefore compares incommensurable units between the two sources.
STEAL: Run order on default paths and print the top 10 rows side by side across sources; if any tape block with 0 tokens outranks a token-rich tesuji block on heat alone, open a card proposing a cross-source normalization or a per-source heat weight.
FALSIFIER: An order run showing tape and tesuji blocks interleaved by score with heat values whose units are directly comparable (same denominator), which would refute the incommensurability claim.
SOURCE: mag/preload_selector.py "for src in ("tesuji", "tape"):  # within-source heat normalization"
LEVERAGE: medium

L3: Missing timestamp recency collapses to zero, biasing order
CLAIM: A block whose ts is missing or unparseable receives recency 0.0, and when all timestamps are known but span is zero every block receives the same recency, so blocks with malformed ts are silently pushed to the tail of the conditioning order. The orderer has no path to detect or report this.
STEAL: Add a one-line counter to cmd_order printing how many blocks landed at recency 0.0 from unparseable ts vs from genuine oldest timestamp, then re-run order on the real trajectory.
FALSIFIER: An order run on real TESUJI_MAP.jsonl where zero blocks have unparseable ts, making the bias inert on current data.
SOURCE: mag/preload_selector.py "(missing/unparseable ts -> 0.0; span<=0 -> 1.0 for all)"
LEVERAGE: medium

L4: Observer-effect guard reports but does not gate the verdict
CLAIM: The conditioned arm is rerun without logprobs and observer_effect_same_text is recorded in the row, but the verdict is emitted from the logprobs runs regardless of whether the guard passed. A perturbing probe still produces a DECORATIVE or LARGE_EFFECT verdict.
STEAL: In cmd_probe, when observer_effect_same_text is False, change status from MEASURED to MEASURED-PERTURBED and append a note field; do not change the verdict logic, only the label so the row is honest.
FALSIFIER: A probe row where observer_effect_same_text is False and the verdict differs materially from a matched probe where it is True, which would show the guard does not need to gate.
SOURCE: mag/preload_selector.py "observer = run_arm(row["model"], cond, args.predict, args.topk,"
LEVERAGE: medium

L5: Selftest checks order/shuffle invariants but not load_blocks determinism
CLAIM: cmd_selftest verifies orderer determinism, shuffle determinism, shuffle difference, multiset equality, and probe subset invariance, but never checks that load_blocks returns identical bytes on repeated reads or that malformed lines are skipped deterministically. A file growing between the two load_blocks calls would fail ok1 silently as a content difference rather than a parser bug.
STEAL: In cmd_selftest, snapshot the raw text of TESUJI_MAP.jsonl and steps.jsonl before ok1 and re-hash both files after ok1; print a distinct flag when file content changed so a failure is attributed to inputs rather than the orderer.
FALSIFIER: A selftest run where ok1 is True across two load_blocks calls while the underlying file hash is unchanged, showing file stability is already implied and the added guard adds no signal.
SOURCE: mag/preload_selector.py "ok1 = ids_a == [b["id"] for b in again]"
LEVERAGE: low
