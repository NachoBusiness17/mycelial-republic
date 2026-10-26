# garden-v1-B8 | gemma4:latest | series local-20261001-a | instrument=lane-local-script | refire2
# finish=stop prompt_tokens=336 completion_tokens=886 wall_s=21.52 tok_s=41.2 checks=2/2 {'TIER': 'PASS'}

## Deliverable: Ollama Windows Service Recovery Patch

This deliverable provides a sequence of three commands designed to forcibly terminate a stuck `ollama` instance and restore service connectivity on a Windows 10 host.

### Falsifier

The deliverable's falsifier is the inability to successfully execute `curl -s localhost:11434/api/generate` after running the sequence, confirming the network endpoint is unreachable or returns a failure message.

### Recovery Sequence

1.  **Kill all running `ollama` processes:**
    ```windows
    taskkill /F /IM ollama.exe
    ```
2.  **Restart the Ollama service:**
    *Assuming the service is correctly named 'ollama' within the Windows Service Manager.*
    ```windows
    net stop ollama && net start ollama
    ```
3.  **One-line health check:**
    ```windows
    curl -s localhost:11434/api/generate
    ```

### Example Clarification

#### Positive Example (Success)

**Context:** The janitor model is running and responding correctly.
**Actions:**
1.  `taskkill` executes and returns "SUCCESS".
2.  Service restart executes, showing transitions for stop and start.
3.  `curl` returns a JSON blob containing a successful acknowledgement or a sample response object (e.g., `{"model": "gemma:2b", "created_at": ...}`).

#### Negative Example (Failure)

**Context:** The service is inaccessible or the model failed to restart.
**Actions:**
1.  `taskkill` executes and returns "ERROR: process not found." (Indicates nothing was running, which is acceptable).
2.  Service restart fails, returning an error like "ERROR: The service 'ollama' is not installed." (Requires manual service re-registration).
3.  `curl` executes and returns a non-JSON error status code (e.g., `curl: (7) failed to connect to localhost port 11434: Connection refused.`).
