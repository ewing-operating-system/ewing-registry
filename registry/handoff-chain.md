# Handoff Chain — What The Next Thread Needs To Know
# Updated by each debrief. Read this FIRST in any new session.
# Updated: 2026-03-23

## Latest Handoff: Consolidation Thread (Mac mini, 2026-03-23)

### What's unfinished
1. Pipeline middle layer NOT WIRED: Google Sheets → Supabase → Salesfinity still disconnected
2. 26 "send an email" follow-ups from this week's calls — not yet drafted or sent
3. 17 "call back later" callbacks — not yet scheduled on calendar
4. 7 meetings from this week — need confirmation and prep materials
5. 3 referrals need immediate action: Ryan (Evo Pest owner), Ian Poacher (Pacific Shore — WANTS TO SELL), Steve at Lenox Advisors
6. GREEN's 3 unpushed commits on coldcall-universe v2-overnight-build branch
7. debugger-tool has 2 unpushed commits
8. GitHub PAT ghp_Y6Z38x3... needs rotation (exposed in remote URLs)
9. MacBook-GREEN disk at 96% — needs cleanup
10. SSH not enabled on Mac mini — physical bottleneck remains

### What's broken
- Slack canvas write from Cowork VMs (abandoned approach, now using GitHub)
- GitHub push from some Cowork VMs (no git credentials)
- Plugin/MCP inconsistency across Cowork sessions

### What's blocking
- SpokePhone integration: waiting on API credentials
- Google Sheets → Supabase wiring: needs development
- Supabase → Salesfinity wiring: needs development
- Remote control of Mac mini: needs SSH setup or Screen Sharing enabled

### What's next (priority order)
1. **Monday offense:** Confirm 7 meetings, call 3 referrals, send 26 follow-up emails, schedule 17 callbacks
2. **Wire the pipeline middle:** Sheets → Supabase → Salesfinity
3. **Run debrief** in remaining open threads to capture everything
4. **Consolidate Supabase:** Verify which of 4 instances are needed, decommission the rest
5. **Unify GitHub:** Pick one account, migrate repos

### What to NOT repeat
- Don't post to Slack canvas — it doesn't work from Cowork VMs
- Don't build apps to solve config problems (Hovering Cloud lesson)
- Don't create new Supabase instances — check existing ones first
- Don't hardcode API keys in skills — reference the vault
- Don't assume file paths — always use find

### Files to read first
- `ewing-registry/analysis/full-tagged-registry.md` — complete inventory with all 30 tags
- `ewing-registry/analysis/engineer-requirements.md` — what the virtual engineer must do
- `ewing-registry/analysis/call-data-summary.md` — this week's 1,386 calls
- `ewing-registry/registry/gotchas.md` — platform bugs to avoid
- This file (handoff-chain.md) — you're reading it
