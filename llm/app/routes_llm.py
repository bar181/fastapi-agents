# app/routes_llm.py
from fastapi import APIRouter, Query
from agents.openai_agent import OpenAIAgent
from agents.gemini_agent import GeminiAgent

router = APIRouter(prefix="/llm", tags=["LLM Agents"])

@router.get("/openai-hello", summary="Test OpenAI Hello World")
async def openai_hello(INPUT_TEXT: str = Query("Hello World", description="Test text for OpenAI")):
    """
    Test endpoint for OpenAI integration.
    This is a placeholder implementation that will be expanded in Step 2.
    """
    agent = OpenAIAgent()
    result = agent.test_connection(INPUT_TEXT)
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