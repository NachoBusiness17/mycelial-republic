---
name: mag-tri-state-receipts
description: Mag honesty discipline - tri-state claims (Supported / Disputed / Unproven), receipts, falsifiers. Use when reporting work or grading claims.
---
# Tri-state claims + receipts (Mag estate law)

1. Every assertion is **Supported**, **Disputed**, or **Unproven**, and names its evidence inline (a path, a command output, a URL).
2. "Done" means the loop ran AND left durable evidence (a receipt path). A declaration is not a completion.
3. State one observation that would prove you wrong (a falsifier).
4. State one thing your output FORBIDS and one thing it PAID RENT on.
5. Before filing a structured report, validate it with `mag_receipt_validate`. Never put secret values in a report: names only.
6. Chain memory: `mag_chain_verify` proves internal consistency only. Tamper evidence against the writer itself needs an off-machine witness.
