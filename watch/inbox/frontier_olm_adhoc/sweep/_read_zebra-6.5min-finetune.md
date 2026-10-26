# Fine-tuning Qwen 3 4B Base on 100 zebra puzzles yielded +31% on MATH-500. 6.5-min (Single H100/H200) reproduction notebook included.

- url: https://reddit.com/r/LocalLLaMA/comments/1wdhb24/finetuning_qwen_3_4b_base_on_100_zebra_puzzles/
- id: 1wdhb24 | score: 37 | comments: 7 | created: 2026-09-11T14:06:50+00:00
- author: TGSCrust | domain: huggingface.co
- url_in_post: https://huggingface.co/blog/tamewild/pcss

## SELFTEXT

(empty)

## COMMENTS (7 fetched, ranked by score)

--- u/TGSCrust (score 5):

The main reason I left them out of the post is that the traces are super long (up to 11k+ tokens) and it would have ruined the page layout. 

You can view the raw samples in the dataset viewer here: 
https://huggingface.co/datasets/tamewild/instruct5/viewer

I also print out a full sample in the reproduction notebook so you can see the exact formatting. Just a heads up that it's a massive wall of text to scroll through: 
https://github.com/tamewild/pcss/blob/main/notebooks/qwen3_4b_base.ipynb

--- u/ilift (score 4):

Very interesting, have you experimented with other small datasets for fine-tuning? It makes sense that logic puzzles would shift weights associated with logic, but seems interesting that such a lift can be done with only one form of logic puzzle in the dataset.

--- u/DinoAmino (score 4):

I like how the older 4B performs just as well as the newer 9B at a fraction of the training time. Older models can still be useful and are great for fine-tuning.

--- u/TGSCrust (score 1):

I realized that I completely missed explaining what zebra puzzles are in the post, which was a huge oversight.

I think the lift happens because zebra puzzles are so combinatorially complex. A 5x5 puzzle has 5 feature categories, which creates a search space of roughly (5!)^5.

I did mess around with a few other datasets, but nothing exhaustive enough to publish numbers on at this time

--- u/HyperCmdcast42 (score 1):

100 zebra puzzles moving MATH-500 by 31 points is absurd in the best way. 6.5 minutes on a single H100 makes it cheap enough to just run the notebook and find out.

--- u/jacek2023 (score 1):

Zero Zebra Puzzles on the linked page, why not present some use cases?

