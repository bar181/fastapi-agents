# agents/classifier.py
import re
from typing import Optional, Dict, Any
from fastapi import APIRouter, Query

class ClassifierAgent:
    """
    Classifier Agent
    ----------------
    Purpose: Classify the input text into one of several categories based on keywords and patterns.

    Advanced dspy Functionality:
    - Uses multiple rules and pattern matching to determine the text category.
    - Provides a confidence score based on rule matches.

    Usage (within FastAPI):
       The agent is designed to be used within a FastAPI application.  It expects
       the input text to be passed as a query parameter named `INPUT_TEXT`.

       Example API call:
       `/agent/classifier?INPUT_TEXT=Hello, how are you?`

    Usage (standalone - for testing):
        # In a Python shell:
        from agents import classifier
        agent = classifier.ClassifierAgent()
        result = agent.classify("Hello, how are you?")
        print(result)
        # Expected output: { "classification": "Greeting/Question", "confidence": 0.85 }  (or similar)

    """

    def __init__(self):
        """Word Boundaries:
            The use of \b ensures that only whole words are matched. For instance, r'\bhi\b' matches 'hi' 
            only if it appears as a separate word, not within this 
        """
        self.rules = {
            "Greeting": [r"\bhello\b", r"\bhi\b", "greeting"],
            "Question": [r"\?$", r"\bwhat\b", r"\bhow\b", r"\bwhy\b", r"\bwhen\b"],
            "Command": [r"\bdo\b", r"\bexecute\b", r"\brun\b"],
        }

    def classify(self, input_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Classifies the input text.

        Args:
            input_text: The text to classify.

        Returns:
            A dictionary containing the classification and confidence score.
            Returns an error message if input_text is invalid.
        """

        if not input_text or not isinstance(input_text, str):
            return {"error": "INPUT_TEXT is not provided or is not a valid string."}

        text = input_text.lower()

        # Initialize scores
        scores = {key: 0 for key in self.rules.keys()}

        # Apply rules: check for each keyword or pattern in the text
        for category, patterns in self.rules.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    scores[category] += 1

        # Determine the classification based on the highest score
        classification = "Statement"  # Default classification
        max_score = 0
        for cat, score in scores.items():
            if score > max_score:
                max_score = score
                classification = cat

        # Combine "Greeting" and "Question" if both have scores
        if scores["Greeting"] > 0 and scores["Question"] > 0:
            classification = "Greeting/Question"


        # Calculate a simple confidence score (normalized)
        confidence = min(max_score / 3.0, 1.0)  # Assume 3 matches gives full confidence

        return {
            "classification": classification,
            "confidence": round(confidence, 2)
        }



def register_routes(router: APIRouter):
    """Registers the classifier agent's routes with the provided APIRouter."""

    agent = ClassifierAgent()

    @router.get("/classifier", summary="Classifies input text", response_model=Dict[str, Any], tags=["Dspy Agents"])
    async def classifier_route(INPUT_TEXT: Optional[str] = Query(None, description="The text to be classified.  Example: Hello, how are you?")):
        """
        Classifies the input text.

        **Input:**

        *   **INPUT_TEXT (optional, string):** The text to be classified. Example Hello, how are you?

        **Process:** An instance of the `ClassifierAgent` is used. The `classify`
        method is called with the `INPUT_TEXT`.

        **Example Input (query parameter):**

        `?INPUT_TEXT=Hello, how are you?`

        **Example Output:**

        ```json
        {
          "classification": "Greeting/Question",
          "confidence": 0.67
        }
        ```
        **Example Output (if no input is provided):**

        ```json
        {
            "error": "INPUT_TEXT is not provided or is not a valid string."
        }
        ```
        """
        result = agent.classify(INPUT_TEXT)
        return result