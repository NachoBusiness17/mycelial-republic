# PUBLIC RELEASE REVIEW

Public manifest sha256: `7cd6b23fa4cbed3f2d7f602587db159cd39727bd92539da4c4c9b12c7da7eeb9`

Built 2026-10-17T19:33:06+00:00 from private vault manifest
`brain_manifest_20261017T191313Z_12a1cd4032fb.json` (sha256 `12a1cd4032fb76b4bb51c4e61589844df03682e29463cab249928a8d5839e0a3`).
v2 chain root `7a89fb705067cf62e613075e5c3543bae55659c35ef74d0696ac495a841d0b10` at n=12182.

Every file below would be published, and nothing else, to `magpublic:lattice/7cd6b23fa4cbed3f2d7f602587db159cd39727bd92539da4c4c9b12c7da7eeb9/`.
Read them in the staging payload folder next to this file. Nothing is published until
you run:

    python scripts/public_lattice_manifest.py push --approve 7cd6b23fa4cbed3f2d7f602587db159cd39727bd92539da4c4c9b12c7da7eeb9

If any byte changes, the sha changes and the old approval stops matching.

| public path | bytes | sha256 (16) | source in brain | masked | derived |
|---|---|---|---|---|---|
| `chain_v2/checkpoints_v2.jsonl` | 2657 | `ffb3e5b92dba6bf8` | `memory/biography_v2/checkpoints_v2.jsonl` | no | no |
| `chain_v2/tip_v2.json` | 382 | `4b89d90e30701220` | `memory/biography_v2/tip_v2.json` | no | no |
| `law_cards.json` | 29303 | `d86f6847707b56ad` | `memory/rib_boot.json` | yes | yes |
| `verify/verify_knot_v2.py` | 23557 | `26f13152030f8cbf` | `scripts/verify_knot_v2.py` | no | no |
| `PUBLIC_MANIFEST.json` | (this manifest) | `7cd6b23fa4cbed3f` | n/a | no | yes |

Excluded after masking (redaction scan still tripped; path only):
- (none)

Attention lines (NOT blocked by rule; identity / account / ops detail you may not
want on a public drive; if any should go, say so and the allowlist/transform is
tightened, which changes the sha):
- `law_cards.json`: ommits - the mirrors are out of jurisdiction. - **A phantom portproxy holds <ip>:8765 -> <ip>:8765 (svchost, needs ELEVATED netsh
- `law_cards.json`: ntom portproxy holds <ip>:8765 -> <ip>:8765 (svchost, needs ELEVATED netsh to delete):** this is why the lab seemed dead. The la
- `law_cards.json`: console window on the operator's desktop). To restore 8765: elevated `netsh interface portproxy delete v4tov4 listenport=876"
- `law_cards.json`: ator's desktop). To restore 8765: elevated `netsh interface portproxy delete v4tov4 listenport=876"
- `law_cards.json`: dry - the succession is by design, not failure. Both Google accounts (sf = <email>, nacho = nachobusinesscorp) are logged into A
- `law_cards.json`: ravity on bob via PowerShell. Gemini 3-class reasoning, two accounts, no marginal cost. The work does not grind to a halt. ## TH
- `law_cards.json`: e (arm 2: no completion_tokens_details at all, 2 completion tokens); thinking:{type:enabled} returned reasoning too (46 chars,
- `law_cards.json`: hinking:{type:enabled} returned reasoning too (46 chars, 12 tokens). THE LAW IS NOW: omission is a MEASURED ON state. Arm 3 is
- `law_cards.json`: e (arm 2: no completion_tokens_details at all, 2 completion tokens); thinking:{type:enabled} returned reasoning too (46 chars,
- `law_cards.json`: hinking:{type:enabled} returned reasoning too (46 chars, 12 tokens). THE LAW IS NOW: omission is a MEASURED ON state. Arm 3 is
- `law_cards.json`: (mag/context_pack.py) renders the index below into the min-token seat. The full card bodies stay in this file; the boot serv
- `law_cards.json`: (mag/context_pack.py) renders the index below into the min-token seat. The full card bodies stay in this file; the boot serv

One-way law: the public drive is write-only from our side. Push = `rclone copy
--ignore-existing`; check = `rclone check --one-way` (hash compare, output discarded).
Nothing is ever read back from public into the brain.
