#!/usr/bin/env python3
"""
Simple test script for MCP server functionality.
"""

import sys
import os

# Set environment variable
os.environ["PYTHON_PROJECTS_DIR"] = "/home/ubuntu/rmi-agent-mcp-server/python_projects"

# Add server to path
sys.path.insert(0, "server")

from mcp_server import run_python, list_python_files

print("=" * 60)
print("Testing MCP Server Tools")
print("=" * 60)
print()

# Test 1: Run hello_world.py
print("Test 1: Running hello_world.py")
print("-" * 60)
result = run_python("python_projects/hello_world.py")
print(result)
print("-" * 60)
print()

# Test 2: Run calculator.py
print("Test 2: Running calculator.py")
print("-" * 60)
result = run_python("python_projects/calculator.py")
print(result)
print("-" * 60)
print()

# Test 3: Run error_test.py (should show error)
print("Test 3: Running error_test.py (expect error)")
print("-" * 60)
result = run_python("python_projects/error_test.py")
print(result)
print("-" * 60)
print()

# Test 4: List Python files
print("Test 4: Listing Python files")
print("-" * 60)
result = list_python_files()
print(result)
print("-" * 60)
print()

# Test 5: Try to run non-existent file
print("Test 5: Running non-existent file (expect error)")
print("-" * 60)
result = run_python("python_projects/nonexistent.py")
print(result)
print("-" * 60)
print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)
