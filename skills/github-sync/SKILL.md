---
name: github-sync
description: "Pull all skills from GitHub to this machine and install them. Trigger whenever Ewing says 'load github', 'sync github', 'pull skills', 'sync skills', 'update skills', 'get my skills', 'load my skills from github', 'refresh skills', or any request to pull the latest skill versions from the ewing-registry repo. Also trigger after creating or editing any skill — offer to push the changes back to the repo so all machines stay in sync. This skill exists because Ewing uses up to 3 machines per day and needs identical skill sets everywhere without manual copying."
---

# GitHub Sync

This skill keeps all of Ewing's machines running the same skill set by syncing with a central GitHub repo.

## The Repo

- **URL:** https://github.com/ewing-operating-system/ewing-registry
- **Branch:** main
- **Skills location in repo:** `skills/` directory at root
- **Local install location:** `~/.claude/skills/`

## PULL — "load github" / "sync skills" / "pull skills"

When Ewing says any of the trigger phrases, run this single command:

```bash
cd ~/ewing-registry && git pull origin main 2>/dev/null || git clone https://github.com/ewing-operating-system/ewing-registry.git ~/ewing-registry; cp -r ~/ewing-registry/skills/* ~/.claude/skills/ && echo "$(ls ~/ewing-registry/skills/ | wc -l) skills synced from GitHub"
```

That's it. One command. It pulls if the repo exists, clones if it doesn't, then copies all skills into place.

After running, confirm with: "[N] skills synced from GitHub." Nothing else.

## PUSH — after creating or editing a skill

When any skill is created or modified (by skill-creator, by hand, or by any other process), offer to push it back to the repo:

```bash
cp -r ~/.claude/skills/[skill-name] ~/ewing-registry/skills/[skill-name] && cd ~/ewing-registry && git add -A && git commit -m "Update [skill-name]: [one-line summary of change]" && git push origin main
```

If the push fails due to auth, tell Ewing:

Push failed — GitHub auth not configured on this machine.

Paste this to set it up:
___
git config --global credential.helper store
___

Then paste the push command again.

Do not troubleshoot further. If credential.helper store doesn't fix it, Ewing will handle auth manually or use a different machine.

## When to push vs. not push

- Skill was created or edited → offer to push
- Skill was temporarily modified for testing → don't push
- Ewing says "don't push" or "local only" → don't push
- Ewing says "push" or "save to github" or "sync back" → push immediately

## Environment awareness

This skill works on any machine — Mac Mini, MacBook Pro, or Cowork VM. The only difference:

- **Mac Mini / MacBook Pro:** Full push and pull. Git is installed, SSH or HTTPS auth is configured.
- **Cowork VM:** Pull only. Cowork VMs are ephemeral — pushing from them would require token auth setup each time, which isn't worth it. If Ewing edits a skill in Cowork and wants to save it, save the file to outputs and tell him to push from a Mac.

## What this skill does NOT do

- It does not resolve merge conflicts. If git pull fails due to conflicts, tell Ewing "merge conflict" and give him `cd ~/ewing-registry && git stash && git pull origin main && git stash pop` to try. If that doesn't work, tell him to handle it manually.
- It does not delete local skills that were removed from the repo. It only adds and updates.
- It does not run at session start automatically. That's skill-loader's job — skill-loader loads skills from the local `~/.claude/skills/` directory. This skill syncs GitHub → local when Ewing asks for it.
