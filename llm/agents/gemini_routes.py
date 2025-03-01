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
        model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env or gemini-pro")

    @router.get("/gemini-hello", summary="Test Gemini Hello World", tags=["LLM Agents"])
    async def gemini_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for Gemini")):
        """
        Test endpoint for Gemini integration.
        Returns a simple response from Gemini's API.
        """
        result = agent.test_connection(INPUT_TEXT)
        return result

    @router.post("/gemini-prompt", summary="Send a prompt to Gemini", tags=["LLM Agents"])
    async def gemini_prompt(request: GeminiPromptRequest):
        """
        Send a prompt to Gemini with additional parameters.
        
        - **prompt**: The text prompt to send to Gemini
        - **system_message**: (optional) System message to set context
        - **max_tokens**: (optional) Maximum tokens to generate
        - **temperature**: (optional) Sampling temperature
        - **model**: (optional) Model to use, defaults to the model in .env or gemini-pro
        """
        result = agent.process_prompt(request.model_dump())
        return result