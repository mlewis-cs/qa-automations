#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { writeFileSync, mkdirSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

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
        name: "write_csv",
        description:
          "Write SQL query results to a CSV file. Accepts an array of row objects and writes them to the db_results folder.",
        inputSchema: {
          type: "object",
          properties: {
            data: {
              type: "array",
              description: "Array of objects representing rows to write to CSV",
              items: {
                type: "object",
              },
            },
            filename: {
              type: "string",
              description: "Name of the CSV file to create (e.g., 'results.csv'). File will be saved in the db_results folder.",
            },
          },
          required: ["data", "filename"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "write_csv") {
    const { data, filename } = request.params.arguments;

    if (!Array.isArray(data)) {
      throw new Error("data must be an array");
    }

    if (typeof filename !== "string" || !filename) {
      throw new Error("filename must be a non-empty string");
    }

    // Resolve path relative to workspace (parent of mcp-csv-writer)
    const workspaceRoot = resolve(__dirname, "..");
    const dbResultsFolder = resolve(workspaceRoot, "db_results");
    mkdirSync(dbResultsFolder, { recursive: true });
    const filePath = resolve(dbResultsFolder, filename);

    // Convert to CSV
    const csv = arrayToCSV(data);

    // Write file
    writeFileSync(filePath, csv, "utf8");

    const rowCount = data.length;

    return {
      content: [
        {
          type: "text",
          text: `Successfully wrote ${rowCount} row(s) to ${filename}\nFull path: ${filePath}`,
        },
      ],
    };
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
