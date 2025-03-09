# agents/openai_prompt.py
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .openai_agent import OpenAIAgent

class OpenAIPromptRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt to send to OpenAI")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
    max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env or gpt-4o-mini")

class OpenAIPromptAgent:
    """
    OpenAI Prompt Agent
    ------------------
    Purpose: Send a prompt to OpenAI's API with additional parameters.

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import openai_prompt
        agent = openai_prompt.OpenAIPromptAgent()
        result = agent.process({
            "prompt": "Explain quantum computing in simple terms",
            "system_message": "You are a science educator for children.",
            "max_tokens": 150,
            "temperature": 0.7
        })
        print(result)
    """

    def __init__(self):
        try:
            self.agent = OpenAIAgent()
        except ValueError as e:
            self.error = str(e)
            self.agent = None

    def process(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt with more options using OpenAI's API.
        
        Args:
            prompt_data: A dictionary containing:
                - prompt: The text prompt to send to OpenAI
                - system_message: (optional) System message to set context
                - max_tokens: (optional) Maximum tokens to generate
                - temperature: (optional) Sampling temperature
                - model: (optional) Model to use, defaults to the model in .env or gpt-4o-mini
        
        Returns:
            A dictionary with the response data
        """
        if not self.agent:
            return {
                "status": "error",
                "message": f"OpenAI API key not configured: {self.error}",
                "model": "none"
            }
            
        return self.agent.process_prompt(prompt_data)

def register_routes(router: APIRouter):
    """Registers the OpenAI prompt agent's route with the provided APIRouter."""
    
    agent = OpenAIPromptAgent()
    
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
        result = agent.process(request.model_dump())
        return result