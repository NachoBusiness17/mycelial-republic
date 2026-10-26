# garden-v1-B5 | gemma2:2b-instruct-q5_K_M | series local-20261001-a | instrument=lane-local-script
# finish=stop prompt_tokens=5684 completion_tokens=336 wall_s=28.47 tok_s=11.8 checks=1/5 {'SHAPE': 0, 'CITES-RESOLVE': 0, 'LINES-IN-RANGE': 0, 'NO-EM-DASH': 1, 'DISTINCT-EVIDENCE': 0}

```yaml
"deliverable": {
    "file_name": "mag_steer_seal.py",
    "source": [
        "the code for a Mag-specific steering guide",
        "an in-depth review of each section of the steering logic"
    ],
    "content":  ```
    # this code is a detailed guide on how to implement a Mag-specific guidance system
    # based on an existing steering system's core
    # this will include code that handles multiple use-cases including
    # different modes such as 'enforce' (more restrictive) and 'warn' (less strict);
    # this implementation leverages existing Mag-specific files such as:
    # -  `mag/steer_seal.py` (for basic code)
    # -  `mag/steer_seal_key` (for handling key files)
    # -  `mag/steer_seal_mode` (for handling mode
    # - `mag/steer_seal_log.jsonl`  (for logging)
    # -  `mag/steer_seal_trust.json`  (for audit trail)

    ...
    # The "restrictive" grammar of an injectable word is crucial:
    # -  A "STOP" in any language (Cyrillic "Te/O/Er" in Cyrillic) is a
    # strict stop, regardless of what it looks like
    # -  This grammar is what we're going to try and protect against

```
}
```
