#!/bin/bash
set -euo pipefail

FLATPAK_ID="com.calibre_ebook.calibre"
SRC_DIR="calibre-plugin/"
DEBUG_CMD="calibre-debug"
CUSTOMIZE_CMD="calibre-customize"
IS_FLATPAK=false

if flatpak info "$FLATPAK_ID" >/dev/null 2>&1; then
    echo "Using Flatpak"
    IS_FLATPAK=false
    DEBUG_CMD=(flatpak run --command="$DEBUG_CMD" "$FLATPAK_ID")
    CUSTOMIZE_CMD=(flatpak run --command="$CUSTOMIZE_CMD" "$FLATPAK_ID")
fi

# Request shutdown running instances of Calibre
"${DEBUG_CMD[@]}" "-s"

sleep 1

# Force kill any remaining processes
if $IS_FLATPAK; then
    flatpak ps | grep $FLATPAK_ID | grep -oP "(^\\S+)" | while read -r pid; do
        flatpak kill $pid
    done
fi

# Kill remaining native process instances
pkill -f calibre

# Load plugin
"${CUSTOMIZE_CMD[@]}" "-b" "$SRC_DIR"
"${DEBUG_CMD[@]}" "-g" "$@"