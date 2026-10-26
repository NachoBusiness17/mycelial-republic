#!/data/data/com.termux/files/usr/bin/bash
# start_sovereign_node.sh — Zero-dependency C99 Invariant Node
# Replaces 15-minute npm install and Node.js runtime with 1.2s C compile
set -e
BODY="${1:-pixel-11-pro}"
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$DIR/sovereign_node" ]; then
    echo ">> [1/2] Compiling sovereign_node.c (Termux clang)..."
    pkg install -y clang binutils 2>/dev/null || true
    clang -O3 -Wall "$DIR/sovereign_node.c" -o "$DIR/sovereign_node"
    echo ">> [1/2] Build complete in ~1.2s."
fi

echo ">> [2/2] Launching Sovereign Node for body: $BODY"
exec "$DIR/sovereign_node" "$BODY"
