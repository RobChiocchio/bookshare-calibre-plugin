#!/bin/bash
set -euo pipefail

CMD="calibre-debug"
FLATPAK_ID="com.calibre_ebook.calibre"
SCRIPT="./build_ui.py"
SRC_DIR="calibre-plugin/"
FLAGS="-e"

# Check if native Calibre binary exists
if command -v "$CMD" >/dev/null 2>&1; then
    echo "Building with Calibre Native"
    "$CMD" -e "$SCRIPT" -- "$SRC_DIR" "$@" # TODO: test this
elif flatpak info "$FLATPAK_ID" >/dev/null 2>&1; then
    echo "Building with Calibre Flatpak"

    # Export source directory to the sandbox
    FLATPAK_SRC_DIR=$(flatpak document-export -trw "$SRC_DIR" -a "$FLATPAK_ID")

    # Cleanup exports on exit
    trap 'flatpak document-unexport "$FLATPAK_SRC_DIR" >/dev/null 2>&1' EXIT

    flatpak run --command="$CMD" "$FLATPAK_ID" "$FLAGS" "$SCRIPT" -- "$FLATPAK_SRC_DIR" "$@"
else
    echo "No Calibre version detected"
fi