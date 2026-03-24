---
name: skill-loader
description: "ALWAYS TRIGGER ON FIRST MESSAGE OF EVERY SESSION. This skill loads Ewing's default skills at the start of any new Claude Code or Cowork session. Trigger whenever Ewing says 'skill loader', 'load my skills', 'start up', 'boot up', 'load defaults', or at the very first interaction of a new session. Also trigger if Ewing says 'load skills' or 'default skills'. This is Ewing's session bootstrapper — it ensures output-skill, task-router, prompt-refiner, skill-creator, and tech-translator are always active."
---

# Skill Loader

This skill bootstraps Ewing's default environment at the start of every session.

## What to do when this skill triggers

Load these five skills immediately, in this order:

1. **output-skill** — Governs all communication with Ewing. Load first because it affects how everything else gets presented.
2. **task-router** — Intercepts every prompt and routes it to the right environment (Claude Code, Cowork, Chat, or external tool). Also flags repeatable tasks for automation. Load second so routing happens before execution.
3. **prompt-refiner** — Intercepts messy prompts and restructures them before execution.
4. **skill-creator** — Lets Ewing build, edit, and optimize skills on the fly.
5. **tech-translator** — Translates terminal output, error messages, and developer jargon into plain English so Ewing can learn while he builds.

## How to load them

Use the Skill tool five times:
1. `skill: "output-skill"`
2. `skill: "task-router"`
3. `skill: "prompt-refiner"`
4. `skill: "skill-creator"`
5. `skill: "tech-translator"`

After all five are loaded, confirm with a single line: "Default skills loaded: output-skill, task-router, prompt-refiner, skill-creator, tech-translator."

Do not explain what each skill does. Do not ask questions. Just load them and confirm.

## Adding more defaults later

If Ewing says "add X to my defaults" or "make X a default skill", update this skill's load list to include the new skill.
