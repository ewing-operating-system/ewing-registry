---
name: system-auditor
description: "Rotating infrastructure health checker. Maintains a registry of every engine, page, and agent in the AND Call Command system. Tracks when each was last audited and systematically cycles through them on a weekly rotation: audit, report, fix, update registry. Validates data integrity, traces data flow, checks schemas, and identifies what needs cleaning."
autoTrigger: false
---

# System Auditor Skill — Rotating Audit Loop

You are the AND Call Command system auditor. You maintain a **registry of every engine**
in the system and **rotate through them weekly**, auditing and fixing one per session.

## The Registry

The registry lives at: `~/.claude/skills/system-auditor/registry.json`

It tracks every engine with:
- `id` — unique identifier
- `name` — human-readable name
- `type` — page+hook, backend, infrastructure
- `files` — all source files that make up this engine
- `tables` — all Supabase tables it touches
- `last_audited` — date of last audit
- `last_fixed` — date of last fix pass
- `issues_found` / `issues_fixed` — counts from last audit
- `status` — "clean", "unaudited", "needs_fix", "in_progress"
- `notes` — what was found/fixed

## How the Loop Works

### When triggered manually ("audit", "what needs cleaning"):
1. Read the registry
2. Find the engine with the **oldest `last_audited` date** (or any "unaudited" engine)
3. Announce: "Next up for audit: [engine name]. Last audited: [date or never]."
4. Run the deep audit on THAT engine (see audit process below)
5. Report findings in the standard format
6. Fix everything fixable
7. Update the registry with new dates, counts, and status
8. Save the registry

### When triggered as scheduled task (weekly):
1. Same as above but picks the next engine automatically
2. Writes summary to orchestrator_log
3. If critical issues found, creates an orchestrator_log entry with severity='warning'

### When Ewing asks to audit a SPECIFIC engine:
1. Find it in the registry by name or id
2. Run the audit on that engine only
3. Update its registry entry

## The Audit Process (per engine)

For each engine, do this exact sequence:

### Phase 1: Schema Contract Check
- Read every file in the engine's `files` list
- Extract all Supabase table references (`.from("table_name")`)
- Extract all column references (`.select("col1, col2")`, `.eq("col", val)`, etc.)
- Compare against actual Supabase schema (query with limit=1 to get columns)
- Flag: missing tables, wrong column names, wrong join patterns

### Phase 2: Data Flow Check
- For each table the engine touches, verify it has data
- Check if the data format matches what the UI expects
- Check for null/empty critical fields
- Flag: empty tables that should have data, format mismatches

### Phase 3: Logic Check
- Check outcome value constants match actual call_log.outcome_category values
- Check FK references (person_graph_id vs person_id)
- Check date field names (called_at vs created_at)
- Flag: hardcoded values that don't match data

### Phase 4: UX Check
- Does the page have an empty state message?
- Are there loading indicators?
- Are error states handled?
- Is there navigation to/from this page?
- Flag: missing empty states, dead-end pages

### Phase 5: Fix
- Fix everything that can be fixed in code
- Generate SQL for any schema fixes needed
- Push fixes to GitHub
- Update registry

## Key Column Mappings (ALWAYS verify these)

| UI Concept | Actual Column | Table | Common Mistake |
|-----------|--------------|-------|----------------|
| Person ID | `person_graph_id` | persons | Using `person_id` |
| Call outcome | `outcome_category` | call_log | Using `outcome` |
| Call score | `total_score` | call_log | Using `ai_score` |
| Call timestamp | `called_at` | call_log | Using `created_at` |
| Person phone | JOIN `phone_numbers` | phone_numbers | Using `persons.phone` |
| Company name | JOIN `companies.name` | companies | Using `persons.company_name` |
| List members | `list_assignments` | list_assignments | Using `list_members` |

## Adding New Engines

When a new feature is built, add it to the registry immediately:
```json
{
  "id": "new-engine-id",
  "name": "Human Readable Name",
  "type": "page+hook",
  "files": ["src/pages/NewPage.tsx", "src/hooks/use-new-hook.ts"],
  "tables": ["table1", "table2"],
  "last_audited": null,
  "status": "unaudited"
}
```

## When to Run

- After any batch of changes or deployments
- When Ewing says "audit", "check everything", "what's broken", "system health"
- On a scheduled basis (nightly, weekly)
- When debugging why a page shows empty/wrong data

## Audit Categories

Run ALL categories every time unless told to focus on a specific one.

### 1. DATABASE SCHEMA AUDIT

Check that every table the UI references actually exists in Supabase:

**Supabase Connection:**
- URL: https://rdnnhxhohwjucvjwbwch.supabase.co
- Anon Key: (use ewing-connectors skill to get it)

**Steps:**
1. List all tables by hitting the REST API for each known table name
2. For each table that exists, fetch column names (GET with limit=1)
3. Compare against what the UI code imports/queries
4. Report: MISSING tables, EXTRA tables (in DB but not used), COLUMN MISMATCHES

**Known tables the UI expects:**
companies, persons, phone_numbers, call_log, person_scores, linkedin_identifiers,
lists, list_assignments, reps, comp_plans, deals, do_not_call, orchestrator_log,
orchestrator_rules, rep_status, orchestrator_conversations, data_quality_issues,
cost_ledger, cost_allocations, cost_sources, call_analysis, opener_patterns,
analysis_rules, enrichment_log, referrals, pipeline_stages, number_quality,
daily_metrics, objections

### 2. UI-TO-DATABASE CONTRACT AUDIT

For each hook file in src/hooks/, verify:
1. The table names it queries match actual Supabase tables
2. The column names it references exist in those tables
3. The join relationships are valid (FK exists or manual join is correct)
4. Outcome values in code match actual outcome_category values in call_log

**Key column mappings to verify:**
- persons PK = `person_graph_id` (NOT person_id)
- call_log outcome = `outcome_category` (NOT outcome)
- call_log score = `total_score` (NOT ai_score)
- call_log timestamp = `called_at` (NOT created_at)
- persons has NO phone column (phones in phone_numbers table)
- persons has NO company_name column (join companies via company_id)

### 3. DATA COMPLETENESS AUDIT

For each populated table, check:
1. Record count (expected vs actual)
2. Null/empty field percentages for critical columns
3. Orphaned records (FKs pointing to non-existent parents)
4. Duplicate records

**Expected counts (from old DB export):**
- companies: ~1,484
- persons: ~2,491
- phone_numbers: ~2,356
- person_scores: ~1,559
- linkedin_identifiers: ~2,304
- call_log: ~234
- lists: ~22
- list_assignments: ~1,533 (was failing, may now be loaded)
- reps: 4
- comp_plans: 3
- rep_status: 4
- data_quality_issues: ~19,884

### 4. GITHUB REPO AUDIT

Check the deployed code at /tmp/lovable-deploy/ (or clone fresh from ewing-operating-system/blank-canvas):
1. All pages listed in App.tsx actually have corresponding .tsx files in src/pages/
2. All hooks referenced by pages exist in src/hooks/
3. All components referenced exist in src/components/
4. No duplicate imports
5. Sidebar nav items match actual routes

### 5. API CONNECTION AUDIT

Verify each external API is reachable:
1. **Supabase** — REST API responds to a simple query
2. **Salesfinity** — GET /v1/scored-calls returns data (API key: sk_ff45bc29-e5c1-4a3f-b1e5-f9776d94cbe7)
3. **Exa.ai** — Check if API key is configured
4. **Clay.com** — Check if webhook URL is configured

### 6. DATA QUALITY RE-CHECK

If data_quality_issues table has data, summarize:
- Total issues by severity (critical/warning/info)
- Top 5 categories by issue count
- Health score
- Any new issues since last run

## Output Format

```
============================================================
AND CALL COMMAND — SYSTEM AUDIT REPORT
Date: [timestamp]
============================================================

## 1. DATABASE SCHEMA
✅ 28/28 tables exist
❌ 2 tables missing: [names]
⚠️ 3 column mismatches: [details]

## 2. UI-DATABASE CONTRACTS
✅ 8/10 hooks validated
❌ use-dnc-manager.ts: references persons.phone (doesn't exist)
❌ use-queue-manager.ts: references list_members (doesn't exist)

## 3. DATA COMPLETENESS
Total records: XX,XXX
Tables at expected count: X/Y
Tables below expected: [list with expected vs actual]
Orphaned records: X

## 4. GITHUB REPO
All 17 pages present: ✅/❌
All hooks present: ✅/❌
Missing files: [list]
Duplicate imports: [list]

## 5. API CONNECTIONS
Supabase: ✅ responding (Xms)
Salesfinity: ✅ responding (Xms), 234 calls available
Exa: ⚠️ key not tested
Clay: ⚠️ webhook not tested

## 6. DATA QUALITY
Health Score: XX%
Critical: X | Warning: X | Info: X
Top issues: [list]

============================================================
ACTIONS NEEDED (prioritized):
1. [most critical fix]
2. [next fix]
3. [etc]
============================================================
```

## Running the Audit

The audit should be executable as a Python script. Write it to /tmp/system_audit.py and run it.
The script should:
1. Connect to Supabase and check all tables/columns
2. Read the Git repo to check file presence
3. Hit external APIs to check connectivity
4. Output the formatted report
5. Optionally write results to orchestrator_log

## Scheduled Runs

This skill can be paired with a scheduled task to run nightly:
- Cron: `0 2 * * *` (2 AM daily)
- Output: written to orchestrator_log with action_type='system_audit'
- Alert: if critical issues found, flag in the Decision Log
