# Clay.com Integration — ACTIVE

## Status: CONNECTED via Webhook + Google Sheets

## Architecture
```
Claude Code → POST company data to Clay Webhook
                    ↓
            Clay enriches automatically:
            1. Claygent (company research + owner lookup) — 1 credit
            2. Phone Waterfall (13 providers) — ~10 credits
            3. Find People at Company (fallback if Claygent misses) — 1 credit
                    ↓
            Push to Google Sheets ("Clay Enriched Results")
                    ↓
Claude Code reads Google Sheet → loads to Salesfinity → triggers SMS
```

## Webhook URL
```
https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-5ea2383e-221b-46a2-99cc-b3986575c7ee
```

## Webhook Payload Format
```json
{
  "company_name": "Baker Roofing Company",
  "company_domain": "bakerroofing.com",
  "industry": "Roofing",
  "location": "Raleigh, NC",
  "request_id": "test-004"
}
```

## Clay Table Structure
- **Workbook:** Home Services Owner Lookup Table
- **Table:** Business Owner List for Claude
- **URL:** https://app.clay.com/workspaces/211231/workbooks/wb_0tc0p1v6N67AXzJDZv2/tables/t_0tc0p2xYnoeNP2mYJdu/views/gv_0tc0p2xZHq9FiKdjFPk

### Columns (in order):
1. Webhook (source)
2. company_name (input)
3. company_domain (input)
4. company_linkedin_url (input)
5. industry (input)
6. location (input)
7. request_id (input)
8. Find People at Company (enrichment — fallback, runs only if Claygent finds no owner)
9. First Name (for Salesfinity — will split from full name)
10. Last Name (for Salesfinity — will split from full name)
11. Company & Owner Data (Claygent — primary enrichment)
12. Company & Owner Data company Domain
13. Company & Owner Data company Linkedin Url
14. Company & Owner Data owner Name
15. Company & Owner Data owner Title
16. Company & Owner Data owner Linkedin
17. Company & Owner Data employee Count
18. Company & Owner Data year Founded
19. Mobile Phone (waterfall — 13 providers)
20. Push to Google Sheets (action — only runs when Mobile Phone has value)

## Google Sheet Output
- **Sheet Name:** Clay Enriched Results
- **Sheet ID:** 1FYAW-321f9Tvt2-K47RELpKG54J4F1CTafW39XuycK4
- **Sheet URL:** https://docs.google.com/spreadsheets/d/1FYAW-321f9Tvt2-K47RELpKG54J4F1CTafW39XuycK4/edit
- **Account:** ewing-google-sheets (ewing@chapter.guide)
- **Tab:** Pushed From Clay
- **Columns (A-M):**
  - A: company_name
  - B: company_domain
  - C: Company & Owner Data company Linkedin Url
  - D: Company & Owner Data owner Name
  - E: Company & Owner Data owner Title
  - F: Company & Owner Data owner Linkedin
  - G: Mobile Phone
  - H: Company & Owner Data employee Count
  - I: Company & Owner Data year Founded
  - J: industry
  - K: location
  - L: request_id
  - M: Phone Source

## Credit Cost Per Company
- Claygent: ~1 credit
- Phone Waterfall: ~10-14 credits (stops when found)
- Find People (fallback only): ~1 credit
- Google Sheets push: free
- **Total: ~11-15 credits per company**

## Webhook Limits
- 50,000 submissions per webhook source
- After 50K, need new webhook or Enterprise passthrough

## Integration with Other Tools
```
Claude Code (builds company list)
        ↓
Clay Webhook (enriches: owner + phone)
        ↓
Google Sheet ("Clay Enriched Results")
        ↓
Claude Code reads sheet
        ↓
Salesfinity Loader (push to dialer)
        ↓
SMS Skill (voicemail follow-up)
```

## calling_for Logic
- **CII** — Trade businesses: HVAC, Plumbing, Roofing, Electrical, Pest, Landscaping, etc.
- **AND Capital** — Banking
- **Design Precast** — Concrete/Precast companies (sourced from customer Design Precast and Pipe)

## Activated: March 17, 2026
