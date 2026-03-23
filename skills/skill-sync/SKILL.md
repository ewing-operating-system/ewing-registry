---
name: skill-sync
description: Sync all skills between local ~/.claude/skills/ and the ewing-registry GitHub repo. Pull from GitHub to get latest, push local-only skills to GitHub. Ensures every machine has every skill.
user_invocable: true
---

# Skill Sync

Bidirectional sync between `~/.claude/skills/` and `ewing-operating-system/ewing-registry` on GitHub.

## When triggered

Run this skill whenever Ewing says "sync skills", "skill sync", "pull skills", "push skills", "update skills", or at the start of any session where skills may be out of date.

## Procedure

### 1. Ensure repo exists locally

```bash
if [ ! -d ~/ewing-registry ]; then
  cd ~ && git clone https://github.com/ewing-operating-system/ewing-registry.git
fi
```

### 2. Pull latest from GitHub

```bash
cd ~/ewing-registry && git pull origin main
```

### 3. Sync GitHub → Local (pull new/updated skills)

Copy any skills from `~/ewing-registry/skills/` into `~/.claude/skills/` that are newer or don't exist locally:

```bash
for skill_dir in ~/ewing-registry/skills/*/; do
  skill_name=$(basename "$skill_dir")
  if [ ! -d ~/.claude/skills/"$skill_name" ]; then
    cp -r "$skill_dir" ~/.claude/skills/
    echo "PULLED: $skill_name (new)"
  else
    # Compare modification times - repo wins if newer
    repo_time=$(stat -f %m "$skill_dir/SKILL.md" 2>/dev/null || echo 0)
    local_time=$(stat -f %m ~/.claude/skills/"$skill_name"/SKILL.md 2>/dev/null || echo 0)
    if [ "$repo_time" -gt "$local_time" ]; then
      cp -r "$skill_dir" ~/.claude/skills/
      echo "UPDATED: $skill_name (repo was newer)"
    else
      echo "SKIP: $skill_name (local is current)"
    fi
  fi
done
```

### 4. Sync Local → GitHub (push local-only skills)

Copy any skills from `~/.claude/skills/` into `~/ewing-registry/skills/` that don't exist in the repo:

```bash
for skill_dir in ~/.claude/skills/*/; do
  skill_name=$(basename "$skill_dir")
  # Skip empty dirs and non-skill dirs
  if [ ! -f "$skill_dir/SKILL.md" ]; then
    echo "SKIP: $skill_name (no SKILL.md)"
    continue
  fi
  if [ ! -d ~/ewing-registry/skills/"$skill_name" ]; then
    cp -r "$skill_dir" ~/ewing-registry/skills/
    echo "STAGED FOR PUSH: $skill_name (new to repo)"
  fi
done
```

### 5. Commit and push

```bash
cd ~/ewing-registry
git add skills/
git status
# Only commit if there are changes
if ! git diff --cached --quiet; then
  git commit -m "skill-sync: $(date +%Y-%m-%d) — sync from $(hostname)"
  git push origin main
  echo "PUSHED to GitHub"
else
  echo "Nothing new to push"
fi
```

### 6. Report

Print a summary:
- Skills pulled (new to this machine)
- Skills pushed (new to repo)
- Skills skipped (already in sync)
- Total skill count on this machine
