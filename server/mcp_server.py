#!/usr/bin/env python3
"""
RmiAgentMcpServer - MCP Server for Python Code Execution

This server exposes a tool that executes Python files and returns their output.
It's adapted from the LaTeX compilation agent described in the PRD, but uses
Python execution instead of LaTeX compilation.

Author: Based on PRD specification
"""

import os
import subprocess
import shlex
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("RmiAgentMcpServer")

# Configuration
ALLOWED_DIRECTORY = os.getenv("PYTHON_PROJECTS_DIR", "/home/ubuntu/python_projects")
PYTHON_TIMEOUT = int(os.getenv("PYTHON_TIMEOUT", "30"))


def validate_file_path(file_path: str) -> Path:
    """
    Validate that the file path is safe and within allowed directory.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Validated Path object
        
    Raises:
        ValueError: If path is invalid or outside allowed directory
    """
    # Convert to absolute path
    abs_path = Path(file_path).resolve()
    
    # Check if file exists
    if not abs_path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    # Check if it's a file (not directory)
    if not abs_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Check if it's a Python file
    if abs_path.suffix != ".py":
        raise ValueError(f"File must have .py extension: {file_path}")
    
    # Security: Check if file is within allowed directory
    allowed_dir = Path(ALLOWED_DIRECTORY).resolve()
    try:
        abs_path.relative_to(allowed_dir)
    except ValueError:
        raise ValueError(
            f"Access denied: File must be within {ALLOWED_DIRECTORY}. "
            f"Got: {abs_path}"
        )
    
    return abs_path


@mcp.tool
def run_python(file_name: str) -> str:
    """
    Execute a Python file and return its output (stdout and stderr).
    
    This tool runs a Python script in a subprocess and captures all output.
    It's useful for testing Python code, running scripts, and debugging.
    
    Args:
        file_name: Path to the Python file to execute. Can be absolute or relative
                   to the allowed directory. Must have .py extension.
    
    Returns:
        Combined stdout and stderr output from the Python execution.
        If there's no output, returns "(No output)".
        
    Example:
        >>> run_python("hello_world.py")
        "Hello, World!"
        
        >>> run_python("/home/ubuntu/python_projects/test.py")
        "Test passed!\nAll assertions successful."
    """
    try:
        # Validate file path
        file_path = validate_file_path(file_name)
        
        # Build command - use python3 explicitly
        cmd = ["python3", str(file_path)]
        
        # Execute Python file
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=PYTHON_TIMEOUT,
            cwd=file_path.parent  # Run in the file's directory
        )
        
        # Combine stdout and stderr
        output = ""
        if proc.stdout:
            output += proc.stdout
        if proc.stderr:
            if output:
                output += "\n--- stderr ---\n"
            output += proc.stderr
        
        # Add return code if non-zero
        if proc.returncode != 0:
            output += f"\n\n[Process exited with code {proc.returncode}]"
        
        return output if output else "(No output)"
        
    except ValueError as e:
        # File validation errors
        return f"Error: {str(e)}"
    
    except subprocess.TimeoutExpired:
        return f"Error: Execution timed out after {PYTHON_TIMEOUT} seconds"
    
    except Exception as e:
        # Unexpected errors
        return f"Error executing Python file: {type(e).__name__}: {str(e)}"


@mcp.tool
def list_python_files(directory: Optional[str] = None) -> str:
    """
    List all Python files in a directory.
    
    Args:
        directory: Directory path to search. If None, uses the allowed directory.
    
    Returns:
        List of Python files found, one per line.
    """
    try:
        if directory is None:
            search_dir = Path(ALLOWED_DIRECTORY)
        else:
            search_dir = Path(directory).resolve()
            # Security check
            allowed_dir = Path(ALLOWED_DIRECTORY).resolve()
            try:
                search_dir.relative_to(allowed_dir)
            except ValueError:
                return f"Error: Directory must be within {ALLOWED_DIRECTORY}"
        
        if not search_dir.exists():
            return f"Error: Directory not found: {search_dir}"
        
        if not search_dir.is_dir():
            return f"Error: Path is not a directory: {search_dir}"
        
        # Find all .py files
        py_files = sorted(search_dir.glob("**/*.py"))
        
        if not py_files:
            return f"No Python files found in {search_dir}"
        
        # Format output
        output = f"Python files in {search_dir}:\n"
        for py_file in py_files:
            rel_path = py_file.relative_to(search_dir)
            output += f"  - {rel_path}\n"
        
        return output
        
    except Exception as e:
        return f"Error listing files: {type(e).__name__}: {str(e)}"


def main():
    """
    Main entry point for the MCP server.
    """
    # Ensure allowed directory exists
    os.makedirs(ALLOWED_DIRECTORY, exist_ok=True)
    
    print(f"RmiAgentMcpServer starting...")
    print(f"Allowed directory: {ALLOWED_DIRECTORY}")
    print(f"Python timeout: {PYTHON_TIMEOUT}s")
    
    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
