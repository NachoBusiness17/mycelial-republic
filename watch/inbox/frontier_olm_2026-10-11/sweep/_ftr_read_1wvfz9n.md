# THREAD 1wvfz9n

title: Perplexity Decider 27B: Open weights decision model fine tune of Qwen3.8 27B
subreddit: LocalLLaMA
score: 68
num_comments: 12
created_utc: 1790901339
author: rm-rf-rm
permalink: /r/LocalLLaMA/comments/1wvfz9n/perplexity_decider_27b_open_weights_decision/

== SELFTEXT ==
(no selftext)

== COMMENTS (12 fetched) ==
--- [20] u/fgk55555 (pdc88ki):
Oof, needing to run prefill on 27B for a decision is going to be rough

--- [9] u/oxygen_addiction (pdcs82l):
First Cloudflare, now Perplexity. Nice.

--- [6] u/Major_Baby_425 (pdd4s00):
I want Qwen 3.8 27B finetuned to do system 1 decisions AND agentic work, and then for the engine (like llama.cpp) to provide endpoints for both, so a single model does both purposes well and with no extra vram used. And then the kvcache prefix can be shared so that the agent can be called on to make system 1 decisions without reprocessing the prefix.

--- [3] u/tomByrer (pdd1rk9):
I was wondering why such a large model also.  
Though if you want it down to Q3\_K\_M & it still works great, model size & maybe prefil would be less of an issue?

--- [2] u/TheRealMasonMac (pdgeoxu):
https://openrouter.ai/liquid/d1 but it's not open weight

--- [2] u/DinoAmino (pdext6p):
The clef-flash is quite amazing. Who the heck needs 27B for this?

--- [1] u/milkipedia (pdo876s):
Sparse attention rocks for prefill speed

--- [1] u/fgk55555 (pdgv232):
I was hoping to use a fast prefill MoE to handle it like Ling 3 tiny, but for some reason my 7GB Q6 ling prefills at 1200, while Qwen3.6-35B or Gemma4-26B prefill at twice that.  I want something small, fast and knowledgeable, it seems like most options are only 1 to 2 of those at most.

--- [1] u/racctajino (pdgq96l):
disappointing! but I guess they need to make money, seems right up their alley

--- [1] u/racctajino (pdg9o35):
Yeah, using a 27B for this really makes it feel like all these companies are rushing these out. I want to see a decision model from Liquid AI.

--- [1] u/racctajino (pdg9dl6):
Oh I missed that they released a smaller model. I'll have to give that one a try.

--- [1] u/BothYou243 (pdea71j):
decision model? i think jev like models. would be better, like opensource ones like nimble, tev, or even if want 27B go for clef (by cloudflared)
