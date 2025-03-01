Below is an updated plan that focuses solely on LLM agents. Please review and let me know if any details need further clarification.

---

# Implementation Guide for LLM Agents Integration

This plan sets up a new folder in a mono repo dedicated to LLM agents. It confirms proper setup and tests while referencing instructions from **docs/llm-guide.md**. Detailed step-by-step instructions reside in the **/plans** folder, and each completed step is logged in the **/logs** folder with file references and next steps.

---

## Folder Structure and Setup

- **New Folder in Mono Repo:**  
  Create a dedicated folder (e.g., `/llm_agents`) that includes:  
  - **/plans:** Step-by-step process for each major integration step  
  - **/logs:** Logs of successful tests and process reviews; include a list of files to be referenced  
  - **/tests:** Automated tests to confirm that endpoints and routes work as expected  

- **Reference Documentation:**  
  Follow instructions in **docs/llm-guide.md** for provider-specific integration details.

---

## Step 1: Environment Setup and Refactoring

- **Dependencies and Environment:**  
  - Install required dependencies for OpenAI and Gemini:  
    ```bash
    pip install openai requests
    ```  
  - Configure environment variables for API keys in your `.env` file.

- **Application Structure:**  
  - Split the main application to extract agent routes into separate files (e.g., `app/routes_llm.py`).  
  - Update the main entry point to include the new LLM agent routes:
    ```python
    from fastapi import FastAPI
    from app.routes_llm import router as llm_router

    app = FastAPI(title="LLM Agents")
    app.include_router(llm_router)
    ```
- **Testing:**  
  - Confirm that tests run correctly via:
    ```bash
    pytest tests/
    ```

---

## Step 2: LLM Connection Setup with OpenAI (Hello World)

- **Create a Test Route:**  
  - Add a routes file (e.g., `app/routes_llm.py`) with an endpoint to test an OpenAI "Hello World" call.
  - Example snippet:
    ```python
    # app/routes_llm.py
    from fastapi import APIRouter, Query
    from agents.openai_agent import OpenAIAgent

    router = APIRouter()

    @router.get("/openai-hello", summary="Test OpenAI Hello World")
    async def openai_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for OpenAI")):
        agent = OpenAIAgent()
        result = agent.test_connection(INPUT_TEXT)
        return result
    ```
- **Agent Implementation:**  
  Create a simple agent in **agents/openai_agent.py** that sends the test prompt to OpenAI:
    ```python
    # agents/openai_agent.py
    import openai
    from os import getenv

    class OpenAIAgent:
        def __init__(self):
            openai.api_key = getenv("OPENAI_API_KEY")

        def test_connection(self, input_text: str):
            # A simple call for testing purposes
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=input_text,
                    max_tokens=5
                )
                return {"result": response.choices[0].text.strip()}
            except Exception as e:
                return {"error": str(e)}
    ```
- **Log and Test:**  
  - Update logs in **/logs** after running tests and verifying a successful OpenAI connection.

---

## Step 3: Gemini Connection Setup and Testing

- **Create Gemini Test Route:**  
  - Add a Gemini test endpoint in the same routes file:
    ```python
    # app/routes_llm.py (continued)
    from agents.gemini_agent import GeminiAgent

    @router.get("/gemini-hello", summary="Test Gemini Hello World")
    async def gemini_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for Gemini")):
        agent = GeminiAgent()
        result = agent.test_connection(INPUT_TEXT)
        return result
    ```
- **Agent Implementation:**  
  Create a simple agent in **agents/gemini_agent.py**:
    ```python
    # agents/gemini_agent.py
    import requests
    from os import getenv

    class GeminiAgent:
        def __init__(self):
            self.api_key = getenv("GEMINI_API_KEY")
            self.endpoint = getenv("GEMINI_ENDPOINT")  # Define in .env

        def test_connection(self, input_text: str):
            try:
                # Placeholder request for Gemini; replace with actual API call as per docs/llm-guide.md
                response = requests.post(
                    self.endpoint,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"prompt": input_text, "max_tokens": 5}
                )
                response.raise_for_status()
                data = response.json()
                return {"result": data.get("text", "").strip()}
            except Exception as e:
                return {"error": str(e)}
    ```
- **Log and Test:**  
  - Confirm Gemini tests run via automated tests.
  - Update logs in **/logs** with test results and file references.

---

## Step 4: Agent for Dynamic LLM Selection

this will include new llm agents - ensure tests work for each.  save to /logs/4-logs.md once the agent is completed and any resolved issues.  

- **Develop Unified Endpoint:**  
  Create an endpoint that sends a prompt to either Gemini or OpenAI. Gemini is the default.
  ```python
  # app/routes_llm.py (continued)
  @router.get("/agent-prompt", summary="Send prompt to selected LLM")
  async def agent_prompt(
      INPUT_TEXT: str = Query(..., description="Prompt text for LLM"),
      provider: str = Query("gemini", description="LLM provider: gemini or openai")
  ):
      if provider.lower() == "openai":
          agent = OpenAIAgent()
          result = agent.test_connection(INPUT_TEXT)
      else:
          agent = GeminiAgent()
          result = agent.test_connection(INPUT_TEXT)
      return result
  ```
- **Test and Log:**  
  - Ensure tests verify the correct provider is used and error handling works.
  - Update **/logs** with file references, outcomes, and next steps.

---

## Final Testing, Documentation, and Release

- **Testing:**  
  - Run comprehensive tests (automated and manual) to validate each endpoint:
    ```bash
    pytest tests/
    ```
- **Documentation Updates:**  
  - Revise **docs/llm-guide.md** to cover integration steps and error handling.
  - Ensure the **/plans** folder includes detailed steps for every integration phase.
  - Update README with usage instructions and endpoint details.
- **Final Commit and Release:**  
  - Confirm that logs in **/logs** and tests in **/tests** are current.
  - Commit changes with clear messages and prepare the folder for public release.

---

## Summary

This plan integrates LLM agents in a new folder within a mono repo. It covers:  
1. Environment setup and folder structure with tests and logs.  
2. LLM connection setup and testing for OpenAI with a simple "Hello World" route.  
3. Gemini integration setup and testing.  
4. Development of a dynamic agent endpoint that sends a prompt to either Gemini or OpenAI (defaulting to Gemini).  
5. Comprehensive testing, logging, and documentation updates.

---

Please confirm if this updated plan aligns with your requirements or if further modifications are needed. Do you have any questions about specific configurations or testing details for Gemini?