# OPENCODE BUILDER LOG - ATTEMPT 1 ERRATA (preserved from context; the relaunch's log-reset wiped the original before the cp landed)

Attempt 1 (05:57Z-06:45Z): all 5 cycles died instantly on the default provider.

```
> build · glm-5v-turbo
Error: Your current subscription plan does not yet include access to GLM-5V-Turbo
```

Cycles 1-5 at 05:57 / 06:08 / 06:20 / 06:32 / 06:43Z, identical error each; loop completed 06:45Z having built nothing.

Cause: opencode's default `build` provider resolves to glm-5v-turbo, which the Z.AI coding plan does not include; the config's plan-covered models are glm-4.7 and glm-5.3.

Cure (landed same night): explicit `-m zai/glm-5.3` on every opencode invocation, proven awake with the OC-5.3-AWAKE echo before relaunch. Attempt 2 runs 06:49Z onward (first banner already shows `build - glm-5.3`).
