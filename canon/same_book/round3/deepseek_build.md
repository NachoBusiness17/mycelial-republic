```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The House That Runs Itself</title>
<style>
  :root { --ink: #2a2118; --paper: #efe6d3; --warm: #c9a36b; }
  body { background: #14110d; color: var(--paper); font-family: Georgia, serif; margin: 0; }
  #house { max-width: 980px; margin: 0 auto; padding: 24px; }
  h1 { font-weight: normal; letter-spacing: 0.08em; border-bottom: 1px solid #4a3d2c; padding-bottom: 8px; }
  h2 { font-size: 0.95em; text-transform: uppercase; letter-spacing: 0.14em; color: var(--warm); margin-top: 28px; }
  .room { background: var(--paper); color: var(--ink); border: 1px solid #6b5941; border-radius: 4px; padding: 12px 16px; margin: 10px 0; box-shadow: inset 0 0 24px rgba(0,0,0,0.12); }
  .room .label { font-size: 0.78em; text-transform: uppercase; letter-spacing: 0.12em; color: #7a6448; }
  .cold { background: #3a332b; color: #d8ccb4; border-color: #1d1710; }
  .warm { background: #6b4a2a; color: #f6e9cf; border-color: #2d1e10; }
  pre { white-space: pre-wrap; word-break: break-word; font-size: 0.85em; line-height: 1.45; }
  .struck { text-decoration: line-through; color: #8a2016; position: relative; }
  .torn { display: inline-block; background: repeating-linear-gradient(115deg, transparent 0 4px, #d8c9ae 4px 5px); padding: 0 4px; border-bottom: 1px dashed #8a2016; }
  #lamp { width: 100%; height: 8px; background: #221b12; border-radius: 4px; overflow: hidden; }
  #lamp > div { height: 100%; width: 100%; background: linear-gradient(90deg, #ffd479, #b8862c); transition: width 0.4s; }
  .seal { display: inline-block; border: 2px solid #b8862c; border-radius: 50%; padding: 2px 8px; color: #e7c98d; font-size: 0.8em; letter-spacing: 0.1em; }
  .map { font-family: "Courier New", monospace; background: #e7dcc4; color: #3a2f22; padding: 8px 12px; border: 1px dashed #8a7a5c; }
  .note { font-size: 0.8em; color: #b8a888; }
  button { background: #3a2f22; color: #e7dcc4; border: 1px solid #6b5941; padding: 4px 10px; font-family: inherit; cursor: pointer; margin-right: 6px; }
  button:hover { background: #4d3f2e; }
  .aside { color: #9c8b70; font-style: italic; }
  .gap { display: inline-block; min-width: 8em; border-bottom: 1px solid #8a2016; color: #8a2016; text-align: center; }
</style>
</head>
<body>
<div id="house">
  <h1>The House That Runs Itself</h1>
  <p class="aside">A working account. Every system the parable implies runs here; nothing depends on a person standing still.</p>

  <h2>I. The Lamp Is Trimmed</h2>
  <div class="room cold">
    <div class="label">Corridor</div>
    <div id="lamp"><div id="lampFill"></div></div>
    <p id="lampState">Oil: full. Wick: trimmed. The flame holds without being watched.</p>
    <button onclick="trimWick()">Trim wick</button>
    <button onclick="burnOil(0.25)">Time passes (burn)</button>
  </div>

  <h2>II. The Well Is Sealed</h2>
  <div class="room">
    <div class="label">Yard</div>
    <p>Well head: <span id="wellState">sealed</span>. The lid is fixed; no bucket goes down, no name is dipped and raised changed.</p>
    <button onclick="drawFromWell()">Try the well</button>
  </div>

  <h2>III. The Ledger Is Copied</h2>
  <div class="room">
    <div class="label">Archive</div>
    <pre id="ledger"></pre>
    <button onclick="copyLedger()">Copy ledger to magistrate</button>
    <div class="note" id="magistrateNote">No copy sent.</div>
  </div>

  <h2>IV. The Map Is Checked</h2>
  <div class="room">
    <div class="label">East passage</div>
    <div class="map">
      map:  .. east wall .... dotted line .... small room
      <br>floor: [hollow] [hollow] [STONE] [hollow] [hollow]
    </div>
    <p id="mapVerdict">The linen promises an opening. The floor is the only witness. Trust the floor.</p>
    <button onclick="walkMap()">Follow the map</button>
    <button onclick="walkFloor()">Test the boards</button>
  </div>

  <h2>V. The Torn Page Is Preserved</h2>
  <div class="room">
    <div class="label">Inner room</div>
    <p>The list of names:</p>
    <pre id="tornPage"></pre>
    <p class="note">The struck line is left exactly as it is. The tear is part of the record. The blank space must be asked about.</p>
  </div>

  <h2>VI. The Seal Is Passed</h2>
  <div class="room">
    <div class="label">Hall</div>
    <p id="sealState">Seal: worn by the woman on a cord. <span class="seal">SEAL</span></p>
    <p id="tallMan">A tall man in a clean coat stands in the doorway. The servants look past him.</p>
    <button onclick="tallManOrders()">Tall man gives an order</button>
    <button onclick="passSeal()">Pass the seal to Miriam</button>
    <button onclick="threatenLedger()">Tall man threatens to take the ledger</button>
  </div>

  <h2>VII. The Corrections Are Filed Beside the Errors</h2>
  <div class="room">
    <div class="label">Register</div>
    <pre id="register"></pre>
    <div class="note">The corrections sit beside the errors, not over them. Nothing is rubbed out; everything is answered.</div>
  </div>
</div>

<script>
"use strict";

/* ---------- I. THE LAMP: trimmed, not watched ---------- */
const lampFill = document.getElementById("lampFill");
const lampState = document.getElementById("lampState");
let oil = 1.0;
let wickTrim = 1.0;

function renderLamp() {
  const light = Math.max(0, Math.min(1, oil * wickTrim));
  lampFill.style.width = (light * 100).toFixed(1) + "%";
  if (light <= 0.01) {
    lampState.textContent = "Dark. The dark does not care for counting, but the wall does not lie.";
  } else if (light < 0.35) {
    lampState.textContent = "Failing. Trim the wick; the wick is the only thing that answers.";
  } else {
    lampState.textContent = "Oil: " + oil.toFixed(2) + ". Wick: " + wickTrim.toFixed(2) + ". The flame holds without being watched.";
  }
}
function trimWick() { wickTrim = 1.0; renderLamp(); }
function burnOil(amount) { oil = Math.max(0, oil - amount); renderLamp(); }
renderLamp();

/* ---------- II. THE WELL: sealed against the dip-and-rise ---------- */
let wellSealed = true;
function drawFromWell() {
  if (wellSealed) {
    document.getElementById("wellState").textContent =
      "still sealed — the bucket is dry, no name went down, no name came up changed";
  } else {
    document.getElementById("wellState").textContent = "open — (this line should be unreachable)";
  }
}

/* ---------- III. THE LEDGER: copied, never replaced ---------- */
const ledgerNames = ["Hannah", "Josiah", "Miriam", "Elias", "Ruth", "Caleb"];
function ledgerText() {
  return "ledger of the house\n" + ledgerNames.map((n, i) => "  " + String(i + 1).padStart(2, "0") + "  " + n).join("\n");
}
document.getElementById("ledger").textContent = ledgerText();

let copiesSent = 0;
function copyLedger() {
  /* Copy is a transport, not a mutation. The original stays. */
  const copy = ledgerText() + "\n\n(attested copy — made " + new Date().toISOString() + ")";
  copiesSent += 1;
  document.getElementById("magistrateNote").textContent =
    "Copy " + copiesSent + " sent to the magistrate. Original untouched. " +
    "bytes copied: " + copy.length + ".";
}

/* ---------- IV. THE MAP: linen is checked against the floor ---------- */
let mapTrust = "unchecked";
function walkMap() {
  document.getElementById("mapVerdict").textContent =
    "The map promises an opening through the east wall. You walk the dotted line. " +
    "The floor ends at solid stone. The linen is folded and put away.";
  mapTrust = "map failed: stone";
}
function walkFloor() {
  document.getElementById("mapVerdict").textContent =
    "You put the linen in your pocket and trust the boards. " +
    "Where the floor sounds hollow, the passage is. The floor does not lie.";
  mapTrust = "floor confirmed";
}

/* ---------- V. THE TORN PAGE: preserved, blank space intact ---------- */
const tornPage = document.getElementById("tornPage");
tornPage.innerHTML =
  "  01  Hannah\n" +
  "  02  Josiah\n" +
  "  03  Miriam\n" +
  "  04  Elias\n" +
  '  05  <span class="struck">Ruth</span> <span class="torn">   (torn)</span>\n' +
  '  <span class="gap">? ? ?</span>   <-- the blank space is kept so the question survives\n' +
  "  07  Caleb\n";

/* ---------- VI. THE SEAL: worn without ceremony, obeyed by function ---------- */
let sealWornByServants = false;
let tallManStands = true;
const sealState = document.getElementById("sealState");
const tallManEl = document.getElementById("tallMan");

function tallManOrders() {
  if (!sealWornByServants) {
    tallManEl.textContent =
      "He gives an order. The servants look past him to the woman with the seal. Nothing moves. " +
      "He remains in the doorway; no one treats his standing there as a command.";
  } else {
    tallManEl.textContent =
      "He gives an order. The seal is worn without ceremony now; the servants bring bread and a chair. " +
      "He remains in the doorway. The house settles into its old quiet.";
  }
}
function passSeal() {
  sealWornByServants = true;
  sealState.innerHTML = 'Seal: worn by Miriam on a cord, without ceremony. <span class="seal">SEAL</span>';
  tallManEl.textContent =
    "The servants do not cheer. They bring bread and a chair by the fire. The tall man is still in the doorway, but the house has settled.";
}
function threatenLedger() {
  tallManEl.textContent =
    '"Give it to me," he says. "No," she says. "What will you do if I take it anyway?" ' +
    '"I will let you, and then I will tell everyone in the house exactly what you have done." ' +
    "He steps aside. The house records the step-aside as a fact, not as a victory.";
}

/* ---------- VII. CORRECTIONS FILED BESIDE ERRORS ---------- */
const registerEntries = [
  { id: 1, name: "Hannah", note: "" },
  { id: 2, name: "Josiah", note: "" },
  { id: 3, name: "Miriam", note: "" },
  { id: 4, name: "Elias", note: "correction: recorded as 'Eli', amended here; the error remains visible" },
  { id: 5, name: "Ruth", note: "correction: line struck through and torn; the tear is preserved and the correction stands beside it" },
  { id: 6, name: "", note: "correction: name unknown; the blank is filed beside the error so the question is not erased" },
  { id: 7, name: "Caleb", note: "" }
];

function renderRegister() {
  const lines = registerEntries.map(e => {
    const nameCell = e.name === "" ? "<blank>" : e.name;
    return (
      String(e.id).padStart(2, "0") + "  " + nameCell.padEnd(12) +
      (e.note ? "  ||  " + e.note : "")
    );
  });
  document.getElementById("register").textContent =
    "REGISTER (errors and corrections side by side)\n" +
    lines.join("\n");
}
renderRegister();
</script>
</body>
</html>
```