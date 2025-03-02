# app/routes_llm.py
from fastapi import APIRouter
from agents.openai_hello import register_routes as register_openai_hello
from agents.openai_prompt import register_routes as register_openai_prompt
from agents.gemini_hello import register_routes as register_gemini_hello
from agents.gemini_prompt import register_routes as register_gemini_prompt
from agents.provider_hello import register_routes as register_provider_hello
from agents.provider_prompt import register_routes as register_provider_prompt
from agents.sentiment_analyzer_agent import register_routes as register_sentiment_analyzer
from agents.question_answering_routes import register_routes as register_question_answering

router = APIRouter(prefix="/llm", tags=["LLM Agents"])

# Register routes for OpenAI agents
register_openai_hello(router)
register_openai_prompt(router)

# Register routes for Gemini agents
register_gemini_hello(router)
register_gemini_prompt(router)

# Register routes for provider selection
register_provider_hello(router)
register_provider_prompt(router)

# Register routes for Sentiment Analyzer
register_sentiment_analyzer(router)

# Register routes for Question Answering
register_question_answering(router)