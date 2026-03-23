#!/usr/bin/env python3
"""
Finance Agent — Plaid Link Setup
One-time setup to connect Wells Fargo and Chase via Plaid.

STATUS: STUB — requires plaid-python package and API credentials.
Run: pip install plaid-python
Then configure ~/.config/finance-agent/credentials.json
"""

import json
import os
import sys
from pathlib import Path

CREDENTIALS_PATH = Path.home() / ".config" / "finance-agent" / "credentials.json"


def load_credentials():
    if not CREDENTIALS_PATH.exists():
        print(f"No credentials found at {CREDENTIALS_PATH}")
        print("\nTo set up Plaid:")
        print("1. Sign up at https://dashboard.plaid.com/signup")
        print("2. Get your client_id and secret from the dashboard")
        print(f"3. Create {CREDENTIALS_PATH} with:")
        print(json.dumps({
            "plaid_client_id": "YOUR_CLIENT_ID",
            "plaid_secret": "YOUR_SECRET",
            "plaid_env": "sandbox",
            "access_tokens": {}
        }, indent=2))
        print(f"\n4. Run this script again")
        return None

    with open(CREDENTIALS_PATH) as f:
        return json.load(f)


def save_credentials(creds):
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDENTIALS_PATH, "w") as f:
        json.dump(creds, f, indent=2)
    os.chmod(str(CREDENTIALS_PATH), 0o600)


def check_plaid_installed():
    try:
        import plaid
        return True
    except ImportError:
        print("plaid-python not installed.")
        print("Run: pip install plaid-python")
        return False


def create_link_token(client, client_id):
    """Create a Plaid Link token for connecting a new institution."""
    from plaid.model.link_token_create_request import LinkTokenCreateRequest
    from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
    from plaid.model.products import Products
    from plaid.model.country_code import CountryCode

    request = LinkTokenCreateRequest(
        products=[Products("transactions"), Products("investments")],
        client_name="Finance Agent",
        country_codes=[CountryCode("US")],
        language="en",
        user=LinkTokenCreateRequestUser(client_user_id=str(client_id)),
    )
    response = client.link_token_create(request)
    return response["link_token"]


def exchange_public_token(client, public_token):
    """Exchange a public token for an access token."""
    from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)
    return response["access_token"], response["item_id"]


def setup_plaid_link():
    """Main setup flow — creates link token and starts local server for Plaid Link."""
    creds = load_credentials()
    if not creds:
        return

    if not check_plaid_installed():
        return

    import plaid
    from plaid.api import plaid_api
    from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
    from plaid.model.products import Products

    env_map = {
        "sandbox": plaid.Environment.Sandbox,
        "development": plaid.Environment.Development,
        "production": plaid.Environment.Production,
    }

    configuration = plaid.Configuration(
        host=env_map.get(creds["plaid_env"], plaid.Environment.Sandbox),
        api_key={
            "clientId": creds["plaid_client_id"],
            "secret": creds["plaid_secret"],
        },
    )
    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    if creds["plaid_env"] == "sandbox":
        print("Running in SANDBOX mode — using test data")
        print("\nCreating sandbox tokens for Wells Fargo and Chase...")

        for inst_id, name in [("ins_4", "Wells Fargo"), ("ins_3", "Chase")]:
            if name in creds.get("access_tokens", {}):
                print(f"  {name}: already linked")
                continue

            try:
                request = SandboxPublicTokenCreateRequest(
                    institution_id=inst_id,
                    initial_products=[Products("transactions")],
                )
                response = client.sandbox_public_token_create(request)
                access_token, item_id = exchange_public_token(client, response["public_token"])

                if "access_tokens" not in creds:
                    creds["access_tokens"] = {}
                creds["access_tokens"][name] = {
                    "access_token": access_token,
                    "item_id": item_id,
                    "institution_id": inst_id,
                }
                save_credentials(creds)
                print(f"  {name}: linked successfully")
            except Exception as e:
                print(f"  {name}: failed — {e}")

        print("\nSandbox setup complete! Run /finance sync to pull test data.")
    else:
        # For development/production, we need Plaid Link UI
        link_token = create_link_token(client, creds["plaid_client_id"])
        print(f"\nPlaid Link Token: {link_token}")
        print("\nTo connect your bank accounts:")
        print("1. A browser window will need to open with Plaid Link")
        print("2. Select Wells Fargo or Chase and log in")
        print("3. The public token will be exchanged for an access token")
        print("\nNote: Full Plaid Link UI integration requires a web server.")
        print("For now, use sandbox mode for testing, or import CSV files directly.")


if __name__ == "__main__":
    setup_plaid_link()
