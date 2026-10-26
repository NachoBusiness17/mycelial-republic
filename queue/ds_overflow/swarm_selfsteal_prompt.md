You are extracting a self-steal inventory from estate research receipts about swarm signaling and pheromone-style steering. Read the file named in each item. For that file, extract as JSON fields:

- "mechanisms": array of named mechanisms the file describes (tool names, buses, signals, loops)
- "consumers": array of what each mechanism's OUTPUT is consumed by, as stated in the file (or "none-stated" if the file names no consumer)
- "signal_types": array of signal classes (deposit, decay, reinforce, tick, poll, push, etc.) with one-line descriptions
- "stated_gaps": array of limitations, TODOs, or "not wired" admissions the file itself states, quoted short (under 20 words each)
- "event_vs_poll": your one-line verdict for this file: are its updates event-driven (push on arrival) or schedule-driven (poll/tick)?

Be literal: only extract what the file's own text says. No invented mechanisms. Reply with ONE JSON object per item on its own line, carrying the item's id field verbatim plus the fields above.
