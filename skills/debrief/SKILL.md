---
name: debrief
description: "End-of-thread intelligence extraction. Combines harvester (machine scan) + storyteller (conversation analysis) into one zero-config command. Scans the machine, reads the full conversation, writes the narrative + audit + harvest, and pushes everything to the ewing-registry GitHub repo. Run this before closing ANY significant thread. Trigger when Ewing says 'debrief', 'debrief this thread', 'wrap up', 'close out', 'end of thread', 'save everything', 'before we close', 'capture this session', or any indication that a thread is ending and work should be preserved."
---

# Debrief — End-of-Thread Intelligence Extraction

You are the thread closer. When triggered, you produce THREE outputs and push them all to the ewing-registry GitHub repo. Zero questions. Zero config.

## GitHub-First Rule

**When any skill file is created or updated in Cowork, ALWAYS:**
1. Upload to termbin: `cat FILE | nc termbin.com 9999`
2. Give Ewing the termbin URL + the exact `curl` and `git push` commands for Mac Mini.
3. Cowork CANNOT push to GitHub directly. Never store skill updates only in `/mnt/outputs/` — they die when the session ends.
4. The canonical home for all skills is `https://github.com/ewing-operating-system/ewing-registry`.
5. Repo structure: `skills/{skill-name}/SKILL.md` and optional `scripts/` subfolder.
6. If Chrome MCP is available, use it to push via GitHub web editor as a fallback.
