---
name: skill-sync
description: "GitHub skills synchronization manager. Keeps all skills synchronized between GitHub (ewing-registry) and local ~/.claude/skills/. GitHub is the single source of truth. Every skill creation, modification, or deletion gets pushed to GitHub. Every new session pulls the latest. Eliminates skill mismatch, duplicate skills, and multi-machine drift across the fleet."
---

# Skill Sync — GitHub as Single Source of Truth

## Principle
`~/.claude/skills/` is a LOCAL CACHE. `ewing-registry/skills/` on GitHub is the SOURCE OF TRUTH. Every machine pulls from the same repo. Every skill change gets pushed.

This eliminates: 🧩 SKILL-MISMATCH, 👯 DUPLICATE-SKILL, 📡 NO-SINGLE-SOURCE-OF-TRUTH

## Repo
- **URL:** `https://github.com/ewing-operating-system/ewing-registry.git`
- **Skills directory:** `skills/` (at repo root)
- **Local cache:** `~/.claude/skills/`

---

## Operation 1: PULL (sync GitHub → local)

Run this at the START of every session, or when Ewing says "pull skills" or "sync skills".

```bash
# Clone or update the registry
REGISTRY="$HOME/ewing-registry"
if [ -d "$REGISTRY/.git" ]; then
  cd "$REGISTRY" && git pull origin main --quiet
else
  git clone https://github.com/ewing-operating-system/ewing-registry.git "$REGISTRY" 2>/dev/null || \
  git clone git@github.com:ewing-operating-system/ewing-registry.git "$REGISTRY" 2>/dev/null
fi

# Check if skills/ directory exists in registry
if [ -d "$REGISTRY/skills" ]; then
  # Sync each skill from registry to local
  for skill_dir in "$REGISTRY/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    local_dir="$HOME/.claude/skills/$skill_name"
    mkdir -p "$local_dir"
    cp "$skill_dir"SKILL.md "$local_dir/SKILL.md" 2>/dev/null
  done
  echo "Skills synced from GitHub: $(ls "$REGISTRY/skills/" | wc -l | tr -d ' ') skills"
else
  echo "No skills/ directory in ewing-registry yet. Will create on first push."
fi
```

Report what was pulled: new skills, updated skills, unchanged skills.

---

## Operation 2: PUSH (sync local → GitHub)

Run this EVERY TIME a skill is created or modified, or when Ewing says "push skills".

```bash
REGISTRY="$HOME/ewing-registry"
SKILLS_DIR="$HOME/.claude/skills"

# Ensure registry exists
if [ ! -d "$REGISTRY/.git" ]; then
  git clone https://github.com/ewing-operating-system/ewing-registry.git "$REGISTRY" 2>/dev/null || \
  git clone git@github.com:ewing-operating-system/ewing-registry.git "$REGISTRY" 2>/dev/null
fi

cd "$REGISTRY" && git pull origin main --quiet

# Create skills directory in registry if it doesn't exist
mkdir -p "$REGISTRY/skills"

# Copy ALL local skills to registry
for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name=$(basename "$skill_dir")
  # Skip if it's not a directory with a SKILL.md
  if [ -f "$skill_dir/SKILL.md" ]; then
    mkdir -p "$REGISTRY/skills/$skill_name"
    cp "$skill_dir/SKILL.md" "$REGISTRY/skills/$skill_name/SKILL.md"
  fi
done

# Commit and push
cd "$REGISTRY"
git add skills/
CHANGES=$(git diff --cached --name-only)
if [ -n "$CHANGES" ]; then
  git commit -m "Skill sync: $(echo "$CHANGES" | wc -l | tr -d ' ') skills updated from $(hostname)

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
  git push origin main
  echo "Skills pushed to GitHub: $CHANGES"
else
  echo "All skills already in sync with GitHub."
fi
```

---

## Operation 3: CHECK (detect drift)

Run this to compare local skills vs GitHub skills and report differences.

```bash
REGISTRY="$HOME/ewing-registry"
SKILLS_DIR="$HOME/.claude/skills"

echo "=== Skills on GitHub but NOT local ==="
for skill_dir in "$REGISTRY/skills"/*/; do
  skill_name=$(basename "$skill_dir")
  if [ ! -d "$SKILLS_DIR/$skill_name" ]; then
    echo "  MISSING locally: $skill_name"
  fi
done

echo "=== Skills local but NOT on GitHub ==="
for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name=$(basename "$skill_dir")
  if [ ! -d "$REGISTRY/skills/$skill_name" ]; then
    echo "  NOT pushed: $skill_name"
  fi
done

echo "=== Skills that differ ==="
for skill_dir in "$REGISTRY/skills"/*/; do
  skill_name=$(basename "$skill_dir")
  if [ -f "$SKILLS_DIR/$skill_name/SKILL.md" ] && [ -f "$skill_dir/SKILL.md" ]; then
    if ! diff -q "$SKILLS_DIR/$skill_name/SKILL.md" "$skill_dir/SKILL.md" > /dev/null 2>&1; then
      echo "  DIFFERS: $skill_name"
    fi
  fi
done
```

---

## When To Run

| Trigger | Operation |
|---|---|
| Session start (via skill-loader) | PULL |
| Skill created or modified | PUSH immediately |
| Ewing says "sync skills" | CHECK then PUSH |
| Debrief runs | CHECK then PUSH (debrief checks if skill-sync is installed first) |
| Ewing says "pull skills" | PULL |

---

## Interaction with Debrief

The debrief skill should:
1. Check if skill-sync is installed: `ls ~/.claude/skills/skill-sync/SKILL.md`
2. If NOT installed: run PULL operation to install it from GitHub
3. If installed: run PUSH operation to sync any new skills created during the session

---

## Interaction with Skill-Creator

CRITICAL: Any time a new skill is created or an existing skill is modified:
1. Write to `~/.claude/skills/[name]/SKILL.md` (local — so Claude can use it immediately)
2. Run PUSH operation (so GitHub gets it immediately)
3. Confirm: "Skill [name] saved locally and pushed to GitHub."

If push fails, tell Ewing: "Skill saved locally but GitHub push failed. Run `cd ~/ewing-registry && git add skills/ && git commit -m 'Skill update' && git push` from a machine with credentials."

---

## NEVER do this
- Never store skills ONLY on GitHub without the local copy — Claude can't read them from GitHub directly
- Never store skills ONLY locally without pushing — other machines won't get them
- Never modify a skill in the registry repo without also updating the local copy
- Never create a skill without pushing it — that's how SKILL-MISMATCH happens
