---
name: zcode-mobile-run-cards-20260920
description: OPERATOR TOOLING DEFECT 2026-09-20 — ZCode mobile client cannot
  render dynamic-workflow run cards (graph, agent chips, artifact tables
  desktop-only); operator forced to his desk mid-run ("half finished product");
  standing workaround = deliver run status as plain chat text + committed
  receipts; bug report drafted for operator to send
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_55cc19b6-f736-4f07-b261-293f971a8435
---

During the THE 50 native run the operator could not see it from his phone:
"this fucking sucks i cant see it from my phone... im at my desk typing to you
because doesnt render on phone and y'all released a half finished product"
(screenshot of the desktop run card provided). Initial suspicion of a z.ai
subscription failure was WITHDRAWN: the same ZAI_API_KEY probed 200-ALIVE the
same hour; the failure is the ZCode mobile client's rendering, not the
subscription.

**Why:** the operator works from his phone; any monitoring surface that only
exists in the desktop run pane is a half-finished feature to him.

**How to apply:** every dynamic workflow fired in a session he may watch from
the phone gets (1) plain chat-text status updates (counts, phase, failures,
verdicts — no artifact-card references), (2) a committed markdown receipt in
watch/inbox/, (3) an offer of the netlify dashboard URL once deploy auth lands
(long-pending operator gate). Bug report text drafted for the operator to send
upstream: mobile cannot render run cards, subscription connects fine, need
mobile rendering or a read-only status URL per run.

**2026-09-24 reinforcement (operator, mid-turn):** "don't do workflows it's
breaking my phone interface" — the ban is now total for sessions he's in:
no CreateWorkflow/dynamic-workflow runs at all when he is watching from the
phone, execute inline or via background agents and narrate in plain text.
Todo cards also avoided; plain prose + filed markdown receipts only.

Related: [[reset-day-20260920]], [[resume-window-20260919-evening]]
