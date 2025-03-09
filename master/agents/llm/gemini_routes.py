# agents/gemini_routes.py
from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .gemini_agent import GeminiAgent

def register_routes(router: APIRouter):
    """Registers the Gemini agent's routes with the provided APIRouter."""
    
    try:
        agent = GeminiAgent()
    except ValueError as e:
        # If initialization fails, create a dummy agent that returns error messages
        class DummyAgent:
            def test_connection(self, input_text: str):
                return {
                    "status": "error",
                    "message": "Gemini API key not configured",
                    "model": "none"
                }
            
            def process_prompt(self, prompt_data: Dict[str, Any]):
                return {
                    "status": "error",
                    "message": "Gemini API key not configured",
                    "model": "none"
                }
        
        agent = DummyAgent()
    
    class GeminiPromptRequest(BaseModel):
        prompt: str = Field(..., description="The text prompt to send to Gemini")
        system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
        max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
        temperature: Optional[float] = Field(0.7, description="Sampling temperature")
        model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env or gemini-2.0")

    @router.get("/gemini-hello", summary="Test Gemini Hello World", tags=["LLM Agents"])
    async def gemini_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for Gemini")):
        """
        Test endpoint for Gemini integration.
        Returns a simple response from Gemini's API.

        **Input:**

        * **INPUT_TEXT (optional, string):** The text to send to Gemini. Example: Hello World

        **Process:** An instance of the `GeminiAgent` is used. The `test_connection` 
        method is called with the `INPUT_TEXT`.

        **Example Input (query parameter):**

        `?INPUT_TEXT=Hello World`

        **Example Output:**

        ```json
        {
          "status": "success",
          "message": "Hello! I'm Gemini, a large language model. How can I help you today?",
          "model": "gemini-2.0"
        }
        ```

        **Example Output (if API key is not configured):**

        ```json
        {
          "status": "error",
          "message": "Gemini API key not configured",
          "model": "none"
        }
        ```
        """
        result = agent.test_connection(INPUT_TEXT)
        return result

    @router.post("/gemini-prompt", summary="Send a prompt to Gemini", tags=["LLM Agents"])
    async def gemini_prompt(request: GeminiPromptRequest):
        """
        Send a prompt to Gemini with additional parameters.
        
        **Input:**

        * **prompt (required, string):** The text prompt to send to Gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature
        * **model (optional, string):** Model to use, defaults to the model in .env or gemini-2.0

        **Process:** An instance of the `GeminiAgent` is used. The `process_prompt` 
        method is called with the request parameters.

        **Example Input (JSON body):**

        ```json
        {
          "prompt": "Tell me a dad joke",
          "system_message": "You are a comedian who specializes in dad jokes.",
          "max_tokens": 100,
          "temperature": 0.7
        }
        ```

        **Example Output:**

        ```json
        {
          "status": "success",
          "message": "Why don't scientists trust atoms? Because they make up everything!",
          "model": "gemini-2.0",
          "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 12,
            "total_tokens": 32,
            "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
          }
        }
        ```

        **Example Output (if API key is not configured):**

        ```json
        {
          "status": "error",
          "message": "Gemini API key not configured",
          "model": "none"
        }
        ```
        """
        result = agent.process_prompt(request.model_dump())
        return result