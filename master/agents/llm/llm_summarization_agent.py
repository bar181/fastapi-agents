# llm/agents/llm_summarization_agent.py
from typing import Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class LlmSummarizationRequest(BaseModel):
    text: str = Field(..., description="The text to summarize")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a summarization expert.", description="System message to set context")
    max_tokens: Optional[int] = Field(100, description="Maximum tokens for the summary")
    temperature: Optional[float] = Field(0.5, description="Sampling temperature")
    
    @field_validator('text')
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v

class LlmSummarizationAgent:
    """
    LLM Summarization Agent
    ----------
    Purpose: Generate summaries of text using either Gemini or OpenAI.
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

    def summarize(self, text: str, system_message: str = "You are a summarization expert.", 
                 max_tokens: int = 100, temperature: float = 0.5) -> Dict[str, Any]:
        """
        Generate a summary of the given text.
        
        Args:
            text: The text to summarize
            system_message: System message to set context
            max_tokens: Maximum tokens for the summary
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the summary and metadata
        """
        if not text:
            return {
                "status": "error",
                "message": "Text cannot be empty",
                "model": "none"
            }
        
        # Create a prompt for summarization
        prompt = f"Summarize the following text in {max_tokens} tokens or less:\n\n{text}"
        
        prompt_data = {
            "prompt": prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            result = self.agent.process_prompt(prompt_data)
            
            if result["status"] == "success":
                return {
                    "status": "success",
                    "summary": result["message"].strip(),
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
    Register routes for the LlmSummarizationAgent.
    """
    @router.post("/summarize", summary="Summarize text using LLM", tags=["Advanced LLM Agents"])
    async def summarize_text(request: LlmSummarizationRequest):
        """
        Generate a summary of the given text using the selected LLM provider.
        Gemini is the default provider.
        
        **Input:**

        * **text (required, string):** The text to summarize
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens for the summary
        * **temperature (optional, float):** Sampling temperature

        **Process:** Based on the provider parameter, either a `GeminiAgent` or `OpenAIAgent` 
        is instantiated. The agent processes the text and returns a summary.

        **Available Providers:**
        * gemini (default)
        * openai

        **Example Input (JSON body):**

        ```json
        {
          "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. The term 'artificial intelligence' had previously been used to describe machines that mimic and display human cognitive skills that are associated with the human mind, such as learning and problem-solving. This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.",
          "provider": "gemini",
          "system_message": "You are a summarization expert.",
          "max_tokens": 100,
          "temperature": 0.5
        }
        ```

        **Example Output (Gemini):**

        ```json
        {
          "status": "success",
          "summary": "AI is machine intelligence distinct from human intelligence. Originally defined as machines mimicking human cognitive abilities, AI is now defined by researchers as rational systems that perceive environments and act to achieve goals. This broader definition doesn't limit how intelligence can be expressed.",
          "model": "gemini-2.0",
          "usage": {
            "prompt_tokens": 150,
            "completion_tokens": 45,
            "total_tokens": 195,
            "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
          }
        }
        ```

        **Example Output (OpenAI):**

        ```json
        {
          "status": "success",
          "summary": "AI is machine intelligence distinct from human intelligence. Originally defined as machines mimicking human cognitive abilities, AI is now defined by researchers as rational systems that perceive environments and act to achieve goals. This broader definition doesn't limit how intelligence can be expressed.",
          "model": "gpt-4o-mini",
          "usage": {
            "prompt_tokens": 150,
            "completion_tokens": 45,
            "total_tokens": 195
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
            agent = LlmSummarizationAgent(provider=request.provider)
            result = agent.summarize(
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