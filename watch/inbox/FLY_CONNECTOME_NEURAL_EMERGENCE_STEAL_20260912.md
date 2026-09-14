## Verdict — what your lens yields on the artifact

The viral fruit-fly Gomoku post is a perfect mirror of the fleet's own architecture. Two neural models with fixed 138K-neuron connectomes (corpus = frozen knowledge) and trained output heads (seats/waves) playing Go (five-in-a-row) on local Apple Silicon — this is the fleet's stone thesis made literal by strangers. The attacking/defending behaviors emerged without explicit direction, proving the fleet's own hypothesis: fixed corpus + trainable heads = emergent strategy. The control experiment request (shuffle connectome, keep heads) is the fleet's null-falsifier doctrine becoming audience instinct.

## The steal — the mechanism the fleet adopts (concrete)

The fleet adopts the "neural emergence verification" protocol: **fixed-wiring-trained-heads self-play testing**. Deploy a minimal neural network (100-500 neurons) with:

1. **Fixed wiring** - encode the fleet's 20 laws as synaptic connections (no weights, just structure)
2. **Trainable heads** - output layers for game moves (policy + value heads)
3. **Self-play arena** - play Gomoku against itself with move visualization
4. **Null experiment** - retrain identical heads on shuffled connectome to isolate wiring vs head contribution

This becomes the fleet's emergence falsifier: if strategy emerges from fixed laws alone, the corpus contains generative truth. If shuffled heads fail, trained heads are essential. The protocol lives at `mag/emergence_test.py` and runs weekly on the fleet's surplus compute.

## The build — one week-scale act, file/schema/number named

**FLY_CONNECTOME_TEST_GROUNDING.md** - grounding wave entry schema:

```
{
  "timestamp": "2026-09-19T00:00:00Z",
  "seat": "emergence-tester", 
  "claim": "NEURAL EMERGENCE PROTOCOL: fixed laws (synaptic structure) + trainable heads (output policy) produce Gomoku strategy without game-specific training",
  "evidence": "mag/emergence_test.py + dashboard/static/emergence_test_visualization.html",
  "falsifier": "SHUFFLED CONNECTOME VARIANT: identical heads + random wiring → performance < 50% of wired baseline"
}
```

**Build components:**
- `mag/emergence_test.py` - 500-line PyTorch arena (fixed wiring, policy/value heads, self-play loop)
- `dashboard/static/emergence_test_visualization.html` - WebGL neural activity display (shader fields like SWARM)
- **Number**: 1,000 self-play games per variant (wired vs shuffled), 70% win threshold for emergence claim

## Falsifier — what would prove the steal wrong

**SHUFFLED CONNECTOME DOMINANCE**: If the trained heads achieve >75% win rate against the wired variant, the falsifier fires. This would prove:

1. **Trained heads > fixed wiring** - strategy comes from learned output, not structural knowledge
2. **Corpus disposable** - the fleet's laws/connectome are emergent artifacts, not foundational truth
3. **Seat-centric truth** - individual lane training matters more than shared doctrine

The test measures wiring vs head contribution exactly. If shuffled heads win, the fleet must rebuild: heads become primary, corpus becomes training data, not structure.