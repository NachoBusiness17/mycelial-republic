"""probe20_tasks - the 20 labeled verdict tasks (seed, v1) for probe20_run.

Split out of tools/probe20_run.py 2026-09-27 (ratchet file-too-long fix):
a pure data move, task bytes unchanged. Single-claim TRUE/FALSE probes so the
verdict-token logprob margin is well-defined. Balanced-ish 13 TRUE / 7 FALSE.
"""

TASKS = [
    {"id": "t01", "text": "The capital of France is Paris.", "answer": "TRUE"},
    {"id": "t02", "text": "Water boils at 50 degrees Celsius at sea level.", "answer": "FALSE"},
    {"id": "t03", "text": "The integer 7 is prime.", "answer": "TRUE"},
    {"id": "t04", "text": "Humans breathe nitrogen as their primary respiratory gas.", "answer": "FALSE"},
    {"id": "t05", "text": "A triangle's interior angles sum to 180 degrees.", "answer": "TRUE"},
    {"id": "t06", "text": "The Pacific Ocean is the largest ocean on Earth.", "answer": "TRUE"},
    {"id": "t07", "text": "Sound travels faster in vacuum than in air.", "answer": "FALSE"},
    {"id": "t08", "text": "The chemical symbol for gold is Au.", "answer": "TRUE"},
    {"id": "t09", "text": "There are 30 days in February in a non-leap year.", "answer": "FALSE"},
    {"id": "t10", "text": "A square has four equal sides.", "answer": "TRUE"},
    {"id": "t11", "text": "The speed of light in vacuum is about 300,000 km/s.", "answer": "TRUE"},
    {"id": "t12", "text": "Spiders are insects.", "answer": "FALSE"},
    {"id": "t13", "text": "Python is a programming language.", "answer": "TRUE"},
    {"id": "t14", "text": "The Moon orbits the Earth.", "answer": "TRUE"},
    {"id": "t15", "text": "Ice is less dense than liquid water.", "answer": "TRUE"},
    {"id": "t16", "text": "9 times 8 equals 72.", "answer": "TRUE"},
    {"id": "t17", "text": "Mount Everest is in the Andes mountain range.", "answer": "FALSE"},
    {"id": "t18", "text": "Oxygen has atomic number 8.", "answer": "TRUE"},
    {"id": "t19", "text": "A year on Mars is shorter than a year on Earth.", "answer": "FALSE"},
    {"id": "t20", "text": "The Great Barrier Reef is off the coast of Australia.", "answer": "TRUE"},
]
