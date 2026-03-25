---
name: password-migration
description: "Password manager import/export tool. Migrates passwords from any source manager (Keeper, LastPass, Dashlane, Bitwarden, Chrome, Firefox) into 1Password. Full pipeline: discover exports, parse, clean, deduplicate, convert format, and deliver a ready-to-import CSV. Built from a real Keeper-to-1Password migration of 1,200 entries down to 803 clean records."
---

# Password Migration Skill

Migrate passwords from any source manager into 1Password through a complete pipeline: discover exports, parse, clean, deduplicate, convert format, and deliver a ready-to-import CSV with a summary report.

## Project Record

This skill was built from a real completed migration (Keeper -> 1Password, March 2026). The reference implementation processed 1,200+ raw Keeper entries down to 803 clean deduplicated records. Active effort was ~3-4 hours. The proven Python pipeline is bundled at `scripts/convert_to_1password.py`.

---

## How This Works

The migration has two sides: what Claude handles automatically, and what the user must do themselves (because password managers require authenticated human interaction).

### What Claude Does

1. **Discovery** — Search the user's computer for password export files (CSV, JSON, .1pif, .pif, .xml) from any manager. Common locations: Downloads, Desktop, Documents, Google Drive, iCloud Drive.

2. **Consolidation** — Collect all found files into a single working folder (default: `Password Migration/` in user's Drive or Documents).

3. **Parsing & Cleaning** — Detect the source manager's format and parse it. Fix garbled/misaligned rows, strip empty entries, clean URLs (remove tracking params, normalize schemes).

4. **Deduplication** — Two-phase dedup:
   - Phase 1: Exact match on `title + login + domain` (keeps most complete version)
   - Phase 2: Same `login + password + domain` with different titles (keeps best title)

5. **Type Detection** — Classify entries as Login, Credit Card, Identity, SSN, Driver License, or Secure Note based on custom field labels, title patterns, and data shape.

6. **Format Conversion** — Output a clean CSV with 1Password's columns:
   ```
   Title, Website, Username, Password, Notes, Type
   ```
   Folder paths, shared folder info, and custom fields are preserved in the Notes column.

7. **Summary Report** — Generate `import_summary.txt` with:
   - Total entry count
   - Breakdown by type
   - Entries missing passwords (flagged for review)
   - Top domains (helps spot duplicates)
   - Step-by-step import instructions

### Running the Conversion

Use the bundled script for the heavy lifting:

```bash
python3 scripts/convert_to_1password.py \
  --input "/path/to/export.csv" \
  --source keeper \
  --output-dir "/path/to/Password Migration"
```

Supported `--source` values: `keeper`, `lastpass`, `dashlane`, `bitwarden`, `chrome`, `firefox`, `generic`

If the source format isn't recognized, use `--source generic` and the script will attempt auto-detection from headers.

The script produces:
- `1password_final_import.csv` — the file to upload
- `import_summary.txt` — the report

---

## What the User MUST Do Themselves

These steps require human authentication and cannot be performed by Claude. Present these clearly to the user at the appropriate stage.

### Before Claude Can Help

**Step 1: Export from your current password manager**

You need to log into your password manager and download the export yourself. Claude cannot access your vault.

| Manager | How to Export |
|---------|--------------|
| Keeper | Web Vault -> Settings -> Export -> CSV |
| LastPass | Vault -> Advanced Options -> Export -> CSV |
| Dashlane | Settings -> Export Data -> CSV |
| Bitwarden | Tools -> Export Vault -> CSV |
| Chrome | Settings -> Passwords -> Export passwords |
| Firefox | Logins & Passwords -> ... menu -> Export Logins |

Save the export file somewhere Claude can find it (Downloads folder is fine). Then tell Claude where it is.

### After Claude Delivers the Import File

**Step 2: Upload to 1Password**
1. Go to [my.1password.com/import](https://my.1password.com/import)
2. Select **"CSV File"** or **"Other"** as the import source
3. Upload the `1password_final_import.csv` file Claude created

**Step 3: Map columns during import**

When 1Password asks you to map columns:
- Column 1 (Title) -> Title
- Column 2 (Website) -> Website
- Column 3 (Username) -> Username
- Column 4 (Password) -> Password
- Column 5 (Notes) -> Notes
- Column 6 (Type) -> Tag (or skip)

**Step 4: Select your vault** — Choose which vault to import into (Personal, Private, Shared, etc.)

**Step 5: Confirm the import** — Review the preview and click Import

**Step 6: Post-import cleanup**
- Credit Card, Identity, SSN, and Driver License items import as Login type (1Password CSV import limitation). Their structured data is preserved in Notes.
- Check the import summary for the list of non-Login items and manually convert them to the correct type in 1Password.

**Step 7: Security cleanup**
- Securely delete ALL export CSV files from Downloads and anywhere else. They contain your passwords in plaintext.
- Empty your trash after deleting.
- Consider clearing your terminal/shell history if file paths appeared there.

**Step 8: Cancel your old password manager** — Once you've verified everything imported correctly, cancel your old subscription.

---

## Source Format Detection

Each password manager exports differently. Here's what the script looks for:

| Manager | Key Headers / Signals |
|---------|----------------------|
| Keeper | Columns: Folder, Title, Login, Password, Website URL, Notes, Shared Folder, Custom Fields (paired label+value columns) |
| LastPass | Columns: url, username, password, totp, extra, name, grouping, fav |
| Dashlane | Columns: title, url, login, password, note, category, otpSecret |
| Bitwarden | Columns: folder, favorite, type, name, login_uri, login_username, login_password, login_totp, notes, fields |
| Chrome | Columns: name, url, username, password |
| Firefox | Columns: url, username, password, httpRealm, formActionOrigin, guid, timeCreated |

---

## Edge Cases the Script Handles

These come from real-world experience with messy exports:

- **Garbled rows** — Multi-line notes that break CSV parsing. The script detects orphan rows and reattaches them.
- **Duplicate entries across shared folders** — Same credential appearing in personal vault AND shared folder. Dedup catches these.
- **Entries with no useful data** — Title only, no login/password/URL/notes. Stripped out.
- **Non-URL values in URL field** — Things like "Login" or "N/A" in the website column. Cleaned to empty.
- **Custom fields** — Keeper puts credit card numbers, SSNs, etc. in paired custom field columns. These are preserved in the Notes field with their labels.
- **Encoding issues** — UTF-8 BOM handling for files exported from Windows.

---

## Workflow Sequence

Here's the recommended order of operations when a user asks for help migrating:

1. Ask what password manager they're migrating FROM (if not obvious)
2. Tell them to export their vault (give them the specific steps for their manager)
3. Once they have the export file, search for it and any other password-related files on their machine
4. Consolidate everything into a working folder
5. Run the conversion script
6. Present the summary report to the user
7. Give them the "Steps YOU Must Complete" checklist
8. Offer to move the working folder to a "Completed" location when they confirm the import worked
