#!/usr/bin/env bash
#
# Installs the shipping-code skills into ~/.claude.
#
#   ./install.sh          symlink (default) — `git pull` here updates your install
#   ./install.sh --copy   copy instead, if you'd rather edit your copies freely
#
# Idempotent: re-running refreshes everything it installed before. Anything at a
# target path that this script didn't put there is left alone and reported.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}"
MANIFEST="$DEST/.shipping-skills-installed"
MODE="symlink"

for arg in "$@"; do
  case "$arg" in
    --copy) MODE="copy" ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

installed=0
skipped=0

# Paths this script installed on a previous run. Anything else at a target path
# belongs to the user, and we don't touch it.
ours() {
  [ -f "$MANIFEST" ] && grep -qxF "$1" "$MANIFEST"
}

# install_item <source path> <target path>
install_item() {
  local src="$1" target="$2" name
  name="$(basename "$target")"

  if [ -e "$target" ] || [ -L "$target" ]; then
    if [ "$MODE" = "symlink" ] && [ -L "$target" ] && [ "$(readlink "$target")" = "$src" ]; then
      echo "  ok    $name (already linked)"
      installed=$((installed + 1))
      return
    elif ours "$target"; then
      rm -rf "$target"                      # ours from a previous run — refresh it
    else
      echo "  skip  $name — already exists and wasn't installed by this script"
      skipped=$((skipped + 1))
      return
    fi
  fi

  if [ "$MODE" = "symlink" ]; then
    ln -s "$src" "$target"
  else
    cp -R "$src" "$target"
  fi
  echo "$target" >> "$MANIFEST"
  echo "  ok    $name"
  installed=$((installed + 1))
}

echo "Installing into $DEST ($MODE)"

mkdir -p "$DEST/skills" "$DEST/agents"
touch "$MANIFEST"

echo "skills:"
for skill in "$SRC"/skills/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  install_item "${skill%/}" "$DEST/skills/$(basename "${skill%/}")"
done

echo "agents:"
for agent in "$SRC"/agents/*.md; do
  [ -f "$agent" ] || continue
  install_item "$agent" "$DEST/agents/$(basename "$agent")"
done

# Keep the manifest free of duplicates from repeated runs.
if [ -s "$MANIFEST" ]; then
  sort -u "$MANIFEST" -o "$MANIFEST"
fi

echo
echo "$installed installed, $skipped skipped."
if [ "$skipped" -gt 0 ]; then
  echo "Skipped items already existed — remove them yourself if you want ours instead."
fi
echo "Start a new Claude Code session, then try /create-td."
