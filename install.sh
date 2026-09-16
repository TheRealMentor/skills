#!/usr/bin/env bash
#
# Installs this repo as the "personal" plugin into ~/.claude/skills, so its
# skills and agent load namespaced (/personal:create-td, /personal:dev, ...).
#
#   ./install.sh          symlink (default) — `git pull` here updates your install
#   ./install.sh --copy   copy instead, if you'd rather edit your copy freely
#
# Idempotent: re-running refreshes what it installed before. Anything at the
# target path that this script didn't put there is left alone and reported.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}"
MANIFEST="$DEST/.shipping-skills-installed"
TARGET="$DEST/skills/personal"
MODE="symlink"

for arg in "$@"; do
  case "$arg" in
    --copy) MODE="copy" ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

echo "Installing into $DEST ($MODE)"

mkdir -p "$DEST/skills"
touch "$MANIFEST"

# Earlier versions of this script symlinked each skill (and the agent)
# straight into ~/.claude/skills and ~/.claude/agents. Those are superseded
# by the single plugin symlink below — remove whichever of them are still
# around, but only the ones this script put there.
while IFS= read -r old; do
  [ -n "$old" ] || continue
  [ "$old" = "$TARGET" ] && continue
  if [ -e "$old" ] || [ -L "$old" ]; then
    rm -rf "$old"
    echo "  removed legacy install: $old"
  fi
done < "$MANIFEST"

if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
  if [ "$MODE" = "symlink" ] && [ -L "$TARGET" ] && [ "$(readlink "$TARGET")" = "$SRC" ]; then
    echo "  ok    personal (already linked)"
    echo "$TARGET" > "$MANIFEST"
    echo
    echo "Start a new Claude Code session, then try /personal:create-td."
    exit 0
  elif grep -qxF "$TARGET" "$MANIFEST" 2>/dev/null; then
    rm -rf "$TARGET"                          # ours from a previous run — refresh it
  else
    echo "  skip  personal — $TARGET already exists and wasn't installed by this script"
    echo
    echo "Remove it yourself if you want this plugin installed instead."
    exit 1
  fi
fi

if [ "$MODE" = "symlink" ]; then
  ln -s "$SRC" "$TARGET"
else
  mkdir -p "$TARGET"
  cp -R "$SRC/.claude-plugin" "$SRC/skills" "$SRC/agents" "$TARGET/"
fi
echo "  ok    personal"

echo "$TARGET" > "$MANIFEST"

echo
echo "Start a new Claude Code session, then try /personal:create-td."
