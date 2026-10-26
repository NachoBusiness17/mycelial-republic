# swarm1-glm-flash-mag__perplexity_research (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: CLI flag as final argument crashes with an unhandled IndexError instead of the JSON status fallback | EVIDENCE: mag/perplexity_research.py:272-280 | FIX: guard i+1 < len(argv) before argv[i+1] for --model and --route, else print status and return 1
DEFECT 2: leaf filename uses second-resolution UTC timestamp, so two research calls in the same second silently overwrite the first leaf | EVIDENCE: mag/perplexity_research.py:150-151 | FIX: append uuid4().hex[:8] or a monotonic counter to the leaf filename
DEFECT 3: int(max_results) / int(max_tokens) ValueError escapes research() as a raw exception, violating the {"ok": False} error-contract every other failure path returns | EVIDENCE: mag/perplexity_research.py:193,196,207 | FIX: wrap _search_body call at line 207 in try/except and return the ok=False schema dict on bad numerics
DEAD-CODE: the `if max_results is not None else 10` fallback branch is unreachable: the only caller passes a defaulted int (max_results: int = 10) | EVIDENCE: mag/perplexity_research.py:193,238
ONE-SITTING FIX: add argv-bounds checks to the --model/--route parsing in main so the CLI degrades to a status print instead of a traceback | EVIDENCE: mag/perplexity_research.py:271-284
