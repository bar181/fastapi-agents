# app/routes_llm.py
from fastapi import APIRouter, Query
from agents.openai_routes import register_routes as register_openai_routes
from agents.gemini_routes import register_routes as register_gemini_routes

router = APIRouter(prefix="/llm", tags=["LLM Agents"])

# Register routes for OpenAI agent
register_openai_routes(router)

# Register routes for Gemini agent
register_gemini_routes(router)

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
        from agents.openai_agent import OpenAIAgent
        agent = OpenAIAgent()
    else:
        from agents.gemini_agent import GeminiAgent
        agent = GeminiAgent()
    
    result = agent.test_connection(INPUT_TEXT)
    return result