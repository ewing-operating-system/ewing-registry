# Risk Register — 2026-03-23

## HIGH Risk
| Risk | Machine | Impact | Action |
|---|---|---|---|
| coldcall-universe push blocked | MB-27 | 24 staged files can't reach GitHub (SSH key mismatch + HTTPS token rejected) | Fix GitHub auth on MB-27 |
| coldcall-universe 3 unpushed commits | GREEN | Phases 1-8 of v2-overnight-build only on local disk | Push from GREEN |
| GitHub PAT exposed in git remotes | MB-27 | Token ghp_Y6Z3... visible in recording-library + debugger-tool URLs | Rotate token immediately |
| MacBook-GREEN disk at 96% | GREEN | 850GB/926GB — risk of disk full failure | Run disk-cleanup |

## MEDIUM Risk
| Risk | Machine | Impact | Action |
|---|---|---|---|
| debugger-tool 2 unpushed commits | MB-27 | Law firm case presentation + Fireflies fix only local | Push Branch2 |
| phoenix-tam-engine uncommitted changes | Mac mini | dedup.py changes only in working dir | Commit or stash |
| blank-canvas untracked db-export/ | MB-27 | Database export sitting outside git | Add to .gitignore or commit |
| Pipeline not wired end-to-end | MB-27 | Sheets→Supabase and Supabase→Salesfinity not connected | Wire middle layer |
| Two credential vaults | MB-27 + Mac mini | keys-and-credentials vs ewing-connectors — risk of drift | Merge into one |
| Two GitHub accounts | All | Repos split, auth inconsistent | Consolidate to one account |

## LOW Risk
| Risk | Machine | Impact | Action |
|---|---|---|---|
| nyc-war-story modified | MB-27 | Uncommitted index.html change | Commit or discard |
| Dead Supabase refs | All | iwcvaowfogpffdllqtld still referenced | Remove all references |
| 3 recording transcriptions remaining | MB-27 | 20/23 done, 3 left | Complete transcription |
| SpokePhone blocked | MB-27 | No API credentials | Obtain credentials |
| Disabled scheduled tasks | GREEN + Cowork | 6 tasks defined but not running | Activate or delete |
