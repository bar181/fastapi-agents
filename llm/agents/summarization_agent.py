# llm/agents/summarization_agent.py
from typing import Dict, Any
from fastapi import APIRouter
from .openai_agent import OpenAIAgent

class SummarizationAgent:
    """
    Summarization Agent
    ----------
    Purpose: Generate summaries of text using OpenAI.
    """

    def __init__(self):
        self.openai_agent = OpenAIAgent()
        self.supported_models = ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"]

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt to generate a summary of the given text.
        
        Args:
            prompt_data: A dictionary containing:
                - text: The text to summarize
                - model: (optional) Model to use, defaults to the model in .env or gpt-4o-mini
                - max_tokens: (optional) Maximum tokens for the summary
        
        Returns:
            A dictionary with the summary and metadata
        """
        try:
            text = prompt_data.get("text", "")
            model = prompt_data.get("model", self.openai_agent.default_model)
            max_tokens = prompt_data.get("max_tokens", 100)
            
            # Validate input
            if not text:
                return {
                    "status": "error",
                    "message": "Text cannot be empty",
                    "model": model
                }
            
            # Validate model
            if model not in self.supported_models:
                return {
                    "status": "error",
                    "message": f"Unsupported model: {model}",
                    "model": model
                }
            
            # Create a prompt for summarization
            prompt = f"Summarize the following text in {max_tokens} tokens or less:\n\n{text}"
            
            # Use OpenAI agent to process the prompt
            result = self.openai_agent.process_prompt({
                "prompt": prompt,
                "model": model,
                "max_tokens": max_tokens
            })
            
            return {
                "status": "success",
                "summary": result["message"].strip(),
                "model": model,
                "usage": result.get("usage", {})
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": model if 'model' in locals() else self.openai_agent.default_model
            }

def register_routes(router: APIRouter):
    """
    Register routes for the SummarizationAgent.
    """
    agent = SummarizationAgent()

    @router.post("/summarize", tags=["Summarization"])
    async def summarize_text(prompt_data: Dict[str, Any]):
        """
        Generate a summary of the given text.
        """
        return agent.process_prompt(prompt_data)