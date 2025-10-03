#!/bin/bash
# Setup script for RmiAgentMcpServer

set -e  # Exit on error

echo "=========================================="
echo "RmiAgentMcpServer Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create python_projects directory
echo ""
echo "Creating python_projects directory..."
mkdir -p python_projects

# Copy test samples
echo "Copying test samples..."
cp -r tests/test_samples/* python_projects/ 2>/dev/null || true

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the server, run:"
echo "  python server/mcp_server.py"
echo ""
echo "To run the client, run:"
echo "  python client/mcp_client.py --server ../server/mcp_server.py"
echo ""
