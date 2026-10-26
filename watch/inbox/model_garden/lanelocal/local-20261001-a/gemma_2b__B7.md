# garden-v1-B7 | gemma:2b | series local-20261001-a | instrument=lane-local-script
# finish=stop prompt_tokens=4098 completion_tokens=614 wall_s=28.25 tok_s=21.7 checks=0/4 {'A1-ITEM': 0, 'A1-PATH': 0, 'A2-CONCEPT': 0, 'A3-COUNT': 0}

## B2-545: .gitattributes, origin field for sha-cited jsonl artifacts

**Positive:**

* Adding an `origin` field to both the `_log` calls in `process_supervisor.py` and `process_reaper.py` ensures both sides can attribute row origin correctly, even if a row is written by a different process.

**Negative:**

* Without the `origin` field, the `_log` call in `process_supervisor.log` may write an incorrect origin, potentially causing inconsistent data across the supervisor and worker side.


## B2-546: Slots-log lines

**Positive:**

* Printing the process ID and UTC timestamp for each line ensures a clear and informative record of each spawned process's activity and helps diagnose issues like duplicate lines.


**Negative:**

* The conditional logic based on counting down from the status may be misleading: it may land before the status is completed and before the process finishes writing to the file, leading to inaccurate logging.


## B2-549: Mixed-case keys

**Positive:**

* Adding a case-insensitive duplicate detection ensures the plugin applies the fix consistently, regardless of the case of the key names in the `confgs/keys.json`.


**Negative:**

* Without the case-insensitive detection, each key in the `confgs/keys.json` will match the exact case during loading, potentially leading to unexpected behavior when multiple keys hold the same value.


## B2_551: Key-law audit

**Positive:**

* Adding a custom case-insensitive duplicate key detection based on both the name and the timestamp ensures that the plugin treats both exact matches on the order they appear in the manifest files during the audit.


**Negative:**

* The exact case comparison in the plugin is likely redundant. By default, the plugin uses the exact case for key, making the custom case check unnecessary.


## B2_552: Env load case collision

**Positive:**

* Explicitly checking for the same keys prevents the load from mixing the two environment entries under WSL while ensuring only the latest valid value takes precedence.


**Negative:**

* Without this check, the environment might contain both MISTRAL_API_KEY and Mistral_API_KEY, leading to conflicting data for the same process.


## B2_553: Duplicate entries

**Positive:**

* The `dotenv` loading is subject to the potential behavior. This issue, where loading a .env with both the same keys causes the plugin to be activated. The new version of the plugin will prevent the loading and report the issue.


## B2_550: Prompt Lineage

**Positive:**

* This positive verifies each manifest environment key has a name match in the .env precisely, ensuring that the plugin treats it as the same key, which the prompt lineage data is read upon the file.
