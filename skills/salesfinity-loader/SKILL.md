---
name: salesfinity-loader
description: "Dialer list push from Supabase. Reads enriched contacts from Supabase and pushes them to Salesfinity's AI parallel dialer. Enforces six pre-load gates: DNC table check, DNC flag check, dedup across lists, geography filter, phone required, and naming convention. Never accepts raw data directly. All contacts must exist in Supabase first."
---

# Salesfinity Loader — Complete API Client (Updated March 2026)

This skill manages the full Salesfinity lifecycle: loading contacts, managing lists,
pulling analytics, reviewing AI-scored calls, managing webhooks, and tracking follow-ups.

## ARCHITECTURE

```
Supabase (persons + phone_numbers + companies + do_not_call) → 6 Gates → Salesfinity API
```

OR (when Ewing explicitly approves):

```
Raw CSV/JSON → Gates (geography, phone, DNC) → Salesfinity API
```

**This skill's primary input is Supabase.** It queries:
- `persons` — people records with enrichment data
- `phone_numbers` — phone numbers linked to person_graph_id
- `companies` — company records for company name/vertical context
- `lists` — dialing list metadata
- `list_assignments` — person-to-list mappings with status tracking
- `do_not_call` — authoritative DNC list (separate table)

**If the user gives you a raw list of contacts:**
1. Ask if they want Supabase-first pipeline or direct push.
2. If Supabase-first: use `exa-enrichment` skill to enrich and write to Supabase, then come back.
3. If direct push (Ewing approved): run gates on the raw data and push directly.

## Credentials

### Salesfinity
- **Base URL**: `https://client-api.salesfinity.co/v1`
- **API Key**: `sk_ff45bc29-e5c1-4a3f-b1e5-f9776d94cbe7` (also in scripts/salesfinity_api.py)
- **Auth Header**: `x-api-key: sk_ff45bc29-e5c1-4a3f-b1e5-f9776d94cbe7`
- **Users:**
  - Ewing: `680edc0d1504192884a148e0` (ewing@engram.nexus)
  - Mark: `68d1caac41d11ac1ce5df7a2` (mark@revsup.com)

### Supabase
- **URL:** `https://rdnnhxhohwjucvjwbwch.supabase.co`
- **Anon Key:** Read from ewing-connectors skill
- **REST API base:** `https://rdnnhxhohwjucvjwbwch.supabase.co/rest/v1`
- **Auth headers for every Supabase call:**
  ```
  apikey: <ANON_KEY>
  Authorization: Bearer <ANON_KEY>
  Content-Type: application/json
  Prefer: return=representation
  ```

## Table Schemas

**companies** (3433+ rows):
- `company_id` (uuid PK), `name`, `domain`, `website`, `vertical`
- `employee_count`, `revenue_estimate`, `year_founded`
- `city`, `state`, `country`, `location`, `source`, `calling_for`
- `industry`, `sub_vertical`
- `do_not_call` (boolean)

**persons** (4586+ rows):
- `person_graph_id` (uuid PK), `company_id` (FK)
- `first_name`, `last_name`, `full_name`, `title`
- `linkedin_url`, `email`, `personal_email`
- `state`, `city`, `timezone`, `zip`
- `source`, `source_detail`, `is_active`, `do_not_call` (boolean)
- `segment_tags`, `enrichment_status`, `calling_for`, `role_category`

**phone_numbers** (4216+ rows):
- `phone_id` (uuid PK), `person_graph_id` (FK)
- `phone_number` (e.g., "+17735752142")
- `phone_type`, `status`, `is_primary`
- `source`, `call_count`, `connect_count`

**lists** (26+ rows):
- `list_id` (uuid PK), `name`, `description`, `list_type`, `status`
- `total_persons`, `vertical_focus`, `salesfinity_id`
- `calling_for`, `contacted_count`, `connected_count`

**list_assignments** (1909+ rows):
- `assignment_id` (uuid PK), `list_id` (FK), `person_graph_id` (FK)
- `rep_id`, `position`, `status`, `priority`
- `last_attempt_at`, `attempt_count`, `next_call_after`, `notes`, `pushed_at`

**do_not_call** (authoritative DNC table):
- `id` (uuid PK)
- `person_graph_id` (FK, nullable)
- `company_id` (FK, nullable)
- `reason` (text)
- `reason_category`, `reason_text`
- `added_by` (text)
- `block_company` (boolean)
- `blocked_from_lists` (array)
- `created_at` (timestamp)

## COMPLETE SALESFINITY API REFERENCE (35 Endpoints)

**Base URL**: `https://client-api.salesfinity.co/v1`
**Auth**: `x-api-key` header on every request

### Contact Lists (8 endpoints)

#### POST /v1/contact-lists — Create list (with optional contacts)
```json
{
  "name": "AND — iBanking — ET Block 1 (v1)",  // max 100 chars
  "user_id": "680edc0d1504192884a148e0",        // REQUIRED — from GET /v1/team
  "contacts": [...]                              // OPTIONAL — max 2,000 contacts
}
```
Returns 201 with `_id` for the new list.
**Max 2,000 contacts per list. No batching needed. Payload max 10MB.**

#### POST /v1/contact-lists/{id} — Add ONE contact to existing list
**CRITICAL: The path is `/v1/contact-lists/{id}` — NO `/contacts` suffix.**
The old `/contacts` suffix returned 404. This is the CORRECT endpoint.
Contact is added to both the list AND the dialing queue immediately.
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@acme.com",
  "phone_numbers": [{"type": "direct", "number": "+14155552671"}],
  "company": "Acme Corp",
  "title": "VP of Sales",
  "notes": "Pitch script goes here — max 2,000 chars",
  "priority": 1,
  "timezone": "America/New_York",
  "custom_fields": [
    {"type": "string", "label": "Hook", "value": "..."},
    {"type": "number", "label": "Employee Count", "value": 250},
    {"type": "boolean", "label": "Decision Maker", "value": true}
  ]
}
```
Returns 201.

#### DELETE /v1/contact-lists/{id}/contacts/{contactId} — Remove contact
Removes from both list and dialing queue. Returns 200.

#### POST /v1/contact-lists/{id}/merge — Merge lists
```json
{
  "source_list_ids": ["id1", "id2", "id3"],  // max 20 source lists
  "delete_sources": true                      // optional, default false
}
```
Merges all source contacts into the target list. Returns 201.

#### GET /v1/contact-lists/csv — Get all lists (metadata only)
Query params: `search`, `filters[user]`, `sort` (default `-createdAt`), `page`, `limit` (max 100)
Returns: `{data: [{_id, name, user, total_contacts, createdAt, updatedAt}], pagination: {total, page, next}}`

#### GET /v1/contact-lists/csv/{id} — Get single list with contacts
Query params: `search` (by name/email/company), `sort`, `page`, `limit` (default 50)
Returns full contact objects with all fields, paginated.

#### DELETE /v1/contact-lists/csv/{id} — Delete a list
**CRITICAL: Path is `/csv/{id}` — NOT just `/{id}`.** The old path returned 404.

#### POST /v1/contact-lists/csv/{id}/reimport — Reset list to full queue
Replaces current queue with full source list. Useful for re-dialing a partially
completed list. Returns 201.

### Contact Schema (for create-list and add-contact)
```
first_name    string   max 200
last_name     string   max 200
email         string   max 320
phone_numbers array    max 10 items
  type        string   REQUIRED — mobile | direct | office
  number      string   REQUIRED — E.164 format (+14155552671)
  country_code string  optional — ISO alpha-2 (US, CA, etc.)
  extension   string   optional
company       string   max 300
title         string   max 300
linkedin      string   max 500
website       string   max 500
account       string   max 500
notes         string   max 2,000
priority      number   lower = higher priority
timezone      string   IANA format (America/New_York)
external_relations object   CRM IDs
custom_fields array    max 10 items
  type        string   REQUIRED — string | number | boolean
  label       string   REQUIRED — max 100
  value       any      string, number, boolean, or string array
```

### Team (1 endpoint)

#### GET /v1/team — Get all users
**CORRECT endpoint. /v1/users returns 404.**
Returns team object with `users` array. Each user has `_id`, `email`, `first_name`, `last_name`.

### Call Logs (2 endpoints)

#### GET /v1/call-log — Paginated call logs
Query params: `page`, `limit` (max 100), `sort`, and filters:
- `filters[start_date]`, `filters[end_date]` — ISO 8601
- `filters[outcome]` — answered | no-answer | cancelled
- `filters[direction]` — inbound | outbound
- `filters[min_duration]`, `filters[max_duration]` — seconds
- `filters[has_recording]` — boolean
- `filters[answered_by]` — human | machine_start
- `filters[is_completed]` — boolean
- `filters[disposition_ids]` — array of numbers
- `filters[user_ids]` — array of strings
- `filters[contact_list_ids]` — array of strings
- `filters[search]` — full-text search
Returns: data array with `_id, call_id, outcome, direction, duration, to, from,
disposition, contact, contact_list, user, recording_url, notes, transcription,
summary, is_completed, started_at, ended_at`

#### GET /v1/call-log/{id} — Single call log

### Scored Calls — AI (2 endpoints)

#### GET /v1/scored-calls — AI-scored calls with coaching
Query params: `page`, `limit`, `sort`, `start_date`, `end_date`, `min_score`, `max_score`, `user_id`
Returns per call: total_score (0-100), six scoring facets (intro 10%, discovery 25%,
pitch 20%, tonality 15%, objection_handling 15%, cta 15%), lead qualification,
messaging analysis, targeting feedback, gaps analysis, coaching recommendations
with top_wins, top_opportunities, suggested_drills.

#### GET /v1/scored-calls/{id} — Full AI insight for one call

### Analytics (3 endpoints)

#### GET /v1/analytics/overview — Aggregated metrics with growth rates
Query params: `start_date` (REQUIRED), `end_date` (REQUIRED), `user_ids`, `disposition_ids`, `timezone`
Returns: total_calls, connected_calls, conversations, meetings_set,
total_follow_up_tasks — each with value + growth %.
**Live data (March 2026): 2,481 total calls, 9 meetings set, 11% connection rate, 27% conversation rate**

#### GET /v1/analytics/list-performance — Metrics per contact list
Same params + `page`, `limit`, `search`
Returns per list: total_calls, connected_calls, conversations, meetings_set,
good_quality_contacts, data_quality score, owner info.

#### GET /v1/analytics/sdr-performance — Metrics per SDR/rep
Same params + `page`, `limit`, `search`
Returns per user: total_calls, connected_calls, connection_rate, conversations,
conversation_rate, avg_dials_day, total_duration, meetings_set, data_quality.

### Snoozed Contacts (5 endpoints)

Snoozed contacts are temporarily suppressed from call lists until their snooze period expires.

#### GET /v1/snoozed-contacts — List all snoozed
Query params: `page`, `limit`, `sort`, `linkedin_username`, `email`, `phone_number`, `external_contact_id`
**Live data: 166 snoozed contacts**

#### GET /v1/snoozed-contacts/by-linkedin/{username} — Lookup by LinkedIn
#### GET /v1/snoozed-contacts/{id} — Get by ID
#### PUT /v1/snoozed-contacts/{id} — Update snoozed contact
#### DELETE /v1/snoozed-contacts/{id} — Delete (un-snooze)

### Follow-up Tasks (1 endpoint)

#### GET /v1/follow-up — All follow-up tasks
Query params: `page`, `limit`, `sort`
Returns: priority (high/medium/low), status (not_overdue/overdue/completed),
follow_up_date, tags (timing/budget/competitor), touches count, context.
**Live data: 3 follow-up tasks**

### Dispositions (2 endpoints)

#### GET /v1/dispositions — All dispositions
Known dispositions:
1. Meeting Set
2. No Longer with Company
3. Not Interested
4. Referral
5. Wrong Contact
6. Call back later
7. Reach out in 6 months
8. Send an email
9. Do not call again
10. No Answer
11. Left Voicemail
12. Gatekeeper
13. Bad Number
14. Cancelled

#### GET /v1/dispositions/{id} — Single disposition

### Sequences (2 endpoints)

#### GET /v1/sequences — All sequences
Query params: `page`, `limit`, searchable, sortable.

#### GET /v1/sequences/{id} — Single sequence

### Custom Fields (1 endpoint)

#### GET /v1/custom-fields — CRM field mappings
Returns field mappings between Salesfinity and integrated CRMs (Salesforce, HubSpot, etc.).
**Live data: 1 mapping (source: csv, 10 fields)**

### Webhooks (6 endpoints)

#### POST /v1/webhooks — Create webhook
```json
{
  "name": "Call Logger",
  "url": "https://your-endpoint.com/webhook",
  "events": ["CALL_LOGGED", "CONTACT_SNOOZED"],
  "dispositions": [1, 3]  // optional — filters CALL_LOGGED events
}
```
Events: CALL_LOGGED, CONTACT_SNOOZED

#### GET /v1/webhooks — All webhooks
#### GET /v1/webhooks/events — Available event types (requires higher auth — 401 with API key)
#### GET /v1/webhooks/{id} — Single webhook
#### PUT /v1/webhooks/{id} — Update webhook
#### DELETE /v1/webhooks/{id} — Delete webhook
#### GET /v1/webhooks/{id}/logs — Webhook delivery logs

## CORRECTIONS LOG (What Was Wrong Before)

| Old Belief | Reality | Impact |
|---|---|---|
| "POST /v1/contact-lists/{id}/contacts returns 404" | Correct path is `POST /v1/contact-lists/{id}` (no /contacts suffix) | We built sub-list workarounds for nothing |
| "413 Payload Too Large with >15 contacts" | Max is 2,000 per list. No batching needed. | We split into 15-contact sub-lists unnecessarily |
| "DELETE /v1/contact-lists/{id} returns 404" | Correct path is `DELETE /v1/contact-lists/csv/{id}` | We thought delete was broken |
| "GET /v1/contact-lists gets all lists" | Correct path is `GET /v1/contact-lists/csv` | Was hitting wrong endpoint |
| "Must create sub-lists for >15 contacts" | Send up to 2,000 in one create-list call | No more (pt 2), (pt 3) suffixes |
| "notes field must be under 50 chars" | Notes max is 2,000 chars | Can put full pitch script in notes |

## MANDATORY PRE-LOAD GATES

These 6 gates are non-negotiable. Every contact must pass ALL 6 before being sent
to Salesfinity. Run them in order. If ANY gate fails, that contact is SKIPPED.

### Gate 1: DNC Check — `do_not_call` Table (Person)
```
GET /rest/v1/do_not_call?person_graph_id=eq.{person_graph_id}
```
If any row returned → SKIP.

### Gate 2: DNC Check — `persons.do_not_call` Flag
`persons.do_not_call = true` → SKIP.

### Gate 3: DNC Check — Company
```
GET /rest/v1/do_not_call?company_id=eq.{company_id}
```
Also check `companies.do_not_call = true`. Either → SKIP.

### Gate 4: Duplicate Check — No Person on Multiple Active Salesfinity Lists
```
GET /rest/v1/list_assignments?person_graph_id=eq.{id}&status=not.in.(completed,skipped)&pushed_at=not.is.null
```
If already on an active list → SKIP.

### Gate 5: Geography Check — US/Canada Only
Phone MUST start with `+1`. International → SKIP.

### Gate 6: Phone Number Required
No phone number → SKIP. Flag as "needs enrichment".

### Gate Summary Report
Show report and wait for user confirmation before pushing.

## AND Capital Pitch Templates (Updated March 2026)

**CRITICAL:** AND Capital is the CLIENT looking for placement partners and iBanks to
RAISE EQUITY for AND Capital's funds. The sweetener is debt and LBO deal flow.
Never position AND Capital as a service provider to these firms.

**CRITICAL:** Never use the word "satellite" anywhere. The satellite project is over.
Rule 14 — permanent.

### Research-First Custom Fields (Hook Priority)
When custom research data is available, use it. Hook priority order:
1. Trigger event (fund raise, deal close, promotion)
2. Their specialty (what they specifically do)
3. Firm achievement (something the firm did)
4. Role-based pain (generic but relevant to title)

```json
"custom_fields": [
  {"type": "string", "label": "Hook", "value": "Research-based opening — what makes them relevant"},
  {"type": "string", "label": "Context", "value": "Their background, career, firm focus"},
  {"type": "string", "label": "Differentiator", "value": "AND Capital — impact-driven alternative fund. Two thesis-driven strategies: O&G Exploration + Wellness & Longevity."},
  {"type": "string", "label": "The Ask", "value": "Raise equity for our funds. Debt and LBO deal flow comes with the relationship."},
  {"type": "string", "label": "Source", "value": "LinkedIn bio + web research"}
]
```

### Notes Field — Full Pitch Script (max 2,000 chars)
The notes field now holds the FULL 15-second call opening script:
```
"notes": "Hi {first_name}, this is Ewing with AND Capital. {HOOK} — we're an alternative fund looking for the right placement partner to raise equity. {ASK}"
```

Ask variations by role:
- Placement Agent: "We also have debt and LBO deal flow we'd want our placement partner involved in. Are you taking on new fund mandates?"
- CEO/President: "The equity raise is the starting point — there's debt and LBO pipeline that comes with it. Can we get 15 minutes on your calendar?"
- MD/Partner: "The equity raise is the starting point — we've also got debt and LBO activity we'd want to route through the right partner. Do you have 30 seconds?"
- IR/Capital Formation: "Beyond the equity raise, there's debt and LBO deal flow attached. Are you evaluating new mandates right now?"

## Workflow

### Step 1: Query Supabase for Contacts
User specifies what to load. Query by list name/ID or by vertical/entity/status.

### Step 2: Run All 6 Gates
Execute gates 1-6 for every contact. Show gate report. Wait for confirmation.

### Step 3: Create List Records in Supabase

#### List Naming Convention
Format: `{Entity} — {Vertical} — {Timezone Group} (v{N})`
- Em-dash ( — ), not hyphen
- Entity: "AND" for AND Capital
- Vertical: "Placement Agent", "iBanking", etc.
- Timezone: "ET Block 1", "ET Block 2", "CT + Intl", "PT + MT"
- Version: increment from last list

### Step 4: Build Salesfinity Contact JSON
For each contact passing gates, build the contact object.
Notes field = full pitch script. Custom fields = research data.

### Step 5: Push to Salesfinity
**Max 2,000 contacts per list. No batching. One API call per list.**

```bash
python <skill-path>/scripts/salesfinity_api.py \
  --action create-list \
  --name "AND — iBanking — ET Block 1 (v1)" \
  --user-id "680edc0d1504192884a148e0" \
  --contacts-json '/path/to/contacts.json'
```

To add a single contact to an existing list:
```bash
python <skill-path>/scripts/salesfinity_api.py \
  --action add-contact \
  --list-id "69c1aa022118877571555c31" \
  --contact-json '/path/to/contact.json'
```

To merge multiple lists into one:
```bash
python <skill-path>/scripts/salesfinity_api.py \
  --action merge-lists \
  --list-id "TARGET_ID" \
  --source-list-ids "ID1,ID2,ID3" \
  --delete-sources
```

### Step 6: Update Supabase After Push
Update `lists.salesfinity_id` and `list_assignments.pushed_at`.

### Step 7: Confirm and Report

## CLI Quick Reference

```bash
# Lists
--action create-list      --name "..." --user-id "..." [--contacts-json ...]
--action add-contact      --list-id "..." --contact-json "..."
--action remove-contact   --list-id "..." --contact-id "..."
--action merge-lists      --list-id "TARGET" --source-list-ids "ID1,ID2" [--delete-sources]
--action get-lists        [--search "..."] [--page N] [--limit N]
--action get-list         --list-id "..."  [--search "..."] [--page N]
--action delete-list      --list-id "..."
--action reimport-list    --list-id "..."

# Team
--action get-team

# Call Logs
--action get-call-logs    [--page N] [--limit N]
--action get-call-log     --call-id "..."

# Scored Calls
--action get-scored-calls [--start-date ...] [--end-date ...] [--page N]
--action get-scored-call  --call-id "..."

# Analytics
--action analytics-overview    --start-date "..." --end-date "..."
--action analytics-list-perf   --start-date "..." --end-date "..."
--action analytics-sdr-perf    --start-date "..." --end-date "..."

# Snoozed
--action get-snoozed      [--page N] [--limit N]
--action delete-snoozed   --contact-id "..."

# Other
--action get-follow-ups   [--page N]
--action get-dispositions
--action get-sequences    [--page N]
--action get-custom-fields

# Webhooks
--action create-webhook   --name "..." --webhook-url "..." --webhook-events "CALL_LOGGED,CONTACT_SNOOZED"
--action get-webhooks
--action get-webhook-events
--action delete-webhook   --webhook-id "..."
--action get-webhook-logs --webhook-id "..."

# Converters
--action convert-exa      --exa-json "..." [--context-json "..."] [--output "..."]
--action convert-csv      --csv-input "..." [--output "..."]
--action validate-name    --name "..."
```

## Important Rules

1. **ALL 6 gates must pass** before any contact reaches Salesfinity.
2. **Show gate report and wait for confirmation** before pushing.
3. **Max 2,000 contacts per list.** No batching, no sub-lists.
4. **Never load a person onto multiple active lists.** Gate 4 enforces this.
5. **DNC is permanent** until Ewing manually removes it.
6. **Phone numbers are required** — contacts without phones are flagged, not loaded.
7. **Naming convention is enforced** — `{Entity} — {Vertical} — {Timezone} (v{N})`.
8. **Notes field holds the full pitch script** (max 2,000 chars). Custom fields hold research.
9. **Update `pushed_at` in Supabase** after every successful push.
10. **ALL backup files go to ~/Downloads.** NEVER write to /tmp.
11. **NEVER fabricate contact data.** Every field comes from Supabase/research or is omitted.
12. **Add-contact path is `/v1/contact-lists/{id}`** — NOT `/v1/contact-lists/{id}/contacts`.
13. **Delete-list path is `/v1/contact-lists/csv/{id}`** — NOT `/v1/contact-lists/{id}`.
14. **NEVER use the word "satellite" anywhere.** The satellite project is over. Permanent rule.
