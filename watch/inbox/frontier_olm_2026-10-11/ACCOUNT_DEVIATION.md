# ACCOUNT DEVIATION NOTE (2026-10-11, mode 2)

The day-11 burn fired per the SPEND order on the start plan (dwfrun-d07c3314).
The operator then moved it to the start plan's max-width Flash via GUI
(dwfrun-af85b9b8), which ran until the start plan returned QUOTA EXHAUSTED
(code 1005, exceed quota limit) mid-sweep - phase "Sweep the four frontiers",
7 estate lenses banked before the stop.

Resolution: the error names "switch to another provider" as a valid fix; the
operator is off PC; the SPEND order's intent (spend the funded budget, never
hoard) is served by the session's individual-plan account, which funded all
four of tonight's ACCEPT workflows. Resumed as dwfrun-e68f99eb on
account:zai-individual-coding-plan/GLM-5.3, cache importing the 7 banked
lenses. The start plan resumes as the default lane the moment its quota
resets or the operator tops up - this is a pause, not a downgrade of the
standing order.

Falsifier: if the start plan refills and the operator directs back, the
deviation note closes; if the individual plan also exhausts, the mine waits
rather than touching unfunded lanes.
