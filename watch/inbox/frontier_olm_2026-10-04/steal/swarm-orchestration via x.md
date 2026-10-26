# STEAL CARD - swarm-orchestration via x

Round 2 draft, frontier_olm 2026-10-04. Revised against the Round-1 critique; every fix re-verified at byte level this session (log at bottom). Both sources live-verified via WebFetch.

## CORRECTION OF THE ROUND-1 CORRECTION (erratum, owned)

The find's anchor laws.md:43 is VALID. watch/inbox/frontier_olm_2026-10-04/lens/laws.md:43 IS the consensus law: "**Consensus strength is not correctness:** the flock converged wrong at high strength (0.6-0.67) on all 3 grounded workloads while the single local model was right on all 3 ... never as a verifiable answer generator" (read this session, sed -n '43p'). The 09-30 lens:33 citation is also valid and remains in play.

Round-1's counter-claim ("line 43 of that same file is the single-controller law") was FALSE, and this card's Round-1 verification log planted it: 09-30 lens :40 is the single-controller bullet and :43 is "Correction becomes law, not apology" (sed -n '33p;40p;43p', this session). Cause: the Round-1 reader mapped the first line of a sed window to line 43. Any future citer should cite 10-04 lens:43 (or 09-30 lens:33), never Round-1's "correction".

## FIND 1 - centralized coordination beats independent swarms

URL: https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
Verified live via WebFetch (twice this session, Rounds 1 and 2). Confirmed on page: "Through a large-scale controlled evaluation of 180 agent configurations"; "centralized coordination improved performance by 80.9% over a single agent" (parallelizable work; Finance-Agent +81% vs PlanCraft -70%); "every multi-agent variant we tested degraded performance by 39-70%" on sequential tasks; "independent multi-agent systems amplify errors by up to 17.2x" vs centralized "contained this amplification to just 4.4x"; the orchestrator "effectively acts as a 'validation bottleneck', catching errors before they propagate".

STEAL (mechanism): the fan-out is only half the mechanism; the money is the single centralized merge turn after it. Independent N-way agreement is measured noise amplification (17.2x); one cheap orchestrator turn converts it (4.4x) AND lifts parallelizable task performance (+80.9%).

PORT (critique fix 1: the callable typechecks now; the merge is NEW CODE, not wiring an existing tool):
- The post-fan-out merge turn calls memweave.consensus_quality(answers: list[str], *, independent=None, rho=None) at mag/memweave.py:115 - the actual N-answer consensus-illusion guard, with the measured rho correction n* = n / (1 + (n - 1) * rho) (docstring :132, implementation :173) and verdicts strong / correlated_weak / single, schema memweave.consensus.v1 (read this session).
- claims_verify is the DESIGN SOURCE only, never the callable: run() (mag/claims_verify.py:87) takes NO arguments and verifies ONE hard-coded claim (:37) through a fixed play sequence (:40-41); grep for claims_verify callers outside the module across mag/, tools/, tests/ returns ZERO hits (run this session, mimosa excluded).
- New code inventory: one merge actor + one consensus_quality call + one trail row. Nothing existing is reused beyond the function.
- VERDICT LANDING SPOT (named, critique fix 4b): the owning lane's trail.jsonl, row shape matched to the live rows read this session (queue/lanes/research/trail.jsonl tail: {"ts","actor","event","detail","artifacts"}): append {"ts": <utc>, "actor": "<lane>-merge", "event": "CONSENSUS_MERGE", "detail": <consensus_quality verdict dict: n_answers, n_effective, rho, verdict + pooled-answer spool paths>, "artifacts": [<spooled pooled answers>]}.

ESTATE MAP (organ): GOPHER FLEET. Gate shape: tools/workflow_gate.py:14 G1 "Mickey17 gopher fan-out: per-item named actors in a fan-out" and :47 (read this session). The merge turn slots between the per-item actors and the trail write.

WIDTH-RUNG PRIOR (critique fix 4a: re-scoped): the direct prior for the untested 15-16 rung is the TOOL-COORDINATION TAX, not the error-amplification pair. Live-verified on the Google page this session, under "The tool-use bottleneck": "As tasks require more tools (e.g., a coding agent with access to 16+ tools), the 'tax' of coordinating multiple agents increases disproportionately." Already banked in this run's sweep at watch/inbox/frontier_olm_2026-10-04/sweep/swarm-orchestration-x.md:140, with the 15-16 rung estimation guidance at :143. 17.2x/4.4x stays in the card as the external QUANTIFICATION of the consensus law (architecture choice), never as a width-throughput number. The sweep also records (same read, :135-143): no published tok/h-versus-width curve exists in anything the sweep read; published curves are quality-vs-width.

## FIND 2 - width via parallel tool calls inside one reasoning step (W&D)

URL: https://arxiv.org/abs/2602.07359
Abstract verified live via WebFetch (Round 1, this session; not re-fetched in Round 2): scaling "not only depth but also width via parallel tool calling"; "leverages intrinsic parallel tool calling to facilitate effective coordination within a single reasoning step"; "we obtain 62.2% accuracy with GPT-5-Medium on BrowseComp, surpassing the original 54.9% reported by GPT-5-High"; width scaling cuts turns.

STEAL (mechanism): a cheaper model at width W beats a premium model at depth, by decoding K parallel samples from ONE reasoning step into verifiable task answers.

PORT (critique fix 2: re-scoped to the layer that exists; the full mechanism is honestly out of reach today):
- What does NOT port: flock_dispatch (mag/archetype_image.py:297-305, read this session) is a thin k8s pod fan over flock_job.flock_positions. W&D's mechanism lives INSIDE one model's serving loop. No estate harness has that loop: mag/mindweave_eval.py (11,878 bytes, mtime Aug 10 11:05) is sample-then-consensus with no tool-calling mechanism - its only "tool" mentions are battery workload labels (:44 "tool-use-style", :55 id "tool_use"; grep -i tool = 2 hits, this session). Touching flock_dispatch produces nothing of W&D.
- What ports TODAY on gemma janitors: the decode half. Decode K samples to the ACTUAL task output space (numbers/text), take the majority answer, run one consensus_quality pass. This is the estate's own demanded redesign (10-04 lens:73 "Flock decode redesign ... 'a real redesign, not a patch'"; rib RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md:40-43) and Find 1's merge mechanism. It is majority-vote self-consistency + guard, NOT W&D native parallel tool calls.
- What needs NEW CODE before it exists: a tool-loop harness that lets a janitor emit K parallel tool calls inside one reasoning step. That harness build is unbaked and uncosted here; until it exists the W&D turn-economy claim is UNTESTED on this estate and this card makes no turn-economy promise.

ESTATE MAP (organs): GOPHER FLEET dispatch shape, PERCOLATOR as sink, MINDWEAVE_EVAL as instrument. Concrete port move: Arm B samples decode to percolator candidates (memory/percolator/), merged by consensus_quality; the ready-made battery is mindweave_eval.py:44-55 (fixed workloads incl "tool_use").

## PROBE (rewritten per critique fix 3)

One battery, two arms, local janitors, max_concurrency 3 per the width cap (corpus/steal/TETHERED_LINK_STEAL_20260925.md:49):
- Arm A: flock surrogate consensus as shipped. Expect: reproduction of 0/3 (rib :14-25).
- Arm B: K janitor samples decoded to the actual numeric/text answer space, majority vote, one consensus_quality merge (rho applied). Explicit label: this is majority-vote self-consistency + guard, NOT the W&D mechanism; the janitors' ability to emit valid parallel tool calls in one step is untested and no harness exists for it.
Falsifier (kept): if B scores 0/3, the decode/merge steal is dead on this estate and the merge turn stays unbuilt.
Clause dropped (critique fix 3): Round-1's "fails to match single_local's 3/3" kill is noise-level at n=3 - one workload flip is 33 points, and the estate itself flags "the n is tiny" (09-30 lens:59). Any positive claim requires scaling the battery first (each workload is one dict entry in the mindweave_eval.py:44-55 shape).
Probe 2 (turn economy) is CUT: it needs the tool-loop harness from Find 2(b); Round-1's cost claim ("the only new cost is the decode mode") covered Arm B only and did not cover it.

## WHAT IS ALREADY HELD vs WHAT IS NEW

- Already held (this card does not re-bank as new): the qualitative law is 09-30 lens:33 verbatim ("do not trust multi-sample agreement on grounded tasks; use single local or remote plus an explicit check"); the decode-redesign demand is rib:40-43 and 10-04 lens:73.
- New in Find 1: the external QUANTIFICATION (+80.9% parallelizable / -39-70% sequential; 17.2x vs 4.4x containment; ~16-tool coordination tax). Already banked hours earlier in this run's sweep (swarm-orchestration-x.md:67-70,137-141); this card is the sweep-to-steal port, which is the intended flow.
- New in Find 2: a published mechanism shape advancing the named-open decode delta.

## VERIFICATION LOG (Round 2, this session)

- sed mag/claims_verify.py '1,12p;35,45p;80,95p': run() :87 no args; CLAIM :37 hard-coded; PLAYS :40-41 fixed. grep claims_verify callers outside module over mag/ tools/ tests/ (mimosa excluded): ZERO hits.
- sed mag/memweave.py '110,165p' + grep -n: def consensus_quality :115; n* formula :132 (docstring) and :173 (implementation); verdict vocabulary strong/correlated_weak/single; schema memweave.consensus.v1.
- sed mag/archetype_image.py '295,312p': flock_dispatch :297-305, thin wrapper over flock_job.flock_positions, builds pod specs.
- mag/mindweave_eval.py: ls -la (11,878 bytes, Aug 10 11:05); sed '1,15p' (sample-then-consensus docstring: single_local / strong_remote / flock N cheap samples -> consensus); grep -i "tool" = 2 hits (:44, :55), workload labels only.
- sed 10-04 lens laws.md '43p;73p': :43 consensus law (find anchor VALID); :73 decode redesign.
- sed 09-30 lens laws.md '33p;40p;43p': :33 consensus, :40 single-controller, :43 correction-becomes-law. Round-1's "line 43 = single-controller" claim was false; corrected in the erratum above.
- sed sweep swarm-orchestration-x.md '65,72p;135,143p' + grep -n: Google numbers banked :67-70; "coordination tax rises disproportionately past ~16 tools" :140; 15-16 rung estimation guidance :143; "No published tok/h-versus-width curve exists" :135.
- tail -c 600 queue/lanes/research/trail.jsonl: live row shape {"ts","actor","event","detail","artifacts"} (two MONITOR rows read).
- WebFetch Google blog (second fetch this session): 16+ tools sentence confirmed verbatim under "The tool-use bottleneck".
- NOT run: the probe itself; the W&D tool-loop harness build; no second arXiv fetch in Round 2 (Round-1 fetch stands); no workflow card JSON introspection.
