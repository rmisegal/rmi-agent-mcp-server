#!/usr/bin/env python3
"""
Test script for LLM-powered MCP client.

This demonstrates automated testing with predefined prompts.
"""

import sys
import os
import asyncio
import json
from pathlib import Path

# Set cross-platform default directory
if "PYTHON_PROJECTS_DIR" not in os.environ:
    project_root = Path(__file__).parent.resolve()
    os.environ["PYTHON_PROJECTS_DIR"] = str(project_root / "python_projects")

sys.path.insert(0, "client")
sys.path.insert(0, "server")

from mcp_client import RmiMcpClient
from mcp_server import mcp as server_mcp


async def test_llm_tool_selection():
    """
    Test that simulates LLM tool selection.
    
    This shows how an LLM would:
    1. Receive a natural language prompt
    2. Select the appropriate tool
    3. Extract parameters
    4. Execute the tool
    """
    
    print("=" * 70)
    print("Testing LLM Tool Selection Simulation")
    print("=" * 70)
    print()
    
    # Test scenarios
    test_cases = [
        {
            "prompt": "Run the hello world program",
            "tool": "run_python",
            "args": {"file_name": "python_projects/hello_world.py"},
            "expected": "Hello, World!"
        },
        {
            "prompt": "Execute calculator.py",
            "tool": "run_python",
            "args": {"file_name": "python_projects/calculator.py"},
            "expected": "Calculator Test"
        },
        {
            "prompt": "Show me all Python files",
            "tool": "list_python_files",
            "args": {},
            "expected": "calculator.py"
        },
        {
            "prompt": "Run the test file that has errors",
            "tool": "run_python",
            "args": {"file_name": "python_projects/error_test.py"},
            "expected": "NameError"
        }
    ]
    
    async with RmiMcpClient(server_mcp) as client:
        print("✓ Connected to MCP server\n")
        
        for i, test in enumerate(test_cases, 1):
            print(f"Test {i}: {test['prompt']}")
            print("-" * 70)
            print(f"🤖 LLM selects tool: {test['tool']}")
            print(f"📝 LLM extracts args: {json.dumps(test['args'], indent=2)}")
            print()
            
            # Execute the tool
            if test['tool'] == "run_python":
                result = await client.run_python(test['args']['file_name'])
            elif test['tool'] == "list_python_files":
                directory = test['args'].get('directory')
                result = await client.list_python_files(directory)
            
            print("📤 Result:")
            print(result)
            
            # Check if expected string is in result
            if test['expected'] in result:
                print(f"\n✅ Test {i} PASSED")
            else:
                print(f"\n❌ Test {i} FAILED - Expected '{test['expected']}' in result")
            
            print("=" * 70)
            print()


async def main():
    """Run the tests."""
    await test_llm_tool_selection()
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)
    print()
    print("To use the real LLM-powered client:")
    print("  1. Set your API key: export OPENAI_API_KEY='sk-...'")
    print("  2. Run: python client/mcp_client_llm.py --server server/mcp_server.py")
    print()


if __name__ == "__main__":
    asyncio.run(main())
