# LLM Agents

This module integrates Large Language Model (LLM) capabilities into the FastAPI Agent System. It supports multiple LLM providers, including OpenAI and Gemini, allowing for dynamic text generation, summarization, and other language tasks.

1. **LLM Agents**: Advanced language processing agents leveraging OpenAI and Gemini
2. **Simple Agents**: Basic agents that return simple responses without validation
3. **Agents with Validation**: Agents that require validation (like token verification)
4. **Dynamic Agents**: Agents that are loaded dynamically at runtime

---

## Features

✅ **Advanced Language Processing with LLMs**
   - **OpenAI Integration:** Connect to OpenAI's powerful language models for text generation, summarization, and more.
   - **Gemini Integration:** Leverage Gemini's language capabilities for various NLP tasks.
   - **Dynamic Provider Selection:** Choose between OpenAI and Gemini at runtime for each request.

✅ **Simple Utility Agents**
   - **Hello World**: Returns a simple greeting.
   - **Time**: Returns the current time in ISO 8601 format.
   - **Quote**: Returns an inspirational quote.

✅ **Organized Swagger UI**
   - Agents are organized into logical categories in the Swagger UI.
   - All agents can be viewed at once via the `/agents` endpoint.

✅ **API Integration**
   - Each agent is accessible via a dedicated API endpoint.
   - LLM-specific endpoints are available under the `/llm` prefix.

---

## LLM Agent Details

- **OpenAI Agent**: This agent connects to OpenAI's API to process text inputs and generate responses. It supports various models and can be configured for different tasks.
- **Gemini Agent**: This agent integrates with Gemini's API for language processing tasks. It provides similar capabilities to the OpenAI agent but uses Gemini's models.
- **Dynamic Provider Selection**: This feature allows you to choose between OpenAI and Gemini at runtime, defaulting to Gemini if no provider is specified.

### Available LLM Agents

1. **OpenAI Hello Agent** (`openai_hello.py`): Simple test endpoint for OpenAI integration
2. **OpenAI Prompt Agent** (`openai_prompt.py`): Advanced prompt endpoint for OpenAI with parameter customization
3. **Gemini Hello Agent** (`gemini_hello.py`): Simple test endpoint for Gemini integration
4. **Gemini Prompt Agent** (`gemini_prompt.py`): Advanced prompt endpoint for Gemini with parameter customization
5. **Provider Hello Agent** (`provider_hello.py`): Dynamic provider selection endpoint for simple testing
6. **Provider Prompt Agent** (`provider_prompt.py`): Dynamic provider selection endpoint with advanced parameter customization

---

## Project Structure

```
llm/
├─ app/
│   ├─ main.py          # FastAPI application entrypoint
│   ├─ routes_llm.py    # LLM-specific routes
│   └─ models.py        # (For future use: data models)
├─ agents/
│   ├─ __init__.py      # Package initializer
│   ├─ hello_world.py   # Hello World agent
│   ├─ time.py          # Time agent
│   ├─ quote.py         # Quote agent
│   ├─ classifier.py    # Text classification agent
│   ├─ openai_agent.py  # OpenAI core implementation
│   ├─ openai_hello.py  # OpenAI hello endpoint
│   ├─ openai_prompt.py # OpenAI prompt endpoint
│   ├─ gemini_agent.py  # Gemini core implementation
│   ├─ gemini_hello.py  # Gemini hello endpoint
│   ├─ gemini_prompt.py # Gemini prompt endpoint
│   ├─ provider_hello.py # Provider selection hello endpoint
│   ├─ provider_prompt.py # Provider selection prompt endpoint
│   ├─ dspy_integration.py # DSPy integration utilities
├─ docs/                # Documentation for this module
├─ plans/               # Step by step instructions for AI code writing
├─ logs/                # Logging steps
├─ tests/               # Test suite
├─ requirements.txt     # Dependencies
└─ LICENSE             # MIT License
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file based on the `.env.sample` template and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=your_model_here_or_gpt-4o-mini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_ENDPOINT=https://api.gemini.example.com/v1/chat/completions
GEMINI_MODEL=your_model_here_or_gemini-2.0
```

3. Run the server:

For standalone modules:
```bash
uvicorn app.main:app --reload
```

For running within the mono repo:
```bash
# First, navigate to the specific module directory
cd llm

# Then run the server using the Python -m flag
python -m uvicorn app.main:app --reload
```

4. Test the endpoints:

Core Endpoints:
- Welcome message: GET /
- Health check: GET /health
- List all agents: GET /agents

LLM Agent Endpoints:
- OpenAI Hello World: GET /llm/openai-hello?INPUT_TEXT=Hello%20World
- OpenAI Prompt: POST /llm/openai-prompt
- Gemini Hello World: GET /llm/gemini-hello?INPUT_TEXT=Hello%20World
- Gemini Prompt: POST /llm/gemini-prompt
- Provider Hello: GET /llm/provider-hello?INPUT_TEXT=Hello%20World&provider=openai
- Provider Prompt: POST /llm/provider-prompt

Agent Categories in Swagger UI:
- **LLM Agents**: Advanced language processing agents
  - OpenAI Hello: GET /llm/openai-hello?INPUT_TEXT=Hello%20World
  - OpenAI Prompt: POST /llm/openai-prompt
  - Gemini Hello: GET /llm/gemini-hello?INPUT_TEXT=Hello%20World
  - Gemini Prompt: POST /llm/gemini-prompt
  - Provider Hello: GET /llm/provider-hello?INPUT_TEXT=Hello%20World&provider=openai
  - Provider Prompt: POST /llm/provider-prompt

- **Simple Agents**: Basic agents without validation
  - Hello World: GET /agent/hello_world
  - Time: GET /agent/time
  - Quote: GET /agent/quote

- **Dynamic Agents**: Dynamically loaded agents
  - Generic Agent: GET /agent/{agent_name}

- **All Agents**: List all available agents
  - List Agents: GET /agents

Example Usage:
```bash
# Test an endpoint (replace SERVER_URL with your server address)
curl SERVER_URL/llm/openai-hello?INPUT_TEXT=Hello%20World

# Test with provider selection
curl "SERVER_URL/llm/provider-hello?INPUT_TEXT=Tell%20me%20a%20joke&provider=openai"

# Test POST endpoint with JSON body
curl -X POST "SERVER_URL/llm/provider-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Tell me a dad joke",
    "provider": "gemini",
    "system_message": "You are a comedian who specializes in dad jokes.",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

## Running Tests

For standalone modules:
```bash
pytest tests/
```

For running within the mono repo:
```bash
# First, navigate to the specific module directory
cd llm

# Then run the tests using the Python -m flag
python -m pytest tests
```

The test suite includes tests to ensure the LLM agents are functioning correctly.

## Documentation
- /docs main documentation for this module
- /plans step by step instructions
- /logs updates

## This repository was created using Documentation First Coding Methodologies

Our development process followed a rigorous Documentation First approach:

1. **Brainstorm and Design:**
   Initial ideas and designs were discussed and documented to establish project goals.

2. **Required Documentation:**
   All technical and implementation documents were created and saved in the `/docs` directory.

3. **Phase Plans:**
   Detailed plans for each development phase were created and are available in the `/plans` folder.

4. **Step-by-Step Execution:**
   Development followed the step-by-step outlines provided in each phase, including comprehensive tests.

5. **Tracking and Logging:**
   Every step of the process was tracked and logged in the `/logs` directory for transparency.

6. **Testing and Updates:**
   Appropriate tests were implemented and documentation was continuously updated to reflect the current state of the project.

## Original Gist
https://gist.github.com/bar181/7fc0286841a38c72848ed037d0e561fd
### Author: Bradley Ross (bar181 on gists and github)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
