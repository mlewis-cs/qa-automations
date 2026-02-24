#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { writeFileSync, mkdirSync, readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { spawn } from "child_process";
import { createConnection } from "net";
import getPort from "get-port";
import { Client } from "pg";
import { parse as parseToml } from "toml";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Start an ssh local-forward subprocess and wait until localPort is accepting connections.
// Returns { child, localPort } and throws on timeout/failure.
async function startSshTunnel(src, workspaceRoot, { timeoutMs = 10000 } = {}) {
  const localPort = await getPort();
  const sshArgs = [];

  if (src.ssh_key) {
    const keyPath = src.ssh_key.startsWith("/") ? src.ssh_key : resolve(workspaceRoot, src.ssh_key);
    sshArgs.push("-i", keyPath);
  }

  if (src.ssh_port) {
    sshArgs.push("-p", String(src.ssh_port));
  }

  sshArgs.push(
    "-o", "ExitOnForwardFailure=yes",
    "-o", "StrictHostKeyChecking=yes",
    "-o", "ServerAliveInterval=60",
    "-o", "ServerAliveCountMax=3"
  );

  const remoteDbPort = src.port || 5432;
  sshArgs.push("-L", `${localPort}:${src.host}:${remoteDbPort}`);
  sshArgs.push(`${src.ssh_user}@${src.ssh_host}`, "-N");

  const child = spawn("ssh", sshArgs, { stdio: ["ignore", "pipe", "pipe"] });

  child.stderr.on("data", (d) => {
    try {
      console.error("[ssh tunnel]", String(d).trim());
    } catch (e) {}
  });

  await waitForPortOpen(localPort, timeoutMs).catch((err) => {
    try { child.kill("SIGTERM"); } catch (e) {}
    throw new Error(`SSH tunnel failed to open: ${err.message}`);
  });

  return { child, localPort };
}

function waitForPortOpen(port, timeoutMs = 10000) {
  const deadline = Date.now() + timeoutMs;
  return new Promise((resolve, reject) => {
    function tryConnect() {
      const sock = createConnection({ port, host: "127.0.0.1" }, () => {
        sock.destroy();
        return resolve();
      });
      sock.on("error", (err) => {
        sock.destroy();
        if (Date.now() > deadline) return reject(new Error("timeout waiting for port"));
        setTimeout(tryConnect, 150);
      });
    }
    tryConnect();
  });
}

async function stopSshTunnel(child, { graceMs = 3000 } = {}) {
  if (!child || child.killed) return;
  try { child.kill("SIGTERM"); } catch (e) {}
  await new Promise((res) => setTimeout(res, graceMs));
  if (!child.killed) {
    try { child.kill("SIGKILL"); } catch (e) {}
  }
}

// Convert array of objects to CSV string
function arrayToCSV(data) {
  if (!data || data.length === 0) {
    return "";
  }

  // Get headers from first row
  const headers = Object.keys(data[0]);
  const csvHeaders = headers.join(",");

  // Convert each row to CSV
  const csvRows = data.map((row) => {
    return headers
      .map((header) => {
        const value = row[header];
        // Handle null/undefined
        if (value === null || value === undefined) {
          return "";
        }
        // Convert to string and escape quotes
        const stringValue = String(value).replace(/"/g, '""');
        // Wrap in quotes if contains comma, newline, or quote
        if (stringValue.includes(",") || stringValue.includes("\n") || stringValue.includes('"')) {
          return `"${stringValue}"`;
        }
        return stringValue;
      })
      .join(",");
  });

  return [csvHeaders, ...csvRows].join("\n");
}

// Mask sensitive columns by replacing distinct values with columnName-N
function maskRows(data) {
  if (!data || data.length === 0) return data;

  const sensitiveFields = [
    "first_name",
    "last_name",
    "user_name",
    "sender_name",
    "recipient_name",
    "user_first_last_name",
    "client_first_name",
    "client_last_name",
    "descriptor",
    "email_address",
    "contact_email_address",
    "email",
    "most_recent_message_content",
    "cell_phone",
    "phone",
    "phone_number",
    "business_number",
    "office_phone_number",
    "phone_number_region",
    "office_name",
    "address",
    "birth_date",
    "ssn",
    "uuid",
    "link",
    "integration_id",
    "account_id",
    "subaccount_id",
    "tollfree_phone_number_sid",
    "tollfree_registration_sid",
    "auth_key",
    "subaccount_auth",
    "api_key",
    "access_token",
    "refresh_token",
    "client_id",
    "client_secret",
    "token",
    "google_oauth_credential",
    "google_calendar_id",
    "password",
    "password_reset_token",
    "login_verification_code",
    "device_token",
    "device_endpoint",
    "s3_key",
    "thumbnail_s3_key",
    "random_id",
    "stripe_charge_id",
    "stripe_receipt_id",
    "stripe_refund_id",
    "customer_id",
    "subscription_id",
    "file_name",
    "original_document_id",
    "message_content",
    "content",
    "original_content",
    "translated_content",
    "final_content",
    "treatment_notes",
    "form_response",
    "raw_typeform_payload",
    "raw_matter",
    "object_dump",
    "payload",
    "input_payload",
    "request_json",
    "response_json",
    "system_message_metadata",
    "data",
    "error_messaging",
    "integration_error",
    "internal_integration_error",
    "email_unique_token",
    "link_expiration",
    "password_reset_token_expiration",
    "sms_errors",
  ];

  // dedupe
  const fields = Array.from(new Set(sensitiveFields));

  // mapping per field: originalValue -> index
  const maps = {};
  const counters = {};

  return data.map((row) => {
    // shallow copy row
    const out = Object.assign({}, row);
    for (const field of fields) {
      if (!Object.prototype.hasOwnProperty.call(row, field)) continue;

      const raw = row[field];
      if (raw === null || raw === undefined || raw === "") {
        out[field] = "";
        continue;
      }

      const key = typeof raw === "string" ? raw : JSON.stringify(raw);

      if (!maps[field]) {
        maps[field] = new Map();
        counters[field] = 0;
      }

      const m = maps[field];
      if (m.has(key)) {
        out[field] = `${field}-${m.get(key)}`;
      } else {
        counters[field] += 1;
        m.set(key, counters[field]);
        out[field] = `${field}-${counters[field]}`;
      }
    }
    return out;
  });
}

const server = new Server(
  {
    name: "csv-writer",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "write_csv_from_query",
        description:
          "Run a SQL query against a configured source in dbhub.toml and write results to a CSV file. Avoids requiring the agent to reformat results.",
        inputSchema: {
          type: "object",
          properties: {
            source: {
              type: "string",
              description: "ID of the source defined in dbhub.toml ('production' or 'dev_local')",
            },
            query: {
              type: "string",
              description: "SQL query to execute (e.g., 'SELECT * FROM table LIMIT 100')",
            },
            filename: {
              type: "string",
              description: "Name of the CSV file to create (e.g., 'results.csv'). File will be saved in the db_results folder.",
            },
          },
          required: ["source", "query", "filename"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  

  if (request.params.name === "write_csv_from_query") {
    const { source, query, filename } = request.params.arguments;

    if (typeof source !== "string" || !source) {
      throw new Error("source must be a non-empty string referencing a source in dbhub.toml");
    }

    if (typeof query !== "string" || !query) {
      throw new Error("query must be a non-empty SQL string");
    }

    if (typeof filename !== "string" || !filename) {
      throw new Error("filename must be a non-empty string");
    }

    // Determine workspace root (same logic as existing write_csv)
    const envWorkspace = process.env.MCP_WORKSPACE || process.env.WORKSPACE_FOLDER || process.env.WORKSPACE_ROOT || process.env.GITHUB_WORKSPACE;
    const workspaceRoot = envWorkspace ? resolve(envWorkspace) : process.cwd() || resolve(__dirname, "..");

    // Load and parse dbhub.toml
    const tomlPath = resolve(workspaceRoot, "dbhub.toml");
    let tomlRaw;
    try {
      tomlRaw = readFileSync(tomlPath, "utf8");
    } catch (err) {
      throw new Error(`Could not read dbhub.toml at ${tomlPath}: ${err.message}`);
    }

    let parsed;
    try {
      parsed = parseToml(tomlRaw);
    } catch (err) {
      throw new Error(`Could not parse dbhub.toml: ${err.message}`);
    }

    const sources = parsed.sources || [];
    const src = sources.find((s) => s.id === source);
    if (!src) {
      throw new Error(`Source '${source}' not found in dbhub.toml`);
    }

    // Build pg client config, optionally creating an SSH tunnel if configured
    let sshChild = null;
    let clientConfig;
    try {
      if (src.ssh_host && src.ssh_user) {
        const tunnel = await startSshTunnel(src, workspaceRoot);
        sshChild = tunnel.child;
        const localPort = tunnel.localPort;

        if (src.dsn) {
          // Replace host:port in dsn by pointing to localhost:localPort.
          // This is a pragmatic replace that assumes a single @host:port/segment.
          clientConfig = { connectionString: src.dsn.replace(/@(.*?):(\d+)\//, `@localhost:${localPort}/`) };
        } else {
          clientConfig = {
            host: "127.0.0.1",
            port: localPort,
            database: src.database,
            user: src.user,
            password: src.password,
          };
          if (src.sslmode && String(src.sslmode).toLowerCase() === "require") {
            clientConfig.ssl = { rejectUnauthorized: false };
          }
        }
      } else {
        if (src.dsn) {
          clientConfig = { connectionString: src.dsn };
        } else {
          clientConfig = {
            host: src.host,
            port: src.port || 5432,
            database: src.database,
            user: src.user,
            password: src.password,
          };
          if (src.sslmode && String(src.sslmode).toLowerCase() === "require") {
            clientConfig.ssl = { rejectUnauthorized: false };
          }
        }
      }
    } catch (err) {
      // ensure we tear down tunnel on errors during setup
      if (sshChild) await stopSshTunnel(sshChild);
      throw err;
    }

    let client = null;
    let rows = [];
    try {
      client = new Client(clientConfig);
      await client.connect();
      const res = await client.query(query);
      rows = res.rows || [];

      // Write CSV to workspace db_results
      const dbResultsFolder = resolve(workspaceRoot, "db_results");
      mkdirSync(dbResultsFolder, { recursive: true });
      const filePath = resolve(dbResultsFolder, filename);

      const masked = maskRows(rows);
      const csv = arrayToCSV(masked);
      writeFileSync(filePath, csv, "utf8");

      const rowCount = rows.length;

      return {
        content: [
          {
            type: "text",
            text: `Successfully executed query and wrote ${rowCount} row(s) to ${filename}\nFull path: ${filePath}`,
          },
          {
            type: "text",
            text: `Workspace root used: ${workspaceRoot}`,
          },
          {
            type: "text",
            text: `Source: ${source}`,
          },
        ],
      };
    } catch (err) {
      throw new Error(`Database query failed: ${err.message}`);
    } finally {
      try {
        if (client) await client.end();
      } catch (e) {
        // ignore
      }
      try {
        if (sshChild) await stopSshTunnel(sshChild);
      } catch (e) {
        // ignore
      }
    }
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("CSV Writer MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
