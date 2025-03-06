# llm/agents/sentiment_analyzer_agent.py
from typing import Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class SentimentAnalyzerRequest(BaseModel):
    text: str = Field(..., description="The text to analyze for sentiment")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a sentiment analysis expert.", description="System message to set context")
    max_tokens: Optional[int] = Field(50, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.3, description="Sampling temperature")
    
    @field_validator('text')
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v

class SentimentAnalyzerAgent:
    """
    Sentiment Analyzer Agent
    ----------
    Purpose: Analyze the sentiment of a given text using either Gemini or OpenAI.
    """
    AVAILABLE_PROVIDERS = ["gemini", "openai"]

    def __init__(self, provider: str = "gemini"):
        self.provider = provider.lower()
        if self.provider not in self.AVAILABLE_PROVIDERS:
            raise ValueError(f"Invalid provider: {provider}. Available providers: {', '.join(self.AVAILABLE_PROVIDERS)}")
            
        if self.provider == "openai":
            self.agent = OpenAIAgent()
        else:
            self.agent = GeminiAgent()

    def analyze_sentiment(self, text: str, system_message: str = "You are a sentiment analysis expert.", 
                         max_tokens: int = 50, temperature: float = 0.3) -> Dict[str, Any]:
        """
        Analyze the sentiment of a given text.
        
        Args:
            text: The text to analyze
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the sentiment analysis result
        """
        if not text:
            return {
                "status": "error",
                "message": "Text cannot be empty",
                "model": "none"
            }
        
        # Create a prompt for sentiment analysis
        prompt = f"Analyze the sentiment of the following text and return only one of: positive, negative, or neutral.\n\nText: {text}"
        
        prompt_data = {
            "prompt": prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            result = self.agent.process_prompt(prompt_data)
            
            if result["status"] == "success":
                # Extract just the sentiment label
                sentiment = result["message"].strip().lower()
                # Normalize to one of the three expected values
                if "positive" in sentiment:
                    sentiment = "positive"
                elif "negative" in sentiment:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                return {
                    "status": "success",
                    "sentiment": sentiment,
                    "message": result["message"],
                    "model": result.get("model", "unknown"),
                    "usage": result.get("usage", {})
                }
            else:
                return result
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": "none"
            }

def register_routes(router: APIRouter):
    """
    Register routes for the SentimentAnalyzerAgent.
    """
    @router.post("/sentiment", summary="Analyze text sentiment using LLM", tags=["Advanced LLM Agents"])
    async def analyze_sentiment(request: SentimentAnalyzerRequest):
        """
        Analyze the sentiment of a given text using the selected LLM provider.
        Gemini is the default provider.
        
        **Input:**

        * **text (required, string):** The text to analyze for sentiment
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature

        **Process:** Based on the provider parameter, either a `GeminiAgent` or `OpenAIAgent` 
        is instantiated. The agent analyzes the text and returns a sentiment classification.

        **Available Providers:**
        * gemini (default)
        * openai

        **Example Input (JSON body):**

        ```json
        {
          "text": "I really enjoyed the movie, it was fantastic!",
          "provider": "gemini",
          "system_message": "You are a sentiment analysis expert.",
          "max_tokens": 50,
          "temperature": 0.3
        }
        ```

        **Example Output (Gemini):**

        ```json
        {
          "status": "success",
          "sentiment": "positive",
          "message": "positive",
          "model": "gemini-2.0",
          "usage": {
            "prompt_tokens": 25,
            "completion_tokens": 1,
            "total_tokens": 26,
            "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
          }
        }
        ```

        **Example Output (OpenAI):**

        ```json
        {
          "status": "success",
          "sentiment": "positive",
          "message": "positive",
          "model": "gpt-4o-mini",
          "usage": {
            "prompt_tokens": 25,
            "completion_tokens": 1,
            "total_tokens": 26
          }
        }
        ```

        **Example Output (if text is empty):**

        ```json
        {
          "status": "error",
          "message": "Text cannot be empty",
          "model": "none"
        }
        ```

        **Example Output (if provider is invalid):**

        ```json
        {
          "status": "error",
          "message": "Invalid provider: xyz. Available providers: gemini, openai",
          "model": "none"
        }
        ```
        """
        try:
            agent = SentimentAnalyzerAgent(provider=request.provider)
            result = agent.analyze_sentiment(
                text=request.text,
                system_message=request.system_message,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            return result
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e),
                "model": "none"
            }