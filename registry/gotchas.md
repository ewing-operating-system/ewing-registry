# Gotcha Library — Platform Bugs, API Limits, and Unexpected Behaviors
# Every debrief adds to this file. Check here BEFORE any batch operation.
# Updated: 2026-03-23

## Supabase
| Gotcha | Impact | Fix |
|---|---|---|
| REST API returns max 1,000 rows by default | Queries silently cap at 1000. Round numbers in results are suspicious. | Always paginate. Use `range()` or check total count first. |
| Service role key needed for RLS bypass | Anon key respects row-level security. Batch operations fail silently. | Use service role key for admin/batch operations. |

## Salesfinity API
| Gotcha | Impact | Fix |
|---|---|---|
| 413 Payload Too Large on bulk uploads | API silently drops records over ~500 per batch | Chunk uploads into batches of 200-300 |
| 404 on add-contacts endpoint | Endpoint changed or requires different auth | Check current API docs, use correct endpoint |
| Notes field character limit unknown | Long call notes may get truncated | Test with a long note first, find the limit |

## Claude / Context
| Gotcha | Impact | Fix |
|---|---|---|
| Context collapse after ~200K tokens | Claude summarizes instead of investigating. Substitutes memory for observation. | Spawn fresh thread for investigation tasks. Re-query, never trust memory. |
| Context compaction loses the HOW | After compaction, WHAT survives but process/method/error details die | Save exact error messages and command sequences to external files before compaction |
| Subagent may refuse harvester-style tasks | Security system flags credential scanning as injection attack | Run harvest in main thread, not subagent |
| Cowork VMs have no Slack canvas write access | slack_update_canvas unavailable on any Cowork session tested | Use GitHub push instead. Slack is read-only from Cowork. |
| Plugin/MCP availability varies by Cowork session | Different VMs get different plugins and MCP tools randomly | Check available tools at session start. Don't assume consistency. |

## Google Drive
| Gotcha | Impact | Fix |
|---|---|---|
| FUSE mount scans timeout on large drives | `find` on Google Drive paths hangs or takes 10+ minutes | Use targeted paths, not broad `find` across Google Drive |
| Multiple drives mount at ~/Library/CloudStorage/ | Paths include account email in folder name | Scan CloudStorage for all mounted drives, don't assume one |

## Git
| Gotcha | Impact | Fix |
|---|---|---|
| SSH vs HTTPS auth mismatch between machines | Mac mini uses HTTPS (clawdking1-GH), MB-27 uses SSH (ewing-operating-system) | Pick one. SSH is more reliable for automated push. |
| PAT exposed in git remote URLs | recording-library and debugger-tool have ghp_ token in remote | Rotate the token. Use credential helper instead of URL-embedded tokens. |

## macOS
| Gotcha | Impact | Fix |
|---|---|---|
| Different iCloud accounts break AirDrop/Handoff | Mac mini on clawdking1@gmail.com can't AirDrop to ewing.gillaspy@gmail.com machines | Fix iCloud account or use git/SSH for file transfer |
