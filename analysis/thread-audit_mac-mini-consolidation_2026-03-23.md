# Thread Audit: Consolidation Thread
# Machine: ClawdBots-Mac-mini-8.local
# Date: 2026-03-23
# Duration: ~8 hours (9pm Mar 22 - 5am Mar 23 Scottsdale time)

## Thread Metadata
- Machine: ClawdBots-Mac-mini-8.local (macOS 26.3.1, Apple Silicon, 7% disk)
- Session: Claude Code terminal
- Duration: ~8 hours
- Tools used: Bash, Read, Write, Edit, Glob, Grep, Slack MCP (disconnected mid-session), Gmail MCP, Google Drive MCP
- Files created/modified: 25+
- Skills triggered: output-skill, prompt-refiner, harvester, storyteller, skill-creator, keys-and-credentials, data-architect
- Skills NOT triggered: rate-oracle, file-share, mission-control, clawdbot-creator, pec-case-manager, exa-enrichment, salesfinity-loader, recording-collector
- Errors: Slack MCP disconnected twice, Cowork VMs couldn't write to Slack canvas, cron polling for canvas was unnecessary
- Pivots: 4 (Slack canvas → paste-to-chat → GitHub repo, skill file approach → prompt approach for Cowork, single tags → 30-tag taxonomy, static inventory → offense analysis)

## Goal Assessment
- **Stated goal:** Build a harvester to consolidate all projects, threads, learnings, skills, files across all machines
- **Achieved:** Yes, with significant scope expansion
- **Scope changes:** 4 times
  1. Harvester only → harvester + analysis
  2. Slack destination → GitHub destination
  3. Inventory → tagged anti-pattern analysis
  4. Analysis → engineer requirements + debrief system

## Items Created or Modified

### harvester skill
- **Type:** skill
- **Created or Modified:** Modified 3 times (Slack → print → GitHub push)
- **Tags:** 🔧🚫 (started with wrong tool — Slack canvas)
- **Offense:** 🔴 (infrastructure, not deals)
- **What happened:** Built, tested, broke on Cowork, rebuilt for GitHub
- **Recommendation:** Keep — now correctly targets GitHub

### storyteller skill
- **Type:** skill
- **Created:** Yes
- **Tags:** 🟢
- **Offense:** 🟡 (captures institutional knowledge that prevents rework)
- **What happened:** Built to read thread history and produce narrative + audit
- **Recommendation:** Keep — high value for learning from past sessions

### debrief skill
- **Type:** skill
- **Created:** Yes
- **Tags:** 🟢
- **Offense:** 🟡 (prevents data loss between sessions)
- **What happened:** Combined harvester + storyteller + audit into one command
- **Recommendation:** Keep — this is the closer for every significant thread

### data-architect skill
- **Type:** skill
- **Created:** Yes (minimal — needs content)
- **Tags:** 📝
- **Offense:** 🟡
- **Recommendation:** Flesh out with Supabase schema patterns

### ewing-registry GitHub repo
- **Type:** repo
- **Created:** Yes
- **Tags:** 🟢
- **Offense:** 🟡 (single source of truth for all machine state)
- **What happened:** Created on clawdking1-GH. Contains harvests, analysis, stories, registry tables.
- **Recommendation:** Keep — this IS the shared foundation that was missing 🧱

### Slack canvas F0ANYTBD0HW
- **Type:** data store
- **Tags:** 💀🔧🚫 (abandoned, wrong tool, no migration)
- **Offense:** 🔴
- **What happened:** First 3 harvests posted here. Then abandoned when Cowork couldn't write to it. Data left behind initially, later recovered.
- **Recommendation:** Delete or archive — GitHub replaced it

### 30-tag anti-pattern taxonomy
- **Type:** decision/framework
- **Tags:** 🟢
- **Offense:** 🟡
- **What happened:** Evolved from 5 questions → 25 tags → 30 tags as new patterns emerged
- **Recommendation:** Keep — this is the diagnostic language for all future analysis

### engineer-requirements.md
- **Type:** file/specification
- **Tags:** 🟢
- **Offense:** 🟡 (defines what the autonomous engineer must do)
- **What happened:** Derived from all harvests + story + CTO feedback + call data
- **Recommendation:** Keep and update with each new debrief

### gotchas.md
- **Type:** file/library
- **Tags:** 🟢
- **Offense:** 🟡 (prevents rediscovering same bugs)
- **Recommendation:** Keep — every debrief adds to it

### handoff-chain.md
- **Type:** file/living doc
- **Tags:** 🟢
- **Offense:** 🟢 (directly enables continuity)
- **Recommendation:** Keep — every debrief updates it

### call data analysis (1,386 calls)
- **Type:** data analysis
- **Tags:** 🟢
- **Offense:** 🟢 (directly informed Monday priorities)
- **What happened:** Ewing uploaded CSV. Claude analyzed: 7 meetings, 3 referrals, 137 conversations, vertical breakdown.
- **Recommendation:** Automate this — call-ingest-hourly should produce this weekly

### CTO feedback integration
- **Type:** decision
- **Tags:** 🟢
- **Offense:** 🟢
- **What happened:** External CTO said "zero outreach." Call data proved him partially wrong. His framework ("does this help get a signed agreement?") was adopted as the offense filter.
- **Recommendation:** Keep the filter. Discard the "zero outreach" conclusion.

## Handoff Notes

### What's unfinished
1. Registry files (skills.md, credentials.md, etc.) have NOT been updated with the 30-tag analysis — they still contain flat deduplicated data
2. Auto-debrief hook not implemented as a settings.json hook (concept documented but not wired)
3. skill-loader updated on Mac mini but not on MacBook-27 or GREEN
4. Updated harvester/storyteller/debrief skills only on Mac mini — other machines have old versions

### What's broken
- Nothing newly broken. Slack canvas approach was abandoned cleanly.

### What's blocking
- Cowork VMs can't push to GitHub (no git credentials for clawdking1-GH)
- MacBook-27 and GREEN don't have the updated skills yet

### What's next
1. Run debrief in remaining open threads across all machines
2. Install updated skills on MacBook-27 and GREEN
3. Wire the pipeline middle layer (Sheets → Supabase → Salesfinity)
4. Monday offense: 7 meetings, 3 referrals, 26 emails, 17 callbacks

### What to NOT repeat
1. Don't pick a destination (Slack, Supabase, Google Drive) without testing if ALL environments can write to it first
2. Don't create cron jobs to poll for data that hasn't arrived yet — just wait for the human to tell you
3. Don't store structured tabular data as flat markdown when you know it'll need querying later
4. Don't build the analysis framework AFTER collecting data — build it first so data arrives pre-tagged

### Gotchas Discovered This Session
- Slack canvas write (slack_update_canvas) is not available on ANY Cowork VM tested
- Slack MCP disconnects mid-session on Claude Code — unpredictable
- Cron polling wastes context — use it only for genuinely time-sensitive monitoring
- Git credentials on Mac mini use HTTPS with keyring for clawdking1-GH — works locally but Cowork VMs can't authenticate

## What This Thread Should Have Done Differently

1. **Test the destination before building the skill.** We built the entire harvester around Slack canvas, then discovered Cowork VMs can't write to it. A 5-minute test in a Cowork thread would have caught this before any code was written.

2. **Build the tag taxonomy FIRST.** We collected 13 harvests as flat data, then built 30 tags, then had to go back and apply tags to everything retroactively. If tags existed from harvest #1, every harvest would have arrived pre-analyzed.

3. **Don't use cron to poll for human-dependent events.** We set up a cron to check the canvas every 3 minutes for Cowork output. The output depended on Ewing pasting a prompt into a different thread. Cron was the wrong tool — just ask Ewing to tell us when it's done.

4. **Commit to GitHub from the start.** We went Slack → paste → GitHub. Two migrations. Should have gone straight to GitHub after the first Slack failure.

5. **Install the skill on all machines before testing.** We tested the skill trigger in Cowork and it wasn't installed. Predictable failure that wasted a round-trip.
