# Harvest — Supabase Consolidation Session

**Date**: 2026-03-23
**Machine**: MacBook (Downloads)

---

## Credentials Confirmed

| Service | Key | Value |
|---|---|---|
| Supabase (consolidated) | Project URL | https://rdnnhxhohwjucvjwbwch.supabase.co |
| Supabase (consolidated) | Anon Key | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...RlPU |
| Supabase (consolidated) | Service Role | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...MjMTg |
| Supabase (consolidated) | CLI Token | sbp_9e7c8ccca6a0d3c09c50ab3d569da2425e231800 |

## Schema: Consolidated Instance (68 tables)

### Core CRM (11 tables)
persons, phone_numbers, companies, person_scores, linkedin_identifiers, list_assignments, lists, reps, rep_status, rep_phone_numbers, user_settings

### Call Intelligence (4 tables)
call_log, call_analysis, do_not_call, enrichment_log

### TAM Engine (11 tables — migrated from asavljgcnresdnadblse)
tam_businesses, tam_final, tam_verifications, tam_cost_log, tam_cost_per_record, tam_cost_summary, tam_owner_profiles, tam_scrape_runs, tam_awards_sources, tam_enrichments, tam_disagreements

### OpenClaw / Outreach (15 tables — migrated from asavljgcnresdnadblse)
targets, boomerang_targets, outreach_queue, outreach_funnel, dialer_queue, pipeline_log, pipeline_summary, messages, operators, approval_settings, cost_log, daily_costs, transcripts

### Debrief System (6 tables — created fresh)
stories, harvests, audits, analysis, skills_registry, registry_docs

### Other/System (21 tables)
Remaining tables from original AND Call Command instance — includes Supabase system tables, auth tables, and any additional custom tables.

## Decommissioned Instances

| Instance | Account | Action |
|---|---|---|
| asavljgcnresdnadblse | clawdking1@gmail.com | Data migrated. Safe to delete. |
| ginqabezgxaazkhuuvvw | GitHub SSO org | Empty. Safe to delete. |
| lhmuwrlpcdlzpfthrodm | Unknown 3rd account | Subset data. Safe to delete. |
| iwcvaowfogpffdllqtld | Unknown | Already dead. |

## Machine State

- **ewing-registry** cloned at `~/ewing-registry/` (primary) and `~/.claude/repos/ewing-registry/` (secondary)
- **37 skills** installed in `~/.claude/skills/`
- **1 scheduled task**: downloads-cleaner
- **Git config**: ewing-operating-system / noreply@github.com
- **SSH key**: ~/.ssh/id_ed25519 (configured)

## Open Items for Next Thread

1. Delete 3 decommissioned Supabase instances
2. Rename consolidated instance to "ewing-central"
3. Set up RLS policies for multi-user/multi-bot access
4. Verify TAM engine queries work on new location
5. Build health-check query for all 68 tables
6. Consider creating a shared API gateway for ClawdBot auth
