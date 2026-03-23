# The Story of Building the Phoenix TAM Engine
**Session:** phoenix-tam-engine-build
**Date:** 2026-03-23
**Machine:** ClawdBots-Mac-mini-8 (Mac Mini)
**Duration:** ~3 hours (afternoon to late evening)

---

Ewing opened the thread with a wall-of-text vision dump — the kind that holds an entire business strategy in a single unstructured paragraph. He wanted to scrape every home services business across the entire Phoenix metropolitan area. HVAC, roofing, pest control, plumbing, electrical, landscaping, pool service, garage doors, fencing, concrete — across 24 cities radiating from Phoenix and Scottsdale. He wanted business names, websites, year founded, owner names, phone numbers, mailing addresses. He wanted it cheap, fast, and validated by two AI models working independently.

The vision was specific where it mattered: two cheap models that compare their findings, disagreements stored in Supabase for manual review, a cost tracker that logs every penny including accidental double-enrichments, awards lists scraped for free, and the AZ Registrar of Contractors mined for owner names and license numbers. He knew his tools — Exa.ai for web contact search, Clay.com with a legacy 50K-credit-per-month plan for waterfall phone enrichment.

Claude recognized this as a prompt-refiner candidate but Ewing wanted it built, not refined. He answered the two setup questions — "Build it now" and "50,000 credits at $800/month on Clay's legacy plan" — and then said "no more questions, just build." So Claude built.

The cost model came first. Discovery via Google Maps at $0.017/record, Gemini 2.0 Flash verification at $0.0005, Claude 3 Haiku cross-verification at $0.001, Exa enrichment at $0.06-0.12, Clay waterfall at $0.22-1.05. Total projected: $0.30-1.19 per fully enriched record, or as cheap as $0.02/record for discovery-only. For the estimated 3,000-8,000 businesses across Phoenix metro, that's $900-4,800 for a full run, or $40-160 for the cheap discovery pass. The recommendation: scrape everything cheap first, then selectively enrich the top 30-40%.

Claude wrote 15 Python files across 5 modules in rapid succession. The Google Maps scraper, awards list scraper (7 sources including Best of the Desert, Best Pick Reports, Angi, Expertise.com, Yelp, BBB, HomeAdvisor), AZ ROC scraper, Gemini Flash verifier, Claude Haiku verifier, consensus engine, Exa enricher, Clay enricher, Supabase client, cost tracker, and main orchestrator. The SQL schema created 6 tables and 2 views — businesses, verifications, disagreements, enrichments, awards sources, cost log, plus aggregated cost views.

The Supabase schema creation hit a wall — the REST API doesn't support DDL operations. Claude pivoted immediately to psycopg2 (already installed) and connected directly to the Postgres instance. All 19 SQL statements executed successfully. Tables were live.

GitHub repo creation was clean — `gh repo create` pushed to `clawdking1-GH/phoenix-tam-engine` as a private repo on the first try.

Then Ewing asked to turn this into an autonomous ClawdBot prompt. Claude loaded the clawdbot-creator skill to get the full environment blueprint — every API key, every credential, every machine detail. The config.py was already populated with Supabase keys and Gemini keys from the skill.

Ewing wanted his Exa API key pulled from his credentials skill. Claude went to retrieve it. Then Ewing made a decisive request: "From now on, any time I give you a key of any kind, label it, store it, time stamp it, and organize it. I'm tired of giving the same keys over and over." This was a fundamental process change — building a permanent credential vault.

Ewing also asked about connecting to 1Password. This led to a frustrating detour. The `op account add` command requires interactive terminal input — email, secret key, master password — none of which Claude can type for him. The conversation went in circles across multiple Claude sessions (visible in the screenshot Ewing shared). Ewing grew frustrated: "I have no idea what to do. I'm mortally confused." Claude simplified: open a fresh Terminal, paste one command, type your credentials when prompted. But ultimately Ewing said "Forget the 1-password stuff. it's obviously too hard for now. let's skip it and continue."

Back on track, Ewing asked about the Google Maps Places API. He shared screenshots of the Google Cloud Console. Claude identified he was on the Maps tab, directed him to Places, and confirmed both Places API and Places API (New) were already enabled. The API was ready.

Meanwhile, the ClawdBot on the Mac Mini had been running the TAM engine independently. It upgraded the Google Maps scraper from the legacy API to the new Places API v1, added junk filtering for awards list scrapers (filtering out article titles like "What Does HVAC Mean"), implemented cross-table dedup against the existing M&A pipeline targets table, auto-agreed on single-model Gemini results with confidence >= 0.6 when Haiku wasn't configured, and added both models' raw findings as separate columns on the business record. The engine had already been running discovery passes.

Ewing then asked to "Build out a lovable project" — a frontend visualization of the research with personal narratives, industry multiples, and valuation parameters. He also wanted QR codes, profile pages per business owner, and the lovable layout mapped by industry with M&A pricing dynamics (single vs. multi-location, residential vs. commercial, home services vs. single-trade).

Then came the confusion about how to start ClawdBot. Ewing asked "what is the terminal command to get clawdbot awake?" Claude initially said `claude` but Ewing corrected — "Claude is for claude. What is _____ for clawdbot?" The answer: `openclaw tui`.

The thread ended with Ewing requesting a debrief.

**What was brilliant:** The speed of the build — from vision dump to working engine with Supabase tables, GitHub repo, and 15 production files in under 2 hours. The cost model was thorough. The AZ ROC scraper was a genuine insight — every licensed contractor in Arizona has their owner name on file, which is exactly the data Ewing needs for handwritten letters.

**What was painful:** The 1Password detour cost 15+ minutes and ended in abandonment. The confusion about `openclaw tui` vs `claude` was a naming/identity issue that should have been answered instantly. Multiple Claude sessions running simultaneously on the Mac Mini created confusion about which bot was doing what.

**The filter:** Does this help Ewing get a signed representation agreement faster? Yes — this engine identifies every home services business owner in Phoenix metro, their phone number, and their mailing address. That's the target list for AND Capital's M&A outreach.
