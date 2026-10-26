# batch_runner.py — batch trajectories

via cage beat ext-02e01ce3a7 folded=True

I have enough understanding of the source. Let me report what I found.

Report:

(1) The source is `batch_runner.py`, a parallel batch agent runner that loads prompts from a dataset, splits them into batches across multiprocessing workers, and runs an AI agent against each prompt with per-task sandb
