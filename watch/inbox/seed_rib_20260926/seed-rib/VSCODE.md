# VSCODE — "download VS Code and use this with the free models"

The path of least resistance from zero to your own estate, in an editor you already know:

1. **Install VS Code** (code.visualstudio.com) and the **Cline** extension (or Continue/Roo —
   any agent extension that reads `AGENTS.md` and takes an OpenAI-compatible endpoint).
2. **Put this seed folder in your project.** Cline-style tools auto-read `AGENTS.md` —
   which points them at FIRST_BOOT and the 11 laws. The method rides along automatically.
3. **Give it a free model:** OpenRouter key (ACCOUNTS.md) → model settings → pick from the
   `:free` wall (nemotron, nex, gemma, gpt-oss — whatever the sweep currently scores best).
   The two-account trick doubles your ceiling.
4. **Talk, work, save.** Everything the agent writes lands in YOUR folder as files —
   markdown records, append-only. That is the whole product: your data, your disk,
   your keys, your models.

**The browser path:** `opencode` (open source) serves a web UI *and* an API from one
command — `opencode serve` — the estate's own NPC-dialogue lane runs this way. Point it
at the same keys; use it from your phone's browser if you want.

**The engine path:** `python engines/cooker.py status` + a scheduled `fire --due` —
your free compute burns on refills without you watching (see MORNING_LOOP.md).
