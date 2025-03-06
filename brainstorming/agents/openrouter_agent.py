# agents/openrouter_agent.py
import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class OpenRouterAgent:
    """
    OpenRouter Agent
    ---------------
    Purpose: Interact with OpenRouter's API to generate text completions.

    Advanced Functionality:
    - Supports multiple models
    - Handles both simple and complex prompts
    - Provides usage statistics

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import openrouter_agent
        agent = openrouter_agent.OpenRouterAgent()
        result = agent.test_connection("Hello, how are you?")
        print(result)
    """

    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
        # Get model from environment or use default
        self.default_model = os.getenv("OPENROUTER_MODEL", "openai/o3-mini-high")
        
        # List of supported models
        self.supported_models = [
            "openai/o3-mini-high",
            "openai/gpt-4",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "anthropic/claude-3-haiku",
            "google/gemini-pro"
        ]
        
        # API endpoint
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def test_connection(self, input_text: str) -> Dict[str, Any]:
        """
        Test the connection to OpenRouter API with a simple chat completion request.
        
        Args:
            input_text: The text to send to OpenRouter
            
        Returns:
            A dictionary containing the response and status
        """
        try:
            payload = {
                "model": self.default_model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": input_text}
                ],
                "max_tokens": 50
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code} - {response.text}",
                    "model": self.default_model
                }
            
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return {
                "status": "success",
                "message": content,
                "model": self.default_model
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": self.default_model
            }

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt with more options using OpenRouter's API.
        
        Args:
            prompt_data: A dictionary containing:
                - prompt: The text prompt to send to OpenRouter
                - system_message: (optional) System message to set context
                - max_tokens: (optional) Maximum tokens to generate
                - temperature: (optional) Sampling temperature
                - model: (optional) Model to use, defaults to the model in .env or openai/o3-mini-high
        
        Returns:
            A dictionary with the response data
        """
        try:
            # Extract parameters with defaults
            prompt = prompt_data.get("prompt", "")
            system_message = prompt_data.get("system_message", "You are a helpful assistant.")
            max_tokens = prompt_data.get("max_tokens", 100)
            temperature = prompt_data.get("temperature", 0.7)
            model = prompt_data.get("model", self.default_model)
            
            # Validate model - use default if invalid
            if not isinstance(model, str) or model not in self.supported_models:
                model = self.default_model

            # Prepare payload
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make API call
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code} - {response.text}",
                    "model": model
                }
            
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract usage statistics if available
            usage = data.get("usage", {})
            usage_data = {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
            
            return {
                "status": "success",
                "message": content,
                "model": model,
                "usage": usage_data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing prompt: {str(e)}",
                "model": model if 'model' in locals() else self.default_model
            }