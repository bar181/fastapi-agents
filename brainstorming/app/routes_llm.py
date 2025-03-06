# app/routes_llm.py
from fastapi import APIRouter
from agents.openai_hello import register_routes as register_openai_hello
from agents.openai_prompt import register_routes as register_openai_prompt
from agents.gemini_hello import register_routes as register_gemini_hello
from agents.gemini_prompt import register_routes as register_gemini_prompt
from agents.provider_hello import register_routes as register_provider_hello
from agents.provider_prompt import register_routes as register_provider_prompt
from agents.sentiment_analyzer_agent import register_routes as register_sentiment_analyzer
from agents.question_answering import register_routes as register_question_answering
from agents.llm_summarization_agent import register_routes as register_summarization
from agents.chatbot import register_routes as register_chatbot
from agents.research_agent import register_routes as register_research
from agents.llm_classifier import register_routes as register_llm_classifier
from agents.research_analyzer import register_routes as register_research_analyzer
from agents.openrouter_routes import register_routes as register_openrouter

# Create router without tags to avoid duplicate tags in Swagger
router = APIRouter(prefix="/llm")

# Register routes for OpenAI agents
register_openai_hello(router)
register_openai_prompt(router)

# Register routes for Gemini agents
register_gemini_hello(router)
register_gemini_prompt(router)

# Register routes for provider selection
register_provider_hello(router)
register_provider_prompt(router)

# Register routes for OpenRouter
register_openrouter(router)

# Register routes for Advanced LLM Agents
register_sentiment_analyzer(router)
register_question_answering(router)
register_summarization(router)
register_chatbot(router)
register_research(router)
register_llm_classifier(router)
register_research_analyzer(router)