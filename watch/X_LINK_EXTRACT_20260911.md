# X_LINK_EXTRACT_20260911 — verbatim harvest (tender: w7s7, lane x_link_research_mine)

Doors used, in doctrine order (`watch/X_HARVEST_DOCTRINE_20260905.md`):
- door 1 (LOWEST risk, sessionless): `https://publish.twitter.com/oembed?url=<status-url>&omit_script=1&dnt=true` — exit 0 on BOTH items.
- door 2 (cite-verify): `https://api.fxtwitter.com/<handle>/status/<id>` — text returned on BOTH items; item 1 re-verified twice, byte-identical (author id 4646156380, created Thu Sep 10 17:59:08 +0000 2026, likes 89, rts 16, views 2725).
- door 3 (item 2 only, article body): `https://api.fxtwitter.com/AnnatarXBT/status/2098032672303968642` carries the quoted X-Article's full block tree.

## ITEM 1 — @PhysRevX status 2098109032472941015
URL: https://x.com/PhysRevX/status/2098109032472941015
created: Thu Sep 10 17:59:08 +0000 2026 (ts 1789063148) · likes 89 · rts 16 · bookmarks 35 · views 2725
outbound link: https://go.aps.org/4xn5lnV  (shortener; target blocked to fetch — see NO SILENT PASS)
media: https://pbs.twimg.com/media/HR37B5WWwAQ70-Z.jpg (1904x1134)
media altText: "A depiction of a quantum birthmark. The figure displays the long-time average of the probability density for a Gaussian wavepacket initialized along a bowtie quantum scar at the center of a stadium billiard."

VERBATIM TWEET TEXT:
A new study presents a theoretical framework showing that isolated quantum systems never fully erase their past. Instead, they leave behind quantum birthmarks — persistent memories of a system's initial state and early dynamics.

Learn more: https://go.aps.org/4xn5lnV

## ITEM 2 — @AnnatarXBT status 2098032672303968642
URL: https://x.com/AnnatarXBT/status/2098032672303968642
created: Thu Sep 10 12:55:43 +0000 2026 · likes 37 · views 1665
quote-tweet target: https://x.com/i/status/2098013767627837827 (article id 2097363355673456640)

VERBATIM TWEET TEXT:
Chinese researchers just published a paper with a brutal title: "The End of Software Engineering."

their argument: writing code is finished as a skill

a human brain holds only so much state and so many dependencies before it stalls

an agent has no such ceiling, and its capacity climbs with the compute you hand it

so the person stops being the one typing the code

you turn into the intent architect - you set the goal, direct the agents, and audit what comes back

which quietly changes what you get paid for: specifying the problem, designing the verification, catching the failure the agent is most confident about

code turns disposable, judgment turns into the job

the person who can prove the output is correct ends up worth more than the person who produced it

that's why i wrote the guide below on building your own agent system from scratch

the paper it's based on is down there too

### Quoted article: $50 or $15: GPT-6 Astra vs Kimi K3, and Why the Smart Money Runs Both
article id: 2097363355673456640 · created 2026-09-10T11:40:36.000Z · modified 2026-09-10T11:40:36.000Z
preview_text: Two frontier models with the same million-token window shipped seven weeks apart. One costs $10 in and $50 out and you rent it. One costs $3 in and $15 out and you can download it. They are not
media_entities: 5

VERBATIM ARTICLE BODY (draft-js blocks, 36 non-empty of 60):

> Two frontier models with the same million-token window shipped seven weeks apart. One costs $10 in and $50 out and you rent it. One costs $3 in and $15 out and you can download it. They are not competing for the same job, and the launch week made that harder to see.

### 1,050,000 vs 1,048,576 tokens · $50 vs $15 out · 99.9% or 62.7%, depending on the harness · 2.8T open weights

On the afternoon of September 3, four chatbots from four companies went quiet inside the same five minutes, right after OpenAI posted a clip of the stars aligning. The replies spelled ASTRA letter by letter. By evening the model was out, Greg Brockman was using the word AGI, and Sam Altman was apologising for a messy rollout.

It was the most-watched launch of the year, and it earned it. GPT-6 Astra is a genuine step on the things OpenAI aimed it at: driving a computer, holding a million tokens without dropping them, finishing hard problems in fewer moves than a human. Pretending otherwise is not a Kimi argument. It is just wrong.

But the week also produced a spec sheet that reads like two different products. Astra costs $10 per million tokens in and $50 out, ships closed, arrives in stages with enterprise access off by default, and carries its most powerful capability behind a gate. @Kimi_Moonshot K3 costs $3 in and $15 out, ships as 2.8 trillion open weights, and has been downloadable since July. Same context window to the token. Everything else points a different way.

> So this is not a piece about which model is smarter. It is about which one is the right tool on Tuesday, because the honest answer changes with the job.

## What Astra is actually for

Start with the part that deserves the hype. Astra's headline is computer use, and the number behind it is real: on OSWorld 2.0 it scores 72.6% at roughly forty minutes per task, where its predecessor managed 65.7% at seventy-five. Faster and better on the same benchmark is the rarest kind of improvement, and it shows up in the demos people actually built during launch week.

Long context is the second strength. On MRCR with eight needles it holds 100% out to 512K tokens and 96.3% in the 512K-to-1M band, the strongest deep-retrieval result any frontier lab has published. And inside Codex, Astra keeps running notes across context windows instead of compacting everything into one summary, so a long debugging session stops forgetting why the first fix failed.

Then there is the ceiling. FrontierMath Tier 4 at 97.6%. Fewer actions than the median tested human on 96% of ARC-AGI-3 levels, with a habit of turning an unfamiliar environment into a compact symbolic model of itself. The alignment table is quietly the most impressive row: 0% cheating on honeypot tasks where its predecessor scored 48.2%, and a 2.4% computer-use safety failure rate against 22% before.

> If you have one hard problem, one agent, and a wrong step that costs more than the tokens do, Astra is the model. That is a real category and it pays for the $50.

## The number to read carefully

The score OpenAI leaned on hardest was 99.9% on ARC-AGI-3, a benchmark built specifically to resist memorisation. ARC Prize published its own run the same day. On their standard harness, where each call is independent and the model can only carry notes it writes for itself, Astra scored 62.7%. On OpenAI's provider adapter harness, which preserves opaque reasoning state between requests and compacts long runs, it scored 99.9%. Same weights, same day, 37 points apart.

ARC Prize accepts both numbers, and so should you. The lesson is not that the high score is fake. It is that the best version of Astra lives inside OpenAI's scaffolding, and that scaffolding is not something you can read, reproduce, or run yourself. Call the model statelessly from your own stack and you get the lower bar.

> The same shape appears elsewhere in the launch. Astra is the first OpenAI model rated Critical for cyber capability. The public model refuses exploit work, the real capability sits behind the Daybreak trusted-access program, and safety checks can pause unrelated tasks while they run. Fortune reported that the efficiency method behind the new architecture has safety researchers worried precisely because it makes the reasoning harder to monitor. Add the staged rollout and the enterprise off-by-default switch, and a pattern emerges: the ceiling comes with a wrapper, and you do not control the wrapper.

## What K3 is actually for

@Kimi_Moonshot K3 is built for the other shape of work. Not one agent going deep for forty minutes, but three hundred going wide at once. Agent Swarm dispatches up to 300 sub-agents across roughly 4,000 coordinated steps, with parallelism trained into the model rather than bolted on as a framework, and Moonshot reports the whole run landing about 4.5 times faster than one agent grinding the same task in sequence.

That shape is cheap by design. At $3 in, $0.30 on cached input, and $15 out, a swarm can afford to be wasteful in a way a $50 model cannot: run the first attempt, throw it away, run it again. The cache rate matters more than it looks, because a swarm re-reads the same spec and the same files hundreds of times, so most of its tokens are the cheap kind.

And it is a model you can hold. 2.8 trillion parameters, published, downloadable, self-hostable behind your own firewall, fine-tunable on your own conventions. The command-line tool is free and MIT licensed. The reasoning is not an opaque state in someone else's harness; it is weights on your disk. Since July, teams that cannot send a proprietary line of code to any API have had a frontier model they can run anyway.

> Vision in the loop is the strength people underrate. K3 writes code, looks at a live screenshot of the result, and corrects. That is how the viral launch demos happened, and it is how a 48-hour unattended run designed and verified a chip on open EDA tools. Not a benchmark number. A finished artifact.

## Strength by strength

Lay it out and the rows stop overlapping. A single hard problem, a single agent driving a browser, the deepest retrieval at a million tokens: Astra, and it is not close. Wide parallel work, cost at any real volume, owning the weights, seeing what the model does, and simply being able to use it this week: K3.

> Notice what the table does not say. It does not say one model is better. It says they were built for different Tuesdays, and the mistake most teams will make this month is paying $50 a million for width, or trying to force a swarm through a problem that needed one deep agent.

## The build that uses both

> The interesting stack is not either model. It is both, routed by job. K3 does the wide work: the research, the fan-out, the hundred files, the first draft of everything. Astra sits at one gate, on the hard tail, where a single wrong judgement costs more than the tokens it takes to check. Most of the tokens run at $15. Only the tokens that decide something run at $50.

> The cost side of that split is arithmetic on published prices, and it is worth doing once so the intuition sticks. Take a swarm run of 4,000 steps, each reading about two thousand tokens and writing five hundred:

> Illustrative shape, not a bill: $180 for the run on Astra, $54 on K3, around $32 once the cache does its job, and about $4.50 to put Astra on the final pass. The expensive model costs less than the price of a coffee when it only reads the answer instead of producing all of it.

The spec that makes the gate work is short, and it is the same evidence rule that keeps a swarm honest on its own:

## When to pay the $50

Be honest about the other side too. If your work is one novel problem a day, Astra is cheaper per outcome than any swarm, because a swarm of three hundred cannot help you with one question that needs a single deep thinker. If your job is a computer-use flow where minutes per task is the metric, Astra's forty-minute OSWorld number is the one that matters and nothing open matches it yet. And if you live inside Codex, the persistent notes are worth the tier on their own.

> Pay for the ceiling when you are standing under it. That is a small fraction of most teams' tokens, which is exactly the point.

## The point

Astra is the most capable single agent you can rent, and the rental terms are the story: a price 2.5 times its predecessor, a best score that lives in a harness you cannot see, a top capability behind a gate, and a rollout that reached your admin console switched off. K3 is the most capable model you can own, and ownership is the story too: the weights, the CLI, the swarm, the bill that tracks work instead of prestige.

> They were built for different jobs. The teams that win this quarter will not pick one. They will route.

- Rent the ceiling when you need it -> own the frontier the rest of the time.

By slash1s (@slash1sol)
