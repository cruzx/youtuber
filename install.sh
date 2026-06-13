#!/usr/bin/env bash
# Author: Cruz Olli
set -euo pipefail
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="$HOME/.agents/skills/youtuber"
mkdir -p "$(dirname "$DEST_DIR")"
rm -rf "$DEST_DIR"
cp -R "$SRC_DIR" "$DEST_DIR"
echo "Installed youtuber skill to: $DEST_DIR"
echo "Invoke in Codex with: \$youtuber"
