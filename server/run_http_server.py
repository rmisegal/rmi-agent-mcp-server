#!/usr/bin/env python3
"""
Run MCP Server with HTTP/SSE transport.

This allows remote clients to connect via HTTP.
"""

import os
import sys
from pathlib import Path

# Set default environment variable if not set (cross-platform)
if "PYTHON_PROJECTS_DIR" not in os.environ:
    # Use project root / python_projects
    project_root = Path(__file__).parent.parent.resolve()
    default_dir = project_root / "python_projects"
    os.environ["PYTHON_PROJECTS_DIR"] = str(default_dir)

# Import the server
from mcp_server import mcp, ALLOWED_DIRECTORY

def main():
    """Run the server with HTTP transport."""
    print("=" * 60)
    print("RmiAgentMcpServer - HTTP/SSE Mode")
    print("=" * 60)
    print(f"Platform: {sys.platform}")
    print(f"Allowed directory: {ALLOWED_DIRECTORY}")
    print(f"Server will listen on: http://0.0.0.0:8000")
    print(f"SSE endpoint: http://0.0.0.0:8000/sse")
    print()
    print("To create ngrok tunnel, run in another terminal:")
    if sys.platform == "win32":
        print("  # PowerShell:")
        print("  ngrok http --region=eu 8000")
    else:
        print("  # Bash:")
        print("  ngrok http --region=eu 8000")
    print()
    print("=" * 60)
    print()
    
    # Run with HTTP transport
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
