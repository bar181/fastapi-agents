# LLM Integration Guide  **Append to Add logs - do not delete existing content on this file**

This document explains how to integrate LLM (Large Language Model) capabilities into the FastAPI Agent System. We cover two popular LLM providers—OpenAI and Gemini—with core instructions and implementation details for each.


---

## 1. Overview

Integrating LLMs allows your agents to perform complex language tasks such as text generation, summarization, translation, and more. In our system, LLM calls can be made from agent code to provide dynamic, context-aware responses.

This guide covers:
- Setup and configuration for OpenAI and Gemini
- Core implementation details and examples
- Security and error-handling considerations
- API endpoint documentation

---

## 2. Prerequisites

- **Python 3.9+**
- Install required packages:
  ```bash
  pip install openai google-generativeai requests
  ```
- Obtain API keys for:
  - **OpenAI:** [OpenAI API](https://openai.com/api/)
  - **Gemini:** [Google AI Studio](https://ai.google.dev/)

- Configure your environment (e.g., in a `.env` file):
  ```env
  OPENAI_API_KEY=your_openai_api_key
  OPENAI_MODEL=gpt-4o-mini
  GEMINI_API_KEY=your_gemini_api_key
  GEMINI_MODEL=gemini-2.0
  ```

---

## 3. OpenAI Integration

### Implementation Details

The OpenAI integration provides two endpoints:

1. **GET /openai-hello**
   - Simple test endpoint
   - Accepts a query parameter `INPUT_TEXT`
   - Returns a basic response from the OpenAI API

2. **POST /openai-prompt**
   - Advanced prompt endpoint
   - Accepts JSON input with the following fields:
     - `prompt`: The text prompt to send to OpenAI
     - `system_message`: (optional) System message to set context
     - `max_tokens`: (optional) Maximum tokens to generate
     - `temperature`: (optional) Sampling temperature
     - `model`: (optional) Model to use, defaults to the model in .env or gpt-4o-mini
   - Returns the generated response with usage statistics

### Supported Models
The following models are currently supported:
- gpt-4o-mini
- gpt-4
- gpt-3.5-turbo

### Example Usage

```python
from agents.openai_agent import OpenAIAgent

# Initialize the agent
agent = OpenAIAgent()

# Simple test connection
response = agent.test_connection("Hello, how are you?")
print(response)

# Process a complex prompt
prompt_data = {
    "prompt": "Explain quantum computing in simple terms",
    "system_message": "You are a helpful assistant.",
    "max_tokens": 150,
    "temperature": 0.7
}
response = agent.process_prompt(prompt_data)
print(response)
```

### Error Handling
The implementation includes robust error handling:
- Invalid model names fall back to the default model
- API errors return detailed error messages
- Usage statistics are safely accessed using getattr

---

## 4. Gemini Integration

### Implementation Details

The Gemini integration provides two endpoints:

1. **GET /gemini-hello**
   - Simple test endpoint
   - Accepts a query parameter `INPUT_TEXT`
   - Returns a basic response from the Gemini API

2. **POST /gemini-prompt**
   - Advanced prompt endpoint
   - Accepts JSON input with the following fields:
     - `prompt`: The text prompt to send to Gemini
     - `system_message`: (optional) System message to set context
     - `max_tokens`: (optional) Maximum tokens to generate
     - `temperature`: (optional) Sampling temperature
     - `model`: (optional) Model to use, defaults to the model in .env or gemini-2.0
   - Returns the generated response with estimated usage statistics

### Supported Models
The following models are currently supported:
- gemini-2.0
- gemini-pro
- gemini-pro-vision
- gemini-ultra

### Example Usage

```python
from agents.gemini_agent import GeminiAgent

# Initialize the agent
agent = GeminiAgent()

# Simple test connection
response = agent.test_connection("Hello, how are you?")
print(response)

# Process a complex prompt
prompt_data = {
    "prompt": "Explain quantum computing in simple terms",
    "system_message": "You are a helpful assistant.",
    "max_tokens": 150,
    "temperature": 0.7
}
response = agent.process_prompt(prompt_data)
print(response)
```

### Error Handling
The implementation includes robust error handling:
- Invalid model names fall back to the default model
- API errors return detailed error messages
- Token usage is estimated as Gemini API doesn't provide exact counts

---

## 5. Security and Error Handling Considerations

- **Authentication:**  
  Always secure your API keys. Do not hard-code them; load them from environment variables.
  
- **Error Handling:**  
  - Use try/except blocks to catch exceptions from API calls
  - Log error details and consider implementing retries or fallback mechanisms
  - Validate all input parameters

- **Rate Limiting:**  
  Ensure your integration respects the rate limits set by the LLM providers. Implement delays or retries as necessary.

---

## 6. Conclusion

This guide provides a comprehensive overview of integrating LLM capabilities into your FastAPI Agent System. Both OpenAI and Gemini implementations follow similar patterns and best practices, making it easy to switch between providers or use them together.