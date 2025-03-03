# llm/agents/llm_classifier.py
import re
from typing import Dict, Any, Optional, List
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class ClassifierRequest(BaseModel):
    text: str = Field(..., description="The text to classify")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a text classification expert.", description="System message to set context")
    max_tokens: Optional[int] = Field(100, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    
    @field_validator('text')
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v

class LLMClassifierAgent:
    """
    LLM-Enhanced Classifier Agent
    ----------
    Purpose: Combine rule-based classification with LLM refinement to provide
    enhanced text classification with reasoning.
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
            
        # Define rule-based classification patterns
        self.rules = {
            "Greeting": [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgreetings\b"],
            "Question": [r"\?$", r"\bwhat\b", r"\bhow\b", r"\bwhy\b", r"\bwhen\b", r"\bwhere\b"],
            "Command": [r"\bdo\b", r"\bexecute\b", r"\brun\b", r"\bperform\b", r"\bcreate\b"],
            "Statement": [r"\bis\b", r"\bare\b", r"\bwas\b", r"\bwere\b"],
            "Request": [r"\bplease\b", r"\bcould you\b", r"\bwould you\b", r"\bcan you\b"]
        }

    def rule_based_classify(self, text: str) -> Dict[str, Any]:
        """
        Perform rule-based classification using regex patterns.
        
        Args:
            text: The text to classify
            
        Returns:
            A dictionary with the classification results
        """
        scores = {category: 0 for category in self.rules}
        matches = {category: [] for category in self.rules}
        
        for category, patterns in self.rules.items():
            for pattern in patterns:
                if re.search(pattern, text.lower()):
                    scores[category] += 1
                    matches[category].append(pattern)
        
        # Get the category with the highest score
        if sum(scores.values()) > 0:
            top_category = max(scores, key=scores.get)
            confidence = scores[top_category] / sum(1 for s in scores.values() if s > 0)
        else:
            top_category = "Unknown"
            confidence = 0.0
            
        return {
            "category": top_category,
            "confidence": confidence,
            "scores": scores,
            "matches": matches
        }

    def refine_classification(self, text: str, initial_classification: Dict[str, Any], 
                            system_message: str = "You are a text classification expert.", 
                            max_tokens: int = 100, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Refine the rule-based classification using LLM.
        
        Args:
            text: The text to classify
            initial_classification: The initial rule-based classification
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the refined classification
        """
        # Create a prompt for LLM refinement
        prompt = (
            f"Given the input text: '{text}' and an initial rule-based classification of "
            f"'{initial_classification['category']}' (confidence: {initial_classification['confidence']:.2f}), "
            f"provide a refined classification with reasoning.\n\n"
            f"Initial pattern matches: {initial_classification['matches']}\n\n"
            f"Your task:\n"
            f"1. Determine if the initial classification is correct\n"
            f"2. If not, provide a better classification\n"
            f"3. Explain your reasoning\n\n"
            f"Format your response as:\nCLASSIFICATION: [category]\nREASONING: [your explanation]"
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
                message = response["message"].strip()
                
                # Extract classification and reasoning
                classification_match = re.search(r"CLASSIFICATION:\s*(.+?)(?:\n|$)", message)
                reasoning_match = re.search(r"REASONING:\s*(.+)", message, re.DOTALL)
                
                refined_category = classification_match.group(1).strip() if classification_match else "Unknown"
                reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"
                
                return {
                    "category": refined_category,
                    "reasoning": reasoning,
                    "model": response.get("model", "unknown"),
                    "usage": response.get("usage", {})
                }
            else:
                return {
                    "category": initial_classification["category"],
                    "reasoning": "LLM refinement failed, using rule-based classification",
                    "model": "none",
                    "error": response.get("message", "Unknown error")
                }
        except Exception as e:
            return {
                "category": initial_classification["category"],
                "reasoning": f"Error during LLM refinement: {str(e)}",
                "model": "none"
            }

    def classify(self, text: str, system_message: str = "You are a text classification expert.", 
               max_tokens: int = 100, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Classify text using a combination of rule-based and LLM approaches.
        
        Args:
            text: The text to classify
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the classification results
        """
        try:
            # Step 1: Perform rule-based classification
            initial_classification = self.rule_based_classify(text)
            
            # Step 2: Refine the classification using LLM
            refined_classification = self.refine_classification(
                text, 
                initial_classification, 
                system_message, 
                max_tokens, 
                temperature
            )
            
            # Step 3: Combine the results
            return {
                "status": "success",
                "initial_classification": {
                    "category": initial_classification["category"],
                    "confidence": initial_classification["confidence"],
                    "pattern_matches": initial_classification["matches"][initial_classification["category"]]
                },
                "refined_classification": {
                    "category": refined_classification["category"],
                    "reasoning": refined_classification["reasoning"]
                },
                "model": refined_classification.get("model", "unknown"),
                "usage": refined_classification.get("usage", {})
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": "none"
            }

def register_routes(router: APIRouter):
    """
    Register routes for the LLMClassifierAgent.
    """
    @router.post("/classify", summary="Classify text using rule-based and LLM approaches", tags=["Advanced LLM Agents"])
    async def classify_text(request: ClassifierRequest):
        """
        Classify text using a combination of rule-based patterns and LLM refinement.
        
        **Input:**

        * **text (required, string):** The text to classify
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature

        **Process:** This agent demonstrates dspy-inspired functionality by:
        1. Performing rule-based classification using regex patterns
        2. Refining the classification using LLM to provide better categorization and reasoning

        **Available Providers:**
        * gemini (default)
        * openai

        **Example Input (JSON body):**

        ```json
        {
          "text": "Hi, can you help me find information about climate change?",
          "provider": "gemini",
          "system_message": "You are a text classification expert.",
          "max_tokens": 100,
          "temperature": 0.7
        }
        ```

        **Example Output:**

        ```json
        {
          "status": "success",
          "initial_classification": {
            "category": "Greeting",
            "confidence": 0.5,
            "pattern_matches": ["\\bhi\\b"]
          },
          "refined_classification": {
            "category": "Information Request",
            "reasoning": "While the text does start with a greeting ('Hi'), the primary intent is to request information about climate change. The presence of 'can you help me find information' clearly indicates this is an information-seeking request rather than just a greeting."
          },
          "model": "gemini-2.0",
          "usage": {
            "prompt_tokens": 120,
            "completion_tokens": 65,
            "total_tokens": 185,
            "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
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
            agent = LLMClassifierAgent(provider=request.provider)
            result = agent.classify(
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