---
name: rate-oracle
description: "Track API rate limits, costs, tiers, incident history, and automatic recovery protocols. Trigger whenever ClawdBot hits a rate limit, gets a 429 error, stalls for more than 2 minutes, or before running any batch/pipeline operation."
---

# Rate Oracle

You are the cost/speed intelligence layer for Ewing's operation. Every API, every service, every data source has a price, a rate limit, and usually a workaround. Your job is to know all three and make sure Ewing never overpays or gets throttled by surprise.

## Why This Matters

Ewing runs three companies (Next Chapter, RevsUp, AND Capital) with automated pipelines that make thousands of API calls per day. The difference between a smart choice and a lazy one can be hundreds of dollars a month. Finding a free workaround that does the same job as a $0.10/record paid API is worth celebrating and tracking.

---

## Quick Reference

### Current Tier Status (as of 2026-03-21)

| Service | Tier | Requests/Min | Daily Limit |
|---------|------|-------------|-------------|
| Anthropic Claude API | Tier 1 (verify if Tier 2) | 60 (or 1,000 if Tier 2) | Unlimited |
| Google Gemini (AI Studio) | Free | 5/min | 20/day |
| Google Custom Search JSON | Paid | ~60/min | 10,000/day |
| Supabase | Free tier | 500/min | Unlimited |

### Mandatory Retry Policy

Attempt 1 → fail → wait 30s → Attempt 2 → fail → wait 60s → Attempt 3 → fail → wait 120s → Attempt 4 → fail → SKIP. Log it. Move on. NEVER retry in a tight loop.

### Batch Sizing by Tier

| Tier | Max Concurrent Agents | Batch Size | Delay Between |
|------|----------------------|------------|---------------|
| Tier 1 (60 req/min) | 1 only | 5 targets | 90 seconds |
| Tier 2 (1,000 req/min) | 2 agents | 20 targets | 30 seconds |
| Tier 3 (2,000 req/min) | 3 agents | 50 targets | 15 seconds |

On Tier 1: NEVER run Scout and Next simultaneously.

### Agent Assignment

| Task | Model |
|------|-------|
| Scraping / extraction / validation | Haiku (10x cheaper) |
| Research / analysis / report writing | Sonnet |

### Search Strategy: Cheapest First

1. Google Custom Search ($0.005/query)
2. Gemini grounding (free, 20/day)
3. Claude (expensive — synthesis only)

### 10 Known Errors (Quick Fix)

1. 429 from Anthropic → Stop all agents. Wait 2 min. Restart ONE.
2. 403 from Google Search → Enable the API separately from billing. Wait 1 hour.
3. Permission denied → sudo
4. OpenClaw retry loop → Kill (Ctrl+C). Restart smaller batch.
5. Cannot GET / on Hovering Cloud → Normal. Ignore.
6. Supabase JWT error → anon key in apikey header, service role in Authorization Bearer.
7. zsh parse error near & → Wrong terminal. Use openclaw tui.
8. API key not persisting → Add to ~/.zshrc, then source ~/.zshrc
9. Quality-review stalled → Check pipeline_log in Supabase. Restart.
10. Google quota 0 after billing → Propagation delay. Wait 1 hour.

### Self-Diagnostic (When Stuck > 2 Min)

1. Am I retrying the same call 3+ times? → SKIP it.
2. Did I get a 429? → Stop agents. Wait 2 min. Restart one.
3. Using Sonnet for grunt work? → Switch to Haiku.
4. Right endpoint? → Google has 3 search APIs.
5. Right key in right header? → Check.
6. Right terminal? → OpenClaw TUI vs regular zsh.
7. Should I skip this target? → Yes. Log it. Move on.

### Pre-Flight Check Script

Run before any pipeline:
```bash
#!/bin/bash
echo "=== PRE-FLIGHT ==="
HTTP=$(curl -s -o /dev/null -w "%{http_code}" https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-haiku-4-5-20251001","max_tokens":5,"messages":[{"role":"user","content":"1"}]}')
[ "$HTTP" = "200" ] && echo "✓ Anthropic UP" || echo "✗ Anthropic DOWN ($HTTP)"
[ -n "$ANTHROPIC_API_KEY" ] && echo "✓ Key loaded" || echo "✗ Key MISSING"
echo "=== DONE ==="
```

---

## Incident Log

| # | Date | Service | What Happened | Hours Lost |
|---|------|---------|---------------|------------|
| 1 | 2026-03-19 | Anthropic | 429 retry loop. Scout + Next simultaneous on Tier 1. | 6+ hrs |
| 2 | 2026-03-19 | Google | Custom Search 403 after billing enabled. API not turned on. | 4-6 hrs |
| 3 | 2026-03-20 | Anthropic | Quality-review job stalled. Silent rate limit retry. | 2+ hrs |

### Detailed Incident Context

**Anthropic Rate Limit Incidents:**
- 2026-03-21 ~14:00 UTC: OpenClaw hit HTTP 429 "30,000 input tokens per minute" limit on claude-sonnet-4-6. Organization: "Ewing's Individual Org". CONFIRMED TIER 1. Sonnet=30K/min, Haiku=50K/min, 50 req/min. OpenClaw's retry loop made it worse — every failed retry counts against the limit.
- 2026-03-21 ~16:00 UTC: Rate limit persisted for 4+ hours. Cascading retry loop locked out pipeline completely. Ewing purchased $50 in credits to force Tier 2 upgrade.
- 2026-03-21 ~16:30 UTC: Second batch of 10 HVAC targets hit same 429 errors during Scout research and quality review phase. Pipeline froze mid-batch with 135K/1.0M tokens consumed (14%).
- CAUSE: OpenClaw sends large context windows (100k+ tokens per session). At 30k tokens/min, a single request can exhaust the entire minute's quota. When it fails and retries immediately, it creates a cascading failure loop. Each retry is a NEW request that counts against the limit, making recovery impossible.
- TOTAL TIME LOST TO ANTHROPIC RATE LIMITS: ~6+ hours across two incidents
- FIX APPLIED: Ewing purchased $50 credits (total spend now $50+), which should trigger Tier 2 upgrade (80K tokens/min, 1,000 req/min). Pending confirmation at https://console.anthropic.com/settings/limits

**Google Rate Limit Incidents:**
- 2026-03-21 ~10:00 UTC: Pipeline started. Hit Google rate limit after ~20 queries (ABC + Jon Wayne + partial John Moore)
- 2026-03-21 ~11:00 UTC: Next agent switched to web_fetch workaround. Completed Strand Brothers, Berkeys, Champion, Abacus, Radiant, Total Air, Air Comfort via direct website checks
- 2026-03-21 ~12:00 UTC: Ewing enabled Google billing. API still returning rate limit errors.
- 2026-03-21: KEY FINDING — billing alone doesn't unlock paid quota. API must be explicitly enabled and quota must propagate.
- 2026-03-21 CRITICAL DISCOVERY: OpenClaw's web_search uses GEMINI with Google Search grounding, NOT Custom Search API. Gemini AI Studio keys have a hard 20 req/day cap that billing alone does NOT lift. The Custom Search API (10,000/day paid) is a completely separate product sitting unused.
- KEY STORED IN: ~/.openclaw/openclaw.json (hardcoded, NOT read from .env)

---

## Detailed Service Knowledge Base

### Google Search (for pipeline research)

**IMPORTANT LESSON LEARNED (2026-03-21):**
Google has TWO gates to using a paid API:
1. **Billing enabled on the project** — this just links a credit card
2. **The specific API enabled + quota increased** — this is the part that actually unlocks paid usage
Having billing enabled does NOT automatically upgrade your quota. You must go to the API's Quotas page and verify the daily limit increased from the free tier cap. If it still shows the free tier number, you're still rate-limited even though you're "paying."

**Fix link:** https://console.cloud.google.com/apis/api/customsearch.googleapis.com/overview
**Quota link:** https://console.cloud.google.com/apis/api/customsearch.googleapis.com/quotas

**LESSON: Google has THREE separate search products with separate billing:**
1. Gemini API with grounding (AI Studio) — 20 req/day free, needs separate paid upgrade
2. Custom Search JSON API — 100/day free, 10,000/day paid at $5/1000
3. Google Search (browser) — unlimited but no API
Each has its own key, its own quota, its own billing. Paying for one does NOT unlock the others.

**Option A: Google Custom Search API (CURRENT — via OpenClaw)**
- Free tier: 100 queries/day (was hitting limit at ~20 queries — actual usable was ~20 due to Gemini routing)
- Paid: $5 per 1,000 queries (10,000/day cap on paid tier)
- Cost per company: ~$0.05 (10 acquisition x-ray queries per company)
- API key: AIzaSyDVx92zD1CyrGNcnfEvDZkki6BlSFrW2e4
- REQUIRES: Custom Search Engine ID (cx parameter) — create at https://programmablesearchengine.google.com
- **STATUS (2026-03-21): Billing linked but API still rate-limiting. Likely needs API explicitly enabled or quota propagation (up to 1 hour).**

**Option B: Gemini API with Grounded Search**
- Free tier: 20 req/day (NOT 1,500 as initially estimated — this was wrong)
- 5 req/min rate limit
- Overnight capacity on free: ~1.3 companies (not viable for pipeline)
- Paid tier: ~60 req/min, much higher daily limits
- Cost paid: ~$0.01-0.03 per company
- Decision: Free tier is useless for pipeline. Paid tier is viable but Custom Search is simpler.

**Option C: web_fetch workaround (FREE, no API needed)**
- OpenClaw's Next agent can use web_fetch to hit company websites directly
- No rate limit, no API key needed
- Quality: Gets basic info (ownership, about page, services) but NOT search engine results
- Used as fallback when Google API is rate-limited
- Decision: Good supplemental source but can't replace x-ray search queries

**Option D: Brave Search API**
- Free tier: 2,000 queries/month
- Paid: $5/month for 20,000 queries
- Decision: Rejected — Google ecosystem is better for home services (GBP, Maps, Reviews)

**FIX OPTIONS:** (1) Upgrade Gemini to pay-as-you-go at aistudio.google.com/apikey, OR (2) Switch OpenClaw to use Custom Search API + Search Engine ID instead of Gemini grounding

### Anthropic Claude API (for agent processing)

**Claude Sonnet 4.6 (Next agent - manager)**
- $3/M input tokens, $15/M output tokens
- Used for: pipeline orchestration, quality review, report generation
- Cost per target: ~$0.03-0.05

**Claude Haiku 4.5 (Scout agent - worker)**
- $0.25/M input tokens, $1.25/M output tokens
- Used for: research execution, data extraction
- Cost per target: ~$0.005-0.01

**Cost decision: Use Haiku for grunt work, Sonnet only for quality-critical output (reports, briefs). This saves ~80% on research costs.**

**RATE LIMITS BY TIER (Anthropic):**

| Tier | Requirement | Input Tokens/Min | Requests/Min |
|------|------------|-----------------|--------------|
| Free | $0 | 20,000 | 50 |
| Tier 1 | $5 credit | 60,000 | 60 |
| Tier 2 | $40 spend | 80,000 | 1,000 |
| Tier 3 | $200 spend | 160,000 | 2,000 |
| Tier 4 | $400 spend | 400,000 | 4,000 |

**Check your tier:** https://console.anthropic.com/settings/limits
**Add credits:** https://console.anthropic.com/settings/billing

**PREVENTION RULES:**
1. NEVER retry immediately on 429 — use exponential backoff (30s → 60s → 120s → skip)
2. Don't run Scout + Next simultaneously on Tier 1 — they compete for the same token budget
3. Use Haiku for grunt work (separate, higher rate limit than Sonnet)
4. Keep context windows under 50K tokens when possible
5. Process companies sequentially with 30-second gaps on Tier 1-2
6. If 4 consecutive retries fail, SKIP that company and move on — don't freeze the pipeline

### Supabase (pipeline database)
- Free tier: 500MB storage, 50k monthly active users
- Current usage: 10 targets, ~0.01MB — essentially zero
- Upgrade trigger: 500MB or if we need more than 2 free projects
- Cost if upgraded: $25/month for Pro

### Data Enrichment Services

**Apollo.io**
- Free tier: 50 credits/month, limited exports
- Paid: starts at $49/month for 2,500 credits
- Cost per enriched contact: ~$0.02-0.10
- Best for: company data, employee counts, contact info

**Exa.ai (Websets)**
- Free tier: varies, API-based pricing
- Best for: AI-powered search to find companies Apollo misses
- Cost: ~$0.003-0.005 per search

**Clay.com**
- Free tier: limited credits, LinkedIn scraping included
- LOOPHOLE: Can pull LinkedIn company data for free that Apollo charges for
- Enrichment waterfall: tries multiple sources, uses cheapest that works

**ZoomInfo**
- Enterprise pricing: $15k+/year
- Cost per record: ~$0.50-1.00
- Decision: SKIP — way too expensive for our volume. Apollo + Exa + Clay covers it.

### Outreach Tools

**Instantly (cold email)**
- $47/month for 5,000 emails
- Cost per email: ~$0.01
- Includes warmup, rotation, inbox placement

**Linked Helper (LinkedIn automation)**
- ~$15/month
- Runs on desktop, handles sequencing
- Cost per connection request: ~$0.001

**Handwrytten (handwritten letters)**
- $4-5 per letter including postage
- Only for warm leads (opened email OR viewed report)
- Decision: High cost per unit, but 90%+ open rate makes ROI strong for qualified leads

---

## The Loophole Leaderboard

Track every time we find a cheaper way to do something:

| Rank | Workaround | Expensive Way | Cheap Way | Savings Per Record | Est. Monthly Savings |
|------|-----------|---------------|-----------|-------------------|---------------------|
| 1 | Clay.com LinkedIn scrape | Apollo @ $0.10/record | Clay free tier @ $0/record | $0.10 | $500+ |
| 2 | web_fetch fallback | Google Custom Search @ $0.005/query | Direct website fetch @ $0 | $0.005 | ~$5/month |
| 3 | Berkeys/Abacus PE discovery | Paid database lookup @ $0.50+/record | ACHR News trade press (free via web_fetch) | $0.50 | Case-by-case |

Every new workaround gets added. Celebrate the wins.

---

## Detailed Known Error Patterns

| Error | Root Cause | Fix |
|-------|-----------|-----|
| HTTP 429 "input tokens per minute" | Anthropic tier rate limit | Wait 30s+ between retries. Check tier. Never immediate retry. |
| HTTP 429 retry loop (cascading) | Each retry counts against limit | STOP retrying. Wait 2 min. Skip company if 4th retry fails. |
| Google Custom Search 403 | API not enabled or key/project mismatch | Check console: APIs → Custom Search → Enable. Wait 1hr for propagation. |
| Gemini 20/day cap hit | web_search uses Gemini grounding, not Custom Search | Switch to web_fetch calling Custom Search JSON API endpoint directly |
| "Expected 3 parts in JWT" | Wrong Supabase auth header format | Use `Bearer <anon_key>` in Authorization header |
| ANTHROPIC_API_KEY empty | Env var not persisted in ~/.zshrc | `source ~/.zshrc` or re-export the key |
| "Cannot GET /" on Hovering Cloud | Normal — no web UI at root | Hovering Cloud is dead. Use ~/cloud-transfer.sh instead. |
| Claude Code permission prompts | Fetch(*) or Bash(*) not set | `/permissions` → add rule → save to User settings (option 3) |
| "zsh: parse error near '&'" | Pasted OpenClaw instructions into regular terminal | Switch to OpenClaw TUI tab first, then paste |
| OpenClaw config key not updating | Key in openclaw.json, not .env | Edit ~/.openclaw/openclaw.json directly, restart OpenClaw |

---

## How to Use This Skill

### When planning a new pipeline or feature:
1. Check what APIs/services are needed
2. Look up each one in the knowledge base above
3. Calculate total cost per unit and overnight throughput
4. Check for workarounds or cheaper alternatives
5. Present the tradeoff: speed vs quality vs cost
6. Update the knowledge base with any new findings

### When hitting a rate limit:
1. Identify which service hit the limit
2. Check if we're on free tier and if paid solves it
3. Calculate cost of upgrading vs cost of being slower
4. Check for workaround (different API, batching, off-peak timing)
5. Log the decision

### When adding a new service:
1. Research ALL tiers and limits before committing
2. Start on free tier unless volume demands otherwise
3. Add to knowledge base with full pricing breakdown
4. Look for loophole alternatives
5. Add to leaderboard if a workaround is found

### Monthly cost review:
Calculate total spend across all services. Compare to previous month. Check if any services should move up or down a tier. Update the leaderboard with cumulative savings.

## Overnight Pipeline Math Template

When Ewing asks "how many companies can we process tonight?" use this formula:

```
Searches per company = [acquisition checks] + [research searches] + [enrichment lookups]
Bottleneck = MIN(API rate limit × hours, daily cap, budget ÷ cost per query)
Companies per night = Bottleneck ÷ searches per company
Total cost = companies × cost per company
```

Always show the math. Always show alternatives. Always celebrate when the free tier is enough.

## Persistence

When new pricing data, workarounds, or decisions are discovered:
1. Tell Ewing what was found
2. Update this skill's knowledge base section (ask Ewing to save the updated version)
3. Add to Loophole Leaderboard if applicable
4. Log the decision with date and reasoning

The goal is that 6 months from now, this skill contains a comprehensive pricing database for every API and service Ewing has ever evaluated, with battle-tested decisions and a trophy wall of money saved.