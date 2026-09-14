## Finding — what your cell yields  
**The error_banner doctrine is inconsistently applied**: Only 9/109 HTML files contain the complete fixture, revealing a gap between stated doctrine ("ship-with-failures-visible") and actual implementation across the dashboard surface.

## Evidence — what in the repo supports it (file/shape, no invention)
- **Audit automation**: `audit_prep/verify_error_banner.py` found 97 files missing the banner entirely, 3 with incomplete fixtures (missing rejection listeners)
- **Complete fixture files**: Only `arrakis.html`, `bad_apple_field.html`, `conservation_room.html`, `eraser_maze.html`, `home.html`, `incident_dungeon.html`, `maze_arena.html`, `spectral_maze.html`, `worldline_dungeon.html` have all three components (banner div + error listener + rejection listener)
- **Pattern inconsistency**: Game files (maze_arena.html, bad_apple_field.html) consistently implement the fixture, while core dashboard pages (index.html, live.html, memory_map.html) lack it entirely
- **Self-test failure**: The grounding wave shows the banner caught its first bug within hours, but the coverage remains limited to specific game types

## Risk if wrong — what the audit breaks on if this is missed  
Matthew Steiniger's abliteration approach would:
1. **Discover the doctrine-inconsistency gap**: The "ship-with-failures-visible" claim is falsified by 89% of the dashboard surface lacking error handling
2. **Identify surface-dependent reliability**: Core pages like index.html, live.html, and memory_map.html would crash silently under stress, contradicting the "honesty over overclaim" invariant  
3. **Question selective transparency**: Why do games have error banners but critical dashboard tools don't? This suggests the doctrine is situational rather than universal
4. **Find unhandled promise rejections**: 3 files have error listeners but miss rejection handlers, creating silent failure modes for async operations

## The act — the concrete prep step (file/spec/number)
**Immediate triage**: Prioritize adding the complete error banner fixture to these high-impact core dashboard files:
1. `index.html` (main dashboard entry point)
2. `live.html` (real-time monitoring)  
3. `memory_map.html` (system memory visualization)
4. `module_map.html` (code architecture browser)
5. `operator_board.html` (operator interface)

**Long-term expansion**: Systematically roll the fixture to all remaining dashboard pages, starting with navigation and tool pages.

## Falsifier — what would prove this wrong
A documented decision that:
1. **Core dashboard pages intentionally omit error banners** for UX reasons (with operator approval), OR
2. **Alternative error handling mechanisms** exist for non-game pages that provide equivalent or better failure visibility, OR  
3. **The error banner doctrine applies only to interactive games/tools** and not to static/dashboard pages (contradicting the "ship-with-failures-visible" principle as universally stated)