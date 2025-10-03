#!/usr/bin/env python3
"""
Test local client-server communication using in-memory transport.
"""

import sys
import os
import asyncio

# Set environment variable
os.environ["PYTHON_PROJECTS_DIR"] = "/home/ubuntu/rmi-agent-mcp-server/python_projects"

# Add paths
sys.path.insert(0, "server")
sys.path.insert(0, "client")

from mcp_server import mcp as server_mcp
from mcp_client import RmiMcpClient


async def test_local_communication():
    """Test client-server communication using in-memory transport."""
    
    print("=" * 60)
    print("Testing Local Client-Server Communication")
    print("=" * 60)
    print()
    
    # Connect to server using in-memory transport
    print("Connecting to server...")
    async with RmiMcpClient(server_mcp) as client:
        print("✓ Connected successfully!")
        print()
        
        # Test 1: List tools
        print("Test 1: Listing available tools")
        print("-" * 60)
        tools_result = await client.list_tools()
        # tools_result is a ListToolsResult object
        if hasattr(tools_result, 'tools'):
            tools = tools_result.tools
        else:
            tools = tools_result
        
        for tool in tools:
            print(f"  Tool: {tool.name}")
            print(f"  Description: {tool.description}")
            print()
        print("-" * 60)
        print()
        
        # Test 2: Run hello_world.py
        print("Test 2: Running hello_world.py")
        print("-" * 60)
        result = await client.run_python("python_projects/hello_world.py")
        print(result)
        print("-" * 60)
        print()
        
        # Test 3: Run calculator.py
        print("Test 3: Running calculator.py")
        print("-" * 60)
        result = await client.run_python("python_projects/calculator.py")
        print(result)
        print("-" * 60)
        print()
        
        # Test 4: Run error_test.py (should show error)
        print("Test 4: Running error_test.py (expect error)")
        print("-" * 60)
        result = await client.run_python("python_projects/error_test.py")
        print(result)
        print("-" * 60)
        print()
        
        # Test 5: List Python files
        print("Test 5: Listing Python files")
        print("-" * 60)
        result = await client.list_python_files()
        print(result)
        print("-" * 60)
        print()
        
        # Test 6: Try to run non-existent file
        print("Test 6: Running non-existent file (expect error)")
        print("-" * 60)
        result = await client.run_python("python_projects/nonexistent.py")
        print(result)
        print("-" * 60)
        print()
        
        # Test 7: Try to access file outside allowed directory (security test)
        print("Test 7: Security test - accessing file outside allowed directory")
        print("-" * 60)
        result = await client.run_python("/etc/passwd")
        print(result)
        print("-" * 60)
        print()
    
    print("=" * 60)
    print("✓ All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_local_communication())
