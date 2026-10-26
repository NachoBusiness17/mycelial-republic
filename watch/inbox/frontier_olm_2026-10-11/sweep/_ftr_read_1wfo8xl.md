# THREAD 1wfo8xl

title: 50 AI hyperparameters, 500 training steps, one verified gradient step improved all 5 unseen seeds by 27.8% on average
subreddit: ollama
score: 4
num_comments: 2
created_utc: 1789345207
author: lovettsendit
permalink: /r/ollama/comments/1wfo8xl/50_ai_hyperparameters_500_training_steps_one/

== SELFTEXT ==
I ran a Catalyst experiment that I think gets much closer to the reason I built it.

The result first:

* **50 AI training controls**
* **500 AdamW steps**
* **3 development seeds differentiated together**
* **5 completely unseen seeds kept untouched until the end**
* **One single bounded Catalyst-guided update**
* **5/5 unseen seeds improved**
* **Held-out mean validation loss improved by 27.8%**
* **Catalyst independently checked 5,050 partial derivatives**
* **53,608,500 optimizer steps executed across differentiation, verification and the measured re-evaluations**
* **546.18 seconds total for the Catalyst differentiation and verification**
* **One CPU core**
* **No GPU**
* Hardware: **Intel i5-11400H and 16 GB RAM**

The RTX 3050 Ti in the laptop was not doing the Catalyst computation. This was CPU-side work in Catalyst's interpreter on one core. 

The part I care about is not simply that Catalyst can calculate hypergradients.

The interesting part is that it can measure how a large set of training decisions affect the final result after an entire training process, independently check those measurements, and then use them to make an engineering decision.

# The problem

AI training has a lot of knobs.

Learning rates, warmup, Adam betas, weight decay, clipping, EMA, dropout, LoRA parameters, loss weights, regularization, noise, curriculum settings and more.

Usually you tune these by trying configurations, training the model, looking at the result, and trying again.

Automated tuning makes this more systematic, but the basic process is still:

settings A → train → result

settings B → train → result

settings C → train → result

For this experiment I wanted something different.

I wanted a map of how the **training process itself** responds to its controls.

So I built a small pretrained network with rank-2 LoRA adapters on both layers and made the entire fine-tuning process one compiled Rust function.

Each run contains **500 AdamW optimizer steps**.

The function exposes **50 continuous training-policy controls**, including:

learning-rate schedule anchors, warmup, cosine schedule shape, per-layer learning-rate scales, LoRA alphas and initialization, Adam betas, epsilon, weight decay, clipping, EMA, dropout, regularization penalties, gradient noise, input noise, loss weights, distillation, auxiliary loss settings, curriculum and freezing behavior. 

# I did not differentiate one lucky training seed

This was important because the first version of this experiment taught me that a gradient from one stochastic training trajectory can partly describe that specific seed.

So this time the objective contains **three complete training runs at once**.

Catalyst differentiates:

mean validation loss across seeds 0, 1 and 2

plus

10 × the variance across those three seeds

The variance term is small at this scale. It acts mainly as a stability tie-breaker.

Seeds **10, 11, 12, 13 and 14 were not evaluated until the final test**. 

So conceptually Catalyst is differentiating:

**50 training controls**

→

**500 optimizer steps on seed 0**

**500 optimizer steps on seed 1**

**500 optimizer steps on seed 2**

→

**one final training objective**

For every control, Catalyst gives me the local effect of changing that setting on the final objective after the entire training process.

# Catalyst produced a sensitivity map of all 50 controls

The strongest controls at this operating point were:

* `beta2`: elasticity **-5.52**
* `ema_decay`: **+0.84**
* `beta1`: **+0.57**

Overall:

* **3 controls were HIGH sensitivity**
* **24 were MEDIUM**
* **23 were NEAR-ZERO**
* **17 of the 50 controls accounted for 90% of total elasticity**

So before changing anything, I already knew something a normal best-configuration search does not directly tell me:

**which controls matter locally, which direction they push the final result, and how strong that effect is relative to the others.**

That is one of the main things I find useful about Catalyst.

If I have 50 things I could spend engineering time tuning and 23 of them are barely affecting the result at the current operating point, that is valuable information by itself.

# The verification is the part I think is easiest to miss

Catalyst does not calculate a derivative and simply assume it is right.

With **N = 50 controls**, Catalyst uses:

**2N + 1 = 101 verification points**

That means:

* the original point
* every control moved slightly downward
* every control moved slightly upward

At every verification point, the independent verifier estimates all 50 partial derivatives using central differences at multiple step sizes.

Each objective evaluation in this experiment means running:

**3 complete seeds × 500 optimizer steps = 1,500 optimizer steps**

The complete measured accounting was:

* **5,050 tangent evaluations**
* **101 primal values**
* **30,486 verifier evaluations**
* **102 measured before/after evaluations**
* **35,739 total objective evaluations**
* **107,217 complete 500-step training trajectories**
* **53,608,500 optimizer steps**

Catalyst completed the differentiation and verification in **546.18 seconds**.

Again, this was on one core of an **Intel i5-11400H laptop CPU**, with no GPU acceleration. 

All **101/101 verification points passed** at the declared tolerance. 

The reason Catalyst spends that much computation checking itself is intentional.

The derivative path produces the sensitivities.

A separate numerical path asks whether the actual program moves the way those sensitivities say it should.

If they disagree beyond the allowed error and uncertainty, Catalyst refuses the result.

# Then I used the information exactly once

Before the derivative existed, I fixed the update rule.

There was no repeated tuning after seeing the answer.

The rule was:

* rank all 50 controls by absolute elasticity
* use only the top 8
* move against the normalized gradient
* trust radius = `0.08`
* maximum move per control = 5% of its declared range
* maximum move per control = 20% of its current value
* respect all parameter bounds
* apply the change once

The actual normalized move ended up being about **4%**, so this was not a giant jump across parameter space. 

Before the update:

**3-seed objective = 0.007466**

After the update:

**3-seed objective = 0.006365**

That is a **14.7% improvement from one bounded step**.

The first-order sensitivity map predicted an improvement of about:

**-0.001194**

The actual measured improvement was:

**-0.001101**

So the verified local gradient did a fairly good job of predicting what the multidimensional change would actually do. 

# Then I froze the settings and touched the unseen seeds for the first time

This was the test I cared about most.

Catalyst had only differentiated development seeds 0, 1 and 2.

The new settings were frozen.

Then I evaluated both the original and Catalyst-guided settings on seeds 10 through 14.

|Seed|Original|Catalyst-guided|Change|
|:-|:-|:-|:-|
|10|0.00967|0.00701|**-27.5%**|
|11|0.00494|0.00442|**-10.7%**|
|12|0.00593|0.00442|**-25.4%**|
|13|0.01300|0.00987|**-24.1%**|
|14|0.01436|0.00890|**-38.0%**|

Held-out mean:

**0.00958 → 0.00692**

That is:

# 27.8% lower mean validation loss

and:

# 5 out of 5 unseen seeds improved



That is the result I found most interesting.

One small update, based only on sensitivities measured across three development seeds, transferred positively to every stochastic training seed that had been kept untouched.

# There was another result I did not expect

The sensitivity map changed substantially when I moved from one development seed to three.

For example, in the earlier single-seed experiment `ema_decay` was almost irrelevant.

In this multi-seed objective it became the **second most influential control**.

`beta1` also changed sign.

That means a hypergradient from one training trajectory can partly be telling you something about that trajectory, not necessarily the broader training process.

Optimizing the mean behavior across several seeds produced a materially different picture.

To me, that is interesting in its own right.

# I also compared it against conventional random search

I do not want to hide this result because it clarifies what Catalyst is and what it is not.

If the only goal is:

**find the lowest loss on this tiny and extremely cheap training problem**

then random search wins.

Quite comfortably.

Giving local random search the same **objective-evaluation count** Catalyst consumed produced a lower final loss.

Even 101 local random configurations found a lower-loss configuration than Catalyst's one deliberately small trust-region step. 

I think that distinction matters.

Random search tells me:

**configuration #22,354 was the best one I happened to test**

Catalyst tells me:

* the direction of every control
* the magnitude of every control
* the relative importance of every control
* which controls are barely relevant
* which controls dominate the result
* independently checked derivatives for each one

And in this demo I only let Catalyst make **one small bounded move**.

This is not evidence that Catalyst replaces hyperparameter search.

It is evidence that the training process can provide a useful, checked **local map** of itself.

# Why I think that could matter for AI development

A lot of AI engineering still involves expensive experimentation.

Something performs badly, so an engineer asks:

maybe learning rate?

maybe clipping?

maybe warmup?

maybe EMA?

maybe loss weighting?

Then you spend compute answering each question.

A tool like Catalyst potentially changes the starting point.

Instead of treating all 50 controls as equally mysterious, you can begin with measured information about:

**what matters, how strongly it matters, and which direction the current training process says to move.**

That does not eliminate experimentation.

It can make experimentation **less blind**.

And there is another angle that interests me.

AI coding systems can already read a training loop and make an educated recommendation like:

**lower the learning rate**

or:

**increase regularization**

Catalyst gives them access to a different kind of information:

**the actual compiled training program measured this sensitivity at this operating point, and an independent numerical verifier agreed.**

That could make automated AI engineering much more grounded than repeatedly asking a language model to guess which training setting to change next.

# What this demo does not prove

I want to be explicit here.

This does not prove that Catalyst finds globally optimal hyperparameters.

It does not prove that Catalyst replaces search.

It does not prove that the current implementation scales directly to arbitrary large-model training.

The network in this demo is deliberately tiny.

Catalyst currently supports a scalar LLVM subset rather than arbitrary tensor-heavy training programs.

This result is about **local sensitivity**, not global optimization.

And when I previously tried the same 500-step training process at a more aggressive learning rate, the local training landscape became too numerically rough for the derivative to be useful.

Catalyst **refused the result** rather than loosening the tolerance until it passed. 

I think that refusal behavior is important too.

# The thing I actually care about

The exciting result for me is not:

**I calculated 50 hypergradients.**

It is:

**I measured the effect of 50 engineering decisions through an entire stochastic training process, independently checked those measurements, used them for one predetermined small update, and that update improved every training seed the system had never seen.**

And all of the differentiation and verification ran in roughly **nine minutes on one core of a six-core 11th-gen consumer laptop CPU**.

If this idea scales, I do not think the future is necessarily one where hyperparameter search disappears.

I think the more interesting possibility is that AI engineers, including AI agents themselves, can get a map of the training landscape **before deciding where expensive experimentation is worth spending time and compute**.

Full unedited demo, source, exact controls, artifacts, all 5,050 checks, timing data, held-out results, and benchmark comparison:

**\[LINK\]**

Catalyst:

[**github.com/lovettsendit/catalyst**](http://github.com/lovettsendit/catalyst)

== COMMENTS (2 fetched) ==
--- [2] u/stealthagents (p9t9uh7):
That’s wild, sounds like you really pushed Catalyst to its limits with just a single CPU. I'm curious about how that performance stacks up against GPU-based runs since most people lean heavily on those for heavy tasks. Have you noticed any particular tuning or setup that made a big difference in this CPU-only scenario?

--- [1] u/lovettsendit (p9taxxx):
I haven’t ran benchmarks comparing the two but that’s something worth me testing in my new build I’m currently working on (it’s not catalyst but I needed aspects of catalyst for it to work)
