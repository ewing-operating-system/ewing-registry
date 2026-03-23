# Diagnostic Report: The clawdking / ewing-operating-system Identity Split
**Date:** 2026-03-23
**Machine:** Mac mini (ewinggillaspy / MacBook-27.local)
**Working dir:** ~/Github/coldcall-universe
**Purpose:** Root cause analysis for Claude Code to investigate on the Mac mini

---

## What Issues Were Found

### 1. The ewing-registry repo didn't exist
Every skill, every debrief reference, every sync command pointed to `clawdking1-GH/ewing-registry.git`. That repo **does not exist**. The GitHub account authenticated on this machine is `ewing-operating-system`, not `clawdking1-GH`. When I tried to clone, git returned `ERROR: Repository not found`.

### 2. GitHub identity mismatch
- **Authenticated account:** `ewing-operating-system` (confirmed via `gh auth status`)
- **Referenced account in skills/prompts:** `clawdking1-GH`
- **All 9 repos on GitHub** are under `ewing-operating-system`
- **Zero repos** exist under `clawdking1-GH`

This means every instruction that says "push to clawdking1-GH/ewing-registry" will fail silently or error out.

### 3. Storyteller skill was an empty directory
The `~/.claude/skills/storyteller/` folder existed but had no SKILL.md inside it. The actual SKILL.md was orphaned in `~/Downloads/storyteller-SKILL.md`. A previous session created the folder but never copied the file in.

### 4. skill-sync and debrief didn't exist anywhere
These two skills were referenced in conversation history and cross-machine instructions but had never been built. Every session that said "run skill-sync" or "run debrief" was invoking skills that didn't exist.

### 5. `cp -r` flattened the directory structure
When copying skills to the repo, `cp -r ~/.claude/skills/*/ ~/ewing-registry/skills/` dumped everything flat instead of preserving the skill-per-folder structure. Had to clean up and redo.

---

## Why So Many Permission Prompts

Claude Code prompts for permission on every `git` command, every file write outside the working directory, and every shell command that touches `~/.claude/`. This session hit all three categories repeatedly:

1. **Cloning a repo** — shell command, needs approval
2. **Creating a GitHub repo** via `gh repo create` — shell command
3. **Writing to `~/.claude/skills/`** — outside working directory
4. **Copying files between directories** — shell commands
5. **Git add, commit, push** on a DIFFERENT repo (`~/ewing-registry/`) — not the working directory

The root cause: **the working directory is `~/Github/coldcall-universe` but all the work was in `~/ewing-registry/` and `~/.claude/skills/`**. Every operation was "outside the project," triggering permission prompts. A normal session working inside one repo would have far fewer prompts.

---

## Where Results Were Stored

Everything is in the `ewing-registry` repo, pushed to GitHub:

```
~/ewing-registry/                  (local clone)
├── README.md                      (repo overview + skill table)
├── skills/                        (11 skill folders, each with SKILL.md)
│   ├── cold-call-workflow/
│   ├── debrief/                   ← NEW (built this session)
│   ├── disk-cleanup/
│   ├── ewing-connectors/
│   ├── finance-agent/
│   ├── password-migration/
│   ├── prompt-refiner/
│   ├── recording-collector/
│   ├── skill-sync/                ← NEW (built this session)
│   ├── storyteller/               ← FIXED (was empty, now has SKILL.md)
│   └── system-auditor/
├── stories/
│   └── coldcall-universe_2026-03-23.md    (thread narrative)
├── audits/
│   ├── 2026-03-23-audit.md                (system audit with anti-pattern tags)
│   └── 2026-03-23-diagnostic-report.md    (THIS FILE)
└── debriefs/                      (empty, ready for future debriefs)
```

**GitHub URL:** https://github.com/ewing-operating-system/ewing-registry
**Visibility:** Private

---

## What I Found When Trying to Push

1. `git clone https://github.com/clawdking1-GH/ewing-registry.git` → **FAILED** (repo not found)
2. `gh repo list` → showed all repos are under `ewing-operating-system`
3. Created repo under correct account → worked
4. Push succeeded on first try after creating under correct account

---

## Root Problem

**There are two GitHub identities and they're not aligned.**

- `clawdking1-GH` — referenced in skills, prompts, and cross-machine instructions. May be a real account on a different machine, or may have been a typo that propagated.
- `ewing-operating-system` — the actual authenticated account on this Mac mini. All repos live here.

Every time a session on this Mac mini follows instructions that say "clawdking" it breaks. Every time the MacBook follows instructions that say "ewing-operating-system" it might also break if it's authenticated differently.

**Secondary problem:** Skills that are referenced but never built. Both skill-sync and debrief were phantom skills — invoked in prompts but never created. Sessions would try to run them, fail silently or get confused, and either skip the step or try to rebuild from scratch (creating duplicates).

---

## Master Solution

### Step 1: Identify which GitHub account each machine uses
Run this on EVERY machine:
```bash
gh auth status
```
Document which account is authenticated where.

### Step 2: Pick ONE canonical account
If `clawdking1-GH` is a real account with repos, decide: is it the primary or is `ewing-operating-system`? All repos should live under ONE account.

### Step 3: Update all references
Every SKILL.md, every CLAUDE.md, every prompt that references a GitHub URL needs to use the canonical account name. Search and replace:
```bash
grep -r "clawdking1-GH" ~/.claude/ ~/Github/
grep -r "clawdking" ~/.claude/ ~/Github/
```

### Step 4: Make skill-sync the first thing that runs
Add to session-start hooks or CLAUDE.md:
```
On session start: run skill-sync to pull latest from ewing-registry
```

### Step 5: Never build skills that already exist
Before building any skill, check:
```bash
ls ~/ewing-registry/skills/
```
If it's there, pull it. Don't rebuild.

---

## Commands for Claude Code on Mac Mini to Investigate

```bash
# 1. Which GitHub account is this machine using?
gh auth status

# 2. Does clawdking1-GH exist as a GitHub account?
gh api users/clawdking1-GH 2>&1 | head -5

# 3. Are there any references to clawdking anywhere in the system?
grep -r "clawdking" ~/.claude/ 2>/dev/null | grep -v ".git"
grep -r "clawdking" ~/Github/ 2>/dev/null | grep -v ".git"

# 4. What's the git remote for each repo?
for repo in ~/Github/*/; do echo "=== $(basename $repo) ==="; cd "$repo" && git remote -v; echo; done

# 5. Is ewing-registry cloned locally?
ls ~/ewing-registry/ 2>/dev/null || echo "NOT CLONED"

# 6. Pull latest skills
cd ~/ewing-registry && git pull origin main
cp -r ~/ewing-registry/skills/* ~/.claude/skills/
echo "Skills synced"
```

---

## Summary

The back-and-forth between machines is caused by a **split identity problem**. Two GitHub accounts, unclear which is canonical, skills referencing the wrong one, and phantom skills that were invoked but never built. The fix is: pick one account, update all references, and make skill-sync automatic so every machine stays current.
