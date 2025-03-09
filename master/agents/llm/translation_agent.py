# llm/agents/translation_agent.py
from typing import Dict, Any
from fastapi import APIRouter
from .openai_agent import OpenAIAgent

class TranslationAgent:
    """
    Translation Agent
    ----------
    Purpose: Translate text between languages using OpenAI.
