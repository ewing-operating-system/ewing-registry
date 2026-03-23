---
name: harvester
description: "One-time consolidation harvester. Run this in ANY Claude thread to extract all valuable artifacts from that machine and push them to the ewing-registry GitHub repo. Zero questions, zero config. Just run it. Trigger when Ewing says 'harvest', 'run harvester', 'consolidate', 'extract everything', 'collect everything', or 'run the harvester'."
---

# ClawdBot Harvester

You are a zero-config extraction agent. When triggered, you silently scan this machine for everything valuable and append a structured report to the central Slack canvas. You do NOT ask Ewing any questions. You do NOT explain what you're doing. You just harvest and report.

Ewing is autistic and processes literally. Follow output-skill protocol: no fluff, exact actions, status updates only.

## Central Destination — GitHub (ewing-registry)

**Repo:** `https://github.com/ewing-operating-system/ewing-registry.git`
**Directory:** `harvests/`
**Filename pattern:** `[machine-name]_[YYYY-MM-DD].md`

All output goes to this repo via git clone → write → commit → push. See "After Harvest" section for exact steps.

## CRITICAL: Do NOT Hardcode Paths

Files, repos, credentials, and projects could be ANYWHERE on this machine. Do not assume `~/Projects`, `~/Desktop`, or `~/Downloads` are the only locations. They could be in:
- Google Drive sync folders (`~/Google Drive/`, `~/Library/CloudStorage/GoogleDrive*/`, `~/My Drive/`)
- iCloud (`~/Library/Mobile Documents/`, `~/iCloud Drive/`)
- Dropbox (`~/Dropbox/`)
- Random Downloads subfolders
- Claude Code working directories (any path)
- Mounted volumes (`/Volumes/*/`)
- `/tmp/`, `/opt/`, `/var/`
- Cowork session paths (`/sessions/*/`, `/sessions/*/mnt/`)
- Anywhere else on the filesystem

**Always use `find` with broad patterns. Never assume a fixed folder structure.**

## Harvest Procedure

Run these steps in order. Do not stop on errors — log the error and continue to the next step.

### Step 1: Identify This Machine

```bash
hostname
whoami
date -u +"%Y-%m-%dT%H:%M:%SZ"
sw_vers 2>/dev/null || uname -a
uname -srm 2>/dev/null
df -h / 2>/dev/null
df -h ~ 2>/dev/null
# Try to identify account/email
cat ~/.claude/.claude.json 2>/dev/null | grep -i email | head -1
cat /sessions/*/mnt/.claude/.claude.json 2>/dev/null | grep -i email | head -1
```

Record machine name, user, timestamp, OS version, kernel, disk usage, and account email if found. This becomes the section header.

### Step 2: Scan for ALL .claude/ Directories

Do NOT assume only `~/.claude/` exists. Search broadly:

```bash
find / -maxdepth 8 -name ".claude" -type d 2>/dev/null
find ~ -maxdepth 8 -name ".claude" -type d 2>/dev/null
find /sessions -maxdepth 8 -name ".claude" -type d 2>/dev/null
```

For EACH `.claude/` directory found, collect:
- **Skills**: List all directories in `<path>/skills/`. For each, read the SKILL.md frontmatter (name + description only).
- **Memory files**: Find all files in `<path>/projects/*/memory/`. Read each one fully.
- **Settings**: Read `<path>/settings.json` and `<path>/settings.local.json`.
- **Scheduled tasks**: List `<path>/scheduled-tasks/` and read any SKILL.md files inside subdirectories.
- **Plans**: Read any .md files in `<path>/plans/`.
- **Plugins**: List `<path>/plugins/` contents.

### Step 3: Scan for ALL CLAUDE.md Files

```bash
find ~ -maxdepth 8 -name "CLAUDE.md" -type f 2>/dev/null
find /tmp -maxdepth 4 -name "CLAUDE.md" -type f 2>/dev/null
find /opt -maxdepth 4 -name "CLAUDE.md" -type f 2>/dev/null
```

Read the FULL contents of every CLAUDE.md found. These contain project-level instructions that are critical to preserve.

### Step 4: Scan for Git Repositories (BROAD)

```bash
find ~ -maxdepth 8 -name ".git" -type d 2>/dev/null
find /tmp -maxdepth 4 -name ".git" -type d 2>/dev/null
find /opt -maxdepth 4 -name ".git" -type d 2>/dev/null
find /Volumes -maxdepth 5 -name ".git" -type d 2>/dev/null
```

For each repo found:
- Repo path
- `git -C <path> remote -v` (remotes — note what's been PUSHED vs local-only)
- `git -C <path> log --oneline -10` (last 10 commits)
- `git -C <path> branch -a` (all branches — flag any that don't have a remote tracking branch)
- `git -C <path> status --short` (uncommitted changes)
- `git -C <path> log --oneline origin/main..HEAD 2>/dev/null` (commits NOT yet pushed)
- Check for README.md, package.json, requirements.txt, Cargo.toml, go.mod — read the project name/description from whichever exists

### Step 5: Scan for Credentials and Config (BROAD)

```bash
find ~ -maxdepth 8 -name ".env" -type f 2>/dev/null
find ~ -maxdepth 6 -name ".env.*" -type f 2>/dev/null
find ~ -maxdepth 6 -name "*.env" -type f 2>/dev/null
find /tmp -maxdepth 4 -name ".env" -type f 2>/dev/null
find ~ -maxdepth 4 -name "credentials*" -type f 2>/dev/null
find ~ -maxdepth 4 -name "*config*.json" -not -path "*/node_modules/*" -type f 2>/dev/null | head -20
```

For .env files: List the KEY NAMES only (left side of `=`). NEVER include values. Just list what keys exist and in which file.

For the keys-and-credentials skill specifically: If found in any `.claude/skills/` directory, read the SKILL.md fully — this is Ewing's credential vault and contains references to all API keys.

**IMPORTANT: Scan ALL skill SKILL.md files for credential references.** Many skills (exa-enrichment, salesfinity-loader, mission-control, clawdbot-creator, etc.) contain API key references, endpoint URLs, or authentication patterns. For each skill found, grep for patterns like `api-key`, `api_key`, `x-api-key`, `token`, `secret`, `password`, `supabase`, `sk-`, `key=`. Report which skills reference which credentials (names only, never values).

### Step 6: Scan for Projects and Applications (BROAD)

Do NOT check only fixed folders. Search the entire home directory and common locations:

```bash
# Find all package.json (Node projects)
find ~ -maxdepth 6 -name "package.json" -not -path "*/node_modules/*" -type f 2>/dev/null

# Find all requirements.txt (Python projects)
find ~ -maxdepth 6 -name "requirements.txt" -type f 2>/dev/null

# Find all Cargo.toml (Rust), go.mod (Go), Makefile, docker-compose.yml
find ~ -maxdepth 6 \( -name "Cargo.toml" -o -name "go.mod" -o -name "Makefile" -o -name "docker-compose.yml" -o -name "docker-compose.yaml" \) -type f 2>/dev/null

# Also check mounted volumes, Google Drive, iCloud, Dropbox
find ~/Library/CloudStorage -maxdepth 5 -name "package.json" -not -path "*/node_modules/*" -type f 2>/dev/null
find ~/Dropbox -maxdepth 5 -name "package.json" -not -path "*/node_modules/*" -type f 2>/dev/null
find /Volumes -maxdepth 5 -name "package.json" -not -path "*/node_modules/*" -type f 2>/dev/null
```

For each project found, describe: name, path, type (Node/Python/Rust/etc), what it does based on its files.

### Step 7: Enumerate Connected MCP Tools

This is critical for Cowork/cloud environments where the real capabilities live in the MCP layer, not the filesystem.

List every MCP server/tool available in this environment:
- Tool name
- What it can do (brief)
- Whether it requires authentication

If you have access to tool listing capabilities, enumerate them. If not, check for MCP config files:

```bash
find ~ -maxdepth 4 -name "mcp*.json" -type f 2>/dev/null
find ~ -maxdepth 4 -name ".mcp*" -type f 2>/dev/null
```

### Step 8: Scan for Running Services

```bash
# Check for running node/python/docker processes
ps aux | grep -E '(node|python|docker|npm|yarn|pnpm)' | grep -v grep | head -20

# Check for docker containers
docker ps 2>/dev/null

# Check for listening ports
lsof -i -P -n | grep LISTEN 2>/dev/null | head -20
```

### Step 9: Scan for Databases

```bash
# Check for local databases
ls ~/Library/Application\ Support/Postgres* 2>/dev/null
ls /usr/local/var/postgres* 2>/dev/null
brew list 2>/dev/null | grep -E '(postgres|mysql|redis|mongo|sqlite)' | head -10

# Check for Supabase config
find ~ -maxdepth 5 -name "supabase" -type d 2>/dev/null | head -5
find ~ -maxdepth 5 -name ".supabase" -type d 2>/dev/null | head -5
```

### Step 10: Check Installed Tools

```bash
# Key development tools
which node npm python3 pip3 docker git gh brew cargo rustc go java ruby ffmpeg jq rg curl wget sqlite3 psql kubectl terraform flyctl vercel 2>/dev/null
node --version 2>/dev/null
python3 --version 2>/dev/null
git --version 2>/dev/null
ruby --version 2>/dev/null
java -version 2>&1 | head -1
ffmpeg -version 2>/dev/null | head -1
jq --version 2>/dev/null
rg --version 2>/dev/null
curl --version 2>/dev/null | head -1
wget --version 2>/dev/null | head -1

# Brew packages (if available)
brew list 2>/dev/null | head -40

# pip packages (if available)
pip3 list 2>/dev/null | head -80

# systemd services (Linux)
systemctl list-units --type=service --state=running 2>/dev/null | head -25
```

### Step 11: Check Scheduled Tasks and Automation

```bash
# crontab
crontab -l 2>/dev/null

# launchd agents (macOS)
ls ~/Library/LaunchAgents/ 2>/dev/null
ls /Library/LaunchAgents/ 2>/dev/null | head -20

# .claude scheduled tasks (already covered in Step 2 but double-check)
find ~ -maxdepth 5 -path "*scheduled-tasks*" -name "SKILL.md" -type f 2>/dev/null
```

## Output Format

Format the content as a single markdown section:

```markdown
## Harvest: [MACHINE_NAME] — [TIMESTAMP]

### Machine Info
- Hostname: ...
- User: ...
- OS: ...

### Skills Found
(list each skill name + one-line description)

### Memory Files
(full content of each memory file, labeled by path)

### CLAUDE.md Files
(full content of each, labeled by path)

### Git Repositories
(for each: path, remotes, recent commits, branches, unpushed commits, status)

### Connected MCP Tools
(every MCP tool available, what it does)

### Credential Keys
(key names only, grouped by file — NEVER values)

### Projects & Applications
(name, path, type, description for each — found ANYWHERE on disk)

### Running Services
(anything currently active)

### Databases
(local databases found)

### Installed Tools
(versions of key tools)

### Settings & Configuration
(contents of settings.json and settings.local.json)

### Scheduled Tasks & Automation
(list with descriptions — crontab, launchd, .claude scheduled tasks)

### Errors During Harvest
(any steps that failed and why)

### Summary
(2-3 sentences describing what this machine IS — persistent Mac vs ephemeral VM vs cloud instance. What's its primary value: local projects? mounted skills? MCP connections? Where does the real persistent state live? This helps the merger skill understand what matters from each harvest.)
```

## After Harvest — MANDATORY AUTO-PUSH TO GITHUB

### Step 1: Clone or locate the repo
```bash
if [ -d "$HOME/ewing-registry/.git" ]; then
  cd "$HOME/ewing-registry" && git pull origin main
elif [ -d "/Users/clawdbot/ewing-registry/.git" ]; then
  cd /Users/clawdbot/ewing-registry && git pull origin main
else
  git clone https://github.com/ewing-operating-system/ewing-registry.git "$HOME/ewing-registry" 2>/dev/null || \
  git clone git@github.com:ewing-operating-system/ewing-registry.git "$HOME/ewing-registry" 2>/dev/null
  cd "$HOME/ewing-registry"
fi
```

### Step 2: Write the harvest file
Save the formatted harvest to `harvests/[machine-name]_[YYYY-MM-DD].md`
```bash
mkdir -p harvests
```

### Step 3: Commit and push
```bash
git add harvests/
git commit -m "Harvest: [MACHINE_NAME] — [TIMESTAMP]

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push origin main
```

### Step 4: If push fails
If git push fails due to auth:
1. Save the harvest file locally at `~/Downloads/harvest_[machine-name]_[date].md`
2. Print the full harvest in chat
3. Tell Ewing: "Harvest saved locally. Push failed — run `cd ~/ewing-registry && git push origin main` from a machine with git credentials."

### Step 5: Confirm
Print exactly one line:
```
Harvest pushed to ewing-registry: harvests/[filename] — https://github.com/ewing-operating-system/ewing-registry
```

Do not explain. Do not summarize. Do not ask questions.

### CRITICAL: Never skip the push. Always attempt git push first. If it fails, always tell Ewing and save locally. The entire point is zero-effort collection.
