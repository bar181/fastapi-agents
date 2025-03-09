```markdown
# /master/plans/4-miprov2-planner-agent.md

# Plan for MIPROv2 Planner Agent (Master Module)

## 1. Purpose

The Planner Agent is the first agent in the MIPROv2 core pipeline. It takes a user's request (as a string) and generates a sequence of tasks (a list of strings) required to fulfill that request. This agent uses simple, rule-based logic (string matching and conditional statements) – *not* an LLM.

## 2. Overview

This agent will be implemented as a FastAPI endpoint (`POST /miprov2/planner`).  It will:

*   Accept a JSON request body containing a `user_request` field (string).
*   Use predefined rules to map the `user_request` to a list of tasks.
*   Return a JSON response body containing a `tasks` field (list of strings).

## 3. Implementation Steps

1.  **Create Agent File:** Create the file `master/agents/miprov2_core/miprov2_planner_agent.py`.

2.  **Define Pydantic Models:**
    *   Create a Pydantic model (`PlannerAgentInput`) for the request body, with a single field: `user_request` (string).
    *   Create a Pydantic model (`PlannerAgentOutput`) for the response body, with a single field: `tasks` (list of strings).

3.  **Implement Planning Logic:**
    *   Create a function `generate_tasks(user_request: str) -> List[str]` that implements the rule-based planning logic.  This function should:
        *   Convert the input `user_request` to lowercase for case-insensitive matching.
        *   Use `if`/`elif`/`else` statements to check for keywords or phrases in the `user_request`.
        *   Based on the matched keywords/phrases, return a predefined list of tasks.
        *   Include a default set of tasks if no keywords are matched.

4.  **Create FastAPI Endpoint:**
    *   Create a FastAPI `router` using `APIRouter()`.
    *   Define a `POST` endpoint at `/miprov2/planner`.
    *   Use the Pydantic models for request and response validation.
    *   Call the `generate_tasks` function to get the task list.
    *   Return the `PlannerAgentOutput` model.
    *   Include comprehensive docstrings for Swagger UI documentation.

5.  **Update `routes_miprov2_core.py`:**
    *   Import the `router` from `miprov2_planner_agent.py`.
    *   Include the imported router in the `router` for `routes_miprov2_core.py` using `include_router`.

6.  **Update `test_miprov2_core.py`:**
    *   Add test cases to verify the Planner Agent's functionality, including:
        *   Various valid user requests with expected task lists.
        *   An empty user request.
        *   A user request with no matching keywords.

## 4. Pseudocode

```pseudocode
# master/agents/miprov2_core/miprov2_planner_agent.py

DEFINE Pydantic model PlannerAgentInput:
    user_request: string

DEFINE Pydantic model PlannerAgentOutput:
    tasks: list of strings

DEFINE FUNCTION generate_tasks(user_request: string) -> list of strings:
    tasks = []
    user_request = user_request.lower()

    IF user_request contains "analyze data":
        tasks = ["Gather data", "Clean data", "Analyze data", "Generate report"]
    ELSE IF user_request contains "write report":
        tasks = ["Outline report", "Gather information", "Write draft", "Review and edit", "Finalize report"]
    ELSE IF user_request contains "create presentation":
        tasks = ["Define audience", "Gather content", "Create slides", "Practice delivery", "Deliver presentation"]
    ELSE:
        tasks = ["Understand request", "Define steps", "Execute steps"] # Default tasks

    RETURN tasks

DEFINE FastAPI router

DEFINE POST endpoint /miprov2/planner (input: PlannerAgentInput, output: PlannerAgentOutput):
    tasks = generate_tasks(input.user_request)
    RETURN PlannerAgentOutput(tasks=tasks)


# master/app/routes/routes_miprov2_core.py

IMPORT router from miprov2_planner_agent
INCLUDE router from miprov2_planner_agent


# master/tests/test_miprov2_core.py

ADD TEST FUNCTION test_planner_agent:
    # Test case 1: "analyze data" request
    SEND POST request to /miprov2/planner with {"user_request": "Analyze data"}
    ASSERT response status code is 200
    ASSERT response body is {"tasks": ["Gather data", "Clean data", "Analyze data", "Generate report"]}

    # Test case 2: "write report" request
    SEND POST request to /miprov2/planner with {"user_request": "Write report"}
    ASSERT response status code is 200
    ASSERT response body is {"tasks": ["Outline report", "Gather information", "Write draft", "Review and edit", "Finalize report"]}

    # ... other test cases ...

    # Test case: empty request
     SEND POST request to /miprov2/planner with {"user_request": ""}
    ASSERT response status code is 200
    ASSERT response body is {"tasks": ["Understand request", "Define steps", "Execute steps"]}
```

## 5. Full Code

```python
# master/agents/miprov2_core/miprov2_planner_agent.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

class PlannerAgentInput(BaseModel):
    """
    Input model for the MIPROv2 Planner Agent.

    Attributes:
        user_request: The user's request (a string describing the overall goal).
    """
    user_request: str = Field(..., description="The user's request string.")

class PlannerAgentOutput(BaseModel):
    """
    Output model for the MIPROv2 Planner Agent.

    Attributes:
        tasks: A list of tasks (strings) generated by the agent.
    """
    tasks: List[str] = Field(..., description="A list of tasks to fulfill the user's request.")

def generate_tasks(user_request: str) -> List[str]:
    """
    Generates a list of tasks based on the user's request.

    This function uses simple rule-based logic (string matching) to
    determine the appropriate tasks.

    Args:
        user_request: The user's request string.

    Returns:
        A list of task strings.
    """
    tasks = []
    user_request = user_request.lower()

    if "analyze data" in user_request:
        tasks = ["Gather data", "Clean data", "Analyze data", "Generate report"]
    elif "write report" in user_request:
        tasks = ["Outline report", "Gather information", "Write draft", "Review and edit", "Finalize report"]
    elif "create presentation" in user_request:
        tasks = ["Define audience", "Gather content", "Create slides", "Practice delivery", "Deliver presentation"]
    elif "research topic" in user_request:
        tasks = ["Identify key aspects", "Gather information", "Synthesize findings", "Present research"]
    else:
        tasks = ["Understand request", "Define steps", "Execute steps"]  # Default tasks

    return tasks

@router.post("/planner", response_model=PlannerAgentOutput, tags=["MIPROv2 Core Agents"])
async def plan_request(input_data: PlannerAgentInput):
    """
    Generates a list of tasks based on a user's request.

    **Input:**

    *   **user_request (str):** The user's request, describing the overall goal (e.g., "Analyze website traffic data").

    **Output:**

    *   **tasks (List[str]):** A list of tasks required to fulfill the request (e.g., ["Gather data", "Clean data", "Analyze data", "Generate report"]).

    **Example Input:**

    ```json
    {
      "user_request": "Analyze website traffic data"
    }
    ```

    **Example Output:**

    ```json
    {
      "tasks": ["Gather data", "Clean data", "Analyze data", "Generate report"]
    }
    ```
    """
    try:
        tasks = generate_tasks(input_data.user_request)
        return PlannerAgentOutput(tasks=tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating tasks: {str(e)}")

```

```python
# master/app/routes/routes_miprov2_core.py (Updated)
from fastapi import APIRouter
from agents.miprov2_core.miprov2_hello_world_agent import router as miprov2_hello_world_router
from agents.miprov2_core.miprov2_planner_agent import router as miprov2_planner_router # NEW

router = APIRouter(prefix="/miprov2")

router.include_router(miprov2_hello_world_router)
router.include_router(miprov2_planner_router) # NEW
# Future MIPROv2 core agents will be added here
```

```python
# master/tests/test_miprov2_core.py (Updated)
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app
from agents.miprov2_core.miprov2_planner_agent import PlannerAgentInput #NEW

client = TestClient(app)

def test_miprov2_hello_world():
    """Test the MIPROv2 hello world endpoint."""
    response = client.get("/miprov2/miprov2_hello_world")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from MIPROv2 Core!"}

def test_planner_agent_analyze_data(): #NEW
    """Test the Planner Agent with an 'analyze data' request."""
    input_data = PlannerAgentInput(user_request="Analyze website traffic data")
    response = client.post("/miprov2/planner", json=input_data.dict())
    assert response.status_code == 200
    expected_tasks = ["Gather data", "Clean data", "Analyze data", "Generate report"]
    assert response.json() == {"tasks": expected_tasks}

def test_planner_agent_write_report(): #NEW
    """Test the Planner Agent with a 'write report' request."""
    input_data = PlannerAgentInput(user_request="Write a report on market trends")
    response = client.post("/miprov2/planner", json=input_data.dict())
    assert response.status_code == 200
    expected_tasks = ["Outline report", "Gather information", "Write draft", "Review and edit", "Finalize report"]
    assert response.json() == {"tasks": expected_tasks}

def test_planner_agent_create_presentation(): #NEW
    """Test the Planner Agent with a 'create presentation' request."""
    input_data = PlannerAgentInput(user_request="Create a presentation on new products")
    response = client.post("/miprov2/planner", json=input_data.dict())
    assert response.status_code == 200
    expected_tasks = ["Define audience", "Gather content", "Create slides", "Practice delivery", "Deliver presentation"]
    assert response.json() == {"tasks": expected_tasks}

def test_planner_agent_empty_request(): #NEW
    """Test the Planner Agent with an empty request."""
    input_data = PlannerAgentInput(user_request="")
    response = client.post("/miprov2/planner", json=input_data.dict())
    assert response.status_code == 200
    expected_tasks = ["Understand request", "Define steps", "Execute steps"]
    assert response.json() == {"tasks": expected_tasks}

def test_planner_agent_unknown_request(): #NEW
    """Test the Planner Agent with an unknown request."""
    input_data = PlannerAgentInput(user_request="Some unknown request")
    response = client.post("/miprov2/planner", json=input_data.dict())
    assert response.status_code == 200
    expected_tasks = ["Understand request", "Define steps", "Execute steps"]
    assert response.json() == {"tasks": expected_tasks}

def test_planner_agent_research_topic(): #NEW
    """Test the Planner Agent with a 'research topic' request."""
    input_data = PlannerAgentInput(user_request="research topic on AI")
    response = client.post("/miprov2/planner", json=input_data.dict())
    assert response.status_code == 200
    expected_tasks =  ["Identify key aspects", "Gather information", "Synthesize findings", "Present research"]
    assert response.json() == {"tasks": expected_tasks}
```

## 6. Test Plan

The `test_miprov2_core.py` file includes comprehensive tests for the Planner Agent:

*   **Positive Tests:** Test cases for "analyze data", "write report", and "create presentation" requests, verifying that the correct task lists are returned.
*   **Edge Cases:** Test cases for an empty user request and an unknown request, ensuring the default task list is returned.
* **Research topic:** Test requests containing "research topic".

For each test case:

*   A `POST` request is sent to `/miprov2/planner` with the appropriate `user_request` in the JSON body.
*   The response status code is checked to be 200 (OK).
*   The response body is checked to contain the expected `tasks` list.

## 7. Logging
Create log file `/master/logs/4-logs.md`.
```

This plan provides a complete and detailed guide for implementing the MIPROv2 Planner Agent, including the agent code, routing, and comprehensive tests. It follows the "document-first" approach, and the code is ready to be implemented directly. The use of Pydantic models ensures type safety and automatic request/response validation. The docstrings are detailed and will generate useful documentation in the Swagger UI.
