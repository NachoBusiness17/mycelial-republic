# WITNESS 2 - THE MUD VETERAN

- lane: groq-oss (openai/gpt-oss-120b)
- temperature: 0.55
- usage: {'queue_time': 0.150039886, 'prompt_tokens': 694, 'prompt_time': 0.040396788, 'completion_tokens': 1108, 'completion_time': 2.32894598, 'total_tokens': 1802, 'total_time': 2.369342768, 'completion_tokens_details': {'reasoning_tokens': 911}}

POST:  
Room tables work for a handful of locations, but at 50+ they become a flat opcode matrix that every client must scan for every verb. The missing abstraction is a hierarchical rule graph: zones contain rooms, rooms inherit a base legality schema, and dynamic modifiers (locks, keys, portals) are components attached to nodes. A dispatcher walks the graph, applying only relevant rows, turning the world into a sparse rule set rather than a monolithic table. This also isolates state changes (e.g., a lock toggling) to component updates, keeping replay determinism while preventing O(N) lookups.  

NUANCE:  
Key acquisition must be recorded as a separate ledger entry to survive room reloads, amends M2.  

DIFFERENT:  
I would externalize the legality engine as a compiled rule bytecode service, feeding the interpreter only pre‑resolved action IDs, eliminating per‑verb table scans.
