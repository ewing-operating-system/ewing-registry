---
name: debrief
description: End-of-session debrief that harvests artifacts, writes the thread story, audits what was built, and pushes everything to ewing-registry. Run this before closing any significant Claude session.
user_invocable: true
---

# Debrief

Full end-of-session wrap-up. Harvests this machine, tells the story of this thread, writes the audit, and pushes everything to GitHub.

## When triggered

Run when Ewing says "debrief", "run debrief", "wrap up", "end of session", "close out", or any request to document and preserve the work from this thread.

## Procedure

### Phase 1: Harvest

Scan for valuable artifacts created or modified in this session:

1. **Skills created/modified** — check `~/.claude/skills/` for recent changes
2. **Scheduled tasks** — check `~/.claude/scheduled-tasks/` for new or modified tasks
3. **Memory files** — check the project memory directory for new entries
4. **Code changes** — `git status` and `git diff` in the current working directory
5. **Files in Downloads** — check `~/Downloads/` for files modified today that look like artifacts (not installers/images)

Compile a manifest of everything found.

### Phase 2: Thread Story

Write a narrative summary of what happened in this session:

- **What was the goal?** — What did Ewing ask for?
- **What was built?** — Skills, scripts, configs, integrations
- **What decisions were made?** — Architecture choices, tool selections, tradeoffs
- **What's unfinished?** — Open items, blockers, next steps
- **Key artifacts** — List with paths

Save to `~/ewing-registry/debriefs/YYYY-MM-DD-HHmm-{topic}.md`

### Phase 3: Audit

Check system health:

1. **Skill inventory** — List all skills, check each has a SKILL.md
2. **Scheduled tasks** — List all, check if any are broken/disabled
3. **Repo status** — Any uncommitted changes across repos?
4. **Credential check** — Are all referenced API keys still valid? (don't log the keys)

Save audit to `~/ewing-registry/audits/YYYY-MM-DD-HHmm-audit.md`

### Phase 4: Push to GitHub

1. Run skill-sync (pull latest, push new skills)
2. Commit debriefs and audits
3. Push everything

```bash
cd ~/ewing-registry
git add -A
git commit -m "debrief: $(date +%Y-%m-%d) — {topic summary}"
git push origin main
```

### Phase 5: Report

Print a final summary for Ewing:
- Thread story (2-3 sentences)
- Artifacts preserved (count + list)
- Skills synced (pulled/pushed)
- Audit findings (if any issues)
- Next steps / open items
