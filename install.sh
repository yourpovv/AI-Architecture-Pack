#!/usr/bin/env bash
# Install the pack's coding-* skills for Claude Code.
#   ./install.sh            install for every project (~/.claude/skills)
#   ./install.sh --project  install into the current directory's .claude/skills
set -euo pipefail

source_dir="$(cd "$(dirname "$0")" && pwd)/dist/skills"

case "${1:-}" in
  --project) target_dir="$PWD/.claude/skills" ;;
  "")        target_dir="$HOME/.claude/skills" ;;
  *)         echo "usage: $0 [--project]" >&2; exit 2 ;;
esac

if [ ! -d "$source_dir" ]; then
  echo "install: $source_dir not found; run 'python scripts/build_skills.py' first" >&2
  exit 1
fi

mkdir -p "$target_dir"
for skill in "$source_dir"/coding-*; do
  name="$(basename "$skill")"
  rm -rf "$target_dir/$name"
  cp -r "$skill" "$target_dir/$name"
  echo "installed $name"
done
echo "Skills installed to $target_dir. Start a new Claude Code session to load them."
