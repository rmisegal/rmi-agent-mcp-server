#!/usr/bin/env python3
"""
Unit tests for MCP Server.
"""

import sys
import os
import pytest
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

from mcp_server import validate_file_path, ALLOWED_DIRECTORY


class TestValidateFilePath:
    """Tests for file path validation."""
    
    def setup_method(self):
        """Setup test environment."""
        # Create test directory
        self.test_dir = Path(ALLOWED_DIRECTORY)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test file
        self.test_file = self.test_dir / "test.py"
        self.test_file.write_text("print('test')")
    
    def test_valid_file(self):
        """Test validation of valid file."""
        result = validate_file_path(str(self.test_file))
        assert result == self.test_file.resolve()
    
    def test_nonexistent_file(self):
        """Test validation of nonexistent file."""
        with pytest.raises(ValueError, match="File not found"):
            validate_file_path(str(self.test_dir / "nonexistent.py"))
    
    def test_directory_not_file(self):
        """Test validation when path is directory."""
        with pytest.raises(ValueError, match="not a file"):
            validate_file_path(str(self.test_dir))
    
    def test_non_python_file(self):
        """Test validation of non-Python file."""
        txt_file = self.test_dir / "test.txt"
        txt_file.write_text("test")
        
        with pytest.raises(ValueError, match=".py extension"):
            validate_file_path(str(txt_file))
    
    def test_path_traversal_attack(self):
        """Test security against path traversal."""
        # Try to access file outside allowed directory
        outside_file = Path("/tmp/test.py")
        outside_file.write_text("print('test')")
        
        with pytest.raises(ValueError, match="Access denied"):
            validate_file_path(str(outside_file))
        
        # Cleanup
        outside_file.unlink()


class TestRunPythonTool:
    """Tests for run_python tool (integration-style)."""
    
    def setup_method(self):
        """Setup test environment."""
        self.test_dir = Path(ALLOWED_DIRECTORY)
        self.test_dir.mkdir(parents=True, exist_ok=True)
    
    def test_successful_execution(self):
        """Test successful Python execution."""
        # Create test file
        test_file = self.test_dir / "success.py"
        test_file.write_text("print('Success!')")
        
        # Import and test
        from mcp_server import run_python
        result = run_python(str(test_file))
        
        assert "Success!" in result
        assert "[Process exited with code" not in result
    
    def test_execution_with_error(self):
        """Test Python execution with error."""
        # Create test file with error
        test_file = self.test_dir / "error.py"
        test_file.write_text("undefined_variable")
        
        from mcp_server import run_python
        result = run_python(str(test_file))
        
        assert "NameError" in result or "stderr" in result
        assert "[Process exited with code 1]" in result
    
    def test_file_not_found(self):
        """Test execution of nonexistent file."""
        from mcp_server import run_python
        result = run_python(str(self.test_dir / "nonexistent.py"))
        
        assert "Error" in result
        assert "File not found" in result


def run_tests():
    """Run all tests."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_tests()
