#!/usr/bin/env python3
"""
Run MCP Server with HTTP/SSE transport.

This allows remote clients to connect via HTTP.
"""

import os
import sys

# Ensure environment variable is set
if "PYTHON_PROJECTS_DIR" not in os.environ:
    os.environ["PYTHON_PROJECTS_DIR"] = "/home/ubuntu/rmi-agent-mcp-server/python_projects"

# Import the server
from mcp_server import mcp, ALLOWED_DIRECTORY

def main():
    """Run the server with HTTP transport."""
    print("=" * 60)
    print("RmiAgentMcpServer - HTTP/SSE Mode")
    print("=" * 60)
    print(f"Allowed directory: {ALLOWED_DIRECTORY}")
    print(f"Server will listen on: http://0.0.0.0:8000")
    print(f"SSE endpoint: http://0.0.0.0:8000/sse")
    print()
    print("To create ngrok tunnel, run in another terminal:")
    print("  ngrok http --region=eu 8000")
    print()
    print("=" * 60)
    print()
    
    # Run with HTTP transport
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
