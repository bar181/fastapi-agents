```markdown
# LLM Integration Guide

This document explains how to integrate LLM (Large Language Model) capabilities into the FastAPI Agent System. We cover two popular LLM providers—OpenAI and Gemini—with core instructions and pseudocode examples for each.

---

## 1. Overview

Integrating LLMs allows your agents to perform complex language tasks such as text generation, summarization, translation, and more. In our system, LLM calls can be made from agent code to provide dynamic, context-aware responses.

This guide covers:
- Setup and configuration for OpenAI and Gemini.
- Core instructions and pseudocode examples.
- Security and error-handling considerations.

---

## 2. Prerequisites

- **Python 3.9+**
- Install required packages:
  ```bash
  pip install openai requests
  ```
- Obtain API keys for:
  - **OpenAI:** [OpenAI API](https://openai.com/api/)
  - **Gemini:** (Refer to your provider’s documentation; this example assumes a RESTful endpoint)

- Configure your environment (e.g., in a `.env` file):
  ```env
  OPENAI_API_KEY=your_openai_api_key
  GEMINI_API_KEY=your_gemini_api_key
  GEMINI_API_URL=https://api.gemini.example.com/v1/chat/completions
  ```

---

## 3. OpenAI Integration

### Setup

- Install the OpenAI Python library.
- Set your API key using `openai.api_key` (or load it from environment variables).

### Pseudocode Example

```python
import openai
import os

# Load the OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_openai(prompt: str) -> str:
    """
    Calls the OpenAI API with the given prompt and returns the generated response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or another model like "gpt-4"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        # Handle errors appropriately (e.g., logging, retries)
        raise Exception(f"OpenAI API error: {str(e)}")

# Example usage:
# result = call_openai("Summarize the following text: ...")
# print(result)
```

---

## 4. Gemini Integration

### Setup

- Use the `requests` library to interact with the Gemini API.
- Configure your API key and endpoint URL from your environment.

### Pseudocode Example

```python
import requests
import os

# Load Gemini configuration from environment variables
GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the generated response.
    """
    url = GEMINI_API_URL  # e.g., "https://api.gemini.example.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gemini-model",  # Replace with the actual model name if different
        "prompt": prompt,
        "temperature": 0.7,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Assuming the API returns a structure similar to OpenAI's
        return data["choices"][0]["text"]
    except Exception as e:
        # Handle errors (logging, retries, etc.)
        raise Exception(f"Gemini API error: {str(e)}")

# Example usage:
# result = call_gemini("Translate 'Hello, world' to Spanish.")
# print(result)
```

---

## 5. Security and Error Handling Considerations

- **Authentication:**  
  Always secure your API keys. Do not hard-code them; load them from environment variables.
  
- **Error Handling:**  
  - Use try/except blocks to catch exceptions from API calls.
  - Log error details and consider implementing retries or fallback mechanisms.

- **Rate Limiting:**  
  Ensure your integration respects the rate limits set by the LLM providers. Implement delays or retries as necessary.

---

## 6. Conclusion

This guide provides a starting point for integrating LLM capabilities into your FastAPI Agent System using OpenAI and Gemini. Adapt the pseudocode to your specific requirements and API documentation, and ensure robust security and error handling for production use.

---
```