# Open source inference engine (like LM Studio or Unsloth Desktop) that optimizes itself for your exact hardware. Compiles and tunes its kernels on your device, so open models run up to 2x faster than llama.cpp. Works on Apple Silicon, NVIDIA, AMD or nothing but a CPU.

- url: https://reddit.com/r/LocalLLaMA/comments/1wuj70v/open_source_inference_engine_like_lm_studio_or/
- id 1wuj70v | score 99 | comments 23 | created 1790808390
- url_in_post: https://github.com/magnitudedev/magnitude

## SELFTEXT

(empty)

## COMMENTS (26)

--- u/tomByrer (score 33):

Thanks, seems like a new project & not really battle tested.  Just 2 guys in 2 months.  
HN has many bugs reported, no multi GPU support, VERY few models (no abliterated , popular fine-tunes) 

Bookmarked to check back later; I have 4 other engines to test which will likely be as fast maybe faster.

--- u/seanthenry (score 24):

I need a raise but you can't do anything about it so I'm taking my lunch break now.

--- u/superslow_jerry (score 20):

Reddit isn’t exactly a citadel of intellectual rigor either

--- u/VotZeFuk (score 13):

> 2x faster than llama.cpp

> +19% in CUDA

yeah, about that...

--- u/quachuoi2 (score 12):

Please explain this to me like I'm the middle manager of a medium sized company

--- u/Shoddy-Tutor9563 (score 6):

Congrats with your release. But can you pls elaborate on "optimizes itself". What exactly does it optimize?

Like for instance, when I want to optimize some model for my GPU(s) on VLLM I take different vanilla quants, for each quant I measure vanilla vs various speculators, then different attention backends, then different KV cache quants and so on and so forth. For each combination I measure pp and tg for both synthetic and real world text, in a single stream and in various parallel streams. As a result I get a table of experiments with many dozens of options. And depending on what exactly I'm optimizing for (pp, tg, biggest KV cache, best aggregate t-put) I pick the one I need for particular use case. There just cannot be a single optimize goal, if you ask me.

So I repeat my question - what exactly does your thing doing, when you're saying it's optimizing itself?

--- u/tomByrer (score 6):

They a small selection of Gemma & Qwen models & forks now: [https://magnitude.dev/models](https://magnitude.dev/models)

But they aren't as specialized as some engines that focus on [serving Qwen3.8-27B](https://github.com/tomByrer/rtx3090-AI/blob/main/README.md#qwen38-27b) or Flash-Next.

--- u/IceFog72 (score 5):

Can't make it run on arch

--- u/thetaFAANG (score 4):

seems perfectly specialized, we need more of that over the one size fits all use cases

--- u/DystopianRealist (score 2):

There's someone that just releasesd a build for exactly your hardware. It's a fork of strata, which is also very recent. Anyways, search this sub, and you should find it. I think the post is within the last 24-48 hours.

--- u/tuifua (score 2):

Pop pop

--- u/Solary_Kryptic (score 2):

[https://magnitude.dev/models](https://magnitude.dev/models)

What do the intelligence %s on the models mean? They list Qwen 3.5 4B at 23% and the 9B at 19%...

--- u/Hodr (score 1):

Everything but ARC, of course.

--- u/de4dee (score 1):

can this be adapted to fine tuning? like "unsloth's kernels reverse engineered or  rewritten from scratch for the hardware that i have", for the model that i tune

--- u/persimmonjones (score 1):

i tried running gemma4 e2b qat on my m4 macbook air, and it didn't seem that much faster (if at all) compared to llama.cpp. maybe they got their 2x on a different model/arch :shrug:

--- u/mantafloppy (score 1):

*snif* Ha... the smell of Ai slop wrapper in the morning.

--- u/IceFog72 (score 1):

it's possible to run .deb on arch. it was stuck on Estimating memory fit and speed on your machine. And show that i have 2 same gpu cards )

--- u/MarcelloT254k (score 1):

Did you try installing only CLI version via npm? Offical desktop versions are only .deb and .rpm so not natively compatible with Arch. (I'm not an expert)

--- u/stcafehtdihhsuB (score 1):

Yeah they changed places. Dunning kruger took over and it went to shit.

--- u/kaliku (score 1):

Agree, especially since redditors flooded it.

--- u/rditorx (score 1):

LM Studio open source?

--- u/paranoidray (score 1):

Website with Video: https://magnitude.dev/

Hacker News Discussion: https://news.ycombinator.com/item?id=49911995

--- u/corbs132 (score 0):

It says in the faq at the bottom of the page.

% intelligence score relative to the top model on artificial analysis

--- u/bonobomaster (score -1):

👎

Couldn't figure out my Nvidia hardware under Windows 11. Two GPUs, 5070 TI and 3060 TI.

Zero options to configure important things.

Trash.

I guess, I'll keep using bare llama.cpp ;)

--- u/stcafehtdihhsuB (score -8):

Why post on HN? It's a cesspit of stupidity and lameness disguised as pseudo intellectualism.

