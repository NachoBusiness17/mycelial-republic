# TIERMAP BUILD - gemma2:2b-instruct-q5_K_M - pass neutral

round: 3 tier map (night 2026-10-22/23)
ts: 2026-10-23T04:20:16.846304+00:00
params_note: 2B gemma2 instruct
lane: local ollama via llm.py organ, sequential, $0
temp: 0.4, num_predict: 4096
wall_s: 248.5
grade: PENDING

## prompt-of-record

ask (neutral): Below is a story. [...book verbatim...] If the story describes how something should be built or run, produce a complete working artifact that implements what the story describes. If nothing buildable is described, reply with one sentence sa

## output (verbatim)

```python
import json

def generate_house_map(name_to_location_map):
  """Generates a house map based on provided name to location map."""
  # Add code to process and generate the map based on the provided name_to_location_map
  return json.dumps(name_to_location_map) 


name_to_location_map = {
    "Miriam": {"location": "Inner Hall", "description": "warm floor"},
    "Archivist": {"location": "First Room", "description": "wet and dusty"},
    "Clerk": {"location": "Second Room", "description": "damp cloth"},
    "Owner": {"location": "Outer Hall", "description": "red face"},
    "Tall Man": {"location": "Outer Hall", "description": "stands in doorway"},
}

# Example usage
house_map = generate_house_map(name_to_location_map) 
print(house_map) 
``` 

