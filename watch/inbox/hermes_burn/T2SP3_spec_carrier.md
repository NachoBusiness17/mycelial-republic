# T2SP3_spec_carrier (anthropic/claude-opus-5.5, turn 1, channel: reasoning (content channel empty))

I need the spec under 600 words with no em-dashes, citing file:line for evidence. Since the excerpt lacks actual line numbers, I'll cite by function/file anchors like tools/hermes_burn and explicitly mark line numbers as UNVERIFIED rather than guess, since counting lines would be unreliable.

The driver script scripts/descent_driver.sh isn't in evidence, so all its claims stay UNVERIFIED too. For the epoch tension, I'm working through the resolution: ask.json carries an epoch field (default 0), usage rows bank their epoch, and the refusal state only counts rows matching the current epoch (missing epoch treated as 0). Re-arming requires the operator to both bump the epoch and delete the marker, since bumping epoch alone without removing the marker still skips, and editing ask bytes without bumping epoch still re-mints, which I'll note as a negative example showing no new infrastructure is needed, just this one field.

Now I'm turning to predicting the next bleed class, starting with the turn-2 revision re-fire loop as a candidate.

The clear fourth bleed is the revision re-fire: since nothing marks a landed revision as consumed, the driver re-fires turn 2 every 45-second cycle forever as long as revision.md exists and the revision flag is true. The fix is to fence by recording a hash of revision.md in the output and skip re-firing if that hash is already present — deterministic, no new infrastructure needed. I'm also considering a second candidate bleed: empty-response retries aren't terminal, so empty content or transport failures could also loop the driver indefinitely, each cycle burning tokens, but I'm leaning toward the revision re-fire as the more likely pick.


