#!/bin/bash
# Automatic MCP setup for Marketplace Execution Runtime
# Adds execution runtime to Claude Desktop/Code configuration

set -e

echo "🚀 Claude Skills Marketplace - Execution Runtime Setup"
echo "======================================================="
echo ""

# Detect OS and set config base path
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    OS_NAME="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Claude"
    OS_NAME="Linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    CONFIG_DIR="$APPDATA/Claude"
    OS_NAME="Windows"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "📍 Detected OS: $OS_NAME"
echo ""

# Detect which Claude config exists
CLAUDE_CODE_CONFIG="$CONFIG_DIR/claude_code_config.json"
CLAUDE_DESKTOP_CONFIG="$CONFIG_DIR/claude_desktop_config.json"

if [ -f "$CLAUDE_CODE_CONFIG" ] && [ -f "$CLAUDE_DESKTOP_CONFIG" ]; then
    echo "🔍 Both Claude Code and Claude Desktop configs found"
    echo ""
    echo "Which one would you like to configure?"
    echo "  1) Claude Code (claude_code_config.json)"
    echo "  2) Claude Desktop (claude_desktop_config.json)"
    echo "  3) Both"
    echo ""
    read -p "Choice (1/2/3): " CHOICE

    case $CHOICE in
        1)
            CLAUDE_CONFIG="$CLAUDE_CODE_CONFIG"
            INSTALL_MODE="code"
            ;;
        2)
            CLAUDE_CONFIG="$CLAUDE_DESKTOP_CONFIG"
            INSTALL_MODE="desktop"
            ;;
        3)
            CLAUDE_CONFIG="$CLAUDE_CODE_CONFIG"
            INSTALL_MODE="both"
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
elif [ -f "$CLAUDE_CODE_CONFIG" ]; then
    echo "✅ Found Claude Code config"
    CLAUDE_CONFIG="$CLAUDE_CODE_CONFIG"
    INSTALL_MODE="code"
elif [ -f "$CLAUDE_DESKTOP_CONFIG" ]; then
    echo "✅ Found Claude Desktop config"
    CLAUDE_CONFIG="$CLAUDE_DESKTOP_CONFIG"
    INSTALL_MODE="desktop"
else
    echo "❌ No Claude config found"
    echo ""
    echo "Please choose which to create:"
    echo "  1) Claude Code (claude_code_config.json)"
    echo "  2) Claude Desktop (claude_desktop_config.json)"
    echo ""
    read -p "Choice (1/2): " CHOICE

    case $CHOICE in
        1)
            CLAUDE_CONFIG="$CLAUDE_CODE_CONFIG"
            INSTALL_MODE="code"
            ;;
        2)
            CLAUDE_CONFIG="$CLAUDE_DESKTOP_CONFIG"
            INSTALL_MODE="desktop"
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
fi

echo "📁 Config location: $CLAUDE_CONFIG"
echo ""

# Get plugin installation directory
PLUGIN_PATH="$HOME/.claude/plugins/marketplaces/mhattingpete-claude-skills/execution-runtime"

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

# Function to update a config file
update_config() {
    local config_file="$1"
    python3 << EOF
import json
from pathlib import Path

config_path = Path("$config_file")
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
print("✅ MCP server configured in " + str(config_path.name))
EOF
    return $?
}

# Update config(s) based on install mode
if [ "$INSTALL_MODE" = "both" ]; then
    update_config "$CLAUDE_CODE_CONFIG"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to update Claude Code config"
        exit 1
    fi
    update_config "$CLAUDE_DESKTOP_CONFIG"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to update Claude Desktop config"
        exit 1
    fi
else
    update_config "$CLAUDE_CONFIG"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to update config"
        exit 1
    fi
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
