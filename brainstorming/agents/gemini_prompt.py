# agents/gemini_prompt.py
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .gemini_agent import GeminiAgent

class GeminiPromptRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt to send to Gemini")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
    max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env or gemini-2.0")

class GeminiPromptAgent:
    """
    Gemini Prompt Agent
    ------------------
    Purpose: Send a prompt to Google's Gemini API with additional parameters.

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import gemini_prompt
        agent = gemini_prompt.GeminiPromptAgent()
        result = agent.process({
            "prompt": "Tell me a dad joke",
            "system_message": "You are a comedian who specializes in dad jokes.",
            "max_tokens": 100,
            "temperature": 0.7
        })
        print(result)
    """

    def __init__(self):
        try:
            self.agent = GeminiAgent()
        except ValueError as e:
            self.error = str(e)
            self.agent = None

    def process(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt with more options using Gemini's API.
        
        Args:
            prompt_data: A dictionary containing:
                - prompt: The text prompt to send to Gemini
                - system_message: (optional) System message to set context
                - max_tokens: (optional) Maximum tokens to generate
                - temperature: (optional) Sampling temperature
                - model: (optional) Model to use, defaults to the model in .env or gemini-2.0
        
        Returns:
            A dictionary with the response data
        """
        if not self.agent:
            return {
                "status": "error",
                "message": f"Gemini API key not configured: {self.error}",
                "model": "none"
            }
            
        return self.agent.process_prompt(prompt_data)

def register_routes(router: APIRouter):
    """Registers the Gemini prompt agent's route with the provided APIRouter."""
    
    agent = GeminiPromptAgent()
    
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
        result = agent.process(request.model_dump())
        return result