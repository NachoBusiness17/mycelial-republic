# THREAD 1widomo

title: I built a native Vulkan training backend for 143 modern Transformer architectures — no CUDA or PyTorch required
subreddit: LocalLLaMA
score: 33
num_comments: 16
created_utc: 1789602196
author: PhysicsDisastrous462
permalink: /r/LocalLLaMA/comments/1widomo/i_built_a_native_vulkan_training_backend_for_143/

== SELFTEXT ==
I've been working on something that started as the training backend for my Hierarchos architecture, but it has grown into a much broader project:

[https://github.com/necat101/Hierarchos-Native](https://github.com/necat101/Hierarchos-Native)

Hierarchos Native now includes a native Rust + Vulkan backend for training and inference across **143 canonical Transformer architectures**, with additional Hugging Face `model_type` aliases bringing the currently advertised registry to **224 model-type spellings**.

The part I'm most interested in sharing isn't actually Hierarchos itself anymore. It's the Transformer backend underneath it.

The goal is to explore how much of the modern Transformer ecosystem can be implemented directly on Vulkan compute rather than assuming CUDA + PyTorch as the default execution stack.

The backend currently includes native implementations for things such as:

* forward and backward passes
* full-model training
* AdamW
* LoRA/PEFT-style fine-tuning
* embeddings and LM heads
* attention and KV-cache paths
* dense and MoE architectures
* RMSNorm / LayerNorm
* RoPE and positional operations
* common activation functions
* cross-entropy and gradient computation
* mixed-precision infrastructure
* checkpointing/resume
* SafeTensors model interchange
* Hugging Face model, tokenizer, and dataset acquisition from Rust
* native generation/inference paths

The supported architecture registry covers families including Llama, Qwen, Gemma, Mistral/Mixtral, DeepSeek, Phi, OLMo, Granite, Cohere, BERT-family models, T5/BART-family models, and many others.

There are also architecture-specific Vulkan kernels for newer model designs rather than attempting to force everything through one generic approximation.

One thing I want to be careful about: **I'm not claiming this is currently a CUDA/PyTorch replacement, or that supporting a model type automatically means every possible configuration and multimodal component of that model has been validated.**

The architecture registry describes native text-graph implementations. Multimodal packages may contain vision/audio/etc. towers that aren't part of the native text backend, and real-world compatibility still needs broader testing across models and hardware.

What I *do* think is interesting is the direction this demonstrates.

Vulkan is available across NVIDIA, AMD, Intel, and a lot of integrated/mobile-class hardware. If native training stacks like this can mature enough, there is potentially room for ML training infrastructure that is substantially less tied to a single vendor compute ecosystem.

I've been developing and testing this on AMD RDNA 3 hardware, including a ROG Ally Z1 Extreme, which has also been useful for exposing assumptions that tend to go unnoticed when ML software is developed exclusively around high-end CUDA systems.

The repository includes the Rust source, Vulkan compute shaders/SPIR-V, CLI, Hierarchos runtime, architecture documentation, validation utilities, and standalone packaging support.

The supported architecture list is here:

`hierarchos-vulkan/README_ARCHITECTURES.md`

And the main README now contains examples for building the backend, checking Vulkan devices, training Hugging Face models, LoRA fine-tuning, inference, and training Hierarchos itself.

I'm especially interested in feedback from people working on:

Vulkan compute, ML compiler/runtime design, GPU kernels, PyTorch alternatives, AMD/Intel ML, portable training systems, or Transformer architecture implementations.

There is still a lot that needs benchmarking, hardware validation, optimization, and independent testing before making strong performance claims.

But getting this many modern architecture graphs running through a native Vulkan-oriented training system has made me think there may be something genuinely useful here beyond the original Hierarchos project.

Repo:

[https://github.com/necat101/Hierarchos-Native](https://github.com/necat101/Hierarchos-Native)

I'd be very interested in technical criticism, architecture compatibility reports, benchmarks on other GPUs, or contributors who want to stress-test the backend.

== COMMENTS (32 fetched) ==
--- [4] u/PhysicsDisastrous462 (paa89me):
actually, a second to what i had just said earlier, i think i can actually do paged KV cache rather quickly! i will try to get that implemented by the  end of tonight or tomorrow! :3 it turns out it will integrate a LOT easier into my existing framework around what I've already built than i had previously expected! >w<

--- [3] u/PhysicsDisastrous462 (pahmkwt):
Gemma4 support with complete under 2e-7 logit parity has been implemented, and i am in the process of implementing kimi k3 before pushing the next update! :3 i will reply to this comment when its done!

--- [3] u/PhysicsDisastrous462 (pabowxt):
Burn could definitely be an option, and using its backend abstraction would make supporting multiple execution APIs easier if i were to bundle the most popular ones with this vulkan backend

I chose raw Vulkan deliberately, though. Hierarchos-Native isn't just intended to be another Rust implementation of Transformer architectures; a major goal of the project is to explore a framework-independent native training/inference backend where I have direct control over the compute shaders, memory behavior, synchronization, scheduling, forward/backward implementation, and optimizer path.

That does mean the execution backend currently targets Vulkan rather than abstracting CUDA/ROCm/Metal/etc. behind a framework, and I agree that's a tradeoff. Burn would substantially reduce the amount of backend work required and make backend portability easier.

Model portability is separate, however. Hierarchos-Native uses standard SafeTensors and preserves the canonical Hugging Face/PyTorch tensor names, shapes, and layouts for the Transformer implementations, so the weights aren't intended to be locked to Vulkan. Other runtimes can consume those model packages if they implement the corresponding architecture.

Candle also wouldn't completely solve the particular issue you're describing, since its backend support is different from Burn's. Burn is probably the stronger comparison here.

Longer term I wouldn't be opposed to exposing an additional Burn/backend-neutral path. I just don't want that abstraction to replace the low-level Vulkan backend, because building and optimizing that execution layer is one of the main purposes of the project.

--- [3] u/renszarv (pabj63m):
Why didn't your agent use a higher level framework to implement these architectures, like Burn/Candle? So you wouldn't be tied to a single hardware abstraction - and others could also use these models

--- [3] u/Zito_Kadaken (paaitk8):
Nice to see this built and tested on AMD first. Has anyone tried it on RDNA 2 yet? Mine is an RX 6800M with 12GB and Ollama runs on Vulkan fine on it, so I'm wondering how training holds up on the older cards.

--- [3] u/ttkciar (pa9uh7v):
I kind of love this.  Been waiting for llama.cpp to develop a Vulkan-target native training feature, but that stalled out.  Perhaps your project is the solution?

I'll give it a whirl and see what it can do!  According to https://github.com/necat101/Hierarchos-Native/blob/main/hierarchos-vulkan/README_ARCHITECTURES.md it lacks Gemma-4 support, but that's okay, it supports some other architectures of interest -- Qwen3.5, GLM-4.x MoE, and Phi-3 (which covers Phi-4 as well).  I can do a lot with that.

Thanks for sharing :-)

--- [2] u/Zito_Kadaken (paptaga):
You're quite welcome!

--- [2] u/Zito_Kadaken (papr5pr):
It's all good, if it makes you feel any better, doing this caused me to discover that my Kernel and Graphics Driver were out of date. lol

--- [2] u/PhysicsDisastrous462 (paiv8fg):
Your so welcome! It is taking significantly longer than expected, so it may not be done by tonight, im still gonna try, but if things arent finished by tonight, you will see it done by tomorrow! :3

--- [2] u/ttkciar (pai53fd):
Yaay! Thank you!! :-) Those are basically all of the architectures I care about continued-pretraining in the foreseeable future, so thank you for completing the set!

--- [2] u/PhysicsDisastrous462 (pabt8u9):
i could not agree more! in the big 2026, we definitely need platform agnostic software for such a critical technological development that has increasingly entrenched itself into our society! if its going to happen, it should be accessible to EVERYONE and not just people with $10k in Nvidia cards!

--- [2] u/PhysicsDisastrous462 (pabscso):
the paged KV-cache update is pushing to the repo now! i will be heading to sleep when it is done and rest for tomorrow :3 thank you so much for your interest in my work! >w< i hope you have a wonderful nights rest as well!

--- [2] u/hurdurdur7 (paboc87):
I salute everything that shakes the old pytorch & cuda & "we will install a bunch of nvidia stuff into your machines stuff despite you having a rocm setup and even rocm torch installed" tree. I think this generation of tools had it's time, but this time is over. 

--- [2] u/PhysicsDisastrous462 (paaldy3):
Unfortunately I do not have one of those cards 3; i am currently working on a user requested paged KV-caching system at the moment! Anyone who can run some tests with other architectures would be doing the project a HUGE favor! :3

--- [2] u/PhysicsDisastrous462 (paa2z62):
that is definitely on the roster for features added next! although right now im entering some serious financial issues and the time i will have to spend on projects will decline substantially over the next few weeks, i uploaded what i had implemented so far just in case the worst happens, so i wont go making any promises yet.

--- [2] u/wayneworkman (pa9vwo6):
This seems substantial, if you can make it perform. Any plans to implement paged KV cache?

--- [2] u/PhysicsDisastrous462 (pa9uzra):
your so welcome! thank you so much for taking a look at my work! :3 let me know if anything needs to be fixed or if you come across any issues!

--- [1] u/PhysicsDisastrous462 (pd0esyk):
just updated the backend to harden gemma 3 and 4 numerical parity support, falcon h1r, deepseek v4, and the minimax models, AND i got full PEFT support now FINALLY lmfaoo!! :3 lmk what you think of it and if it works for you! :3 sorry for the late update, ive been dead sick lmao

--- [1] u/PhysicsDisastrous462 (pd0eiu6):
just updated the backend to harden numerical parity for gemma 3 and 4, smolLM, falconh1r 7b, deepseek, and minimax, and also got full PEFT support going! :3 i hope you enjoy!

--- [1] u/PhysicsDisastrous462 (pbi0l64):
to everyone still sticking around here, there is about to be a MASSIVE update! im adding parity verified support for gemma3, smolLM, Qwen2.5 and  Qwen3.5, Falcon H1R and native PEFT training with all parity checks passed under 2e-7 max drift! reverse engineering huggingface PEFT is proving to be VERY difficult, but progress is nearing completion!

--- [1] u/PhysicsDisastrous462 (paprj48):
that is an amazing silver lining to hours of headaches!! Its good you caught that, so some obscure mythos discovered vulnerability cannot be leveraged against your system lmao! thank you so much again for testing my work and helping me make sure it works on  all platforms!! :3

--- [1] u/PhysicsDisastrous462 (papmt4b):
Your so welcome! Im so sorry for that annoying bug! :3 ❤️

--- [1] u/Zito_Kadaken (papkzr4):
It works now! I pulled 84b44f8 and ran the same stock settings test on 7.2.5. 3 out of 3 on the 6800M, no device lost, and the loss matched llvmpipe to 5 decimals. I only ran the short 3 step test so far. You didn't waste my time. Thanks for fixing it so fast.



--- [1] u/PhysicsDisastrous462 (papfz43):
see if the latest commit works :3 im so sorry to waste your time 3; these latest patches target radv

--- [1] u/Zito_Kadaken (pap3dl9):
Alos, I put the logs in a github issue on your repo :)

--- [1] u/Zito_Kadaken (pap07nd):
No sweat lol. Yeah I mentioned I was on Fedora but maybe should have been more clear.   
  
I pulled d230abf and ran the stock settings test again on 7.2.5. Still ERROR\_DEVICE\_LOST, 3 out of 3, llvmpipe still trains fine. Happy to rerun it when the Linux fix is up.

--- [1] u/PCmoron (paoy6v2):
No sweat. lol. Yeah I mentioned I was on Fedora but maybe should have been more clear. 

 I pulled d230abf and ran the stock settings test again on 7.2.5. Still ERROR\_DEVICE\_LOST, 3 out of 3, llvmpipe still trains fine. Happy to rerun it when the Linux fix is up.

--- [1] u/PhysicsDisastrous462 (paou6ll):
actually a second to what i just said, this appears to be an issue with how my repo handles vulkan submission on linux drivers! i will definitely be fixing this in a VM with passthrough! sorry about that! I usually work with windows 3;

--- [1] u/PhysicsDisastrous462 (paoswg9):
kimi k3 and gemma4 support have been fully implemented and now verified against both RDNA2 and RDNA3 architectures! im very sorry for the long wait, kimi k3 was definitely a BEAST to tackle!

--- [1] u/PhysicsDisastrous462 (paosr57):
thank you SO much for this! i was just coming back here to tell you all that i just updated the repo to natively support gemma4 and kimi k3, and i had a buddy of mine with a cluster of 6800xt's run some tests and give me very similar info, and i have addressed that too in the latest pushes! things should work for you now. i am very sorry the timing sucked this hard man 3;

--- [1] u/Zito_Kadaken (paopvkw):
You said you don't have an RDNA 2 card, so I ran it on mine. Took about 6 hours, this is what I found. On stock settings it dies on the first step because the amdgpu GPU job timeout is only 2 seconds, and the kernel treats your work as a hang. Raising the timeout gets it training and the numbers match CPU, but long sequences still blow past it. I wanted to try Gemma 3 270M too but ran out of time. The last big test, seq 512 with the timeout at 5 minutes, froze my whole computer and I had to hard reboot at least 5 times, so I stopped there. Hope that helps. I've got the RADV hang reports and all the logs if you want them, just let me know.

What I used:

- RX 6800M 12GB laptop, Fedora 44
- Kernels 7.0.13, 7.1.4, 7.2.5
- Mesa 26.1.8 and 26.2.2 (RADV), plus AMD's old AMDVLK
- SmolLM2-135M, Qwen2.5-0.5B, Qwen2.5-1.5B

At stock settings:

- Builds fine, doctor sees the card
- Step 1 logs a loss of 0.0 (SmolLM2 logs 1.2457 when it works), then ERROR_DEVICE_LOST
- dmesg shows a gfx ring timeout
- Same on the integrated Renoir GPU
- llvmpipe trains fine
- Your logits tool still works, matched CPU within 0.0003

Why:

- amdgpu GPU job timeout is 2 seconds on all 3 kernels
- Steps take about 2 to 3.4 seconds each on this card (seq 128)
- Raising the limit to 4 seconds fixed the light runs, 60 seconds fixed more

With amdgpu.lockup_timeout=60000 it trains:

- 200 steps, batch 4, LoRA all passed, and 3 steps of full training on the 1.5B
- Loss matched llvmpipe within 0.00001
- Same crash and fix on all 3 kernels, bigger RADV runs only on 7.1.4 and 7.2.5

The catch is long sequences:

- Seq 1024 with rows long enough to fill it: one GPU job went past 60 seconds
- Seq 512 with rows long enough to fill it: one GPU job went past 5 minutes
- That card runs one of my monitors, so the long one froze my whole desktop
- So raising the timeout only helps short stuff

Other stuff I hit:

- Your trainer (train) loses the device too, then hangs on a full CPU core instead of exiting
- fp16-storage-parity and fp16-storage-fp16-lm-backward stop on batch 1: "dynamic loss scaler rejected a non-finite optimizer window". Same on llvmpipe, so not the GPU
- AMDVLK: steps about 23% faster (on 7.0.13, vs RADV on 7.1.4), same timeout though. Ran out of GPU memory on the 1.5B, RADV fits it fine


--- [1] u/[deleted] (pagh4id):
[removed]
