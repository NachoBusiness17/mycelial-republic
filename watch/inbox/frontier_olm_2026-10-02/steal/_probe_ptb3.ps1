$ErrorActionPreference = 'SilentlyContinue'
Select-String -Path 'tools\duel_harness.py' -Pattern 'p=0.0436','style-control regression','run_rejudge','ember-judged only','markdown-header count','fireworks/ember-1' | ForEach-Object { "{0}: {1}" -f $_.LineNumber, $_.Line.Trim() }
