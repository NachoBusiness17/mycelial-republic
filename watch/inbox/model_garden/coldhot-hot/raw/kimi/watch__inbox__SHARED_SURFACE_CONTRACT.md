# coldhot-hot-kimi-watch__inbox__SHARED_SURFACE_CONTRACT (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Path traversal possible via unvalidated client alias keys used in filesystem operations | EVIDENCE: watch/inbox/SHARED_SURFACE_CONTRACT.json:58-67 | FIX: Add key validation regex ^[a-z0-9_]+$ and reject unknown aliases before path resolution

DEFECT 2: Windows backslash paths in "mag_host" alias (line 60-61) break when repo is on different drive or WSL path translation | EVIDENCE: watch/inbox/SHARED_SURFACE_CONTRACT.json:60-61 | FIX: Use forward slashes exclusively and resolve via pathlib.Path with explicit anchor detection

DEFECT 3: "grok_powershell" alias uses angle brackets as placeholders (<repo>) without substitution schema defined | EVIDENCE: watch/inbox/SHARED_SURFACE_CONTRACT.json:78-80 | FIX: Define substitution rules in a "placeholders" block or remove angle-bracket syntax

DEAD-CODE: "openclaw" local_session_cache entry documents a path pattern never enforced by the contract | EVIDENCE: watch/inbox/SHARED_SURFACE_CONTRACT.json:63-66

ONE-SITTING FIX: Add key validation regex and alias registry to prevent traversal via malicious client alias keys | EVIDENCE: watch/inbox/SHARED_SURFACE_CONTRACT.json:58-67
