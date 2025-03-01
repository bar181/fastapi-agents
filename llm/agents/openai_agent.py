# agents/openai_agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIAgent:
    """
    Agent for interacting with OpenAI's API using the latest client.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Get model from environment or use default
        self.default_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
    
    def test_connection(self, input_text: str):
        """
        Test the connection to OpenAI API with a simple chat completion request.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": input_text}
                ],
                max_tokens=50
            )
            
            return {
                "status": "success",
                "message": completion.choices[0].message.content,
                "model": self.default_model
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": self.default_model
            }
    
    def process_prompt(self, prompt_data):
        """
        Process a prompt with more options using OpenAI's API.
        
        Args:
            prompt_data: A dictionary containing:
                - prompt: The text prompt to send to OpenAI
                - system_message: (optional) System message to set context
                - max_tokens: (optional) Maximum tokens to generate
                - temperature: (optional) Sampling temperature
                - model: (optional) Model to use, defaults to the model in .env or gpt-4o-mini
        
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
            
            # Make API call
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "status": "success",
                "message": completion.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": completion.usage.prompt_tokens,
                    "completion_tokens": completion.usage.completion_tokens,
                    "total_tokens": completion.usage.total_tokens
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": model if 'model' in locals() else self.default_model
            }