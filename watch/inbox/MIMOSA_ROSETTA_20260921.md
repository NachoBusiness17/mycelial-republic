# MIMOSA ROSETTA — the security gate's Chinese verdicts, translated (2026-09-21)
**Purpose:** Mimosa guards every Write/Edit in the estate (PreToolUse scan + block,
PostToolUse). Its verdicts arrive in Chinese. Any seat or tool hitting them
translates on sight and fixes the flagged pattern — the gate is legitimate and
has caught real defects (2026-09-21: path traversal in estate_smith_chart,
eval-in-test in cathedral_smoke, SSRF in blind_probe).

## Fixed vocabulary
| Chinese | English |
|---|---|
| 发现高危 / 中危 / 低危 | high / medium / low severity finding |
| 路径穿越 | path traversal (unvalidated path) |
| 代码注入 | code injection (dynamic execution of external input) |
| SSRF 服务端请求伪造 | server-side request forgery |
| 已拦截写入 | write blocked |
| 请改用安全写法 | rewrite with the safe pattern |
| 建议 | remediation hint |
| 只处理与本次候选代码直接相关的修复 | fix only what this candidate touched — no scope creep |
| 正在检查候选代码… | scanning candidate code… |
| 正在检查命令与 Git 门禁… | checking command and Git gate… |

## Standing rules
1. Seat replies, filed records, and register purposes stay English — translate
   or strip hook Chinese, never propagate it (plain-English law, 09-21).
2. The gate is fail-closed for security findings and its feedback is
   actionable: fix the flagged pattern in the same write.
3. Its scans are also available on demand for the whole repo (deep audit) —
   a standing verification organ for estate code, usable any time.

## Status-line patch (2026-09-21)
The plugin's hook statusMessages (the visible "正在检查候选代码…" lines) were
patched to English in place: hooks/hooks.json, backup hooks.json.bak-zh-20260921.
Fragility: plugin updates overwrite the cache — if Chinese status lines return,
re-run the patch (walk hooks.json, replace any statusMessage containing CJK with
"Mimosa security gate: scanning…"). Verdict bodies stay Chinese internally; the
Rosetta + seat-side translation cover those permanently.

## ROOT CAUSE + DOCUMENTED FIX (2026-09-21 night, ponytail/lessig pass)
Root cause of recurring Chinese: the plugin's **UserPromptSubmit hook**
(prompt-hook.mjs) injects a Chinese "pre-generation security constraints" block
into EVERY prompt turn — statusMessage patches never touched it.
Fix: the plugin's OWN documented env switches (README, not a file hack —
survives plugin updates):
- `MIMOSA_NO_PROMPT_GUARD=1` — disables the per-turn constraint injection
  (set user-level via setx; arms at next process start)
- `MIMOSA_HOOK_STATUS=important` — keeps risk visibility, drops chatter
Kept: PreToolUse/PostToolUse write gates (the value), statusMessages patch
(redundant but harmless), Rosetta for verdict bodies on actual blocks.
