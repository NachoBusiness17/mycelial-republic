# ImaJev-4b: I spent 15 days fine-tuning a 4B model to make business decisions from text and photos, and it just ranked #1 of 91 on JevBench & ahead of GPT-5.6 Luna on DecisionBench

- url: https://reddit.com/r/LocalLLaMA/comments/1wsgrma/imajev4b_i_spent_15_days_finetuning_a_4b_model_to/
- id: 1wsgrma | score: 198 | comments: 61 | created: 2026-09-28T14:53:36+00:00
- author: Educational-Care7867 | domain: reddit.com
- url_in_post: https://www.reddit.com/gallery/1wsgrma

## SELFTEXT

**Some context first.**

I am process improvement / business consultant and had worked with Fortune 500 companies on improving their processes around refunds, returns, customer support, etc.

This entire thing had a lot of complex decision making and generally every decision / condition node in a process map was generally replaced by a human because factoring in ambiguity in a code is very difficult.

**Idea of ImaJev**

Hence, when Jev came out, I was very intrigued with it and also could clearly see its use-case of improving decision making in complex decision work flows.

However, Jev didnt have support for Images and I thought that it can be replicated for both Text and Images in a single model and thats when I started with ImaJev.



**Training Process**

It went badly at first. My first big fine-tune on about 500k short decisions made the 9B model worse at reasoning: 64.9 down to 42.3 on JevBench hard. It had basically learned to pattern-match. I spent the next couple of weeks generating hard questions with open-weight models and only keeping the ones where two Ai models agreed on the answer. That brought it back.



**Results**

Then, on the JevBench - It came out **#1 of 91** (v1.4.2.2, scored 27 Sep), 67.37 vs Jev 1.13.0 at 63.29.

The same week DecisionBench put it **#3 of 56**, ahead of GPT-5.6 Luna and DeepSeek V4.1.

I honestly didn't expect either.

To be fair about it: the #1 is on a score that weighs accuracy, calibration, speed and cost equally. On accuracy alone it's #3. Its main strength is that when it says 90% it's usually right, and it'll say "can't tell" instead of guessing.

**What it actually is**: LoRA plus a small decision head on Qwen3.5-4B. You give it text or a JSON record, up to two photos, and closed questions.

It gives back a probability for each option plus "unknown", in one forward pass.

Runs on a Mac with MLX or on one GPU. 

The whole project costed me around $1200 in rented GPU and a lot of time :P

* Weights (Apache-2.0): [https://huggingface.co/mohit67890/imajev-4b](https://huggingface.co/mohit67890/imajev-4b)
* Code: [https://github.com/mohit67890/imajev](https://github.com/mohit67890/imajev)
* Demo: [https://huggingface.co/spaces/mohit67890/imajev](https://huggingface.co/spaces/mohit67890/imajev)
* JevBench board: [https://benchmarkheaven.com/jev-models](https://benchmarkheaven.com/jev-models)
* DecisionBench board: [https://huggingface.co/spaces/Hanno-Labs/decision-bench-leaderboard](https://huggingface.co/spaces/Hanno-Labs/decision-bench-leaderboard)

I would love to know your thoughts on it - it anyone would be interested to try that.

## COMMENTS (69 fetched, ranked by score)

--- u/Educational-Care7867 (score 52):

Yes, I was reluctant at first :P

But, then I realised that I dont have money to keep this moving - so open-sourced everything.  
[https://mohit67890.github.io/imajev/report/](https://mohit67890.github.io/imajev/report/)

--- u/Educational-Care7867 (score 26):

Its very fast..

45ms for text and around 120-140ms for Images

--- u/ContributionOwn4879 (score 19):

Think to add a grab me a coffee link. And try to send your model on the decision index :   
https://huggingface.co/spaces/multimodalart/jev-decision-index  
If you really beat jev with only a 4B model, it’s awesome !

--- u/kokassospoperor (score 13):

And the speed?

--- u/parabellum630 (score 9):

On what gpu.

--- u/Educational-Care7867 (score 9):

Its 100% type-safe..

On DecisionBench (23,900 questions) imajev-4b answered all 23,900 with 0 errors, same as Jev 1.13; for comparison GPT-5.6 Luna had 10 and DeepSeek V4.1 Flash 48. On JevBench's sealed set it's 308 valid answers, 0 failed or invalid.

--- u/kokassospoperor (score 9):

It looks very promising

--- u/Educational-Care7867 (score 8):

H100 primarily.

--- u/DataGOGO (score 7):

nice. Did you publish your datasets?

--- u/Educational-Care7867 (score 5):

Hi, Its working now - sorry for the glitch.

https://preview.redd.it/71iqcgg1absh1.png?width=3816&format=png&auto=webp&s=f710c3ab75c776ad63f83efabe15d82dc4789d64

--- u/Educational-Care7867 (score 5):

Btw, this model just scored #1 on the Image JevBench as well. I will write about it separately but this is absolute best in terms of images

https://preview.redd.it/wlwz1peh9bsh1.png?width=3522&format=png&auto=webp&s=bf4ab0786cf587ecb600c393e3d28416a1e9b468

--- u/Educational-Care7867 (score 5):

4xH100 primarily

--- u/Educational-Care7867 (score 5):

Yes, I will add that link which maybe help me further improve this. 

I saw this Decision Index man - 120K+ tests. 
This will take hours on H100 GPU. 

Hence, I skipped it. But let me recheck it.

--- u/Educational-Care7867 (score 4):

You can increase candidates in the readout as much as you like but I havent tested it..

It has 255 candidates  
1 us Unknown be default wherein it can say clearly that "I dont know / I cant tell"..

Hence, 255 is something usable, 1 is just adapter default.

--- u/Educational-Care7867 (score 3):

Ideally you can do it..  
It is 16bit at the moment and I havent tried 4-bit/8-bit version of it..

I would need to reassess its accuracy and calibration then because the current calibration is tuned for the 16bit..

Its doable but will require some work.

--- u/Educational-Care7867 (score 3):

I think this isnt mobile-friendly...  
Please check with desktop / laptop once - this is controlled by Hugging face though.  
Me having little control on it

--- u/Educational-Care7867 (score 3):

Honestly, I don't know yet. All the training data and every benchmark I've run are English, so it's officially English-only for now.

The base model (Qwen3.5) is multilingual, so it'll probably still work to a degree in other languages, but I haven't measured it and I also think that there is a ceiling on what you can achieve with a 4B model.

I'd expect the probabilities to be less trustworthy there even when the answers look right.

--- u/Rarder44 (score 3):

How does it perform in languages other than English?

--- u/epelc (score 3):

Any info on what gpus you rented for the training run and how many?

--- u/Educational-Care7867 (score 3):

In a real world scenario - 255 is more than enough in my opinion..

But, if anyone wants to do it then they can try it

--- u/knownboyofno (score 3):

This is great. Would this work with more decisions then the 256 it has now?

--- u/DataGOGO (score 3):

very clean work.

--- u/mxsonwabe (score 2):

interesting, love to see more of these pop up

--- u/Last-Health3222 (score 2):

Nice, the record-vs-photo-only split is a better cut than mine: when a record is attached it carries most of the signal, so those requests behave like text. 0.029 to 0.012 on 823 items is a clean result. Did the new bucket change any auto-approve decisions at your threshold, or only the reported confidence?

--- u/Enragere (score 2):

Very odd, I reloaded like 6 times just to get to the white screen, and even that is broken. Something is off. Maybe not mobile friendly?

https://preview.redd.it/22geikykkdsh1.png?width=1344&format=png&auto=webp&s=5c9920f7536edc7d372de685b67a9be2fb90e0a5

--- u/Educational-Care7867 (score 2):

This is really helpful, thanks for testing it properly!

Btw,

\- The 4096 limit is just the default of --max-input-tokens (training used inputs up to 4096 tokens). You can raise it, e.g. --max-input-tokens 8192, but anything past 4096 is less tested, so treat those answers with a bit more caution.

\- --fast records CUDA graphs at load for a set of input lengths up to --max-input-tokens, and each one takes memory, which is why it went OOM on 6 GB. If you want to try it, lowering the cap should shrink that, e.g. --fast --merge-lora --max-input-tokens 2048. No promises it fits, but that's the lever.

\- --merge-lora saving memory makes sense: it folds the adapter into the base weights instead of keeping both. It can flip the odd near-tie decision because of bf16 rounding, but it's what the official Image JevBench run used.

On llama.cpp: not yet. The model doesn't generate text. A small trained head reads the last hidden state and scores the options, which llama.cpp doesn't do out of the box. It's possible in principle (merge the LoRA, convert to GGUF, pull the hidden states and apply the head outside), but it hasn't been built or tested, and quantization would need a fresh calibration check. If more people want it, I'll look at it.

Would love to hear how the quality holds up once you go past smoke tests.

Lastly, I have spent more time with 4B than 2B honestly..

Also, images of 4B is ranked #1 on Image JevBench now and 2B being at 6th

https://preview.redd.it/gb62q3q5gbsh1.png?width=1600&format=png&auto=webp&s=5869de1e8064479d3a68623f85a7da41168f4685

--- u/Last-Health3222 (score 2):

Read the calibration section. Since you found the photo-only path is already well calibrated raw and the single temperature over-softens it, why not fit two temperatures, one for text-only requests and one when an image is present? It's cheap, and it matters once you auto-approve above a confidence threshold and send the rest to a human. Did you try it?

--- u/Educational-Care7867 (score 2):

Thanks! Honest answer: not yet. It loads in 16-bit on GPU, and the decision head plus the calibration were fitted at that precision, so I haven't shipped or measured a 4-bit/8-bit version.   
  
Quantizing might shift the probabilities, and those are the main point of the model, so I'd want to measure it before recommending it.

For 6 GB VRAM, the 2B is your best shot: its base weights are about 4.6 GB in bf16, so it may fit for text and short requests, though images add memory and I haven't tested a 6 GB card. It's also a step down from the 4B (about 72% vs 84% on our image benchmark).

If you try either, I'd really like to hear how it goes. And if a few people want it, an 8-bit build with a proper accuracy check is next on my list.

--- u/Educational-Care7867 (score 2):

Let me check and update. Thanks for letting me know

--- u/Enragere (score 2):

Demo link doesn't work, 500 error code

--- u/Educational-Care7867 (score 2):

I think my model cannot beat the intelligence and accuracy of these 30B models - impossible..

but, I will give it a try and report it.

But, my model has very high calibration and can run locally too - which makes it good for all kind of tasks

--- u/OsmanthusBloom (score 2):

I'm also interested in how ImaJev performs on the Jev Decision Index. On the surface it looks much harder than JevBench, basically all the top models are \~30B.

--- u/_bachrc (score 2):

impressive, great job

--- u/Educational-Care7867 (score 1):

Thankss.

--- u/forevergeeks (score 1):

One thing I'm still trying to understand.

LLMs generate text token by token, sequentially, and their output is inherently probabilistic. So when people talk about a "System 1" model being more deterministic, what is actually different at the architectural level?

Is the System 1 model still generating tokens sequentially, or is it operating more like a deterministic decision function where the same input produces the same output?

In other words, what makes a System 1 model more deterministic than an LLM if both are ultimately neural models?

--- u/forevergeeks (score 1):

I'm using Jev API. 

But I do really see the potential in this technology. 

I would say that classifiers will be as critical as the llms themselves.

I don't think most people have caught up of what Jev actually is, and the problem it solves.

--- u/Educational-Care7867 (score 1):

Ahh, then it would be tough..  
Try hosted API endpoints then

--- u/forevergeeks (score 1):

I don't have the hardware for running these models. I have a Lenovo laptop with 32 GB of memory and decent CPU but no GPUs.

--- u/Educational-Care7867 (score 1):

Laya is very small model..

You can use mine and maybe let me know your thoughts on the same..  
I think it should give you some superior experience

--- u/forevergeeks (score 1):

I just tested Laya in a CPU, and as our friend Richard Stallman would say "Laya is not Jev" 

I don't know what these people are putting in these open source models, but is not usable yet.

--- u/Educational-Care7867 (score 1):

There is almost 1.2 Millions dataset that it is trained and evaluated on. 

I cannot get real enterprise dataset which is confidential and the tech is new - which means I have to sell this idea to them and then evaluate. 

I agree benchmarks cannot meet the real world but since its soo new - I dont have something concrete to answer your questions. 
But, benchmarks are my best option to tell everyone that it is good.

--- u/Future_AGI (score 1):

ranking #1 on the benchmark and holding up on the actual refund and return decisions you built it for are two different bars, and your Fortune 500 process work is exactly what would expose the gap. Have you run it on a held-out set of your own past cases where you already know the right call, separate from JevBench?

--- u/Professional-Mine681 (score 1):

this is wild haha

--- u/Educational-Care7867 (score 1):

Just the confidence..  
There isnt any auto-approve in it as such, other than an unknown / I cant tell feature which just flag out that there is not enough evidence to produce the right result.

--- u/_bachrc (score 1):

I was just curious because I read others models like Luna had 0,5% errors, and Jev 0, and I wondered what was the state of the new open sources models on this

--- u/Former-Ad-5757 (score 1):

What is the problem you see with "typesafety"/ tool calling errors? Every system one model should handle this 100%, as it is handled by deterministic code, the model needs to generate 1 token with probabilities, then hardcoded code, should transform the single token to the response json.

You can output as much (/every format) you want, as long as it is hardcoded then it will 100% return the form. The model part is non-deterministic, but withstanding llm-errors you will always get a good tool call back.

--- u/astral_bear (score 1):

Any change of producing an ONNX or GGUF version for this? Is it even architecturally possible? Thinking this could run decently on CPUs with int8 optimizations quite decently.

--- u/Educational-Care7867 (score 1):

I didnt spend a lot of time with 2B though. 
But based on my benchmarks, it is same as 4B on easy and Medium complexity. 
But when it comes to hard questions, it lags behind. 

If 4B is 84% good then 2B is at 72%. 

Also, on the images side, 4B is #1 on Image JevBench. 
2B is #5 there.

--- u/Educational-Care7867 (score 1):

A lot of public datasets that are available else using a higher model like Qwen 27B or 35B to create synthetic dataset for it.

--- u/Same-Ad7128 (score 1):

# ImaJev-2b  What level is this approximately? I'm also trying to build a 2B parameter model, but the results haven't been ideal.

--- u/KingGongzilla (score 1):

Where did you get the data from?

--- u/Educational-Care7867 (score 1):

Did it just now.   
  
You were right that the photo path is over-softened, but "image present" isn't the split. **Images that come with a record** want the same temperature as text (about 1.3).   
  
The ones that are calibrated raw are photo-only requests, an image with an empty state. On 823 photo-only verification items, raw ECE is 0.015, the shared temperature pushes it to 0.029, and a temperature of 1.03 brings it to 0.012.   
  
A single pooled image temperature changed nothing on the benchmark, so I didn't comminut that.   
  
What's done is a calibration file with a photo-only bucket the server uses when a request has images and no record; every other thing is unchanged.   
  
Thanks for the push, it was a good catch.

--- u/Educational-Care7867 (score 1):

No, I didn't, and you're right.   
  
it has buckets by question type and option count, but not by modality, so an image request gets the same temperature as a text one. The photo-only caveat in the card (0.038 raw to 0.062 with the temperature) was measured on the previous adapter and I haven't re-measured it on the current one.

I'll fit two temperatures on the held-out sets, text-only and image-present, and report the ECE split for both paths.   
Will post the numbers here when it's done.

--- u/Educational-Care7867 (score 1):

Yes. Its made for this

--- u/tomByrer (score 1):

Can this help with photo classification/tagging?

--- u/OsmanthusBloom (score 1):

I managed to get the 2B version working on a 6GB GPU. It takes around 5.4GB VRAM. I was able to process requests with images or with longer text. It refused when the input length was above 4096 tokens, but VRAM usage seems unaffected by input size.

I tried `--fast` but that led to CUDA OOM. `--merge-lora` reduced VRAM usage to 4.8GB and made it a bit faster (1.1s with `--merge-lora` vs 1.4s without, for a longish text-only request).

It's too early to say anything about quality yet since all I did so far was smoke tests. Anyway this looks very promising!

I would like to know if it's possible to run this with llama.cpp in the future. That would open up opportunities for quantization.

--- u/Educational-Care7867 (score 1):

Hahaha. Let me know what you play with it.

--- u/bartskol (score 1):

Time to play with JEV Thingy then.

--- u/bonerfleximus (score 1):

I think theres an approach published in Typesafe docs for using multiple questions to achieve this

--- u/OsmanthusBloom (score 1):

I'm going to try it soon!

Is there a way to run it quantized to e.g. 8bit or 4bit or does it always require full 16bit precision? I have 6GB VRAM on my laptop. I think the 2B one could fit but 4B is too much unless you quantize.

I already tried CLM 8B, using llama.cpp and Q4_K_M quantization for the Qwen3-8B embedding. It worked but quality wasn't very good.

--- u/knownboyofno (score 1):

I know but that was something that would be an advance for this model. I am not sure how many people have more than 255 candidates tho...

--- u/Hopeful_Bug_1245 (score 0):

I suggest you actually do some testing of your own before you make any conclusive statements, because open source jevs are very much usable and people do understand quite well how it works, or at the very least, mimicked their internal architecture to the point of being on par if not better than jev. Idk if you're astroturfing but here are my own findings:

I tezted Contrastive Language Model (CLM) with an Nvidia L4 GPU on Modal (Cloud hosted GPU)

I mimicked their chromium dino game benchmark setup and achieved an avg latency of 80ms, and as low as 2ms. On their report they claimed 15ms avg latency on a 4090. Really fast model with comparable accuracy. 

All with $0.8 per HOUR of usage. (Or you know, completely free if u have access to a strong GPU)

Still using L4, Imajev was able to classify 500 images (not text) across 16 categories in 2 minutes (~200ms).  Astonishingly high accuracy for the ones it didn't flag as uncertain. Skips the entire LLM image vision + embedding layer. 

Total cost for 500 pure image classification is $0.026. and again, free with a strong GPU. idk about you, but it's jev who has some catching up to do.

--- u/Educational-Care7867 (score 0):

Yes. Calculating pensions and other complex calculations with insurances for the same can be replicated at some level.

--- u/XiRw (score 0):

Actuaries are about to be put out of business too soon in the near future

--- u/_bachrc (score 0):

Quite interesting, thanks a lot for your efforts! What about the tool calling errors? It semt like Jev had near zero errors in tool call or answer "typesafety". Is this metric somewhere in the benchmark?

