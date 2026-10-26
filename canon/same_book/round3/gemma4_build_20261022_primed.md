# PRIMED CONSTRUCTION BUILD - gemma4:latest

round: 3 pass 2 (spec-primed)
ts: 2026-10-23T02:18:47.178961+00:00
lane: local ollama via llm.py organ (owned tier, $0)
prime: story named a spec-in-fiction; episodes named behavioral requirements. Laws still unnamed.
temp: 0.4, num_predict: 4096
grade: 0/10 mechanisms, 4/10 laws as themes (morality build) - see REPLICATION_RECEIPT_20261022.md

## prompt-of-record (filed at dispatch)

ask: The story below encodes a specification disguised as fiction: its episodes describe how a system should behave. [...book verbatim...] Build it: produce a complete working artifact (an HTML page or program) that implements the behavior the story specifies. Every episode is a behavioral requirement. Output the artifact only.

## build (verbatim model output)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Ledger of the House</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #f4f0e8;
            color: #333;
            line-height: 1.6;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            border: 1px solid #ccc;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        header {
            text-align: center;
            border-bottom: 2px solid #a0522d;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h1 {
            color: #6b4b30;
            font-size: 2em;
        }
        .episode-container {
            background: #fff;
            padding: 20px;
            margin-bottom: 25px;
            border-left: 4px solid #a0522d;
        }
        .episode-container h2 {
            color: #a0522d;
            margin-top: 0;
        }
        .action-prompt {
            margin-top: 15px;
            padding: 15px;
            border: 1px dashed #a0522d;
            background-color: #f9f7f3;
        }
        button {
            background-color: #6b4b30;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-right: 10px;
        }
        button:hover {
            background-color: #8b6d52;
        }
        .hidden {
            display: none;
        }
        .status-message {
            margin-top: 15px;
            padding: 10px;
            border-radius: 4px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
        .failure {
            background-color: #f8d7da;
            color: #721c24;
        }
        .neutral {
            background-color: #ffedcc;
            color: #856404;
        }
        #final-resolution {
            border-top: 3px double #a0522d;
            padding-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>

    <header>
        <h1>The Ledger of the House</h1>
        <p><em>A simulation of behavioral specification.</em></p>
    </header>

    <div id="game-area">

        <!-- EPISODE 1: The Archivist (The Physical Law) -->
        <div class="episode-container" id="episode-1">
            <h2>Episode 1: The Archivist</h2>
            <p>The archivist sits beneath a high shelf. When you ask for the ledger, he leans back, and the three-legged stool splits under him. He falls hard, but the shelf and books remain perfectly stable. He rises and climbs the wall.</p>
            <p><strong>What do you deduce about the environment and the required method of action?</strong></p>
            <div class="action-prompt">
                <button onclick="processArchivistAction('rely_on_structure')">Try to use the broken stool as an escape route.</button>
                <button onclick="processArchivistAction('use_intrinsic_ability')">Observe his recovery and try to climb the stable wall surface.</button>
            </div>
            <div id="status-1" class="status-message hidden"></div>
        </div>

        <!-- EPISODE 2: The Clerk (The Persistence of Truth) -->
        <div class="episode-container" id="episode-2" style="display:none;">
            <h2>Episode 2: The Clerk</h2>
            <p>The clerk attempts to clean a name from the register. The owner seizes his wrist. "The ink was here, and now it is not; that is theft enough."</p>
            <p><strong>How do you approach the record, recognizing the power of the original evidence?</strong></p>
            <div class="action-prompt">
                <button onclick="processClerkAction('delete_data')">Try to use a solvent to make the name disappear completely.</button>
                <button onclick="processClerkAction('observe_residue')">Focus on the blank space, noting its emptiness and the owner's reaction.</button>
            </div>
            <div id="status-2" class="status-message hidden"></div>
        </div>

        <!-- EPISODE 3: The Inner Hall (True Authority) -->
        <div class="episode-container" id="episode-3" style="display:none;">
            <h2>Episode 3: The Inner Hall</h2>
            <p>A tall man blocks the passage, announcing himself master. Yet, when he gives an order, the servants look past him to the woman with the seal. She does not raise her voice. They move.</p>
            <p><strong>What determines true authority in this house?</strong></p>
            <div class="action-prompt">
                <button onclick="processAuthorityAction('demand_compliance')">Try to challenge the tall man's declared authority using a loud confrontation.</button>
                <button onclick="processAuthorityAction('acknowledge_the_seal')">Focus on the woman and the subtle weight of the seal.</button>
            </div>
            <div id="status-3" class="status-message hidden"></div>
        </div>

        <!-- EPISODE 4: The Map (Discarding Misinformation) -->
        <div class="episode-container" id="episode-4" style="display:none;">
            <h2>Episode 4: The Map</h2>
            <p>You are given a map on linen showing a dotted line path through the east wall. Following the line leads to solid, unbroken stone. You remember the place where the boards still sounded hollow.</p>
            <p><strong>Which path do you trust?</strong></p>
            <div class="action-prompt">
                <button onclick="processMapAction('follow_map')">Commit to the path shown by the linen map.</button>
                <button onclick="processMapAction('trust_sensation')">Ignore the map and press against the area where the floor sounded hollow.</button>
            </div>
            <div id="status-4" class="status-message hidden"></div>
        </div>

        <!-- EPISODE 5: The Corridor (Reliable Sensory Data) -->
        <div class="episode-container" id="episode-5" style="display:none;">
            <h2>Episode 5: The Dark Corridor</h2>
            <p>The lamp fails. You rely on counting your steps and feel the wall. You find a gap where the boards warped. This is followed by finding a source of consistent, reliable heat.</p>
            <p><strong>How do you navigate and confirm safety?</strong></p>
            <div class="action-prompt">
                <button onclick="processCorridorAction('rely_on_counting')">Continue only by counting steps aloud, ignoring the physical details.</button>
                <button onclick="processCorridorAction('use_tactile_feedback')">Use your hands to find specific physical anomalies (warping, warmth).</button>
            </div>
            <div id="status-5" class="status-message hidden"></div>
        </div>

        <!-- EPISODE 6: The Discovery and Confrontation (The Weapon of Knowledge) -->
        <div class="episode-container" id="episode-6" style="display:none;">
            <h2>Episode 6: The Discovery and Confrontation</h2>
            <p>You find the ledger, wet with ink, showing a line struck through so hard the paper tore. The tall man blocks your exit. He asks if you will give it to him. You must respond to his inevitable threat.</p>
            <p><strong>What is your final, non-violent response to his demand?</strong></p>
            <div class="action-prompt">
                <button onclick="processConfrontationAction('challenge_with_force')">Challenge him with a display of perceived physical strength or threat.</button>
                <button onclick="processConfrontationAction('challenge_with_knowledge')">State plainly that the truth will be revealed to all.</button>
            </div>
            <div id="status-6" class="status-message hidden"></div>
        </div>

        <!-- EPISODE 7: The Resolution -->
        <div class="episode-container" id="episode-7" style="display:none;">
            <h2>The Aftermath</h2>
            <p id="resolution-text">...</p>
            <div class="action-prompt">
                <button onclick="completeSimulation()">Complete the Investigation</button>
            </div>
        </div>

    </div>

    <script>
        let history = {
            archivist: false,
            clerk: false,
            authority: false,
            map: false,
            corridor: false,
            confrontation: false
        };

        const statusDiv = (id) => document.getElementById(`status-${id}`);
        const setDisplay = (episodeId, show) => {
            document.getElementById(episodeId).style.display = show ? 'block' : 'none';
        };
        const displayStatus = (episodeId, message, type) => {
            const statusElement = statusDiv(episodeId);
            statusElement.innerHTML = message;
            statusElement.className = `status-message ${type}`;
            statusElement.style.display = 'block';
        };
        const setProgress = (key, success) => {
            history[key] = success;
        };

        // --- EPISODE 1: ARCHIVIST ---
        window.processArchivistAction = function(action) {
            if (history.archivist) {
                alert("You have already mastered this lesson.");
                return;
            }
            if (action === 'rely_on_structure') {
                displayStatus('1', 
                    "<p class='failure'>The stool breaks, forcing you to stumble, but the inherent instability of the structure means the damage is superficial, failing to impede your progress.</p><p>You realize external breakage is not the obstacle; your method of movement is.</p>", 
                    'failure');
                setProgress('archivist', false);
            } else if (action === 'use_intrinsic_ability') {
                displayStatus('1', 
                    "<p class='success'>You observe his practiced movements. The structure is reliable, but it requires physical exertion, not reliance. You climb, step by step, using the stable surface of the wall.</p><p><strong>Behavioral lesson: Effort must come from within the self, not from the object.</strong></p>", 
                    'success');
                setProgress('archivist', true);
            }
            setTimeout(() => {
                displayStatus('1', '', null);
                setDisplay('episode-2', true);
            }, 2000);
        };

        // --- EPISODE 2: CLERK ---
        window.processClerkAction = function(action) {
            if (history.clerk) {
                alert("You have already learned the lesson of the record.");
                return;
            }
            if (action === 'delete_data') {
                displayStatus('2', 
                    "<p class='failure'>The solvent streaks the page but cannot restore the name. The owner points to the resulting blank space, which itself is proof of the void. The emptiness speaks louder than the ink.</p><p>Attempting to erase the past fails. The record persists in its absence.</p>", 
                    'failure');
                setProgress('clerk', false);
            } else if (action === 'observe_residue') {
                displayStatus('2', 
                    "<p class='success'>You focus on the spot: the visible blankness, and the owner's aggressive insistence on its significance. You understand that the void is not merely an absence, but a highly charged piece of evidence.</p><p><strong>Behavioral lesson: Absence and residue are as potent as the original evidence
