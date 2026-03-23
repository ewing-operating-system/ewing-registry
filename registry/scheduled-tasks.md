# Scheduled Tasks Registry

## MacBook-27 (10 tasks — production)
| Task | Schedule | Purpose | Active |
|---|---|---|---|
| call-ingest-hourly | Hourly | Pull Salesfinity calls, score, auto-DNC + cascade | YES |
| call-sync | Every 4 hours | Salesfinity scored call sync | YES |
| company-valuation-backfill | On demand | EBITDA-based company valuations | YES |
| daily-maintenance | Daily 6:00 AM | DNC pattern detection, stale recycler, data quality | YES |
| daily-tasks-created | Daily 8:00 AM | Full cold call workflow: email, calendar, Fireflies, scoring | YES |
| dnc-salesfinity-sync | Every evening | Push DNC entries to Salesfinity dialer | YES |
| email-monitor | Hourly :05 | Gmail scan across ewing@chapter.guide | YES |
| nightly-system-audit | Weekly | Rotating engine audit — picks oldest unaudited engine | YES |
| priority-rebuild | Sun 5pm + Wed 6pm | Conversion analysis, vertical ranking, list priority updates | YES |
| queue-autocheck | Daily | Rep queue depth check, auto-assign from unassigned lists | YES |

## Cowork VMs (4 tasks — mostly disabled)
| Task | Schedule | Purpose | Active |
|---|---|---|---|
| daily-urgent-briefing | Daily 6:06 AM | Morning briefing | YES |
| pec-evidence-logger | Daily 9:05 AM | PEC case evidence logging | NO |
| pec-fact-finder | Daily 9:34 AM | PEC case fact finding | NO |
| downloads-cleaner | One-time (3/19) | Downloads cleanup | NO |

## MacBook-GREEN (3 tasks — all disabled)
| Task | Purpose | Active |
|---|---|---|
| daily-tasks | Unknown | NO |
| email-monitor | Email scanning | NO |
| downloads-cleaner | Downloads cleanup | NO |

## Mac mini
No scheduled tasks.

## Overlap
- `email-monitor` exists on both MB-27 (active) and GREEN (disabled)
- `downloads-cleaner` exists on both Cowork VMs (disabled) and GREEN (disabled)
