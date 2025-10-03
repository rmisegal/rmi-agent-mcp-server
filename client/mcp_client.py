#!/usr/bin/env python3
"""
MCP Client for RmiAgentMcpServer

This client connects to the MCP server and provides a simple interface
for calling tools. It supports both local (stdio) and remote (HTTP/SSE) connections.

Author: Based on PRD specification
"""

import asyncio
import sys
from typing import Optional
from fastmcp import Client


class RmiMcpClient:
    """
    Client for interacting with RmiAgentMcpServer.
    """
    
    def __init__(self, server_url: str):
        """
        Initialize the MCP client.
        
        Args:
            server_url: URL or path to the MCP server
                       - For local: path to server script (e.g., "../server/mcp_server.py")
                       - For HTTP: URL with /sse endpoint (e.g., "http://localhost:8000/sse")
                       - For ngrok: ngrok URL (e.g., "https://abc123.ngrok.io/sse")
        """
        self.server_url = server_url
        self.client = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.client = Client(self.server_url)
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def list_tools(self):
        """
        List all available tools on the server.
        
        Returns:
            List of tool definitions
        """
        return await self.client.list_tools()
    
    async def run_python(self, file_name: str) -> str:
        """
        Execute a Python file on the server.
        
        Args:
            file_name: Path to the Python file to execute
        
        Returns:
            Output from the Python execution
        """
        result = await self.client.call_tool("run_python", {"file_name": file_name})
        
        # Extract text content from result
        if result.content and len(result.content) > 0:
            return result.content[0].text
        return "(No output)"
    
    async def list_python_files(self, directory: Optional[str] = None) -> str:
        """
        List Python files in a directory.
        
        Args:
            directory: Directory to search (optional)
        
        Returns:
            List of Python files
        """
        args = {}
        if directory:
            args["directory"] = directory
        
        result = await self.client.call_tool("list_python_files", args)
        
        if result.content and len(result.content) > 0:
            return result.content[0].text
        return "(No files found)"


async def interactive_mode(server_url: str):
    """
    Run the client in interactive mode.
    
    Args:
        server_url: URL or path to the MCP server
    """
    print("=" * 60)
    print("RmiAgentMcpServer - Interactive Client")
    print("=" * 60)
    print(f"Connecting to: {server_url}")
    print()
    
    try:
        async with RmiMcpClient(server_url) as client:
            print("✓ Connected successfully!")
            print()
            
            # List available tools
            tools = await client.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Interactive loop
            while True:
                print("-" * 60)
                print("Commands:")
                print("  1. Run Python file")
                print("  2. List Python files")
                print("  3. List tools")
                print("  q. Quit")
                print()
                
                choice = input("Enter command: ").strip().lower()
                print()
                
                if choice == 'q' or choice == 'quit':
                    print("Goodbye!")
                    break
                
                elif choice == '1':
                    file_name = input("Enter Python file path: ").strip()
                    if file_name:
                        print(f"\nExecuting: {file_name}")
                        print("-" * 60)
                        output = await client.run_python(file_name)
                        print(output)
                        print("-" * 60)
                
                elif choice == '2':
                    directory = input("Enter directory (or press Enter for default): ").strip()
                    directory = directory if directory else None
                    print()
                    output = await client.list_python_files(directory)
                    print(output)
                
                elif choice == '3':
                    tools = await client.list_tools()
                    print("Available tools:")
                    for tool in tools.tools:
                        print(f"\n  Tool: {tool.name}")
                        print(f"  Description: {tool.description}")
                        if hasattr(tool, 'inputSchema'):
                            print(f"  Input Schema: {tool.inputSchema}")
                
                else:
                    print("Invalid command. Please try again.")
                
                print()
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


async def run_single_command(server_url: str, file_name: str):
    """
    Run a single Python file and exit.
    
    Args:
        server_url: URL or path to the MCP server
        file_name: Path to the Python file to execute
    """
    try:
        async with RmiMcpClient(server_url) as client:
            print(f"Executing: {file_name}")
            print("-" * 60)
            output = await client.run_python(file_name)
            print(output)
            print("-" * 60)
    
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        sys.exit(1)


def main():
    """
    Main entry point for the client.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MCP Client for RmiAgentMcpServer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with local server
  python mcp_client.py --server ../server/mcp_server.py
  
  # Interactive mode with HTTP server
  python mcp_client.py --server http://localhost:8000/sse
  
  # Interactive mode with ngrok
  python mcp_client.py --server https://abc123.ngrok.io/sse
  
  # Run single file
  python mcp_client.py --server ../server/mcp_server.py --file test.py
        """
    )
    
    parser.add_argument(
        "--server",
        required=True,
        help="Server URL or path (local script, http://..., or https://...)"
    )
    
    parser.add_argument(
        "--file",
        help="Python file to execute (single command mode)"
    )
    
    args = parser.parse_args()
    
    # Run appropriate mode
    if args.file:
        asyncio.run(run_single_command(args.server, args.file))
    else:
        asyncio.run(interactive_mode(args.server))


if __name__ == "__main__":
    main()
