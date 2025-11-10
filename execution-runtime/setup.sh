#!/bin/bash
# Installation script for Claude Code Execution Runtime
# Installs Python package for direct imports

set -e

echo "🚀 Claude Code - Execution Runtime Setup"
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_NAME="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_NAME="Linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS_NAME="Windows"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "📍 Detected OS: $OS_NAME"
echo "📁 Installation directory: $SCRIPT_DIR"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    echo ""
    echo "Please install Python 3.11 or later:"
    echo "  macOS: brew install python@3.11"
    echo "  Linux: apt install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found $PYTHON_VERSION"
echo ""

# Check for pip or uv
if command -v uv &> /dev/null; then
    echo "✅ Found uv package manager"
    INSTALLER="uv pip"
elif command -v pip3 &> /dev/null; then
    echo "✅ Found pip"
    INSTALLER="pip3"
else
    echo "❌ Neither pip nor uv found"
    echo ""
    echo "Please install pip or uv first"
    exit 1
fi

echo ""
echo "📦 Installing execution-runtime package..."
echo ""

cd "$SCRIPT_DIR"

# Install package in editable mode
$INSTALLER install -e .

if [ $? -eq 0 ]; then
    echo ""
    echo "✨ Installation Complete!"
    echo "========================"
    echo ""
    echo "The execution runtime is now available for direct import:"
    echo ""
    echo "  from execution_runtime import fs, code, transform, git"
    echo ""
    echo "Example usage:"
    echo "  # Find functions (metadata only)"
    echo "  functions = code.find_functions('app.py')"
    echo ""
    echo "  # Rename across codebase"
    echo "  result = transform.rename_identifier('.', 'old', 'new', '**/*.py')"
    echo ""
    echo "  # Copy lines between files"
    echo "  code_block = fs.copy_lines('source.py', 10, 20)"
    echo ""
    echo "📖 Documentation: $SCRIPT_DIR/README.md"
    echo ""
    echo "Happy coding! 🚀"
else
    echo ""
    echo "❌ Installation failed"
    echo ""
    echo "Try manually:"
    echo "  cd $SCRIPT_DIR"
    echo "  pip3 install -e ."
    exit 1
fi
