# Plan for RUV ReAct Decision Engine Agent Implementation

## Objective

- **Integrate the RUV ReAct Decision Engine agent** into the FastAPI system.
- **Showcase ReAct (Reasoning + Acting) methodology** with deductive and inductive reasoning capabilities.
- **Demonstrate domain-specific reasoning** in financial, medical, and legal contexts.
- **Enable dynamic loading** via the existing `/agent/{agent_name}` endpoint.

---

## Overview

The RUV ReAct Decision Engine agent will be developed as a module within the `agents/` folder. The agent uses the OpenRouter API to interact with LLMs and implements a ReAct (Reasoning + Acting) methodology. It incorporates both deductive and inductive reasoning capabilities for financial, medical, and legal domains, and includes a calculator tool for arithmetic operations.

---

## Implementation Guidelines

Based on our existing agent implementations, we'll follow these guidelines for the RUV ReAct Decision Engine agent:

1. **Use OpenRouter API**: The agent will use the OpenRouter API to interact with LLMs.
2. **Environment Variables**:
   - `OPENROUTER_API_KEY`: Required for API authentication.
   - `OPENROUTER_MODEL`: Optional, defaults to "openai/o3-mini-high".
3. **ReAct Methodology**: The agent will follow the ReAct (Reasoning + Acting) methodology, which combines reasoning and acting to solve tasks.
4. **Reasoning Capabilities**:
   - **Deductive Reasoning**: Apply general rules to specific cases.
   - **Inductive Reasoning**: Derive general principles from specific cases.
5. **Domain Support**:
   - Financial domain: Investment decisions based on expected returns and risk levels.
   - Medical domain: Diagnoses based on symptoms and test results.
   - Legal domain: Legal outcomes based on case types and evidence.
6. **Tool Support**: The agent will include a calculator tool for arithmetic operations.
7. **Error Handling**: Implement robust error handling for API failures and invalid inputs.
8. **Response Format**: Maintain consistent response format.
9. **Swagger Tag and Labels**: The agent should be listed in the Swagger with detailed instructions.

---

## Implementation Steps

### Step 1: Set Up the Agent Structure

- **File**: `agents/ruv_react_decision_engine.py`
- **Dependencies**:
  - FastAPI
  - Requests
  - OpenRouter API

### Step 2: Implement the Agent Class

- **Functionality**:
  - Deductive reasoning for financial, medical, and legal domains.
  - Inductive reasoning for financial, medical, and legal domains.
  - Query processing that combines deductive and inductive reasoning.

- **Implementation**:
  ```python
  class Agent:
      def apply_deductive(self, domain: str, user_input: dict):
          # Deductive reasoning logic for financial, medical, and legal domains
          if domain == "financial":
              # Financial deductive reasoning
              pass
          elif domain == "medical":
              # Medical deductive reasoning
              pass
          elif domain == "legal":
              # Legal deductive reasoning
              pass
          return None

      def apply_inductive(self, domain: str, user_input: dict):
          # Inductive reasoning logic for financial, medical, and legal domains
          if domain == "financial":
              # Financial inductive reasoning
              pass
          elif domain == "medical":
              # Medical inductive reasoning
              pass
          elif domain == "legal":
              # Legal inductive reasoning
              pass
          return None

      def process_query(self, domain: str, user_input: dict):
          # Process query using deductive and inductive reasoning
          reasoning_type = user_input.get("reasoningType", "both")
          
          if reasoning_type == "deductive":
              # Apply deductive reasoning
              pass
          elif reasoning_type == "inductive":
              # Apply inductive reasoning
              pass
          else:
              # Apply both reasoning types
              pass
  ```

### Step 3: Implement the OpenRouter API Integration

- **Functionality**:
  - Send messages to the OpenRouter API.
  - Process the API response.

- **Implementation**:
  ```python
  def call_openrouter(messages: list[ChatMessage]) -> str:
      # Set up the API request
      url = "https://openrouter.ai/api/v1/chat/completions"
      payload = {
          "model": MODEL,
          "messages": [{"role": m.role, "content": m.content} for m in messages],
          "stop": ["Observation:"],
          "temperature": 0.0,
      }
      headers = {
          "Authorization": f"Bearer {OPENROUTER_API_KEY}",
          "Content-Type": "application/json",
      }

      # Send the request and process the response
      resp = requests.post(url, json=payload, headers=headers, timeout=30)
      if resp.status_code != 200:
          raise ValueError(f"OpenRouter API error: {resp.status_code} - {resp.text}")
      
      # Extract the content from the response
      data = resp.json()
      content = data.get("choices", [{}])[0].get("message", {}).get("content")
      if not isinstance(content, str):
          raise ValueError("LLM response missing or invalid.")
      
      return content
  ```

### Step 4: Implement the ReAct Loop

- **Functionality**:
  - Run the agent with a query.
  - Process the query using the Agent class if it contains a domain key.
  - Execute the ReAct loop to generate a response.

- **Implementation**:
  ```python
  async def run_agent(query: str) -> str:
      # Initialize messages
      messages = [
          ChatMessage("system", system_prompt),
          ChatMessage("user", query),
      ]

      # Check if the query contains a domain key
      domain = None
      try:
          parsed = eval(query)  # or json.loads(query)
          if isinstance(parsed, dict) and "domain" in parsed:
              domain = parsed["domain"]
      except Exception:
          pass

      # If the query contains a domain key, process it using the Agent class
      if domain:
          parsed_input = eval(query)  # or json.loads(query)
          ag = Agent()
          preliminary = ag.process_query(domain, parsed_input)
          sys_msg = f"Preliminary agentic reasoning result: {preliminary}"
          messages.append(ChatMessage("system", sys_msg))

      # Execute the ReAct loop
      for _ in range(10):
          # Get the assistant's reply
          assistant_reply = call_openrouter(messages)
          reply = assistant_reply if isinstance(assistant_reply, str) else ""
          messages.append(ChatMessage("assistant", reply))

          # Check if the final answer is found
          answer_match = None
          import re
          match = re.search(r"Answer:\s*(.*)$", reply)
          if match:
              answer_match = match.group(1).strip()

          if answer_match:
              return answer_match

          # Check for action
          action_match = re.search(r"Action:\s*([^\[]+)\[([^\]]+)\]", reply)
          if action_match:
              tool_name = action_match.group(1).strip()
              tool_input = action_match.group(2).strip()

              # Find the tool
              found_tool = None
              for t in tools:
                  if t.name.lower() == tool_name.lower():
                      found_tool = t
                      break

              # Execute the tool
              if not found_tool:
                  obs = f'Tool "{tool_name}" not found'
              else:
                  try:
                      obs = found_tool.run(tool_input)
                  except Exception as exc:
                      obs = f"Error: {exc}"

              # Add the observation to the messages
              messages.append(ChatMessage("system", f"Observation: {obs}"))
              continue

          return reply.strip()

      raise ValueError("No final answer produced within step limit.")
  ```

### Step 5: Implement the FastAPI Endpoints

- **Functionality**:
  - Root endpoint to provide information about the agent.
  - POST endpoint to handle queries.

- **Implementation**:
  ```python
  @app.get("/")
  def read_root():
      return {
          "message": "Agentic ReAct Agent in FastAPI!",
          "usage": "POST JSON to '/' with { 'query': 'your question' }",
      }

  @app.post("/")
  async def handle_query(request: Request):
      try:
          body = await request.json()
      except:
          return Response("Invalid JSON body", status_code=400)

      query = body.get("query") or body.get("question")
      if not query or not isinstance(query, str):
          return Response('Missing "query" string in request body.', status_code=400)

      try:
          answer = await run_agent(query)
          return {"answer": answer}
      except Exception as exc:
          return Response(f'Error: {str(exc)}', status_code=500)
  ```

---

## Integration with FastAPI and Testing

- **Dynamic Endpoint**:
  The agent module will be loaded via the existing dynamic endpoint `/agent/{agent_name}`.

- **Testing**:
  - Create automated tests under the `/tests` folder verifying:
    - Correct functionality of the agent.
    - Deductive and inductive reasoning capabilities.
    - Domain-specific reasoning in financial, medical, and legal contexts.
    - ReAct methodology implementation.
    - Tool usage (calculator).
    - OpenRouter API integration.
    - Error handling.

- **Test Cases**:
  1. **Financial Domain**:
     - Test deductive reasoning with expected returns and risk levels.
     - Test inductive reasoning with past returns.
  2. **Medical Domain**:
     - Test deductive reasoning with symptoms and test results.
     - Test inductive reasoning with symptoms.
  3. **Legal Domain**:
     - Test deductive reasoning with case types and evidence.
     - Test inductive reasoning with case types.
  4. **Calculator Tool**:
     - Test arithmetic operations.
     - Test error handling for invalid expressions.
  5. **API Integration**:
     - Test successful API calls.
     - Test error handling for API failures.

- **Logging**:
  Document progress, test results, and any issues in **/logs/5-react-agent-logs.md**.

---

## Summary

This plan outlines the implementation of the RUV ReAct Decision Engine agent, which uses the OpenRouter API to interact with LLMs and implements a ReAct methodology. The agent incorporates both deductive and inductive reasoning capabilities for financial, medical, and legal domains, and includes a calculator tool for arithmetic operations.

The implementation follows a structured approach, with clear steps for setting up the agent, implementing the reasoning capabilities, integrating with the OpenRouter API, and implementing the ReAct loop. The plan also includes guidelines for testing the agent's functionality, reasoning capabilities, and API integration.

The RUV ReAct Decision Engine agent showcases advanced reasoning capabilities and demonstrates how to integrate external APIs into the FastAPI system. It provides a foundation for developing more sophisticated agents that can reason about complex domains and interact with external tools and APIs.