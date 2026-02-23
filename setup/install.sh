#!/bin/bash

set -e

echo "QA Automations - Environment Setup"
echo ""

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Please install Homebrew using Kandji, then run this script again."
    echo ""
    exit 1
fi

# Install Node.js
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    brew install node
else
    NODE_VERSION=$(node --version)
    echo "Node.js already installed: $NODE_VERSION"
fi

echo ""

# Install MCP CSV Writer dependencies
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"

cd "$PROJECT_ROOT/mcp-csv-writer"
npm install
cd "$PROJECT_ROOT"
echo "MCP CSV Writer dependencies installed"

echo ""

# Copy dbhub.toml.example to dbhub.toml
if [ -f "$PROJECT_ROOT/dbhub.toml" ]; then
    echo "dbhub.toml already exists"
else
    cp "$PROJECT_ROOT/dbhub.toml.example" "$PROJECT_ROOT/dbhub.toml"
    echo "Created dbhub.toml"
fi

echo ""
echo "======================================"
echo "          Setup Complete!"
echo "======================================"
echo ""
echo "📝 Next Steps:"
echo "   1. Open dbhub.toml in your editor"
echo "   2. Replace the following placeholders with your database credentials:"
echo "      - DB_USER"
echo "      - DB_PASSWORD"
echo "      - DB_HOST"
echo "      - DB_NAME"
echo ""
echo "   3. Open this workspace in VS Code"
echo "   4. Copilot will auto-load the DBHub MCP server"
echo ""
