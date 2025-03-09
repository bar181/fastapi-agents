# step 1 miprov2 setup

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