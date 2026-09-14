# hermes docs wing 00

via resident b1 beat ext-92e821b941 folded=True

Plugin manager state keyed by Hermes home path to prevent cross-profile leakage. Uses ContextVar for profile override without mutating os.environ; singleton replaced with cache dict keyed on resolved home. Clear all prefixed sys.modules entries on reload/switch; test fixture drops entire cache and p
