# The Story of Hovering Cloud
**Session:** hovering-cloud-build
**Date:** 2026-03-23
**Machine:** ClawdBots-Mac-mini-8 (Cowork)
**Duration:** ~3 hours

---

Ewing opened the thread with a vision: a floating cloud that hovered on every Mac's screen, acting as a universal drag-and-drop clipboard across all his machines. No clicking through folders. No AirDrop failures. Just drag something onto a cloud, and every other Mac sees it instantly. He called it "Hovering Cloud" — a visual virtual drop-off and retrieve folder across desktops.

He asked Claude to first load his skills, refine the prompt, and assess feasibility. Claude loaded the skill-loader (output-skill, prompt-refiner, skill-creator, tech-translator) and restructured Ewing's stream-of-consciousness feature list into a clean specification: Electron app, Express + WebSocket server, Bonjour/mDNS discovery, 200MB capacity, author-only delete, computer names as identifiers.

Feasibility: high. Claude recommended building it right there in Cowork and handing Ewing a one-liner. Ewing agreed, and the build began.

Claude created six source files from scratch — cloud.html (the floating SVG cloud with animations), main.js (Electron frameless transparent window), server.js (Express HTTP + WebSocket with file upload), discovery.js (Bonjour LAN discovery), renderer.js (frontend logic), and install-and-run.sh. The app was designed to float in the top-right corner as a translucent cloud with a badge count, expandable panel, and drag-and-drop support.

Ewing ran the installer on his Mac Mini. It worked. The cloud appeared, the server started on port 51764, mDNS began broadcasting. But macOS popped a hostname conflict — "ClawdBots-Mac-mini.local is already in use" — renaming it to ClawdBots-Mac-mini-2.local. Claude explained this was a Bonjour collision (likely dual network interfaces) and told Ewing to click OK.

Then came the debugging. Ewing showed screenshots of npm deprecation warnings and 10 vulnerabilities (5 high). Claude walked him through running npm audit in a separate terminal tab — Ewing initially pasted it into the wrong tab (the one running the app). Claude redirected him to tab 4. The audit fixed everything: 0 vulnerabilities.

Meanwhile, Ewing's OpenClaw agents were running in other tabs — "Next" (his pipeline manager for Next Chapter M&A Advisory) had processed 10 HVAC acquisition targets across Texas, and "Scout" was mid-research on those targets, 17 minutes into a web search session. Ewing showed Claude these tabs as status updates. Claude acknowledged them without interfering.

Claude then ran a full efficiency audit, finding 12 issues (grade C+). All were fixed: in-memory caching for items.json, async file I/O, stale-peer interval cleanup, conditional peer polling, WebSocket direct updates, scoped JSON parser, cached local IPs, dead code removal, exponential reconnect backoff, and string-based escapeHtml. Grade upgraded to A-.

The critical architectural flaw surfaced next. Claude audited the cross-machine sharing model and found it was fundamentally broken — every HTTP and WebSocket call was hardcoded to 127.0.0.1. Machine B could never see Machine A's files. Claude rewrote the entire renderer.js networking layer: multi-peer item fetching, origin tagging, WebSocket connections to all discovered peers, deduplication, and origin-aware download/copy/delete.

Ewing then needed the app on GitHub so his other Macs could install it. Claude created the repo at clawdking1-GH/hovering-cloud with a get.sh one-liner installer: `curl -fsSL https://raw.githubusercontent.com/clawdking1-GH/hovering-cloud/main/get.sh | bash`. This included auto-update (checks GitHub every 30 minutes), a `hovering-cloud` launch command, and a `hovering-cloud-update` force-update command.

Feature requests kept coming. Ewing wanted categorized items (text vs. documents vs. images), type-aware click actions, quick clipboard import on cloud click, and recipient tagging (tag items for specific colleagues). Claude broke this into 3 parallel agents and implemented everything: collapsible category headers with color-coded borders, image thumbnails, text previews, and a recipient selection modal.

But Ewing wasn't satisfied. He called the app "dreadful" and demanded simpler interactions: single click opens preview, double click copies, right click pastes text only. Claude stripped out the overengineered behavior and rewired everything cleanly. The copyItem function was upgraded to handle images via Electron's nativeImage clipboard.

The file-share skill was created so any Claude session could send output directly to the Hovering Cloud server. Ewing tried installing on MacBook Green (success) but MacBook 14 kept failing — permission issues and missing files. Claude built a bulletproof public installer (get.sh) that worked without GitHub authentication.

By the end, the Hovering Cloud was a real product: floating animated cloud UI, multi-peer LAN sharing, categorized items, type-aware interactions, auto-update from GitHub, and a one-command installer. Ewing had gone from a rough idea to a working cross-desktop app in a single session.

The thread ended with a debrief request — the final act of preservation before closing out.
