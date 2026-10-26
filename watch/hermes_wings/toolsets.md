# toolsets.py — the toolset registry

via cage beat ext-53b2121819 folded=True

**Report: toolsets.txt (Hermes toolset registry)**

**(1) What it does:** This file is Hermes's central toolset registry â a declarative Python dict mapping named toolsets (`web`, `terminal`, `browser`, plus per-platform `hermes-*` sets) to lists of tool names, composable via optional `includes`. 
