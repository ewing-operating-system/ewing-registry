# The Great Consolidation — Supabase Unification Thread

**Date**: 2026-03-23
**Machine**: MacBook (Downloads session)
**Thread Type**: Infrastructure consolidation + research + planning
**Duration**: Extended multi-phase session

---

## What Happened

Ewing opened this thread with a three-part mission: find the debrief/skills/stories repository from past threads, audit every Supabase instance tied to his accounts, and build a master plan to consolidate everything into one shared Supabase that works across all projects, machines, and users.

### Phase 1: Finding the Repository of Knowledge

The thread started by scanning GitHub repos under `ewing-operating-system`. The target was `ewing-command-center` and the `ewing-registry` — the repo where all debrief outputs, skills, stories, harvests, and audits get pushed. The registry was confirmed as the canonical home at `github.com/ewing-operating-system/ewing-registry`.

### Phase 2: Supabase Instance Audit

Four live Supabase instances were discovered across multiple accounts:

1. **rdnnhxhohwjucvjwbwch** (AND Call Command) — The biggest and most active. 14+ core tables. CRM, call intelligence, enrichment. Connected to the Pro plan on the `ewing-operating-systems` org account via GitHub SSO.

2. **ginqabezgxaazkhuuvvw** (ewing-operating-system's Project) — Same GitHub SSO org. Mostly empty or minimal data. Candidate for deletion.

3. **asavljgcnresdnadblse** (OpenClaw Number 1 BDR) — Under a different account (clawdking1@gmail.com). Contained TAM engine tables, OpenClaw outreach pipeline, targets, transcripts, cost tracking. Significant data.

4. **lhmuwrlpcdlzpfthrodm** (ColdCall Universe) — Under yet another account. Subset of CRM data. Overlap with rdnnhxhohwjucvjwbwch.

Plus one dead instance: `iwcvaowfogpffdllqtld`.

### Phase 3: The Consolidation

The thread executed a full data migration:

- **TAM Engine tables** (11 tables) migrated from `asavljgcnresdnadblse` → `rdnnhxhohwjucvjwbwch`
- **OpenClaw/Outreach tables** (15 tables) migrated from `asavljgcnresdnadblse` → `rdnnhxhohwjucvjwbwch`
- **Debrief System tables** (6 tables) created fresh in `rdnnhxhohwjucvjwbwch`: stories, harvests, audits, analysis, skills_registry, registry_docs
- **Registry docs** (11 documents) imported from GitHub registry into Supabase `registry_docs` table

Final state: `rdnnhxhohwjucvjwbwch` now has **68 tables** covering everything — CRM, TAM engine, call intelligence, outreach pipeline, debrief artifacts, and the full skills/registry system.

### Phase 4: Registry Update

The `supabase-instances.md` registry doc was rewritten to reflect the new reality:
- One consolidated instance as single source of truth
- Three decommissioned instances documented with migration status
- Full credentials stored for the surviving instance
- Table categories documented by function

---

## Decisions Made

1. **rdnnhxhohwjucvjwbwch is THE instance** — everything consolidates here
2. **Three instances marked for deletion** — ginqabezgxaazkhuuvvw (empty), lhmuwrlpcdlzpfthrodm (subset), asavljgcnresdnadblse (migrated)
3. **Debrief system lives in Supabase now** — not just GitHub markdown files
4. **Registry docs duplicated into Supabase** — so any ClawdBot on any machine can query the registry via API without needing a git clone

---

## Anti-Patterns Detected

| Tag | Description |
|---|---|
| `#account-sprawl` | 4 Supabase instances across 3 different accounts. Classic fragmentation from rapid prototyping. |
| `#data-duplication` | ColdCall Universe instance had overlapping person/company data with AND Call Command. |
| `#credential-scatter` | Different login methods (GitHub SSO vs email) for different instances made audit harder. |
| `#naming-drift` | Instance names didn't match their actual purpose — "OpenClaw Number 1 BDR" held TAM engine data. |
| `#single-session-migration` | Entire multi-instance consolidation done in one thread — high risk but successful. |

---

## What's Left

- [ ] Actually delete the 3 decommissioned Supabase instances (requires logging into each account)
- [ ] Rename `rdnnhxhohwjucvjwbwch` project from "and-call-command" to "ewing-central" or similar
- [ ] Set up RLS policies on the consolidated instance for multi-user access
- [ ] Create a shared service account or API gateway so all ClawdBots authenticate the same way
- [ ] Verify TAM engine queries still work against the new table locations
- [ ] Build a simple health-check query that validates all 68 tables are present and non-empty
