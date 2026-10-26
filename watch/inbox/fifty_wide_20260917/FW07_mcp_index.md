# FW-07 — docs/mirrors/mcp/INDEX.md: the 31 "dead spec paths" were census truncation noise (2026-09-28)

- Ask: rebuild or tombstone the 31 dead spec paths in `docs/mirrors/mcp/INDEX.md`.
- Verdict: **neither — the paths were never dead.** The 31 refs live inside
  `[source](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/specification/2026-07-28/....mdx)`
  links. Two stacked instrument defects manufactured the finding:
  1. `_REF_RE` (`mag/prose_census.py:42`) had no `mdx` in its extension class → every
     `index.mdx` truncated to `index.md` before the exists() check. Reproduced mechanically:
     old pattern on INDEX.md → `refs: 31, unique dead: 31, all end .md`.
  2. Regex alternation is leftmost-first, so `md|mdx` still matches `md` and leaves the
     trailing `x` — verified after the first fix attempt, corrected to `mdx|md`.
  3. Even untruncated, the captured `docs/specification/...` is a REMOTE URL path; the local
     mirror lives at `docs/mirrors/mcp/spec/2026-07-28/`. A path fragment inside an `https://`
     URL is not a claim about this repo — URL fragments are now stripped before scanning
     (`run_census`, `re.sub(r"https?://\S+", "", text)`).
- Mirror bytes verified: `find docs/mirrors/mcp/spec -name "*.mdx" | wc -l` → **31/31 present**
  (architecture/index.mdx, basic/patterns/cancellation.mdx, … all on disk).
- Post-fix check on INDEX.md: `refs: 0, dead: 0` — the file drops off the ghost list entirely.
- Code change: `mag/prose_census.py` `_REF_RE` gains `mdx`, reorders `jsonl` ahead of `json`
  (same leftmost-first defect, found via FW-10's evidence), plus the URL strip in `run_census`;
  fix comment carries this receipt path. No tests exist for prose_census (grep of tests/ → no
  hits) — nothing to re-run there; the mechanical before/after reproductions above are the check.
- INDEX.md itself: untouched. Nothing to rebuild, nothing to tombstone.
