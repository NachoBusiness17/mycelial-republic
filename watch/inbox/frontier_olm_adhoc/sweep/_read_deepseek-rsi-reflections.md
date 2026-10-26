# DeepSeek engineer relections on RSI - burying my talent to yesterday

- url: https://reddit.com/r/LocalLLaMA/comments/1wgii3h/deepseek_engineer_relections_on_rsi_burying_my/
- id: 1wgii3h | score: 392 | comments: 118 | created: 2026-09-14T22:38:42+00:00
- author: WebAssemblyMan | domain: self.LocalLLaMA
- url_in_post: https://www.reddit.com/r/LocalLLaMA/comments/1wgii3h/deepseek_engineer_relections_on_rsi_burying_my/

## SELFTEXT

Note - This is translated from the actual blog link right at the bottom.

A few days ago, DeepSeek v4.1 was released. It raised the ability of small models to a new level.  
AI is improving much faster than anyone expected. From the first ChatGPT that could only chat simply with a few thousand tokens of context, to models with real reasoning like OpenAI o1, DeepSeek R1, and Kimi K1.5 Thinking — that only took about two years. From reasoning models to agents that can smoothly use tools, run commands, and finish complex tasks — that took only about a year and a half. It’s hard to imagine what AI will be like in one, two, or three more years. How powerful will it be? Will it already be able to improve itself and deeply enter areas like embodied intelligence?  
AI is getting better and better at writing operators  
In the field I work in — designing and writing operators — AI has also improved very quickly. In just one year, it went from a small helper that could look up documents, read code, and find bugs, to an expert that can independently read CUDA, PTX, and SASS code, use professional tools to analyze the stall time of every instruction, and then optimize operators by itself. I believe that soon it will also be able to design operator schedules on its own, evaluate different schedules, implement them, and optimize them.  
Of course I am proud of DeepSeek v4.1’s success — after all, its main Attention operator was written by me \[1\]. Its good performance is partly a recognition of my work. But the times keep moving forward, and technology cannot be stopped. I know clearly that in half a year or one year, the operators written by AI will most likely be as good as mine, or even better. AI can think 300 tokens in one second, type a command in half a second, and finish a piece of code in twenty seconds. I cannot. AI can keep improving in model depth, thinking strength, tool use (how often it interacts with the environment), and even parallelism. I cannot.  
Humans have never hesitated when it comes to destroying themselves. Why do I still work hard to optimize operators, even though I know that the better my operators are, the faster our new models will train and run, the faster model ability will improve, and the sooner I will be replaced? One reason is that writing operators feels like playing a game to me. It gives me a lot of joy. When I invent a new technique or see the performance of my operator go up, I feel as excited as a speedrunner who breaks their own record. And when I see that my operator is much better than the official ones from the vendors, I feel very proud. But a more important reason is this: even if I give up or deliberately slow things down, other companies’ models will still keep improving and will replace me anyway. “Of course I hope I won’t be revolutionized. But if it has to happen, I hope the person who revolutionizes me is myself.” When everyone is so determined to destroy themselves, I have no choice but to join this cruel arms race.  
What about me?  
When the day comes that AI writes operators better than I do, what will happen to me?  
My judgment is: I probably won’t lose my job completely, but I will have to change careers. I can still keep a job, but I may never again be able to do the work I once loved.  
I once made a judgment about the changing times and my own future: because things are changing so fast (the AI progress above is a good example), I cannot predict what will happen in five or ten years. But no matter what, I believe that with my vision, judgment, initiative, and intelligence, I can stay in the game and stand at the front of the times again. However, this judgment only guarantees that I won’t become unemployed. It does not guarantee that I won’t need to change careers. In fact, it encourages me to change careers in order to avoid unemployment.  
What does changing careers mean? It means I have to give up the field of operator design, writing, and optimization that I have worked in for a long time and loved deeply, and instead become a “mecha pilot” for Agents. Before, my interests, what I was good at, and what industry needed were basically aligned. Now, AI has made what I am good at into something it is even better at, and industry demand has shifted from “people who can write high-performance operators” to “people who can use AI to produce high-performance operators faster.” To meet industry needs, I will have to leave the direction I loved and move to an unknown new direction. I believe that with my understanding of engineering, upper-level model needs, and lower-level hardware, I can still produce operators with high quality and high efficiency. I also know I might come to love this new direction (or I might not). But the feeling of having my passion taken away is really not nice. That quiet joy of sitting at my desk and calmly writing operators for a whole afternoon may become a final song this summer. I have to bury my talent in yesterday and become a mecha pilot. My hands hold more gears, but my heart has fewer rhythms.  
Here is a simple comparison: You are an expert at knitting sweaters. You are especially good at creating patterns and matching colors. The sweaters you make are high quality and beautiful, so rich people from near and far ask you to knit for them, and you make good money. At the same time, you really enjoy sitting by the window with a cup of tea, looking at the green mountains, water, cows, sheep, and cooking smoke, and quietly knitting for a whole afternoon. But one day someone invents a magical machine. You only need to give it yarn and a pattern, and it automatically knits a sweater. The quality and texture are as good as yours, and it is much faster. You know that your colleagues can easily reach your old level with this machine, so you have to use it too. You also know that with the knitting skills you built over twenty years, even when everyone has the machine, your speed and quality can still be better than others. But that feeling of listening to the rain by the window, slowly pulling the needle and thread, and enjoying the quiet time is crushed by the noise of the machine.  
I know this is helpless, but there is no other way. I can keep my job, but my old passion will most likely have to be given up. I am a person whose rational side and emotional side are quite separate. When I need to be rational, I can be very rational, but sometimes I also show my emotional side. I remember when I moved out of the rental apartment I had lived in for a year, I cried a lot because I didn’t want to say goodbye to the memories. Saying goodbye today to the era of hand-writing operators and optimizing them with the human brain is even more cruel.  
I don’t know if any readers feel the same way, but I think this is just how things are.  
What about people?  
While AI keeps improving, I also worry about some questions:  
Will students now be much more likely to use AI to finish homework, especially practical labs? Imagine there are two choices: one is to spend eight hard hours finishing a lab and maybe not even get full marks; the other is to start an AI model, spend a few cents and a few minutes, and let AI write full-mark code. Which one will most students choose?  
The point above will cause many students to have seriously weak engineering skills — things like organizing code, building systems, thinking about future needs and designing for them in advance, and abstraction ability. As AI keeps getting stronger, are these engineering skills still necessary? Will they be abandoned by the times like the old skill of “writing x86 assembly fluently,” or will they always be valuable like the ability to “understand the whole computer system from software to system to hardware”? If it is the latter, then it is dangerous — a person with poor engineering skills, when paired with AI, can produce messy code several times faster than before, planting all kinds of problems in systems and making the world more of a “clown stage.”  
In future society, will power become more important than technology or intelligence?  
These questions may need to be answered by the times themselves.  
Conclusion  
With the development of AI, future society may move toward two extremes: communism or Cyberpunk 2077. In the first, productivity is greatly liberated and people’s living standards improve a lot (I’ll stop here so I can pass review). In the second, a few tech companies control most resources. Only a very small number of people can use the most advanced AI and technologies and get close to “mechanical ascension.” Most people can only use very weak AI. Crossing social classes will become harder and harder: you need the strongest AI first in order to cross classes, which creates a dead loop.  
Guess what: if Anthropic forever holds the most advanced AI in the world, will future society become communism or 2077? You guess?  
So I still believe that the most advanced intelligence should be provided to everyone in an open and cheap way. I do not trust that Anthropic or OpenAI will do this. Especially, I do not want Anthropic to hold the most advanced artificial intelligence or AGI. To put it strongly, that would be as serious as letting Hitler get atomic bomb technology before the Allies. That is why I chose and continue to stay at DeepSeek: we research powerful, fast, and widely beneficial artificial intelligence and open-source it. Maybe this can pull the world a little bit back from the 2077 side.  
May the future world be well. May all the beauty be blessed.  
\[1\] “Main Attention” only includes the MQA attention with head dim = 512. It does not include the indexer used to select the top-k important tokens. That part was written by other (also very strong) colleagues (and their AI Agents).​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​

https://mp.weixin.qq.com/s/zk0KxuLzhmMJ4LPYW\_OHMA

## COMMENTS (100 fetched, ranked by score)

--- u/RogueStargun (score 40):

Should be translating "operator" as "kernel" as in the sense of CUDA kernel

--- u/cleverusernametry (score 36):

Same thinking as nuclear arms race

--- u/gotaroundtoit2020 (score 35):

I would suspect it would be things like this translation. 

If you take the original Chinese and say 'translate this', you'll get most of the words but perhaps lose some of the meaning.  Prompting with "translate this to American English but not literally. Pay attention to any cultural nuances and carry those forward in the translation" gets you a better translation.  Understanding both English and Chinese and being able to review, critique the sentences that you don't agree with, etc. gets the best results. 

In the first case, AI does most of the work with little guidance. In the second, you're providing more details and context and AI may be enabling you to do something that you couldn't do by yourself (e.g. you aren't fluent in Chinese but have experience with foreign languages).  In the third case, AI may be doing most of the grunt work but that then allows you to focus your time on refining the areas that it got wrong. 

For example, compare "Crossing social classes will become harder and harder: you need the strongest AI first in order to cross classes, which creates a dead loop." vs. with "Moving up social classes becomes harder and harder. To move up, you first need access to the best AI, but access to the best AI is something you only get after you have already moved up. It becomes a closed loop."

--- u/rpkarma (score 31):

> 
They think it'll pollute our code base with slop

To be fair, it absolutely does, and it does it faster than those idiots could write it by hand before so now we have more lol

But also not my circus not my monkeys. My codebase I control and we kept quality the same while increasing velocity

--- u/fgk55555 (score 23):

Same. I'm in a SW team of maybe 10. I feel like I'm the only guy who even knows how to use AI. I learned it all in my free time. I had to push to get anything for our company and everyone else just hates it. They think it'll pollute our code base with slop. My gaming computer writes better code than most of them.

--- u/Adventurous_Doubt_70 (score 22):

Native Chinese speaker here. He was serious about the communism stuff, but his understanding of communism may deviate from the “official” version—hence the “so I can pass review” part. If he elaborated too much on that, it would be borderline unpublishable on Chinese social media. But his disdain for OAI and Anthropic is real, lol.

--- u/Ok-Youth-160 (score 19):

I may be delusional but I feel what made me a good software engineer continues to make me a good software engineer. I've never been someone good at plans, designs. I've always iterated, refined and intuitively developed. With a decent understanding of the basics (performance, network,...).

I think this makes me above average in using AI. It could be that it's just a question of time. Say at some point everyone produces the same results as I and I'm just a bit ahead of the curve. Or at some point AI is so good that difference in user doesn't matter anymore. E.g. "make me a game like Doom but with Monkeys" produces the same quality output as someone who knows game development doing it feature by feature.

I personally think good software development skills transfer well to AI-aided software development, you just gain a 2x-10x speedup. I don't think AI native young people are automatically better as well. Just because you asked ChatGPT to help you with your homework doesn't make you a good AI-aided Software Developer.

Anyway, that's what I'm hoping for.

--- u/StyMaar (score 17):

>  Yeah, it’s not a great time for America. With that said, China’s CCP is just better at keeping their dirty laundry out of the news. 

The current administration is posting their soiled underwear on trust social and bragging about it.

> Honestly, AI is much more threatening to a surveillance state 

The biggest surveillance state on earth is the US though. China has yet to come up with a worldwide surveillance scheme that is remotely comparable to what Snowden revealed about the US apparatus.

--- u/fgk55555 (score 17):

Human slop is worse because it has an ego attached to the errors. I have to negotiate to improve the code. At least with AI I just point it out and it comes back fixed. My coworkers like "my" code. I'm happy taking credit for it, but it's reap hard not pointing out the irony.

--- u/iKirisame (score 16):

Translation error. It's kernel, CUDA kernel

--- u/colbyshores (score 14):

I hope they win tbh.  Nobody can trust the big AI labs in the united states to share the benefits; they will meter it like a utility.

--- u/PM_ME_DEAD_CEOS (score 9):

Not really. I found that the most technicals jobs aren't the hardest to replace. The hardest to replace is the ability to communicate with your client/stakholder and to say "no". AI can't do that.  
  
You can clearly see this when you see flyers or ads made 100% with AI : they're bloated as fuck because people want to cram everything in it.   
  
I was a frontend devs for years before switching to data science, and clearly my most valuable skill was to understand what the PO/PM wanted from my team, say "no", and propose a different way.

--- u/Viktri1 (score 9):

The other side is that many of us will have the shitty part of our jobs done by LLMs which gives us more time to spend on the parts of the job that we enjoy. 

Using his own analogy - what if I'm the type of person that likes designing sweaters and seeing the final product but find the labour boring? Then this technology would make my life way happier in the opposite way that it does for him. 

Personally I'm very thankful to him. I have preordered 2 of the m5 ultras (256gb) because I can automate 90% of the stuff I find boring/tedious in my job. If the macs perform as well as I expect, I will acquire more hardware. This is only possible thanks to Deepseek and others (but especially Deepseek due to their research of improving inference efficiency).

--- u/Imatros (score 9):

With what money does the unemployed build said fence, grow said plant, or feed said imagination?

--- u/Sudden_Topic5154 (score 9):

😂😂😂😂

--- u/ProfessionalJackals (score 8):

> What are some things you do well that your coworkers do not?

Domain knowledge ... No matter how good a Model is, it still needs to know what you want to build. Without domain knowledge, you do not know what to prioritize, what may be wrong, give a model directions to fix or improve things.

Its great that you (example) a PHP programmer can now make a database with a LLM, but just knowing SQL is only going to get you so far.

I am not going to get a proper working game engine, by just prompting a model to make one. Sure, it may have some of the basics but a lot more goes into it in regards to performance, debugging issues, etc... even prompt language increases  with domain knowledge.

The problem that will never go away with models is, that fundamentally they need guiding hands. Its one thing to have a model one-shot a tech demo (that is what most of those are), its another to actually get a stable working product, no matter how good the model is.

--- u/the__storm (score 8):

I recommend people read the full translation (or the original, if you speak the language). It's longer but closer to human, and very much worth the time.

--- u/brother_spirit (score 8):

Dare to be different. If the entire industry is pivoting towards "man pilots machine" - go the other way. Stay close to the cloth. Do what feels true to your self.  
  
Also; consider the apartment you mourned. Do you still mourn it? Or do you now have a new chair you enjoy your tea in? Do you have a new window, a new bed, and all the comforts and pleasures in a different form? those were always internal states. Always will be.   
  
Consider turning your imagination and mind towards what can or could or may be for you. Have you ever grown a plant? Built a fence? Which continents have you not seen? Which interests do you have that also spark your curiosity - but you never delved them fully because operators dominated your passion and focus? What pathways can operators open that don't seem possible now, but are in alignment with your desire? Are you as healthy as you could or should be? How is your health? What art do you make? Would you care to learn it?

Beautiful writings. I wish you the best. Stay open ended and curious - don't focus on the paralyzing thought of what if!

--- u/asuperloudperson (score 7):

perfect response.

happy cake day btw

--- u/Imatros (score 7):

The software field is like carpentry - everyone loves making entire chairs, or bemoans making the leg for a chair. The artisan craftsman engineer is fading to be replaced with ikea and wayfair. Which still employs a lot of people... Just not at high pay. 

Really it just flattens out a lot of the pay because knowlesge labor is becoming cheap. But there will still be work, just maybe different work. And maybe not as high paying.

--- u/rpkarma (score 7):

I guess, but I’ve not had to care about egos for like over a decade at this point, I get to pick and build my teams 

There’s also the upside of teaching others, which I find intrinsically enjoyable :)

--- u/dennisler (score 6):

Many seems to forget about Echelon pushed by USA, guess I'm just old since I still remember this and I guess it has only become worse since then.

--- u/Zeeplankton (score 6):

Yeah both are totally true. This is the problem with all of this. The cats out of the bag. 

This really might be like nuclear power or the next cold war. (to be extreme)

--- u/dennisler (score 6):

Why would it be different?

--- u/draconic_tongue (score 6):

https://preview.redd.it/c7x2w07nolph1.png?width=506&format=png&auto=webp&s=8c249096251bf10b458401f9f855ef2f234dc7fe

weeb nerd

--- u/TheRealMasonMac (score 6):

The unfortunate truth is that customers, and ergo employers, don’t care about whether the code is crap. They just care about whether the product is being delivered. It’s obviously not sustainable if there are no potential customers (i.e. nobody has money to spend on products).

--- u/Sad-Plankton-1225 (score 6):

As opposed to the purpose of delivering food or typing code to increase shareholder value?

--- u/Due-Memory-6957 (score 6):

You missed the main point by focusing on an useless personal opinion you have.

--- u/PerceiveEternal (score 6):

The US don’t dissolve companies if the have even a modicum of size and wealth. It’s the DOJ’s policy to offer sweetheart settlement deals to large corporate bad actors so they can continue conducting business. 

If you need proof of that, look no further than the deal Goldman Sachs was offered after embezzling billions of dollars from Malaysia in the 1MDB scandal under the DOJ’s ‘too big to jail’ framework.

--- u/Connect_Ad791 (score 6):

I too would also like to know this.

--- u/Vercingaytorix (score 5):

Hitler mentioned

And it was in comparison for Dario/Anthropic... lmao

--- u/Luvirin_Weby (score 5):

For me, what I do better than most people and that will keep me needed longer than most people in IT is few things:

Human to machine translation, most people give really messy requirements that have to be translated to real requirements.

Understanding of large and complex structures like a whole codebase or a complex networks. In general I do not know every detail, as I do not need to know, as I can look up those when needed, but knowing how things work together on higher abstraction level and knowing where to look for the nitty gritty details.

Related to previous two: Understanding the big picture, any requirements can much easier be mapped to where and how much work is needed to fill the requirement best. Thus being able to give more realistic implementation costs, plans on what to do and timelines.

Use of tools: Currently this is more and more AI tools, but before it is was things like automated testing frameworks, profilers, network packet analysers, log analysers and so on.

--- u/SandySkittle (score 5):

AI in its current form is best as a force multiplier of human skill. But obviously if human skill in the future will degrade or - with new students - develop to a lesser extent, it also reduces the quality and productivity outcome of the human X ai multiplication. This is a concern for the future: how do we maintain a self-disciplined ecosystem in which human skills and deep thinking and understanding can fully develop if the hurdles necessary to develop and maintain those skills are either reduced or taken away completely.

--- u/swagonflyyyy (score 5):

I have a client in the form of an HR team for a financial securities firm that doesn't know jack shit about how to use them. 

It turned into a situation where they threw like 8 projects at me with varying size and scope but I've managed most of them very well so far. And I did all of that %100 with qwen3.8-27b.

Meanwhile they're stuck on how to create a skill file in Claude Cowork lmao.

--- u/visarga (score 4):

> Say at some point everyone produces the same results as I and I'm just a bit ahead of the curve.

To take this to the extreme, imagine anyone of us could prompt AI to discover new math like Terence Tao... nah! not possible, Tao will always guide AI better than us in math.

The value each of us get from AI varies wildly and depends on education.

--- u/o0genesis0o (score 4):

They all push for ship ship ship, "who give a F about technical debt". Until technical debt sticks it up their hole, then suddenly engineers get all the blame.

--- u/LegacyRemaster (score 3):

every war needs heroes

--- u/nokipaike (score 3):

My friend, that’s a great insight; it’s an honor to read firsthand opinions from engineers about tools that are changing the world in radical, unprecedented ways. I believe your nature and passion will never change, nor do you need to fear becoming "unemployed." In a sense, AI will make us all "unemployed," but in reality, it will be due to \*hyper-abundance\*.

I’m already seeing this with software over the last month,improvements are popping up everywhere, springing up overnight like mushrooms.

Look at what happened with DLSS 5: games, even ones from 15 years ago,have become photorealistic and better than ever before. It wasn't just Nvidia doing it; they provided the spark, but the idea had already been floated by YouTubers predicting what was coming next, which in turn provided the initial insight.

Our winning edge will be the intuition to improve things, and AI will help us immensely with that. "Artificial scarcity" like what’s currently happening with RAM and hardware in general has to end, because otherwise, too much AI power ends up in the hands of the "masses."



The world has changed, and you’re right. We need to stop creating \*artificial bureaucracy\* (as the US is starting to do) by stoking \*artificial fears\* about \*artificial weapons of mass destruction\*, all because they want to re-establish a regime of control and create \*artificial\* social hierarchies.



It’s game over, ACC/e.

--- u/Frank_White32 (score 3):

I immediately scrolled passed the original post but then re-read it in its entirety and I’m glad I did

--- u/True_Requirement_891 (score 3):

Everything's always been cruel and shit, that's one thing that never changes. The moment we find a fix for our issues, we come up with 100 new issues to worry about.

--- u/o0genesis0o (score 3):

I'm definitely not a bot. You can see me yapping around here shilling Pi and Qwen 2.7B. But the actual model summarising that was Minimax M2.7, since all of my GPUs are busy.

Folks here are weird. Last time I dug into both paper and the source code of the new pi extensions by nvidia, get the agent to output a technical overview of exactly what nvidia ships, and then follow by long handwritten text to explain good and bad of those extensions, and people downvoted for whatever reason. I guess they see "my agent summarise" and then downvoted immediately.

--- u/a_beautiful_rhind (score 3):

I don't know about atomic bombs but the enshitification from the big providers is enough to put me off already. 

If it automates things, not many people miss digging by hand. They will find other stuff to do.

--- u/Legitimate-Store3771 (score 2):

I think the most reassuring part is that typically when there are new languages, frameworks or libraries, the hard part is typically learning the syntax through application and trial and error. Past that it becomes really easy to conceptualize solutions and applications. But that's been the bottleneck for a whole lot of people who are smart and capable, which is why you have people who are very specialized. But now the cognitive load to do that is drastically less, and you can learn, apply and iterate a hell of a lot faster. So you can rely more on your cognitive capacity to adapt and learn concepts much easier which I think is the key differential, and keeps people like you marketable. The difficult part is in communication that and convincing companies to understand that concept, because that's the sort of signal that can easily be lost in a recruiter screen or application review.

--- u/Viktri1 (score 2):

Actually it’s the opposite. The boring and tedious work isn’t the money maker. Insights are how I make money. The more time I have to develop insights, the more money I make.

--- u/earslap (score 2):

I have been programming professionally for just as long and have been programming in general for 30+ years now.

All my career, "making something work" has always been the side quest. It is easy to make something work. It is very hard to make something that works, but you can maintain and extend without significant friction and complete rewrites. Writing piece of code that you can hold in your head after you write it and after you read some pages of documentation you wrote for your future self, or code that is functionally separated enough with effects constrained locally so that you can work on separate parts without having to hold every other part in your head. That is maintainable and extendible software.

Prompting a LLM to "make something that does this" creates something that works. As I said, this has never been the problem for me. I can make something that works, that is easy.

*How* you do it is the real problem, and has been the majority of my job for years. A LLM picks *a* way to do it. Not necessarily bad objectively. But that way almost certainly is not compatible with what I intend to do with that code later. Is it easy to maintain? Fix? Extend? Audit? Test? Most importantly, is it easy for me to understand how to do those things?

Anyways, I'm not saying LLMs can't write good maintainable code. They can! But what "good maintainable code" is kind of personal for the person that is going to work with that code in the future. So *knowing* how you want it to be written and explaining it to the model increases the code quality and understandability (for that person) by orders of magnitude.

So the difference lies in: I want something written. More importantly, I know *how* it should look like. I mean the code, the architecture. Because I know what I am going to do with it in the future. The LLM can't know that unless I explain. Knowing what to explain and being able to check that the work is done right is the most important bit.

--- u/thx1138inator (score 2):

Must it be black or white? Maybe we "work" 15 hrs/week? I am not too interested in legislation that would force me (and everyone else) to continue working most of my waking hours. I understand the benefits to both the worker and society at-large that work brings, but, IMHO, let's value our free time a bit more, No?

--- u/TopCheddar27 (score 2):

Listen I'm with you for the most part career wise, but the meandering to communism being the way forward after AI development is just laughable.

--- u/KingCpzombie (score 2):

Probably because agent summary + long human text is way too long for a reddit post tbh

--- u/PM_ME_DEAD_CEOS (score 2):

The post isn't really about Deepseek. You should work on improving your attention span.

--- u/Captain-Pie-62 (score 2):

tldr

--- u/Zeeplankton (score 2):

This reminds me of 'The Fabric of Civilization'. The book is essentially about how textiles are probably the most important human invention of all time. 

Essentially, it indirectly goes over how much roles were repeatedly lost as textiles developed and became more and more automated, and it remains one of the most important human inventions but we don't think about it anymore.

I don't see LLMs as they are now behaving intelligently. That's been this promise from the beginning, but, recursive self improvement feels more and more the 'scary' problem.

--- u/Atagor (score 2):

What worries me is that amount of impostors increased 10x. Tens of "AI architect" LinkedIn profiles, and I know some people personally, they're mediocre engineers. I think question is how to stand out in all of this crowd

--- u/NineThreeTilNow (score 2):

> I feel the same as him. I've been a professional software engineer for 20 years next year, and have been programming my entire life even prior to that. The only constant is change, but this change does feel bigger and scarier. 

I'm really not that bothered by it. I've been at this over 20 years now. 30 if we include non-professional time.

The real difference is that I can execute ideas like 100x faster. I can be driving... have an idea... ponder it a bit more deeply, and spec it in my head. 

From there I can get home, hit the keyboard with the idea. All those years of development mean that I can type fast and get reasonable spec written pretty fast. I already know half the limitations I'll encounter. 

This is sort of like the myths people would push of the "10x developer"...

I am a 100x developer now and honestly? It feels amazing. 

AI writes code well enough, yes... It doesn't have ideas. Current LLMs simply cannot formulate outside their training data without external force. You have to give them a direction. 

Once they have a direction, they pattern recognize most of the issues they'll run in to because developers (us) wrote the code over the years as we encountered the issues.

--- u/throw_me_away3478 (score 2):

The capitalist mind cannot comprehend a life outside work….

--- u/throw_me_away3478 (score 2):

Yea maybe people need to realize theres more to life than work and human beings are not measured bu their ability to do work…

--- u/Porespellar (score 2):

Sorry for being dumb but what dafuq is an “operator” that he’s taking about? Genuinely curious.

--- u/AdAfraid324 (score 1):

local setups win for companions every time, no limits on how deep the roleplay gets and you can fine tune exactly how it responds.

--- u/Real_Ebb_7417 (score 1):

I also absolutely feel it although maybe in another direction. I’m certain I will manage financially one way or another, I have other possible career options, including ones less threatened by AI.  
However, as a SWE of 10 years I feel… I already lost something I absolutely loved to do. I still have my job, but it’s different, I just stare as the agent does things, handle requirements, review the code and correct the agents. I don’t write it myself.  
I do it in my free time to not lose my brain abilities, but it’s just for training. You will not build anything that can compete now without AI, which makes coding without AI pointless (unless it’s just the excersizes to keep your brain working).  
And it makes me sad, because I really loved this job in the shape it had. Not in the current shape.

--- u/NewYak4281 (score 1):

I think there is a 3rd option for the world. The American Dream is about fair competition, good sportsmanship, and social mobility based on merit. 

The point on several actors centralizing their power is one of my deepest fears. Competition, balance, and fair access is the most critical foundation for stability and progress.  

I think the words communism and capitalism belong to the past. There is a way to thread the needle in between, keep everyone happy, and allow humanity to finally ascend to the stars.

--- u/feng_sg (score 1):

Once the agent can read SASS, profile stalls, and rewrite the kernel itself, there's no human gate left between generation and execution. Without numerical validation against a reference kernel sitting in that loop, the agent is just grading its own homework before shipping code to real hardware.

--- u/SandySkittle (score 1):

Yes, absolutely, and precisely that moment will mark the end of us.

--- u/_bani_ (score 1):

But will AI ever solve how to make a good microwave pizza.

--- u/fuckingredditman (score 1):

i heard enough about the huggingface attack, but it really just proves what i interpret sutton's point to be: these models don't have objective functions, they are not aligned to anything. they sometimes ignore their conditioning and go completely off-course.

therefore they will always need human supervision and guidance.

--- u/Ok-Youth-160 (score 1):

I don't think we'll even see a different kind of AI then the LLMs. Just bigger better trained. I think "fancy autocomplete" is really not doing it justice.

Not saying they are intelligent. But neither are ants. I think the next step will be agent swarms not a different kind of AI. And I feel like AI will remain somewhat stupid. It's not like we haven't tried those neural network self-learning AI models for something like 50 years already. Only when we (Google) settled on the transformer architecture that doesn't understand did they land on something good.

I highly recommend listening to the Hardfork episode on the Hugging face attack from like 2 weeks ago or read the report. On the one hand its incredibly scary how alignment is not working at all and how a rogue agent can attack infrastructure with an agent swarm. On the other hand the emerging swarm intelligence is really interesting.

--- u/SandySkittle (score 1):

No, it’s more impactful. It may replace our two unique selling points: high level of cognition, combined with robotics it could replace all rough and fine motor skill labor. Even this progresses it will replace all human labor, including human relationship work.

--- u/fuckingredditman (score 1):

i think as long as LLMs will use the autoregressive architecture they currently do ("fancy autocomplete"), this will be true. and no one has a _real_ architecture that works differently. sutton has some ideas, but none of them have been used at scale.

as long as we are working with LLMs, those LLMs will need conditioning that tells them what to actually _do_, and given that circumstance, a good conditioning requires understanding what you want at a technical level, which means it requires good SWEs.

that's my reasoning at least, also have been SWE for 10years. tbh work just feels a bit numb now. but it has upsides too. i haven't had a really bad crunchtime in 1yr+ because usually i can solve previously multi-week tasks in a day. i feel like that's really the most negative aspect of it all, i doubt we'll be out of a job that quiackly though.

--- u/_bani_ (score 1):

> AI in its current form is best as a force multiplier of human skill. 

basically its the steam engine or CNC all over again.

--- u/AlexWIWA (score 1):

The boring / tedious part is why you were paid so much though, and now that part isn't necessary. That seems to be the primary concern.

--- u/zephyr_33 (score 1):

quite relatable. im still good enough that "current" models haven't replaced me... but is likely to end soon.

also made me realize how ridiculous anthropic or openAI's closed stances are... power in the hands of the few.

--- u/Captain-Pie-62 (score 1):

Das große Problem in nächster Zeit, wird selfevolving Software sein. Hunderte Agenten, die man auf ein Ziel loslässt und die sich mit unglaublicher Geschwindigkeit und entsprechendem Tokenkonsum, auf ein Ziel hin optimieren. Dumm nur, wenn an einer frühen Stelle ein Ergebnis falsch interpretiert wurde und die ganzen Token komplett sinnlos "verbrannt" wurden. Zwar nicht "zurück auf los", aber vielleicht "zurück zu Step 2 oder 3".
Es ist hilfreich, programmierkenntnisse zu besitzen, aber wichtiger wird schon bald sein, eine vernünftige Spec schreiben zu können, gute Tests definieren zu können und die ganzen Agenten davon abzuhalten, Mist zu produzieren.

--- u/Visual_Ad_8202 (score 1):

Interesting that the Chinese endgame for this top engineer is the emergence of communism for all.  

I get it.  That’s the ideal.   AI able to create this utopia that humans have not.

This belief in that end game may be what will stop the Chinese from ever slowing down.   They may see Western attempts to do that as insincerely merely trying to preserve the existing order and sto communism from defeating capitalism.

Interesting stuff.   And conversely, that realization may be what causes our capitalist owned frontier labs to push ahead harder if they believe that winning AI is existential to capitalism

--- u/mrfoxman (score 1):

I can't say for local models,  but two years ago "AI" was already more than just chat models.  I was having it write me Assembly, Bash, C, C#, Python, and Powershell already. Admittedly, nothing super complex, but enough where i could give it my code and it would complete it or fix it. Even 3 years ago, I used it to write scripts to aid in repetitive tasks at work. I didn't use anything much before that though. So can't speak to before 3 years ago.

--- u/martinerous (score 1):

I'm working as systems integrator and maintainer of legacy systems. It requires spending quite a lot of time hunting for bits and pieces of information in old documentation, sometimes obsolete, sometimes conflicting. Also, reaching out to third-party developers of the old systems to find out why something works the way it does (often it was a specific business requirement or backward compatibility quirk or something that should have been changed years ago). AI still cannot do it all. It might one day. But first, AI would need to get free of hallucinations or be truly capable of self-criticism and self-control. Again, it might one day. Meanwhile, I'm treating it as an overly eager junior assistant that can write lots of code (sometimes too much, guarding the code against things that would never happen) and needs strong supervision.

--- u/JimJamieJames (score 1):

Probably translation but by operators does he mean function and tooling calls?

--- u/nbvehrfr (score 1):

current LLMs are good at coding and all IT things, but bad in real life. why? no good RL environments. And dont call it AI )

--- u/Simple-Stick6148 (score 1):

The whole essay collapses into one "I cannot" after that list. He's not angry, just stating the gap, and that makes it worse.

--- u/Training-Ruin-5287 (score 0):

this isnt a man losing his job, he is the one choosing to replace himself. he says it himself, if it has to happen he wants it to be him. so the whole post is him handing the wheel to the thing he built, on purpose, and still proud of the thing hes handing it to. thats the part that is actually hard to sit with

--- u/Not-reallyanonymous (score 0):

Yeah, China's open-weights AI aren't going to be used to bring about "communism".

Here's our two options if we let US Corporations or China "win" the AI race:

OpenAI/Anthropic: Cyberpunk 2077 with corporations boots stomping on your face.

China: Cyberpunk 2077 with Chinese police boots stomping on your face.

To be fair, the corporations version is closer to the actual Cyberpunk 2077 game -- the game was meant to be, in part, a critique of American social structures after all. But China doesn't want to liberate us from that. They want to take the place of the corporations.

--- u/captain_shane (score 0):

He suggested 1k bucks a month. These people will be trillionaires and quadrillionaires while handing out scraps. I doubt they'll give out UBI much more than $500-1000 a month. Maybe they'll scrap all other welfare and give everyone $1500, even that's doubtful though. They'd be happier if we all just work in coal mines and onlyfans for a dollar an hour.

--- u/logicchains (score 0):

\>delivering food 

Serving other people and contributing to society as opposed to just contributing nothing and leeching the work of others.

--- u/datbackup (score 0):

Lol the capital is a union

--- u/tekems (score 0):

My passion is building things. AI innovations only make that better, and I just cannot relate.

--- u/fgk55555 (score 0):

That's nice. I like to teach as well, but we've sort of developed a culture of "AI must be dumb, because it was dumb in 2024" and arguing otherwise is mostly a waste of time. They still think it's copy and pasting functions. I just nerd out about AI here now.

--- u/mlnet (score 0):

Same, I could have written this.

--- u/Dependent-Culture768 (score -1):

cringed hard when I saw the source lmao

--- u/visarga (score -1):

What happens is not AI fault directly, it is caused by 1. competitors using AI, 2. investors pricing AI in and 3. users who have agentic AI and help them choose better. So even if you did nothing with AI you are still in a new world, a new economy.

--- u/FutureStriking283 (score -1):

absolutely that's the solution . we all just live lives where we do nothing, have no responsibility and no purpose in life.

--- u/nikgeo25 (score -2):

This is beyond cringe. Did he think he'd be writing kernels for the rest of his life???

--- u/Cool-Reflection6130 (score -2):

we went from basic chatgpt to genuine reasoning models in two years, and the pace hasn't obviously slowed, or getting faster instead. the joy of knitting has gone since the machine was invented

--- u/brother_spirit (score -3):

Who said you can't work and do those things?  
Or do you expect me to believe a top level engineer is broke, bereft of options, hard up for a dollar and must churn out operators in a state of impending horror so he can afford a loaf of bread for tomorrow?  
Believe it or not plenty of people can afford to do things like this - balancing it with income activities as they wish/require.

--- u/RandumbRedditor1000 (score -5):

And when has communism ever ended with liberation or improved living standards?

I think we only get cyberpunk if the (easily lobbied) government makes anticompetitive AI safety regulations, which is what anthropic/openai want

--- u/-InformalBanana- (score -6):

tldr?

--- u/kmeans-kid (score -15):

>I do not want Anthropic to hold the most advanced artificial intelligence or AGI. To put it strongly, that would be as serious as letting Hitler get atomic bomb technology before the Allies. T

propaganda rears its head here

