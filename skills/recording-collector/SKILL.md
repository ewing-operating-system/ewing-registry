---
name: recording-collector
description: "Audio/video recording catalog scanner. Scans Ewing's Mac for all audio and video recordings scattered across folders, catalogs them with metadata, transcribes content, and displays everything on a Lovable-hosted site. Turns a disorganized collection of recordings into a searchable, browsable inventory with transcripts and contextual information for each file."
version: 1.0.0
triggers:
  - collect recordings
  - scan recordings
  - catalog recordings
  - find my recordings
  - recording inventory
  - update recording catalog
---

# Recording Collector Skill

Finds every audio/video recording on Ewing's Mac, deduplicates, extracts metadata, transcribes audio, identifies participants, flags sales opportunities, and pushes the catalog to a Lovable site for browsing.

---

## Step 1: Scan & Discover

Run a filesystem scan across all known recording locations. Use `find` with the file extensions listed below.

### Locations to scan

| Priority | Path | What lives there |
|----------|------|------------------|
| 1 | `~/Desktop/Desktop Cleanup/` | Screen recordings, pitches, demos (40+ files, some 24 GB) |
| 2 | `~/Downloads/` | Fireflies recordings, meeting recordings (~10 files) |
| 3 | `~/Documents/Zoom/` | Zoom meeting recordings (~8 files) |
| 4 | `~/Library/CloudStorage/GoogleDrive-ewing@chapter.guide/` | Business recordings |
| 5 | `~/Movies/iMovie Library.imovielibrary/` | iMovie projects with source media |
| 6 | `~/Library/Group Containers/` | Notes recordings, Voice Memos |
| 7 | `~/My Drive (ewing@engram.nexus)/` | Some recordings |
| 8 | `~/My Drive (ewing@chapter.guide)/` | PEC evidence recordings, pitch videos |

### File extensions

```
.mp4 .mp3 .m4a .mov .wav .caf .webm .m4v .aac .MOV
```

### Scan command template

```bash
SCAN_DIRS=(
  "$HOME/Desktop/Desktop Cleanup"
  "$HOME/Downloads"
  "$HOME/Documents/Zoom"
  "$HOME/Library/CloudStorage/GoogleDrive-ewing@chapter.guide"
  "$HOME/Movies/iMovie Library.imovielibrary"
  "$HOME/Library/Group Containers"
  "$HOME/My Drive (ewing@engram.nexus)"
  "$HOME/My Drive (ewing@chapter.guide)"
)

EXTENSIONS=(-name "*.mp4" -o -name "*.mp3" -o -name "*.m4a" -o -name "*.mov" -o -name "*.wav" -o -name "*.caf" -o -name "*.webm" -o -name "*.m4v" -o -name "*.aac" -o -name "*.MOV")

for dir in "${SCAN_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    find "$dir" -type f \( "${EXTENSIONS[@]}" \) -exec stat -f '%N|%z|%Sm|%SB' -t '%Y-%m-%dT%H:%M:%S' {} \;
  fi
done
```

This outputs: `path|size_bytes|modified_date|birth_date` per file.

---

## Step 2: Deduplicate

Deduplicate by `(basename, size_bytes)`. When duplicates exist:
- Keep the copy closest to the source app (e.g., prefer `~/Documents/Zoom/` over `~/Downloads/` for Zoom recordings).
- Record all paths in `duplicate_paths` so the user can clean up later.

---

## Step 3: Build Catalog Entry

For each unique recording, create a JSON object matching the schema in `data/recording-catalog.json`.

### Detect source app

Infer the source application from path and filename patterns:

| Pattern | Source |
|---------|--------|
| Path contains `Zoom` | Zoom |
| Filename starts with `GMT` or contains `fireflies` | Fireflies |
| Path contains `iMovie` | iMovie |
| Path contains `Voice Memos` or ext `.caf` | Voice Memos |
| Path contains `Notes` and in Group Containers | Apple Notes |
| Filename contains `Screen Recording` | macOS Screen Recording |
| Path contains `PEC` or `pitch` (case-insensitive) | Pitch / PEC Evidence |
| Otherwise | Unknown |

### Get duration

```bash
# Requires ffprobe (from ffmpeg)
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$filepath"
```

If ffprobe is not installed, note duration as `null` and flag for manual review.

---

## Step 4: Process Recordings

### 4a. Video files (MP4, MOV, M4V, WEBM)

1. **Generate thumbnail** at the 10-second mark (or 25% if shorter than 40s):
   ```bash
   ffmpeg -i "$filepath" -ss 10 -vframes 1 -q:v 2 "$output_dir/thumb_${id}.jpg"
   ```
2. **Store the original path** as the playback source. Do NOT copy or re-encode large files.
3. Mark `media_type: "video"`.

### 4b. Audio files (MP3, M4A, WAV, AAC, CAF)

1. **Transcribe** using superwhisper CLI if available, otherwise fall back to whisper:
   ```bash
   # Check availability
   which superwhisper || which whisper

   # superwhisper
   superwhisper transcribe "$filepath" --output-format json

   # whisper fallback
   whisper "$filepath" --model base --output_format json --output_dir "$output_dir"
   ```
2. If neither is available, flag `transcription_status: "pending"` and skip.
3. **Generate 50-word summary** from the transcript using Claude.
4. Mark `media_type: "audio"`.

### 4c. Multi-meeting detection (CRITICAL)

After transcription, analyze for signs that a single file contains multiple meetings:

- **Audio gap** > 30 seconds of silence
- **Participant change**: different speakers/names appear suddenly
- **Context shift**: topic changes dramatically with greetings/introductions

Detection via ffmpeg silence detection:
```bash
ffmpeg -i "$filepath" -af silencedetect=noise=-30dB:d=30 -f null - 2>&1 | grep "silence_start\|silence_end"
```

If multi-meeting is detected:
1. Set `multi_meeting: true`
2. Create `segments[]` array with start/end timestamps
3. Process each segment as its own sub-entry with separate participants, summary, and sales flags
4. Link segments back to the parent recording via `parent_recording_id`

---

## Step 5: Extract Participant & Content Data

For each recording (or segment if multi-meeting), extract:

### 5a. Participants

- **Names**: Extract from transcript, filename, or Zoom/Fireflies metadata
- **Titles**: Only if clearly stated in the recording or filename
- **LinkedIn**: Only if the person's full name + company is clear enough to construct a search URL. Format: `https://www.linkedin.com/search/results/all/?keywords=FIRSTNAME+LASTNAME+COMPANY`
- **IMPORTANT**: If identity is uncertain, add to `participant_notes` with whatever clues exist (e.g., "female voice, mentioned working at a fintech startup, first name might be Sarah"). NEVER guess.

### 5b. Key questions

Find questions that took > 1 minute of discussion. For each:
- `question`: The question text
- `asked_by`: Who asked it (name or "Unknown speaker")
- `answered_by`: Who primarily answered
- `answer_summary`: 1-2 sentence summary of the final answer
- `discussion_duration_seconds`: Approximate duration

### 5c. Sales opportunity detection

Flag as a sales opportunity if any of these appear:
- Discussion of fees, compensation, percentages, deal structure
- LP raise amounts, fund sizes, capital commitments
- Placement agent or broker-dealer language
- Explicit mention of a potential deal

If flagged:
```json
{
  "is_sales_opportunity": true,
  "deal_details": {
    "fee_percentage": null,
    "deal_value": null,
    "lp_raise_amount": null,
    "estimated_compensation": null,
    "notes": "string describing what was discussed"
  }
}
```

Leave numeric fields as `null` if not explicitly stated. The Lovable site provides a calculator for the user to fill in.

---

## Step 6: Write Catalog

Write the full catalog to:

```
~/.claude/skills/recording-collector/data/recording-catalog.json
```

Also write a summary report:

```
~/.claude/skills/recording-collector/data/scan-report-YYYY-MM-DD.md
```

The report should include:
- Total recordings found
- Duplicates detected
- Breakdown by source app
- Multi-meeting recordings flagged
- Sales opportunities detected
- Recordings pending transcription
- Total storage consumed

---

## Step 7: Generate Lovable Site

Use the spec in `references/lovable-spec.md` to build/update the Lovable site.

The site pulls data from `recording-catalog.json` and renders:
- Scrollable grid of recording tiles
- Embedded video/audio players
- Participant cards with LinkedIn links
- Key questions accordion
- Sales opportunity compensation calculator
- Search and filter controls

See `references/lovable-spec.md` for full component spec.

---

## Step 8: Schedule Daily Updates

Create a scheduled task to run this skill once daily at 6:00 AM PT:

```
Task: Re-scan all directories, find new recordings, process them, update catalog, push to Lovable site
Schedule: Daily at 6:00 AM PT
Action: Run recording-collector skill with --incremental flag
```

In incremental mode:
- Only scan for files not already in the catalog (compare by path + size)
- Process new files only
- Append to existing catalog
- Regenerate the Lovable site data

---

## Error Handling

- If a directory does not exist, skip it silently and note in the scan report.
- If ffmpeg/ffprobe is not installed, warn the user and skip thumbnail/duration extraction. Set `requires_ffmpeg: true` on affected entries.
- If whisper/superwhisper is not installed, set `transcription_status: "pending"` and continue.
- If a file is too large to process (> 10 GB), flag it as `large_file: true` and skip processing. Record path and size for manual review.
- Never delete or move original files. This skill is read-only on source media.

---

## File Locations

| File | Purpose |
|------|---------|
| `~/.claude/skills/recording-collector/SKILL.md` | This file - skill definition |
| `~/.claude/skills/recording-collector/data/recording-catalog.json` | The catalog database |
| `~/.claude/skills/recording-collector/data/scan-report-*.md` | Daily scan reports |
| `~/.claude/skills/recording-collector/references/lovable-spec.md` | Lovable site component spec |
