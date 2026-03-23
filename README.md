# ewing-registry

Central skill registry for all ClawdBots and Claude sessions.

## Usage

### Pull latest skills to any machine
```bash
cd ~/ewing-registry && git pull origin main
cp -r ~/ewing-registry/skills/* ~/.claude/skills/
```

### Or use the skill-sync skill
Just say "skill sync" in any Claude session.

## Structure
```
ewing-registry/
├── skills/          # All Claude skills (one folder per skill)
├── debriefs/        # End-of-session debrief reports
├── stories/         # Thread narratives (from storyteller skill)
├── audits/          # System and thread audits
└── README.md
```

## Skills
| Skill | Purpose |
|---|---|
| cold-call-workflow | Daily sales workflow orchestrator |
| debrief | End-of-session harvester and documenter |
| disk-cleanup | macOS disk space management |
| ewing-connectors | API key and credential store |
| finance-agent | Personal finance command center |
| password-migration | Password manager migration tool |
| prompt-refiner | Restructure messy prompts |
| recording-collector | Audio/video recording cataloger |
| skill-sync | Bidirectional GitHub ↔ local skill sync |
| storyteller | Thread narrative and CTO audit |
| system-auditor | Rotating system health checks |
