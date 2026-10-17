# Operations runbook

## Before enabling a scheduled workflow
- Verify PostgreSQL query and read-only account permissions.
- Select the correct Google Sheets document and tab; grant access only to the workflow service identity.
- Create a Slack app/webhook approved by the organization and limit channel access.
- Test with synthetic data, then compare totals with the source-of-truth report.
- Set the schedule timezone explicitly and avoid overlapping runs.

## Failure handling
- **PostgreSQL unavailable:** configure retry with exponential backoff; alert after retry exhaustion.
- **Google Sheets quota/timeout:** retry transient failures; do not treat an empty response as a valid zero.
- **Missing or malformed values:** route rows to a review output and include counts in the run summary.
- **Duplicate order IDs:** use a stable order ID and deterministic upsert/deduplication rule.
- **Slack failure:** persist report outputs first; retry notification independently so a notification outage does not lose the report.

## Security and change management
- Store credentials only in n8n credential storage/environment secrets, never in workflow exports or Git.
- Rotate tokens, use least privilege, and keep production data out of demo logs.
- Document owner, run frequency, source schemas, data retention, and rollback procedure.
- Review changes with a second person before production activation.
