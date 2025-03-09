# app/routes_llm.py
from fastapi import APIRouter
from agents.llm.openai_hello import register_routes as register_openai_hello
from agents.llm.openai_prompt import register_routes as register_openai_prompt
from agents.llm.gemini_hello import register_routes as register_gemini_hello
from agents.llm.gemini_prompt import register_routes as register_gemini_prompt
from agents.llm.provider_hello import register_routes as register_provider_hello
from agents.llm.provider_prompt import register_routes as register_provider_prompt
from agents.llm.sentiment_analyzer_agent import register_routes as register_sentiment_analyzer
from agents.llm.question_answering import register_routes as register_question_answering
from agents.llm.llm_summarization_agent import register_routes as register_summarization
from agents.llm.chatbot import register_routes as register_chatbot
from agents.llm.research_agent import register_routes as register_research
from agents.llm.llm_classifier import register_routes as register_llm_classifier
from agents.llm.research_analyzer import register_routes as register_research_analyzer

# Create router without tags to avoid duplicate tags in Swagger
router = APIRouter()

# Register routes for OpenAI agents
register_openai_hello(router)
register_openai_prompt(router)

# Register routes for Gemini agents
register_gemini_hello(router)
register_gemini_prompt(router)

# Register routes for provider selection
register_provider_hello(router)
register_provider_prompt(router)

# Register routes for Advanced LLM Agents
register_sentiment_analyzer(router)
register_question_answering(router)
register_summarization(router)
register_chatbot(router)
register_research(router)
register_llm_classifier(router)
register_research_analyzer(router)