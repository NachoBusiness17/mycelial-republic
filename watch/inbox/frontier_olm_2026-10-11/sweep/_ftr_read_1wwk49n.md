# THREAD 1wwk49n

title: The ultimate guide to multi-harness RL
subreddit: LocalLLaMA
score: 84
num_comments: 12
created_utc: 1791023977
author: lewtun
permalink: /r/LocalLLaMA/comments/1wwk49n/the_ultimate_guide_to_multiharness_rl/

== SELFTEXT ==
Hi folks, it's Lewis here from the post-training team at Hugging Face. We've been exploring how to train open models in different coding harnesses and wrote up a looong guide on how we solved this using open source libraries like TRL and the Harbor framework for RL environments. We hope you find this interesting, especially since everyone nowadays has their own custom harness (e.g. Pi + extensions) and now there's a recipe on how to squeeze the best performance on them with whatever open model you use as your daily driver. Happy to hear any comments or feedback!

Link to the guide: [https://huggingface.co/spaces/FineEnvs/multi-harness-rl](https://huggingface.co/spaces/FineEnvs/multi-harness-rl)

== COMMENTS (12 fetched) ==
--- [10] u/Then-Topic8766 (pdlj8gh):
Guide is cool but those damn bots...

--- [9] u/Then-Topic8766 (pdljw07):
Do you have a good recipe for apple pie?

--- [9] u/Equivalent-Flan-1590 (pdlhmqp):
This is an incredibly timely guide. Anyone trying to do RL for coding tasks quickly realizes that overfitting to a single harness format completely ruins a model's generalizability when you move it to a different setup. Moving between environments like Pi and standard benchmarks usually breaks the agent's parsing logic or formatting habits. Leveraging the Harbor framework with TRL to create a robust multi-environment recipe is exactly what the community needs to build models that do not immediately fall apart outside of a specific test sandbox.

--- [5] u/lewtun (pdm05i1):
It's bots all the way down ...

--- [1] u/jazir55 (pdpd47m):
Which harness do you think they used?

--- [1] u/zephyr_33 (pdmq6ma):
Easy fix - Forget Harness benchmax for shell/terminal. In harness use only shell tool to so everything.

--- [1] u/[deleted] (pdl540j):
[removed]

--- [-1] u/Certain-Cod-1404 (pdmvwej):
Really interesting, I might actually need to do something like this in a couple months so I appreciate the resources, good work !

--- [-2] u/MomentJolly3535 (pdmtopn):
It's very interesting, i always thought the harness didn't matter much for bigger models

--- [-2] u/returnity (pdmkfaq):
Wow killer guide. This is so incredibly helpful for my learning process right now. Thank you!

--- [-2] u/Equivalent-Flan-1590 (pdljfgz):
Haha yeah, the comment sections on Hugging Face spaces and Reddit are getting absolutely flooded with them lately. It is a massive pain trying to dig through all the generic fluff just to find the actual technical discussion. The irony of using AI to bury actual AI research is pretty funny though.

--- [-4] u/GuruCsharp (pdmfv8j):
Wow that's an angle I never thought of! I kept focusing on the models themselves and their weights, but this is quite valuable to consider!
