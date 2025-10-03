#!/usr/bin/env python3
"""
Test MCP client connection through ngrok tunnel.
"""

import sys
import os
import asyncio

# Add paths
sys.path.insert(0, "client")

from mcp_client import RmiMcpClient

# Get ngrok URL
NGROK_URL = "https://confessedly-humid-meggan.ngrok-free.dev/sse"


async def test_ngrok_connection():
    """Test client-server communication through ngrok."""
    
    print("=" * 60)
    print("Testing MCP Client Connection Through ngrok")
    print("=" * 60)
    print(f"Server URL: {NGROK_URL}")
    print()
    
    try:
        # Connect to server via ngrok
        print("Connecting to server via ngrok...")
        async with RmiMcpClient(NGROK_URL) as client:
            print("✓ Connected successfully through ngrok!")
            print()
            
            # Test 1: List tools
            print("Test 1: Listing available tools")
            print("-" * 60)
            tools_result = await client.list_tools()
            if hasattr(tools_result, 'tools'):
                tools = tools_result.tools
            else:
                tools = tools_result
            
            for tool in tools:
                print(f"  Tool: {tool.name}")
                print(f"  Description: {tool.description[:100]}...")
                print()
            print("-" * 60)
            print()
            
            # Test 2: Run hello_world.py
            print("Test 2: Running hello_world.py via ngrok")
            print("-" * 60)
            result = await client.run_python("python_projects/hello_world.py")
            print(result)
            print("-" * 60)
            print()
            
            # Test 3: Run calculator.py
            print("Test 3: Running calculator.py via ngrok")
            print("-" * 60)
            result = await client.run_python("python_projects/calculator.py")
            print(result)
            print("-" * 60)
            print()
            
            # Test 4: List Python files
            print("Test 4: Listing Python files via ngrok")
            print("-" * 60)
            result = await client.list_python_files()
            print(result)
            print("-" * 60)
            print()
        
        print("=" * 60)
        print("✓ All ngrok tests completed successfully!")
        print("=" * 60)
        print()
        print("The MCP server is accessible from anywhere via:")
        print(f"  {NGROK_URL}")
        print()
        
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_ngrok_connection())
