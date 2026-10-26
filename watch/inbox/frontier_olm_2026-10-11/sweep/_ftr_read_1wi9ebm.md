# THREAD 1wi9ebm

title: Xiaomi MiMo 2.6 Live Training Dashboard
subreddit: LocalLLaMA
score: 439
num_comments: 75
created_utc: 1789591758
author: skeole
permalink: /r/LocalLLaMA/comments/1wi9ebm/xiaomi_mimo_26_live_training_dashboard/

== SELFTEXT ==
Cool to see this as it happens!

== COMMENTS (85 fetched) ==
--- [92] u/MomentJolly3535 (pa8tzwn):
Kind of satisfying to watch

--- [58] u/Zeeplankton (pa8wo84):
it is really crazy how expensive these models are to train. I feel like we take this for granted

--- [35] u/Thin_Pollution8843 (pa8yjel):
I was stressed at first but after reminding that this is not my money I relaxed

--- [32] u/parepeg (pa99ucp):
$10 per second. Might be contrarian but I actually kind of prefer mimo over deepseek. It has a nice persona. Deepseek is super smart and focused whereas mimo has a more "connectedness" smartness.

--- [30] u/pyr0kid (pa8v1tk):
huh thats cool. do we have any idea how big these models will be?

--- [28] u/power97992 (pa93dkd):
Around 4000 gpus for 2.6 pros. That is a lot less than astra… 

--- [24] u/fgk55555 (pa8xvbv):
Mimo 2.5 I think was 1T and 333B.  I suspect same arch.

--- [19] u/viag (pa90dky):
Post-training is not just RL. And yeah it takes time, you guys don't realize the amount of work that goes behind gathering data and training those models

--- [18] u/MuzafferMahi (pa8zet5):
A nice little fuck you to closedAI and disanthropic

--- [17] u/NandaVegg (pa94zrs):
Hmm. There was a casual SNS report from DeepMind researcher that (for a single training run) GPU does not really scale above 4k cluster (it even slowed down above 8k presumably because bottlenecks) and mocking Meta and Tesla for acquiring too many GPUs just for training before. This is probably just one intermediate run for Xiaomi's model.

--- [14] u/Kahvana (pa96l9y):
It feels really cool to see the dashboard!

It's really heavily trained on code. I wish it would've been trained a bit more on general / chat data.

--- [14] u/rostadd (pa8zfqy):
what am I looking at, more precisely?

--- [14] u/shy_monkee (pa8ri3m):
1M is like nothing for training a 1T parameters model, bro. You think they just init a project and the model is immediately better than the older one?

--- [12] u/crusaderky (pa9hxez):
I was not expecting Flash and Pro to be trained in parallel. I always assumed that Flash models were always distilled from the Pro model.

--- [11] u/wren6991 (paa1n7h):
Normally I would say 2.5 -> 2.6 would be the same base model in "LLM semver" but after what DeepSeek pulled with dipsy flash V4.1 I honestly have no idea any more

--- [10] u/irfantogluk (pacgwwf):
$1M

https://preview.redd.it/7uvurmu0d2qh1.jpeg?width=1080&format=pjpg&auto=webp&s=f0e599d000a6a82c54892d55c189bfb738904284

--- [10] u/TheRealMasonMac (paa48zy):
Async RL is supposed to alleviate that bottleneck as far as I understand it, though. You can also always train separate teacher models to distill back to the final model as well.

--- [9] u/Qwen30bEnjoyer (pa9mqpb):
hi again claude

--- [8] u/nuclearbananana (pa8ss9s):
That's how model training works. It's not always up

--- [7] u/NandaVegg (pac0aqb):
Yeah, that's how the paper for GLM-5 (the first one) described how they did for the final post-training. Basically creating many domain expert post-train variations and "merged" them into one final model via synthetic datasets.

--- [7] u/NandaVegg (pa8zx1k):
Oh no, this is insane (to see this kind of thing in this scale). I've never seen anything like this since 2022 distributed training experiment in HF.

--- [6] u/Zeeplankton (pac41q5):
4.1 flash being a .1 release makes zero sense to me lol

--- [6] u/power97992 (pa91zxq):
Gathering data takes a lot of time.

--- [5] u/Cross_Whales (paa96r1):
damn... ~3 USD per second for flash model and ~5 USD per second for pro model. I wonder what frontier models are costing the big dogs. 

--- [5] u/nullmove (pa9dv7f):

>this feels so unserious

Possibly because you have never trained a model yourself and have no conception about what any of that entails

--- [5] u/power97992 (pa92lta):
Bigger i think since almost 5 months have passed already

--- [5] u/Bitter-College8786 (pa8wxdi):
Can we already see how long this will run?

--- [5] u/Professional_Price89 (pa8w2zb):
Tell Xiaomi team to show that dashboard to MiMo when benchmark it

--- [5] u/viag (pa8sbp5):
But the benchmark score is improving? And yeah it's noisy, but that's normal when you train with RL.. 

And the price does not surprise me given the scale, doing RL on a 8B model on a single environment can quickly cost thousands / tens of thousands (especially for long-horizon tasks, with LLM-judges, web search tool calls etc.), so yeah training a 1T parameters model is costly yeah...

--- [4] u/thats_so_bro (paan4g3):
Was also looking for that, don't see it. Likely they'll stop once performance stops improving

--- [4] u/Ok-Direction-4480 (pa9y8g1):
I've never seen a model trained live before, cool!

--- [4] u/zball_ (pa9tzlz):
They aren't. Most likely a lot of Hoppers.

--- [3] u/Adventurous-Menu7257 (paizrht):
Deepseek is a bit random and unpredictable as they also have introduced terminale during 3.1 and their 3.2 introduced a new architecture. And also their decision on whether to retire the v4 pro changed constantly 

--- [3] u/GasSmooth7439 (pae2a31):
Honestly, a live training dashboard is almost as interesting as the model itself 

Being able to watch the RL process in real time makes the whole thing feel way less like “a model suddenly appeared” and more like seeing how the model is actually being shaped.

--- [3] u/mudkipdev (pabglv1):
It's RL

--- [3] u/ThaCrrAaZyyYo0ne1 (pa9q3bp):
[u/XiaomiMiMo](https://x.com/XiaomiMiMo) streaming since 2026-09-16 04:00 UTC **Open is what we value.**

Based.

--- [3] u/indicava (pa92oha):
Is it just me or do those loss functions not look healthy? 

--- [3] u/Elouakili_Flexy (pa90lsx):
Watching someone else's reward curve live has become a spectator sport. Every bump up is "we're so back", every dip is "it's joever".

--- [2] u/raamu_thegreat (pau8wxt):
How long will this go for? 

--- [2] u/Adventurous-Menu7257 (paj0od6):
I think the paradigm changed as the right synthetic data for RL code start and rlvr infra matters more. So, traditional distillation on sft no longer is much more trivial. 

And even for the synthetic data like cot and agentic task trajectories, they would prefer 
distilling better models such as claude, gpt, and K3 and other open weight flagships, rather than their own 2.6 pro.

--- [2] u/Bitter-College8786 (paijm8v):
OK, if the training is finished, will they release it or will they apply some post-training stuff which will delay the release further?

--- [2] u/Terminator857 (pagwbuh):
What gemini told me:  
The page at `[https://mimo.xiaomi.com/rl/](https://mimo.xiaomi.com/rl/)` acts as a live dashboard tracking the **Reinforcement Learning (RL) training process** for Xiaomi's AI models—specifically **mimo-v2.6-pro** and **mimo-v2.6-flash**.

Because this is an active training dashboard meant for AI engineers and researchers, it is packed with technical machine learning metrics.

If you look at the training metrics list, one of the primary graphs tracks `critic/rewards/mean`**:**

* **What it is:** During Reinforcement Learning, the AI model generates answers, and a secondary model (called the "critic" or reward model) scores those answers based on how well they follow instructions, solve coding problems, or provide correct logic.
* **The Y-axis (Value):** Represents the average score (reward) the model is achieving during that training step.
* **The Trend:**
   * **Going Up (↑):** This is what engineers want to see. It means the model is learning from its mistakes, figuring out better ways to reason, and successfully adapting to tasks (like the `DeepSWE` software engineering benchmarks listed on the page).
   * **Flattening Out:** This usually means the model has reached a point of diminishing returns, and the training team might need to change strategies, adjust the learning rate, or feed it harder data.

# Other Key Metrics on the Dashboard Explained Simply:

If you are looking at other charts on that page, they generally fall into three categories:

1. **Performance & Progress:**
   * `dynsam/avg@n`**:** Measures the dynamic sampling performance score of the model over time. A higher number or a positive delta (Δ) means the model's outputs are getting better.
   * `DeepSWE` **Benchmarks:** Scores showing how well the models (`pro` vs. `flash`) handle software engineering tasks. Higher numbers mean better coding capabilities.
2. **Training Health (Loss & Entropy):**
   * `actor/entropy_loss`**:** Measures how "creative" or random the model's choices are. If entropy drops too close to zero, the model becomes too repetitive and rigid. Engineers want to see it stay healthy so the model explores different paths of reasoning.
   * `actor/pg_loss` **(Policy Gradient Loss):** Tracks how much the model's behavior is changing update-by-update. It helps ensure the training doesn't suddenly destabilize or "break" the model.
3. **Infrastructure & Cost:**
   * `total cost` **/** `perf/total_num_tokens`**:** Shows the massive scale of the operatio

--- [2] u/waiting_for_zban (pad7ojn):
Windows XP defrag vibes

--- [2] u/NandaVegg (pac12ez):
For general/chat RL, how do you evaluate the output remains largely unresolved (other than 4o/Llama-4-style emoji-spamming attaboy feelgoodizer and janky LLM-as-a-judge scoring which IMO never even worked for IF), though it can be used as an alternative way to augment the datasets by randomly masking input, promoting variations/baking in repetition penalty by n-gram, etc.

--- [2] u/LegacyRemaster (pabpe6d):
already better then opus 4.8 [https://codingfleet.com/blog/deepswe-v11-leaderboard-2026/](https://codingfleet.com/blog/deepswe-v11-leaderboard-2026/)

--- [2] u/comperr (pabe8z6):
It's not, they have a Singapore endpoint that tunnels to CN.

--- [2] u/TheRealMasonMac (paa0jjm):
Crazy to think that this is probably a relatively small amount of compute compared to what Western labs do. I kind of understand why Western models are so far ahead in soft skills since those require more RL especially to hone.

--- [2] u/slndk (pa9mzv5):
This is amazing! Thank you for sharing

--- [2] u/En-tro-py (pa9aqdw):
Data pretty much is the main moat now in my opinion.

Well, that and the $$$ to rent/build the massive compute required...

--- [2] u/power97992 (pa95qyp):
It could be more if they are using ascends. 5/hr is for a b300

--- [2] u/Toooooool (pa90jdp):
how is this accessible globally but their actual MiMo chat interace is china domestic IP's only

--- [2] u/Constandinoskalifo (pa8wjda):
That's actually a cool idea!

--- [2] u/Cool-Chemical-5629 (pa8tmg3):
Trolling much? Pro was tested against DeepSWE at Step 8 of training. Currently it sits at Step 10 and the training is still on-going. It's not the final benchmark, just intermediate review of the current state which is imho a neat thing because it gives us insight into the big model training which other labs keep private.

--- [1] u/raamu_thegreat (pb51b9i):
Oh. Good eye mate. It's possible. 

--- [1] u/scaledev (pb4l7mm):
[https://mimo.xiaomi.com/rl/](https://mimo.xiaomi.com/rl/)

--- [1] u/raamu_thegreat (pb47j8h):
That's very specific. How, and from where, did you get this info? 

--- [1] u/ndrefg (pb1varu):
Both stopped... what does it mean?

--- [1] u/scaledev (pb13jpd):
5 days, 7 hours for pro, 3 days 11 hours for flash

--- [1] u/[deleted] (payalh2):
[removed]

--- [1] u/Terminator857 (painrz2):
If it went well the next stage would be safety training.  If goes bad, they need to fix stuff and try again.  Often can go good for flash model, but not so good for pro model.

--- [1] u/Randomdotmath (pahc7jz):
worth noting: they added visual to 2.6 pro training. does that mean it now has vision unlike 2.5 pro? (only 2.5 flash had it before)

--- [1] u/Terminator857 (pagyat9):
Gemini says another week if things go well:  
We can estimate using the step duration, dataset size, budget burn rate, and standard reinforcement learning (RL) stopping criteria.

1. The Raw Math: Step Timing & Throughput

From the metrics logged on the dashboard:

|**Metric**|**MiMo-v2.6-Pro**|**MiMo-v2.6-Flash**|
|:-|:-|:-|
|`timing_s/step`|\~2 hours 06 minutes|\~2 hours 16 minutes|
|**Tokens per Step**|\~2.22 Billion tokens|\~2.81 Billion tokens|
|**Current Progress**|Step 11 (\~34 hours in)|Step 15 (\~30 hours in)|
|**Pace**|\~11.5 steps / day|\~10.5 steps / day|

Because each step takes **just over 2 hours**, every additional 10 steps adds roughly **21 to 23 hours** of wall-clock time (barring node restarts or crashes).

# 2. Likely Run Duration

In post-training RL, runs do not go on indefinitely because models experience diminishing returns, reward hacking, or entropy collapse.

# Multi-Epoch Agentic Run (1 to 2 Weeks) — ~70 to 120 Steps

* **Estimated End Date:** Late September (around **September 22–27, 2026**)
* **Why:** Xiaomi's MiMo team (headed by Luo Fuli) noted that this experiment is specifically probing **"how far RL can scale"** across 3 dimensions (compute, harnesses/environments, and grader compute). If they want to test long-horizon scaling to see where the `dynsam/avg@n` and `DeepSWE` benchmark curves finally plateau, they may let it run for a full week or two.
* **Total Cost:** This would push cumulative compute past **$5M+**.

# 3. What Will Actually Trigger the Stop?

RL runs are rarely stopped by a calendar timer; they are stopped by the graphs on that dashboard:

1. **Reward Saturation (**`dynsam/avg@n` **&** `critic/rewards/mean` **flattening):** As seen on the dashboard, Pro's gain per step has already started tapering to \~0.5 percentage points per step. Once 3–5 consecutive steps yield zero statistical improvement on the evaluation benchmark (`DeepSWE`), they will stop.
2. **Policy Divergence / Collapse (**`actor/entropy_loss` **&** `train_infer_diff/.../kl`**):** If KL divergence spikes or entropy plummets, the model begins collapsing into repetitive degeneration ("reward hacking"). If they can't recover it with learning rate decay, they will terminate the run and pick the best checkpoint.
3. **Target Parity:** Pro is currently scoring \~62–64 on DeepSWE v1.1. If their internal objective was to match a specific tier of frontier models, hitting that threshold may trigger the final freeze.

# Bottom Line

If the reward curves 

--- [1] u/firejava (pafj3uv):
very cool

--- [1] u/ComposerGen (pad5i6u):
$1,520,218 now 

--- [1] u/power97992 (pad4zlz):
If 200 mw , then 220dollars/s ?

--- [1] u/[deleted] (pacppf9):
[removed]

--- [1] u/Kerem-6030 (pacmowt):
its so cool 🥹

--- [1] u/fugogugo (pabz7fn):
428k 5 hours later 

they burn 10k per hour? damn 

--- [1] u/power97992 (pabog42):
That too

--- [1] u/SPYFF0 (pabmdg9):
It would be the best if OpenAI simply change its name and let others who deserve it (like this) use it instead. 

--- [1] u/WithoutReason1729 (pabbi7q):
Your post is getting popular and we just featured it on our Discord! [Come check it out!](https://discord.gg/PgFhZ8cnWW)

You've also been given a special flair for your contribution. We appreciate your post!

*I am a bot and this action was performed automatically.*

--- [1] u/LongjumpingProduce48 (pab6tvv):
Wow  it's amazed.

--- [1] u/jazir55 (pab4yes):
>There was a casual SNS report from DeepMind researcher that (for a single training run) GPU does not really scale above 4k cluster (it even slowed down above 8k presumably because bottlenecks) and mocking Meta and Tesla for acquiring too many GPUs just for training at the time. This is probably just one intermediate run for Xiaomi's model.

It's like he never thought about that they can do multiple training runs in parallel lmao

--- [1] u/jazir55 (pab4qtl):
They just started training Mimo 2.6 yesterday? Tf?

--- [1] u/[deleted] (pab0sql):
[removed]

--- [1] u/fugogugo (paayv8h):
Jesus 378k usd

--- [1] u/roofedora (paan449):
Why is it so expensive? Don't they have the infra to support the trainings for cheap?

--- [1] u/[deleted] (paafl7z):
[removed]

--- [1] u/Wise-Chain2427 (paadhqd):
that expensive 

--- [1] u/wren6991 (paa219i):
Fun to watch. Any word on whether these will be open-weight?

--- [1] u/MuzafferMahi (pa8zbt8):
I rememher them promoting 1000 t/s type speeds, so probably optimizing inference and gathering training data? Its definetly weird that it took them months to do this tho

--- [1] u/power97992 (pa8wxu7):
It will be at least 2-3 tril params lol,,, this is a new mod like ds v4.1? If it was the same pretraining and the same size  , they wouldve finished post training months ago since v2.5 came out in april

--- [1] u/power97992 (pa8wk5c):
Lol they started    Post training 1.4 days ago, what ahve they been doing for almost 5 months? 2.5 pro came out in april. Pretraining  and experiments  took them almost 5 
 months ?

--- [0] u/Zennytooskin123 (pa905dx):
Inference! 

--- [-20] u/Aggravating-Push-207 (pa8q129):
this feels so unserious

"yeah bruh we kinds spent $1mil but benchmark went down 6%, oops :)"
