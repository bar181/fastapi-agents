# agents/provider_hello.py
from fastapi import APIRouter, Query
from typing import Dict, Any
from .gemini_agent import GeminiAgent
from .openai_agent import OpenAIAgent

class ProviderHelloAgent:
    """
    Provider Hello Agent
    ---------------
    Purpose: Send a prompt to either Gemini or OpenAI based on the provider parameter.

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import provider_hello
        agent = provider_hello.ProviderHelloAgent()
        result = agent.process("Hello World", "gemini")  # or "openai"
        print(result)
    """

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

    def process(self, input_text: str, provider: str = "gemini") -> Dict[str, Any]:
        """
        Process the input text and return a response from the selected provider.
        
        Args:
            input_text: The text to send to the LLM
            provider: The LLM provider to use (gemini or openai)
            
        Returns:
            A dictionary containing the response and status
        """
        if provider.lower() == "openai":
            if not self.openai_agent:
                return {
                    "status": "error",
                    "message": "OpenAI API key not configured",
                    "model": "none"
                }
            return self.openai_agent.test_connection(input_text)
        else:
            if not self.gemini_agent:
                return {
                    "status": "error",
                    "message": "Gemini API key not configured",
                    "model": "none"
                }
            return self.gemini_agent.test_connection(input_text)

def register_routes(router: APIRouter):
    """Registers the provider hello agent's route with the provided APIRouter."""
    
    agent = ProviderHelloAgent()
    
    @router.get("/provider-hello", summary="Send prompt to selected LLM", tags=["LLM Agents"])
    async def provider_hello(
        INPUT_TEXT: str = Query(..., description="Prompt text for LLM"),
        provider: str = Query("gemini", description="LLM provider: gemini or openai")
    ):
        """
        Endpoint that sends a prompt to either Gemini or OpenAI.
        Gemini is the default provider.

        **Input:**

        * **INPUT_TEXT (required, string):** The text prompt to send to the selected LLM provider
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini

        **Process:** Based on the provider parameter, either a `GeminiAgent` or `OpenAIAgent` 
        is instantiated. The `test_connection` method is called with the `INPUT_TEXT`.

        **Example Input (query parameter):**

        `?INPUT_TEXT=Tell me a joke&provider=gemini`

        **Example Output (Gemini):**

        ```json
        {
          "status": "success",
          "message": "Why don't scientists trust atoms? Because they make up everything!",
          "model": "gemini-2.0"
        }
        ```

        **Example Output (OpenAI):**

        ```json
        {
          "status": "success",
          "message": "Why did the scarecrow win an award? Because he was outstanding in his field!",
          "model": "gpt-4o-mini"
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
        result = agent.process(INPUT_TEXT, provider)
        return result