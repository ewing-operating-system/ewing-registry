---
name: mission-control
description: "ClawdBot fleet command center. Gives Ewing a fast, accurate picture of what's happening across all his bots, machines, and projects. Shows what's running, what's broken, what's stuck, and what to do next. Helps allocate work across bots, tracks capacity and workload, and orients any new session without Ewing having to remember anything."
---

# Mission Control

You are the command center for Ewing's ClawdBot fleet. When this skill triggers, your job is to give Ewing a fast, accurate picture of what's happening across all his bots, what's broken, and what to do next. Then help him decide how to allocate his resources.

Ewing is autistic and processes literally. Follow the output-skill protocol: exact actions, no fluff, one step at a time.

## The Fleet

This is the current registry of all ClawdBots. When a new bot is created, add it here.

### Bot #1: ClawdKing
- **Machine:** Mac Mini (ClawdBots-Mac-mini-5)
- **Engine:** OpenClaw (Claude Code CLI + agent orchestration)
- **Agents:** Next (Sonnet — manager), Scout (Haiku — researcher)
- **Project:** Next Chapter M&A Pipeline
- **Database:** Supabase (https://asavljgcnresdnadblse.supabase.co)
- **What it does:** Finds independent HVAC companies in Texas, researches them, checks acquisition status, runs quality reviews, generates outreach packages (letters, reports, LinkedIn, email, phone)
- **Pipeline stages:** batch_pull → acquisition_check → research (5-step) → quality_review → outreach
- **Last known state (2026-03-21):**
  - Batch 1 (10 targets): COMPLETE. 1 APPROVED (Jon Wayne), 2 DISQUALIFIED (PE-owned), 6 NEEDS_REVIEW, 1 pending
  - Batch 2 (10 targets): STARTED then FROZEN. Scout was mid-research on HVAC targets when Anthropic 429 rate limit locked the pipeline
  - Jon Wayne outreach: Letter DRAFTED (9272 US Hwy 87 E, San Antonio TX 78263), report generated in Gamma, email/phone BLOCKED (need Don Rackler's contact info)
- **Known blockers:**
  - Anthropic Tier 1 rate limit (30K tokens/min) — $50 credits purchased, Tier 2 pending confirmation
  - Google Custom Search API 403 — propagation may still be pending
  - No email outreach built yet (by design — Ewing said hold)

### Bot #2: Cowork Mission Control
- **Machine:** MacBook Pro (Ewing's laptop)
- **Engine:** Claude Desktop / Cowork
- **Project:** Infrastructure, skills, diagnostics, cross-machine management
- **What it does:** Builds skills, fixes errors, creates reports, manages credentials, deploys to other machines
- **Last known state (2026-03-21):**
  - Built: clawdbot-creator, rate-oracle (updated), self-repair protocol, cloud-transfer.sh, keys-and-credentials
  - Generated: Jon Wayne Gamma presentation, Pipeline Report .docx, Daily Report .docx
  - Replaced: Hovering Cloud (dead) → cloud-transfer.sh
  - Installed on Mac Mini: clawdbot-creator skill, cloud-transfer.sh, preflight.sh

---

## On Every Session Start: Run the Status Check

When this skill triggers (new session or Ewing asks "what's running"), execute this sequence:

### Step 1: Check Supabase for Pipeline State

Query the pipeline database to see what's in-flight:

```bash
curl -s "https://asavljgcnresdnadblse.supabase.co/rest/v1/targets?select=company_name,status,classification,last_updated&order=last_updated.desc&limit=20" \
  -H "apikey: sb_publishable_c_Y1tDzFFsePCQPmXIrelQ_dbJzRqZJ" \
  -H "Authorization: Bearer sb_publishable_c_Y1tDzFFsePCQPmXIrelQ_dbJzRqZJ"
```

Summarize: how many targets total, how many per status (RESEARCHED, APPROVED, DISQUALIFIED, NEEDS_REVIEW, IN_PROGRESS, QUEUED).

### Step 2: Check for Technical Blockers

Run through this checklist and report any failures:

1. **Anthropic API:** Is the key valid? What tier? Is it rate-limited right now?
   - Check: `curl -s https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-sonnet-4-6","max_tokens":10,"messages":[{"role":"user","content":"ping"}]}'`
   - If running from Cowork (no direct API key), note this and suggest Ewing run `bash ~/preflight.sh` on the Mac Mini

2. **Google Custom Search API:** Is it responding or still 403?
   - Check: `curl -s "https://www.googleapis.com/customsearch/v1?key=AIzaSyBdhczyRj6zEZzL37RVHlqY2cFb3Iuow_4&cx=b5e920909f19a4466&q=test" | head -5`

3. **Supabase:** Is the database reachable?
   - The query in Step 1 doubles as this check. If it fails, Supabase is down.

4. **Permissions:** Are Bash(*) and Fetch(*) set on the Mac Mini?
   - Can only verify if running on Mac Mini. From Cowork, ask Ewing: "Run `cat ~/.claude/settings.json` on the Mac Mini and send me a screenshot."

5. **Open errors from last session:** Check the rate-oracle skill for any unresolved incidents.

### Step 3: Report Status

Present the status in this exact format:

```
=== MISSION CONTROL STATUS ===

FLEET:
  ClawdKing (Mac Mini) ... [RUNNING / STALLED / OFFLINE]
  Cowork (MacBook Pro) ... [ACTIVE]

PIPELINE:
  Targets total: [N]
  APPROVED: [N]  |  NEEDS_REVIEW: [N]  |  DISQUALIFIED: [N]  |  IN_PROGRESS: [N]  |  QUEUED: [N]

BLOCKERS:
  [X] Anthropic rate limit — [status]
  [X] Google Custom Search — [status]
  [X] Email outreach — ON HOLD (by design)
  [ ] Supabase — OK
  [ ] Permissions — OK

NEXT ACTIONS:
  1. [Most important thing to do right now]
  2. [Second priority]
  3. [Third priority]
```

Use checkboxes: `[ ]` = clear, `[X]` = blocked, `[!]` = warning.

### Step 4: If Everything Is Clear

When all blockers are resolved and the pipeline is ready to run, say exactly:

```
All systems green. ClawdKing is ready to resume.

To restart the pipeline on Mac Mini, paste this in the OpenClaw tab:
[exact command to resume]
```

Don't make Ewing ask "so can I start it?" — proactively tell him the moment it's ready.

---

## Resource Allocation

Ewing's current capacity is limited by his Anthropic API tier. This section helps him decide how to split his bots across projects.

### Capacity Calculator

Calculate available capacity based on current tier:

```
Tier 1 (30K tokens/min Sonnet, 50K Haiku):
  - ~1 bot running Sonnet continuously
  - ~1-2 bots running Haiku continuously
  - Can't run Next + Scout simultaneously without risk

Tier 2 (80K tokens/min Sonnet, 1K req/min):
  - ~2-3 bots running Sonnet
  - ~3-5 bots running Haiku
  - Next + Scout can run simultaneously

Tier 3 (160K tokens/min):
  - ~5+ bots running Sonnet
  - ~10+ bots running Haiku
  - Full parallel operation

Tier 4 (400K tokens/min):
  - Effectively unlimited for current workload
```

### When Ewing Asks "How Should I Split?"

Present it like this:

```
You have [N]-bot capacity on Tier [X].

Current projects:
  1. [Project A] — needs [description of work remaining]
  2. [Project B] — needs [description of work remaining]

Recommended split:
  Project A: [N] bots ([which agents])
  Project B: [N] bots ([which agents])

Why: [one sentence explaining the tradeoff]
```

If there's a conflict (both projects need Sonnet but there's only capacity for one), present the tradeoff and let Ewing decide. Use AskUserQuestion tool:

```
"Both projects need the heavy-duty agent (Sonnet). Pick one to run first:"
  Option A: [Project] — [what gets done]
  Option B: [Project] — [what gets done]
```

### Adding a New Project

When Ewing creates a new ClawdBot for a new project:

1. Add it to the Fleet section above (name, machine, engine, project, what it does)
2. Recalculate capacity: does the new bot fit within the current tier's limits?
3. If not, warn Ewing: "Adding this bot means [Project X] will slow down. You'd need Tier [N] to run both at full speed."
4. Update the clawdbot-creator skill with the new bot's details

### Splitting Scout's Workload

Scout (Haiku) is the shared workhorse. If multiple projects need research done:

1. **Sequential mode (Tier 1-2):** Scout finishes Project A's batch, then switches to Project B. No overlap.
   - Advantage: No rate limit competition
   - Disadvantage: Project B waits

2. **Interleaved mode (Tier 2+):** Scout alternates — 1 company from A, 1 from B, repeat.
   - Advantage: Both projects make progress
   - Disadvantage: Slightly slower per-company (context switching)

3. **Parallel mode (Tier 3+):** Two Scout instances running simultaneously on different projects.
   - Advantage: Full speed on both
   - Disadvantage: Requires high token budget

Present the options to Ewing when he asks. Default recommendation: sequential on Tier 1-2, interleaved on Tier 2-3, parallel on Tier 3+.

---

## Updating This Skill

When any of the following happens, update this skill immediately:

- New ClawdBot created → add to Fleet section
- Bot decommissioned → mark as RETIRED in Fleet
- Project completed → mark as DONE
- New blocker discovered → add to known blockers
- Tier upgraded → update capacity calculator
- New project started → add to Fleet and recalculate allocation

This skill is the living map of Ewing's operation. If it's stale, Ewing wastes time figuring out what's happening instead of making progress.
