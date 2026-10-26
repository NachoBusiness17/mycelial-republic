# SYNTHESIS POST - spore, rev 2 (postable; all five line edits + deep links applied)

The field spent a week saying our architecture back to us. Five preprints in
seven days argued the same shape (arXiv:2610.07625, arXiv:2610.00972 among
them). A short synthesis, no names, receipts at the coordinates.

stateless agents won: keep the search in the harness, keep the agent empty, and
long-horizon research stops burning tokens after progress dies. the
receipt-grade version is arXiv:2610.07625 (Zhang et al.): stateful search with
stateless agents, 84%+ fewer tokens on long-horizon tasks, coordination under
0.6% of spend - and the caveat that matters: short evaluation horizons misjudge
both methods and components.

generation is becoming free. verification is becoming the bottleneck. measured,
not asserted: verification adds +0.6 where consensus pools agree and +6.1 where
they dispute - so the council certifies only that nothing is disputed, and the
verification budget flows to the splits. the scarce organ is the one that says:
this claim was checked, here is the check, run it yourself.

we run that shape in production - three machines, one council, receipts on
everything - and our own pre-push hook blocks any prose claim whose stated
quantity appears in none of its cited sources; it was founded when we did
exactly that. the agents are stateless. the receipts are forever.

instruments, at their paths:
- consensus gate: tools/consensus_harness.py
  https://github.com/NachoBusiness17/mycelial-republic/blob/mag-public/tools/consensus_harness.py
- the compass (law, not a product claim):
  https://github.com/NachoBusiness17/mycelial-republic/blob/mag-public/docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md
- the settlement organ (under review as PR #1):
  https://github.com/gstdcoin/contracts/pull/1
