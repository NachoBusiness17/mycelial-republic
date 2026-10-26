# THREAD 1wybqq3

title: Finetuned 1.5B Qwen to generate bash commands at gpt-4o level using 400k synthetic examples + Fully opensource finetune dataset
subreddit: LocalLLaMA
score: 26
num_comments: 5
created_utc: 1791214696
author: Comfortable-Rock-498
permalink: /r/LocalLLaMA/comments/1wybqq3/finetuned_15b_qwen_to_generate_bash_commands_at/

== SELFTEXT ==
Purely a hobby side project to see how far I can push a really small model, using (mostly) automated training pipelines

Full synthetic data: [https://huggingface.co/datasets/dirac-run/ec-training-data](https://huggingface.co/datasets/dirac-run/ec-training-data)



Models: [https://huggingface.co/dirac-run/ec-1.5b-gguf](https://huggingface.co/dirac-run/ec-1.5b-gguf) and [https://huggingface.co/dirac-run/ec-0.6b-gguf](https://huggingface.co/dirac-run/ec-0.6b-gguf)



Cli [https://github.com/dirac-run/ec](https://github.com/dirac-run/ec)



feel free to train/use the data as you wish.

== COMMENTS (5 fetched) ==
--- [5] u/Comfortable-Rock-498 (pe1i56x):
I tried SmolLM 135M, SmolLM 360M, Qwen3-0.6B, Qwen2.5-Coder-1.5B, Qwen3.5-0.8B, and Qwen3.5-2B. 2.5 coder 1.5B was showing the most consistent SFT gains. Plus a bunch of prior work also used the same model.

I haven't tried it yet but funetuning a larger model using above data might show much larger gains 

--- [4] u/wingwing124 (pe1ioce):
I see! Your post inspired me to try out a little something something, so I am using your same data set and methodology on minicpm5 1B, 2B, and qwen3.5 2B (as well as qwen2.5 coder 1.5B as a control).

If anything interesting comes of it I'll lyk!

--- [2] u/Liberaces_Isopod (pe2bi1x):
Might try the LiquidAI/LFM models as well.  They're pretty impressive for the size and seem to take training pretty well.  I did a finetune around image recognition and it took it pretty well.

--- [2] u/Comfortable-Rock-498 (pe1ml2m):
Good luck! 

--- [1] u/wingwing124 (pe1h6hk):
Very interesting! Can you walk me through why you landed on qwen2.5 coder 1.5B?
