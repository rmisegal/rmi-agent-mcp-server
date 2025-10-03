# RmiAgentMcpServer - AI Python Execution Agent

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0+-green.svg)](https://github.com/jlowin/fastmcp)

A full-stack AI agent system for remote Python code execution, built on the **Model Context Protocol (MCP)**. This project demonstrates how to create an MCP server that exposes tools for executing Python code, and how AI assistants (like Claude or Gemini) can interact with it.

## 📋 Table of Contents

- [What This Code Does](#what-this-code-does)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Option 1: Using venv (Standard)](#option-1-using-venv-standard)
  - [Option 2: Using UV (Modern, Recommended)](#option-2-using-uv-modern-recommended)
- [ngrok Setup](#ngrok-setup)
- [Running the Server](#running-the-server)
  - [Linux/Mac](#linuxmac)
  - [Windows PowerShell](#windows-powershell)
- [Testing](#testing)
- [LLM-Powered Client](#llm-powered-client)
  - [Natural Language Interface](#natural-language-interface)
  - [How It Works](#how-it-works)
  - [Usage Examples](#usage-examples)
- [MCP Architecture Explained](#mcp-architecture-explained)
- [Using with LLMs](#using-with-llms)
  - [Use Case 1: Claude Desktop Integration](#use-case-1-claude-desktop-integration)
  - [Use Case 2: API Key as Environment Variable](#use-case-2-api-key-as-environment-variable)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 What This Code Does

This project implements a **client-server system** where:

1. **MCP Server** (`server/mcp_server.py`):
   - Exposes a `run_python` tool that can execute any Python file
   - Validates file paths to prevent unauthorized access
   - Captures stdout, stderr, and exit codes
   - Returns results to the client
   - Runs with HTTP/SSE transport for remote access

2. **MCP Client** (`client/mcp_client.py`):
   - Connects to the server (locally or remotely via ngrok)
   - Discovers available tools
   - Invokes the `run_python` tool with file paths
   - Displays results to the user

3. **AI Integration**:
   - AI assistants (Claude, Gemini) can use this server as a tool
   - The AI can execute Python code on your behalf
   - The AI interprets results and suggests fixes for errors

**Real-world use case**: An AI coding assistant that can run Python scripts, test code, debug errors, and iterate on solutions automatically.

---

## 🏗️ Architecture Overview

### MCP (Model Context Protocol)

MCP is an open standard by Anthropic for connecting AI applications to external tools and data sources. It uses JSON-RPC 2.0 for communication.

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   AI/LLM    │ ◄─────► │ MCP Client  │ ◄─────► │ MCP Server  │
│  (Claude/   │  MCP    │             │  HTTP/  │             │
│   Gemini)   │ Protocol│             │  stdio  │             │
└─────────────┘         └─────────────┘         └─────────────┘
                                                        │
                                                        ▼
                                                 ┌─────────────┐
                                                 │   Python    │
                                                 │  Executor   │
                                                 └─────────────┘
```

### Communication Flow

1. **Tool Discovery**: Client asks server "What tools do you have?"
2. **Tool Invocation**: Client sends `tools/call` request with tool name and arguments
3. **Execution**: Server runs the Python file and captures output
4. **Response**: Server returns output, errors, and exit code to client
5. **Display**: Client shows results to user or AI

---

## 📁 Project Structure

```
rmi-agent-mcp-server/
├── server/
│   ├── mcp_server.py           # Main MCP server with run_python tool
│   ├── run_http_server.py      # HTTP/SSE server launcher
│   └── requirements.txt        # Server dependencies
├── client/
│   ├── mcp_client.py           # MCP client implementation
│   └── requirements.txt        # Client dependencies
├── tests/
│   ├── test_samples/           # Sample Python files for testing
│   │   ├── hello_world.py
│   │   ├── calculator.py
│   │   └── error_test.py
│   ├── test_server.py          # Server unit tests
│   └── test_integration.py     # Integration tests
├── python_projects/            # Directory for user Python files
├── .gitignore
├── .env.example                # Environment variables template
├── README.md
├── requirements.txt            # Combined dependencies
└── setup.sh                    # Setup script for Linux/Mac
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+**
- **pip** or **uv** (package manager)
- **git**

### Option 1: Using venv (Standard)

#### Linux/Mac:

```bash
# Clone the repository
git clone https://github.com/rmisegal/rmi-agent-mcp-server.git
cd rmi-agent-mcp-server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create python_projects directory
mkdir -p python_projects
cp tests/test_samples/*.py python_projects/
```

#### Windows PowerShell:

```powershell
# Clone the repository
git clone https://github.com/rmisegal/rmi-agent-mcp-server.git
cd rmi-agent-mcp-server

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create python_projects directory
New-Item -ItemType Directory -Force -Path python_projects
Copy-Item tests\test_samples\*.py python_projects\
```

### Option 2: Using UV (Modern, Recommended)

**UV** is a modern, fast Python package and project manager written in Rust. It's significantly faster than pip and handles virtual environments automatically.

#### Install UV:

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows PowerShell:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Setup with UV:

```bash
# Clone the repository
git clone https://github.com/rmisegal/rmi-agent-mcp-server.git
cd rmi-agent-mcp-server

# UV automatically creates and manages the virtual environment
uv venv

# Activate the environment (UV does this automatically for most commands)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\Activate.ps1  # Windows

# Install dependencies with UV (much faster than pip!)
uv pip install -r requirements.txt

# Create python_projects directory
mkdir -p python_projects
cp tests/test_samples/*.py python_projects/
```

**Why UV?**
- ⚡ **10-100x faster** than pip
- 🔒 Automatic dependency resolution
- 🎯 Built-in virtual environment management
- 🦀 Written in Rust for performance

---

## 🌐 ngrok Setup

**ngrok** creates secure tunnels from public URLs to your localhost, allowing remote access to your MCP server without configuring firewalls or port forwarding.

### Why We Need ngrok

1. **Remote Access**: Expose your local server to the internet
2. **Testing**: Test your MCP server with cloud-based AI services
3. **Collaboration**: Share your server with team members
4. **No Configuration**: No need to configure routers or firewalls

### Installation

#### Linux (Debian/Ubuntu):

```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok
```

#### Mac:

```bash
brew install ngrok
```

#### Windows:

Download from [ngrok.com/download](https://ngrok.com/download) or use Chocolatey:

```powershell
choco install ngrok
```

### Configuration

1. **Sign up** at [ngrok.com](https://ngrok.com/)
2. **Get your auth token** from [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)
3. **Configure ngrok**:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

---

## 🖥️ Running the Server

The MCP server must run in a **separate terminal** or in the **background** because it's a long-running process that listens for connections.

### Linux/Mac

#### Option 1: Separate Terminal (Recommended)

**Terminal 1 - Start Server:**
```bash
cd rmi-agent-mcp-server
source venv/bin/activate
export PYTHON_PROJECTS_DIR=$(pwd)/python_projects
python server/run_http_server.py
```

**Terminal 2 - Start ngrok:**
```bash
ngrok http --region=eu 8000
```

**Terminal 3 - Run Client:**
```bash
cd rmi-agent-mcp-server
source venv/bin/activate
python client/mcp_client.py --server https://YOUR_NGROK_URL.ngrok.io/sse
```

#### Option 2: Background Process

```bash
# Start server in background
cd rmi-agent-mcp-server
source venv/bin/activate
export PYTHON_PROJECTS_DIR=$(pwd)/python_projects
nohup python server/run_http_server.py > server.log 2>&1 &

# Save the process ID
echo $! > server.pid

# Start ngrok in background
nohup ngrok http --region=eu 8000 > ngrok.log 2>&1 &
echo $! > ngrok.pid

# Get ngrok URL
sleep 3
curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"

# To stop the server later:
kill $(cat server.pid)
kill $(cat ngrok.pid)
```

### Windows PowerShell

#### Option 1: Separate Windows (Recommended)

**PowerShell Window 1 - Start Server:**
```powershell
cd rmi-agent-mcp-server
.\venv\Scripts\Activate.ps1
$env:PYTHON_PROJECTS_DIR = "$PWD\python_projects"
python server\run_http_server.py
```

**PowerShell Window 2 - Start ngrok:**
```powershell
ngrok http --region=eu 8000
```

**PowerShell Window 3 - Run Client:**
```powershell
cd rmi-agent-mcp-server
.\venv\Scripts\Activate.ps1
python client\mcp_client.py --server https://YOUR_NGROK_URL.ngrok.io/sse
```

#### Option 2: Background Process (PowerShell Jobs)

```powershell
# Navigate to project directory
cd rmi-agent-mcp-server
.\venv\Scripts\Activate.ps1

# Set environment variable
$env:PYTHON_PROJECTS_DIR = "$PWD\python_projects"

# Start server as background job
$serverJob = Start-Job -ScriptBlock {
    param($projectPath)
    cd $projectPath
    .\venv\Scripts\Activate.ps1
    $env:PYTHON_PROJECTS_DIR = "$projectPath\python_projects"
    python server\run_http_server.py
} -ArgumentList $PWD

# Start ngrok as background job
$ngrokJob = Start-Job -ScriptBlock {
    ngrok http --region=eu 8000
}

# Wait for server to start
Start-Sleep -Seconds 5

# Get ngrok URL (open http://localhost:4040 in browser)
Start-Process "http://localhost:4040"

# Check job status
Get-Job

# View server output
Receive-Job -Id $serverJob.Id

# To stop the server:
Stop-Job -Id $serverJob.Id
Stop-Job -Id $ngrokJob.Id
Remove-Job -Id $serverJob.Id
Remove-Job -Id $ngrokJob.Id
```

#### Option 3: Using Start-Process (Detached)

```powershell
# Start server in new window (stays open)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $PWD; .\venv\Scripts\Activate.ps1; `$env:PYTHON_PROJECTS_DIR='$PWD\python_projects'; python server\run_http_server.py"

# Start ngrok in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http --region=eu 8000"

# To stop: Close the PowerShell windows or use Task Manager
```

---

## 🧪 Testing

### 1. Test Local Communication (No Internet Required)

This tests the client and server on the same machine using stdio transport.

```bash
# Terminal 1: No need to start server separately for stdio
# Terminal 2: Run test
cd rmi-agent-mcp-server
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
python test_local_communication.py
```

### 2. Test with ngrok (Remote Access)

This tests the client connecting to the server through ngrok.

```bash
# Make sure server and ngrok are running (see "Running the Server" section)
# Then run:
python test_ngrok_connection.py
```

### 3. Manual Testing

```bash
# Test a specific file
python manual_test.py python_projects/hello_world.py

# Test non-existent file (should show error)
python manual_test.py python_projects/nonexistent.py

# Test file with Python error
python manual_test.py python_projects/error_test.py
```

### 4. Unit Tests

```bash
pytest tests/test_server.py -v
```

### 5. Integration Tests

```bash
pytest tests/test_integration.py -v
```

---

## 🤖 LLM-Powered Client

The project includes an **LLM-powered client** (`client/mcp_client_llm.py`) that lets you use **natural language** to execute Python code!

### Natural Language Interface

Instead of manually selecting tools and files, you can chat with an AI that:
1. **Understands your intent** from natural language
2. **Selects the right tool** (run_python or list_python_files)
3. **Chooses the correct file** based on your description
4. **Executes the code** and shows you results
5. **Interprets the output** in human-friendly language

### How It Works

```
You: "Run the hello world program"
         ↓
    LLM analyzes prompt
         ↓
    LLM selects: run_python("python_projects/hello_world.py")
         ↓
    MCP Server executes the file
         ↓
    LLM interprets results
         ↓
AI: "The program executed successfully! Output: Hello, World!"
```

### How the LLM Client Works

#### Understanding API Keys and Model Selection

The LLM client needs two pieces of information:

1. **API Key**: Your authentication token for the LLM service
2. **Model Name**: Which AI model to use (e.g., gpt-4o-mini, gemini-2.5-flash)

**How the client detects them:**

```python
# API Key detection (priority order):
1. Command line: --api-key YOUR_KEY
2. Environment variable: OPENAI_API_KEY
3. Error if neither is found

# Model selection:
1. Command line: --model gpt-4
2. Default: gpt-4o-mini (fast and cost-effective)
```

**Example:**
```bash
# Method 1: Environment variable (recommended)
export OPENAI_API_KEY='sk-proj-...'
python client/mcp_client_llm.py --server server/mcp_server.py

# Method 2: Command line argument
python client/mcp_client_llm.py --server server/mcp_server.py --api-key 'sk-proj-...'

# Method 3: With specific model
export OPENAI_API_KEY='sk-proj-...'
python client/mcp_client_llm.py --server server/mcp_server.py --model gpt-4
```

#### How the LLM Understands Your Prompts

When you type a prompt, the LLM:

1. **Receives your message** - "Run the hello world program"
2. **Analyzes available tools** - Sees `run_python` and `list_python_files`
3. **Reads tool descriptions** - Understands what each tool does
4. **Matches intent to tool** - Realizes you want to execute code
5. **Extracts parameters** - Figures out the file name
6. **Calls the tool** - Executes `run_python("python_projects/hello_world.py")`
7. **Interprets results** - Explains the output in natural language

**The LLM has context about:**
- Available tools and their parameters
- The `python_projects/` directory structure
- Common file names (hello_world.py, calculator.py, error_test.py)
- Python execution concepts (stdout, stderr, exit codes)

### 5 Practical Prompt Examples

#### Example 1: Run a Specific File

**Prompt:**
```
Run the hello world program
```

**What the LLM does:**
1. Identifies intent: Execute Python code
2. Selects tool: `run_python`
3. Determines file: `python_projects/hello_world.py`
4. Executes the file

**Expected Output:**
```
🤖 AI: (Executing tool...)
🔧 Tool: run_python
📝 Arguments: {
  "file_name": "python_projects/hello_world.py"
}
----------------------------------------------------------------------
Hello, World!
This is a test Python file.
MCP Server is working correctly!
----------------------------------------------------------------------

🤖 AI: The program executed successfully! It printed "Hello, World!" 
and confirmed that the MCP Server is working correctly.
```

---

#### Example 2: List Available Files

**Prompt:**
```
What Python files are available?
```

**What the LLM does:**
1. Identifies intent: List files
2. Selects tool: `list_python_files`
3. No parameters needed (uses default directory)
4. Lists all .py files

**Expected Output:**
```
🤖 AI: (Executing tool...)
🔧 Tool: list_python_files
📝 Arguments: {}
----------------------------------------------------------------------
Python files in /path/to/python_projects:
  - calculator.py
  - error_test.py
  - hello_world.py
----------------------------------------------------------------------

🤖 AI: I found 3 Python files:
1. calculator.py - Likely contains mathematical operations
2. error_test.py - Probably tests error handling
3. hello_world.py - The classic hello world program

Would you like me to run any of these?
```

---

#### Example 3: Run and Analyze Results

**Prompt:**
```
Execute calculator.py and tell me what it does
```

**What the LLM does:**
1. Identifies intent: Execute and analyze
2. Selects tool: `run_python`
3. Determines file: `python_projects/calculator.py`
4. Executes and interprets output

**Expected Output:**
```
🤖 AI: (Executing tool...)
🔧 Tool: run_python
📝 Arguments: {
  "file_name": "python_projects/calculator.py"
}
----------------------------------------------------------------------
Calculator Test
========================================
10 + 5 = 15
10 * 5 = 50
3.14 + 2.0 = 5.140000000000001
3.14 * 2.0 = 6.28
========================================
All tests passed!
----------------------------------------------------------------------

🤖 AI: The calculator.py program performs basic arithmetic operations:
- Addition: 10 + 5 = 15
- Multiplication: 10 * 5 = 50
- Floating-point addition: 3.14 + 2.0 = 5.14
- Floating-point multiplication: 3.14 * 2.0 = 6.28

All tests passed successfully! This appears to be a simple calculator 
test suite that validates basic mathematical operations.
```

---

#### Example 4: Handle Errors Gracefully

**Prompt:**
```
Run error_test.py and explain what went wrong
```

**What the LLM does:**
1. Identifies intent: Execute and debug
2. Selects tool: `run_python`
3. Determines file: `python_projects/error_test.py`
4. Executes, captures error, explains issue

**Expected Output:**
```
🤖 AI: (Executing tool...)
🔧 Tool: run_python
📝 Arguments: {
  "file_name": "python_projects/error_test.py"
}
----------------------------------------------------------------------
Starting test...
About to cause an error...
--- stderr ---
Traceback (most recent call last):
  File "/path/to/error_test.py", line 10, in <module>
    undefined_variable
NameError: name 'undefined_variable' is not defined
[Process exited with code 1]
----------------------------------------------------------------------

🤖 AI: The program encountered a NameError. Here's what happened:

**Error:** NameError: name 'undefined_variable' is not defined
**Location:** Line 10 of error_test.py
**Cause:** The code tried to use a variable called 'undefined_variable' 
that was never created or assigned a value.

**How to fix:**
1. Define the variable before using it: `undefined_variable = "some value"`
2. Or remove the line that references it

The program exited with code 1, indicating an error occurred.
```

---

#### Example 5: Conversational Follow-up

**Prompt 1:**
```
Show me all Python files
```

**LLM Response:**
```
🤖 AI: I found 3 Python files:
  - calculator.py
  - error_test.py
  - hello_world.py
```

**Prompt 2 (Follow-up):**
```
Run the calculator one
```

**What the LLM does:**
1. Remembers previous context (knows about calculator.py)
2. Understands "the calculator one" refers to calculator.py
3. Executes the file

**Expected Output:**
```
🤖 AI: (Executing tool...)
🔧 Tool: run_python
📝 Arguments: {
  "file_name": "python_projects/calculator.py"
}
----------------------------------------------------------------------
Calculator Test
========================================
10 + 5 = 15
10 * 5 = 50
...
----------------------------------------------------------------------

🤖 AI: The calculator program ran successfully! All arithmetic 
operations completed correctly.
```

---

### More Prompt Ideas

Here are additional prompts you can try:

- `"Is there a test file I can run?"`
- `"Execute all Python files one by one"`
- `"Run hello_world.py and tell me if it works"`
- `"What's in the python_projects directory?"`
- `"Try running the error test and debug it"`
- `"Compare the output of calculator.py and hello_world.py"`
- `"Run the simplest program you can find"`

### Usage Examples

#### 1. Setup

First, install the OpenAI package and set your API key:

```bash
# Install OpenAI package
pip install openai

# Set API key (Linux/Mac)
export OPENAI_API_KEY='sk-your-key-here'

# Set API key (Windows PowerShell)
$env:OPENAI_API_KEY = "sk-your-key-here"
```

#### 2. Run the LLM Client

**Local server:**
```bash
python client/mcp_client_llm.py --server server/mcp_server.py
```

**Remote server (ngrok):**
```bash
python client/mcp_client_llm.py --server https://your-ngrok-url.ngrok.io/sse
```

**Use specific model:**
```bash
# Use GPT-4
python client/mcp_client_llm.py --server server/mcp_server.py --model gpt-4

# Use Gemini (via OpenAI-compatible API)
python client/mcp_client_llm.py --server server/mcp_server.py --model gemini-2.5-flash
```

#### 3. Example Conversation

```
You: Run the hello world program

🤖 AI: (Executing tool...)
🔧 Tool: run_python
📝 Arguments: {
  "file_name": "python_projects/hello_world.py"
}
----------------------------------------------------------------------
Hello, World!
This is a test Python file.
MCP Server is working correctly!
----------------------------------------------------------------------

🤖 AI: The program executed successfully! It printed "Hello, World!" 
along with a confirmation that the MCP Server is working correctly.

You: Show me all Python files

🤖 AI: (Executing tool...)
🔧 Tool: list_python_files
📝 Arguments: {}
----------------------------------------------------------------------
Python files in /home/ubuntu/rmi-agent-mcp-server/python_projects:
  - calculator.py
  - error_test.py
  - hello_world.py
----------------------------------------------------------------------

🤖 AI: I found 3 Python files in the directory:
1. calculator.py - likely contains mathematical operations
2. error_test.py - probably a test file for error handling
3. hello_world.py - the classic hello world program

Would you like me to run any of these?

You: Run the calculator

🤖 AI: (Executing tool...)
🔧 Tool: run_python
📝 Arguments: {
  "file_name": "python_projects/calculator.py"
}
----------------------------------------------------------------------
Calculator Test
========================================
10 + 5 = 15
10 * 5 = 50
3.14 + 2.0 = 5.140000000000001
3.14 * 2.0 = 6.28
========================================
All tests passed!
----------------------------------------------------------------------

🤖 AI: The calculator program ran successfully! It tested addition and 
multiplication with both integers and floating-point numbers. All tests 
passed correctly.
```

#### 4. Test LLM Tool Selection (Without API Key)

You can test the LLM tool selection logic **without an API key** using the simulation script:

```bash
python test_llm_client.py
```

This demonstrates how the LLM would:
- Parse natural language prompts
- Select appropriate tools
- Extract parameters
- Execute code

**Example output:**
```
Test 1: Run the hello world program
----------------------------------------------------------------------
🤖 LLM selects tool: run_python
📝 LLM extracts args: {
  "file_name": "python_projects/hello_world.py"
}

📤 Result:
Hello, World!
This is a test Python file.
MCP Server is working correctly!

✅ Test 1 PASSED
```

### Supported Models

The LLM client supports any OpenAI-compatible API:

- **OpenAI**: gpt-4o-mini, gpt-4, gpt-3.5-turbo
- **Google Gemini**: gemini-2.5-flash (via OpenAI-compatible endpoint)
- **Anthropic Claude**: claude-3-5-sonnet (via OpenAI-compatible endpoint)
- **Local models**: Any model running with OpenAI-compatible API

### Benefits

✅ **Natural language interface** - No need to remember exact file names
✅ **Intelligent tool selection** - LLM chooses the right tool automatically
✅ **Context-aware** - LLM maintains conversation history
✅ **Error interpretation** - LLM explains errors in human-friendly way
✅ **Interactive debugging** - Ask follow-up questions about results

---

## 🔧 MCP Architecture Explained

### Server Structure (`server/mcp_server.py`)

The server uses **FastMCP**, a Python framework for building MCP servers.

```python
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("RmiAgentMcpServer")

# Define a tool using decorator
@mcp.tool
def run_python(file_name: str) -> str:
    """Execute a Python file and return output."""
    # 1. Validate file path (security)
    # 2. Run Python file using subprocess
    # 3. Capture stdout and stderr
    # 4. Return combined output
    pass

# Run the server
if __name__ == "__main__":
    mcp.run()  # Default: stdio transport
    # or
    mcp.run(transport="sse")  # HTTP/SSE transport
```

**Key Components:**

1. **Tool Definition**: The `@mcp.tool` decorator exposes a Python function as an MCP tool
2. **Input Schema**: FastMCP automatically generates JSON Schema from type hints
3. **Validation**: The `validate_file_path()` function ensures security
4. **Execution**: Uses `subprocess.run()` to execute Python files
5. **Output Capture**: Captures both stdout and stderr
6. **Error Handling**: Returns errors as strings instead of raising exceptions

### Client Structure (`client/mcp_client.py`)

The client uses the **FastMCP Client** to connect to servers.

```python
from fastmcp import Client

class RmiMcpClient:
    def __init__(self, server_url: str):
        self.client = Client(server_url)
    
    async def run_python(self, file_name: str) -> str:
        # Call the tool on the server
        result = await self.client.call_tool("run_python", {"file_name": file_name})
        return result.content[0].text
```

**Key Components:**

1. **Connection**: Client connects to server via URL (stdio, HTTP, or ngrok)
2. **Tool Discovery**: `list_tools()` discovers available tools
3. **Tool Invocation**: `call_tool()` sends JSON-RPC request to server
4. **Result Handling**: Extracts text content from response

### MCP Protocol Flow

```
Client                          Server
  │                               │
  ├──── initialize ──────────────>│
  │<─── initialize response ──────┤
  │                               │
  ├──── tools/list ──────────────>│
  │<─── [run_python, ...] ────────┤
  │                               │
  ├──── tools/call ──────────────>│
  │     {                         │
  │       "name": "run_python",   │
  │       "arguments": {          │
  │         "file_name": "test.py"│
  │       }                       │
  │     }                         │
  │                               │
  │                               ├─> Execute Python
  │                               ├─> Capture output
  │                               │
  │<─── result ────────────────────┤
  │     {                         │
  │       "content": [{           │
  │         "type": "text",       │
  │         "text": "Hello!"      │
  │       }]                      │
  │     }                         │
  │                               │
```

---

## 🤖 Using with LLMs

### Use Case 1: Claude Desktop Integration

**Claude Desktop** is Anthropic's desktop application that supports MCP servers natively.

#### Step 1: Install Claude Desktop

Download from [claude.ai/download](https://claude.ai/download)

#### Step 2: Configure MCP Server

Edit Claude's configuration file:

**Mac/Linux:**
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

Add your server configuration:

```json
{
  "mcpServers": {
    "python-executor": {
      "command": "python",
      "args": [
        "/absolute/path/to/rmi-agent-mcp-server/server/mcp_server.py"
      ],
      "env": {
        "PYTHON_PROJECTS_DIR": "/absolute/path/to/rmi-agent-mcp-server/python_projects"
      }
    }
  }
}
```

**For remote server (via ngrok):**

```json
{
  "mcpServers": {
    "python-executor-remote": {
      "url": "https://your-ngrok-url.ngrok.io/sse",
      "transport": "sse"
    }
  }
}
```

#### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop. The MCP server will be available.

#### Step 4: Use in Claude

In Claude, you can now say:

> "Run the hello_world.py file in my python_projects directory"

Claude will:
1. Discover the `run_python` tool
2. Call it with the file path
3. Receive the output
4. Display it to you

### Use Case 2: API Key as Environment Variable

For programmatic access using LLM APIs (OpenAI, Gemini, etc.), you need to set API keys.

#### Step 1: Get API Key

- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google Gemini**: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- **Anthropic**: [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

#### Step 2: Set Environment Variable

**Linux/Mac (temporary):**
```bash
export OPENAI_API_KEY='sk-...'
export GEMINI_API_KEY='AIza...'
```

**Linux/Mac (permanent - add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows PowerShell (temporary):**
```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:GEMINI_API_KEY = "AIza..."
```

**Windows PowerShell (permanent):**
```powershell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-...', 'User')
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'AIza...', 'User')
```

#### Step 3: Use .env File (Recommended)

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
GEMINI_API_KEY=AIza-your-key-here
PYTHON_PROJECTS_DIR=/home/ubuntu/rmi-agent-mcp-server/python_projects
PYTHON_TIMEOUT=30
```

**Load in Python:**

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

#### Step 4: Example LLM Integration

```python
import os
from openai import OpenAI
from mcp_client import RmiMcpClient

# Initialize OpenAI client
client_llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize MCP client
async with RmiMcpClient("https://your-ngrok-url.ngrok.io/sse") as mcp_client:
    # Get available tools
    tools = await mcp_client.list_tools()
    
    # Ask LLM to use the tool
    response = client_llm.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Run hello_world.py"}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "run_python",
                "description": "Execute a Python file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {"type": "string"}
                    }
                }
            }
        }]
    )
    
    # Execute tool if LLM requests it
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        result = await mcp_client.run_python(
            tool_call.function.arguments["file_name"]
        )
        print(result)
```

---

## 🔒 Security Considerations

1. **Path Validation**: The server only allows access to files within `PYTHON_PROJECTS_DIR`
2. **Timeout Protection**: Python execution is limited to 30 seconds (configurable)
3. **No Shell Escape**: Uses `subprocess.run()` with list arguments, not shell=True
4. **Environment Isolation**: Runs in a controlled environment
5. **ngrok Security**: Free ngrok URLs are public but randomized. Use auth for production.

**For Production:**
- Use ngrok's password protection: `ngrok http --auth="user:pass" 8000`
- Implement API key authentication in the server
- Use HTTPS with proper certificates
- Rate limiting and request validation

---

## 🐛 Troubleshooting

### Server won't start

```bash
# Check if port 8000 is already in use
netstat -tlnp | grep 8000  # Linux
netstat -an | findstr 8000  # Windows

# Kill existing process
kill <PID>  # Linux
Stop-Process -Id <PID>  # Windows
```

### ngrok connection fails

```bash
# Check ngrok status
curl http://localhost:4040/api/tunnels

# Restart ngrok
pkill ngrok  # Linux
Stop-Process -Name ngrok  # Windows
ngrok http --region=eu 8000
```

### Client can't connect

1. Verify server is running: `curl http://localhost:8000/sse`
2. Check ngrok URL is correct
3. Ensure firewall allows connections
4. Try local connection first to isolate issue

### Python file not found

1. Check `PYTHON_PROJECTS_DIR` is set correctly
2. Use absolute paths or paths relative to `PYTHON_PROJECTS_DIR`
3. Verify file exists: `ls python_projects/`

---

## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastMCP**: [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- **Model Context Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **ngrok**: [ngrok.com](https://ngrok.com)
- **Anthropic Claude**: [claude.ai](https://claude.ai)

---

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

**Author**: Based on PRD specification for AI-assisted LaTeX compilation agent, adapted for Python execution.
