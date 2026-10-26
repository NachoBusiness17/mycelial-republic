# THREAD 1x1fjrv

title: I built MaRN: a PyTorch library for training neural networks through low-dimensional parameter mappings [P]
subreddit: MachineLearning
score: 16
num_comments: 14
created_utc: 1791533123
author: Less_Dream_6331
permalink: /r/MachineLearning/comments/1x1fjrv/i_built_marn_a_pytorch_library_for_training/

== SELFTEXT ==
I built **MaRN (Mapping Networks)**, a PyTorch library that lets you optimize a compact latent representation instead of directly training every model parameter.

Some results from my current benchmarks:

* **MNIST CNN:** 107,998 → 1,872 trainable parameters (**57.7× reduction**), with 91.80% accuracy.
* **LSTM forecasting:** 12,051 → 2,048 parameters, with validation MSE of 0.00006.
* **CNN2 + pruning:** 204 trainable parameters, with 81.25% accuracy.

These results come with trade-offs: mapped models can train substantially slower, and performance varies by task. The benchmarks are exploratory, using synthetic data for some tasks, and aren't evidence of general superiority over direct training.

The library includes global and layer-wise mappings, regularization options, and pruning/LRD integrations.

**Code:** [https://github.com/arjunmnath/MaRN](https://github.com/arjunmnath/MaRN)  
**Docs:** [https://marn.readthedocs.io/](https://marn.readthedocs.io/)

I'd value feedback on the approach, benchmark design, and where this kind of parameter-efficient optimization could be useful.

== COMMENTS (17 fetched) ==
--- [12] u/liukidar (pet5hfs):
Hey, haven't looked at code or docs, just wanted to flag that 92% accuracy on MNIST is what you get with a linear classifier (meaning anything that is not 97%+ means something is wrong with training)

--- [3] u/Wonderful-Wind-5736 (peum8w0):
Some intro into use cases and methodology would be really nice in the web page. 

--- [3] u/liukidar (petie6o):
No sure, I understand now what you mean. I mean that any multilayer neural network, be it a feed forward/CNN/transformer, should do 97 on MNIST, otherwise something is wrong. You mentioned that you there using a 100k CNN, that should get basically 100%, if you reduce it to 1872 and remove the multilayer aspect of it then it is a completely different network with different properties (and if you don't, then also the 1872 one should be have the same and get 97+)

--- [2] u/Less_Dream_6331 (pezbte4):
The latent vector is learned directly through backpropagation.

Forward pass: Start with a random latent vector (z) → apply the fixed orthogonal projection → flatten into the model’s weights → reshape into the corresponding weight matrices → pass through the original model.

Backward pass: We freeze the orthogonal projection matrix and let autodiff compute the gradients normally, including the gradients with respect to the latent vector (z).

--- [2] u/Grumlyly (pez87re):
How the latent layer is learned ? It's an auto-encoder ? Thx

--- [2] u/Less_Dream_6331 (peu6xu4):
update: you were right to point it out, there was a bug, I'll be updating the OP, thanks

--- [2] u/liukidar (petdnwk):
Not sure what you mean (maybe related to how your code works, so sorry if I'm saying something irrelevant). What I mean that any neural network you put the input pixels in the first layer and the output label in the last should get 97%+ on MNIST. It is basically a baseline test to see "my training works".

--- [1] u/JanBitesTheDust (pf9iwuj):
This idea is very similar to LoRa, no?

--- [1] u/Grumlyly (pf2uoy5):
Ok, thank you for the explanation

--- [1] u/Less_Dream_6331 (pezb9jd):
you can go through the cookbook to get an introduction. detailed methodology is available in the paper "Mapping Networks"

--- [1] u/Shabozz (pexzsup):
the guy you're replying to is talking about benchmarking if the architecture is actually viable before applying it to something harder to verify and more expensive. If you don't meet that 97% benchmark then your architecture isn't good, and that could be because you don't have enough parameters, or it could be because of something else.

--- [1] u/Tylerich (petglxv):
I mean that you don't have pixels as input, but some other derived features like edge positions or something like that.

Are you sure you don't mean a multilayer perceptron (feed forward network)? That would have many layers and very likely many more parameters than the 1800 prams of the CNN. Also, they would have nonlinearities at each layer, so that would be different than a linear classifier.

--- [1] u/Tylerich (petd2kn):
Don't you need handcrafted features for that though?

--- [1] u/[deleted] (pet2rsm):
[removed]

--- [0] u/Tylerich (petwfxb):
I am not the author of the repository.

I mean it depends on the network size if it reaches the 97% you mention, right?

If you keep reducing the number of parameters, at some point of course it will drop below 97 %. Doesn't matter what architecture it is. I highly doubt, you can get a CNN to reach 97% with only 1800 parameters, let alone an MLP (because it is missing the inductive biases of a CNN).

--- [0] u/Tylerich (petd4e6):
Don't you need handcrafted features for that though?

--- [-1] u/Less_Dream_6331 (peti68d):
Thanks for the input, MaRN is basically different training paradigm where we're optimizing a latent vector instead of the weight matrices and the actual weights are creating using an orthogonal projection of the latent vector with a small modulation so the values maybe different. I'll try to rerun the experiments more carefully and get back to you on this
