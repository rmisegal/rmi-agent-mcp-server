#!/usr/bin/env python3
"""
Interactive demo script that shows step-by-step execution.
"""

import sys
import os
import asyncio

sys.path.insert(0, "client")
from mcp_client import RmiMcpClient

async def demo_local():
    """Demo local connection."""
    print("=" * 70)
    print("DEMO 1: LOCAL CONNECTION (stdio)")
    print("=" * 70)
    print()
    
    # Import server
    sys.path.insert(0, "server")
    os.environ["PYTHON_PROJECTS_DIR"] = "/home/ubuntu/rmi-agent-mcp-server/python_projects"
    from mcp_server import mcp as server_mcp
    
    print("Connecting to local server...")
    async with RmiMcpClient(server_mcp) as client:
        print("✓ Connected!\n")
        
        # Demo 1: List tools
        print(">>> Listing available tools...")
        tools_result = await client.list_tools()
        tools = tools_result.tools if hasattr(tools_result, 'tools') else tools_result
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}")
        print()
        
        # Demo 2: Run existing file
        print(">>> Running: python_projects/hello_world.py")
        print("-" * 70)
        result = await client.run_python("python_projects/hello_world.py")
        print(result)
        print("-" * 70)
        print()
        
        # Demo 3: Run calculator
        print(">>> Running: python_projects/calculator.py")
        print("-" * 70)
        result = await client.run_python("python_projects/calculator.py")
        print(result)
        print("-" * 70)
        print()
        
        # Demo 4: Try non-existent file
        print(">>> Running: python_projects/nonexistent.py (SHOULD FAIL)")
        print("-" * 70)
        result = await client.run_python("python_projects/nonexistent.py")
        print(result)
        print("-" * 70)
        print()
        
        # Demo 5: Run error file
        print(">>> Running: python_projects/error_test.py (SHOULD SHOW ERROR)")
        print("-" * 70)
        result = await client.run_python("python_projects/error_test.py")
        print(result)
        print("-" * 70)
        print()


async def demo_ngrok():
    """Demo ngrok connection."""
    print("\n")
    print("=" * 70)
    print("DEMO 2: REMOTE CONNECTION (via ngrok)")
    print("=" * 70)
    print()
    
    ngrok_url = "https://confessedly-humid-meggan.ngrok-free.dev/sse"
    print(f"Connecting to: {ngrok_url}")
    
    async with RmiMcpClient(ngrok_url) as client:
        print("✓ Connected through ngrok!\n")
        
        # Demo 1: Run existing file
        print(">>> Running: python_projects/hello_world.py (via ngrok)")
        print("-" * 70)
        result = await client.run_python("python_projects/hello_world.py")
        print(result)
        print("-" * 70)
        print()
        
        # Demo 2: Try non-existent file
        print(">>> Running: python_projects/does_not_exist.py (SHOULD FAIL)")
        print("-" * 70)
        result = await client.run_python("python_projects/does_not_exist.py")
        print(result)
        print("-" * 70)
        print()
        
        # Demo 3: List files
        print(">>> Listing all Python files")
        print("-" * 70)
        result = await client.list_python_files()
        print(result)
        print("-" * 70)
        print()


async def main():
    """Run both demos."""
    await demo_local()
    await demo_ngrok()
    
    print("=" * 70)
    print("✓ ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
