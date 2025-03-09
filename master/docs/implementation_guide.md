# miprov2# MIPROv2 Implementation Guide
Okay, let's update the `implementation_guide.md` for the `master` module, incorporating the "Master + Standalone Modules" approach and the refactoring steps.  I'll also address the routing and agent folder organization. We'll be working exclusively within the `master` directory.

# Master Module Implementation Guide

This guide outlines the implementation and integration of agents within the `master` module of the agent framework.  This module includes *all* agent types (LLM, MIPROv2 Core, MIPROv2 Extended, Simple, etc.) and all dependencies.  It follows a "document-first" approach.

## Core Principles

*   **Document-First:** All steps (planning, implementation, testing, logging) are thoroughly documented *before* code is written.
*   **FastAPI-Based:** Agents are implemented as self-contained FastAPI endpoints.
*   **Modular Design:** Agents and routes are organized into subdirectories for clarity and maintainability.
*   **Comprehensive:** The `master` module includes *all* agent types and features.
*   **Test-Driven:** Each agent has corresponding unit tests.
*   **Detailed Logging:** All development steps and results are recorded in log files.

## Folder Structure

```
master/
├── app/
│   ├── main.py       # FastAPI entry point for the master module
│   ├── routes/       # Organized routing
│   │   ├── __init__.py
│   │   ├── routes_llm.py             # Routes for LLM agents
│   │   ├── routes_miprov2_core.py    # Routes for MIPROv2 Core agents
│   │   ├── routes_miprov2_extended.py # Routes for MIPROv2 Extended agents
│   │   ├── routes_simple.py          # Routes for simple agents
│   │   └── ... other routes ...
│   ├── models.py        # (For future use: data models)
├── agents/
│   ├── __init__.py
│   ├── llm/          # LLM agents (OpenAI, Gemini, etc.)
│   │   ├── __init__.py
│   │   ├── openai_hello.py
│   │   ├── openai_prompt.py
│   │   ├── gemini_hello.py
│   │   ├── gemini_prompt.py
│   │   ├── provider_hello.py
│   │   ├── provider_prompt.py
│   │   ├── sentiment_analyzer_agent.py
│   │   ├── llm_summarization_agent.py
│   │   ├── question_answering.py
│   │   ├── chatbot.py
│   │   ├── research_agent.py
│   │   ├── llm_classifier.py
│   │   └── research_analyzer.py
│   ├── miprov2_core/  # MIPROv2 core agents (no LLM)
│   │   ├── __init__.py
│   │   ├── miprov2_planner_agent.py
│   │   ├── miprov2_data_prep_agent.py
│   │   ├── miprov2_analyzer_agent.py
│   │   ├── miprov2_evaluator_agent.py
│   │   └── miprov2_report_generator_agent.py
│   ├── miprov2_extended/ # MIPROv2 extended agents (with LLM, DSPy, MCP)
│   │   ├── __init__.py
│   │   └── ...
│   ├── simple/        # Simple utility agents
│   │    ├── __init__.py
│   │    ├── hello_world.py
│   │    ├── time.py
│   │    └── quote.py
│   ├── validation/
│   │    ├── __init__.py
│   │    └── ... # Agents requiring validation (if any)
│   └── dspy_integration.py # DSPy integration utilities (if used)
├── tests/
│   ├── __init__.py
│   ├── test_llm.py              # Tests for LLM agents
│   ├── test_miprov2_core.py     # Tests for MIPROv2 Core agents
│   ├── test_miprov2_extended.py # Tests for MIPROv2 Extended agents
│   ├── test_simple.py           # Tests for simple agents
│   └── ... other tests ...
├── docs/         # Documentation for the master module
├── plans/        # Plans for the master module
├── logs/         # Logs for the master module
├── requirements.txt  # ALL dependencies
└── README.md     # README for the master module
```

## Development Workflow

1.  **Plan:** Create a detailed plan document in the `master/plans/` folder.  The plan *must* include:
    *   **Purpose:** A clear description of the agent's functionality.
    *   **Pseudocode:** A step-by-step algorithmic description of the agent's logic.
    *   **Full Code (Single File):** The complete Python code for the FastAPI agent.
    *   **Test Plan:**  A description of the testing strategy, including specific test cases.

2.  **Implement:** Create the agent file in the appropriate subdirectory under `master/agents/` (e.g., `master/agents/llm/my_new_agent.py`).

3.  **Route:**  Add the agent's route to the appropriate routing file in `master/app/routes/` (e.g., `master/app/routes/routes_llm.py`).

4.  **Test:** Write corresponding tests in the appropriate test file under `master/tests/` (e.g., `master/tests/test_llm.py`).

5.  **Log:** Record the results in a log file in `master/logs/`.

6.  **Run Tests:** From the `master` directory:

    ```bash
    cd master
    python -m pytest tests
    ```

7.  **Copy to Standalone Modules (If Applicable):** After successfully implementing and testing in `master`, copy the relevant files (agent, route updates, test cases) to the corresponding standalone modules (e.g., `llm_only`, `miprov2_core`).  Run tests in those modules as well.

## Getting Started (Within `master`)

1.  **Navigate:** `cd master`
2.  **Install Dependencies:** `pip install -r requirements.txt`
3.  **Run Server:** `python -m uvicorn app.main:app --reload`
4.  **Run Tests:** `python -m pytest tests`

## Routing

The `master/app/routes/` directory contains separate routing files for different agent categories:

*   `routes_llm.py`:  For all LLM-based agents (OpenAI, Gemini, etc.).
*   `routes_miprov2_core.py`: For the core MIPROv2 agents (no LLM).
*   `routes_miprov2_extended.py`: For the extended MIPROv2 agents (with LLM, DSPy, MCP).
*   `routes_simple.py`: For simple utility agents.
*   ... and so on ...

This keeps the routing logic organized and prevents the `main.py` file from becoming too large.

## Agent Organization

The `master/agents/` directory uses subdirectories to categorize agents:

*   `llm/`:  All agents that use LLMs.
*   `miprov2_core/`: The core, dependency-free MIPROv2 agents.
*   `miprov2_extended/`: MIPROv2 agents that use LLMs, DSPy, and MCP.
*   `simple/`: Simple utility agents (hello world, time, quote).
*   `validation/`: Agents that perform validation checks.
*   ... and so on ...

## Step 1: Refactor Existing LLM Agents (Example)

This is the first step you outlined. Here's how it would look in practice:

1.  **Create Directories:**

    ```bash
    cd master/agents
    mkdir llm
    mv hello_world.py simple/
    mv time.py simple/
    mv quote.py simple/
    mv *.py llm/ #move all llm agents
    cd llm
    touch __init__.py
    cd ../../
    cd app/routes
    touch __init__.py
    cd ../../
    ```

2.  **Move Agent Files:** Move all existing LLM-related agent files from `master/agents/` to `master/agents/llm/`.  This includes:
    *    `openai_hello.py`
    *    `openai_prompt.py`
    *  ... all other LLM agent files ...
3.  **Create `master/app/routes/routes_llm.py`:** If it doesn't already exist (the original code had a combined file), create it.  If it *does* exist, move its contents to this new file.  The file should look like this:

    ```python
    # master/app/routes/routes_llm.py
    from fastapi import APIRouter
    from agents.llm.openai_hello import router as openai_hello_router
    from agents.llm.openai_prompt import router as openai_prompt_router
    # ... import all other LLM agent routers ...
    from agents.llm.research_analyzer import router as research_analyzer_router

    router = APIRouter(prefix="/llm")

    router.include_router(openai_hello_router)
    router.include_router(openai_prompt_router)
    # ... include all other LLM agent routers ...
    router.include_router(research_analyzer_router)

    ```

4.  **Update `master/app/main.py`:**

    ```python
    # master/app/main.py
    from fastapi import FastAPI, APIRouter
    from fastapi.responses import JSONResponse, Response
    from app.routes.routes_llm import router as llm_router
    # ... import other route files as you create them ...
    from app.routes import routes_simple
    from app.routes import routes_llm

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
    app.include_router(routes_simple.router, prefix="/simple") #added
    # ... include other routers as you create them ...
    ```
5. **Update agents:** add router = APIRouter()
6.  **Update Tests:**  Move the relevant tests from `master/tests/test_llm.py` (if they were in a combined file) to `master/tests/test_llm.py`. Update the import statements in the test file to reflect the new agent locations (e.g., `from agents.llm.openai_hello import ...`).
7. **Create simple agents:** create simple agents and routes.

8.  **Run Tests:**  `cd master; python -m pytest tests`
9.  **Create Log file**

**Step 2 and Beyond:**

You would follow a similar process for refactoring the other agent categories (MIPROv2 Core, Simple, etc.):

*   Create the necessary subdirectories in `master/agents/`.
*   Move the agent files.
*   Create the corresponding `routes_*.py` files in `master/app/routes/`.
*   Update `master/app/main.py` to include the new routers.
*   Update/create the test files in `master/tests/`.

This revised implementation guide and the example refactoring steps provide a clear and actionable plan for organizing your agent framework.  The key is the consistent use of subdirectories for agents and separate routing files. This structure scales well and keeps the codebase organized. Remember to create detailed plans *before* implementing each new agent or refactoring step.
```
```python
# master/app/routes/routes_simple.py
from fastapi import APIRouter
from agents.simple.hello_world import router as hello_world_router
from agents.simple.time import router as time_router
from agents.simple.quote import router as quote_router

router = APIRouter()

router.include_router(hello_world_router)
router.include_router(time_router)
router.include_router(quote_router)
```
```python
# master/agents/simple/hello_world.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/hello_world")
async def read_hello_world():
    """
    Returns a simple hello world message.
    """
    return {"message": "Hello World"}
```
```python
# master/agents/simple/time.py
from fastapi import APIRouter
import datetime

router = APIRouter()

@router.get("/time")
async def read_time():
    """
    Returns the current time in ISO 8601 format.
    """
    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {"current_time": current_time}
```
```python
# master/agents/simple/quote.py
from fastapi import APIRouter
import random

router = APIRouter()

QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "The mind is everything. What you think you become. - Buddha",
    "Life is what happens when you're busy making other plans. - John Lennon",
    "You only live once, but if you do it right, once is enough. - Mae West"
]
@router.get("/quote")
async def read_quote():
    """
    Returns an inspirational quote.
    """
    quote = random.choice(QUOTES)
    return {"quote": quote}
```
```python
# master/tests/test_simple.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app

client = TestClient(app)

def test_hello_world():
    response = client.get("/simple/hello_world")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_time():
    response = client.get("/simple/time")
    assert response.status_code == 200
    assert "current_time" in response.json()  # Basic check for key presence

    # More robust check for ISO 8601 format (optional)
    try:
        datetime.datetime.fromisoformat(response.json()["current_time"])
    except ValueError:
        pytest.fail("Time is not in ISO 8601 format")

def test_quote():
    response = client.get("/simple/quote")
    assert response.status_code == 200
    assert "quote" in response.json()
    assert isinstance(response.json()["quote"], str)  # Check if it's a string

```

```bash
#example log file /master/logs/1-logs.md
# Log for Refactoring LLM Agents and Creating Simple Agents

**Date:** 2024-07-24

**Step:** 1 - Refactor Existing LLM Agents and Create Simple Agents

**Status:** Complete

**Details:**

1.  **Created Directories:**
    *   Created `master/agents/llm/` directory for LLM agents.
    *   Created `master/agents/simple/` directory for simple utility agents.
     *   Created `master/app/routes/__init__.py`.
    *   Created `master/agents/llm/__init__.py`.

2.  **Moved LLM Agent Files:**
    *   Moved all existing LLM agent files (e.g., `openai_hello.py`, `openai_prompt.py`, etc.) from `master/agents/` to `master/agents/llm/`.

3.  **Created `routes_llm.py`:**
    *   Created `master/app/routes/routes_llm.py`.
    *   Imported all LLM agent routers from `master/agents/llm/`.
    *   Included all imported routers in the `llm_router` using `include_router`.

4.  **Updated `main.py`:**
    *   Imported `llm_router` from `master/app/routes/routes_llm.py`.
    *   Included `llm_router` in the FastAPI app using `app.include_router(llm_router, prefix="/llm")`.

5.  **Created Simple Agents:**
    *   Created `master/agents/simple/hello_world.py` with a `/hello_world` endpoint.
    *   Created `master/agents/simple/time.py` with a `/time` endpoint.
    *   Created `master/agents/simple/quote.py` with a `/quote` endpoint.
	* Created `master/app/routes/routes_simple.py`.
    *   Imported all Simple agent routers from `master/agents/simple/`.
    *   Included all imported routers in the `simple_router` using `include_router`.
	*   Imported `simple_router` from `master/app/routes/routes_simple.py`.
    *   Included `simple_router` in the FastAPI app using `app.include_router(simple_router, prefix="/simple")`.

6.  **Updated Tests:**
    *   Created  `master/tests/test_simple.py`.
    *    Added tests for hello_world, time and quote.
    *   Updated `master/tests/test_llm.py`
        *   Updated import statements to reflect new agent locations (e.g., `from agents.llm.openai_hello import ...`).

7.  **Ran Tests:**
    *   Successfully ran `python -m pytest tests` from the `master` directory.  All tests passed.

8. **Updated agents:** Added router = APIRouter()

**Issues Encountered:**

*   None

**Files Created/Modified:**

*   `master/agents/llm/__init__.py`
*   `master/agents/llm/openai_hello.py` (Moved)
*   `master/agents/llm/openai_prompt.py` (Moved)
*   ... (all other LLM agent files - Moved)
*    `master/agents/simple/hello_world.py` (Created)
*    `master/agents/simple/time.py` (Created)
*    `master/agents/simple/quote.py` (Created)
*   `master/app/routes/routes_llm.py` (Created/Modified)
*    `master/app/routes/routes_simple.py` (Created)
*   `master/app/main.py` (Modified)
*   `master/tests/test_llm.py` (Modified)
*   `master/tests/test_simple.py`

**Next Steps:**

*   Step 2: Refactor/create MIPROv2 Core agents.
* Create plans for miprov2 agents
