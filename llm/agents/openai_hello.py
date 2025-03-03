# agents/openai_hello.py
from fastapi import APIRouter, Query
from typing import Dict, Any
from .openai_agent import OpenAIAgent

class OpenAIHelloAgent:
    """
    OpenAI Hello Agent
    -----------------
    Purpose: Test the connection to OpenAI's API with a simple text generation request.

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import openai_hello
        agent = openai_hello.OpenAIHelloAgent()
        result = agent.process("Hello World")
        print(result)
    """

    def __init__(self):
        try:
            self.agent = OpenAIAgent()
        except ValueError as e:
            self.error = str(e)
            self.agent = None

    def process(self, input_text: str) -> Dict[str, Any]:
        """
        Process the input text and return a response from OpenAI.
        
        Args:
            input_text: The text to send to OpenAI
            
        Returns:
            A dictionary containing the response and status
        """
        if not self.agent:
            return {
                "status": "error",
                "message": f"OpenAI API key not configured: {self.error}",
                "model": "none"
            }
            
        return self.agent.test_connection(input_text)

def register_routes(router: APIRouter):
    """Registers the OpenAI hello agent's route with the provided APIRouter."""
    
    agent = OpenAIHelloAgent()
    
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
        result = agent.process(INPUT_TEXT)
        return result