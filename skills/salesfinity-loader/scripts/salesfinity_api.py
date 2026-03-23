#!/usr/bin/env python3
"""
Salesfinity API — Complete Python Client (March 2026)
Covers ALL 35 endpoints. Auth: x-api-key header.
"""
import argparse, json, sys, os, re
try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests

BASE_URL = "https://client-api.salesfinity.co/v1"
DEFAULT_API_KEY = "sk_ff45bc29-e5c1-4a3f-b1e5-f9776d94cbe7"

def api_headers(api_key=None):
    return {"Content-Type": "application/json", "x-api-key": api_key or DEFAULT_API_KEY}

# === TEAM ===
def get_team(api_key):
    """GET /v1/team. CORRECT endpoint (NOT /v1/users)."""
    r = requests.get(f"{BASE_URL}/team", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === CONTACT LISTS ===
def create_list(api_key, name, user_id, contacts=None):
    """POST /v1/contact-lists. Max 2000 contacts, 10MB payload."""
    p = {"name": name, "user_id": user_id}
    if contacts: p["contacts"] = contacts
    r = requests.post(f"{BASE_URL}/contact-lists", headers=api_headers(api_key), json=p)
    r.raise_for_status()
    return r.json()

def add_contact(api_key, list_id, contact):
    """POST /v1/contact-lists/{id}. CRITICAL: NO /contacts suffix."""
    r = requests.post(f"{BASE_URL}/contact-lists/{list_id}", headers=api_headers(api_key), json=contact)
    r.raise_for_status()
    return r.json()

def remove_contact(api_key, list_id, contact_id):
    """DELETE /v1/contact-lists/{id}/contacts/{contactId}"""
    r = requests.delete(f"{BASE_URL}/contact-lists/{list_id}/contacts/{contact_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def merge_lists(api_key, target_id, source_ids, delete_sources=False):
    """POST /v1/contact-lists/{id}/merge. Max 20 sources."""
    p = {"source_list_ids": source_ids, "delete_sources": delete_sources}
    r = requests.post(f"{BASE_URL}/contact-lists/{target_id}/merge", headers=api_headers(api_key), json=p)
    r.raise_for_status()
    return r.json()

def get_lists(api_key, search=None, page=1, limit=50):
    """GET /v1/contact-lists/csv. CORRECT path (NOT /contact-lists)."""
    params = {"page": page, "limit": limit}
    if search: params["search"] = search
    r = requests.get(f"{BASE_URL}/contact-lists/csv", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

def get_list_by_id(api_key, list_id, search=None, page=1, limit=50):
    """GET /v1/contact-lists/csv/{id}. Full contacts."""
    params = {"page": page, "limit": limit}
    if search: params["search"] = search
    r = requests.get(f"{BASE_URL}/contact-lists/csv/{list_id}", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

def delete_list(api_key, list_id):
    """DELETE /v1/contact-lists/csv/{id}. CRITICAL: path is /csv/{id} NOT /{id}."""
    r = requests.delete(f"{BASE_URL}/contact-lists/csv/{list_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def reimport_list(api_key, list_id):
    """POST /v1/contact-lists/csv/{id}/reimport. Reset to full queue."""
    r = requests.post(f"{BASE_URL}/contact-lists/csv/{list_id}/reimport", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === CALL LOGS ===
def get_call_logs(api_key, page=1, limit=50, **filters):
    """GET /v1/call-log. Filters: start_date, end_date, outcome, direction, etc."""
    params = {"page": page, "limit": limit}
    for k, v in filters.items(): params[f"filters[{k}]"] = v
    r = requests.get(f"{BASE_URL}/call-log", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

def get_call_log(api_key, call_id):
    """GET /v1/call-log/{id}"""
    r = requests.get(f"{BASE_URL}/call-log/{call_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === SCORED CALLS (AI) ===
def get_scored_calls(api_key, page=1, limit=50, **kwargs):
    """GET /v1/scored-calls. Params: start_date, end_date, min_score, max_score, user_id."""
    params = {"page": page, "limit": limit}
    params.update(kwargs)
    r = requests.get(f"{BASE_URL}/scored-calls", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

def get_scored_call(api_key, call_id):
    """GET /v1/scored-calls/{id}"""
    r = requests.get(f"{BASE_URL}/scored-calls/{call_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === ANALYTICS ===
def get_analytics_overview(api_key, start_date, end_date, **kwargs):
    """GET /v1/analytics/overview. start_date and end_date REQUIRED."""
    params = {"start_date": start_date, "end_date": end_date}
    params.update(kwargs)
    r = requests.get(f"{BASE_URL}/analytics/overview", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

def get_analytics_list_performance(api_key, start_date, end_date, **kwargs):
    """GET /v1/analytics/list-performance"""
    params = {"start_date": start_date, "end_date": end_date}
    params.update(kwargs)
    r = requests.get(f"{BASE_URL}/analytics/list-performance", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

def get_analytics_sdr_performance(api_key, start_date, end_date, **kwargs):
    """GET /v1/analytics/sdr-performance"""
    params = {"start_date": start_date, "end_date": end_date}
    params.update(kwargs)
    r = requests.get(f"{BASE_URL}/analytics/sdr-performance", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

# === SNOOZED CONTACTS ===
def get_snoozed_contacts(api_key, page=1, limit=50, **kwargs):
    """GET /v1/snoozed-contacts"""
    params = {"page": page, "limit": limit}
    params.update(kwargs)
    r = requests.get(f"{BASE_URL}/snoozed-contacts", headers=api_headers(api_key), params=params)
    r.raise_for_status()
    return r.json()

def get_snoozed_by_linkedin(api_key, username):
    """GET /v1/snoozed-contacts/by-linkedin/{username}"""
    r = requests.get(f"{BASE_URL}/snoozed-contacts/by-linkedin/{username}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def get_snoozed_contact(api_key, contact_id):
    """GET /v1/snoozed-contacts/{id}"""
    r = requests.get(f"{BASE_URL}/snoozed-contacts/{contact_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def update_snoozed_contact(api_key, contact_id, data):
    """PUT /v1/snoozed-contacts/{id}"""
    r = requests.put(f"{BASE_URL}/snoozed-contacts/{contact_id}", headers=api_headers(api_key), json=data)
    r.raise_for_status()
    return r.json()

def delete_snoozed_contact(api_key, contact_id):
    """DELETE /v1/snoozed-contacts/{id}"""
    r = requests.delete(f"{BASE_URL}/snoozed-contacts/{contact_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === FOLLOW-UPS ===
def get_follow_ups(api_key, page=1, limit=50):
    """GET /v1/follow-up"""
    r = requests.get(f"{BASE_URL}/follow-up", headers=api_headers(api_key), params={"page": page, "limit": limit})
    r.raise_for_status()
    return r.json()

# === DISPOSITIONS ===
def get_dispositions(api_key):
    """GET /v1/dispositions"""
    r = requests.get(f"{BASE_URL}/dispositions", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def get_disposition(api_key, disp_id):
    """GET /v1/dispositions/{id}"""
    r = requests.get(f"{BASE_URL}/dispositions/{disp_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === SEQUENCES ===
def get_sequences(api_key, page=1, limit=50):
    """GET /v1/sequences"""
    r = requests.get(f"{BASE_URL}/sequences", headers=api_headers(api_key), params={"page": page, "limit": limit})
    r.raise_for_status()
    return r.json()

def get_sequence(api_key, seq_id):
    """GET /v1/sequences/{id}"""
    r = requests.get(f"{BASE_URL}/sequences/{seq_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === CUSTOM FIELDS ===
def get_custom_fields(api_key):
    """GET /v1/custom-fields"""
    r = requests.get(f"{BASE_URL}/custom-fields", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === WEBHOOKS ===
def create_webhook(api_key, name, url, events, dispositions=None):
    """POST /v1/webhooks. Events: CALL_LOGGED, CONTACT_SNOOZED"""
    p = {"name": name, "url": url, "events": events}
    if dispositions: p["dispositions"] = dispositions
    r = requests.post(f"{BASE_URL}/webhooks", headers=api_headers(api_key), json=p)
    r.raise_for_status()
    return r.json()

def get_webhooks(api_key):
    """GET /v1/webhooks"""
    r = requests.get(f"{BASE_URL}/webhooks", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def get_webhook_events(api_key):
    """GET /v1/webhooks/events (may need higher auth)"""
    r = requests.get(f"{BASE_URL}/webhooks/events", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def get_webhook(api_key, wh_id):
    """GET /v1/webhooks/{id}"""
    r = requests.get(f"{BASE_URL}/webhooks/{wh_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def update_webhook(api_key, wh_id, data):
    """PUT /v1/webhooks/{id}"""
    r = requests.put(f"{BASE_URL}/webhooks/{wh_id}", headers=api_headers(api_key), json=data)
    r.raise_for_status()
    return r.json()

def delete_webhook(api_key, wh_id):
    """DELETE /v1/webhooks/{id}"""
    r = requests.delete(f"{BASE_URL}/webhooks/{wh_id}", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

def get_webhook_logs(api_key, wh_id):
    """GET /v1/webhooks/{id}/logs"""
    r = requests.get(f"{BASE_URL}/webhooks/{wh_id}/logs", headers=api_headers(api_key))
    r.raise_for_status()
    return r.json()

# === CONVERTERS ===
def validate_list_name(name):
    """Validate list naming convention: {Entity} \u2014 {Vertical} \u2014 {Timezone} (v{N})"""
    pattern = r'^.+ \u2014 .+ \u2014 .+ \(v\d+\)$'
    if not re.match(pattern, name):
        print(f"WARNING: Name '{name}' doesn't match convention: {{Entity}} \u2014 {{Vertical}} \u2014 {{Timezone}} (v{{N}})")
        return False
    return True

def convert_exa_to_salesfinity(exa_results, context=None):
    """Convert Exa enrichment results to Salesfinity contact format."""
    contacts = []
    for person in exa_results:
        contact = {
            "first_name": person.get("first_name", ""),
            "last_name": person.get("last_name", ""),
            "email": person.get("email", ""),
            "company": person.get("company", ""),
            "title": person.get("title", ""),
            "phone_numbers": [],
        }
        if person.get("phone"):
            contact["phone_numbers"].append({"type": "direct", "number": person["phone"]})
        if person.get("linkedin_url"):
            contact["linkedin"] = person["linkedin_url"]
        if context:
            contact["notes"] = context.get("notes", "")
            contact["custom_fields"] = context.get("custom_fields", [])
        contacts.append(contact)
    return contacts

def convert_csv_to_salesfinity(csv_path):
    """Convert CSV file to Salesfinity contact format."""
    import csv
    contacts = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            contact = {
                "first_name": row.get("first_name", row.get("First Name", "")),
                "last_name": row.get("last_name", row.get("Last Name", "")),
                "email": row.get("email", row.get("Email", "")),
                "company": row.get("company", row.get("Company", "")),
                "title": row.get("title", row.get("Title", "")),
                "phone_numbers": [],
            }
            phone = row.get("phone", row.get("Phone", row.get("phone_number", "")))
            if phone:
                if not phone.startswith("+"): phone = "+1" + re.sub(r'\D', '', phone)
                contact["phone_numbers"].append({"type": "direct", "number": phone})
            contacts.append(contact)
    return contacts

# === CLI ===
def main():
    p = argparse.ArgumentParser(description="Salesfinity API Client")
    p.add_argument("--action", required=True, help="API action")
    p.add_argument("--api-key", default=DEFAULT_API_KEY)
    p.add_argument("--name", help="List name")
    p.add_argument("--user-id", default="680edc0d1504192884a148e0")
    p.add_argument("--list-id", help="List ID")
    p.add_argument("--contact-id", help="Contact ID")
    p.add_argument("--call-id", help="Call ID")
    p.add_argument("--webhook-id", help="Webhook ID")
    p.add_argument("--contacts-json", help="Path to contacts JSON")
    p.add_argument("--contact-json", help="Path to single contact JSON")
    p.add_argument("--source-list-ids", help="Comma-sep list IDs for merge")
    p.add_argument("--delete-sources", action="store_true")
    p.add_argument("--search", help="Search query")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--start-date", help="Start date (ISO 8601)")
    p.add_argument("--end-date", help="End date (ISO 8601)")
    p.add_argument("--webhook-url", help="Webhook URL")
    p.add_argument("--webhook-events", help="Comma-sep events")
    p.add_argument("--exa-json", help="Path to Exa results JSON")
    p.add_argument("--context-json", help="Path to context JSON")
    p.add_argument("--csv-input", help="Path to CSV")
    p.add_argument("--output", help="Output file path")
    args = p.parse_args()
    k = args.api_key

    actions = {
        "get-team": lambda: get_team(k),
        "create-list": lambda: create_list(k, args.name, args.user_id,
            json.load(open(args.contacts_json)) if args.contacts_json else None),
        "add-contact": lambda: add_contact(k, args.list_id,
            json.load(open(args.contact_json))),
        "remove-contact": lambda: remove_contact(k, args.list_id, args.contact_id),
        "merge-lists": lambda: merge_lists(k, args.list_id,
            args.source_list_ids.split(","), args.delete_sources),
        "get-lists": lambda: get_lists(k, args.search, args.page, args.limit),
        "get-list": lambda: get_list_by_id(k, args.list_id, args.search, args.page, args.limit),
        "delete-list": lambda: delete_list(k, args.list_id),
        "reimport-list": lambda: reimport_list(k, args.list_id),
        "get-call-logs": lambda: get_call_logs(k, args.page, args.limit),
        "get-call-log": lambda: get_call_log(k, args.call_id),
        "get-scored-calls": lambda: get_scored_calls(k, args.page, args.limit),
        "get-scored-call": lambda: get_scored_call(k, args.call_id),
        "analytics-overview": lambda: get_analytics_overview(k, args.start_date, args.end_date),
        "analytics-list-perf": lambda: get_analytics_list_performance(k, args.start_date, args.end_date),
        "analytics-sdr-perf": lambda: get_analytics_sdr_performance(k, args.start_date, args.end_date),
        "get-snoozed": lambda: get_snoozed_contacts(k, args.page, args.limit),
        "delete-snoozed": lambda: delete_snoozed_contact(k, args.contact_id),
        "get-follow-ups": lambda: get_follow_ups(k, args.page, args.limit),
        "get-dispositions": lambda: get_dispositions(k),
        "get-sequences": lambda: get_sequences(k, args.page, args.limit),
        "get-custom-fields": lambda: get_custom_fields(k),
        "create-webhook": lambda: create_webhook(k, args.name, args.webhook_url,
            args.webhook_events.split(",")),
        "get-webhooks": lambda: get_webhooks(k),
        "get-webhook-events": lambda: get_webhook_events(k),
        "delete-webhook": lambda: delete_webhook(k, args.webhook_id),
        "get-webhook-logs": lambda: get_webhook_logs(k, args.webhook_id),
        "validate-name": lambda: validate_list_name(args.name),
        "convert-exa": lambda: convert_exa_to_salesfinity(
            json.load(open(args.exa_json)),
            json.load(open(args.context_json)) if args.context_json else None),
        "convert-csv": lambda: convert_csv_to_salesfinity(args.csv_input),
    }

    if args.action not in actions:
        print(f"Unknown action: {args.action}")
        print(f"Available: {', '.join(sorted(actions.keys()))}")
        sys.exit(1)

    result = actions[args.action]()
    output = json.dumps(result, indent=2, default=str)
    if args.output:
        with open(args.output, 'w') as f: f.write(output)
        print(f"Written to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
