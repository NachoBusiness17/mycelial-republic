# AgileRL Arena v1.0: manifest-driven RL training (local or cloud), with LoRA/GRPO LLM finetuning

- url: https://reddit.com/r/LocalLLaMA/comments/1wdjk0y/agilerl_arena_v10_manifestdriven_rl_training/
- score 5 comments 0

## SELFTEXT

`agilerl-arena` has released v1.0. It's the SDK/CLI half of AgileRL, split out as its own PyPI distribution (no torch dependency) that shares the `agilerl.*` namespace:

    pip install agilerl-arena   # SDK + CLI only
    pip install agilerl         # core, depends on arena

With AgileRL Arena you describe a run in a YAML manifest (algorithm, environment, network, mutation, selection strategy, replay buffer) and the same file runs locally or gets submitted to their managed cluster. Validation is Pydantic, so bad configs fail before training instead of 40 minutes in. Unknown keys are now rejected in 1.0.

The LLM finetuning path takes any HF model ID plus a LoRA config, and supports either rollout envs (model generates, gets scored by a reward function you supply) or supervised datasets with `objective: sft` or `preference`.

    network:
      pretrained_model_name_or_path: Qwen/Qwen2.5-0.5B-Instruct
      max_context_length: 512
      lora_config:
        lora_r: 16
        lora_alpha: 64
        target_modules: [q_proj, k_proj, v_proj, o_proj]

Running it locally is two lines, no account needed:

python

    from agilerl import LocalTrainer
    trainer = LocalTrainer.from_manifest("dqn.yaml", device="cuda")
    population, fitnesses = trainer.train()

**Evolutionary HPO:** instead of one agent, you train a population and periodically mutate architecture and hyperparameters, keeping the fittest. Costs more compute for the same wall-clock, but you're not hand-tuning learning rates.

**What's new in 1.0:** specs now build algorithms through paradigm builders, local training dispatches through strategy selection based on paradigm flags rather than per-spec branching, and the manifest schema lives in one package instead of being duplicated. Also `arena manifest validate` / `arena manifest schema` for checking configs without submitting anything. PEFT bumped to 0.20, which rejects LoRA on Mamba `out_proj`/`conv1d` — they exclude those automatically now.

Docs: docs.agilerl.com · Release notes: github.com/AgileRL/AgileRL/releases

## COMMENTS

