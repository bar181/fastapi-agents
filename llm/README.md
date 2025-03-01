# DSPy Agents

This module contains a variety of agents organized into different categories:

1. **DSPy Agents**: Advanced text processing agents leveraging DSPy
2. **Simple Agents**: Basic agents that return simple responses without validation
3. **Agents with Validation**: Agents that require validation (like token verification)
4. **Dynamic Agents**: Agents that are loaded dynamically at runtime

---

## Features

✅ **Advanced Text Processing with DSPy**
   - **DSPy Overview:** DSPy is a framework for building complex AI systems using declarative programming. It allows you to define the desired behavior of your system and automatically optimizes the underlying prompts and models to achieve the best performance. DSPy excels in tasks requiring reasoning, multi-hop information retrieval, and complex decision-making. It works by composing smaller modules (like prompting, filtering, or re-ranking) into larger programs, and then automatically tuning these programs to maximize their effectiveness.
   - **DSPy Use Cases:** DSPy is particularly well-suited for building question answering systems, chatbots, and other applications that require sophisticated natural language understanding and generation. It is designed to be adaptable to different models and data sources, making it a versatile tool for a wide range of AI tasks.
   - **Classifier Agent**: Uses advanced rule-based logic for text classification.
   - **Summarizer Agent**: Processes and summarizes long-form text.
   - **TextRank Summarizer**: Summarizes text using the TextRank algorithm.

✅ **Simple Utility Agents**
   - **Hello World**: Returns a simple greeting.
   - **Goodbye**: Returns a farewell message.
   - **Echo**: Returns an echo message.
   - **Time**: Returns the current time in ISO 8601 format.
   - **Joke**: Returns a random programming joke.
   - **Quote**: Returns an inspirational quote.

✅ **Agents with Validation**
   - **Math**: Evaluates mathematical expressions after token verification.

✅ **Dynamic Agent Execution**
   - **Agents are loaded dynamically** via FastAPI and executed on demand.

✅ **Organized Swagger UI**
   - Agents are organized into logical categories in the Swagger UI.
   - All agents can be viewed at once via the `/agents` endpoint.

✅ **API Integration**
   - Each agent is accessible via a dedicated API endpoint.

---

## Agent Details

- **Classifier Agent**: This agent uses DSPy to classify text based on predefined categories. It takes an input text and returns the predicted category. DSPy optimizes the prompts used for classification to achieve high accuracy.
- **Summarizer Agent**: This agent leverages DSPy to summarize long-form text. It takes an input text and returns a concise summary. DSPy automatically tunes the summarization prompts to generate summaries that are both informative and coherent.
- **TextRank Summarizer**: This agent uses the TextRank algorithm to summarize text. It identifies the most important sentences in the text and combines them to create a summary.

---

## Project Structure

```
fastapi-agent-system/
├─ app/
│   ├─ main.py          # FastAPI application entrypoint
│   └─ models.py        # (For future use: data models)
├─ agents/
│   ├─ __init__.py              # Package initializer
│   ├─ hello_world.py           # Hello World agent
│   ├─ goodbye.py               # Goodbye agent
│   ├─ echo.py                  # Echo agent
│   ├─ time.py                  # Time agent
│   ├─ joke.py                  # Joke agent
│   ├─ quote.py                 # Quote agent
│   ├─ math.py                  # Math agent with validation
│   ├─ classifier.py            # Text classification agent
│   ├─ summarizer.py            # Text summarization agent
│   ├─ textrank_summarizer.py   # TextRank summarization agent
│   ├─ dspy_integration.py      # DSPy integration utilities
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

2. Run the server:

For standalone modules:
```bash
uvicorn app.main:app --reload
```

For running within the mono repo:
```bash
# First, navigate to the specific module directory
cd dspy

# Then run the server using the Python -m flag
python -m uvicorn app.main:app --reload
```

3. Test the endpoints:

Core Endpoints:
- Welcome message: GET /
- Health check: GET /health
- List all agents: GET /agents

Agent Categories in Swagger UI:
- **Dspy Agents**: Advanced text processing agents
  - Classifier: GET /agent/classifier?INPUT_TEXT=Hello,%20how%20are%20you?
  - Summarizer: GET /agent/summarizer?TEXT_TO_SUMMARIZE=FastAPI%20is%20efficient&max_length=10
  - TextRank Summarizer: GET /agent/textrank_summarizer?TEXT_TO_SUMMARIZE=FastAPI%20is%20efficient&num_sentences=2

- **Simple Agents**: Basic agents without validation
  - Hello World: GET /agent/hello_world
  - Goodbye: GET /agent/goodbye
  - Echo: GET /agent/echo
  - Time: GET /agent/time
  - Joke: GET /agent/joke
  - Quote: GET /agent/quote

- **Agents with Validation**: Agents requiring validation
  - Math: GET /agent/math?token=MATH_SECRET&expression=3*(4+2)

- **Dynamic Agents**: Dynamically loaded agents
  - Generic Agent: GET /agent/{agent_name}

- **All Agents**: List all available agents
  - List Agents: GET /agents

Example Usage:
```bash
# Test an endpoint (replace SERVER_URL with your server address)
curl SERVER_URL/agent/hello_world

# Test with parameters
curl "SERVER_URL/agent/summarizer?TEXT_TO_SUMMARIZE=FastAPI%20is%20efficient&max_length=10"
curl "SERVER_URL/agent/textrank_summarizer?TEXT_TO_SUMMARIZE=FastAPI%20is%20efficient&num_sentences=2"
```
```

## Running Tests

For standalone modules:
```bash
pytest tests/
```

For running within the mono repo:
```bash
# First, navigate to the specific module directory
cd base-framework

# Then run the tests using the Python -m flag
python -m pytest tests
```

The test suite includes 30 tests to ensure the agents are functioning correctly.

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
