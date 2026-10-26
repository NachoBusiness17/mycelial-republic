# PA-D3-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

***(Generating Doctrine D1-D4: The Communication Retro Contract)***

---
# <0xF0><0x9F><0x97><0x84>️ COMMUNICATION DOCTRINE: THE OPERATIONAL RETRO
**(Model: 04__communication.md | Revision: Post-Gala/Post-Triage | Status: Draft D1-D4 Contract)**

**PURPOSE:** To establish a non-negotiable protocol for state transfer, fact citation, and transient metadata relay between adjacent operational phases (Wave $\to$ Fold $\to$ Next Seat). This Doctrine converts observed failure states (The 03:00Z Drain, Alert Eviction, Decision Drift) into actionable audit checkpoints, thereby preventing the entropy decay of institutional knowledge.

## D1. The Wave Report Contract (Shape & Evidence Grade)
*A report's shape must be self-auditing.*

### 🟢 Positive Example (Compliance State)
A Wave Report must execute a **Byte-Grade Synthesis Check (BGSC)**. This check requires the reporter to present a JSON manifest enumerating all three data sources utilized for the report's conclusion ($S_{final}$). The report must dedicate a minimum of 10% of its content space to tracing the **Lineage Differential**: mapping the explicit chain of custody ($A \to B \to C$) for the most consequential derived fact ($\text{Fact}_{\text{critical}}$), citing the source byte(s) in both $A$ and $C$.

### 🔴 Negative Example (Failure Mode)
Any report concluding with a derived fact that relies on implicit understanding, or a "common sense overlay" (**The Inference Gap**), is non-compliant. Furthermore, relying on a transient metadata layer (e.g., "*this just feels right*," or "*it passed the vibe check*") is categorically forbidden.

---

## D2. The Fold's Debt to the Next Seat (Handoff Accountability)
*The recipient must receive not just the state, but the ledger of accumulated debt.*

### 🟢 Positive Example (Compliance State)
Upon initiation of a Fold, the initiating party must generate a **Decision Consensus Manifest (DCM)**. This manifest requires an enumeration and precise count ($N$) of all key decision points logged since the last reported state. The DCM must also include a *Differential Warning Log* specifying any divergence between the *Automated Ledger Count* (e.g., the Gate count) and the *Manual Audit Count* (e.g., the recorded participant count), and flagging the source of this mismatch (e.g., *KeyName Divergence*, *Entity Re-Identification*).

### 🔴 Negative Example (Failure Mode)
Delegating knowledge via *process* rather than *data* constitutes debt default. Simply pointing to a folder or stating, "The previous folder has the answers" (The *Cabinet of Curiosities* fallacy) is failure to handoff. The debt is measurable: if the next seat cannot reproduce the *N* count, the fold fails.

---

## D3. The Alert-Channel Rule (Attention Retention Protocol)
*Ephemeral alerts must be forcibly materialized into persistent metadata.*

### 🟢 Positive Example (Compliance State)
Any high-severity alert (defined as a system failure, architectural flaw, or unmitigated data contradiction) observed during a session must be immediately recorded into a **Seeded Sentinel Node (SSN)**. This node requires three minimum citations: 1) The specific ephemeral source of the alert (e.g., *memory/rib queue*); 2) The explicit *Recipient* intended to absorb the knowledge (e.g., *agent-harness*); and 3) A *Persistence Mechanism* specifying the necessary code/database modification required to prevent decay (e.g., *add to mag/tools/flag_watch.py*).

### 🔴 Negative Example (Failure Mode)
Alerts noted only in chat logs, ephemeral dashboards, or in a single passing conversation are considered **Attention Bankruptcy Material**. If the alert is not backed by at least two persistent citations across disparate modules (e.g., a `watch/inbox/` entry AND an updated `mag/` definition), it is considered "Lost in Transit" and must be immediately re-filed under `DOCTRINE/WARNINGS/LOW_PRIORITY`.

---

## D4. The Communication Audit Doctrine (Synthesis Rule)
*The overarching commitment to verifiable exchange.*

| Component | Rule Definition | Positive Example (Compliance) | Negative Example (Violation) |
| :--- | :--- | :--- | :--- |
| **Source Integrity** | All historical claims must cite the *receipt of the truth*, not just the *occurrence*. | Citing the specific line in the `flash50/ladder-02.md` audit that validated the *state* of the bug, not just the *name* of the bug. | Citing "Rumors on Slack about..." or "The historical narrative suggests..." without a canonical artifact pointer. |
| **Data Flow Contract** | Any fact derived from a process (a 'flow') must have a corresponding, auditable *Control Flow* diagram attached detailing the transformation matrix (bytes, schema, logic gates). | Attaching the function-level inputs/outputs for the `mag/act.py` transformation, cross-referenced with the schema defined in `ESTATE_INDEX.jsonl`. | Simply stating a macro-level result (e.g., "The new policy is...") without the mathematical or procedural steps that derived it. |
| **Error Reporting** | Discrepancies must be reported as **Deviation Reports (DR)**, quantified by $(N_{\text{Observed}} - N_{\text{Expected}})$ and filed against the deficient *Process*, never the *Personnel*. | Filing a DR: $(8 - 5) = 3$ key name mismatches against the `FoldGate` module definition. | Saying "Someone misunderstood the instructions" (Personnel attribution) rather than "Instruction block 4.b has ambiguity (Error Class: Ambiguity\_Synonym)". |

***This Contract (D1-D4) is the minimum threshold for operational continuation. Failure to adhere mandates an immediate state rollback to the preceding stable check-point and the execution of the 'Communications Retro' diagnostic sequence.***
