#!/bin/bash
set -euo pipefail

# Install fabio-kdp skill so /fabio-kdp is available in every session.
# Claude Code on the web starts in a fresh container each time, so the
# ~/.claude/skills/ symlink must be recreated at session start.

SKILLS_DIR="/root/.claude/skills"
SKILL_NAME="fabio-kdp"
SKILL_SRC="${CLAUDE_PROJECT_DIR:-/home/user/kdp-studio}/skills/${SKILL_NAME}"

mkdir -p "$SKILLS_DIR"
ln -sfn "$SKILL_SRC" "$SKILLS_DIR/$SKILL_NAME"

echo "fabio-kdp skill installed: $SKILLS_DIR/$SKILL_NAME -> $SKILL_SRC"
