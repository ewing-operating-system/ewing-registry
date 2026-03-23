# Supabase Instances

## Live
| Instance ID | Purpose | Region | Referenced By | Tables |
|---|---|---|---|---|
| rdnnhxhohwjucvjwbwch | AND Call Command CRM + Exa enrichment | West US / us-east-1 | ewing-connectors, exa-enrichment, debugger-tool, .env files, MB-27 scheduled tasks | 14 tables, 1,844 persons |
| ginqabezgxaazkhuuvvw | ewing-operating-system's Project | East US | clawdbot-creator | Unknown |
| asavljgcnresdnadblse | Phoenix TAM Engine / OpenClaw / mission-control | Unknown | clawdbot-creator, mission-control (Mac mini) | Unknown |
| lhmuwrlpcdlzpfthrodm | ColdCall Universe pipeline | Unknown | Supabase CLI on MB-27 | Unknown |

## Dead
| Instance ID | Purpose | Status |
|---|---|---|
| iwcvaowfogpffdllqtld | debugger-tool (old) | DEAD — remove all references |

## Overlap Warning
`rdnnhxhohwjucvjwbwch` is referenced as BOTH "and-call-command" AND "Exa enrichment" — confirm whether this is one DB serving both purposes or if they should be separated.

## Known Schema (rdnnhxhohwjucvjwbwch)
Tables: companies, persons, phone_numbers, call_log, lists, list_assignments, reps, comp_plans + others (14 total)
