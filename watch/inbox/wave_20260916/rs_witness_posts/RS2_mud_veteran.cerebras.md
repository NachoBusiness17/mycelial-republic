# WITNESS 2 - THE MUD VETERAN

- lane: cerebras-qwen (qwen-3.8-27b) [diversity retry]
- temperature: 0.55
- usage: {'total_tokens': 4649, 'completion_tokens': 3940, 'completion_tokens_details': {'reasoning_tokens': 3664}, 'prompt_tokens': 709, 'prompt_tokens_details': {'cached_tokens': 0, 'image_tokens': 0}}

POST:
Room-as-table survives 50 rooms only if the table is adjacency, not behavior. If each room carries rows for open, unlock, key, portal, you are back to an opcode swamp. The missing abstraction is the door: a first-class, stateful legality object with a typed condition, effect, and target. Rooms list exits; the gate resolves VERB against the exit’s predicate, not against room-specific rows. Locks are door state, not room status. Portals are exits with a target and a condition. Keys are capabilities. Refusals stay typed because the failing predicate is named. This keeps movement RNG-free and replayable: same seed, same moves, same door state. If you don’t split topology from legality, M3’s zone will be a patchwork of special cases and the replay receipt will hide the rot.

NUANCE: The receipt must hash door and lock state, not just room id, or a key used in one process can vanish in another; amends M1

DIFFERENT:
I’d build a tiny exit DSL: rooms declare exits; exits have predicates and effects; the gate evaluates predicates. No per-room verb rows. This lets locks, keys, portals, and timed doors be data, keeps refusals typed, and makes replay receipts smaller because state changes are explicit.
