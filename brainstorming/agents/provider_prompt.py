# agents/provider_prompt.py
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from .gemini_agent import GeminiAgent
from .openai_agent import OpenAIAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class ProviderPromptRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt to send to the selected LLM")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
    max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env for the selected provider")

class ProviderPromptAgent:
    """
    Provider Prompt Agent
    -------------------
    Purpose: Send a prompt to either Gemini or OpenAI based on the provider parameter.

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import provider_prompt
        agent = provider_prompt.ProviderPromptAgent()
        result = agent.process({
            "prompt": "Tell me a joke",
            "provider": "gemini",  # or "openai"
            "system_message": "You are a comedian.",
            "max_tokens": 100,
            "temperature": 0.7
        })
        print(result)
    """

    AVAILABLE_PROVIDERS = ["gemini", "openai"]

    def __init__(self):
        self.gemini_agent = None
        self.openai_agent = None
        
        # Initialize agents on demand to avoid unnecessary API key errors
        try:
            self.gemini_agent = GeminiAgent()
        except ValueError:
            pass
            
        try:
            self.openai_agent = OpenAIAgent()
        except ValueError:
            pass

    def process(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt with more options using the selected provider's API.
        
        Args:
            prompt_data: A dictionary containing:
                - prompt: The text prompt to send to the LLM
                - provider: The LLM provider to use (gemini or openai)
                - system_message: (optional) System message to set context
                - max_tokens: (optional) Maximum tokens to generate
                - temperature: (optional) Sampling temperature
                - model: (optional) Model to use, defaults to the model in .env for the selected provider
        
        Returns:
            A dictionary with the response data
        """
        provider = prompt_data.get("provider", "gemini").lower()
        
        if provider not in self.AVAILABLE_PROVIDERS:
            return {
                "status": "error",
                "message": f"Invalid provider: {provider}. Available providers: {', '.join(self.AVAILABLE_PROVIDERS)}",
                "model": "none"
            }
            
        if provider == "openai":
            if not self.openai_agent:
                return {
                    "status": "error",
                    "message": "OpenAI API key not configured",
                    "model": "none"
                }
            # Remove provider from prompt_data before passing to the agent
            prompt_data_copy = prompt_data.copy()
            prompt_data_copy.pop("provider", None)
            return self.openai_agent.process_prompt(prompt_data_copy)
        else:  # gemini
            if not self.gemini_agent:
                return {
                    "status": "error",
                    "message": "Gemini API key not configured",
                    "model": "none"
                }
            # Remove provider from prompt_data before passing to the agent
            prompt_data_copy = prompt_data.copy()
            prompt_data_copy.pop("provider", None)
            return self.gemini_agent.process_prompt(prompt_data_copy)

def register_routes(router: APIRouter):
    """Registers the provider prompt agent's route with the provided APIRouter."""
    
    agent = ProviderPromptAgent()
    
    @router.post("/provider-prompt", summary="Send a prompt to selected LLM provider", tags=["LLM Agents"])
    async def provider_prompt(request: ProviderPromptRequest):
        """
        Send a prompt to either Gemini or OpenAI with additional parameters.
        Gemini is the default provider.
        
        **Input:**

        * **prompt (required, string):** The text prompt to send to the selected LLM
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature
        * **model (optional, string):** Model to use, defaults to the model in .env for the selected provider

        **Process:** Based on the provider parameter, either a `GeminiAgent` or `OpenAIAgent` 
        is instantiated. The `process_prompt` method is called with the request parameters.

        **Available Providers:**
        * gemini (default)
        * openai

        **Example Input (JSON body):**

        ```json
        {
          "prompt": "Tell me a dad joke",
          "provider": "gemini",
          "system_message": "You are a comedian who specializes in dad jokes.",
          "max_tokens": 100,
          "temperature": 0.7
        }
        ```

        **Example Output (Gemini):**

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

        **Example Output (OpenAI):**

        ```json
        {
          "status": "success",
          "message": "Why did the scarecrow win an award? Because he was outstanding in his field!",
          "model": "gpt-4o-mini",
          "usage": {
            "prompt_tokens": 25,
            "completion_tokens": 15,
            "total_tokens": 40
          }
        }
        ```

        **Example Output (if API key is not configured):**

        ```json
        {
          "status": "error",
          "message": "API key not configured",
          "model": "none"
        }
        ```
        """
        result = agent.process(request.model_dump())
        return result