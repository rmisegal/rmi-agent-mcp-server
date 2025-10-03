#!/usr/bin/env python3
"""
Integration tests for MCP Server and Client.
"""

import sys
import os
import asyncio
import pytest
from pathlib import Path

# Set cross-platform default directory
if "PYTHON_PROJECTS_DIR" not in os.environ:
    project_root = Path(__file__).parent.parent.resolve()
    os.environ["PYTHON_PROJECTS_DIR"] = str(project_root / "python_projects")

# Add directories to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "server"))
sys.path.insert(0, str(project_root / "client"))

from mcp_server import mcp as server_mcp, ALLOWED_DIRECTORY
from mcp_client import RmiMcpClient


@pytest.mark.asyncio
class TestClientServerIntegration:
    """Integration tests for client-server communication."""
    
    @pytest.fixture
    async def client(self):
        """Create client connected to server via in-memory transport."""
        # Use in-memory transport for testing
        async with RmiMcpClient(server_mcp) as client:
            yield client
    
    async def test_list_tools(self, client):
        """Test listing available tools."""
        tools = await client.list_tools()
        
        assert tools is not None
        assert len(tools.tools) >= 2  # run_python and list_python_files
        
        tool_names = [tool.name for tool in tools.tools]
        assert "run_python" in tool_names
        assert "list_python_files" in tool_names
    
    async def test_run_hello_world(self, client):
        """Test running hello world sample."""
        # Create test file
        test_dir = Path(ALLOWED_DIRECTORY)
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = test_dir / "test_hello.py"
        test_file.write_text("print('Hello from integration test!')")
        
        # Run the file
        output = await client.run_python(str(test_file))
        
        assert "Hello from integration test!" in output
        assert "Error" not in output
    
    async def test_run_with_error(self, client):
        """Test running file that produces error."""
        test_dir = Path(ALLOWED_DIRECTORY)
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = test_dir / "test_error.py"
        test_file.write_text("raise ValueError('Test error')")
        
        output = await client.run_python(str(test_file))
        
        assert "ValueError" in output or "Test error" in output
    
    async def test_list_python_files(self, client):
        """Test listing Python files."""
        # Create some test files
        test_dir = Path(ALLOWED_DIRECTORY)
        test_dir.mkdir(parents=True, exist_ok=True)
        
        (test_dir / "file1.py").write_text("pass")
        (test_dir / "file2.py").write_text("pass")
        
        output = await client.list_python_files()
        
        assert "file1.py" in output or "file2.py" in output
        assert "Error" not in output


def run_integration_tests():
    """Run integration tests."""
    pytest.main([__file__, "-v", "-s"])


if __name__ == "__main__":
    run_integration_tests()
