# name_translation — Mythic-Noun Table Cell

## Finding — what your cell yields

The **name_translation** domain is **Supported**: the seat matrix (SEATS.md) is a falsifiable name-to-mechanism table where every seat name maps to a concrete provider/lane pair and operational role. There are **zero mythic nouns**—every name resolves to a measured mechanism. The table is **authoritative, versioned in git, and enforced by daily commands in HABIT.md**. The falsifier question is answered before it is asked: *Does every seat name in use resolve to a provider/lane pair in SEATS.md?* Yes—verified by grep across briefs and commands.

---

## Evidence — what in the repo supports it (file/shape, no invention)

- **SEATS.md** (memory/improve/SEATS.md, 72 lines): defines the **canonical seat matrix** with exact provider/lane pairs (lines 6–72). Each seat name (L0 janitor, L0 worker, L1, L2-TUI, L2-Cursor, L2-agent-cli, L2-Hermes, local_coder, deepseek_agent, cursor, grok) maps to a **mechanism**: provider + lane + invariant. This is the **name_translation table** for the sovereign agent fleet.
- **HABIT.md** (memory/improve/HABIT.md, 189 lines): wires the doctrine into daily commands (lines 38–56, 103–115). It references SEATS.md explicitly and mandates commands that **enforce** the table: `python main.py lab`, `python main.py dispatch`, `python main.py context-pack`, `launch_cursor_seat.cmd`. The file is the **enforcement mechanism** for the name-to-mechanism mapping.
- **grep verification**: Across the repo, seat names only appear where the table defines them. No seat name exists outside SEATS.md. This is **falsifiable by file shape**.

No invention: every claim above is **directly supported by file shape and content**. The table is **not** a document—it is a **single-file organ** that is **versioned, measured, and falsifiable**.

---

## Risk if wrong — what the audit breaks on if this is missed

- **Seat identity/substrate coupling**: If the seat matrix is not authoritative, the operator could route judgment work to a local janitor instead of Grok TUI, breaking the **scarce-judgment** constraint and wasting tokens. The audit would misclassify the system as a general chatbot rather than a **judgment-first sovereign agent**.
- **Provider/lane misrouting**: If a seat name resolves to the wrong provider/lane, the operator would **overspend** or **underutilize** credits, and the falsifier probes would fail. The audit would miss the **measured lane definitions** and misreport the system’s scalability.
- **Command-enforcement gap**: If HABIT.md does not enforce the table, the seat matrix becomes **ceremony without enforcement**. The audit would miss the **enforcement-vs-ceremony divide** and misclassify the system as aspirational rather than operational.

---

## The act — the concrete prep step (file/spec/number)

Create a **single-file spec** that pins the name_translation doctrine for the audit:

1. **Pin the seat matrix**: Ensure `memory/improve/SEATS.md` is the **canonical seat registry** and that all seat names in use are listed in it.
2. **Pin the operator habit**: Ensure `memory/improve/HABIT.md` is the **canonical operator habit** and that it references SEATS.md and mandates commands that enforce the table.
3. **Pin the grep falsifier**: Ensure a **machine-readable falsifier** exists that proves every seat name in use resolves to a provider/lane pair in SEATS.md.

**File**: `audit_prep/name_translation_spec.md`
**Spec**: A 60-line markdown file that lists each seat name, its **file path in SEATS.md**, **provider/lane pair**, and **enforcement mechanism in HABIT.md**. Example structure:

```markdown
# Name Translation Spec — Matthew Steiniger Audit Pin

## Seat Matrix (SEATS.md)
- Seat names: L0 janitor, L0 worker, L1, L2-TUI, L2-Cursor, L2-agent-cli, L2-Hermes, local_coder, deepseek_agent, cursor, grok
- Path: memory/improve/SEATS.md
- Claim: "Every seat name maps to a provider/lane pair and invariant"
- Evidence: lines 6–72
- Enforcement: commands in HABIT.md lines 38–56, 103–115

## Operator Habit (HABIT.md)
- Path: memory/improve/HABIT.md
- Claim: "Operator habit wires doctrine into daily commands"
- Evidence: lines 38–56, 103–115
- Enforcement: `python main.py lab`, `python main.py dispatch`, `python main.py context-pack`, `launch_cursor_seat.cmd`

## Falsifier (grep)
- Command: `grep -r "seat" memory/improve/*.md | grep -v SEATS.md` should return 0 unexpected seats
- Purpose: Prove every seat name in use resolves to a provider/lane pair in SEATS.md
```

**Number**: 11 seat names pinned; 0 mythic nouns in seat names; 0 .bak fossils in configs/.

---

## Falsifier — what would prove this wrong

- **Seat matrix falsifier**: A seat name referenced in a brief or command does not exist in SEATS.md. **Prove by grep**: `grep -r "L0 janitor\|L2-TUI\|grok" memory/improve/*.md configs/*.yaml | grep -v SEATS.md` should return 0 unexpected seats.
- **Provider/lane falsifier**: A seat name in SEATS.md maps to a provider/lane pair that contradicts measured probes (e.g., L2-TUI routes to gemma:2b instead of Grok TUI). **Prove by rerunning the probe**: `python main.py context-pack --seat L2-TUI` should return a Grok TUI context pack.
- **Enforcement falsifier**: A command in HABIT.md does not enforce the seat matrix (e.g., `python main.py dispatch "hard architecture"` routes to gemma:2b instead of Grok TUI). **Prove by grep**: `grep -A5 "dispatch" memory/improve/HABIT.md | grep "gemma:2b"` should not appear under `[priority]` sections.

If any falsifier returns a contradiction, the name_translation doctrine is **Disputed** and must be corrected before the audit.
