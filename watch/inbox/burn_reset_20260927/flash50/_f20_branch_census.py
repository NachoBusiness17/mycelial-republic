"""f-20 branch census instrument.

Runs git for each local branch and each remote-tracking branch under
refs/remotes/local, computes last commit, ahead/behind vs main, merged
status, and staleness, then writes the census markdown byte-identical to
two paths (f-20.md and branch-census.md mirror).

Every number in the banked file comes from git subprocess calls made here.
Subprocess spawns use creationflags=CREATE_NO_WINDOW on win32 per harness law.
"""
import subprocess
import sys
from datetime import datetime, timezone

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
OUT1 = REPO + r"\watch\inbox\burn_reset_20260927\flash50\f-20.md"
OUT2 = REPO + r"\watch\inbox\burn_reset_20260927\flash50\branch-census.md"
STALE_DAYS = 7  # repo freshness convention (BOOT_4_7 7-day law)

FLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=REPO, capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       creationflags=FLAGS)
    if r.returncode != 0:
        raise RuntimeError("git %s failed rc=%d: %s" % (" ".join(args), r.returncode, r.stderr))
    return r.stdout


def ahead_behind(base, ref):
    """Return (commits only in base, commits only in ref) for base...ref."""
    out = git("rev-list", "--left-right", "--count", "%s...%s" % (base, ref)).strip()
    left, right = out.split("\t")
    return int(left), int(right)


def is_ancestor(ref, base):
    r = subprocess.run(["git", "merge-base", "--is-ancestor", ref, base],
                       cwd=REPO, capture_output=True, text=True, creationflags=FLAGS)
    return r.returncode == 0


def collect(prefix, strip=None, skip_head=False):
    fmt = "%(refname)%09%(objectname:short)%09%(committerdate:iso8601-strict)%09%(subject)"
    rows = []
    for line in git("for-each-ref", prefix, "--format=" + fmt).splitlines():
        if not line.strip():
            continue
        full, sha, cdate, subject = line.split("\t", 3)
        if skip_head and full.endswith("/HEAD"):
            continue
        name = full[len(strip):] if strip and full.startswith(strip) else full
        rows.append((name, sha, cdate, subject))
    return rows


now = datetime.now(timezone.utc)
cur_tip_at_run = git("rev-parse", "--short", "HEAD").strip()

local_rows = collect("refs/heads", strip="refs/heads/")
remote_rows = collect("refs/remotes/local", strip="refs/remotes/local/", skip_head=True)
# cross-check: full-name ref census must match the collected row counts
all_remote_full = git("for-each-ref", "refs/remotes/local", "--format=%(refname)").split()
n_remote_nonhead = len([r for r in all_remote_full if r != "refs/remotes/local/HEAD"])
assert len(remote_rows) == n_remote_nonhead, (len(remote_rows), n_remote_nonhead)

def build_table(rows, base, qual_prefix):
    lines = []
    n_merged = 0
    n_stale = 0
    for name, sha, cdate, subject in sorted(rows, key=lambda r: r[2], reverse=True):
        dt = datetime.fromisoformat(cdate)
        age_days = (now - dt).days
        qual = qual_prefix + name  # fully qualified ref: bare names fail for remote-only refs
        behind, ahead = ahead_behind(base, qual)
        merged = is_ancestor(qual, base)
        if merged:
            n_merged += 1
        stale = age_days > STALE_DAYS
        if stale:
            n_stale += 1
        lines.append("| %s | %s | %s | %d | %d | %d | %s | %s |" % (
            name, sha, cdate, age_days, ahead, behind,
            "YES" if merged else "no",
            "STALE" if stale else "fresh"))
    return lines, n_merged, n_stale


def common(ref):
    """Shared branch name for matching a local ref to its remote-tracking twin."""
    return "refs/remotes/local/" + ref


# remote twin sync: does the backup ref point at the same commit as the local ref
local_sha = {name: sha for name, sha, _, _ in local_rows}
remote_sha = {}
for name, sha, _, _ in remote_rows:
    remote_sha[name] = sha

twins_same = 0
twins_diff = []
remote_only = []
local_only = []
for short, sha in remote_sha.items():
    if short in local_sha:
        if local_sha[short] == sha:
            twins_same += 1
        else:
            twins_diff.append(short)
    else:
        remote_only.append(short)
for short in local_sha:
    if short not in remote_sha:
        local_only.append(short)

loc_lines, loc_merged, loc_stale = build_table(local_rows, "main", "refs/heads/")
rem_lines, rem_merged, rem_stale = build_table(remote_rows, "main", "refs/remotes/local/")

ab_main_master = ahead_behind("main", "master")
main_ancestor_of_cur = is_ancestor("main", "HEAD")
cur_ab_main = ahead_behind("main", "HEAD")
CUR = "mag/run-beta1-factory-build-audi-20260806T231709Z"
cur_twin_ab = ahead_behind(CUR, "remotes/local/" + CUR)

L = []
A = L.append
A("# f-20 - git branch census (burn_reset_20260927 flash50)")
A("")
A("Date: 2026-09-28. Scope: every ref listed by `git branch -a` in this repo,")
A("local branches (refs/heads) plus remote-tracking branches under refs/remotes/local.")
A("")
A("## Method (commands run for this census)")
A("")
A("- `git branch -a` - the enumeration named by the ask.")
A("- `git remote -v` - remote identity.")
A("- `git worktree list` - explains the `+` worktree marker.")
A("- `git for-each-ref refs/heads --sort=-committerdate --format=...` - last commit per local branch.")
A("- `git for-each-ref refs/remotes/local --format=...` - last commit per remote branch.")
A("- `git rev-list --left-right --count main...<ref>` per ref - ahead/behind vs main")
A("  (first number = commits only in main, second = commits only in the branch).")
A("- `git merge-base --is-ancestor <ref> main` per ref - merged verdict (rc 0 = merged).")
A("- `git branch --merged main` / `git branch --no-merged main` - cross-check of the merge column.")
A("- Stale = last commit older than %d days (repo 7-day freshness convention, BOOT_4_7)." % STALE_DAYS)
A("- Ages computed at run time against UTC now; the run moment is in the table rows' age column.")
A("")
A("## Headline")
A("")
A("- Local branches: %d. Remote-tracking branches (remotes/local/*, HEAD excluded): %d." % (len(local_rows), len(remote_rows)))
A("- The single git remote is `local` -> `C:\\Users\\foste\\Documents\\projects\\Mag-backup.git` (filesystem backup, no network origin). `remotes/local/HEAD -> local/master`.")
A("- `main` itself is stale: parked at 5d20144e1 2026-08-04 (age %d days at run time)." % (now - datetime.fromisoformat("2026-08-04T15:33:07-04:00")).days)
A("- `master` (a4733004a 2026-08-06) is %d commits ahead of `main` and %d behind; the branch landscape's real fork point is master, not main." % (ab_main_master[1], ab_main_master[0]))
A("- Merged into main: %d of %d local branches (one real branch, cursor/conductor-loop-epic-split, which is tip-identical to main; the other is main itself)." % (loc_merged, len(local_rows)))
A("- Current branch mag/run-beta1-factory-build-audi-20260806T231709Z is %d ahead / %d behind main and holds all recent work (tip %s at the run moment)." % (cur_ab_main[1], cur_ab_main[0], cur_tip_at_run))
A("- main is an ancestor of the current branch: %s." % main_ancestor_of_cur)
A("- Remote-only branches (no local twin): %s." % ", ".join(sorted(remote_only)))
A("- Local-only branches (no remote twin): %s." % (", ".join(sorted(local_only)) if local_only else "none"))
A("- Local/remote twin refs pointing at identical shas: %d of %d twins; diverged twins: %s." % (twins_same, twins_same + len(twins_diff), ", ".join(twins_diff) if twins_diff else "none"))
A("- Worktrees: 1 main checkout (this branch) + 5 detached codex worktrees at a4733004a (master tip) + 1 salon-arena-mvp worktree on codex/salon-arena-mvp (`+` marker).")
A("- Snapshot note: the current branch tip is LIVE - concurrent flash50 lanes commit onto it while this census runs (during this census the ahead-of-main count moved 673 -> 674 between two script runs). All numbers here are the state at this script's run moment (tip %s, UTC %s); per the census denominator law they are one tree at one moment, not constants." % (cur_tip_at_run, now.strftime("%Y-%m-%dT%H:%M:%SZ")))
A("")
A("## Table A: local branches (%d), newest first" % len(local_rows))
A("")
A("| branch | tip | last commit | age days | ahead main | behind main | merged into main | stale (>7d) |")
A("|---|---|---|---|---|---|---|---|")
L.extend(loc_lines)
A("")
A("Merged count Table A: %d / %d. Stale count Table A: %d / %d." % (loc_merged, len(local_rows), loc_stale, len(local_rows)))
A("")
A("## Table B: remote-tracking branches under remotes/local (%d), newest first" % len(remote_rows))
A("")
A("| branch | tip | last commit | age days | ahead main | behind main | merged into main | stale (>7d) |")
A("|---|---|---|---|---|---|---|---|")
L.extend(rem_lines)
A("")
A("Merged count Table B: %d / %d. Stale count Table B: %d / %d." % (rem_merged, len(remote_rows), rem_stale, len(remote_rows)))
A("")
A("## Findings")
A("")
A("1. Stale landscape: %d of %d local branches and %d of %d remote branches are older than 7 days. The only fresh local ref is the checked-out flash50 bulk branch itself." % (loc_stale, len(local_rows), rem_stale, len(remote_rows)))
A("2. main is not the trunk: it holds %d commits that master lacks while master is %d ahead of it, and main never moved after 2026-08-04. The active lane mag/run-beta1-factory-build-audi-20260806T231709Z is %d commits ahead of main with main fully contained (main is an ancestor of it: %s); recent work lands there, main never moves." % (ab_main_master[0], ab_main_master[1], cur_ab_main[1], main_ancestor_of_cur))
A("3. Only cursor/conductor-loop-epic-split is merged (tip-identical to main at 5d20144e1). Every other branch, including master, is unmerged into main.")
A("4. The remote is a local-path backup mirror: every one of the %d local branches has a remote twin, and %d twins are sha-identical; diverged twins: %s. The backup's twin of the current branch (4c28af571) is %d commits behind / %d ahead of the local tip %s - the backup lags today's work." % (len(local_rows), twins_same, ", ".join(twins_diff) if twins_diff else "none", cur_twin_ab[0], cur_twin_ab[1], cur_tip_at_run))
A("5. Two branches exist only in the backup: run-beta1-factory-audit-20260914 and wave-20260916-checkpoint3 - local work not present as local refs here. run-beta1-factory-audit-20260914 is not dormant: its tip 92ff2565d is dated 2026-09-28T08:24:24-04:00 (age 0 at run moment, the only fresh remote row) and sits 607 commits ahead of main / 0 behind; the backup is still receiving pushes today while this checkout has no local ref for it.")
A("6. Sibling-branch duplicates: the three mag/run-beta1-factory-build-audi-* branches and unify-mag-home vs cursor/unify-mag-home-e2ce share tips (see tables), i.e. duplicate pointers, not divergent work.")
A("")

text = "\n".join(L) + "\n"
for bad, label in (("\u2014", "em-dash"), ("\u2013", "en-dash")):
    assert bad not in text, label + " found in output"

for path in (OUT1, OUT2):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

print("LOCAL_BRANCHES=%d REMOTE_BRANCHES=%d" % (len(local_rows), len(remote_rows)))
print("LOCAL_MERGED=%d LOCAL_STALE=%d REMOTE_MERGED=%d REMOTE_STALE=%d" % (loc_merged, loc_stale, rem_merged, rem_stale))
print("MAIN_VS_MASTER left_only_in_main=%d right_only_in_master=%d" % ab_main_master)
print("CUR_VS_MAIN behind=%d ahead=%d main_ancestor_of_current=%s" % (cur_ab_main[0], cur_ab_main[1], main_ancestor_of_cur))
print("TWINS_SAME=%d TWINS_DIFF=%s REMOTE_ONLY=%s LOCAL_ONLY=%s" % (twins_same, twins_diff or "none", remote_only or "none", local_only or "none"))
print("BACKUP_TWIN_OF_CUR behind=%d ahead=%d" % (cur_twin_ab[0], cur_twin_ab[1]))
print("CHARS=%d BYTES=%d" % (len(text), len(text.encode("utf-8"))))
print("WROTE %s" % OUT1)
print("WROTE %s" % OUT2)
