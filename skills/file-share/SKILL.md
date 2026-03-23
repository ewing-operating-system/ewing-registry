---
name: file-share
description: "Send files, text, or documents to the Hovering Cloud shared clipboard so all connected Macs can instantly access them. Also installs or updates the Hovering Cloud app. Use this skill whenever the user says 'file share', 'share this', 'put this in the cloud', 'send to cloud', 'hovering cloud', 'output to cloud', 'share across machines', 'send to my other Mac', 'push to cloud', or asks to make any file, document, or output available to their other computers. Also trigger when the user says 'install hovering cloud', 'update hovering cloud', 'set up file sharing', or references sharing files between their Macs. If the user says 'output using file share' or 'use file share skill' after completing a task, send the output files to the Hovering Cloud. Even if the user just mentions wanting something on another machine or accessible from other computers, this is the right skill."
---

# File Share — Hovering Cloud Integration

This skill connects Claude to Ewing's Hovering Cloud app — a floating shared clipboard that runs across all his Macs on the same Wi-Fi. Files and text sent to the cloud are instantly visible and downloadable from any connected machine.

## What This Skill Does

Two modes:

### Mode 1: Send files/text to the cloud
When the user completes a task and wants the output shared across machines, or explicitly asks to share something, send it to the running Hovering Cloud server.

### Mode 2: Install or update the app
When the user asks to install, update, or set up Hovering Cloud on a machine.

## How It Works

### Detecting the Running Server

The Hovering Cloud server writes its port to `~/.hovering-cloud/port` on startup. Read that file to get the current port, then hit `http://127.0.0.1:{port}/items` to confirm it's alive.

```bash
PORT=$(cat ~/.hovering-cloud/port 2>/dev/null)
```

If the file doesn't exist or the server doesn't respond, the app isn't running. Tell the user and offer to install/launch it.

### Sending a File to the Cloud

Use curl to POST to the local server's `/upload` endpoint:

```bash
curl -s -F "file=@/path/to/file" -F "author=$(hostname)" http://127.0.0.1:${PORT}/upload
```

The file is now instantly visible on every connected Mac's Hovering Cloud panel.

### Sending Text to the Cloud

POST JSON to the `/paste` endpoint:

```bash
curl -s -X POST http://127.0.0.1:${PORT}/paste \
  -H "Content-Type: application/json" \
  -d '{"type":"text","data":"the text content","name":"Description of clip","author":"'$(hostname)'"}'
```

### Sending Multiple Files

Loop through files and upload each one. The skill script at `scripts/send-to-cloud.sh` handles this automatically.

### Checking What's in the Cloud

```bash
curl -s http://127.0.0.1:${PORT}/items | python3 -m json.tool
```

### Installing or Updating

The app source lives at `~/Downloads/hovering-cloud/`. The install script handles everything:

```bash
bash ~/Downloads/hovering-cloud/install.sh
```

If the source folder doesn't exist, tell the user they need the hovering-cloud folder first. If they're on a different Mac, they need to copy it from the machine that has it (via AirDrop, USB, or the cloud itself once one machine is running).

## Workflow: "Output using file share"

When the user says something like "do X and output using file share" or "share that with file share":

1. Complete the task normally (create the file, generate the document, etc.)
2. Save the output to a temp location or the user's working directory
3. Read the port from `~/.hovering-cloud/port`
4. Upload the file(s) using the send-to-cloud script
5. Confirm to the user what was shared and how many devices can see it

## Workflow: "Install hovering cloud"

1. Check if `~/Downloads/hovering-cloud/` exists
2. If yes: run `bash ~/Downloads/hovering-cloud/install.sh`
3. If no: tell the user they need the source folder

## Error Handling

- **Port file missing**: "Hovering Cloud isn't running. Want me to launch it?"
- **Server not responding**: "Hovering Cloud server isn't responding. It may have crashed. Want me to restart it?"
- **Upload fails with 413**: "The cloud is full (200MB limit). Delete some items first."
- **File too large**: Warn the user before attempting upload if the file is over 50MB.

## Important Notes

- Files uploaded to the cloud live on the machine that uploaded them. Other machines fetch them over the LAN when requested.
- Only the author (the hostname that uploaded) can delete items.
- The cloud has a 200MB capacity per machine.
- All machines must be on the same Wi-Fi network.
