# llm/agents/chatbot.py
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class ChatbotRequest(BaseModel):
    message: str = Field(..., description="The initial message from the user")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
    max_tokens: Optional[int] = Field(150, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    
    @field_validator('message')
    @classmethod
    def message_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v

class MultiStepChatbotAgent:
    """
    Multi-Step Chatbot Agent
    ----------
    Purpose: Engage users in multi-turn conversations for context-aware responses.
    """

    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        if provider == "gemini":
            self.agent = GeminiAgent()
        elif provider == "openai":
            self.agent = OpenAIAgent()
        else:
            raise ValueError(f"Invalid provider: {provider}")

    def ask_clarification(self, initial_input: str, system_message: str = "You are a helpful assistant.", 
                         max_tokens: int = 50, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Ask a clarifying question based on the initial input.
        """
        prompt_data = {
            "prompt": f"Ask a clarifying question for the following input:\n{initial_input}",
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        return self.agent.process_prompt(prompt_data)

    def generate_response(self, context: str, system_message: str = "You are a helpful assistant.", 
                         max_tokens: int = 150, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate a response based on the combined context.
        """
        prompt_data = {
            "prompt": f"Using the following context, provide a helpful answer:\n{context}",
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        return self.agent.process_prompt(prompt_data)

def register_routes(router: APIRouter):
    """
    Register routes for the MultiStepChatbotAgent.
    """
    agent = MultiStepChatbotAgent()

    @router.post("/chatbot", summary="Engage in a multi-turn conversation", tags=["Advanced LLM Agents"])
    async def chatbot(request: ChatbotRequest):
        """
        Engage in a multi-turn conversation with the chatbot.
        
        **Input:**

        * **message (required, string):** The initial message from the user
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature

        **Process:**
        1. The chatbot first asks a clarifying question based on the initial input.
        2. It then uses the combined context to generate a final response.

        **Example Input (JSON body):**

        ```json
        {
          "message": "I need help with my account",
          "provider": "gemini",
          "system_message": "You are a customer service representative.",
          "max_tokens": 150,
          "temperature": 0.7
        }
        ```

        **Example Output:**

        ```json
        {
          "status": "success",
          "clarification": "Could you specify what kind of help you need with your account?",
          "final_response": "For account assistance, please visit our support page at...",
          "model": "gemini-2.0",
          "usage": {
            "clarification": {
              "prompt_tokens": 20,
              "completion_tokens": 10,
              "total_tokens": 30
            },
            "final_response": {
              "prompt_tokens": 40,
              "completion_tokens": 20,
              "total_tokens": 60
            }
          }
        }
        ```
        """
        try:
            # Step 1: Ask for clarification
            clarification_result = agent.ask_clarification(
                request.message,
                request.system_message,
                50,  # Fewer tokens for clarification
                request.temperature
            )
            
            if clarification_result["status"] != "success":
                return clarification_result
                
            # Step 2: Generate final response using combined context
            combined_context = f"{request.message}\nClarification: {clarification_result['message']}"
            response_result = agent.generate_response(
                combined_context,
                request.system_message,
                request.max_tokens,
                request.temperature
            )
            
            return {
                "status": "success",
                "clarification": clarification_result["message"],
                "final_response": response_result["message"],
                "model": response_result["model"],
                "usage": {
                    "clarification": clarification_result.get("usage", {}),
                    "final_response": response_result.get("usage", {})
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": request.provider
            }