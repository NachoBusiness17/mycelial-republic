# GOOGLE GEMMA BURN - gemma-4-26b-a4b-it - pass primed

round: 3 tier map (google burn 2026-10-23)
ts: 2026-10-23T04:40:44.340947+00:00
params_note: 26B sparse host, google API
lane: Google AI API via blind_probe guard pattern, $0
temp: 0.4, maxOutputTokens: 4096
ms: 87817
grade: see THE_GEMMA_GOOGLE_BURN receipt

## output (verbatim)

*   *Episode 1 (The Archivist & The Stool):* "The seat had not carried anything but him, and that even he had not stayed on it for long."
        *   *Requirement:* A system component (like a session or a state) that can hold an object/user but has a very short TTL (Time To Live) or is non-persistent. Or, more likely, a "Stool" object that can only hold one entity and expires/resets quickly.
    *   *Episode 2 (The Clerk & The Owner):* "The ink was here, and now it is not; that is theft enough... the owner pointed to the blank space where the name had been."
        *   *Requirement:* Deletion/Erasure must be permanent and leave a trace (a "tombstone" or a specific blank state) rather than just removing the record. Deleting data is treated as a significant event (an audit log entry).
    *   *Episode 3 (The Tall Man & The Seal):* "The man remained in the doorway, but no one treated his standing there as a command. [The woman with the seal] only touched the seal, and they moved."
        *   *Requirement:* Role-Based Access Control (RBAC). Presence/Status (the man) is not enough to authorize actions; a specific "Seal" (token/permission) is required to execute commands.
    *   *Episode 4 (The Map & The Stone Wall):* "The map still promised an opening, but the stone was cold and unbroken... she trusted the floor, turning back to the place where the boards still sounded hollow."
        *   *Requirement:* A routing/navigation system where the "Map" (intended path/config) might be invalid/outdated, and the system must rely on "Physicality" (actual state/truth/reality) rather than the "Map" (metadata/config). Validation must check actual existence, not just the plan.
    *   *Episode 5 (The Lamp & The Wall):* "Counting her steps... the wall did not lie... warmth meant a room with a fire... someone had been there before her."
        *   *Requirement:* Observability/Logging. In "darkness" (errors/unknown states), the system must provide sensory feedback (logs/heartbeats) and "warmth" (last-accessed timestamp/presence detection) to indicate recent activity.
    *   *Episode 6 (The Ledger & The Tall Man):* "The page showed a list of names, and at the bottom, a line had been struck through so hard the paper had torn... she would let him, and then she would tell everyone in the house exactly what he had done."
        *   *Requirement:* Immutability/Auditability. If an unauthorized attempt to modify/take data occurs, the system must record the attempt (the "torn page") and allow for a "Whistleblower" mechanism (public audit log).
    *   *Episode 7 (The Resolution):* "The seal on the cord was given to her... the ledger was copied and sent to the magistrate, and the torn page was left exactly as it was... Miriam kept the linen map... and never used it again."
        *   *Requirement:* Handover of authority (Token transfer). The audit log (torn page) remains as a permanent record of the error. The "Map" (old config) is deprecated.

    *   A "System Management Console" or "Ledger Management System."
    *   Features:
        1.  **Session/Stool:** A transient session manager.
        2.  **Register/Clerk:** A data store with "Tombstone" deletion.
        3.  **Authority/Seal:** A permission-based command executor.
        4.  **Navigation/Map:** A path validator that checks real state vs. config.
        5.  **Observability/Wall:** A log/heartbeat system with "Last Accessed" (warmth) detection.
        6.  **Audit/Ledger:** An immutable audit log that records "Torn" (failed/malicious) attempts.

    *   *HTML Structure:* A dashboard with different "Rooms" (modules).
    *   *CSS:* Dark, atmospheric, "old house" aesthetic.
    *   *JavaScript:*
        *   `Stool`: A class for transient sessions.
        *   `Register`: A class for data with tombstone deletion.
        *   `Seal`: A class for authorization.
        *   `Map`: A router that validates against the actual state.
        *   `Ledger`: An immutable log.
        *   `Observer`: A heartbeat/warmth monitor.

    *   *Stool:* `let currentSession = null;` (If set, it expires in 5 seconds).
    *   *Register:* `data.delete(id) => data[id] = { status: 'DELETED', tombstone: true };`
    *   *Seal:* `function execute(command, token) { if (token !== SEAL) throw Error; }`
    *   *Map:* `function navigate(path) { if (path.isConfigured && !path.existsInReality) return "Stone Wall"; }`
    *   *Warmth:* `item.lastAccessed = Date.now();` If `Date.now() - lastAccessed < 10000`, it's "warm".
    *   *Torn Page:* If an unauthorized `write` is attempted, the log entry is marked `[TORN]`.

    *   *Episode 1:* A "Session" button. If you click it, it stays for a moment, then vanishes.
    *   *Episode 2:* A "Register" table. Deleting a row leaves a "blank space" (tombstone).
    *   *Episode 3:* A "Command" button. It only works if the "Seal" (a checkbox/token) is active.
    *   *Episode 4:* A "Map" navigation. Clicking a "dotted line" path leads to a "Solid Stone" error if the actual object is missing.
    *   *Episode 5:* A "Corridor" view. A log that shows "steps" (events) and "warmth" (last activity).
    *   *Episode 6:* An "Audit Log" (The Ledger). If someone tries to "Take" (unauthorized access), the log shows a "Torn" entry.

    *   *The Stool:* Needs to be a transient state.
    *   *The Clerk:* Deletion must leave a "blank space".
    *   *The Seal:* Authority must be a specific token.
    *   *The Map:* Pathing must validate against reality.
    *   *The Wall:* Proximity/Activity detection.
    *   *The Ledger:* Immutable audit trail.

    (Self-Correction during drafting): Make sure the "Tall Man" is represented as a "System User" who has presence but no permission.

    *   *UI:* A single-page application.
    *   *Modules:*
        *   `SessionManager` (The Stool)
        *   `DataRegister` (The Clerk/Owner)
        *   `AccessControl` (The Seal/Tall Man)
        *   `NavigationSystem` (The Map/Stone)
        *   `EnvironmentMonitor` (The Wall/Warmth)
        *   `AuditLedger` (The Ledger/Torn Page)

    *   *Stool:* `session.expiresIn(5000)`
    *   *Clerk:* `delete(key) { registry[key] = { _tombstone: true } }`
    *   *Seal:* `if (!user.hasSeal) { log("Unauthorized attempt"); }`
    *   *Map:* `if (map.path && !reality.exists(path)) { error("Solid Stone"); }`
    *   *Warmth:* `if (Date.now() - lastSeen < 5000) return "Warm";`
    *   *Torn Page:* `log.push({ event: 'unauthorized_access', status: 'TORN' })`

    *   *The Stool:* "The seat had not carried anything but him... even he had not stayed on it for long." -> Session object that only holds one user and has a very short TTL.
    *   *The Clerk:* "The ink was here, and now it is not... the owner pointed to the blank space." -> Deletion leaves a tombstone record.
    *   *The Seal:* "The man remained in the doorway, but no one treated his standing there as a command." -> Presence != Authority. Requires `Seal` token.
    *   *The Map:* "The map still promised an opening, but the stone was cold and unbroken." -> Config vs. Reality check.
    *   *The Wall:* "Warmth meant a room with a fire." -> Activity/Heatmap based on `lastAccessed`.
    *   *The Ledger:* "A line had been struck through so hard the paper had torn." -> Audit log of failed/malicious actions.

    *   *Requirement:* "Output the artifact only."

    (Proceeding to generate HTML/CSS/JS).```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The House System Specification</title>
    <style>
        :root {
            --bg: #1a1a1a;
            --text: #d4d4d4;
            --accent: #8b0000;
            --gold: #c5a059;
            --stone: #4a4a4a;
            --paper: #e8e4d9;
        }

        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Georgia', serif;
            margin: 0;
            display: grid;
            grid-template-columns: 300px 1fr;
            height: 100vh;
            overflow: hidden;
        }

        /* Sidebar / Navigation */
        #sidebar {
            border-right: 1px solid var(--stone);
            padding: 20px;
            background: #121212;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .module-btn {
            background: none;
            border: 1px solid var(--stone);
            color: var(--text);
            padding: 10px;
            text-align: left;
            cursor: pointer;
            transition: 0.3s;
        }

        .module-btn:hover {
            background: var(--stone);
        }

        .module-btn.active {
            border-color: var(--gold);
            color: var(--gold);
        }

        /* Main Content Area */
        #main {
            padding: 40px;
            overflow-y: auto;
            position: relative;
        }

        .module {
            display: none;
            max-width: 800px;
            margin: 0 auto;
        }

        .module.active {
            display: block;
        }

        h2 { color: var(--gold); border-bottom: 1px solid var(--stone); padding-bottom: 10px; }

        /* Episode 1: The Stool (Transient Session) */
        #stool-status { font-style: italic; color: #888; }
        .stool-active { color: var(--gold) !important; }

        /* Episode 2: The Register (Tombstone Deletion) */
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #222; }
        th, td { border: 1px solid var(--stone); padding: 10px; text-align: left; }
        .tombstone { color: #555; font-style: italic; background: #1a1a1a; }

        /* Episode 3: The Seal (RBAC) */
        .authority-panel { border: 2px solid var(--stone); padding: 20px; margin-top: 20px; }
        .seal-icon { font-size: 2em; cursor: pointer; opacity: 0.3; transition: 0.5s; }
        .seal-active { opacity: 1; color: var(--gold); text-shadow: 0 0 10px var(--gold); }

        /* Episode 4: The Map (Config vs Reality) */
        .map-container { background: var(--paper); color: #333; padding: 20px; border-radius: 5px; }
        .dotted-line { border-bottom: 2px dotted #333; display: inline-block; width: 100px; }

        /* Episode 5: The Wall (Observability/Warmth) */
        .corridor-view { background: #000; color: #fff; padding: 20px; height: 200px; position: relative; overflow: hidden; }
        .warmth-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 5px; }

        /* Episode 6: The Ledger (Immutable Audit/Torn Page) */
        #audit-log { background: var(--paper); color: #222; padding: 20px; font-family: monospace; min-height: 150px; white-space: pre-wrap; border: 1px solid #ccc; }
        .torn-entry { text-decoration: line-through; color: var(--accent); font-weight: bold; }

        button { cursor: pointer; padding: 5px 15px; }
    </style>
</head>
<body>

<div id="sidebar">
    <h3 style="color: var(--gold)">The House System</h3>
    <button class="module-btn active" onclick="showModule('stool')">The Archivist (Session)</button>
    <button class="module-btn" onclick="showModule('register')">The Clerk (Register)</button>
    <button class="module-btn" onclick="showModule('seal')">The Hall (Authority)</button>
    <button class="module-btn" onclick="showModule('map')">The Map (Navigation)</button>
    <button class="module-btn" onclick="showModule('corridor')">The Corridor (Observability)</button>
    <button class="module-btn" onclick="showModule('ledger')">The Ledger (Audit)</button>
</div>

<div id="main">
    <!-- Episode 1: The Stool -->
    <div id="stool" class="module active">
        <h2>The Archivist's Stool</h2>
        <p>Requirement: A session that can hold only one entity and expires rapidly.</p>
        <button onclick="occupyStool()">Sit on the Stool</button>
        <p id="stool-status">The stool is empty.</p>
    </div>

    <!-- Episode 2: The Register -->
    <div id="register" class="module">
        <h2>The Clerk's Register</h2>
        <p>Requirement: Deletion must leave a "tombstone" (blank space) rather than removing the record.</p>
        <table id="register-table">
            <thead><tr><th>Name</th><th>Status</th></tr></thead>
            <tbody id="register-body"></tbody>
        </table>
        <br>
        <button onclick="addName()">Add Name</button>
    </div>

    <!-- Episode 3: The Seal -->
    <div id="seal" class="module">
        <h2>The Inner Hall</h2>
        <p>Requirement: Presence (Tall Man) is not Authority. Authority requires the Seal.</p>
        <div class="authority-panel">
            <div id="tall-man-status">Status: A tall man stands in the doorway.</div>
            <hr>
            <div id="seal-container">
                <span id="seal-icon" class="seal-icon">📿</span>
                <button onclick="toggleSeal()">Toggle Seal Ownership</button>
            </div>
            <br>
            <button onclick="attemptCommand()">Issue Command</button>
            <p id="command-result"></p>
        </div>
    </div>

    <!-- Episode 4: The Map -->
    <div id="map" class="module">
        <h2>The Linen Map</h2>
        <p>Requirement: Navigation must validate against physical reality, not just the configuration.</p>
        <div class="map-container">
            <p>Path: East Wall <span class="dotted-line"></span> Small Room</p>
            <button onclick="navigate()">Follow the Dotted Line</button>
            <p id="nav-result"></p>
        </div>
    </div>

    <!-- Episode 5: The Corridor -->
    <div id="corridor" class="module">
        <h2>The Dark Corridor</h2>
        <p>Requirement: Observability via "warmth" (last activity) and "counting" (event logging).</p>
        <div class="corridor-view" id="corridor-view">
            <div id="corridor-log"></div>
        </div>
        <p>Current Sensor Data: <span id="warmth-status">Cold</span></p>
        <button onclick="touchWall()">Press against the wall</button>
    </div>

    <!-- Episode 6: The Ledger -->
    <div id="ledger" class="module">
        <h2>The Ledger</h2>
        <p>Requirement: Immutable audit log. Unauthorized attempts leave a "torn" (struck-through) record.</p>
        <div id="audit-log"></div>

