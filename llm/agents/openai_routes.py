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
        """
        result = agent.test_connection(INPUT_TEXT)
        return result

    @router.post("/openai-prompt", summary="Send a prompt to OpenAI", tags=["LLM Agents"])
    async def openai_prompt(request: OpenAIPromptRequest):
        """
        Send a prompt to OpenAI with additional parameters.
        
        - **prompt**: The text prompt to send to OpenAI
        - **system_message**: (optional) System message to set context
        - **max_tokens**: (optional) Maximum tokens to generate
        - **temperature**: (optional) Sampling temperature
        - **model**: (optional) Model to use, defaults to the model in .env or gpt-4o-mini
        """
        result = agent.process_prompt(request.model_dump())
        return result