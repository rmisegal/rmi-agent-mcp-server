#!/usr/bin/env python3
"""
MCP Client with LLM Integration

This client uses an LLM (OpenAI/Gemini) to interpret natural language prompts
and automatically select the right tool and parameters.

Usage:
    export OPENAI_API_KEY='your-key-here'
    python mcp_client_llm.py --server <server-url>

Example prompts:
    - "Run the hello world program"
    - "Execute calculator.py"
    - "Show me all Python files"
    - "Run the test file that has errors"
"""

import sys
import os
import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Add client directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_client import RmiMcpClient


class LLMClient:
    """
    Wrapper for LLM API calls.
    Supports OpenAI and Gemini.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key (if None, reads from OPENAI_API_KEY env var)
            model: Model to use (gpt-4o-mini, gpt-4, gemini-2.5-flash, etc.)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        self.model = model
        
        # Initialize OpenAI client
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "OpenAI package required. Install with: pip install openai"
            )
    
    def call_llm(self, messages: list, tools: Optional[list] = None) -> Dict[str, Any]:
        """
        Call the LLM with messages and optional tools.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions
        
        Returns:
            Response dict with message and optional tool_calls
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        
        response = self.client.chat.completions.create(**kwargs)
        
        message = response.choices[0].message
        
        return {
            "content": message.content,
            "tool_calls": message.tool_calls if hasattr(message, 'tool_calls') else None
        }


async def llm_interactive_mode(server_url: str, api_key: Optional[str] = None):
    """
    Run interactive mode with LLM integration.
    
    Args:
        server_url: URL or path to MCP server
        api_key: Optional API key (defaults to OPENAI_API_KEY env var)
    """
    print("=" * 70)
    print("RmiAgentMcpServer - LLM-Powered Interactive Client")
    print("=" * 70)
    print(f"Connecting to: {server_url}")
    print()
    
    try:
        # Initialize LLM client
        llm = LLMClient(api_key=api_key)
        print(f"✓ LLM initialized: {llm.model}")
        
        # Connect to MCP server
        async with RmiMcpClient(server_url) as mcp_client:
            print(f"✓ Connected to MCP server")
            print()
            
            # Get available tools from MCP server
            tools_result = await mcp_client.list_tools()
            tools = tools_result.tools if hasattr(tools_result, 'tools') else tools_result
            
            print(f"Available MCP tools ({len(tools)}):")
            for tool in tools:
                print(f"  - {tool.name}")
            print()
            
            # Convert MCP tools to OpenAI tool format
            openai_tools = []
            for tool in tools:
                tool_def = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }
                
                # Extract parameters from inputSchema if available
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    schema = tool.inputSchema
                    if isinstance(schema, dict):
                        if 'properties' in schema:
                            tool_def["function"]["parameters"]["properties"] = schema['properties']
                        if 'required' in schema:
                            tool_def["function"]["parameters"]["required"] = schema['required']
                
                openai_tools.append(tool_def)
            
            # Conversation history
            conversation = [
                {
                    "role": "system",
                    "content": """You are an AI assistant that helps users execute Python code via MCP tools.

Available tools:
- run_python(file_name): Execute a Python file and return output
- list_python_files(directory): List Python files in a directory

When the user asks to run a file, use the run_python tool.
When the user asks to list files, use the list_python_files tool.

File paths should be relative to python_projects/ directory, like:
- python_projects/hello_world.py
- python_projects/calculator.py
- python_projects/error_test.py

Be helpful and interpret user requests naturally."""
                }
            ]
            
            print("=" * 70)
            print("💬 Chat with the AI to execute Python code!")
            print("=" * 70)
            print()
            print("Example prompts:")
            print("  - 'Run the hello world program'")
            print("  - 'Execute calculator.py'")
            print("  - 'Show me all Python files'")
            print("  - 'Run the test file that has errors'")
            print()
            print("Type 'quit' or 'exit' to quit.")
            print("=" * 70)
            print()
            
            # Interactive loop
            while True:
                # Get user input
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Add user message to conversation
                conversation.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Call LLM
                print("\n🤖 AI: ", end="", flush=True)
                response = llm.call_llm(conversation, tools=openai_tools)
                
                # Check if LLM wants to call a tool
                if response["tool_calls"]:
                    print("(Executing tool...)\n")
                    
                    for tool_call in response["tool_calls"]:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"🔧 Tool: {function_name}")
                        print(f"📝 Arguments: {json.dumps(function_args, indent=2)}")
                        print("-" * 70)
                        
                        # Execute the tool via MCP
                        if function_name == "run_python":
                            result = await mcp_client.run_python(function_args["file_name"])
                        elif function_name == "list_python_files":
                            directory = function_args.get("directory")
                            result = await mcp_client.list_python_files(directory)
                        else:
                            result = f"Unknown tool: {function_name}"
                        
                        print(result)
                        print("-" * 70)
                        
                        # Add tool result to conversation
                        conversation.append({
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": function_name,
                                        "arguments": json.dumps(function_args)
                                    }
                                }
                            ]
                        })
                        
                        conversation.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": result
                        })
                    
                    # Get LLM's interpretation of the result
                    print("\n🤖 AI: ", end="", flush=True)
                    final_response = llm.call_llm(conversation)
                    print(final_response["content"])
                    
                    conversation.append({
                        "role": "assistant",
                        "content": final_response["content"]
                    })
                
                else:
                    # LLM responded without calling a tool
                    print(response["content"])
                    conversation.append({
                        "role": "assistant",
                        "content": response["content"]
                    })
                
                print()
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MCP Client with LLM Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Local server with LLM
  export OPENAI_API_KEY='sk-...'
  python mcp_client_llm.py --server ../server/mcp_server.py
  
  # Remote server via ngrok with LLM
  python mcp_client_llm.py --server https://abc123.ngrok.io/sse
  
  # Use specific model
  python mcp_client_llm.py --server ../server/mcp_server.py --model gpt-4
  
  # Use Gemini
  python mcp_client_llm.py --server ../server/mcp_server.py --model gemini-2.5-flash
        """
    )
    
    parser.add_argument(
        "--server",
        required=True,
        help="Server URL or path"
    )
    
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="LLM model to use (default: gpt-4o-mini)"
    )
    
    parser.add_argument(
        "--api-key",
        help="API key (defaults to OPENAI_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Run interactive mode
    asyncio.run(llm_interactive_mode(args.server, api_key=args.api_key))


if __name__ == "__main__":
    main()
