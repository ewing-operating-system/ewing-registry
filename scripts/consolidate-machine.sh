#!/bin/bash
# =============================================================
#  MACHINE CONSOLIDATION SCRIPT
#  Run on every Mac to unify GitHub + Supabase references
# =============================================================
#
#  GITHUB (unified):  ewing-operating-system
#    KILL: clawdking1-GH, ClawdKing-GH, clawdking1
#
#  SUPABASE (unified): rdnnhxhohwjucvjwbwch (and-call-command)
#    KILL: asavljgcnresdnadblse  (Phoenix TAM)
#    KILL: lhmuwrlpcdlzpfthrodm  (ColdCall Universe)
#    KILL: ginqabezgxaazkhuuvvw  (empty)
#    KILL: iwcvaowfogpffdllqtld  (debugger-tool)
#
#  SAFE TO RUN MULTIPLE TIMES — idempotent
# =============================================================

SB_TARGET="rdnnhxhohwjucvjwbwch"
SB_OLD=("asavljgcnresdnadblse" "lhmuwrlpcdlzpfthrodm" "ginqabezgxaazkhuuvvw" "iwcvaowfogpffdllqtld")

GH_TARGET="ewing-operating-system"
GH_OLD=("clawdking1-GH" "ClawdKing-GH" "clawdking1")

echo ""
echo "=========================================="
echo "  MACHINE CONSOLIDATION"
echo "  GitHub  -> $GH_TARGET"
echo "  Supabase -> $SB_TARGET (and-call-command)"
echo "=========================================="
echo ""
echo "Machine: $(hostname)"
echo "User:    $(whoami)"
echo "Date:    $(date)"
echo ""

CHANGES=0

# =============================================================
# PART 1: GITHUB
# =============================================================
echo "=== GITHUB ==="
echo ""

# 1a. Git global config
CURRENT_NAME=$(git config --global user.name 2>/dev/null)
echo "git user.name: $CURRENT_NAME"
for old in "${GH_OLD[@]}"; do
  if [ "$CURRENT_NAME" = "$old" ]; then
    git config --global user.name "$GH_TARGET"
    echo "  -> CHANGED to $GH_TARGET"
    CHANGES=$((CHANGES+1))
    break
  fi
done

# 1b. gh CLI
GH_ACCOUNT=$(gh auth status 2>&1 | grep "Logged in" | head -1)
echo "gh CLI: $GH_ACCOUNT"
if echo "$GH_ACCOUNT" | grep -qi "clawdking"; then
  echo ""
  echo "  !! NEEDS MANUAL FIX: run 'gh auth login'"
  echo "  !! Choose: GitHub.com > HTTPS > Web browser > log in as $GH_TARGET"
  echo ""
fi

# 1c. Git remotes in all repos
echo ""
echo "Scanning git repos for old remotes..."
for dir in $(find ~/ -maxdepth 5 -name ".git" -type d 2>/dev/null | grep -v Library | grep -v node_modules | grep -v .Trash | grep -v "Google Drive"); do
  repo_dir=$(dirname "$dir")
  for old in "${GH_OLD[@]}"; do
    if git -C "$repo_dir" remote -v 2>/dev/null | grep -q "$old"; then
      echo "  REPO: $repo_dir"
      git -C "$repo_dir" remote -v 2>/dev/null | grep "$old" | awk '{print $1}' | sort -u | while read remote_name; do
        old_url=$(git -C "$repo_dir" remote get-url "$remote_name" 2>/dev/null)
        new_url=$(echo "$old_url" | sed "s|$old|$GH_TARGET|g")
        git -C "$repo_dir" remote set-url "$remote_name" "$new_url"
        echo "    $remote_name: $old_url"
        echo "           -> $new_url"
        CHANGES=$((CHANGES+1))
      done
    fi
  done
done

# 1d. GitHub refs in skills, configs, env files
echo ""
echo "Scanning files for old GitHub references..."
SEARCH_DIRS="$HOME/.claude/skills $HOME/.zshrc $HOME/Projects $HOME/.openclaw $HOME/Downloads"
for old in "${GH_OLD[@]}"; do
  for f in $(grep -rl "$old" $SEARCH_DIRS 2>/dev/null | grep -v node_modules | grep -v ".git/" | grep -v Library/ | grep -v "consolidate-machine"); do
    sed -i '' "s|$old|$GH_TARGET|g" "$f"
    echo "  UPDATED: $f ($old -> $GH_TARGET)"
    CHANGES=$((CHANGES+1))
  done
done

echo ""

# =============================================================
# PART 2: SUPABASE
# =============================================================
echo "=== SUPABASE ==="
echo ""

echo "Scanning for old Supabase instance IDs..."
SEARCH_DIRS="$HOME/.claude/skills $HOME/.zshrc $HOME/Projects $HOME/.openclaw"

# Also search .env files specifically
ENV_FILES=$(find ~/Projects ~/.openclaw ~/Downloads ~/ -maxdepth 3 -name ".env*" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/Library/*" 2>/dev/null)

for old_id in "${SB_OLD[@]}"; do
  # Skills and config dirs
  for f in $(grep -rl "$old_id" $SEARCH_DIRS 2>/dev/null | grep -v node_modules | grep -v ".git/" | grep -v Library/ | grep -v "consolidate-machine"); do
    sed -i '' "s|$old_id|$SB_TARGET|g" "$f"
    echo "  UPDATED: $f ($old_id)"
    CHANGES=$((CHANGES+1))
  done

  # .env files
  for env_file in $ENV_FILES; do
    if grep -q "$old_id" "$env_file" 2>/dev/null; then
      sed -i '' "s|$old_id|$SB_TARGET|g" "$env_file"
      echo "  UPDATED: $env_file ($old_id)"
      CHANGES=$((CHANGES+1))
    fi
  done

  # Config files in projects
  for config_file in $(find ~/Projects -maxdepth 3 \( -name "config.py" -o -name "config.js" -o -name "config.ts" -o -name "supabase.ts" -o -name "supabase.js" \) 2>/dev/null | grep -v node_modules); do
    if grep -q "$old_id" "$config_file" 2>/dev/null; then
      sed -i '' "s|$old_id|$SB_TARGET|g" "$config_file"
      echo "  UPDATED: $config_file ($old_id)"
      CHANGES=$((CHANGES+1))
    fi
  done
done

echo ""

# =============================================================
# PART 3: ZSHRC RELOAD
# =============================================================
if [ -f ~/.zshrc ]; then
  source ~/.zshrc 2>/dev/null
  echo "Reloaded ~/.zshrc"
fi

echo ""

# =============================================================
# VERIFICATION
# =============================================================
echo "=== VERIFICATION ==="
echo ""

CLEAN=1

for old in "${GH_OLD[@]}"; do
  found=$(grep -rl "$old" $HOME/.claude/skills $HOME/.zshrc $HOME/Projects 2>/dev/null | grep -v node_modules | grep -v ".git/" | grep -v Library/ | grep -v "consolidate-machine" | head -5)
  if [ -n "$found" ]; then
    echo "STILL FOUND $old in:"
    echo "$found"
    CLEAN=0
  fi
  git_found=$(find ~/ -maxdepth 5 -name ".git" -type d 2>/dev/null | grep -v Library | grep -v node_modules | grep -v .Trash | while read d; do
    git -C "$(dirname "$d")" remote -v 2>/dev/null | grep "$old"
  done)
  if [ -n "$git_found" ]; then
    echo "STILL IN GIT REMOTES ($old):"
    echo "$git_found"
    CLEAN=0
  fi
done

for old_id in "${SB_OLD[@]}"; do
  found=$(grep -rl "$old_id" $HOME/.claude/skills $HOME/.zshrc $HOME/Projects $HOME/.openclaw 2>/dev/null | grep -v node_modules | grep -v ".git/" | grep -v Library/ | grep -v "consolidate-machine" | head -5)
  if [ -n "$found" ]; then
    echo "STILL FOUND $old_id in:"
    echo "$found"
    CLEAN=0
  fi
done

echo ""
echo "=========================================="
if [ "$CLEAN" -eq 1 ]; then
  echo "  STATUS: ALL CLEAN"
else
  echo "  STATUS: SOME REFS REMAIN (see above)"
fi
echo "  CHANGES MADE: $CHANGES"
echo ""
echo "  GitHub:   $GH_TARGET"
echo "  Supabase: https://$SB_TARGET.supabase.co"
echo "=========================================="
echo ""
if gh auth status 2>&1 | grep -qi "clawdking"; then
  echo "!! MANUAL STEP NEEDED:"
  echo "   Run: gh auth login"
  echo "   Choose: GitHub.com > HTTPS > Web browser"
  echo "   Log in as: $GH_TARGET"
  echo ""
fi
