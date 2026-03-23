# Lovable Site Spec: Recording Catalog

## Overview

A single-page application that displays all of Ewing's recordings in a searchable, filterable grid. Built with Lovable (React + Tailwind + Supabase).

---

## Data Source

The site reads from `recording-catalog.json`. On initial build, the JSON is imported into a Supabase table. Daily updates push incremental changes.

### Supabase Tables

**recordings**
- All fields from the catalog entry schema
- `participants` stored as JSONB
- `key_questions` stored as JSONB
- `deal_details` stored as JSONB
- `segments` stored as JSONB

---

## Pages

### 1. Main Dashboard (`/`)

**Header**
- Title: "Recording Catalog"
- Subtitle: total count, total storage, date range
- Search bar (full-text across filename, participants, summary, questions)

**Filter Bar** (horizontal, sticky below header)
- Source app: multi-select chips (Zoom, Fireflies, iMovie, Voice Memos, Screen Recording, etc.)
- Media type: Video | Audio | All
- Sales opportunity: Yes | No | All
- Date range picker
- Sort by: Date (newest first default), Duration, Size, Name

**Recording Grid**
- Responsive grid: 3 columns on desktop, 2 on tablet, 1 on mobile
- Each tile is a RecordingCard component (see below)
- Infinite scroll or paginate at 30 items

---

## Components

### RecordingCard

A card representing one recording. Displays summary info and expands on click.

**Collapsed state (card face):**
```
+----------------------------------------------+
|  [Thumbnail / Audio Waveform Icon]           |
|  Filename (truncated)                        |
|  Duration  |  Size  |  Date                  |
|  Source badge (e.g., "Zoom", "Fireflies")    |
|  [Sales $] indicator if is_sales_opportunity |
|  Participant avatars (initials, max 4)       |
+----------------------------------------------+
```

**Expanded state (modal or drawer):**

#### Media Player Section
- **Video**: Embedded `<video>` player with controls. Source is the file path served via a local file server or Supabase storage.
- **Audio**: Embedded `<audio>` player with waveform visualization (use wavesurfer.js or similar).
- Playback speed controls: 1x, 1.25x, 1.5x, 2x

#### Metadata Section
- Filename (full)
- Path (clickable to reveal in Finder via `file://` link)
- Duration, size, created date, modified date
- Source app with icon
- Multi-meeting badge if applicable

#### Participants Section
- List of participant cards:
  ```
  [Initials Avatar]  Name
                     Title at Company
                     [LinkedIn icon -> search URL]
                     Confidence: high/medium/low
                     Notes: "clues text"
  ```
- If `participant_notes` exists, show in an info callout

#### Key Questions Section
- Accordion list, each item:
  ```
  Q: "Question text"
  Asked by: Name  |  Answered by: Name
  Duration: Xm Ys
  Answer: "Summary text"
  ```

#### Sales Opportunity Section (only if `is_sales_opportunity`)
- Highlighted section with dollar-sign accent color
- Display any pre-filled deal details from the catalog
- **Compensation Calculator** (interactive):
  ```
  Fee %:        [___________]  (editable input, default from catalog or empty)
  Deal Value:   [___________]  (editable input)
  LP Raise:     [___________]  (editable input)
  ─────────────────────────────
  Est. Comp:    $XX,XXX        (auto-calculated: fee% * deal_value)
  ```
- "Save" button to persist edits back to catalog
- Notes field (pre-filled from catalog, editable)

#### Multi-Meeting Section (only if `multi_meeting`)
- Tab interface, one tab per segment
- Each tab shows its own participants, summary, questions, sales data
- Timeline bar showing segment boundaries on the full recording

#### Duplicate Paths Section (only if duplicates exist)
- Collapsible list of all paths where this file exists
- Total wasted space calculation

---

### FilterChip

Small pill-shaped toggle for filter values. Active state has filled background.

### SearchBar

- Debounced search (300ms)
- Searches across: filename, participant names, summary text, question text, notes
- Highlights matching text in results

### CompensationCalculator

Reusable component for the sales opportunity section.

Props:
- `feePercentage: number | null`
- `dealValue: number | null`
- `lpRaiseAmount: number | null`
- `onSave: (values) => void`

Behavior:
- All three fields are editable number inputs with currency/percentage formatting
- `estimatedCompensation` = `feePercentage / 100 * dealValue`
- Updates in real time as user types
- Save button persists to Supabase and updates local state

### StatsBar

Top-of-page summary strip:
```
[Total Recordings: 67]  [Total Size: 142 GB]  [Sales Opportunities: 8]  [Pending Transcription: 12]
```

---

## Styling

- **Theme**: Dark mode default with light mode toggle
- **Accent color**: Indigo (#6366F1) for primary actions, Amber (#F59E0B) for sales opportunity highlights
- **Font**: Inter or system font stack
- **Cards**: Rounded corners (lg), subtle shadow, hover lift effect
- **Source badges**: Color-coded by app (Zoom = blue, Fireflies = orange, iMovie = purple, Voice Memos = red, Screen Recording = green)

---

## File Serving

For local development / demo:
- Serve media files via a simple Express/Python HTTP server that maps file paths
- Endpoint: `GET /media?path=<encoded_absolute_path>`
- The server reads the file from disk and streams it with appropriate Content-Type

For production:
- Large files stay local; the site is a local-first tool
- Optionally upload smaller files (< 500 MB) to Supabase storage for remote access

---

## Tech Stack

- **Framework**: React 18 + TypeScript (via Lovable)
- **Styling**: Tailwind CSS
- **State**: React Query for data fetching, Zustand for UI state
- **Database**: Supabase (PostgreSQL)
- **Media**: Native HTML5 video/audio elements, wavesurfer.js for audio waveforms
- **Search**: Client-side fuzzy search (fuse.js) for < 500 recordings, Supabase full-text search for larger catalogs

---

## API Endpoints (Supabase Edge Functions or local server)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/recordings` | List all recordings (supports filters, pagination) |
| GET | `/api/recordings/:id` | Get single recording with full details |
| PATCH | `/api/recordings/:id/deal` | Update deal_details for a recording |
| GET | `/api/stats` | Dashboard statistics |
| POST | `/api/sync` | Trigger incremental catalog sync |
| GET | `/media` | Stream media file from local path |

---

## Deployment

1. Use Lovable to scaffold the project
2. Connect to a Supabase project for persistence
3. Import `recording-catalog.json` as seed data
4. Deploy via Lovable's built-in hosting
5. For media playback, run the local file server on Ewing's Mac

---

## Future Enhancements

- Drag-and-drop to manually add recordings
- Bulk tagging (e.g., tag multiple recordings as "Q1 2026 pipeline")
- Export sales opportunities to a CRM-ready CSV
- Auto-link Fireflies transcripts via the Fireflies MCP tool
- Calendar integration: match recordings to Google Calendar events by date/time
