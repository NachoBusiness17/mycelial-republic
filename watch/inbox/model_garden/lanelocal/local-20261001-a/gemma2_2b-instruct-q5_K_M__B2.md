# garden-v1-B2 | gemma2:2b-instruct-q5_K_M | series local-20261001-a | instrument=lane-local-script
# finish=stop prompt_tokens=4099 completion_tokens=540 wall_s=23.89 tok_s=22.6 checks=1/5 {'SHAPE': 0, 'CITES-RESOLVE': 0, 'LINES-IN-RANGE': 0, 'NO-EM-DASH': 1, 'DISTINCT-EVIDENCE': 0}

```json
[{"condition": "missing_source_verification", "priority": 1, "eligible_organ": "ghost_memlance", "capability": "tool_invoke", "reason": "Board lacks active source verification stream"},
{"condition": "missing_fork_verdicts", "priority": 2, "eligible_organ": "verkle_lance", "capability": "verkle_link", "reason": "Fork resolutions are prose-only, not knotted"},
{"condition": "board_quiescent", "priority": 3, "eligible_organ": "swarm_cycle", "capability": "lane_spawn", "reason": "Board has <5 notes; suggest cycle run"},]
```

 
* **Format:** The JSON array consists of dictionaries with the following key-value structures:

    * **`condition`**: Description of the unmet need. 
    * **`priority`**: Priority level (higher number means more urgency).
    * **`eligible_organ`**: The entity responsible for the unmet need.
    * **`capability`**:  The relevant capability the organ requires to fulfill the need.
    * **`reason`**: Reasoning behind the unmet condition. 


 

 

 
**Explanation:**

1. **Unmet Condition Extraction:**  The code identifies situations where the "board" (presumably a service providing a source of verification) is missing crucial aspects needed to process actions: 
    * "missing_source_verification" - a requirement from the "tool invoke" capability needs verification from a source.
    * "missing_fork_verdicts" -  "verkle_link" needs to check for multiple forks, which are expressed as prose-based resolutions
    * "board_quiescent" requires a swarm cycle to get active.


2. **Data Representation:** 
    * **Clarity:** The structured output is easily readable and informative, making debugging and understanding the board's situation straightforward. 


3. **Example Usage:** You could use these outputs to: 
    * Identify and prioritize which situations necessitate immediate action from the "switchboard"
    * Inform the "switchboard" about necessary resource allocation
    * Guide the development team toward fixing the board's deficiencies.
 
 
 



Let me know if you'd like to explore other, specific requirements for the contract's deliverables. This example focuses on the format you provide in the `reconcile()` method, and I can expand based upon your needs. .  
