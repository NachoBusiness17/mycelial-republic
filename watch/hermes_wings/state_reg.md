# hermes_state_registry.py — state registry

via cage beat ext-d5eefe726f folded=True

(1) This is a process-wide registry that deduplicates SQLite `SessionDB` opens so every caller for the same resolved path shares one writer connection, refcounted per generation. It retires a generation when the underlying file's inode changes (snapshot restore/recovery swap), holds retired instance
