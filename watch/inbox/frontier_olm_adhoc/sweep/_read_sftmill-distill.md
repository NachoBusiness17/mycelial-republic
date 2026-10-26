# SFTMill: Easily [off-policy] distill any existing LLM with an OpenAI Compatible Endpoint. Turn any behavioral goal into a comprehensive dataset.

- url: https://reddit.com/r/LocalLLaMA/comments/1wtqpjt/sftmill_easily_offpolicy_distill_any_existing_llm/
- id: 1wtqpjt | score: 11 | comments: 10 | created: 2026-09-30T00:22:53+00:00
- author: jjusko20 | domain: i.redd.it
- url_in_post: https://i.redd.it/djne5o4nwjsh1.png

## SELFTEXT

Hey guys - half a tutorial/guide, and half an I built this. This is something that I created for myself recently when I couldn't find any good existing solution. I wrote this post myself, no AI!



Probably a fair number of you have seen my posts about fine-tuning AliceAI 80B A3B according to my own synthetic datasets. If you did, I'm still fine tuning it on a live stream right now - check out [https://figure-bios-expect-cio.trycloudflare.com/](https://figure-bios-expect-cio.trycloudflare.com/) \-- it'll let you inspect any and all of the training data that I generated. If you have any interest, it's pretty neat!



That thread was at [https://www.reddit.com/r/LocalLLaMA/comments/1wslgkw/comment/pcw4kgw/?context=1&screen\_view\_count=1](https://www.reddit.com/r/LocalLLaMA/comments/1wslgkw/comment/pcw4kgw/?context=1&screen_view_count=1)



That run is using off-policy distillation, and that's I made this for. my training data for that project with this repo, and just customized it for an OSS release. Basically, you create a "curriculum" for your goal - e.g. if I was training an agentic model, I'd need things like tool calls, bug fixing, working in a workspace, tracing errors, etc. You define your curriculum in a yaml file, then an LLM creates tasks based on the curriculum you defined, and the chosen LLM you're distilling from then solves each task, leaving you with a full Q/A set that encompasses your fine tune goals.



I used qwen 3.8 27b on medium to generate the tasks - I'd recommend avoiding anything any weaker than that.



I forked my private repo of this that I've been using into SFTMill, which is basically just the same thing with great documentation and a few steps added to get anyone onboarded rapidly. I created it \[and my original version\] because I couldn't find any existing pieces of software made with this design, for this purpose.



I release it because I enjoy contributing to the community, and there's a vague hope someone will eventually see one of my pieces of work and want to hire me (if you're reading this and you like the project and you need a software/ml engineer remote or in NYC, let me know <3). It makes me happy when my software helps others so I'd love if you let me know if it helped you. Cheers!

Shoutout u/FullOf_Bad_Ideas for helping me with my alice train in areas I wasn't experienced enough in - I threw a Multi-Turn Hybrid-Reasoning (`user <> assistant`) section in the readme just for you bud, hope it helps.

[https://github.com/jackjusko/sftmill](https://github.com/jackjusko/sftmill)

## COMMENTS (10 fetched, ranked by score)

--- u/son-of-chadwardenn (score 3):

I figured it wouldn't be easy but I'm wondering if it is the strategy the local llm community will turn towards when companies decide to turn off the free model buffet.

--- u/Dany0 (score 3):

How do you handle censored CoT (Opus 5.5 for example)?

--- u/jjusko20 (score 2):

A full distillation is a big task, but you could probably do a QLoRA with this and get a decent train relatively easily.

--- u/son-of-chadwardenn (score 2):

This makes me curious. People are worried that their favorite smaller model like qwen 35b is getting phased out. How expensive and difficult would it be for a person or small group to distill a 35b model using one of the larger open models hosted on a cloud API?

--- u/HVACcontrolsGuru (score 2):

Let me know! I'm happy to collab and mainly do this for the love of the game haha. Working on some updates here this work for the competition stuff but plan to push this work a lot further once I get some more training runs in place on Modal!

--- u/jjusko20 (score 2):

Thanks! And no problem. Maybe we could collab on a merge later on, our software fits together very conveniently

--- u/HVACcontrolsGuru (score 2):

I've been tinkering around a bit with distillation as well: [Ghostwriter](https://github.com/jscott3201/ghostwriter-rs) I'll have to deep dive this work of yours some more but if you don't mind I may roll some of this into my work and credit you as needed and link back if that works! Doing a Kaggle competition to get Gemma to be a cracked out coder with the 31B model. That goes good I'm going to move to the 12B model and push that work down as well.

Nice work!

--- u/jjusko20 (score 1):

I mean, strong Chinese models like DeepSeek 4.1 and glm 5.2 exist, you'll be able to make good distillations from those

--- u/jjusko20 (score 1):

I don't unfortunately - the model you're distilling from needs to release CoT in its endpoint.

--- u/jjusko20 (score 1):

Good luck let me know as well 🫡

