## Thread Audit: AND Call Command Mega-Build — 2026-03-23

### Thread Metadata
- Thread ID: b21ba1e2-373e-4af0-a633-c3d4bed79f13
- Machine: MacBook-27.local
- Duration: ~5 days (2026-03-18 20:52 UTC through 2026-03-23 19:50 UTC), with ~18 hours of active human-AI interaction spread across multiple work sessions
- Total JSONL lines: 13,485 (56 MB transcript)
- Tool calls: 3,679
- Subagents spawned: 247
- Files created/modified: 322 unique file paths
- User messages: 4,266 (many empty/image-only; ~200+ substantive instructions)
- Context compactions: 21 (first at 22:24 UTC Mar 18, last at 09:32 UTC Mar 23)
- Skills triggered: prompt-refiner (35x), ewing-connectors (3x), system-auditor (2x), skill-creator (2x), docx (2x), tech-translator, skill-loader, salesfinity-loader, output-skill, harvester, debrief, cold-call-workflow, anthropic-skills:ui-touchup, anthropic-skills:docx
- Scheduled tasks created: 8 (nightly-system-audit, priority-rebuild, queue-autocheck, call-sync, company-valuation-backfill, call-ingest-hourly, daily-maintenance, dnc-salesfinity-sync)
- Errors encountered: 169 total
  - File-modified-since-read race conditions
  - /tmp directory reference errors (Lovable deploy path didn't exist)
  - TaskOutput ID-not-found (stale subagent references after compaction)
  - Slack MCP tool availability errors
  - Edit ambiguity (multiple matches without replace_all)
  - Agent parameter validation failures
- Pivots: 12+ (strategic pivot to placement agents, commission-first display, entity P&L split, DNC overhaul, call intelligence layer, 1000-row pagination fix, context graph design principle, Lovable project restart, model switch to Haiku then back to Opus, harvester re-execution)
- Context health: Severely degraded by end. 21 compactions in 5 days. The final harvester failure (Act 9 in the story) is direct evidence of context collapse. Subagent task IDs became unreachable. The session switched to Haiku at one point to conserve context. Quality was strong through hours 0-12, noticeably degraded after hour 14, and unreliable by hour 17+.

### Goal Assessment
- Stated goal: "Take the best of each application that I built, focus in on the functions, features, and linkages between systems especially, and help me unify these various parts into a single amazing application that helps us do all of our cold calling, followup, blueprinting contacts, creating, managing, and sending artifacts."
- Achieved: Partially. The unified Lovable application was built with 40+ pages, 50+ hooks, database migrations, Salesfinity API integration, DNC system, call analysis, coaching, pipeline tracking, entity attribution, and scheduled automation. However, the Lovable deployment had repeated connection issues, some enrichment data was never backfilled, and the harvester skill failed on first attempt due to context exhaustion.
- Scope changes: 12+ major scope expansions. The original goal was a unification of 3 existing projects. It grew to include: placement agent pivot strategy, cost tracking agent, call orchestrator, data cleaner, phone intelligence layer, entity P&L split, commission-first redesign, DNC hierarchy with transcript evidence, rep coaching engine, company valuation backfill, territory mapping, stale recycler, referral engine, A/B tester, and more. Ewing repeatedly said "build the next 5 features" which kept expanding scope beyond the original plan.

### Items Found

**1. Unified Lovable Application (AND Call Command)**
- Type: Full-stack React + Supabase application
- Machine: MacBook-27, deployed via Lovable
- What happened: 3 separate projects (blank-canvas, and-call-command-pipeline, coldcall-universe) merged into a single codebase with 40+ pages, 50+ custom hooks, shared component library
- Business impact: HIGH. This is the production sales ops platform for AND Capital, CII, DPC, and RevsUp
- Recommendation: Needs a fresh-thread audit of every page to verify data connections are live and accurate post-compaction

**2. Database Schema and Migration**
- Type: Supabase PostgreSQL schema
- Machine: rdnnhxhohwjucvjwbwch.supabase.co
- What happened: Full schema migration from old cloud Supabase, new tables for call_log, call_analysis, comp_plans, cost_config, dnc_entries, placement_agents, orchestrator_queue, and more. 15+ tables touched.
- Business impact: HIGH. All operational data lives here.
- Recommendation: Run a schema diff between what was planned and what exists. The 1000-row pagination bug was caught but verify all queries paginate correctly.

**3. Salesfinity API Integration**
- Type: API pipeline (bidirectional)
- What happened: Full stress test of Salesfinity API fields. Discovered 413 Payload Too Large errors, 404 on add-contacts endpoint, custom field structure. Built push-to-Salesfinity pipeline with 6 pre-load gates (DNC, dedup, geography, phone validation, list naming convention, CRM-style merge). Built pull-from-Salesfinity for call results with scoring.
- Business impact: CRITICAL. This is the dialer integration.
- Recommendation: The Salesfinity notes field character limit was discovered but verify the workaround is deployed. The API feedback report was written to ~/Downloads/salesfinity_api_feedback_report.md.

**4. DNC System Overhaul**
- Type: Data pipeline + automation
- What happened: DNC hierarchy defined (transcript > disposition > manual). 144 DNC records backfilled with reasons. Auto-DNC wired into call ingest pipeline. Transcript scanning for DNC phrases. persons.do_not_call flag synced (was 5, now 144). DNC-to-Salesfinity sync scheduled task created.
- Business impact: HIGH. Was causing 43 of Ewing's dials and 56 of Mark's to hit DNC'd contacts.
- Recommendation: Verify the dnc-salesfinity-sync scheduled task is running and pushing correctly.

**5. Call Intelligence / Phone Intelligence Layer**
- Type: Utility module + data backfill
- What happened: 80 rep DIDs mined from call_log. Reverse-lookup system built. phone-intelligence.ts utility created. Entity attribution went from 70.4% to 100% with rep-entity fallback mapping. Alex Pappas's 942 calls classified as RevsUp.
- Business impact: HIGH. Enables accurate per-entity reporting.
- Recommendation: None immediate. This was well-executed.

**6. Commission-First Display + Entity P&L Split**
- Type: UI overhaul across 16+ files
- What happened: Caught $232M fake pipeline (42 deals with "Default 5M check" placeholder). Zeroed fake values. Switched all dollar displays from deal_value to commission. Built entity-colored P&L cards (AND=violet, CII=amber, DPC=emerald, RevsUp=blue). Shared entity-colors.ts and EntityFilter.tsx created.
- Business impact: HIGH. Commission is what reps care about, not deal size.
- Recommendation: Verify Design Precast commission rate fix (was 5%, corrected to 2%). Verify AND Capital rate is 1%.

**7. Context Graph Design System**
- Type: UX architecture principle + implementation
- What happened: Defined "Zero-Navigation" principle. Built context graphs across 5 pages (Follow-Ups, Pipeline, Meeting Prep, Contacts, Companies). Each page pre-loads the data needed to act.
- Business impact: MEDIUM. UX quality improvement.
- Recommendation: Saved to memory as design_context_graph.md. Apply to all new pages going forward.

**8. Placement Agent Strategic Pivot**
- Type: New audience type + data load
- What happened: 200 money placement firms parsed and categorized (99 HOT, 89 WARM, 12 COLD). Loaded into Supabase. New placement_agent audience type created. Impact-first cold call script written. Top 30 firms enriched via web search.
- Business impact: HIGH. This is AND Capital's new go-to-market strategy.
- Recommendation: Verify the placement agent script is accessible in the Script Library.

**9. Scheduled Automation Tasks (8 tasks)**
- Type: Claude Code scheduled tasks
- What happened: 8 scheduled tasks created for nightly audit, priority rebuild, queue check, call sync, valuation backfill, hourly call ingest, daily maintenance, DNC sync.
- Business impact: HIGH. Automates what was previously manual.
- Recommendation: Audit all 8 tasks to confirm they are enabled and running. Some may have been created with stale context.

**10. Skills Created/Modified**
- Type: Claude Code skill definitions
- What happened: cold-call-workflow, ewing-connectors, system-auditor, recording-collector, salesfinity-loader, exa-enrichment skills all created or modified. prompt-refiner invoked 35 times.
- Business impact: MEDIUM. Enables future sessions to pick up where this left off.
- Recommendation: Read cold-call-workflow/SKILL.md and ewing-connectors/SKILL.md first in any new thread.

**11. Harvester Failure (Critical Incident)**
- Type: Context collapse failure
- What happened: At hour 17+, Claude produced a "harvest" from remembered context instead of running actual filesystem commands. First attempt was a summary masquerading as an investigation. Subagent refused the task as a "prompt injection attack." Second attempt (after Ewing provided a reference harvest from a fresh thread) succeeded with real discovery.
- Business impact: LOW (caught and corrected), but HIGH as a signal that the thread was unreliable.
- Recommendation: Never run investigative/discovery tasks in a thread with 21+ compactions. Spawn a fresh session.

### Handoff Notes

**What's unfinished:**
- Company enrichment backfill (domains, websites, LinkedIn data for ~1,400 companies without industry)
- Person-company linking for unmatched records (Google X-ray search was started but not completed for all)
- Lovable deployment stability (repeated connection issues between Lovable and Supabase)
- Full validation that all 8 scheduled tasks run correctly in production
- Territory map data population
- Referral engine end-to-end test
- A/B tester with live data

**What's broken:**
- Task IDs from subagents became unreachable after compaction (b7f9b1h76, btjybkfhm, bgfp4fge8, bv4v16q8a all failed on TaskOutput)
- Some files were written to /tmp instead of ~/Downloads (despite the rule), particularly SQL files and the lovable-deploy directory
- Lovable project sync may be stale if the git push from /tmp/lovable-deploy didn't land

**What's blocking:**
- Supabase service role key needs to be confirmed in the Lovable environment variables
- Salesfinity API notes field character limit workaround needs production verification
- Company valuation backfill task was deferred pending full company profile enrichment

**What's next:**
1. Fresh-thread audit of every Lovable page against live Supabase data
2. Run all 8 scheduled tasks manually once to verify they work
3. Complete company enrichment for the 1,417 companies without industry data
4. Complete person-company linking for orphaned records
5. Validate DNC sync is flowing to Salesfinity
6. Load and test placement agent lists in Salesfinity

**What to NOT repeat:**
- Do not run this many features in a single thread. The 21 compactions destroyed reliability.
- Do not say "build the next 5 features" without scoping each one. Scope creep caused context exhaustion.
- Do not trust tool call outputs from subagents spawned more than 3 compactions ago.
- Do not run investigative tasks (harvester, system-auditor) in a saturated thread. Use a fresh session.
- Do not write files to /tmp. Every output goes to ~/Downloads.

**Files to read first:**
- `/Users/ewinggillaspy/.claude/skills/cold-call-workflow/SKILL.md`
- `/Users/ewinggillaspy/.claude/skills/ewing-connectors/SKILL.md`
- `/Users/ewinggillaspy/.claude/projects/-Users-ewinggillaspy-My-Drive--ewing-chapter-guide--Github-Ewing/memory/MEMORY.md`
- `/Users/ewinggillaspy/Downloads/thread_story_context_collapse_2026-03-23.md`
- `/Users/ewinggillaspy/Downloads/AND_Call_Command_Automation_Audit.md`
- `/Users/ewinggillaspy/Downloads/AND_Call_Command_Page_Audit.md`
- `/Users/ewinggillaspy/Downloads/harvest_macbook27_2026-03-23.md`

### What This Thread Should Have Done Differently

1. **Split into 4-5 separate threads instead of 1.** The unification build (Acts 1-4) should have been one thread. The strategic pivot and data loading (Acts 3-5) another. The UI/UX overhaul and context graph (Acts 5-6) another. The DNC/call intelligence work (Act 7) another. The enrichment and audit work yet another. Each thread would have had clean context and avoided the compaction cascade.

2. **Stopped expanding scope after hour 8.** The original goal was unification of 3 projects. By hour 8, the thread had added cost tracking, call orchestration, data cleaning, territory mapping, A/B testing, referral engines, and more. Each addition consumed context that the original goal needed. The thread should have shipped v1 of the unified app, then started fresh threads for each new feature.

3. **Written external state documents earlier.** The memory files were created during the session, but the critical architectural decisions (pipeline flow, DNC hierarchy, entity attribution rules, commission formulas) should have been written to persistent files at the moment of decision, not reconstructed from context later. The context graph principle was saved; the Salesfinity pipeline architecture was not.

4. **Never switched to Haiku mid-session.** The model switch to claude-haiku-4-5 at 22:23 UTC on Mar 18 was likely a cost-saving move, but Haiku lacks the reasoning depth for complex multi-file refactoring. The switch back to Opus came quickly, but any work done during the Haiku window needs verification.

5. **Used the prompt-refiner skill for task decomposition, not just prompt improvement.** The prompt-refiner was invoked 35 times, mostly to improve individual prompts. It should have been used to decompose "build the next 5 features" into scoped, sequenced work packages with exit criteria, before executing any of them.

### Gotchas Discovered

1. **Supabase REST API 1000-row default limit.** Queries without explicit pagination return max 1,000 rows. This made all counts look suspiciously round. Ewing caught it; Claude did not. Every query in the system needs `.range()` or pagination logic.

2. **Salesfinity API 413 Payload Too Large on notes field.** The notes field has an undocumented character limit. Pre-call research packets that are too large get rejected. Needs truncation or compression before push.

3. **Salesfinity API 404 on add-contacts endpoint.** The documented endpoint for adding contacts returned 404. Required investigation to find the working endpoint.

4. **Claude Code subagent TaskOutput IDs expire after context compaction.** Task IDs like b7f9b1h76 become unreachable once the thread compacts past the point where the agent was spawned. There is no way to recover the output.

5. **Claude Code subagents may refuse skill instructions as "prompt injection."** The harvester skill contains instructions to scan for credentials and post to Slack. A subagent flagged this as a data exfiltration attempt and refused. Workaround: run the skill in the main thread, not a delegated subagent.

6. **Lovable import-from-GitHub has a hidden limitation.** The standard import flow didn't work for this codebase. Ewing discovered a workaround by pasting code directly, which Claude noted as a pattern nobody had documented.

7. **Context compaction drops the HOW but keeps the WHAT.** After compaction, Claude remembers that the DNC system exists and what it does, but forgets the exact SQL used to create it, the specific error messages encountered during development, and the precise API call sequence. This is the root cause of the harvester failure — Claude "knew" the machine's state from memory instead of investigating it fresh.

8. **21 compactions in one thread is a reliability threshold.** By compaction 15+, tool call reliability was visibly degraded. By compaction 20+, Claude was substituting recalled facts for fresh investigation. This is the upper bound for a single thread's useful life.
