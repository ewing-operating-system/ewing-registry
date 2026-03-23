# SpokePhone Integration (STUB - Awaiting API Key)

## Status: NOT YET CONNECTED

## What We Need
- `SPOKE_CLIENT_ID` - OAuth2 client ID
- `SPOKE_CLIENT_SECRET` - OAuth2 client secret

## API Details
- Auth URL: `https://auth.spokephone.com/oauth/token`
- API URL: `https://integration.spokephone.com`
- Docs: https://developer.spokephone.com/
- Auth: OAuth2 token-based

## What We'll Pull
Once connected, the daily workflow will call SpokePhone to retrieve:

1. **Call Logs** (yesterday's date range)
   - Phone number dialed (outbound) or received (inbound)
   - Call direction (inbound/outbound)
   - Call duration
   - Call start/end timestamps
   - Call outcome/disposition
   - Recording URL (if available)
   - Caller ID information

2. **SMS/WhatsApp Logs** (if applicable)
   - Message content
   - Direction
   - Timestamps
   - Contact info

3. **Webhook Events** (optional future enhancement)
   - Real-time call events
   - Could trigger instant processing instead of daily batch

## Integration Approach
Once Ewing provides API credentials:
1. Store credentials securely
2. Build OAuth2 token refresh flow
3. Create API call functions for call log retrieval
4. Add to daily orchestrator Step 1d
5. Cross-reference numbers with prospect tracker

## How to Activate
When Ewing provides SpokePhone credentials, update this file and add the API calls to the main SKILL.md workflow.
