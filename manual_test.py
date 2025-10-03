#!/usr/bin/env python3
"""
Manual test - run specific file names provided as arguments.
"""

import sys
import os
import asyncio

sys.path.insert(0, "client")
sys.path.insert(0, "server")

os.environ["PYTHON_PROJECTS_DIR"] = "/home/ubuntu/rmi-agent-mcp-server/python_projects"

from mcp_client import RmiMcpClient
from mcp_server import mcp as server_mcp


async def test_file(filename):
    """Test a specific file."""
    print(f"\n{'='*70}")
    print(f"Testing: {filename}")
    print('='*70)
    
    async with RmiMcpClient(server_mcp) as client:
        result = await client.run_python(filename)
        print(result)
        print('='*70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manual_test.py <filename>")
        print("\nExamples:")
        print("  python manual_test.py python_projects/hello_world.py")
        print("  python manual_test.py python_projects/calculator.py")
        print("  python manual_test.py python_projects/nonexistent.py")
        sys.exit(1)
    
    filename = sys.argv[1]
    asyncio.run(test_file(filename))
