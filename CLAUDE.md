# QA Automations - Claude Code Project Guide

## Database Access (DBHub MCP)

This project includes a read-only PostgreSQL connection via the DBHub MCP server.

### Setup

1. Copy `dbhub.toml.example` to `dbhub.toml`:

   ```bash
   cp dbhub.toml.example dbhub.toml
   ```
2. Fill in your actual database credentials in `dbhub.toml`.
3. Restart Claude Code — DBHub auto-detects `dbhub.toml` and starts automatically.

### Constraints

- **Read-only**: Only `SELECT` queries are permitted. `INSERT`, `UPDATE`, `DELETE`, and DDL are blocked.
- **Row limit**: All queries are capped at **50 rows**. If you need more, paginate using `LIMIT` and `OFFSET`.

### Using the Database Tool

Use the `execute_sql` tool from the `dbhub` MCP server to query the database. Examples:

```sql
-- List tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Inspect a table
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'your_table';

-- Query data (limit is enforced automatically, but be explicit)
SELECT * FROM your_table LIMIT 50;

-- Paginate
SELECT * FROM your_table ORDER BY id LIMIT 50 OFFSET 50;
```

### Requirements

- Node.js / `npx` must be available in your PATH.
- The first run will download `@bytebase/dbhub` automatically via `npx`.
