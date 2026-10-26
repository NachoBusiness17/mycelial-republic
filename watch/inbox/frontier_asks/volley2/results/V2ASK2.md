# THE_LENSING: frontier judgment on the route (MC6 paid ask)

Status: ok. Metered cost: $0.0705. Seconds: 46.2. Usage: {"prompt_tokens": 617, "completion_tokens": 3403, "total_tokens": 4020, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 2658, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.070528, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}. Finish: content_filter.
Prompt sha256: fe1f7cc20d35956fe01818ef7d604053478c4e71f9528c74b70038eee38a47db (1570B).
Full return below, verbatim. Em-dash count in return body: 0.

---

# Build Instructions: Witness, Continuity, Artifact (Q07, Q08, Q09)

**Caveat:** I can't see V2CTX.md. Anything below that depends on your chain's internals (the "verkle chain" structure, the table names behind the 618 and 2821 rows, your backup target, your export presets) is flagged **[inference]**. Please check it against the context file before building.

---

## Q07: Witness Architecture

### Verdict on the three options

**1. A gist alone is not sufficient.**
- **[public]** A gist is a git repository the owner controls. The owner can force-push, which rewrites its history, and can delete it.
- A gist witness is therefore still writer-controlled. It moves the tip somewhere public, but it does not make the tip independent of you. It only becomes a witness once someone else mirrors it.
- Keep it as a convenience mirror and a human-readable feed.

**2. A transparency log is the core layer.**
- **[public]** Sigstore's Rekor is a public, append-only log run by a third party. It accepts `hashedrekord` entries (a sha256 plus a signature plus a public key).
- Rekor returns an inclusion proof and a signed entry timestamp. Once your checkpoint hash is in Rekor, you cannot quietly regenerate history behind it.
- **[public]** Add OpenTimestamps (`ots stamp`) as a second, independent anchor. It is Bitcoin-anchored, free, and runs through a separate trust path.

**3. Countersigning is the upgrade path, not day one.**
- **[public]** The C2SP `tlog-checkpoint` / `tlog-witness` specs, used by transparency-dev's omniwitness, let independent witnesses cosign your checkpoint after checking consistency with the last one they saw.
- This is the strongest option. It also requires witnesses willing to follow your log.
- Adopt the C2SP checkpoint format now so that cosigning later needs no format change.

### Spec W1: Checkpoint log (parallel to the chain)

**[inference]** Verkle commitments (KZG or IPA vector commitments) don't come with a standard append-only consistency proof. Don't try to witness the verkle root directly. Instead, ma