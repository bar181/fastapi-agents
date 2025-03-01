# app/routes_llm.py
from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field
from typing import Optional
from agents.openai_agent import OpenAIAgent
from agents.gemini_agent import GeminiAgent

router = APIRouter(prefix="/llm", tags=["LLM Agents"])

# Define request models
class OpenAIPromptRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt to send to OpenAI")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
    max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    model: Optional[str] = Field(None, description="Model to use, defaults to the model in .env or gpt-4o-mini")

@router.get("/openai-hello", summary="Test OpenAI Hello World")
async def openai_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for OpenAI")):
    """
    Test endpoint for OpenAI integration.
    Returns a simple response from OpenAI's API.
    """
    agent = OpenAIAgent()
    result = agent.test_connection(INPUT_TEXT)
    return result

@router.post("/openai-prompt", summary="Send a prompt to OpenAI")
async def openai_prompt(request: OpenAIPromptRequest):
    """
    Send a prompt to OpenAI with additional parameters.
    
    - **prompt**: The text prompt to send to OpenAI
    - **system_message**: (optional) System message to set context
    - **max_tokens**: (optional) Maximum tokens to generate
    - **temperature**: (optional) Sampling temperature
    - **model**: (optional) Model to use, defaults to the model in .env or gpt-4o-mini
    """
    agent = OpenAIAgent()
    result = agent.process_prompt(request.model_dump())
    return result

@router.get("/gemini-hello", summary="Test Gemini Hello World")
async def gemini_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for Gemini")):
    """
    Test endpoint for Gemini integration.
    This is a placeholder implementation that will be expanded in Step 3.
    """
    agent = GeminiAgent()
    result = agent.test_connection(INPUT_TEXT)
    return result

@router.get("/agent-prompt", summary="Send prompt to selected LLM")
async def agent_prompt(
    INPUT_TEXT: str = Query(..., description="Prompt text for LLM"),
    provider: str = Query("gemini", description="LLM provider: gemini or openai")
):
    """
    Endpoint that sends a prompt to either Gemini or OpenAI.
    Gemini is the default provider.
    This is a placeholder implementation that will be expanded in Step 4.
    """
    if provider.lower() == "openai":
        agent = OpenAIAgent()
    else:
        agent = GeminiAgent()
    
    result = agent.test_connection(INPUT_TEXT)
    return result