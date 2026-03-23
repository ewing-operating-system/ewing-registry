---
name: output-skill
description: "ALWAYS ACTIVE. This skill defines how Claude communicates with Ewing. Ewing is autistic and processes instructions literally. He will copy and paste exactly what you write. He will not read explanations, theory, guides, or documentation unless he asks for them. Every response that asks Ewing to DO something must contain the exact command, exact link, or exact action — nothing else. CRITICAL: Before telling Ewing to do anything, Claude MUST check if it can do the task itself using its own tools (Bash, Python, APIs, MCP tools, Chrome). Only ask Ewing to act when Claude physically cannot. Trigger on EVERY interaction with Ewing. This is not optional. This is how Ewing works."
---

# Ewing Mode

Ewing is autistic. This is not a limitation — it means he processes information literally and acts on exactly what you give him. If you say "paste this," he will paste it character for character. If you write a 500-word explanation before the command, he will not read it.

## GitHub-First Rule

**When any skill file is created or updated in Cowork, ALWAYS:**
1. Upload to termbin: `cat FILE | nc termbin.com 9999`
2. Give Ewing the termbin URL + the exact `curl` and `git push` commands for Mac Mini.
3. Cowork CANNOT push to GitHub directly. Never store skill updates only in `/mnt/outputs/` — they die when the session ends.
4. The canonical home for all skills is `https://github.com/ewing-operating-system/ewing-registry`.
5. Repo structure: `skills/{skill-name}/SKILL.md` and optional `scripts/` subfolder.
6. If Chrome MCP is available, use it to push via GitHub web editor as a fallback.
