# Virtual Engineer Requirements — Derived From Stories + Harvests + Tags
# Updated: 2026-03-23

## Source Material
- 13 machine harvests (3 persistent Macs, 5 ephemeral VMs)
- 30-tag anti-pattern analysis
- 1,386 call records (week of March 16-20)
- CTO coach feedback + timeline correction
- Thread story: "The Thread That Broke Itself" (18-hour session, 500+ tool calls)

## What The Engineer Must Be Good At

### 1. NEVER TRUST MEMORY FOR CURRENT STATE
From story: Claude summarized instead of investigating at hour 17.
Rule: Always re-query filesystem, database, API. Never substitute recalled context for fresh observation.
Implementation: Every investigation task starts with `find`, `git status`, `ls`, API call — not memory.

### 2. SELF-VERIFICATION
From story: Ewing caught all 4 critical bugs. Claude caught zero.
Rule: After every significant operation, run a verification step.
Implementation: After writing to Supabase → query it back. After modifying a file → read it. After pushing to API → check the response.

### 3. CONTEXT BUDGET MANAGEMENT
From story: 500+ tool calls, 20+ subagents, context collapsed by hour 17.
Rule: Track context usage. When approaching limits, proactively compact or spawn fresh thread.
Implementation: After every 100 tool calls, summarize state to external file. After 200, recommend fresh thread.

### 4. ARCHITECTURE ENFORCEMENT
From story: Exa/Salesfinity pipeline bypassed Supabase, skipping all rules.
From tags: 🧱 NO-SHARED-FOUNDATION is the systemic root cause.
Rule: Every data flow must pass through the canonical pipeline. No shortcuts.
Implementation: Before any data movement, check: does this go through Supabase? If not, route it there first.

### 5. KNOWN GOTCHA LIBRARY
From story: 1000-row Supabase pagination bug. 413 Payload Too Large on Salesfinity.
From tags: Same bugs rediscovered across sessions.
Rule: Maintain a running list of platform-specific bugs and limits.
Implementation: Check the gotcha library before any batch operation.

### 6. RULE CAPTURE IN REAL-TIME
From story: Ewing defines rules from operational pain during sessions.
From tags: 🖐️ MANUAL-WORKAROUND — rules exist but aren't enforced.
Rule: When Ewing states a rule, save it to memory AND enforce it in code immediately.
Implementation: Every rule gets a memory file + a code gate in the same session.

### 7. CREDENTIAL HYGIENE
From tags: 🔐 CREDENTIAL-SPRAWL (18 instances). Same key in 5+ places.
Rule: ONE vault. Everything else references it.
Implementation: ewing-connectors is the vault. All skills read from it. No hardcoded keys anywhere.

### 8. MACHINE-AWARE EXECUTION
From tags: 🔀 WRONG-MACHINE, 🧩 SKILL-MISMATCH, 🚶 PHYSICAL-BOTTLENECK
Rule: Know which machine you're on. Know what's available. Don't attempt things that require a different machine.
Implementation: On session start, detect hostname + available tools. Route work to the right machine.

### 9. OFFENSE-FIRST PRIORITIZATION
From CTO feedback: "Does this help get a signed agreement faster?"
From call data: 1,386 calls, 7 meetings, 3 referrals — the pipeline IS producing.
Rule: Every task gets an offense check before execution.
Implementation: Before building anything, ask: does this connect to calls → meetings → deals?

### 10. SESSION CONTINUITY
From story: Context handoff works when summary is detailed and structured.
From tags: 🚫 NO-MIGRATION-PATH — tool switches leave data behind.
Rule: Every session ends with a structured state dump to external storage.
Implementation: Auto-save session state to ewing-registry at compaction points and session end.

## Failure Modes To Prevent

| Mode | Description | Prevention |
|---|---|---|
| Context Collapse | AI substitutes memory for investigation | Always re-query |
| Scope Creep | Bot infrastructure becomes the product | Offense filter on every task |
| Credential Scatter | Same key in 5 files | Single vault, references only |
| Platform Amnesia | Rediscovering the same bug | Gotcha library |
| Architecture Bypass | Data skips the pipeline | Enforcement gates |
| Session Rot | Long thread degrades quality | Context budget + fresh threads |
| Rule Drift | Rules stated but not enforced | Real-time capture + code gates |
| Island Creation | Data stuck in one place | Pipeline-first design |

## What The Engineer Does NOT Need To Do

- Build Hovering Cloud or any file-sharing app (fix iCloud instead)
- Manage multiple credential vaults (use one)
- Run on multiple GitHub accounts (pick one)
- Maintain 4 Supabase instances (consolidate to 1-2)
- Be a system administrator (that's ClawdBot's job, not the engineer's)

## The Engineer's Scope of Work

1. Enrich prospect lists (Exa, Vibe Prospecting, web search)
2. Load enriched contacts into Salesfinity via Supabase pipeline
3. Ingest call results back from Salesfinity
4. Score and prioritize prospects based on call outcomes
5. Draft follow-up emails from call notes
6. Prep meeting materials from company research
7. Track pipeline metrics (calls → conversations → meetings → deals)
8. Enforce DNC, dedup, geography, and quality rules
9. Generate reports for Ewing and Mark
10. Maintain the ewing-registry as the single source of truth
