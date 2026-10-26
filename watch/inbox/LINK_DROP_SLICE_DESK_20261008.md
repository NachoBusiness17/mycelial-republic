# LINK DROP: Slice Desk, a LittleBit-on-Grok-1 planner on grok.me (2026-10-08)

Drop: operator pasted https://beepboop.grok.me/#model (bare URL, no comment).

## What the surface is (fetched this sitting)

beepboop.grok.me hosts "Slice Desk", a single-page calculator and workflow
tool for PLANNING a low-bit quantization experiment on Grok-1 (xAI's 314B
MoE, open weights). Same grok.me toy-surface family as gt2samples.grok.me
(configs/aos_grok.yaml). Tabs:

- Rank: given a matrix shape (default 32768 x 6144 expert up-projection),
  target BPW, and path count, solves Eq. 17 for the SVD rank: LOCKED result
  r = 243 (242.595 exact, 0.1002 BPW), memory footprints FP16 402.65 MB
  down to 2.52 MB packed, bar chart.
- Model: sums Grok-1's published shapes to 316.49B params; some file-size
  estimates explicitly marked "parked, not to be used".
- Splits: correction notes on earlier drafts (why ranks 150-200 are wrong;
  why r = 32 on a 4096-corner underestimates BPW; why an Adam-based init
  loop is NOT quantization-aware training).
- Corner: in-browser check of the math on a tiny random 160x160 matrix.
- Jobs: a 0/6 rules checklist (rank must not be reused on smaller matrices;
  no downloading checkpoints; no inventing perplexity scores; et al.).
- Script: a complete Python file, littlebit_slice.py, running a SYNTHETIC
  256x256 test at 0.5 BPW (truncated SVD + sign factors, "dual_svid"),
  comparing relative L2 error against a 4-bit quantization proxy, printing
  a JSON report. No model weights downloaded.

## Why the estate cares (three laws wearing someone else's shirt)

The app's self-enforced constraints are the estate's own discipline, arrived
at independently on xAI's own toy domain: no fabricated perplexity (the
no-fabrication law), synthetic-init-is-not-QAT honesty (the manifest law),
a locked pre-registered rank that must not be silently reused (the
pre-registration / four-pinned-choices law). Ties: the Samsung LittleBit
drop carded this same morning (arXiv 2506.13771, LINK_DROP_LITTLEBIT);
the quant A/B spec (QUANT_AB_SPEC_AMEND.md) is the matching instrument if a
slice run ever graduates from synthetic to real.

## Honest limits

- Grok-1 at 314B does not fit any estate hardware; nothing here changes the
  fleet's quant posture today. The only locally runnable piece is the
  synthetic script.
- The script bytes were read by the fetch summarizer, not extracted
  verbatim. Estate law: never reconstruct code from a summary. If the
  synthetic test is to run, the browser lane extracts littlebit_slice.py
  byte-exact first, then the venv runs it ($0, deterministic, no weights).
- Authorship of the app is unknown (grok.me surfaces are community/X-linked);
  no claim made about who built it.

## Disposition

CARD ONLY, $0. Pull trigger named: browser-lane extraction of the script
bytes + local synthetic run + receipt. Waits at the gate.
