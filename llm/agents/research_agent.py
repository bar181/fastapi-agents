# llm/agents/research_agent.py
from typing import Dict, Any, Optional, List
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class ResearchRequest(BaseModel):
    query: str = Field(..., description="The research query to analyze")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a research assistant.", description="System message to set context")
    max_tokens: Optional[int] = Field(150, description="Maximum tokens for each analysis")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    
    @field_validator('query')
    def query_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Research query cannot be empty')
        return v

class ResearchAgent:
    """
    Multi-Step Research Agent
    ----------
    Purpose: Conduct multi-step research by extracting topics from a query, 
    analyzing each topic, and aggregating the results.
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

    def extract_topics(self, query: str, system_message: str = "You are a research assistant.", 
                     max_tokens: int = 60, temperature: float = 0.7) -> List[str]:
        """
        Extract key topics from the research query.
        
        Args:
            query: The research query
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A list of extracted topics
        """
        prompt = (
            f"Extract 3-5 key topics from the following research query. "
            f"Return ONLY a comma-separated list of topics, with no numbering or additional text.\n\n"
            f"Research query: {query}"
        )
        
        prompt_data = {
            "prompt": prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                topics = response["message"].strip().split(',')
                return [topic.strip() for topic in topics if topic.strip()]
            return ["No topics extracted"]
        except Exception as e:
            return [f"Error extracting topics: {str(e)}"]

    def analyze_topic(self, topic: str, system_message: str = "You are a research analyst.", 
                    max_tokens: int = 150, temperature: float = 0.7) -> str:
        """
        Provide a detailed analysis on a specific topic.
        
        Args:
            topic: The topic to analyze
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A detailed analysis of the topic
        """
        prompt = f"Provide a detailed analysis on the following topic:\n\n{topic}"
        
        prompt_data = {
            "prompt": prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                return response["message"].strip()
            return f"Could not analyze topic: {topic}"
        except Exception as e:
            return f"Error analyzing topic {topic}: {str(e)}"

    def aggregate_results(self, topics: List[str], analyses: List[str], 
                         system_message: str = "You are a research assistant.", 
                         max_tokens: int = 200, temperature: float = 0.7) -> str:
        """
        Aggregate the individual topic analyses into a comprehensive summary.
        
        Args:
            topics: List of topics
            analyses: List of analyses corresponding to the topics
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A comprehensive summary of the research
        """
        # Create a combined text of topics and their analyses
        combined_analyses = ""
        for i, (topic, analysis) in enumerate(zip(topics, analyses)):
            combined_analyses += f"Topic {i+1}: {topic}\nAnalysis: {analysis}\n\n"
        
        prompt = (
            f"Create a comprehensive summary that synthesizes the following topic analyses "
            f"into a cohesive research overview:\n\n{combined_analyses}"
        )
        
        prompt_data = {
            "prompt": prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                return response["message"].strip()
            return "Could not generate a comprehensive summary."
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def research(self, query: str, system_message: str = "You are a research assistant.", 
               max_tokens: int = 150, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Conduct multi-step research on the given query.
        
        Args:
            query: The research query
            system_message: System message to set context
            max_tokens: Maximum tokens for each analysis
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the research results
        """
        try:
            # Step 1: Extract topics from the query
            topics = self.extract_topics(query, system_message, 60, temperature)
            
            # Step 2: Analyze each topic
            analyses = []
            for topic in topics:
                analysis = self.analyze_topic(topic, system_message, max_tokens, temperature)
                analyses.append(analysis)
            
            # Step 3: Aggregate the analyses into a comprehensive summary
            summary = self.aggregate_results(topics, analyses, system_message, max_tokens * 2, temperature)
            
            return {
                "status": "success",
                "topics": topics,
                "analyses": analyses,
                "summary": summary,
                "model": self.agent.model if hasattr(self.agent, 'model') else "unknown"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": "none"
            }

def register_routes(router: APIRouter):
    """
    Register routes for the ResearchAgent.
    """
    @router.post("/research", summary="Conduct multi-step research using LLM", tags=["Advanced LLM Agents"])
    async def conduct_research(request: ResearchRequest):
        """
        Conduct multi-step research on a given query using the selected LLM provider.
        
        **Input:**

        * **query (required, string):** The research query to analyze
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens for each analysis
        * **temperature (optional, float):** Sampling temperature

        **Process:** This is a multi-step agent that:
        1. Extracts key topics from the research query
        2. Generates detailed analyses for each topic
        3. Aggregates the analyses into a comprehensive summary

        **Available Providers:**
        * gemini (default)
        * openai

        **Example Input (JSON body):**

        ```json
        {
          "query": "Impact of climate change on agriculture",
          "provider": "gemini",
          "system_message": "You are a climate science expert.",
          "max_tokens": 150,
          "temperature": 0.7
        }
        ```

        **Example Output:**

        ```json
        {
          "status": "success",
          "topics": [
            "Rising temperatures",
            "Changing precipitation patterns",
            "Extreme weather events",
            "Crop yields",
            "Adaptation strategies"
          ],
          "analyses": [
            "Rising temperatures affect growing seasons and plant development...",
            "Changing precipitation patterns impact water availability for crops...",
            "Extreme weather events like floods and droughts damage crops...",
            "Crop yields are projected to decrease in many regions...",
            "Adaptation strategies include drought-resistant crops..."
          ],
          "summary": "Climate change significantly impacts agriculture through multiple pathways. Rising temperatures alter growing seasons and affect plant development cycles, potentially reducing yields in many regions. Changing precipitation patterns create water stress in some areas while causing flooding in others. Extreme weather events like droughts, floods, and storms cause direct crop damage and soil erosion. These factors collectively threaten global food security, with developing regions facing the greatest risks. However, adaptation strategies such as developing drought-resistant crops, implementing efficient irrigation systems, and diversifying agricultural practices offer potential solutions to mitigate these impacts.",
          "model": "gemini-2.0"
        }
        ```

        **Example Output (if query is empty):**

        ```json
        {
          "status": "error",
          "message": "Research query cannot be empty",
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
            agent = ResearchAgent(provider=request.provider)
            result = agent.research(
                query=request.query,
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