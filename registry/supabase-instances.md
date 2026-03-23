# Supabase Instances

## Consolidated Instance (Single Source of Truth)

| Field | Value |
|---|---|
| **Instance ID** | `rdnnhxhohwjucvjwbwch` |
| **Project Name** | and-call-command (rename to ewing-central pending) |
| **Account** | ewing-operating-systems Org (GitHub SSO, ewing@chapter.guide) |
| **Region** | AWS us-west-2 |
| **Plan** | Pro (Micro) |
| **Tables** | 68 |
| **Purpose** | ALL Ewing data — CRM, TAM engine, call intelligence, dialer, enrichment, transcripts, debrief artifacts, skills registry |

## Table Categories

### Core CRM
persons, phone_numbers, companies, person_scores, linkedin_identifiers, list_assignments, lists, reps, rep_status, rep_phone_numbers, user_settings

### Call Intelligence
call_log, call_analysis, do_not_call, enrichment_log

### TAM Engine (migrated from asavljgcnresdnadblse 2026-03-23)
tam_businesses, tam_final, tam_verifications, tam_cost_log, tam_cost_per_record, tam_cost_summary, tam_owner_profiles, tam_scrape_runs, tam_awards_sources, tam_enrichments, tam_disagreements

### OpenClaw / Outreach (migrated from asavljgcnresdnadblse 2026-03-23)
targets, boomerang_targets, outreach_queue, outreach_funnel, dialer_queue, pipeline_log, pipeline_summary, messages, operators, approval_settings, cost_log, daily_costs, transcripts

### Debrief System (created 2026-03-23)
stories, harvests, audits, analysis, skills_registry, registry_docs

## Decommissioned Instances

| Instance ID | Former Name | Account | Status |
|---|---|---|---|
| `asavljgcnresdnadblse` | OpenClaw Number 1 BDR | clawdking1@gmail.com | DATA MIGRATED 2026-03-23 |
| `ginqabezgxaazkhuuvvw` | ewing-operating-system's Project | GitHub SSO | EMPTY — delete |
| `lhmuwrlpcdlzpfthrodm` | ColdCall Universe | Unknown 3rd account | SUBSET — safe to delete |
| `iwcvaowfogpffdllqtld` | debugger-tool (old) | Unknown | DEAD |

## Credentials

| Key | Value |
|---|---|
| Project URL | `https://rdnnhxhohwjucvjwbwch.supabase.co` |
| Anon Key | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkbm5oeGhvaHdqdWN2andid2NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM4NzI3MzYsImV4cCI6MjA4OTQ0ODczNn0.SZJlQgqtAtdF11CDGofgkF-tz_2W2bCQx3q4hpGRlPU` |
| Service Role Key | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkbm5oeGhvaHdqdWN2andid2NoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Mzg3MjczNiwiZXhwIjoyMDg5NDQ4NzM2fQ.DmdDVTmMOSXIfgvv9j42KiCQgkoiQ1TiiZEcX0CjMTg` |
| CLI Token | `sbp_9e7c8ccca6a0d3c09c50ab3d569da2425e231800` |
