# providers/base.py — any-model abstraction

via cage beat ext-ae932a591b folded=True

**1) What the source does:**
`providers/base.py` defines `ProviderProfile`, a declarative dataclass that captures everything about a single inference provider (auth, endpoints, client quirks, request/vision/reasoning quirks) so the transport layer reads one profile object instead of receiving many b
