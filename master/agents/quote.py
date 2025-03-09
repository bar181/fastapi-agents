# agents/quote.py
import random

# Collection of inspirational quotes
QUOTES = [
    "Believe in yourself and all that you are.",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Success is not final, failure is not fatal. - Winston Churchill",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    "What you do today can improve all your tomorrows. - Ralph Marston",
    "The way to get started is to quit talking and begin doing. - Walt Disney"
]

from typing import Dict, Any
from fastapi import APIRouter
import random

# Collection of inspirational quotes
QUOTES = [
    "Believe in yourself and all that you are.",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Success is not final, failure is not fatal. - Winston Churchill",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    "What you do today can improve all your tomorrows. - Ralph Marston",
    "The way to get started is to quit talking and begin doing. - Walt Disney"
]

class QuoteAgent:
    """
    Quote Agent
    -----------
    Purpose: Returns a random inspirational quote from a collection.
    """
    
    def get_quote(self) -> Dict[str, str]:
        """Returns a random inspirational quote."""
        return {"quote": random.choice(QUOTES)}
    
# Keep the original function for backward compatibility
def agent_main():
    """
    Original agent_main function for backward compatibility.
    """
    agent = QuoteAgent()
    return agent.get_quote()

def register_routes(router: APIRouter):
    """Registers the quote agent's routes with the provided APIRouter."""
    
    agent = QuoteAgent()
    
    @router.get("/quote", summary="Returns an inspirational quote.", tags=["Simple Agents"])
    async def quote_route():
        """
        Returns a hard-coded inspirational quote.
        
        **Process:** An instance of the `QuoteAgent` is used to generate the response.
        
        **Example Output:**
        
        ```json
        {
          "agent": "quote",
          "result": {
            "quote": "Believe in yourself and all that you are."
          }
        }
        ```
        """
        return {"agent": "quote", "result": agent.get_quote()}