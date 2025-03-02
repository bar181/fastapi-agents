# llm/agents/sentiment_analyzer_agent.py
from typing import Dict, Any
from fastapi import APIRouter
from .openai_agent import OpenAIAgent

class SentimentAnalyzerAgent:
    """
    Sentiment Analyzer Agent
    ----------
    Purpose: Analyze the sentiment of a given text using OpenAI.
    """

    def __init__(self):
        self.openai_agent = OpenAIAgent()

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt to analyze the sentiment of a given text.
        
        Args:
            prompt_data: A dictionary containing:
                - text: The text to analyze
                - model: (optional) Model to use, defaults to the model in .env or gpt-4o-mini
        
        Returns:
            A dictionary with the sentiment analysis result
        """
        try:
            text = prompt_data.get("text", "")
            model = prompt_data.get("model", self.openai_agent.default_model)
            
            # Validate input
            if not text:
                return {
                    "status": "error",
                    "message": "Text cannot be empty",
                    "model": model
                }
            
            # Create a prompt for sentiment analysis
            prompt = f"Analyze the sentiment of the following text and return only one of: positive, negative, or neutral. Text: {text}"
            
            # Use OpenAI agent to process the prompt
            result = self.openai_agent.process_prompt({
                "prompt": prompt,
                "model": model
            })
            
            return {
                "status": "success",
                "sentiment": result["message"].strip().lower(),
                "model": model
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": model if 'model' in locals() else self.openai_agent.default_model
            }

def register_routes(router: APIRouter):
    """
    Register routes for the SentimentAnalyzerAgent.
    """
    agent = SentimentAnalyzerAgent()

    @router.post("/sentiment", tags=["Sentiment Analysis"])
    async def analyze_sentiment(prompt_data: Dict[str, Any]):
        """
        Analyze the sentiment of a given text.
        """
        return agent.process_prompt(prompt_data)