# i would like to learn deeply about fine-tuning local models before burning money

- url: https://reddit.com/r/LocalLLaMA/comments/1wu9zkn/i_would_like_to_learn_deeply_about_finetuning/
- id: 1wu9zkn | score: 17 | comments: 49 | created: 2026-09-30T16:46:27+00:00
- author: SignificantZebra5883 | domain: self.LocalLLaMA
- url_in_post: https://www.reddit.com/r/LocalLLaMA/comments/1wu9zkn/i_would_like_to_learn_deeply_about_finetuning/

## SELFTEXT

There's so many new techniques like RL, RL LoRA, QLoRA, CPT LoRA.

I believe i would have a usecase for them, but i don't know where to learn, youtube is filled with bad quality tutorials if i just search and the good channels (fireship, bycloud) don't cover these as they're quite new concepts, i guess?.

  
how can a regular joe like me learn about these concepts in a "practical depth" so i can actually fine-tune qwen 27b successfuly on lets say custom corpus? without spending 100$ figuring out that "oh i didnt even need CPT here" or "well i chose the wrong Rank count! time to start this 2 day run again!"

context and TLDR: im building a legal general purpose chatbot for context, i have a big corpus, but im a bit stuck on what to do next

  
thanks for reading and any pointers!

## COMMENTS (53 fetched, ranked by score)

--- u/DataGOGO (score 22):

First, the training itself isn’t the hard part. Turning your corpus in to a good, clean, properly labeled, and balanced dataset is 99% of the work, AI sucks at it, doing it right takes a long time, and a LOT of compute. 

If you just point Opus at it (or any model really), it will build all kinds of scripted builders, checkers, and verifiers, and you will beat on it for weeks, think you have it right, because the model will tell you it is, then you will train 10-15 times and each time find more dataset errors during evaluation and acceptance. 

Full fine tuning is almost never a one shot deal, at least not if quality matters. Even if you do it all right you will almost certainly go through multiple revisions. 

That said, how big is your dataset roughly? Are you renting the compute for this, or do you have local compute? Have you calculated how much vram you require?

--- u/ttkciar (score 8):

Like Choice_Celery9481 already said, for a general-purpose chatbot you are almost certainly better off using RAG with a good general-purpose model and your corpus in a database.  I have found that Gemma 4 (31B or 26B-A4B) are very good at RAG tasks.  r/RAG is all about RAG, if you want to learn more about it.

That having been said, if you really want to pursue fine-tuning, there are a few good resources that come to mind:

* r/Unsloth is all about training and fine-tuning (albeit focused around the Unsloth framework, which is excellent),

* r/LearnMachineLearning is specifically for learning about ML in depth,

* Huggingface has some really good tutorials which walk you through these concepts at intermediate depth.  Perhaps start here: https://huggingface.co/docs/peft/en/index

Good luck :-)

--- u/DataGOGO (score 5):

This isn't true. You absolutely can embed new knowledge via fine tuning.

--- u/DataGOGO (score 5):

you can completely screw up a model even with a very tiny dataset. 

if you are trying to embed legal knowledge into weights, your odds of messing up the model behavior itself decreases vs other activities.  How big is your dataset? What is your dataset exactly?

You are not going to learn this from a youtube video, or a tutorial. Data Science is a really complex field, and learning how to structure that data, and how to train it is also, extremely complex and nuanced.

--- u/toothpastespiders (score 3):

Yep, it's just hard work and requires some perseverance and understanding of the process. Along with the humility to realize one isn't going to have great results the first try. Or second. Or probably tenth. And I think a lot of people make one go at it, fail, and from that point just assume it can't be done.

I've been training models to "add knowledge" since the llama 1 days. Not saying that the results are mind blowing or anything. But I've gotten 30b size local models from oblivious on a lot of subjects to at least competent.

--- u/SignificantZebra5883 (score 3):

thanks for taking the time. i posted a comment with dataset sizes in the thread.

i have fine-tuned successfuly models with LoRA before but i was kinda vibe-coding and i wanna learn more.

--- u/wllmsaccnt (score 3):

They are asking how to get the knowledge to know when to apply training. Its a chicken-and-the-egg situation for them. They want someone to help them bootstrap their knowledge without spending a bunch of money burning compute just to see

--- u/Choice_Celery9481 (score 3):

personally i think your usecase need uncensored model + rag more than fine tuning

--- u/FullOf_Bad_Ideas (score 2):

Nice that you have a big dataset, most people have like 1 million tokens when they want to start finetuning. It's way easier to prune out stuff than to come up with it!

--- u/DataGOGO (score 2):

Make skills, and RAG it. If that doesn't work, then look into training.

--- u/SignificantZebra5883 (score 2):

Probably not haha, I don't own any local hardware, but I can rent and have a pretty big budget.

I also don't plan to do the whole 20b I doubt it's needed. Claude even recommended doing a CPT LoRA and distill from teacher model QnA training rows from corpus docs.

Now I don't even know if that's a thing which is why I'm making this post, full fine-tune CPT is probably not the way but again I don't know and I don't even know all the options.

--- u/Double_Cause4609 (score 2):

Okay, makes sense.

What I'm going to say: Don't start with legal docs. That's a really specific field, and you won't get it right on the first try. Don't start with a 27B model either. Start with a much smaller model.

You are going to fail.

You want to fail as fast, and as many times, as possible.

Start with a manageable 2B-4B sized model, and focus on just getting it to output in good Polish. This can look like continued pre-training on a polish corpus, this can look like taking questions and giving answers in Polish, whatever.

You will learn way more with 20 runs on a small model for basically free than you would get out of training a 27B once.

A couple of things you'll want to get a feel for:

* What happens if you include a specific type of phrasing in continued pre-training data, versus what happens if you chat template it in the SFT data?
   * How does the model generalize in either case?
* If you do a V1 training run, and run into issues, what could you include in the training data next time to do better?
* How can you make a function that tells you if an answer in your domain (legal, I guess) is good or bad?
   * If you can't make a function to do it, can you train a verifier to figure it out reliably?
* How does your model handle a bad scenario? Like, if you force words in its mouth, and write a scenario where it's already made a mistake, how does it recover from that?

The problem is there's way too much to teach to another person. You really do just have to experiment and start doing it to figure it out. There's a lot you learn along the way.

--- u/sn2006gy (score 2):

Go to amazon and search for "The Hundred-Page Language Models Book" and give that a read over - all the books related are also great to start from.

Your library may have these books, and you may be able to request them if they don't.

--- u/DataGOGO (score 2):

>20B to 24B

Do you have the compute for this?  How are you planning on standardizing and labeling your dataset?

--- u/TheRealJesus2 (score 2):

This is how you should always start in my opinion. Maybe not vector rag specifically but some way to ground the system with factual up to date info as well as a model that doesn’t reject the request outright because you need those things with or without training.

--- u/rmonsurate (score 1):

You realize this is just distilling the original into the pruned + quantized model right? Maple is a fine tune and I calibrated the training data mix to minimize catastrophic forgetting.

--- u/rmonsurate (score 1):

Yes this was my 6th training run result (Victoria)

--- u/rmonsurate (score 1):

Cheers

--- u/bruhhhhhhhhhhhh_h (score 1):

This person has distilled and taken the time to communicate, very succinctly, great information and knowledge.

Good on ya legend

--- u/DataGOGO (score 1):

I mean you can try, but that is a BIG ass Lora

--- u/tomByrer (score 1):

I was wondering if keep making LoRAs the way to go?

--- u/NeilCPA (score 1):

I would start here, it is three hours, but it is actually digestible, then fork into the next layer of understanding. [https://youtu.be/7xTGNNLPyMI?si=BEpTs3pIcRlJJE5s](https://youtu.be/7xTGNNLPyMI?si=BEpTs3pIcRlJJE5s)

--- u/llama-impersonator (score 1):

> without spending $100 figuring out ...

good luck man, i've spent thousands of dollars in the process of learning all this. one thing i can say is that full finetuning is kind of overrated, loras are a lot more forgiving and cheaper for most training runs and can usually handle the data if the rank is high enough, unless your goal is a major architecture overhaul like adding a new modality or grafting different model parts in.

also doing legal stuff is hard mode because there will always be consequences when it goes off the rails.

--- u/TheRealJesus2 (score 1):

Yeah I originally had old school thinking traces (using a non thinking model from the frontier). But that cause more problem than solution so most data does not have that. 

And I mean I am doing retrievals and reasoning over that and have been doing so for 6 months :) I full agree that’s where to start and frankly where most projects should end. I’m trying to learn more tho on ways that make sense to train and the types of problems it can solve. Got the book another person suggested.

--- u/FullOf_Bad_Ideas (score 1):

just do OPD from the base model later

https://thinkingmachines.ai/blog/on-policy-distillation/

And then tune it for the right kind of answers.

This way you can stuff mid-training and knowledge into a model

what is emergent reasoning?

--- u/sn2006gy (score 1):

you lose the emergent reasoning of a model when you overfit.

You are full of bad ideas. :D

--- u/FullOf_Bad_Ideas (score 1):

And how that's a problem? He's finetuning an LLM for a single task of being a legal assistant.

--- u/sn2006gy (score 1):

Chat traces to show behaviors are common to train in, but hard to train in if you're trying to train in the reasoning.

Easier to see if a model can reason over a RAG and get what you want before you try training in anything.

If it's just a style/approach of chat you want, go fine tune away

--- u/sn2006gy (score 1):

That would be way overfit IMHO

--- u/FullOf_Bad_Ideas (score 1):

You can add knowledge, you just need a lot of compute and data. This guy has ~20B tokens of data, he can add knowledge :D

--- u/FullOf_Bad_Ideas (score 1):

I am sure there are guided runbooks for it, lots of them. I know of some but don't want to advertise here and IDK how public they are. But I'm sure there are many of them. I wouldn't use Youtube.

--- u/Objective-Pair8231 (score 1):

HF guides like these one were very helpful to me: 

[https://huggingface.co/docs/transformers/en/training](https://huggingface.co/docs/transformers/en/training)

[https://huggingface.co/docs/peft/en/developer\_guides/quantization](https://huggingface.co/docs/peft/en/developer_guides/quantization)

--- u/Objective-Pair8231 (score 1):

I would check out nanochat by Karpathy. Possibly HF guides like this one: [https://huggingface.co/docs/transformers/en/training](https://huggingface.co/docs/transformers/en/training)

--- u/jjusko20 (score 1):

You may want to look at https://github.com/jackjusko/sftmill

--- u/toothpastespiders (score 1):

Just adding to the choir of people agreeing with you on the datasets. A few recommendations as well from how I go about it as well. 

I put togther a format that's planned around having as much categorize data for every item as possible. Then I script out conversion of that format into whatever format I'm going to be training with. The main point is that it makes it easier to get a subset tailored to specific use. That way I'm not just getting the training dataset, I can also easily leverage it for RAG or anything else with specific criteria. Likewise easier for tracking any ongoing changes. And getting notified of formatting issues. 

>AI sucks at it

Though to stress that point, I force myself to go through the dataset by hand. Godawfully slowly. First with a quick glance method for anything with even a tiny variation from the standard methodology I'd been using. Usually enough to get the glaring issues down. But then actual reading and editing. Just a bit each day to avoid burnout. Partially for factual issues but also for poor writing quality/repetion/slop. With a gui that can at least help a bit with the process with some external tools.

--- u/DataGOGO (score 1):

agreed.

--- u/SignificantZebra5883 (score 1):

Got it thanks. This makes sense.

Claude recommended something similar CPT LoRA on corpus based document QnA that would be generated from a teacher model (fable or opus). 

Now I don't even know if that's a thing you see I feel like I don't even know all the options. I mentioned this on a reply to Datagogo

--- u/TheRealJesus2 (score 1):

Thank you! 🙏

--- u/TheRealJesus2 (score 1):

Yep full agree. And I’m ignorant on training LLMs specifically. I’ve trained classifiers in the past for a few different things with relatively small datasets but we’re talking 100-600 features, not billions lol. 

Here are some concrete answers for a task I have:

1800 chat records with feedback on 10% from people for a chat-based tool I run. Half of those are one turn and a few go much beyond 2. Most of it’s relevant to the use of the tool (2% extraneous requests or nonsense). 

I feed the model with a corpus of 50k natural language objects on demand which can be queried with a tool I provide to LLM. This context is all captured in my dataset. Those objects also require special definitions of words similar to in legal space. And there are natural language rules to abide by which are also fetched on demand. No vector indexes. 

I rely on the model to make the tool call for those objects. That’s one thing that can be improved on I think with training because sometimes it misses or searches for the wrong obj. Also general speed can always be improved so I want to use a smaller model for that reason. 

I cap requests at 60k tokens total so I don’t need big context window or anything so i do think it could work well for a smaller model esp with some fine tuning. Just not sure which aspects are worth fine tuning on…the glossary? Existing chat records? The 50k obj themselves? I generally think capturing knowledge like those rules is wrong because it can change and same with the 50k objects unless it also improves ability to call my speech tool to do so or adherence to instruction from prompt, user, natural language rules, etc. But I’m lacking the framework to think this through.

Where I am starting is just to build out better evals because I need that either way. And looking at where there was friction for the user to spot where I can improve the model itself 

All advice appreciated including “this is dumb and you won’t get any benefit because X”

--- u/sn2006gy (score 1):

You can shove shit into a model by fine tuning, doesn't mean you should.

Fine-tuning is often best at teaching:

* format
* style
* behavior
* decision rules
* task performance

When you shove shit into a model that isn't format/style/behavior/decision rules/task performance, you start altering the base knowledge and over fitting and you lose emergent behavior which leads me back to the original premise.

--- u/SignificantZebra5883 (score 1):

thank you very much, you seem knowledgable in this field. i will definitelly read the docs, even if it will be cumbersome.

i posted a comment in the root of this thread, with my corpus.

i geniuenly think i need finetuning of some sorts not prompting or RAG, because the agent will be in polish (small language) and will need to learn complex polish law reasoning in order to even know what function calls to run (yes RAG is still in the picture)  
  
or complex court decision summirazion (i LoRA'd this successfuly actually, but i was half-vibecoding and didnt 100% understand parameters like Rank Rate of learning or whatever, so thats why im asking for resources) 

Asking on reddit feels way more like a shortcut, you guys literally distill knowledge into me, way better than docs, but i was hoping theres some resource (like bycloud he's really good)

but again, i dont even know where to start cuz theres so many methods, i feel like i need to load them all in my head to know in which direction i wanna take the project and models, and like i said i would have to do a lot of reading (im scared and as i said i feel like theres more efficient ways to distill into my head, maybe i will use AIs help to learn idk)

--- u/DataGOGO (score 1):

Agree completely.

--- u/SignificantZebra5883 (score 1):

thanks for taking the time.I know very well about RAG, im not after RAG anymore i feel like i understand it well.   
  
 i posted a comment with dataset sizes in the thread. could you please check it? thanks!

i have fine-tuned successfuly models with LoRA before but i was kinda vibe-coding and i wanna learn more.

--- u/SignificantZebra5883 (score 1):

thanks for all the answers!

I am very well familiar with RAG and its benefits and drawbacks and i for sure wanna do fine-tuning yes, but again, i wanna learn about the techniques better like CPT LoRA and RL LoRA for example.



here is my corpus (unstructured, uncleaned)

AI:

Legal commentaries and textbooks come to about 770M characters. That is roughly 250M tokens.  
Legislation comes to about 170M characters. That is roughly 55M tokens.  
Court decisions stored locally come to about 71 GB of text. That is roughly \~22B tokens.

In total, about 3.6B tokens are available locally, and about 20B to 24B tokens including cloud storage.

These are estimates at about 3 characters per token, not measured counts.

--- u/no_witty_username (score 1):

Chat gpt is your friend learn from it. Also most people who have dealt with fine tuning will tell you its not worth it and whatever you want to do most likely can be done with in context learning. Fine tuning is costly and usually only needed for very niche cases and the advantages don't last long enough to justify the effort. Also most likely there's already a fin tuned model for whatever you need so search those first.

--- u/rmonsurate (score 1):

Strongly agree with this take in general. Spend more time on dataset than technique, however, some papers, given the same excellent dataset, can enable material gains in post trained performance. See QAD from Nvidia which is what I used recently when making a QFN fine tune.

--- u/TheRealJesus2 (score 1):

Have a rec for book? I’m getting to the point with some projects to consider training as I am generally against training LLMs because I never run anything at the scale to necessitate the complexity there lol. But I want to learn more and my knowledge foundations here are shaky. I’ve built 
datasets for clustering and classifiers in the past so am aware that the work is mostly data curation 😂

--- u/Double_Cause4609 (score 1):

So, part of the problem is "what am I trying to solve?"

Do you want your model to have knowledge?

Specific reasoning patterns?

To perform well on a set of problems you can verify the solution of?

To have a specific style of output?

These things all point to different solutions. For knowledge, usually you don't want to finetune, because it's better to have the knowledge in context. This points you more to things like embedding similarity RAG for style, knowledge graphs or RDBs for conceptual relationships and semantic content, and some sort of rolling summary pattern for autonoetic memory.

For reasoning patterns, you might want to finetune...But you should probably test a lighter weight option like a DSPy optimization run (they're a lot easier than traditional training and get you surprisingly close).

If you want to do well on a set of problems you can verify, you absolutely can do RL...But most of the benefit of RL is captured by online learning in general. You can actually take a problem, generate a number of solutions to it by the model, evaluate the solutions, and train on the highest performing ones. This is precisely RAFT/rejection sampling, and it's very similar to RL in performance when done right. But, online methods only capture what the model can already do, and just makes it more reliable at finding those solutions.

For style of output, you're honestly best off getting as close as you can with prompting, and then training a very lightweight LoRA adapter to adjust the style the last mile. Usually this is done with an SFT objective.

So, to recap more or less:

To introduce new general knowledge and capabilities: CPT is usually what you want, but read LoRA without regret first before deciding if you need FFT or LoRA.

To introduce a new style or values: SFT can be sufficient as an objective, but it's better with some preference optimization or RL (you can do RAFT if it's easier, though online DPO is also good).

To improve reliability on things the model can already do well sometimes: Turn to RL or online learning methods in general.

If your target policy is captured well by prompting (you should verify if it is, first), don't finetune, just do a DSPy optimization run.

If your target is captured well in a small number of tokens (hundreds of thousands to low millions), or is captured well by online methods, do LoRA.

If your target is far from the model's existing behavior, you may need full parameter fine tuning.

Where to learn about this? Arxiv. Find an interesting paper, look at its references, read those, read the references in those, and you'll get there eventually. Read the Axolotl and Unsloth docs. Read the DSPy docs.

--- u/TheRealJesus2 (score 1):

How big of a dataset do you need for actual change to a model behavior? 

Better question maybe…how do you reason about that question given different model sizes, architectures, and data set sizes? 

Any good sources I can read to learn more? Outside of hyper specific papers on specific techniques. Looking to understand from the higher level when to apply different techniques

--- u/sn2006gy (score 1):

This is partly because you never asked Opus if you should have done this to begin with :)  Fine tuning never really teaches an existing model usable data, it teachers behaviors,

This is also the major shortfall of all models; they never tell you what you don't know and I won't call it "AGI" at all until they act like experts.

--- u/sn2006gy (score 1):

Fine tuning is more about behaviors than adding knowledge.  There are good books about LLM engineering i'd start with vs jumping into videos.

--- u/purple621 (score 1):

I second this. RAG. I recommend bge-m3 it does keyword match AND semantic search

https://huggingface.co/BAAI/bge-m3

Just aks Opus 5.5 how to build your usecase

