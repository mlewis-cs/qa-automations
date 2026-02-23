# QA Automations - Database Access & Setup Guide

## Database Access (DBHub MCP)

This project includes a read-only PostgreSQL connection via the DBHub MCP server, configured for use with GitHub Copilot in VS Code.

### Initial Setup

1. **Copy the example configuration:**
   ```bash
   cp dbhub.toml.example dbhub.toml
   ```

2. **Fill in your actual database credentials** in `dbhub.toml`:
   - `host`: PostgreSQL database host
   - `user`: Database username
   - `password`: Database password
   - `database`: Database name (default: `case_status`)
   - `ssh_host`, `ssh_user`, `ssh_key`: SSH tunnel details (if required)
   - The `dbhub.toml` file is gitignored — never commit it

3. **Requirements:**
   - Node.js (v16+) must be installed and available in your PATH
   - VS Code with GitHub Copilot extension

### How It Works

The `.mcp.json` file (version-controlled) configures the DBHub MCP server for Copilot. When you open this workspace in VS Code:
- Copilot automatically discovers and loads the DBHub MCP server
- You can query the database directly through Copilot's chat interface
- The first run downloads `@bytebase/dbhub` automatically via `npx`

### Database Constraints

- **Read-only**: Only `SELECT` queries are permitted. `INSERT`, `UPDATE`, `DELETE`, and DDL are blocked.
- **Row limit**: All queries are capped at **50 rows**. Paginate using `LIMIT` and `OFFSET` for larger result sets.

### Query Examples

Use the `execute_sql` tool within Copilot to query the database:

```sql
-- List tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Inspect a table schema
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'your_table';

-- Query data with explicit limit
SELECT * FROM your_table LIMIT 50;

-- Paginate through results
SELECT * FROM your_table ORDER BY id LIMIT 50 OFFSET 50;
```

### Troubleshooting

- **MCP server not connecting**: Ensure `dbhub.toml` exists and has valid credentials
- **Node.js not found**: Verify Node.js is installed: `node --version`
- **Copilot not using the MCP**: Reload VS Code or restart the Copilot extension

## CSV Writer (MCP Tool)

This project includes a custom MCP server that provides a tool for writing SQL query results to CSV files.

### Initial Setup

The CSV Writer MCP server is automatically configured when you open this workspace. To ensure it's ready:

1. **Install dependencies** (if not already done):
   ```bash
   cd mcp-csv-writer
   npm install
   ```

2. **The tool is available immediately** - no additional configuration needed

### How to Use

Ask Copilot to write query results to CSV files:

**Examples:**
- "Execute this SQL query and save the results to results.csv"
- "Query the users table and write the output to users.csv"  
- "Get all cases from the last week and export to cases.csv"

### Tool Details

**write_csv** - Writes an array of objects (like SQL query results) to a CSV file

**Parameters:**
- `data`: Array of objects representing rows
- `filename`: Name of the CSV file (e.g., 'results.csv')

**Features:**
- Automatic CSV formatting with proper escaping
- Handles commas, quotes, and newlines in data
- Files are saved to the workspace root directory
- Supports null/undefined values

**Note:** Generated CSV files are gitignored and won't be committed to version control.
