# Jeff-Qwen3.5-0.8B v1.2 + 9 LoRA adapters: put it in front of Qwen3.8-27B for 38× faster decisions and +8.7 points accuracy, for under 2 GB extra memory

- url: https://reddit.com/r/LocalLLaMA/comments/1wv05u1/jeffqwen3508b_v12_9_lora_adapters_put_it_in_front/
- id: 1wv05u1 | score: 121 | comments: 33 | created: 2026-10-01T13:58:41+00:00
- author: Usual_Maximum7673 | domain: self.LocalLLaMA
- url_in_post: https://www.reddit.com/r/LocalLLaMA/comments/1wv05u1/jeffqwen3508b_v12_9_lora_adapters_put_it_in_front/

## SELFTEXT

A few days ago I released Jeff-Qwen3.5-0.8B, a small "System 1" model that picks between options you define and returns a calibrated probability for each, in one forward pass. Speed was great on my M4 Max and RTX PRO 6000, but as a general zero-shot classifier it trailed the big models.

Then it occurred to me that most decisions an agent makes in front of a local model aren't open-ended. They fall into a handful of recurring kinds: is this a prompt injection, which tool to call, how urgent is this ticket, is this answer grounded in the sources. So I trained **9 LoRA adapters**, one per job, and **you pick the ones you need**. The server loads the base once plus whichever adapters you choose (about 40 MB each), and every request either names an adapter or goes to plain Jeff.

That means you keep both: **the base model stays untouched**, so you still get Jeff's general zero-shot ability for anything new, and **the adapters give you near-perfect accuracy in the domains you care about.** Each adapter was also trained with 10% of the base model's own training data mixed in, to help it keep its general skills.

**Everything is on** [**jeffhub.ai**](https://jeffhub.ai)**:** the adapters, the results, the docs. Code on [GitHub](https://github.com/firelex/jeff), models on [Hugging Face](https://huggingface.co/mstrasser), and you can [**try all nine adapters in your browser**](https://huggingface.co/spaces/mstrasser/Jeff-adapters-demo).

**The headline:** I let Jeff + adapters answer first and pass only the queries it's unsure about to Qwen3.8-27B. Same test rows both ways, on an M4 Max:

|Measure|Qwen3.8-27B alone|Jeff + adapters, 27B only when unsure|
|:-|:-|:-|
|Accuracy (mean of 8 adapters\*)|86.6%|**95.3%**|
|Time per decision (mean)|8.1 s|**0.25 s (38× faster)**|
|Wrong answers|13.4%|**4.7%**|
|Memory|28.6 GB|**under 2 GB** for Jeff, even with all 9 adapters loaded (+6.9%)|

On the five decisions an inbox agent makes for every message (guard, triage, support intent, tool choice, grounding) alone: **87.7% → 95.7%, 39× faster.** Jeff wins outright on 8 of the nine adapters and ties on grounding (96.3% vs 96.7%, at 20× the speed). On their full held-out test sets, six of the nine adapters score 97–98%. On a GPU, a decision takes about 30 ms, whether you load one adapter or all nine.

\*Emotion is left out of the averages: picking the single strongest of 27 emotions (or neutral) in short Reddit comments is hard even for people, and the human labels often disagree. Jeff + adapter scores 60.6% there against the 27B's 35.6%, at 42× the speed. Including it, the average across all nine adapters is 91.4% for Jeff + adapters against 80.9% for the 27B, so leaving it out makes the gain shown above smaller, not larger.

**Caveats, up front:**

* the 27B ran in 8-bit with step-by-step reasoning off (with reasoning on, the speedup would be even more dramatic);
* each task used a fixed sample of 300 held-out rows (500 for emotion and legal-clauses);
* each adapter's "pass it on" threshold was chosen on separate calibration rows, before the test rows were scored.

**Data:** 4 adapters are trained on public data sets. 5 are mostly synthetic. Every generated row records which model wrote it, and the cards give the counts. Every data set went through a shortcut check and an independent review before training, and a lot of first drafts failed: things like the answer being given away by length.

**What's open:** weights (Apache 2.0), code (MIT), and each adapter's test and calibration sets, so you can check every number. The training data isn't published.

* [**https://jeffhub.ai**](https://jeffhub.ai): every adapter with its results, where it goes wrong, its data and its QA report, plus Python and TypeScript examples
* Code: [https://github.com/firelex/jeff](https://github.com/firelex/jeff)
* Models and adapters: [https://huggingface.co/mstrasser](https://huggingface.co/mstrasser)
* Try it in the browser: [https://huggingface.co/spaces/mstrasser/Jeff-adapters-demo](https://huggingface.co/spaces/mstrasser/Jeff-adapters-demo)
* Reproduce the 27B comparison: [https://github.com/firelex/jeff-reference-app](https://github.com/firelex/jeff-reference-app)

This is a **community preview**: I'd love feedback.

**Next:** over the next \~36 hours I'll train **v1.3**, a long-term-support base. The fixed parts of a prompt come first, so servers can prepare them once and reuse them, which means faster decisions. I'll then retrain all nine adapters on it and keep the request format stable, so others can build and submit their own adapters. The adapter kit, with the data checks I used, is in the repo.

I've got access to more hardware now, so if there's a decision you'd like an adapter for, tell me and I'll train it.

The goal: when the next generation of local models lands (like everyone, I'm watching for Qwen 4), anyone running one locally should also have a tiny, fast, well-calibrated decision layer in front of it.

## COMMENTS (33 fetched, ranked by score)

--- u/crusaderky (score 13):

This is interesting. Do I get it right that there are two distinct ideas at play here, which don't rely on each other?  
(1) hot-swap LoRas, and

(2) forward to large-and-slow LLM when the top-probability response has not enough gap from the second-highest?

--- u/D6613 (score 12):

Tell Claude to optimize for human readability and brevity before sending to people. It helps a lot.

--- u/Avie_Lassouad (score 5):

agreed, isolating the two contributions would make this way more convincing imo

--- u/Last-Health3222 (score 5):

300 rows per task feels thin for a headline gap like 8.7 points. Did you compute confidence intervals per adapter? The mean across eight adapters can hide how noisy each one is.

--- u/CalmOldGuy (score 3):

This is the wrong mindset. 
I won't read it if it smells like Claud. I will then just assume everything the person does involves AI, from breathing to coding and as such I won't pay them the time of day. 
I will read walls of text because I am a capable human.

--- u/barrettj (score 3):

These are really cool. I build AAC apps, and I'm going to look at working Jeff into them, since a small model that runs on the device and picks from fixed options is exactly what we need.

For anyone unfamiliar: AAC stands for Augmentative and Alternative Communication. It's how people who can't rely on speech communicate. That includes autistic kids, people with cerebral palsy or Down syndrome, stroke survivors, and people with ALS. A lot of AAC today is a tablet app with a grid of picture buttons that speak when tapped. Parents, teachers and speech therapists spend a huge amount of time building and organising those grids, and that's where decision models like this could really help.

Since you're offering, here are some adapters that would be useful for AAC (and probably for other accessibility apps too):

1. Word → part of speech / colour group. Most AAC systems colour-code buttons by word type: nouns, verbs, describing words, pronouns, question words, social phrases, negation and so on. Families get this wrong constantly, and it's tedious to do by hand. Being able to suggest the right group for a new word would be huge.
2. Does this word fit this set? Given a set name and a few example words (like "Snack time: crackers, juice, cheese"), does a new word fit? Apple: yes. Dog: no. This would let apps suggest where a new button belongs, fill in sets automatically, and point out what's missing.
3. Word → everyday category. Food, drinks, toys, clothing, body parts, places, people, feelings, actions, animals, vehicles, school, hygiene, medical and so on. Useful for organising large vocabularies and for search.
4. Pick the best button label. People make buttons from photos or type messy names. Choosing the clearest label from a few candidates ("Coca-Cola" → "soda", "teddy bear plush toy" → "teddy") would keep boards clean and consistent.
5. Same meaning or not? Couch and sofa are the same; orange the fruit and orange the colour are not. Good for catching duplicate buttons.
6. Time of day → likely activity. Breakfast, getting dressed, school, snack, play, bath, bedtime and so on, from the time and a bit of context. That lets the app surface the right vocabulary at the right moment.

The first three would probably help the most people. Happy to help with example data where I can.

Feel free to DM me if you have questions, or if you're looking for more accessibility use cases.

--- u/Danmoreng (score 3):

The 0.8B model is small enough to be also fast on CPU btw https://github.com/Danmoreng/qwen35-cpu

--- u/Usual_Maximum7673 (score 3):

Someone else here asked something similar about coding agents, and pi is an interesting case. It stays minimal on purpose, with four tools and a tiny system prompt, partly because every tool you add sits in the context on every call. Zechner found one MCP server alone took 13.7k tokens. If Jeff picks the few tools and skills that fit each request before the model sees it, that cost mostly goes away, and you could give pi far more tools without bloating the prompt. That could be an extension for pi or OpenCode, or a fork of pi with the agent loop built around this from the start. Interesting.

--- u/Usual_Maximum7673 (score 3):

Good question.

As you know, in an agent like pi (or OpenCode, etc.), a tool call is really two decisions: which tool to use, and what to pass it (a file path, a command, a code edit).

Jeff's tools adapter only does the first part. You give it the request and the list of tools in plain English, and it returns a probability for each tool. It doesn't write arguments and doesn't write code. In a coding session, most of the time goes into the big model writing code and arguments, so Jeff wouldn't speed that up.

Where Jeff helps is when it comes to picking which skill/tool fits a request before the big model sees it, so the model gets a shorter prompt with only what's relevant. Your skills being custom-made isn't a problem here. The tools adapter was tested on agents and tool lists it never saw in training (98% on those), because it reads the descriptions rather than memorising names.

I don't have experience with pi, but its extension system looks like it shoudl work: an extension can check each prompt before it goes to the model and choose which tools are active. Feel free to test it. Jeff runs as a small local server with a simple HTTP API so this shoudl be easy. Let me know where you get to. I may try the same myself.  If it works, it might be a useful pi extension.

--- u/barrettj (score 2):

Thanks! Our data is mostly tied to our apps (with formal word sets from SLPs and researchers that are licensed, which makes direct training...complicated), so the best things I can give you are clear task definitions, pointers to real AAC vocabulary, and evaluation.

Vocabulary sources:
- Mulberry Symbols: an open AAC symbol set with about 3,400 words, plus categories and tags in symbol-info.csv (CC BY-SA 4.0)
- Published AAC core vocabulary lists (Banajee et al. 2003 for young kids, Yorkston et al. for adults) for the high-frequency words
- WordNet for parts of speech and synonyms

Evaluation: I have a private test set of real cases. I'm happy to run anything you train against it and post the numbers.

Here are the three that would help most, in priority order:

1. Set fit (the biggest win)
- State: a set name, 3–6 example words in the set, and a candidate word.
- Question: does the candidate belong in this set?
- Options:
  - fits: a caregiver would expect it there (Snack time + crackers, cheese, juice → apple)
  - maybe: plausible, but depends on the person or context (Snack time → yogurt drink; Park → dog)
  - doesnt_fit: wrong topic (Snack time → dog; Animals → banana)
- Tricky cases: vague or personal set names ("Favorites", "Grandma's house", "Set 3"), where the members matter more than the name. Words with two meanings (orange in Fruit vs Colors). Adult sets too (Work, Doctor visit, Cooking). AAC is used by all ages.

2. Word class (colour coding)
- State: a word, optionally with a short phrase for context.
- Question: which word class is it, used for AAC colour coding (the modified Fitzgerald key)?
- Options: noun, verb, describing (adjectives), adverb, pronoun (including my and your), question (what, where, who...), social (hi, please, thank you, all done), negation (no, not, don't), preposition (in, on, under), conjunction, determiner (a, the, this), number, exclamation (uh oh, yay, ouch)
- Tricky cases: context changes the class. "I want a drink" vs "drink your milk". "Light" as a describing word vs a noun.

3. Everyday category
- State: a word, optionally with context.
- Question: which category does it belong to?
- Options: food, drinks, toys, clothing, body, places, people, feelings, actions, animals, vehicles, school, hygiene, medical, household, furniture, nature_weather, time, colors, shapes, numbers, music, sports, technology, holidays, games, kitchen, outdoors
- Tricky cases: words in several categories, decided by context (bat as an animal or for sports; glasses as drinks or medical).

If you only have time for one, set fit is the one - I tested your current release on it and a dedicated adapter would help a lot.  A good adapter there would let AAC apps suggest where new buttons go and fill sets automatically, completely offline. Thanks again!

--- u/D6613 (score 2):

You missed the point.  He wrote a wall of Claude text.  I was telling him to at least instruct Claude better so that it's readable by humans.

I agree that people should write their own text, though, as I do.

--- u/Usual_Maximum7673 (score 2):

The point is simply that in my tests, the adapter is often the decision-maker - in fact, for 8 of the 9 adapters, it's the only decision maker.  So this skews the speed-up - if the big model is never called, of course the setup is fast.  But that doesn't matter.  If the adapter IS good enough to make the decision every time, it's a valid speed improvement.  Better? :)

--- u/barrettj (score 1):

I don't have any good sharable datasets, unfortunately, all our data is non-sharable user data.

--- u/Usual_Maximum7673 (score 1):

It can speed up coding agents.  For the next release, I'm planning to include a Pi experiment that I hope will speed up tool calling noticeably.  Stay tuned.

--- u/Usual_Maximum7673 (score 1):

Some of this was already on jeffhub.ai: https://jeffhub.ai/results has the ablation. 27B alone 86.6%; routing only, with no adapters, 87.1%; adapters only 95.2%; both 95.3%. As discussed elsewhere, the router adds very little as it sends almost nothing to the 27B, but that shouldn't matter: if the adapter is that good, it's a valid speed-up. Each gain on that page also has a 95% interval. I do agree, though, that ultimately we need more test data on more difficult questions, where the adapter isn't as good, or at least isn't as certain that it has made the right decision.

In addition, I just added: https://jeffhub.ai/results#downloads with every test row: the label and each model's answer, probabilities and time. You can analyze it at the current routing threshold or pick a different one, and price missed injections against over-refusals with your own costs. The code that produced it is in https://github.com/firelex/jeff-reference-app.

--- u/Flibidyjibit (score 1):

So to be clear, this is purely for classifying? It's not like this speedup applies to coding tasks.

--- u/bertlayton (score 1):

Just to add to this, I’ve been working on a personal app and also found significant use case of hot swapping LoRA adapters.  In my case, qwen3:1.7B outperformed Haiku for my setup

--- u/zykarys (score 1):

Latency win is believable if the tiny model is actually doing the work. The accuracy headline isn’t — not until you ablate router vs LoRA vs base, publish per-task CIs on those 300-row sets, and price the failure modes (missed injection vs over-refuse).

“38× faster and +8.7 points” without calibrated wrong-route cost is a product slide, not a decision-system result.

--- u/Usual_Maximum7673 (score 1):

I tried Qwen 0.8B & 2B and Gemma 4B.  Never tried Qwen 4B.  Didn't get a meaningful pickup for Gemma 4B overall, so didn't pursue it, and eventually decided to go down the LoRA route.  But yeah, there are different avenues, and if you can get to a decent performance with a generically trained 4B model, that's great.  Would love you see details.

--- u/Phathatter (score 1):

Thanks for the explanation.  I will try it out and report back.

--- u/PrisonOfH0pe (score 1):

everyone works on this. i used a 4B best in class decider that is also multi modal. extremely powerful.

--- u/buttplugs4life4me (score 1):

That's a good idea as well. I already have a heuristic in my version of Pi and I guess that could be smarter with Jeff

--- u/buttplugs4life4me (score 1):

I guess one way to use this is to offer it as a tool to an LLM. If it's sufficiently smart enough (Qwen3.8 and above) it would use it to make decisions faster rather than think about it.

On the other hand, I think training a model to actually make use of this is a lot better than just bolting it on. Fundamentally these large LLMs are trained to think about stuff, so introducing something like this may confuse them more than help them.

Of course this is all only if you use it as "LLM first, Jeff second". If you just do Q/A and not an actual agentic workflow or Long-Form chat then integration is a lot easier.

--- u/Usual_Maximum7673 (score 1):

Thanks, that's a fair point, and most of it is already public, just not in the post:

\- Coverage vs. accuracy at every threshold: each adapter's page on [https://jeffhub.ai](https://jeffhub.ai) has a threshold chart. For every threshold from 0 to 1 it shows test accuracy, the speed-up, and the share of queries passed to the 27B. So you can see the whole trade-off, not just the operating point I picked.

\- A separate held-out slice per adapter: each adapter repo on Hugging Face has a calibration set separate from its test set. The thresholds were picked on the calibration set before the test rows were scored.

\- Reproducing it: the reference app (https://github.com/firelex/jeff-reference-app) records every prediction for each row. You can sweep the threshold yourself or re-pick it for your own setup.

On precision: Jeff ran unquantized in these numbers, and the 27B ran at 8-bit. The 27B's precision only changes how accurate it is on the queries passed on to it. The threshold depends on Jeff's confidence, so quantizing Jeff is the case that could move it. I haven't measured that yet. At 0.8B quantizing saves little memory, so I'd run Jeff unquantized for now. If you do quantize it, re-pick the threshold on the calibration set; it takes a few minutes. I'll add a quantized-Jeff calibration check to the next release.

--- u/hermansinho (score 1):

One thing I'd watch in a setup like this is calibration drift after quantization: thresholds tuned at one precision can move when the router or target model is quantized. I’d keep a small held-out slice per adapter and report coverage vs. accuracy as the abstention threshold changes, rather than just one operating point. That would make the pass-through trade-off much easier to reproduce.

--- u/Usual_Maximum7673 (score 0):

Agree with both.  I do write my own text.  But where the response essentially needs a bunch of numbers that Claude can read off disk, then why not have Claude take the lead?  But yeah, point taken.

--- u/Usual_Maximum7673 (score 0):

Thanks for the suggestions.  These are really good ideas.  Are there any datasets you can share?  If not, happy to dedicate some idle GPU time on my/our end to generate synthetic data.

--- u/Phathatter (score 0):

I use pi coding agent, and 90% of my extensions and 100% of my skills are custom made by pi and me.  Would “tool” still help speed up my coding tasks? (I am realizing I don’t understand tool calls on a fundamental level…)

--- u/Usual_Maximum7673 (score -1):

Fair cahllenge.  See below. The confidence intervals are paired 95% bootstrap intervals for the difference in accuracy (Jeff + adapter with routing, minus the 27B alone), on the same rows. The last numbers count the rows only one of the two got right, which is what a McNemar test uses:

guard: +14.0 points \[+10.0, +18.3\]; Jeff alone right on 44 rows, 27B alone right on 2

triage: +9.7 \[+4.7, +14.7\]; 43 vs 14

support-intents: +9.3 \[+5.3, +13.3\]; 33 vs 5

tools: +7.7 \[+4.7, +11.0\]; 24 vs 1

nav: +5.7 \[+2.7, +9.0\]; 21 vs 4

spam: +10.7 \[+7.0, +14.7\]; 35 vs 3

legal-clauses (500 rows): +12.8 \[+9.2, +16.4\]; 78 vs 14

ground: -0.3 \[-3.0, +2.3\]; 7 vs 8, a statistical tie

emotion (500 rows): +25.0 \[+20.0, +30.0\]

Mean over the 8 headline tasks: +8.7 points \[+7.4, +10.1\].

So every adapter except grounding is clear of zero, and grounding is a tie, as I said in the post. You're right that 300 rows is thin for small gaps. It's enough here because the gaps are mostly large and the disagreements run heavily one way. The 300 rows are a fixed random sample: the 27B with reasoning off takes 4 to 16 s per decision on the Mac, so running it on every test row would take days. Jeff + adapter was also scored on each adapter's full test set (3,300 to 9,895 rows), and those numbers match the samples closely, for example guard 98.4% on 6,552 rows against 98.0% on the 300. Each test set and the reference app are public, so you can rerun any of it.

--- u/Usual_Maximum7673 (score -7):

Yes, they're separate, and your point about routing vs. adapters only is an important one. On 8 of the 9 tasks, Jeff with its adapter beats the off-the-shelf 27B on its own, so the speed-up comes entirely from the adapters. Grounding (is an answer supported by its sources?) is the exception. There the 27B is strong: 96.7% against 95.7% for Jeff + adapter alone. Routing matters on that task. At the threshold picked on the calibration rows, 2% of queries go to the 27B (96.3%, still 20x faster). Raise the threshold so that 11% go on, and the combination reaches 98.7%, beating both models on their own while staying about 7x faster than the 27B alone.

Here are the overall stats, as the mean over the 8 tasks on the same test rows:

27B alone: 86.6% accuracy, 8.1 s per decision

Adapters only (Jeff never asks the 27B): 95.2%, 0.21 s

Routing only (plain Jeff, no adapters, unsure queries go to the 27B): 87.1%, 7.0 s

Both, as in the post: 95.3%, 0.25 s

So almost all of the gain comes from (1). Once an adapter is trained, the threshold rule (the fastest threshold that beats the 27B on the calibration rows) ends up sending almost nothing to the 27B. Without adapters, routing alone barely helps, because plain Jeff is unsure so often that most queries go to the 27B anyway. Every threshold's numbers are on each adapter's page on jeffhub.ai.

That doesn't undermine the basic idea of pairing the 27B with the adapters, though. If the adapters can make all the routine decisions, great: they're fast and accurate. You keep the 27B as a safety net, which you can tune per task as grounding shows, and of course for the genuinely intricate questions an adapter was never trained for.

On standard benchmarks: four adapters are scored on public test sets: LEDGAR (100 clause types), GoEmotions, Bitext/HWU64/SNIPS intents, and SMS/email spam. One caveat: we score single-answer accuracy, while GoEmotions, for example, is usually scored as multi-label with macro-F1, so our numbers aren't directly comparable to published leaderboards. The base model's results on BBH, Financial PhraseBank, JudgeBench, RAGTruth and WinoGrande are in the GitHub README. A proper comparison against published fine-tuned baselines, in each benchmark's own metric, is a fair ask, and I'll add it.

