# LW2 — Adam invite to the-mountain (2026-09-30)

## Result: NOT INVITED — no GitHub username for Adam exists in the estate. Command filed below.

## Last-mile state (all verified live 2026-09-30)

1. **Push state:** `git log origin/main..HEAD` in `the-mountain` = EMPTY. main in sync at `bac2b89` `[origin/main]`. Nothing unpushed.
2. **Push:** `git push origin main` → mountain-gate hook fired ("scanning outgoing changeset for provider-shaped secrets... clean."), output `Everything up-to-date`, exit 0.
3. **gh auth:** Logged in as `NachoBusiness17` (keyring, https protocol, PAT). Active.
4. **Collaborators** (`gh api repos/NachoBusiness17/the-mountain/collaborators`): exactly one — `NachoBusiness17` (admin). **No Adam.**

## The username hunt (everywhere the estate names Adam)

| Handle | Surface | Evidence | GitHub? |
|---|---|---|---|
| **Adam Crigler** | real name | `watch/inbox/ADAM_ONBOARDING_FULL_20260924.md` step 12 (`git config user.name "Adam Crigler"`); `LETTER_ADAM_CRIGLER.md` | `gh api users/AdamCrigler` → **404** |
| **ItsCommodore** | **Discord** | `watch/onboard/README.md` ("Adam = ItsCommodore"); `packs/p8_adam_onboard_20260912.json` ("handle ItsCommodore... he asked... on Discord"); `watch/onboard/WELCOME.md` ("Adam, in Discord") | `gh api users/ItsCommodore` → **404** |
| **@AdamCrigler** | X | `memory/runs/x_bookmark_harvest_20260905/canon_folder_harvest.md` (reply chain with @NachoQuixotic = Mark; "Thanks Bro") | not probed as GitHub; X-only evidence |
| @adamdotnew | CAD vendor | `watch/INTAKE_FABLE51_CAD_20260903.md` guard: **NOT Adam Crigler — do not conflate** | NO |

Conclusion: Adam's GitHub username was never captured. Both plausible guesses 404 on GitHub. A push-permission invite to a guessed handle would grant a possible stranger write access — the exact identity-skipped-for-resemblance failure the stranger-register exists to stop. Not sent.

## The exact command the operator runs when he has the name

Ask Adam on Discord (`ItsCommodore`): "what's your GitHub username?" Then:

```bash
gh api -X PUT repos/NachoBusiness17/the-mountain/collaborators/USERNAME -f permission=push
```

(Replace USERNAME with Adam's literal GitHub login. Verify it first: `gh api users/USERNAME` — must return 200 and look like him, not a name-squatter.)

After the invite: `gh api repos/NachoBusiness17/the-mountain/invitations` shows it pending until Adam accepts.

## Doctrine note

Guest protocol (`watch/onboard/GLOSSARY.md`, 2026-09-12) held Adam as witness-only ("cannot sign, spend, or trigger gates"). This mission's push-permission invite supersedes that for `the-mountain` — operator's explicit 2026-09-30 instruction, recorded here so the shift is visible.
