#!/bin/bash
set -euo pipefail

# Belt-and-suspenders fallback.
#
# The skill now lives at .claude/skills/fabio-kdp/ inside the repo, so Claude
# Code auto-discovers it as a PROJECT skill — no install step is needed and
# /fabio-kdp works in every fresh session, including Claude Code on the web.
#
# This hook only adds a personal-scope symlink as a redundant safety net in
# case project-skill discovery is unavailable for some agent/runtime. It is
# idempotent and harmless.

SKILLS_DIR="/root/.claude/skills"
SKILL_NAME="fabio-kdp"
SKILL_SRC="${CLAUDE_PROJECT_DIR:-/home/user/kdp-studio}/.claude/skills/${SKILL_NAME}"

mkdir -p "$SKILLS_DIR"
ln -sfn "$SKILL_SRC" "$SKILLS_DIR/$SKILL_NAME"

echo "fabio-kdp project skill at $SKILL_SRC (also symlinked to $SKILLS_DIR/$SKILL_NAME)"
