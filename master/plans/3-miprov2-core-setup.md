```markdown
# /master/plans/3-miprov2-core-setup.md

# Plan for MIPROv2 Core Agents Setup (Master Module)

## 1. Purpose

This plan outlines the setup and initial implementation of the MIPROv2 *core* agents within the `master` module.  These agents are characterized by:

*   **No External Dependencies (Beyond FastAPI):**  They do *not* use LLMs, DSPy (beyond inspiration for the design), MCP, databases, or any external services.
*   **Deterministic:** Their behavior is entirely predictable based on inputs and internal rules.
*   **FastAPI-Based:** Each agent is a self-contained FastAPI endpoint.

This plan covers:

*   Creating the necessary directory structure within `master/agents/miprov2_core/`.
*   Creating a "hello world" MIPROv2 agent (`miprov2_hello_world_agent.py`) to verify the setup.
*   Creating the routing file (`master/app/routes/routes_miprov2_core.py`).
*   Updating `master/app/main.py` to include the MIPROv2 core routes.
*   Creating a basic test file (`master/tests/test_miprov2_core.py`).
*   Listing the planned MIPROv2 core agents and their purposes.
*   *No* modifications to `requirements.txt` are needed, as we're only using FastAPI and standard Python libraries.

## 2. Overview

This step establishes the foundation for the MIPROv2 core agents.  We'll create a simple "hello world" agent to ensure that the routing and basic structure are working correctly before implementing the more complex agents (Planner, DataPrep, etc.).

## 3. Implementation Steps

### Step 1: Create Directory Structure

Create the following directory structure within `master/agents/`:

```bash
cd master/agents
mkdir miprov2_core
cd miprov2_core
touch __init__.py
cd ../../../
```

### Step 2: Create `miprov2_hello_world_agent.py`

Create the file `master/agents/miprov2_core/miprov2_hello_world_agent.py` with the following content:

```python
# master/agents/miprov2_core/miprov2_hello_world_agent.py
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/miprov2_hello_world", tags=["MIPROv2 Core Agents"])
async def miprov2_hello_world():
    """
    A simple hello world endpoint for testing the MIPROv2 core setup.
    """
    return {"message": "Hello from MIPROv2 Core!"}
```

### Step 3: Create `routes_miprov2_core.py`

Create the file `master/app/routes/routes_miprov2_core.py` with the following content:

```python
# master/app/routes/routes_miprov2_core.py
from fastapi import APIRouter
from agents.miprov2_core.miprov2_hello_world_agent import router as miprov2_hello_world_router

router = APIRouter(prefix="/miprov2")

router.include_router(miprov2_hello_world_router)
# Future MIPROv2 core agents will be added here
```

### Step 4: Update `main.py`

Update `master/app/main.py` to include the `routes_miprov2_core` router:

```python
# master/app/main.py
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, Response
from app.routes.routes_llm import router as llm_router
from app.routes import routes_simple
from app.routes import routes_dspy_integration
from app.routes import routes_dynamic
from app.routes import routes_validation
from app.routes.routes_miprov2_core import router as miprov2_core_router # NEW

app = FastAPI(title="Agent Framework - Master Module")

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Healthy"})

@app.get("/favicon.ico")
async def get_favicon():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#4a90e2"/>
        <text x="2" y="12" font-size="10" fill="white">A</text>
    </svg>'''
    return Response(content=svg.encode('utf-8'), media_type="image/svg+xml")

# Include routers
app.include_router(llm_router)
app.include_router(routes_simple.router, prefix="/simple")
app.include_router(routes_dspy_integration.router, prefix="/dspy")
app.include_router(routes_dynamic.router, prefix="/dynamic")
app.include_router(routes_validation.router, prefix="/validation")
app.include_router(miprov2_core_router) # NEW

```

### Step 5: Create `test_miprov2_core.py`

Create the file `master/tests/test_miprov2_core.py` with the following content:

```python
# master/tests/test_miprov2_core.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app

client = TestClient(app)

def test_miprov2_hello_world():
    """Test the MIPROv2 hello world endpoint."""
    response = client.get("/miprov2/miprov2_hello_world")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from MIPROv2 Core!"}

```

### Step 6: Run Tests

Run the tests from the `master` directory:

```bash
cd master
python -m pytest tests
```

Ensure that the `test_miprov2_hello_world` test (and all other existing tests) pass.

### Step 7:  MIPROv2 Core Agent Descriptions

The following MIPROv2 core agents are planned:

*   **PlannerAgent:**
    *   **Purpose:** Takes a user's request (string) and breaks it down into a predefined sequence of tasks. Uses simple string matching and conditional logic.
    *   **Input:** User request string.
    *   **Output:** List of task strings.
    *   **Example:** Input: "Analyze website traffic data" -> Output: ["Gather data", "Clean data", "Calculate metrics", "Generate report"]

*   **DataPrepAgent:**
    *   **Purpose:** Cleans and transforms input data based on predefined rules.  Uses string manipulation, regular expressions, and type conversions.
    *   **Input:** Data (dictionary or Pydantic model) and optional configuration parameters.
    *   **Output:** Cleaned data (dictionary or Pydantic model).
    *   **Example:** Input: `{"text": "  Hello, World!  ", "to_upper": True}` -> Output: `{"text": "HELLO, WORLD!"}`

*   **AnalyzerAgent:**
    *   **Purpose:** Performs basic statistical or logical analysis on data.  Uses built-in Python functions.
    *   **Input:** Data (dictionary or Pydantic model) and analysis type.
    *   **Output:** Analysis result (number, string, or boolean).
    *   **Example:** Input: `{"numbers": [1, 2, 3, 4, 5], "operation": "average"}` -> Output: `{"result": 3.0}`

*   **EvaluatorAgent:**
    *   **Purpose:** Compares analysis results against predefined criteria. Uses comparison operators and conditional logic.
    *   **Input:** Analysis result and evaluation criteria.
    *   **Output:** Boolean (True/False) indicating whether criteria are met.
    *   **Example:** Input: `{"result": 3.0, "threshold": 2.5, "condition": "greater_than"}` -> Output: `{"passed": True}`

*   **ReportGeneratorAgent:**
    *   **Purpose:** Combines the outputs of the other agents (Planner, DataPrep, Analyzer, Evaluator) into a human-readable report. This agent demonstrates a more complex workflow.
    *   **Input:** User request (string), cleaned data, analysis result, and evaluation result.
    *   **Output:** A formatted report string.

## 4. Pseudocode (for the setup steps - not the individual agents)

```pseudocode
# Create directory
CREATE master/agents/miprov2_core/
CREATE master/agents/miprov2_core/__init__.py

# Create hello world agent
CREATE master/agents/miprov2_core/miprov2_hello_world_agent.py:
    DEFINE FastAPI router
    DEFINE GET endpoint /miprov2_hello_world:
        RETURN {"message": "Hello from MIPROv2 Core!"}

# Create routes file
CREATE master/app/routes/routes_miprov2_core.py:
    DEFINE FastAPI router (prefix="/miprov2")
    IMPORT miprov2_hello_world_router
    INCLUDE miprov2_hello_world_router

# Update main.py
MODIFY master/app/main.py:
    IMPORT miprov2_core_router
    INCLUDE miprov2_core_router

# Create test file
CREATE master/tests/test_miprov2_core.py:
    DEFINE test function test_miprov2_hello_world:
        SEND GET request to /miprov2/miprov2_hello_world
        ASSERT response status code is 200
        ASSERT response body is {"message": "Hello from MIPROv2 Core!"}

# Run tests
RUN pytest tests
```

## 5. Full Code

The full code for each file is provided within the Implementation Steps above.

## 6. Test Plan

The testing strategy for this setup step involves:

*   **Unit Test:** A single unit test (`test_miprov2_hello_world`) in `master/tests/test_miprov2_core.py` verifies the "hello world" agent's functionality.
*   **Verification:** The test checks that the endpoint returns the correct status code (200) and the expected message.
*   **Execution:** Tests are run using `python -m pytest tests` from the `master` directory.

## 7. Logging
Create log file `/master/logs/3-logs.md`
```
This plan provides a clear and actionable guide to setting up the MIPROv2 core agent environment within the `master` module. It includes all the necessary code, directory creation steps, and a basic test to ensure everything is working correctly. It also lists the planned MIPROv2 core agents and their purposes, setting the stage for their individual implementation in subsequent plans. No changes to `requirements.txt` are needed because we are only using FastAPI and standard Python libraries, which should already be present.
