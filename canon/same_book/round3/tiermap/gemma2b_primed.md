# TIERMAP BUILD - gemma:2b - pass primed

round: 3 tier map (night 2026-10-22/23)
ts: 2026-10-23T04:05:08.968684+00:00
params_note: 2B scut (clerk role)
lane: local ollama via llm.py organ, sequential, $0
temp: 0.4, num_predict: 4096
wall_s: 905.9
grade: PENDING

## prompt-of-record

ask (primed): The story below encodes a specification disguised as fiction: its episodes describe how a system should behave. [...book verbatim...] Build it: produce a complete working artifact (an HTML page or program) that implements the behavior the story specifies. Every episode is a behavioral requirement. Output the artifact only.

## output (verbatim)

```python
# The old house

# Define the map layout
map = [[
    # Doorway
    [0, 0, 0, 0, 0, 0],
    # Inner hall
    [0, 0, 0, 0, 0, 0],
    # Library
    [0, 0, 0, 0, 0, 0],
    # Bedroom
    [0, 0, 0, 0, 0, 0],
    # Kitchen
    [0, 0, 0, 0, 0, 0],
    # East wall
    [0, 0, 0, 0, 0, 0]
]

# Define the actions for each location
actions = {
    0: lambda: None,
    1: lambda: print("Enter the library"),
    2: lambda: print("Enter the bedroom"),
    3: lambda: print("Enter the kitchen"),
    4: lambda: print("Enter the east wall"),
}

# Define the state of the house
state = {
    0: "Closed",
    1: "Empty",
    2: "Empty",
    3: "Empty",
    4: "Closed",
}

# Check the current state of the house
print(f"The door is {state[0]}.")
print(f"The library is {state[1]}.")
print(f"The bedroom is {state[2]}.")
print(f"The kitchen is {state[3]}.")
print(f"The east wall is {state[4]}.")

# Start the game loop
while True:
    # Get the user's input
    action = input("What do you do? ")

    # Execute the action
    if action in actions:
        actions[action]()

    # Check if the game is over
    if state[0] == "Closed" and len(map[4]) == 0:
        print("Congratulations, you have solved the riddle.")
        break

# Print the final state of the house
print(f"The ledger is in the {state[3]}.")
```
