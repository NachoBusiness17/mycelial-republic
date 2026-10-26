# garden-v1-B8 | gemma2:2b-instruct-q5_K_M | series local-20261001-a | instrument=lane-local-script
# finish=stop prompt_tokens=486 completion_tokens=177 wall_s=3.73 tok_s=47.4 checks=1/2 {'TIER': 'PARTIAL'}

## CONTRACT

1. `taskkill /pid <ProcessID of Ollama Process>.`
2. `net stop ollama service`
3. `net start ollama service`
4. `gemma-health-check` 
   - This should be defined based on your specific implementation of gemma's health-check functionality.  Example could be in-memory, filesystem, etc.



## EVIDENCE

1.  `taskkill /pid <ProcessID of Ollama Process>`
2. `net stop ollama service` 
3.  `net start ollama service`



This is a one-line script.  A more detailed solution would involve a more involved health check solution to determine when the model has been restored fully, and other checks to verify if the service has been fully restarted. 

