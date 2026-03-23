#!/usr/bin/env python3
"""
Universal Password Manager → 1Password CSV Converter

Converts exports from Keeper, LastPass, Dashlane, Bitwarden, Chrome, Firefox
into 1Password's CSV import format.

Based on a proven Keeper migration that processed 1,200+ entries into 803 clean records.

Usage:
    python3 convert_to_1password.py --input export.csv --source keeper --output-dir ./output
    python3 convert_to_1password.py --input export.csv --source generic --output-dir ./output
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse


# ─── Source Format Definitions ───────────────────────────────────────────────

SOURCE_HEADERS = {
    'keeper': {
        'title': 1, 'login': 2, 'password': 3, 'url': 4,
        'notes': 5, 'folder': 0, 'shared_folder': 6,
        'custom_fields_start': 7,  # paired label+value columns
    },
    'lastpass': {
        'url': 'url', 'username': 'username', 'password': 'password',
        'totp': 'totp', 'extra': 'extra', 'name': 'name',
        'grouping': 'grouping', 'fav': 'fav',
    },
    'dashlane': {
        'title': 'title', 'url': 'url', 'login': 'login',
        'password': 'password', 'note': 'note', 'category': 'category',
    },
    'bitwarden': {
        'folder': 'folder', 'type': 'type', 'name': 'name',
        'uri': 'login_uri', 'username': 'login_username',
        'password': 'login_password', 'totp': 'login_totp',
        'notes': 'notes', 'fields': 'fields',
    },
    'chrome': {
        'name': 'name', 'url': 'url', 'username': 'username',
        'password': 'password',
    },
    'firefox': {
        'url': 'url', 'username': 'username', 'password': 'password',
    },
}


# ─── URL Cleaning ────────────────────────────────────────────────────────────

def clean_url(url):
    """Clean and normalize a URL — strip tracking params, normalize scheme."""
    if not url:
        return ''
    url = url.strip()
    if url.lower() in ('login', 'n/a', 'none', '', 'http://', 'https://'):
        return ''
    if url and not url.startswith('http'):
        if '.' in url and ' ' not in url:
            url = 'https://' + url
        else:
            return ''
    try:
        parsed = urlparse(url)
        clean = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')
        return clean
    except Exception:
        return url


def domain_from_url(url):
    """Extract base domain from URL for dedup."""
    if not url:
        return ''
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        if host.startswith('www.'):
            host = host[4:]
        return host
    except Exception:
        return ''


# ─── Type Detection ──────────────────────────────────────────────────────────

def detect_type(record):
    """Determine the 1Password item type from record data."""
    title_lower = record.get('title', '').lower()
    notes_lower = record.get('notes', '').lower()
    custom_labels = [cf[0].lower() for cf in record.get('custom_fields', [])]

    # Credit Card
    if any('cardholder' in l or 'card number' in l or 'payment card' in l for l in custom_labels):
        return 'Credit Card'
    if 'payment card' in notes_lower:
        return 'Credit Card'

    # Driver License
    if 'driver' in title_lower and 'license' in title_lower:
        return 'Driver License'
    if any('license number' in l for l in custom_labels):
        return 'Driver License'

    # SSN
    if 'social security' in title_lower or 'ssn' in title_lower:
        return 'Social Security Number'
    if any('social security' in l or 'ssn' in l for l in custom_labels):
        return 'Social Security Number'

    # Identity
    if any('date of birth' in l or 'birth date' in l for l in custom_labels):
        return 'Identity'
    if title_lower in ('identity', 'eg personal'):
        if any(l in ('first name', 'last name', 'middle name', 'name', 'address', 'phone')
               for l in custom_labels):
            return 'Identity'

    # Secure Note
    if record.get('notes') and not record.get('login') and not record.get('password') and not record.get('url'):
        if not record.get('custom_fields'):
            return 'Secure Note'

    return 'Login'


# ─── Parsers ─────────────────────────────────────────────────────────────────

def parse_keeper(filepath):
    """Parse Keeper CSV export."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or all(c.strip() == '' for c in row):
                continue
            custom_fields = []
            i = 7
            while i + 1 < len(row):
                label = row[i].strip() if i < len(row) else ''
                value = row[i + 1].strip() if i + 1 < len(row) else ''
                if label or value:
                    custom_fields.append((label, value))
                i += 2

            records.append({
                'folder': row[0].strip() if len(row) > 0 else '',
                'title': row[1].strip() if len(row) > 1 else '',
                'login': row[2].strip() if len(row) > 2 else '',
                'password': row[3].strip() if len(row) > 3 else '',
                'url': row[4].strip() if len(row) > 4 else '',
                'notes': row[5].strip() if len(row) > 5 else '',
                'shared_folder': row[6].strip() if len(row) > 6 else '',
                'custom_fields': custom_fields,
            })
    return records


def parse_lastpass(filepath):
    """Parse LastPass CSV export."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            notes = row.get('extra', '').strip()
            grouping = row.get('grouping', '').strip()
            if grouping:
                notes = f"[LastPass Folder: {grouping}]\n{notes}".strip()
            records.append({
                'folder': grouping,
                'title': row.get('name', '').strip(),
                'login': row.get('username', '').strip(),
                'password': row.get('password', '').strip(),
                'url': row.get('url', '').strip(),
                'notes': notes,
                'shared_folder': '',
                'custom_fields': [],
            })
    return records


def parse_dashlane(filepath):
    """Parse Dashlane CSV export."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row.get('category', '').strip()
            note = row.get('note', '').strip()
            if category:
                note = f"[Dashlane Category: {category}]\n{note}".strip()
            records.append({
                'folder': category,
                'title': row.get('title', '').strip(),
                'login': row.get('login', '').strip(),
                'password': row.get('password', '').strip(),
                'url': row.get('url', '').strip(),
                'notes': note,
                'shared_folder': '',
                'custom_fields': [],
            })
    return records


def parse_bitwarden(filepath):
    """Parse Bitwarden CSV export."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            folder = row.get('folder', '').strip()
            notes = row.get('notes', '').strip()
            fields_str = row.get('fields', '').strip()
            custom_fields = []

            if fields_str:
                # Bitwarden custom fields format: "label: value, label2: value2"
                for field in fields_str.split('\n'):
                    if ':' in field:
                        label, value = field.split(':', 1)
                        custom_fields.append((label.strip(), value.strip()))

            if folder:
                notes = f"[Bitwarden Folder: {folder}]\n{notes}".strip()

            records.append({
                'folder': folder,
                'title': row.get('name', '').strip(),
                'login': row.get('login_username', '').strip(),
                'password': row.get('login_password', '').strip(),
                'url': row.get('login_uri', '').strip(),
                'notes': notes,
                'shared_folder': '',
                'custom_fields': custom_fields,
            })
    return records


def parse_chrome(filepath):
    """Parse Chrome CSV export."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'folder': '',
                'title': row.get('name', '').strip(),
                'login': row.get('username', '').strip(),
                'password': row.get('password', '').strip(),
                'url': row.get('url', '').strip(),
                'notes': '',
                'shared_folder': '',
                'custom_fields': [],
            })
    return records


def parse_firefox(filepath):
    """Parse Firefox CSV export."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get('url', '').strip()
            title = domain_from_url(url) if url else 'Unknown'
            records.append({
                'folder': '',
                'title': title,
                'login': row.get('username', '').strip(),
                'password': row.get('password', '').strip(),
                'url': url,
                'notes': '',
                'shared_folder': '',
                'custom_fields': [],
            })
    return records


def parse_generic(filepath):
    """Auto-detect format from CSV headers and parse accordingly."""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        first_row = next(reader, [])

    headers_lower = [h.strip().lower() for h in first_row]

    # Try to detect source
    if 'grouping' in headers_lower and 'fav' in headers_lower:
        return parse_lastpass(filepath)
    if 'login_uri' in headers_lower and 'login_username' in headers_lower:
        return parse_bitwarden(filepath)
    if 'otpsecret' in headers_lower or ('title' in headers_lower and 'category' in headers_lower):
        return parse_dashlane(filepath)
    if 'httpRealm' in [h.strip() for h in first_row] or 'formActionOrigin' in [h.strip() for h in first_row]:
        return parse_firefox(filepath)

    # Check if it looks like Chrome (simple: name, url, username, password)
    if set(headers_lower) == {'name', 'url', 'username', 'password'}:
        return parse_chrome(filepath)

    # Check if it's already in 1Password format
    if 'title' in headers_lower and 'website' in headers_lower:
        records = []
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append({
                    'folder': '',
                    'title': row.get('Title', row.get('title', '')).strip(),
                    'login': row.get('Username', row.get('username', '')).strip(),
                    'password': row.get('Password', row.get('password', '')).strip(),
                    'url': row.get('Website', row.get('website', row.get('URL', row.get('url', '')))).strip(),
                    'notes': row.get('Notes', row.get('notes', '')).strip(),
                    'shared_folder': '',
                    'custom_fields': [],
                })
        return records

    # If no headers match, assume Keeper-style positional format
    # (Keeper doesn't always have a header row)
    return parse_keeper(filepath)


PARSERS = {
    'keeper': parse_keeper,
    'lastpass': parse_lastpass,
    'dashlane': parse_dashlane,
    'bitwarden': parse_bitwarden,
    'chrome': parse_chrome,
    'firefox': parse_firefox,
    'generic': parse_generic,
}


# ─── Cleaning & Dedup ───────────────────────────────────────────────────────

def clean_records(records):
    """Fix garbled entries, remove junk, clean URLs."""
    cleaned = []
    for r in records:
        # Skip completely empty entries
        if not r['title'] and not r['login'] and not r['password'] and not r['url']:
            if not r.get('notes') and not any(v for _, v in r.get('custom_fields', [])):
                continue

        # Skip entries with title but absolutely no data
        if r['title'] and not r['login'] and not r['password'] and not r['url'] and not r.get('notes'):
            if not any(v for _, v in r.get('custom_fields', [])):
                continue

        r['url'] = clean_url(r['url'])
        cleaned.append(r)

    return cleaned


def deduplicate(records):
    """Two-phase deduplication, keeping the most complete version."""
    # Phase 1: Exact dedup on title + login + domain
    seen = {}
    for r in records:
        domain = domain_from_url(r['url'])
        key = (r['title'].lower().strip(), r['login'].lower().strip(), domain)

        if key in seen:
            existing = seen[key]
            existing_score = sum([
                bool(existing['password']), bool(existing.get('notes', '')),
                bool(existing['url']), len(existing.get('custom_fields', [])),
            ])
            new_score = sum([
                bool(r['password']), bool(r.get('notes', '')),
                bool(r['url']), len(r.get('custom_fields', [])),
            ])
            if new_score > existing_score:
                seen[key] = r
        else:
            seen[key] = r

    phase1 = list(seen.values())

    # Phase 2: Same login + password + domain (different titles = same account)
    seen2 = {}
    for r in phase1:
        if not r['login'] or not r['password']:
            seen2[id(r)] = r
            continue

        domain = domain_from_url(r['url'])
        key2 = (r['login'].lower().strip(), r['password'], domain)

        if key2 in seen2:
            existing = seen2[key2]
            existing_score = len(existing.get('title', '')) + len(existing.get('notes', ''))
            new_score = len(r.get('title', '')) + len(r.get('notes', ''))
            if new_score > existing_score:
                seen2[key2] = r
        else:
            seen2[key2] = r

    return list(seen2.values())


# ─── Output ──────────────────────────────────────────────────────────────────

def build_notes(r):
    """Combine folder, shared folder, notes, and custom fields into Notes."""
    parts = []
    if r.get('folder'):
        parts.append(f"[Folder: {r['folder']}]")
    if r.get('shared_folder'):
        parts.append(f"[Shared: {r['shared_folder']}]")
    if r.get('notes'):
        parts.append(r['notes'])
    custom = r.get('custom_fields', [])
    if custom:
        cf_parts = []
        for label, value in custom:
            if not label and not value:
                continue
            if label and value:
                cf_parts.append(f"{label}: {value}")
            elif value:
                cf_parts.append(value)
        if cf_parts:
            parts.append('; '.join(cf_parts))
    return '\n'.join(parts)


def write_1password_csv(records, filepath):
    """Write records in 1Password CSV import format."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Website', 'Username', 'Password', 'Notes', 'Type'])
        for r in records:
            writer.writerow([
                r['title'],
                r['url'],
                r['login'],
                r['password'],
                build_notes(r),
                detect_type(r),
            ])


def write_summary(records, filepath, source):
    """Write detailed import summary."""
    type_counts = defaultdict(int)
    for r in records:
        type_counts[detect_type(r)] += 1

    domain_counts = defaultdict(int)
    for r in records:
        d = domain_from_url(r['url'])
        if d:
            domain_counts[d] += 1

    with open(filepath, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("  1PASSWORD IMPORT SUMMARY\n")
        f.write(f"  Source: {source.title()}\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Total entries ready for import: {len(records)}\n\n")

        f.write("BY TYPE:\n")
        f.write("-" * 30 + "\n")
        for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {t:.<25} {count}\n")
        f.write("\n")

        no_pass = [r for r in records if not r['password']]
        f.write(f"ENTRIES WITHOUT PASSWORDS ({len(no_pass)}):\n")
        f.write("-" * 30 + "\n")
        for r in no_pass:
            f.write(f"  [{detect_type(r)}] {r['title']}\n")
        f.write("\n")

        f.write("TOP DOMAINS (3+ entries):\n")
        f.write("-" * 30 + "\n")
        for d, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
            if count >= 3:
                f.write(f"  {d:.<35} {count}\n")
        f.write("\n")

        f.write("=" * 60 + "\n")
        f.write("  IMPORT INSTRUCTIONS\n")
        f.write("=" * 60 + "\n\n")
        f.write("1. Go to my.1password.com/import\n")
        f.write("2. Select 'CSV File'\n")
        f.write("3. Upload: 1password_final_import.csv\n")
        f.write("4. Map columns:\n")
        f.write("   Column 1 (Title)    -> Title\n")
        f.write("   Column 2 (Website)  -> Website\n")
        f.write("   Column 3 (Username) -> Username\n")
        f.write("   Column 4 (Password) -> Password\n")
        f.write("   Column 5 (Notes)    -> Notes\n")
        f.write("   Column 6 (Type)     -> Tag (or ignore)\n")
        f.write("5. Select your vault and confirm import\n\n")
        f.write("NOTE: Credit Card, Identity, SSN, and Driver License\n")
        f.write("items import as Login type. Their structured data\n")
        f.write("is preserved in the Notes field. Manually convert\n")
        f.write("them to the correct type in 1Password after import.\n")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Convert password exports to 1Password CSV format')
    parser.add_argument('--input', required=True, help='Path to the source CSV export file')
    parser.add_argument('--source', required=True, choices=list(PARSERS.keys()),
                        help='Source password manager')
    parser.add_argument('--output-dir', required=True, help='Directory to write output files')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 50)
    print(f"  {args.source.title()} -> 1Password Migration")
    print("=" * 50)

    print(f"\n[1/4] Parsing {args.source.title()} export...")
    parse_fn = PARSERS[args.source]
    records = parse_fn(args.input)
    print(f"      Raw records: {len(records)}")

    print("[2/4] Cleaning entries...")
    records = clean_records(records)
    print(f"      After cleanup: {len(records)}")

    print("[3/4] Deduplicating (2-phase)...")
    records = deduplicate(records)
    print(f"      After dedup: {len(records)}")

    records.sort(key=lambda r: r['title'].lower())

    output_csv = os.path.join(args.output_dir, '1password_final_import.csv')
    output_summary = os.path.join(args.output_dir, 'import_summary.txt')

    print("[4/4] Writing output files...")
    write_1password_csv(records, output_csv)
    write_summary(records, output_summary, args.source)

    print(f"\n  Import CSV:  {output_csv}")
    print(f"  Summary:     {output_summary}")
    print(f"\n  Total entries for import: {len(records)}")
    print("  Done!")


if __name__ == '__main__':
    main()
