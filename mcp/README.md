# Fastapi MCP Agents

A FastAPI-based agent system that integrates the Model Context Protocol (MCP) for enhanced context sharing between agents. This project features intelligent agents with advanced DSPy functionality for dynamic, context-aware responses.

# Fastapi MCP Agents

A FastAPI-based agent system that implements the Model Context Protocol (MCP) for context sharing and state management between agents. This project showcases multi-step reasoning, workflow coordination, and decisioning capabilities through a set of specialized MCP agents.

---

## Features

- Dynamic agent loading and execution with dedicated endpoints
- MCP integration for enhanced context sharing and state management
- Advanced DSPy-powered classifier agent for text categorization
- Specialized MCP agents for different use cases:
  - Calculator agent for arithmetic expression evaluation
  - Multi-step reasoning agent for iterative hypothesis refinement
  - Workflow coordinator agent for sub-agent orchestration
  - Workflow decisioning agent for task-based agent selection
- Interactive Swagger UI documentation with detailed examples
- Agent listing and discovery endpoint
- Health check endpoint
- Comprehensive test suite with mocking and error handling

---

## Project Structure

```
mcp-llm-agents/
├─ app/
│   ├─ main.py           # FastAPI application entrypoint
│   ├─ routes.py         # Dedicated routes for agent endpoints
│   ├─ mcp_adapter.py    # MCP adapter for context sharing between agents
│   └─ models.py         # Data models for the API
├─ agents/
│   ├─ __init__.py       # Package initializer
│   ├─ dspy_integration.py # DSPy integration utilities
│   ├─ hello_world.py    # Basic Hello World agent
│   ├─ classifier.py     # Advanced dspy showcase: Classifier agent
│   ├─ calculator.py     # MCP agent: Evaluates arithmetic expressions
│   ├─ multi_step_reasoning.py # MCP agent: Iterative hypothesis refinement
│   ├─ workflow_coordinator.py # MCP agent: Coordinates multiple sub-agents
│   ├─ workflow_decisioning.py # MCP agent: Makes decisions based on task descriptions
│   ├─ time.py           # Simple Time agent
│   └─ quote.py          # Simple Quote agent
├─ docs/                # Documentation files
│   ├─ Implementation_Guide.md # Setup and usage instructions
│   ├─ MCP_Integration.md # MCP integration documentation
│   └─ Technical_Specifications.md # Endpoint and data model details
├─ logs/                # Development logs
│   ├─ 1-logs.md        # Initial setup logs
│   ├─ 2-logs.md        # MCP setup logs
│   ├─ 3-logs.md        # MCP agents implementation logs
│   ├─ 4-mcp-transfer.md # MCP transfer logs
│   ├─ 5-step2.md       # MCP integration step 2 logs
│   ├─ 6-swagger.md     # Swagger UI documentation logs
│   └─ 7-other-tests.md # Test updates logs
├─ plans/               # Detailed plans for each development phase
│   ├─ 1-frameworks.md  # Framework setup plan
│   ├─ 2-mcp-setup.md   # MCP setup plan
│   └─ 3-mcp-agents.md  # MCP agents implementation plan
├─ tests/               # Test suite
│   ├─ test_dspy_agents.py # Tests for DSPy agents
│   ├─ test_main.py     # Tests for core application endpoints
│   ├─ test_mcp.py      # Tests for MCP adapter
│   ├─ test_mcp_agents.py # Tests for MCP agents
│   └─ test_starter_agents.py # Tests for starter agents
├─ static/              # Static files
│   └─ favicon.ico      # Favicon
├─ requirements.txt     # Dependencies
└─ LICENSE              # MIT License
```

---

## Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root with your API keys and configuration (for MCP and LLM integrations):

```env
# MCP Configuration
MCP_API_KEY=your_mcp_api_key
MCP_ENDPOINT=your_mcp_endpoint_url

# Example:
# MCP_API_KEY=abc123
# MCP_ENDPOINT=http://localhost:5000/mcp
```

Both `MCP_API_KEY` and `MCP_ENDPOINT` are required for the MCP adapter to function properly. If these environment variables are not set, the MCP adapter will still initialize but will operate in a degraded mode, returning the original context data without sending it to the MCP endpoint.

### Run the Server

```bash
uvicorn app.main:app --reload
```
2. Choose a module and navigate to its directory:
```bash
cd dspy  # or starter or base-framework
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
# Using the Python -m flag for proper module resolution
python -m uvicorn app.main:app --reload
```
## Running Tests

Navigate to the specific module directory and run:
```bash
# Using the Python -m flag for proper module resolution
python -m pytest tests
```
5. Test the endpoints:

Core Endpoints:
- Welcome message: GET /
- Health check: GET /health
- List all agents: GET /agents
---

## API Endpoints

### Core Endpoints

- **Welcome Message:** GET `/`
- **Health Check:** GET `/health`
- **List All Agents:** GET `/agents`

### Dedicated Agent Endpoints

- **Dynamic Agent Execution:** GET `/agent/{agent_name}`
  Loads and executes an agent by its file name.

- **Quote Agent:** GET `/agent/quote`
  Returns an inspirational quote.

- **Classifier Agent:** GET `/classifier?INPUT_TEXT=Hello,%20how%20are%20you?`
  Classifies input text into categories with a confidence score.


### MCP Agents

The MCP integration enables advanced context sharing and inter-module communication between agents. These agents showcase different aspects of MCP functionality:

✅ **Calculator Agent**
   - **Purpose**: Evaluates arithmetic expressions with context sharing via MCP.
   - **Features**: Safely evaluates expressions and maintains context between calls.
   - **Endpoint**: POST `/agents/calculator`
   - **Example**: `{"expression": "3 + 4 * 2"}`

✅ **Multi-Step Reasoning Agent**
   - **Purpose**: Iteratively refines a hypothesis through context updates.
   - **Features**: Demonstrates advanced reasoning capabilities using MCP for state management.
   - **Endpoint**: POST `/agents/multi_step_reasoning`
   - **Example**: `{"hypothesis": "The Earth is flat"}`

✅ **Workflow Coordinator Agent**
   - **Purpose**: Coordinates and aggregates responses from multiple sub-agents.
   - **Features**: Simulates a workflow where multiple sub-agents contribute to a final decision or report.
   - **Endpoint**: POST `/agents/workflow_coordinator`
   - **Example**: `{}`

✅ **Workflow Decisioning Agent**
   - **Purpose**: Makes intelligent workflow decisions based on task descriptions.
   - **Features**: Selects and executes sub-agents based on keywords in the task description.
   - **Endpoint**: POST `/agents/workflow_decisioning`
   - **Example**: `{"task_description": "Please analyze and report the data"}`

For detailed documentation on MCP integration, see `/docs/MCP_Integration.md`.

## Swagger UI Documentation

The API is fully documented using Swagger UI, which provides an interactive interface for exploring and testing the endpoints. The documentation includes:

- Detailed descriptions of each endpoint
- Request and response schemas
- Example requests and responses
- Categorization of endpoints by tags (e.g., "MCP Agents", "Dspy Agents")

To access the Swagger UI documentation:

1. Start the server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/docs
   ```

The Swagger UI provides a convenient way to test the endpoints directly from the browser, making it easy to understand and use the API.

---

## Running Tests

Execute the test suite with:

```bash
# Using the Python -m flag for proper module resolution
python -m pytest tests/
```

### Test Suite Overview

The project includes a comprehensive test suite that covers various aspects of the system:

1. **MCP Agent Tests** (`tests/test_mcp_agents.py`):
   - Tests for all MCP agents (calculator, multi-step reasoning, workflow coordinator, workflow decisioning)
   - Verifies correct response structures and functionality
   - Uses mocked MCP adapter for isolated testing

2. **MCP Adapter Tests** (`tests/test_mcp.py`):
   - Tests for the MCPAdapter class
   - Verifies initialization with and without environment variables
   - Tests context sending and response retrieval
   - Tests agent integration with the MCP adapter

3. **DSPy Agent Tests** (`tests/test_dspy_agents.py`):
   - Tests for the classifier agent
   - Verifies correct classification of different types of input
   - Tests error handling for invalid input

4. **Main Application Tests** (`tests/test_main.py`):
   - Tests for core application endpoints
   - Verifies health check and welcome message

5. **Starter Agent Tests** (`tests/test_starter_agents.py`):
   - Tests for basic starter agents

To run specific test files:

```bash
# Run only MCP agent tests
python -m pytest tests/test_mcp_agents.py

# Run only MCP adapter tests
python -m pytest tests/test_mcp.py

# Run only DSPy agent tests
python -m pytest tests/test_dspy_agents.py
```

To run tests with verbose output:

```bash
python -m pytest tests/ -v
```

---

## Documentation

- **Implementation Guide:** Detailed setup and usage instructions are in `/docs/Implementation_Guide.md`.
- **Technical Specifications:** See `/docs/Technical_Specifications.md` for endpoint and data model details.
- **Testing Documentation:** Refer to `/docs/Testing_and_Validation.md`.
- **Additional Plans:** See the `/plans` folder for phase-specific implementation guides.

---

## Documentation First Coding

This repository was created using Documentation First Coding methodologies:

1. **Brainstorm and Design:**  
   All ideas and designs were thoroughly documented.
2. **Required Documentation:**  
   Technical and implementation documents are maintained in the `/docs` directory.
3. **Phase Plans:**  
   Detailed plans for each development phase are available in the `/plans` folder.
4. **Step-by-Step Execution:**  
   Development followed outlined steps with comprehensive testing.
5. **Tracking and Logging:**  
   Progress was tracked in the `/logs` directory.
6. **Testing and Updates:**  
   The project includes a complete test suite and regularly updated documentation.

---

## Easter Egg

```
go install github.com/boyter/scc@latest
scc .

```

---


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Original Gist:**  
[https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd](https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd)

**Author:** Bradley Ross (bar181 on GitHub and Gists)
```
