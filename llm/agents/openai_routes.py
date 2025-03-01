# agents/openai_routes.py
from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .openai_agent import OpenAIAgent

def register_routes(router: APIRouter):
    """Registers the OpenAI agent's routes with the provided APIRouter."""
    
    try:
        agent = OpenAIAgent()
    except ValueError as e:
        # If initialization fails, create a dummy agent that returns error messages
        class DummyAgent:
            def test_connection(self, input_text: str):
                return {
                    "status": "error",
                    "message": "OpenAI API key not configured",
                    "model": "none"
                }
            
            def process_prompt(self, prompt_data: Dict[str, Any]):
                return {
                    "status": "error",
                    "message": "OpenAI API key not configured",
                    "model": "none"
                }
        
        agent = DummyAgent()
    
    class OpenAIPromptRequest(BaseModel):
        prompt: str = Field(..., description="The text prompt to send to OpenAI")
        system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
        max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
        temperature: Optional[float] = Field(0.7, description="Sampling temperature")
        model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env or gpt-4o-mini")

    @router.get("/openai-hello", summary="Test OpenAI Hello World", tags=["LLM Agents"])
    async def openai_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for OpenAI")):
        """
        Test endpoint for OpenAI integration.
        Returns a simple response from OpenAI's API.

        **Input:**

        * **INPUT_TEXT (optional, string):** The text to send to OpenAI. Example: Hello World

        **Process:** An instance of the `OpenAIAgent` is used. The `test_connection` 
        method is called with the `INPUT_TEXT`.

        **Example Input (query parameter):**

        `?INPUT_TEXT=Hello World`

        **Example Output:**

        ```json
        {
          "status": "success",
          "message": "Hello! How can I assist you today?",
          "model": "gpt-4o-mini"
        }
        ```

        **Example Output (if API key is not configured):**

        ```json
        {
          "status": "error",
          "message": "OpenAI API key not configured",
          "model": "none"
        }
        ```
        """
        result = agent.test_connection(INPUT_TEXT)
        return result

    @router.post("/openai-prompt", summary="Send a prompt to OpenAI", tags=["LLM Agents"])
    async def openai_prompt(request: OpenAIPromptRequest):
        """
        Send a prompt to OpenAI with additional parameters.
        
        **Input:**

        * **prompt (required, string):** The text prompt to send to OpenAI
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature
        * **model (optional, string):** Model to use, defaults to the model in .env or gpt-4o-mini

        **Process:** An instance of the `OpenAIAgent` is used. The `process_prompt` 
        method is called with the request parameters.

        **Example Input (JSON body):**

        ```json
        {
          "prompt": "Explain quantum computing in simple terms",
          "system_message": "You are a science educator for children.",
          "max_tokens": 150,
          "temperature": 0.7
        }
        ```

        **Example Output:**

        ```json
        {
          "status": "success",
          "message": "Quantum computing is like having a super-fast calculator that can try many answers at once...",
          "model": "gpt-4o-mini",
          "usage": {
            "prompt_tokens": 25,
            "completion_tokens": 120,
            "total_tokens": 145
          }
        }
        ```

        **Example Output (if API key is not configured):**

        ```json
        {
          "status": "error",
          "message": "OpenAI API key not configured",
          "model": "none"
        }
        ```
        """
        result = agent.process_prompt(request.model_dump())
        return result