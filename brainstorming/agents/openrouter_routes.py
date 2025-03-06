# agents/openrouter_routes.py
from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .openrouter_agent import OpenRouterAgent

def register_routes(router: APIRouter):
    """Registers the OpenRouter agent's routes with the provided APIRouter."""
    
    try:
        agent = OpenRouterAgent()
    except ValueError as e:
        # If initialization fails, create a dummy agent that returns error messages
        class DummyAgent:
            def test_connection(self, input_text: str):
                return {
                    "status": "error",
                    "message": "OpenRouter API key not configured",
                    "model": "none"
                }
            
            def process_prompt(self, prompt_data: Dict[str, Any]):
                return {
                    "status": "error",
                    "message": "OpenRouter API key not configured",
                    "model": "none"
                }
        
        agent = DummyAgent()
    
    class OpenRouterPromptRequest(BaseModel):
        prompt: str = Field(..., description="The text prompt to send to OpenRouter")
        system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
        max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
        temperature: Optional[float] = Field(0.7, description="Sampling temperature")
        model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env or openai/o3-mini-high")

    @router.get("/openrouter-hello", summary="Test OpenRouter Hello World", tags=["LLM Agents"])
    async def openrouter_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for OpenRouter")):
        """
        Test endpoint for OpenRouter integration.
        Returns a simple response from OpenRouter's API.

        **Input:**

        * **INPUT_TEXT (optional, string):** The text to send to OpenRouter. Example: Hello World

        **Process:** An instance of the `OpenRouterAgent` is used. The `test_connection` 
        method is called with the `INPUT_TEXT`.

        **Example Input (query parameter):**

        `?INPUT_TEXT=Hello World`

        **Example Output:**

        ```json
        {
          "status": "success",
          "message": "Hello! How can I assist you today?",
          "model": "openai/o3-mini-high"
        }
        ```

        **Example Output (if API key is not configured):**

        ```json
        {
          "status": "error",
          "message": "OpenRouter API key not configured",
          "model": "none"
        }
        ```
        """
        result = agent.test_connection(INPUT_TEXT)
        return result

    @router.post("/openrouter-prompt", summary="Send a prompt to OpenRouter", tags=["LLM Agents"])
    async def openrouter_prompt(request: OpenRouterPromptRequest):
        """
        Send a prompt to OpenRouter with additional parameters.
        
        **Input:**

        * **prompt (required, string):** The text prompt to send to OpenRouter
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature
        * **model (optional, string):** Model to use, defaults to the model in .env or openai/o3-mini-high

        **Process:** An instance of the `OpenRouterAgent` is used. The `process_prompt` 
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
          "model": "openai/o3-mini-high",
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
          "message": "OpenRouter API key not configured",
          "model": "none"
        }
        ```
        """
        result = agent.process_prompt(request.model_dump())
        return result