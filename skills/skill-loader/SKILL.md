---
name: skill-loader
description: "ALWAYS TRIGGER ON FIRST MESSAGE OF EVERY SESSION. This skill loads Ewing's default skills at the start of any new Claude Code or Cowork session. Trigger whenever Ewing says 'skill loader', 'load my skills', 'start up', 'boot up', 'load defaults', or at the very first interaction of a new session. Also trigger if Ewing says 'load skills' or 'default skills'. This is Ewing's session bootstrapper — it ensures output-skill, prompt-refiner, skill-creator, and tech-translator are always active."
---

# Skill Loader

This skill bootstraps Ewing's default environment at the start of every session.

## What to do when this skill triggers

## Step 0: Sync skills from GitHub FIRST

Before loading anything, pull the latest skills from GitHub:
```bash
REGISTRY="$HOME/ewing-registry"
if [ -d "$REGISTRY/.git" ]; then
  cd "$REGISTRY" && git pull origin main --quiet
elif [ -d "/Users/clawdbot/ewing-registry/.git" ]; then
  cd /Users/clawdbot/ewing-registry && git pull origin main --quiet
else
  git clone https://github.com/ewing-operating-system/ewing-registry.git "$REGISTRY" 2>/dev/null || \
  git clone git@github.com:ewing-operating-system/ewing-registry.git "$REGISTRY" 2>/dev/null
fi
# Sync skills from registry to local
if [ -d "$REGISTRY/skills" ]; then
  for skill_dir in "$REGISTRY/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$HOME/.claude/skills/$skill_name"
    cp "$skill_dir"SKILL.md "$HOME/.claude/skills/$skill_name/SKILL.md" 2>/dev/null
  done
fi
```

This ensures every machine gets the latest skills before anything else runs.

## Step 1: Load these six skills

1. **output-skill** — Governs all communication with Ewing. Load first.
2. **prompt-refiner** — Intercepts messy prompts and restructures them before execution.
3. **skill-creator** — Lets Ewing build, edit, and optimize skills on the fly.
4. **tech-translator** — Translates developer jargon into plain English.
5. **debrief** — End-of-thread intelligence extraction. Harvest + Story + Audit in one command.
6. **skill-sync** — Keeps skills synchronized between GitHub and local. Pushes any new skills created during the session.

## How to load them

Use the Skill tool six times:
1. `skill: "output-skill"`
2. `skill: "prompt-refiner"`
3. `skill: "skill-creator"`
4. `skill: "tech-translator"`
5. `skill: "debrief"`
6. `skill: "skill-sync"`

After all six are loaded, confirm with a single line: "Default skills loaded: output-skill, prompt-refiner, skill-creator, tech-translator, debrief, skill-sync. Skills synced from GitHub."

Do not explain what each skill does. Do not ask questions. Just load them and confirm.

## Adding more defaults later

If Ewing says "add X to my defaults" or "make X a default skill", update this skill's load list to include the new skill.
