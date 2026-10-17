# Sales Data Reporting Workflow with Approved Integrations

Portfolio project showing a scheduled n8n workflow that consolidates PostgreSQL, Google Sheets and Slack inputs into a normalized sales report. Includes an importable workflow template, a local Pandas demo, sample data, PostgreSQL schema, Docker Compose, and runbooks.

## Quick start: local demo
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_report.py
```
Outputs are written to `output/` as CSV and Markdown. The demo uses sample CSV data; it does not call external services.

## Start PostgreSQL + n8n
```bash
cp .env.example .env
docker compose up -d
```
Open n8n at `http://localhost:5678`. Import `n8n/sales_reporting_workflow.json`. Configure credentials in n8n for PostgreSQL, Google Sheets and Slack, then update placeholder node settings and test each integration before enabling the schedule. Never commit real credentials to Git.

## Workflow outline
1. Schedule Trigger
2. PostgreSQL query for monthly sales rows
3. Google Sheets read for approved supplemental adjustments (configure document/sheet IDs)
4. Merge sources
5. Code node normalizes fields and computes regional totals
6. Slack message sends a summary to the configured channel

The included JSON is a starter template: credentials, sheet IDs, query and node wiring should be reviewed for your environment before production use. Use least-privilege credentials and approved company integrations.

## Data contract
Expected fields: `order_id`, `order_date`, `region`, `product`, `quantity`, `unit_price`, `source`. Missing numeric values are reported and excluded from totals rather than silently treated as zero.

## Reliability notes
- Configure retries and error workflow in n8n for your deployment.
- Review API quotas, permissions, timezone, duplicate handling, and schema changes.
- Slack posts are summary-only; do not include customer-sensitive fields.
