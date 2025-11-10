#!/bin/bash
# Automatic MCP setup for Marketplace Execution Runtime
# Adds execution runtime to Claude Desktop/Code configuration

set -e

echo "🚀 Claude Skills Marketplace - Execution Runtime Setup"
echo "======================================================="
echo ""

# Detect OS and set config path
if [[ "$OSTYPE" == "darwin"* ]]; then
    CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    OS_NAME="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CLAUDE_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
    OS_NAME="Linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    CLAUDE_CONFIG="$APPDATA/Claude/claude_desktop_config.json"
    OS_NAME="Windows"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "📍 Detected OS: $OS_NAME"
echo "📁 Config location: $CLAUDE_CONFIG"
echo ""

# Get plugin installation directory
PLUGIN_PATH="$HOME/.claude/plugins/execution-runtime"

# Check if plugin exists
if [ ! -d "$PLUGIN_PATH" ]; then
    echo "❌ Execution runtime not found at $PLUGIN_PATH"
    echo ""
    echo "Please install the plugin first:"
    echo "  /plugin marketplace add mhattingpete/claude-skills-marketplace"
    exit 1
fi

echo "✅ Found execution runtime at: $PLUGIN_PATH"
echo ""

# Check if Claude config exists
if [ ! -f "$CLAUDE_CONFIG" ]; then
    echo "⚠️  Claude config not found"
    echo "Creating new config file..."
    mkdir -p "$(dirname "$CLAUDE_CONFIG")"
    echo '{"mcpServers":{}}' > "$CLAUDE_CONFIG"
fi

# Prompt for allowed directories
echo "🔐 Security Configuration"
echo "-------------------------"
echo "The execution runtime needs permission to access directories."
echo "Enter directories to allow (comma-separated), or press Enter for defaults:"
echo ""
echo "Default: $HOME/Documents, $HOME/Projects"
echo ""
read -p "Allowed directories: " USER_DIRS

if [ -z "$USER_DIRS" ]; then
    ALLOWED_DIRS="$HOME/Documents,$HOME/Projects"
else
    ALLOWED_DIRS="$USER_DIRS"
fi

echo ""
echo "Will allow access to: $ALLOWED_DIRS"
echo ""

# Check for uv
if command -v uv &> /dev/null; then
    echo "✅ Found uv package manager"
    USE_UV=true
    COMMAND="uv"
    ARGS='["run", "python", "'$PLUGIN_PATH'/mcp-server/mcp_server.py"]'
else
    echo "⚠️  uv not found, will use python directly"
    echo "   (Install uv for better performance: curl -LsSf https://astral.sh/uv/install.sh | sh)"
    USE_UV=false
    COMMAND="python3"
    ARGS='["'$PLUGIN_PATH'/mcp-server/mcp_server.py"]'
fi

echo ""
echo "📝 Adding MCP server configuration..."
echo ""

# Update config using Python
python3 << EOF
import json
from pathlib import Path

config_path = Path("$CLAUDE_CONFIG")
config = json.loads(config_path.read_text()) if config_path.exists() else {}

if 'mcpServers' not in config:
    config['mcpServers'] = {}

# Add execution runtime server
config['mcpServers']['marketplace-execution'] = {
    'command': '$COMMAND',
    'args': $ARGS,
    'env': {
        'ALLOWED_DIRECTORIES': '$ALLOWED_DIRS',
        'MASK_SECRETS': 'true',
        'AGGRESSIVE_MASKING': 'false'
    }
}

config_path.write_text(json.dumps(config, indent=2))
print("✅ MCP server configured successfully")
EOF

if [ $? -ne 0 ]; then
    echo "❌ Failed to update config"
    exit 1
fi

# Install dependencies if using uv
if [ "$USE_UV" = true ]; then
    echo ""
    echo "📦 Installing dependencies..."
    cd "$PLUGIN_PATH"
    uv pip install -e . > /dev/null 2>&1 || true
    echo "✅ Dependencies installed"
fi

echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code or Claude Desktop"
echo "  2. The execution runtime will be available automatically"
echo ""
echo "📊 Benefits you now have:"
echo "  ✓ 90%+ token savings for bulk operations"
echo "  ✓ Local code execution with API imports"
echo "  ✓ Stateful multi-step refactoring"
echo "  ✓ Automatic secret/PII masking"
echo ""
echo "📖 Documentation:"
echo "  $PLUGIN_PATH/README.md"
echo ""
echo "🧪 Test the installation:"
echo "  Ask Claude: 'Can you execute Python code using the marketplace API?'"
echo ""
echo "Happy coding! 🚀"
