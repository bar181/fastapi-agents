# llm/agents/question_answering_routes.py
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from .question_answering import QuestionAnsweringAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class QuestionAnsweringRequest(BaseModel):
    question: str = Field(..., description="The question to be answered")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
    max_tokens: Optional[int] = Field(150, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")

def register_routes(router: APIRouter):
    """Registers the question answering agent's route with the provided APIRouter."""
    
    @router.post("/question-answering", summary="Get an answer to a question using LLM", tags=["Advanced LLM Agents"])
    async def question_answering(request: QuestionAnsweringRequest):
        """
        Get an answer to a question using the selected LLM provider.
        Gemini is the default provider.
        
        **Input:**

        * **question (required, string):** The question to be answered
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature

        **Process:** Based on the provider parameter, either a `GeminiAgent` or `OpenAIAgent` 
        is instantiated. The agent processes the question and returns an answer.

        **Available Providers:**
        * gemini (default)
        * openai

        **Example Input (JSON body):**

        ```json
        {
          "question": "What is the capital of France?",
          "provider": "gemini",
          "system_message": "You are a geography expert.",
          "max_tokens": 100,
          "temperature": 0.5
        }
        ```

        **Example Output (Gemini):**

        ```json
        {
          "status": "success",
          "message": "The capital of France is Paris.",
          "model": "gemini-2.0",
          "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 7,
            "total_tokens": 22,
            "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
          }
        }
        ```

        **Example Output (OpenAI):**

        ```json
        {
          "status": "success",
          "message": "The capital of France is Paris.",
          "model": "gpt-4o-mini",
          "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 7,
            "total_tokens": 22
          }
        }
        ```

        **Example Output (if API key is not configured):**

        ```json
        {
          "status": "error",
          "message": "API key not configured",
          "model": "none"
        }
        ```
        """
        try:
            agent = QuestionAnsweringAgent(provider=request.provider)
            result = agent.get_answer(
                question=request.question,
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