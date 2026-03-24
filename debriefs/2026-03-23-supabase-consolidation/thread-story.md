# Thread Story: The Great Supabase Consolidation

**Date**: 2026-03-23 → 2026-03-24
**Machine**: MacBook-GREEN
**Thread Type**: Infrastructure consolidation + data migration + debrief
**Trigger**: Ewing asked to find the debrief repository and consolidate all Supabase instances

---

## Act 1: The Search

Ewing opened the thread with a triple mission: find the repository of skills, stories, and debrief outputs; audit every Supabase instance connected to his accounts; and build a master plan to consolidate everything into a single shared database.

The search started at GitHub. The `ewing-operating-system` org was scanned. `ewing-command-center` was identified, but the real prize was `ewing-registry` — the canonical home for all debrief artifacts, skills, and operational intelligence.

## Act 2: The Supabase Audit

Using Claude Chrome, the thread navigated into Supabase dashboards and audited every instance across multiple accounts:

1. **rdnnhxhohwjucvjwbwch** (AND Call Command) — The biggest. 14+ CRM tables, call intelligence, enrichment. Pro plan, ewing-operating-systems org.
2. **ginqabezgxaazkhuuvvw** — Same org, mostly empty. Candidate for deletion.
3. **asavljgcnresdnadblse** (OpenClaw Number 1 BDR) — Different account (clawdking1@gmail.com). TAM engine + OpenClaw outreach pipeline. Significant data.
4. **lhmuwrlpcdlzpfthrodm** (ColdCall Universe) — Third account. Subset of CRM data.
5. **iwcvaowfogpffdllqtld** (debugger-tool) — Dead.

The pattern was clear: account sprawl from rapid prototyping. Four live instances across three accounts, with overlapping data and no single source of truth.

## Act 3: The Migration

The thread executed a full consolidation into `rdnnhxhohwjucvjwbwch`:

- **11 TAM Engine tables** migrated from asavljgcnresdnadblse
- **15 OpenClaw/Outreach tables** migrated from asavljgcnresdnadblse
- **6 Debrief System tables** created fresh (stories, harvests, audits, analysis, skills_registry, registry_docs)
- **11 registry documents** imported from GitHub into Supabase

Final count: **68 tables** in one instance. Three instances marked for deletion.

## Act 4: The Documentation

The registry was updated. `supabase-instances.md` was rewritten with the new consolidated reality. A full debrief was produced (story + audit + harvest) and pushed to GitHub.

## Act 5: The Harvest and Story

The thread closed with a full machine harvest of MacBook-GREEN: 36 skills, 11 memory files, 10 git repos, 10 MCP connections. Everything documented and pushed to ewing-registry.

---

## Anti-Pattern Audit (30-Tag Taxonomy)

| # | Tag | Severity | Description |
|---|---|---|---|
| 1 | `#account-sprawl` | HIGH | 4 Supabase instances across 3 different login accounts. Classic fragmentation from rapid prototyping without a consolidation plan. |
| 2 | `#data-duplication` | HIGH | ColdCall Universe and AND Call Command had overlapping person/company data. No dedup strategy existed. |
| 3 | `#credential-scatter` | HIGH | Different auth methods (GitHub SSO, email login) for different instances. Google Drive repos embed PAT tokens in remote URLs. |
| 4 | `#naming-drift` | MEDIUM | Instance names didn't match actual purpose — "OpenClaw Number 1 BDR" held TAM engine data. "AND Call Command" is now the universal store. |
| 5 | `#single-session-migration` | MEDIUM | Entire multi-instance consolidation done in one thread. High risk, no rollback plan, but source instances preserved. |
| 6 | `#repo-duplication` | MEDIUM | `and-call-command-pipeline` cloned in both `~/.claude/repos/` and `~/Documents/`. `ewing-registry` cloned in both `~/` and `~/.claude/repos/` and `/tmp/`. |
| 7 | `#disk-pressure` | MEDIUM | 90% disk usage (797GB of 926GB). Google Drive sync likely consuming significant space. |
| 8 | `#pat-in-remote` | HIGH | GitHub PAT token embedded in git remote URLs for Google Drive repos. Should be SSH. |
| 9 | `#no-rls` | MEDIUM | Consolidated Supabase has no Row Level Security policies. Multi-user access is wide open. |
| 10 | `#orphan-repos` | LOW | `overwatch` repo is empty. `hovering-cloud` is under `clawdking1-GH` not `ewing-operating-system`. |
| 11 | `#no-backup-strategy` | MEDIUM | 68-table Supabase has no documented backup/export strategy. |
| 12 | `#mixed-auth-accounts` | MEDIUM | ewing-operating-system (SSH), clawdking1-GH (HTTPS), and Google Drive PAT — three different GitHub auth patterns on one machine. |
| 13 | `#stale-branch` | LOW | coldcall-universe has `v2-overnight-build` branch with untracked files. |
| 14 | `#no-health-check` | MEDIUM | No automated validation that all 68 tables exist and are queryable. |
| 15 | `#service-role-in-registry` | HIGH | Supabase service role key stored in plain text in ewing-registry/registry/supabase-instances.md. Should be in vault skill only. |

## Patterns That Worked Well

| Pattern | Description |
|---|---|
| `+registry-as-truth` | Using ewing-registry as the single canonical source for all operational intelligence — skills, debriefs, harvests, registry docs. |
| `+debrief-on-close` | Running debrief at end of every significant thread captures knowledge that would otherwise be lost. |
| `+supabase-as-store` | Duplicating registry docs into Supabase means any ClawdBot can query via API without needing git. |
| `+skill-system` | 36 skills covering the full operational surface — from sales to legal to infrastructure. |
| `+mcp-integration` | 10 MCP services connected gives comprehensive access to email, calendar, Slack, Drive, browser. |

---

## Open Items

1. Delete 3 decommissioned Supabase instances
2. Rename consolidated instance to "ewing-central"
3. Set up RLS policies for multi-user access
4. Rotate GitHub PAT in Google Drive repos, switch to SSH
5. Build health-check query for all 68 tables
6. Move service role key out of registry docs into vault only
7. Deduplicate repo clones (and-call-command-pipeline, ewing-registry)
8. Free disk space (90% used)
9. Address empty overwatch repo — build or delete
