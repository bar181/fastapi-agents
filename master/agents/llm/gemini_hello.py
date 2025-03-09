# agents/gemini_hello.py
from fastapi import APIRouter, Query
from typing import Dict, Any
from .gemini_agent import GeminiAgent

class GeminiHelloAgent:
    """
    Gemini Hello Agent
    -----------------
    Purpose: Test the connection to Google's Gemini API with a simple text generation request.

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import gemini_hello
        agent = gemini_hello.GeminiHelloAgent()
        result = agent.process("Hello World")
        print(result)
    """

    def __init__(self):
        try:
            self.agent = GeminiAgent()
        except ValueError as e:
            self.error = str(e)
            self.agent = None

    def process(self, input_text: str) -> Dict[str, Any]:
        """
        Process the input text and return a response from Gemini.
        
        Args:
            input_text: The text to send to Gemini
            
        Returns:
            A dictionary containing the response and status
        """
        if not self.agent:
            return {
                "status": "error",
                "message": f"Gemini API key not configured: {self.error}",
                "model": "none"
            }
            
        return self.agent.test_connection(input_text)

def register_routes(router: APIRouter):
    """Registers the Gemini hello agent's route with the provided APIRouter."""
    
    agent = GeminiHelloAgent()
    
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
        result = agent.process(INPUT_TEXT)
        return result