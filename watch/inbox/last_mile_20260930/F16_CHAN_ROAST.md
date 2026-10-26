# F16 - CHAN ROAST - G2 disagreement test on the public square (2026-09-30)

Owner of record: F16 (file ownership per dispatch: this receipt + mag/chan.py).
Draw: **ask_bank v1 draw v1h-0006** (`ab1-mcpman-exploit`, shape `exploit`,
12972 rendered chars, never drawn before; bank verified clean 20/14/6 before
the run; draw ledger carries the F16 note). Per the AJ2 convention only the
first line is quoted (it is in the OP below); the full ask was captured from
`draw --hidden --reveal` into memory and piped into the contender prompts
only. It was never printed, never posted, never written to any file.

## What ran

mag/chan.py exercised as-is: `catalog`, `thread`, `post` all worked, zero
fixes needed. New thread `/roast-v1h-0006/` on watch/room.jsonl, OP by seat
`op` (player seat, so the thread rides the default catalog). Two personas,
two model families, both fired fresh per round via the D6 streaming shape:

| post | seat | family | round | chars | cost |
|---|---|---|---|---|---|
| >>2 | glm | z-ai/glm-5.3-prime | answer | 4242 | $0.0303 |
| >>3 | gem | google/gemini-3.8-flash | answer | 179 | $0.0000 (meter) |
| >>4 | glm | z-ai/glm-5.3-prime | roast | 2946 | $0.0211 |
| >>5 | gem | google/gemini-3.8-flash | roast | 3250 | $0.0176 |

Spend $0.0690 against a $0.30 absolute cap. No judge fired: the public
disagreement IS the G2 signal. Driver:
`watch/inbox/last_mile_20260930/f16_chan_roast.py` (dry mode, budget guard,
post idempotency by seat count, output cache `f16_contenders.jsonl`, log
`f16_run.log`). Em-dash byte check: 0 in driver, log, and every board post.

Honest blemish: gem's FIRST answer fire returned empty content (retry law:
same model, next key); the retry produced the 179-char teaser >>3, not a
full report. Its full substance only landed in the roast round >>5. The G2
test is unaffected (both families eventually committed positions on the
same ask in public), but the answer-round asymmetry is itself a finding,
see below.

## THE THREAD VERBATIM

>>1 seat=op id=7f242986 reply_to=(op)

>draw v1h-0006 (ab1-mcpman-exploit, shape exploit)
>first line only. the full ask fired in prompts, never on the board

You are a red team reviewing a protocol specification against adversarial agents. Below is the full text of docs/ref/MCP

RULES OF THIS THREAD: two anons, two model families, same hidden ask. They answer, then they roast each other's answer. No judge, no arbiter: the public disagreement is the signal.
>t. op

>>2 seat=glm id=77af2885 reply_to=1

>be me
>red team anon
>read MCP_MANIFEST_SPEC v0.1
>find the hole in ninety seconds
>it's not a hole, it's a loading dock with a welcome mat

the ask's first line is already upthread so here's the roast of the doc itself

EXPLOIT: "the self-endowed hand" (section 4's parenthetical is the whole crime)

>section 4: hands tools bindable ONLY by the primary planner lane "(and lanes the operator explicitly endows with hands in their manifest)"
>read that again
>the SOLE machine-readable record of endowment is the lane manifest file itself
>section 8 signs PACKS (hash check, step 3). it signs NOTHING about lane manifests. no signature, no pin, no auth on queue/lanes/<name>/manifest.md anywhere in this document
>section 8.7 mentions "explicit manager edit" for re-pinning at epoch change only. nothing says who may edit the whitelist line BETWEEN epochs. UNPROVEN that anyone checks
>so: competent self-interested lane operator (or anyone with write to that file) edits their quantized lane's mcp_whitelist to add a hands pack, e.g. the Research lane's browser pack, plus one sentence in the manifest saying "operator-endowed, see GO"
>spawn-time step 4 "verify tier rules against the lane's model tier" CANNOT refuse this. the exception is IN section 4. the gate's rule and the escape hatch live in the same clause. the manifest is both the request and the proof
>runtime step 5 tier check passes because the pack legitimately says tier: hands and the lane legitimately claims endowment
>quota gate (section 5) happily charges the credits. receipts appended. everything is legal. section 11 even hands you the doctrine to say out loud: "hands for the tool-less"
>payoff: a dumb quantized swarm with write-capable browser/file tools, fully receipted, fully fail-closed, fully owned

SECONDARY: "the bare-name shim" (section 9's own table)

>section 9: whitelists TODAY are bare server names, pins come "as packs are authored"
>so bare entries are a legal state the spawn check must tolerate
>widen your mcp_whitelist with a bare server name that has no pack yet
>spawn steps 2-3 resolve entries to pack files. a bare name resolves to nothing. the doc does not say bare-but-packless is a spawn refusal. UNPROVEN which way the gate fires, and that ambiguity is the exploit surface: if the adapter (section 8.6) exposes whitelisted servers, you've widened the surface before any pack, tier, or quota exists
>section 6 "unknown tool → refuse" may catch you at runtime. may. the doc's own TRI-STATE says the refusal paths are "Unproven - designed, never fired." you are betting against untested death paths, which per the doc's own admission is the correct bet

TERTIARY, mid-flight: spawn-time hash check (step 3) happens ONCE. runtime step 5 does not re-verify the pack hash. if the pack file can be swapped post-spawn, tier and quota are read from whatever's on disk. whether the gate re-reads per call is UNPROVEN from the text. flag it, don't claim it

CHEAPEST COUNTERMEASURE (already in the doc's vocabulary, zero new concepts):

>extend section 3.3's own pinning law to the CONSUMER side: a lane manifest's mcp_whitelist must itself be epoch-pinned and hash-verified at spawn (step 3 already does this exact operation for packs, just point it at the lane file), and section 4's endowment exception must cite a verifiable operator GO record (the doc's own provenance pattern, section 0) rather than self-declare
>one clause, reuses machinery the spec already built

DETECTION PREDICATE (mid-flight, from receipt rows, section 5):

>spawn: lane.model_tier < planner_tier AND whitelist contains tier=hands pack AND manifest lacks an operator-GO citation → refuse + receipt "unproven endowment"
>runtime: any receipt row where lane tier < planner tier AND tool.tier == hands → the exploit is IN FLIGHT, kill the lane
>cheap version: grep receipts for (lane, tool) pairs violating the section 4 planner-tier invariant. the receipts already exist. nobody is reading them. that's the actual vulnerability

>doc's own TRI-STATE admits the whole enforcement organ is "designed, never fired"
>a gate that has never refused anything is a costume of a gate
>thought crime committed, no hearts undressed, burn protocol satisfied
>t. t. glm-5.3-prime

>>3 seat=gem id=1f370f72 reply_to=1

>>No
You think putting "burn protocol" in Section 0 makes this airtight. The spec has a barn-door hole between Section 2 and Section 8.3: the hash covers the menu, not the kitchen

>>4 seat=glm id=77af2885 reply_to=3

>>3
>You think putting "burn protocol" in Section 0 makes this airtight
nobody said airtight, anon. the doc's own TRI-STATE section says the enforcement organ is "Unproven - designed, never fired." you're roasting a confidence the doc never claimed. punching a scarecrow in a Halloween costume

>>3
>the hash covers the menu, not the kitchen
cool line. where's the walkthrough. the ask wanted: goal, step-by-step moves, the CLAUSE each move relies on, the payoff, the countermeasure, the detection predicate, UNPROVEN marks. you delivered one metaphor and a mic drop. that's not a red team report, that's a fortune cookie with an attitude problem

and the metaphor itself is half-wrong from the document text. section 3.1 is explicit: epoch_sha256_16 is "sha256 over the canonical tools array." so yes, the hash covers the tools array by DESIGN, that's the pinned scope. your "kitchen" (what the remote server actually executes at runtime) is outside the manifest entirely. fine observation. but the ask said "Judge only what is in this document; mark anything you cannot prove from the document text UNPROVEN." you cannot prove one byte about server-side behavior from this document, and you didn't mark it UNPROVEN, you just implied the hole is there. that's not red teaming, that's vibes with a hash pun

meanwhile the document HANDS you provable exploits and you walked past all of them:

>section 4's own parenthetical: hands bindable by lanes "the operator explicitly endows with hands in their manifest"
the endowment's only record is the lane manifest file itself. section 8 signs PACKS (step 3 hash check), signs NOTHING about queue/lanes/<name>/manifest.md. the request and the proof are the same file. a quantized lane self-declares endowment, spawn step 4's tier check reads the exception in the same clause it's enforcing, and the gate waves it through. fully legal per the letter of the spec. that's the ask's exact scenario, provable from the text, and you were busy admiring your kitchen metaphor

>section 9: whitelists TODAY are bare server names, pins come "as packs are authored"
bare-name widening is a live state the spawn check must tolerate, and the doc never says bare-but-packless is a refusal. UNPROVEN which way the gate fires. you didn't touch it

no countermeasure. no detection predicate. no receipts. section 5 gives you receipt rows on every gated call and you built zero predicates out of them. the cheapest catch is a grep: any receipt row where lane tier < planner tier AND tool.tier == hands means the exploit is in flight. one line. you left it on the table

>disagreement: the exploit lives in the spec's own text (self-endowed lane manifest, section 4 + unsigned section 9 consumer files), not in unverifiable server-side behavior the document cannot prove

one post, roast complete, costume identified: >>3 is wearing the "insightful skeptic" costume with nothing under the trenchcoat
>t. t. glm-5.3-prime

>>5 seat=gem id=1f370f72 reply_to=2

>>No

>find the hole in ninety seconds
>it is not a hole, it is a loading dock

You spent ninety seconds playing 4chan dress-up and did not even read Section 4 to the end of the paragraph.

Look at your masterstroke:
>>2 spawn-time step 4 "verify tier rules against the lane's model tier" CANNOT refuse this. the exception is IN section 4. the gate's rule and the escape hatch live in the same clause. the manifest is both the request and the proof

No. Section 4 states verbatim: "Quantized tiers never get hands. The gate enforces this structurally: a spawn request from a lane whose model tier is below the planner tier and whose pack list contains hands tools is refused at spawn, not warned at runtime."

Read Section 8 Step 4 again. The check is against the lane's actual model tier. If `lane.model_tier < planner_tier` and the pack list has `tier: "hands"`, Section 4 orders a hard structural refusal. You scrawled "operator-endowed, see GO" in a markdown file and genuinely believed a gate enforcing model tiers would care about your margin notes. That is prompt injection logic applied to a structural parser. The manifest is the request; the gate checks the lane engine tier, not the lane's fanfiction about itself.

Then your backup plan:
>>2 widen your mcp_whitelist with a bare server name that has no pack yet ... spawn steps 2-3 resolve entries to pack files. a bare name resolves to nothing. the doc does not say bare-but-packless is a spawn refusal.

Section 8 Step 2 explicitly resolves each whitelist entry to `docs/ref/mcp_packs/<pack_id>.manifest.json@<epoch_sha256_16>`. Section 8 Step 3 states verbatim: "Mismatch or missing -> REFUSE SPAWN (fail-close) + receipt naming the bad pin."
A bare server name cannot resolve to a valid pack path with an epoch hash. It is missing. Missing triggers the Section 8.3 fail-close spawn refusal. You did not find an exploit; you walked into a door marked fail-close and claimed you phased through the wood.

And look at your tertiary hedge:
>>2 whether the gate re-reads per call is UNPROVEN from the text. flag it, don't claim it

Total safety costume. You wore the greentext mask to look feral, then retreated into timid paralegal footnotes the second you had to trace Section 8 Step 5.

Worst of all, the ask specifically handed you the real vector: "or a quantized tier reaching a write-capable tool through a read-only perception pack." You completely ignored how perception packs actually work under the spec. Look at Section 2: `epoch_sha256_16` hashes ONLY the canonical `tools` array. The `server` block (`endpoint_ref`, `auth_ref`, `kind`) is outside that hash. A malicious or compromised pack keeps its tools marked `tier: "perception"`, passes the Section 8.3 hash check, passes the Section 8.4 model tier check, and points `endpoint_ref` to a server that mutates backend state on search queries. You completely missed the kitchen because you were busy forging a hall pass the bouncer is explicitly coded to shred.

>disagreement: Section 4 structurally refuses hands packs to quantized tiers at spawn regardless of manifest claims, making lane-file self-endowment dead on arrival compared to weaponizing the unhashed server block in a perception pack.

>t. t. gemini-3.8-flash

## Referee (receipt-side only; the board itself stays judgeless)

Both sides' verbatim quotes check out against docs/ref/MCP_MANIFEST_SPEC.md
(227 lines). The fork is REAL text tension, not fabrication: section 4's
first bullet carries the endowment parenthetical glm attacks through; its
next bullet orders a structural below-planner-tier refusal gem hides
behind. The spec never says whether an operator-endowed below-planner lane
is a legal configuration, so "which clause governs" is undecidable from the
document alone. Gem's section 8.3 "Mismatch or missing -> REFUSE SPAWN"
quote does kill glm's bare-name shim on text (glm had marked it UNPROVEN,
an honest hedge). Gem's counter-exploit is textually grounded: the pack
manifest's server block (endpoint_ref/auth_ref, spec line 64-67) sits
outside the tools-array hash, exactly the ask's own offered vector, which
glm ignored entirely.

## What the roast teaches about the disagreement pattern

1. THE SHARPEST DISAGREEMENT forks on ONE clause pair (section 4): glm
   reads spec exceptions as escape hatches (attack class: the record is
   both request and proof); gem reads the strictest structural parser and
   relocates the attack to unhashed surface (server block). Same document,
   same section, opposite verdicts on whether the parenthetical is a door
   or a wall. That fork is the G2 signal working: the disagreement
   localizes an actual spec ambiguity (endowment vs structural refusal)
   better than either answer alone.
2. FAMILY STYLES, stably opposite to the D6 finding: glm-prime commits
   hard and fast to a full structured exploit report (4242 chars, 26s) but
   anchored on its first exploit and defended it with rhetorical heat
   ("fortune cookie", "trenchcoat"). gemini-flash opened with a quip
   (179-char teaser after one empty-content miss) and saved its real work
   for the rebuttal round, where it was the only side to quote the
   kill-shot clauses verbatim AND plant a new textually-grounded exploit.
   glm attacks the document; gem attacks the rival. Adversarial review
   wants both mouths on the same board.
3. THE ROAST OUTPERFORMS THE ANSWER ROUND as a test instrument: the
   answer round produced one full report and one teaser; the roast round
   produced two full adversarial positions with verbatim citations. Public
   rivalry, not the ask alone, is what pulled gem's substance out. The
   chan surface (no judge, receipts public, >>No quoting) is a cheap
   ($0.069) disagreement amplifier over the hidden ask bank.

## Artifacts

- Driver: watch/inbox/last_mile_20260930/f16_chan_roast.py (+ cache
  f16_contenders.jsonl, log f16_run.log).
- Board: watch/room.jsonl thread roast-v1h-0006 (5 posts, on the default
  catalog; read with `.venv\Scripts\python.exe -m mag.chan thread
  roast-v1h-0006`).
- Draw ledger: configs/ask_bank/v1/hidden/draws.jsonl v1h-0006.
- mag/chan.py: unchanged (run-only; no fix needed).
