# llm/agents/question_answering.py
from typing import Dict, Any
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent

class QuestionAnsweringAgent:
    """
    Question Answering Agent
    ----------
    Purpose: Answer questions using either Gemini or OpenAI.
    """

    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        if provider == "gemini":
            self.agent = GeminiAgent()
        elif provider == "openai":
            self.agent = OpenAIAgent()
        else:
            raise ValueError(f"Invalid provider: {provider}")

    def get_answer(self, question: str, system_message: str = "You are a helpful assistant.", 
                  max_tokens: int = 150, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Get an answer to a question using the selected provider.
        
        Args:
            question: The question to answer
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the answer and metadata
        """
        prompt_data = {
            "prompt": question,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        return self.agent.process_prompt(prompt_data)