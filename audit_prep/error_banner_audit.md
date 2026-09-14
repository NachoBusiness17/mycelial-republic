## Finding — what your cell yields
The error_banner doctrine is a deliberate ship-with-failures-visible mechanism that signals system honesty to abliteration-minded examiners. It transforms JavaScript errors from silent failures into visible, logged events without breaking user experience.

## Evidence — what in the repo supports it (file/shape, no invention)
- **Presence**: 17 single-file HTML games in `dashboard/static/` all contain the error banner fixture (lines 16-17 in maze_arena.html: `window.addEventListener('error',...)` and `window.addEventListener('unhandledrejection',...)`)
- **Pattern**: Standardized implementation - error banner div with red background, monospace font, positioned fixed top, captures both runtime errors and promise rejections
- **Real-world validation**: Grounding wave evidence shows it caught its first live bug within hours of shipping (Adam hit black screen on SWARM title - banner showed TypeError reading x @ line 234)
- **Self-referential honesty**: The banner itself is documented in the grounding wave as "error-banner fixture present" and "error-banner the fold mandated caught its first live bug"

## Risk if wrong — what the audit breaks on if this is missed
Matthew Steiniger's abliteration approach would strip safeguards to see what emerges. Without visible error handling, he would:
1. Discover silent failures that contradict the "honesty over overclaim" invariant
2. Find systems that crash gracefully without logging the actual failure mode
3. Identify gaps between the claimed "ship-with-failures-visible" doctrine and actual implementation
4. Question the system's ability to surface its own problems during stress testing

## The act — the concrete prep step (file/spec/number)
Create an error_banner audit checklist in `audit_prep/error_banner_audit.md`:
1. **Inventory verification**: Confirm all 17 game files contain the banner fixture
2. **Error simulation**: Test each page with deliberate syntax errors to verify banner visibility
3. **Promise rejection test**: Verify unhandled promise rejections are captured
4. **Positioning check**: Confirm banner appears above content (z-index:99)
5. **Documentation audit**: Cross-reference grounding wave claims about banner catches

## Falsifier — what would prove this wrong
A single game file in the dashboard that:
- Lacks the error banner fixture entirely, OR
- Has the fixture but errors are silently swallowed (banner appears but errors aren't logged), OR  
- The banner is present but positioned such that users can't see it (z-index too low, hidden by content), OR
- Shows evidence of error suppression code that bypasses the event listeners