#!/bin/bash

# Meeting sync wrapper for Alfred workflow
SCRIPT_DIR="/Users/weijunsteventey/Documents/Programming Projects/alfred-notion-helper"
cd "$SCRIPT_DIR"

if [ "$1" = "--sync" ]; then
    # Execute sync operation
    mode="${2:-week}"
    python3 meeting_sync.py --sync "$mode" 2>&1
else
    # Script filter mode
    query="$1"
    python3 meeting_sync.py "$query" 2>/dev/null || echo '{"items": [{"title": "Error", "subtitle": "Failed to load meeting sync", "valid": false}]}'
fi