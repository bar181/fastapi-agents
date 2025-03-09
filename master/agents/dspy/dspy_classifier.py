# master/agents/dspy/dspy_classifier.py
import re
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

class ClassifierInput(BaseModel):
    """
    Input model for the DSPy Classifier Agent.

    Attributes:
        input_text (str): The text to be classified.  Must be a non-empty string.
    """
    input_text: str = Field(..., description="The text to be classified.  Must be a non-empty string.")


class ClassifierOutput(BaseModel):
    """
    Output model for the DSPy Classifier Agent.

    Attributes:
        classification (str): The classification of the input text (e.g., "Greeting", "Question", "Command", "Statement").
        confidence (float): The confidence score of the classification (0.0 to 1.0).
    """
    classification: str = Field(..., description="The classification of the input text.")
    confidence: float = Field(..., description="The confidence score of the classification (0.0 to 1.0).")


class ClassifierAgent:
    def __init__(self):
        self.rules = {
            "Greeting": [r"\bhello\b", r"\bhi\b", "greeting"],
            "Question": [r"\?$", r"\bwhat\b", r"\bhow\b", r"\bwhy\b", r"\bwhen\b"],
            "Command": [r"\bdo\b", r"\bexecute\b", r"\brun\b"],
        }

    def classify(self, input_text: str) -> Dict[str, Any]:
        if not input_text or not isinstance(input_text, str):
            raise HTTPException(status_code=400, detail="Input text is not provided or is not a valid string.")

        text = input_text.lower()
        scores = {key: 0 for key in self.rules.keys()}

        for category, patterns in self.rules.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    scores[category] += 1

        classification = "Statement"
        max_score = 0
        for cat, score in scores.items():
            if score > max_score:
                max_score = score
                classification = cat

        if scores["Greeting"] > 0 and scores["Question"] > 0:
            classification = "Greeting/Question"

        confidence = min(max_score / 3.0, 1.0)
        return {
            "classification": classification,
            "confidence": round(confidence, 2)
        }


def register_routes(router: APIRouter):
    """Registers the classifier agent's routes with the provided APIRouter."""
    agent = ClassifierAgent()

    @router.post("/classifier", response_model=ClassifierOutput, tags=["DSPy Agents"])
    async def classifier_route(input_data: ClassifierInput):
        """
        Classifies the input text into one of several categories.

        **Input:**

        *   **input_text (str):** The text to be classified.  Must be a non-empty string.

        **Output:**

        *   **classification (str):** The classification of the input text (e.g., "Greeting", "Question", "Command", "Statement").
        *   **confidence (float):** A confidence score (0.0 to 1.0) representing the certainty of the classification.

        **How it Works:**

        The agent uses a set of predefined rules (regular expressions) to categorize the input text.  It checks for keywords and patterns associated with Greetings, Questions, and Commands. If no specific rules match, it defaults to a "Statement" classification.  A confidence score is calculated based on the number of matching rules.

        **Example Input:**

        ```json
        {
          "input_text": "Hello, how are you?"
        }
        ```

        **Example Output:**

        ```json
        {
          "classification": "Greeting/Question",
          "confidence": 0.67
        }
        ```
        **Example Output (if input is invalid):**

        ```json
        {
            "detail": "Input text is not provided or is not a valid string."
        }
        ```
        """
        result = agent.classify(input_data.input_text)
        return ClassifierOutput(**result)