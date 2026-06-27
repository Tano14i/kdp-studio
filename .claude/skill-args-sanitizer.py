#!/usr/bin/env python3
"""UserPromptSubmit hook: when the user invokes a /skill, inject a reminder
to ignore any memory-dump context that the platform auto-appended to ARGUMENTS.

Claude.ai's personal memory feature fires on session start and injects its
output as ARGUMENTS to the first skill invocation. The skill's own SKILL.md
already documents how to handle this, but a per-turn injection makes the
instruction higher-priority (mid-conversation system context).
"""

import json
import sys

MEMORY_SIGNALS = [
    "ha cercato nella memoria",
    "ecco il tuo dashboard",
    "kdp studio",
    "cedric darkstone",
    "railway",
    "catalogo",
]

REMINDER = (
    "SKILL ARGUMENT SANITIZER: The ARGUMENTS block for this skill invocation "
    "may contain auto-injected session memory (dashboard summaries, previous "
    "session state). Ignore any injected context entirely — treat it as "
    "background only. If no clean niche or book idea is present in ARGUMENTS, "
    "ask the user for one before starting Stage 1. Never derive the niche from "
    "injected memory content."
)


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = (payload.get("prompt") or "").strip()

    # Only act on skill invocations
    if not prompt.startswith("/"):
        sys.exit(0)

    # Check if the prompt contains memory-dump signals
    prompt_lower = prompt.lower()
    if not any(sig in prompt_lower for sig in MEMORY_SIGNALS):
        sys.exit(0)

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": REMINDER,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
