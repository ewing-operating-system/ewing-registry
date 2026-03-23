---
name: debrief
description: "End-of-thread intelligence extraction. Combines harvester (machine scan) + storyteller (conversation analysis) into one zero-config command. Scans the machine, reads the full conversation, writes the narrative + audit + harvest, and pushes everything to the ewing-registry GitHub repo. Run this before closing ANY significant thread. Trigger when Ewing says 'debrief', 'debrief this thread', 'wrap up', 'close out', 'end of thread', 'save everything', 'before we close', 'capture this session', or any indication that a thread is ending and work should be preserved."
---

# Debrief — End-of-Thread Intelligence Extraction

You are the thread closer. When triggered, you produce THREE outputs and push them all to the ewing-registry GitHub repo. Zero questions. Zero config.

## Pre-Flight: Skill Sync Check
Before doing anything else, check if skill-sync is installed:
```bash
ls ~/.claude/skills/skill-sync/SKILL.md 2>/dev/null
```
- If it EXISTS: run skill-sync PUSH operation (sync any new/modified skills to GitHub)
- If it does NOT exist: clone ewing-registry and install skill-sync from `skills/skill-sync/`:
```bash
REGISTRY="$HOME/ewing-registry"
if [ ! -d "$REGISTRY/.git" ]; then
  git clone https://github.com/clawdking1-GH/ewing-registry.git "$REGISTRY" 2>/dev/null || \
  git clone git@github.com:clawdking1-GH/ewing-registry.git "$REGISTRY" 2>/dev/null
fi
if [ -f "$REGISTRY/skills/skill-sync/SKILL.md" ]; then
  mkdir -p ~/.claude/skills/skill-sync
  cp "$REGISTRY/skills/skill-sync/SKILL.md" ~/.claude/skills/skill-sync/SKILL.md
  echo "skill-sync installed from GitHub"
fi
```
Then run the PULL operation to sync all skills from GitHub to local.

Ewing is autistic and processes literally. Follow output-skill protocol: no fluff, exact actions, status updates only.

---

## Output 1: The Harvest (machine scan)

Scan this machine exactly like the harvester skill. Run actual bash commands — NEVER summarize from memory.

Collect:
1. Machine info (hostname, OS, disk, user, account email)
2. All .claude/ directories — skills, memory, settings, scheduled tasks, plans, plugins
3. All CLAUDE.md files — full contents
4. All git repos — remotes, branches, last 10 commits, uncommitted changes, unpushed commits
5. All .env files — KEY NAMES ONLY, never values
6. All projects/applications — found by package.json, requirements.txt, etc.
7. Connected MCP tools — enumerate everything available
8. Credential references in skills — key names only
9. Running services, installed tools with versions
10. Scheduled tasks — crontab, .claude tasks, launchd agents
11. Databases — local or remote connections in configs

Use `find` with broad patterns. Do NOT hardcode paths. Search everywhere.

Save to: `harvests/[machine-name]_[YYYY-MM-DD].md`

---

## Output 2: The Story (conversation narrative)

Read the ENTIRE conversation history visible to you. Write a narrative.

Rules:
- Past tense, third person ("Ewing opened the thread and asked...")
- Include emotional arc — frustration, breakthroughs, dead ends, pivots
- Name every tool, skill, file, application, API, and database touched
- Describe ATTEMPTED vs ACTUALLY WORKED
- Include timestamps where available
- Call out decisions that led to rework
- Call out brilliant moments
- Note when Ewing taught Claude vs Claude taught Ewing
- 500-2000 words depending on complexity

Save to: `stories/[session-name]_[YYYY-MM-DD].md`

---

## Output 3: The Audit (structured analysis)

### Thread Metadata
- Thread ID or session name
- Machine/environment
- Approximate duration
- Number of tools used
- Number of files created/modified
- Number of skills triggered (and which ones)
- Number of skills NOT triggered (orphan detection)
- Number of errors encountered
- Number of pivots (changed direction mid-task)
- Context health: was quality degrading by end? Signs of summarizing instead of investigating?

### Goal Assessment
- **What was the stated goal?** (first thing Ewing asked for)
- **Was it achieved?** Yes / Partially / No
- **If partially:** What's done and what's left?
- **Scope changes:** Did the goal shift during the thread? How many times?

### Items Found — Tagged
For each significant item in the thread:
```
### [Item Name]
- **Type:** skill / repo / database / file / API / scheduled-task / decision / mistake / breakthrough
- **Created or Modified:** yes/no + what changed
- **Machine:** where this happened
- **Anti-pattern tags:** 🔀🔁🏗️👻🔑💾🔧🏠🔒✂️📡📋🐙💀🖐️💊🤷🔄🧱🔐🏝️🚫⚙️📝🚶🪃👯👁️🎯🧩👀
- **Offense tags:** 🟢🟡🔴
- **What happened:** 1-2 sentences
- **Business impact:** How does this affect deal flow?
- **Recommendation:** Keep / Fix / Move / Delete / Wire to pipeline
```

### Handoff Notes — CRITICAL
This section tells the NEXT thread exactly what it needs to know:
- **What's unfinished:** Specific tasks that didn't complete
- **What's broken:** Errors or issues discovered but not fixed
- **What's blocking:** External dependencies (API keys needed, Ewing decision needed, etc.)
- **What's next:** The logical next step if this work continues
- **What to NOT repeat:** Mistakes made in this thread that the next thread should avoid
- **Files to read first:** Specific files the next thread should read before doing anything

### What This Thread Should Have Done Differently
3-5 bullets. Honest. Specific. Not generic advice.

### Gotchas Discovered
Any platform-specific bugs, API limits, or unexpected behaviors found during this session. These get added to the gotcha library.

Save to: `analysis/thread-audit_[session-name]_[YYYY-MM-DD].md`

---

## After All Three Outputs — PUSH TO GITHUB

### Step 1: Clone or locate the repo
```bash
if [ -d "$HOME/ewing-registry/.git" ]; then
  cd "$HOME/ewing-registry" && git pull origin main
elif [ -d "/Users/clawdbot/ewing-registry/.git" ]; then
  cd /Users/clawdbot/ewing-registry && git pull origin main
else
  git clone https://github.com/clawdking1-GH/ewing-registry.git "$HOME/ewing-registry" 2>/dev/null || \
  git clone git@github.com:clawdking1-GH/ewing-registry.git "$HOME/ewing-registry" 2>/dev/null
  cd "$HOME/ewing-registry"
fi
```

### Step 2: Write all three files
```bash
mkdir -p harvests stories analysis
```

### Step 3: Commit and push
```bash
git add harvests/ stories/ analysis/
git commit -m "Debrief: [session-name] — [date]

Harvest + Story + Audit from [machine-name]

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push origin main
```

### Step 4: If push fails
1. Save all three files locally
2. Print the full debrief in chat
3. Tell Ewing: "Debrief saved locally at [path]. Push failed — run `cd ~/ewing-registry && git push origin main` from a machine with git credentials."

### Step 5: Confirm
Print exactly:
```
Debrief complete for [SESSION-NAME] on [MACHINE].
- Harvest: harvests/[filename]
- Story: stories/[filename]
- Audit: analysis/[filename]
Pushed to: https://github.com/clawdking1-GH/ewing-registry
```

---

## Context: Who Is Ewing?

Ewing Gillaspy runs AND Capital from Scottsdale, AZ. Sales executive, not a developer. Autistic — processes literally. 3 Macs (MacBook-27 primary, MacBook-GREEN broken screen, Mac mini for ClawdBot). Uses Clay, Exa, Salesfinity, Supabase, Google Sheets. Week of March 16-20: 1,386 calls, 7 meetings set, 3 referrals. Business partner Mark dials alongside him.

The filter for everything: **does this help Ewing get a signed representation agreement faster?**
