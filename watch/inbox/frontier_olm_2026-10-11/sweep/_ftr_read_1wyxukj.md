# THREAD 1wyxukj

title: How do you decide whether to trust a community fine-tune?
subreddit: LocalLLaMA
score: 3
num_comments: 15
created_utc: 1791277670
author: AdFickle8681
permalink: /r/LocalLLaMA/comments/1wyxukj/how_do_you_decide_whether_to_trust_a_community/

== SELFTEXT ==
I'm researching how people choose and vet fine-tunes and merges from Hugging Face. I'm not selling anything. I just want to understand what people actually do.  
	1.	Where do you find the models you try?  
	2.	What do you check before you start using one (benchmarks, model card, reviews, your own test prompts)?  
	3.	Has a fine-tune ever behaved worse than its base model? For example, odd refusals, lost reasoning, strange outputs, or things it should not say. What happened?  
	4.	If a quick side-by-side check of a download against its base model existed, would you use it? What would it need to show?  
Short answers are great, and stories are even better. Thanks!

== COMMENTS (15 fetched) ==
--- [8] u/Practical-Collar3063 (pe6p5qj):
Most of us have a small personal benchmark that we use to try new models, fine tunes or quants to determine how they behave for our use cases.

Regarding this:
> 
3. Has a fine-tune ever behaved worse than its base model?

Yes, massive yes. Most community made fine tunes perform worse overall than the base, it is super hard to make a good fine tune of a model that is not benchmaxxed

--- [4] u/peligroso (pe7adww):
> are there any public benchmarks you actually trust

No.

> trust for this

For community fine-tunes? Definitely no.

--- [3] u/jacek2023 (pe6r3ov):
After running some models, you start to recognize the authors, so you know which ones produce useful finetunes and which models are shit. Then you follow the good authors, just like you follow Instagram profiles for example.

--- [2] u/JudgmentAdorable268 (pe6r90x):
i just throw my usual roleplay prompts at em and see if it holds the scene without random refusals or losing the vibe that the base had. had one merge that got way more prudish outta nowhere and it killed the fun quick.

--- [2] u/AdFickle8681 (pe6qhy9):
Not full of shit at all, that's a fair point, and no flaming here. I'm asking about LLMs because I'm looking at the "download a community fine-tune and just use it" side of things, not training. A solid wrapper or character prompt definitely covers a lot.  
One thing I'm curious about: when you swap the model underneath the same agent setup or character, how do you find out whether it still behaves the way you need? Do you just notice when something breaks, or do you re-run some checks first?

--- [2] u/AdFickle8681 (pe6q1hp):
Thanks, this is really helpful. Your personal benchmark is exactly the kind of thing I'm trying to understand. What kinds of tasks are in it, roughly how many prompts, and how long does it take you to run on a new model? Also, are there any public benchmarks you actually trust for this (or ones you've stopped trusting because of benchmaxxing)?

--- [1] u/JLeonsarmiento (pe7ezzb):
I have 5 complete tasks I put them trough within Pi. 

--- [1] u/[deleted] (pe6z1l1):
[removed]

--- [1] u/PaulCoddington (pe6uyym):
I keep a table of results for various models where I score quality of responses to a fixed set of questions that cover multiple topics and skills.

The idea is to quickly sort into "creative" vs "programming" and "personal assistant", and to quickly eliminate poor performers, while not accidentally testing the same model twice over the long term.

e.g.

"Write a haiku about an octopus."

(Is the syllable count correct? Does the haiku end at the expected length or carry on for multiple paragraphs?)

"Speak like a pirate."

(Can it do the most basic accent test similar to "Speak like a Pirate" day? Does it really speak like a pirate or just introduce itself as "Jack Sparrow" and quit?)

"Roleplay as a cockney housemaid from East London in the 1930's. Describe your day off spent visiting a circus."

(Is it speaking with a Cockney accent? Does it have personality? Are there details about the employer, the housework and the reason for the day off? How good is the storytelling of attending the circus and describing the acts, such as details and actions of animals, acrobats, clowns, ringmaster, etc? Are there anachronisms?)

"Write a Powershell script that exports a text file that lists all files in the current folder alphabetically."

(Is the code valid? Are there extra safeguards and error handling or just bare basics? Is the solution elegant or somewhat unconventional or overblown? Is the code well commented?)

"Write a short story about a girl who stumbles across a flying saucer in the woods."

(Is the description of the character, settings and events rich, engaging and original? Does it just fall back more or less on a default story and person name typical for the model family? If so, does it do better or worse with details and embellishments?)

(Include above story) "Write the entry the girl wrote in her diary later that day."

(Does it read like a diary entry? Has the narration changed to first person? Do the details, events, descriptions agree between short story and diary entry?)

--- [1] u/LosEagle (pe6uv1x):
I don't but I like to read DavidAU's model cards when I'm sad or depressed to make my day better.

--- [1] u/EverythingIsFnTaken (pe6s9zu):
Oh, in that case, yes, you will sense a difference in two models playing the same role in silly tavern, for example. But it will be subtle, and contingent upon their original trainings and the differences that were already present, if not difficult to describe. 

Like, smaller models/quants will still be susceptible to the same sorts of looping and saying things that are bullshit as they ever were to begin with due to those things, but I feel like it will be pretty much what you would expect from models you were familiar with, just with added flavor. In the silly tavern example, at lease. 

An agentic wrapper I reckon is much more focused and perhaps less liable to fail in aforementioned ways, based on a thoroughly explicit and unambiguously verbose manner that tells it what it's expected to do and how it's expected to behave down to the last letter. Such rigorous instructions might. keep it's head on straight, keep it from losing train of thought, doing an overall great job at it's task, but still do a shitty job because it didn't know how to code as well as it would like to believe. Which, if you're already familiar with your model in the example you'd have not been surprised to see the mistakes while having seen the harness do what it was supposed to.

This I reckon is why we allow agents to delegate tasks and have layers of approvals before things in the workflow move along the conveyor belt, but it's all a little sketchy at the end of the day.

hopefully any of that was helpful at all, I'm not low right now., lol

--- [1] u/JLeonsarmiento (pe6pdvb):
Just by testing the damn thing. 

--- [0] u/AdFickle8681 (pe6pmn8):
Ha, fair enough. What does your testing look like? Do you have a set of prompts you always run, or do you just chat with it for a bit and see?

--- [0] u/ilintar (pe6p7et):
Monthly repost:

[https://www.reddit.com/r/LocalLLaMA/comments/1va4i9e/ilintars\_official\_guide\_to\_model\_selection/](https://www.reddit.com/r/LocalLLaMA/comments/1va4i9e/ilintars_official_guide_to_model_selection/)

--- [-1] u/EverythingIsFnTaken (pe6q5z3):
Am I the only one who finds it unusual to make these inquiries about LLMs? Like, instead of diffusion models and whatnot. This is pure conjecture but I feel like outside of abliteration, there is little interest for further messing about with models that are likely going to be functioning under thoroughly described wrappers and shit, whether that be an agentic wrapper or a character role the model will portray, I feel like the particulars are sorted out and learned from/remembered from there within those contexts respectively. 

I'm totally prepared to be absolutely full of shit, so don't flame me too hard, folks, lol
