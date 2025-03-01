# Plan for LLM Agents Implementation

## Objective

- **Integrate five LLM-based agents** into the FastAPI system.
- **Showcase both straightforward and multi-step workflows.**
- **Demonstrate dspy functionality** in two agents.
- **Enable dynamic loading** via the existing `/agent/{agent_name}` endpoint.

The five agents to be implemented are:

1. **Question Answering Agent (Straightforward)**
2. **Multi-Step Chatbot Agent (Multi-Step)**
3. **Multi-Step Research Agent (Multi-Step)**
4. **LLM-Enhanced Classifier Agent (Straightforward with dspy)**
5. **Multi-Step Research Analyzer Agent (Multi-Step with dspy)**

---

## Overview

Each agent will be developed as a separate module within the `agents/` folder. The agents will use the Gemini LLM by default, with the option to switch to OpenAI. For the dspy-enabled ones, they will combine rule-based processing with LLM refinement. Detailed pseudocode is provided to illustrate the intended functionality.

---

## Implementation Guidelines from Gemini Integration

Based on our successful Gemini integration and provider-based endpoints, we'll follow these guidelines for all LLM agents:

1. **Default to Gemini**: Use Gemini as the default LLM provider, with OpenAI as an alternative option.
2. **Common Parameters**: All agents should support these parameters:
   - `system_message`: (optional) System message to set context
   - `max_tokens`: (optional) Maximum tokens to generate
   - `temperature`: (optional) Sampling temperature
3. **Provider Selection**: Include a `provider` parameter to switch between "gemini" and "openai"
4. **Error Handling**: Implement robust error handling for API failures
5. **Response Format**: Maintain consistent response format across all agents
6. **Token Usage**: Include token usage statistics in responses (estimated for Gemini)
7. **Provider Validation**: Validate provider against a list of available providers

---

## Implementation Steps

### Step 1: Develop the Question Answering Agent

- **Functionality:**
  - Receives a question as input.
  - Sends the question to the selected LLM provider.
  - Returns the generated answer.

- **Pseudocode:**
  ```python
  # agents/question_answering.py
  from agents.gemini_agent import GeminiAgent
  from agents.openai_agent import OpenAIAgent

  class QuestionAnsweringAgent:
      AVAILABLE_PROVIDERS = ["gemini", "openai"]
      
      def __init__(self, provider="gemini"):
          self.provider = provider.lower()
          if self.provider not in self.AVAILABLE_PROVIDERS:
              raise ValueError(f"Invalid provider: {provider}. Available providers: {', '.join(self.AVAILABLE_PROVIDERS)}")
              
          if self.provider == "openai":
              self.agent = OpenAIAgent()
          else:
              self.agent = GeminiAgent()

      def get_answer(self, question: str, system_message: str = "You are a helpful assistant.", 
                    max_tokens: int = 150, temperature: float = 0.7) -> dict:
          prompt_data = {
              "prompt": question,
              "system_message": system_message,
              "max_tokens": max_tokens,
              "temperature": temperature
          }
          return self.agent.process_prompt(prompt_data)

  def agent_main(question: str, provider: str = "gemini", system_message: str = "You are a helpful assistant.", 
                max_tokens: int = 150, temperature: float = 0.7):
      """
      Direct call instructions:
      1. Import the agent and set your question.
      2. Call agent_main() with the question string and optional parameters.
      
      Example:
          >>> from agents import question_answering
          >>> result = question_answering.agent_main(
          ...     "What is the capital of France?",
          ...     provider="gemini",  # or "openai"
          ...     system_message="You are a geography expert.",
          ...     max_tokens=100,
          ...     temperature=0.5
          ... )
          >>> print(result)
      """
      agent = QuestionAnsweringAgent(provider)
      return agent.get_answer(question, system_message, max_tokens, temperature)
  ```

---

### Step 2: Develop the Multi-Step Chatbot Agent

- **Functionality:**
  - Begins by asking a clarifying question based on the user input.
  - Uses the clarification to generate a final, context-aware answer.

- **Pseudocode:**
  ```python
  # agents/chatbot.py
  from agents.gemini_agent import GeminiAgent
  from agents.openai_agent import OpenAIAgent

  class ChatbotAgent:
      AVAILABLE_PROVIDERS = ["gemini", "openai"]
      
      def __init__(self, provider="gemini"):
          self.provider = provider.lower()
          if self.provider not in self.AVAILABLE_PROVIDERS:
              raise ValueError(f"Invalid provider: {provider}. Available providers: {', '.join(self.AVAILABLE_PROVIDERS)}")
              
          if self.provider == "openai":
              self.agent = OpenAIAgent()
          else:
              self.agent = GeminiAgent()

      def ask_clarification(self, initial_input: str, system_message: str = "You are a helpful assistant.", 
                           max_tokens: int = 50, temperature: float = 0.7) -> str:
          prompt_data = {
              "prompt": f"Ask a clarifying question for the following input:\n{initial_input}",
              "system_message": system_message,
              "max_tokens": max_tokens,
              "temperature": temperature
          }
          response = self.agent.process_prompt(prompt_data)
          return response["message"] if response["status"] == "success" else "Could not generate clarification."

      def generate_response(self, context: str, system_message: str = "You are a helpful assistant.", 
                           max_tokens: int = 150, temperature: float = 0.7) -> str:
          prompt_data = {
              "prompt": f"Using the following context, provide a helpful answer:\n{context}",
              "system_message": system_message,
              "max_tokens": max_tokens,
              "temperature": temperature
          }
          response = self.agent.process_prompt(prompt_data)
          return response["message"] if response["status"] == "success" else "Could not generate response."

  def agent_main(user_input: str, provider: str = "gemini", system_message: str = "You are a helpful assistant.", 
                max_tokens: int = 150, temperature: float = 0.7):
      """
      Direct call instructions:
      1. Import the chatbot agent and provide an initial input.
      2. The agent will first generate a clarifying question.
      3. It then uses the combined context to produce a final answer.
      
      Example:
          >>> from agents import chatbot
          >>> result = chatbot.agent_main(
          ...     "I need help with my account",
          ...     provider="gemini",  # or "openai"
          ...     system_message="You are a customer service representative.",
          ...     max_tokens=150,
          ...     temperature=0.7
          ... )
          >>> print(result)
      """
      agent = ChatbotAgent(provider)
      clarification = agent.ask_clarification(user_input, system_message, 50, temperature)
      # For demonstration, combine the initial input with the generated clarification.
      combined_context = f"{user_input}\nClarification: {clarification}"
      answer = agent.generate_response(combined_context, system_message, max_tokens, temperature)
      return {"clarification": clarification, "final_answer": answer}
  ```

---

### Step 3: Develop the Multi-Step Research Agent

- **Functionality:**
  - Accepts a research query.
  - Extracts key topics from the query.
  - Generates detailed analyses for each topic.
  - Aggregates the analyses into a comprehensive summary.

- **Pseudocode:**
  ```python
  # agents/research_agent.py
  from agents.gemini_agent import GeminiAgent
  from agents.openai_agent import OpenAIAgent

  class ResearchAgent:
      AVAILABLE_PROVIDERS = ["gemini", "openai"]
      
      def __init__(self, provider="gemini"):
          self.provider = provider.lower()
          if self.provider not in self.AVAILABLE_PROVIDERS:
              raise ValueError(f"Invalid provider: {provider}. Available providers: {', '.join(self.AVAILABLE_PROVIDERS)}")
              
          if self.provider == "openai":
              self.agent = OpenAIAgent()
          else:
              self.agent = GeminiAgent()

      def extract_topics(self, query: str, system_message: str = "You are a research assistant.", 
                        max_tokens: int = 60, temperature: float = 0.7) -> list:
          prompt_data = {
              "prompt": f"Extract key topics from the research query:\n{query}",
              "system_message": system_message,
              "max_tokens": max_tokens,
              "temperature": temperature
          }
          response = self.agent.process_prompt(prompt_data)
          if response["status"] == "success":
              topics = response["message"].strip().split(',')
              return [topic.strip() for topic in topics if topic.strip()]
          return ["No topics extracted"]

      def analyze_topic(self, topic: str, system_message: str = "You are a research analyst.", 
                       max_tokens: int = 150, temperature: float = 0.7) -> str:
          prompt_data = {
              "prompt": f"Provide a detailed analysis on the following topic:\n{topic}",
              "system_message": system_message,
              "max_tokens": max_tokens,
              "temperature": temperature
          }
          response = self.agent.process_prompt(prompt_data)
          return response["message"] if response["status"] == "success" else f"Could not analyze topic: {topic}"

      def aggregate_results(self, analyses: list) -> str:
          return "\n\n".join(analyses)

  def agent_main(query: str, provider: str = "gemini", system_message: str = "You are a research assistant.", 
                max_tokens: int = 150, temperature: float = 0.7):
      """
      Direct call instructions:
      1. Import the research agent.
      2. Pass a research query to agent_main().
      
      Example:
          >>> from agents import research_agent
          >>> result = research_agent.agent_main(
          ...     "Impact of climate change on agriculture",
          ...     provider="gemini",  # or "openai"
          ...     system_message="You are a climate science expert.",
          ...     max_tokens=200,
          ...     temperature=0.7
          ... )
          >>> print(result)
      """
      agent = ResearchAgent(provider)
      topics = agent.extract_topics(query, system_message, 60, temperature)
      analyses = [agent.analyze_topic(topic, system_message, max_tokens, temperature) for topic in topics]
      summary = agent.aggregate_results(analyses)
      return {"topics": topics, "analysis_summary": summary}
  ```

---

### Step 4: Develop the LLM-Enhanced Classifier Agent (Showcasing dspy Functionality)

- **Functionality:**
  - Uses rule-based logic (dspy-style) for initial classification.
  - Enhances the classification by calling an LLM to provide refined categorization and reasoning.

- **Pseudocode:**
  ```python
  # agents/llm_classifier.py
  import re
  from agents.gemini_agent import GeminiAgent
  from agents.openai_agent import OpenAIAgent

  class LLMClassifierAgent:
      AVAILABLE_PROVIDERS = ["gemini", "openai"]
      
      def __init__(self, provider="gemini"):
          self.provider = provider.lower()
          if self.provider not in self.AVAILABLE_PROVIDERS:
              raise ValueError(f"Invalid provider: {provider}. Available providers: {', '.join(self.AVAILABLE_PROVIDERS)}")
              
          if self.provider == "openai":
              self.agent = OpenAIAgent()
          else:
              self.agent = GeminiAgent()
          self.rules = {
              "Greeting": [r"\bhello\b", r"\bhi\b"],
              "Question": [r"\?$", r"\bwhat\b", r"\bhow\b"],
              "Command": [r"\bdo\b", r"\bexecute\b"]
          }

      def rule_based_classify(self, text: str) -> str:
          scores = {category: 0 for category in self.rules}
          for category, patterns in self.rules.items():
              for pattern in patterns:
                  if re.search(pattern, text.lower()):
                      scores[category] += 1
          # Return the category with the highest score
          return max(scores, key=scores.get)

      def refine_classification(self, text: str, initial_classification: str, 
                               system_message: str = "You are a text classification expert.", 
                               max_tokens: int = 100, temperature: float = 0.7) -> str:
          prompt = (
              f"Given the input text: '{text}' and an initial classification of "
              f"'{initial_classification}', provide a refined classification with reasoning."
          )
          prompt_data = {
              "prompt": prompt,
              "system_message": system_message,
              "max_tokens": max_tokens,
              "temperature": temperature
          }
          response = self.agent.process_prompt(prompt_data)
          return response["message"] if response["status"] == "success" else "Could not refine classification."

  def agent_main(text: str, provider: str = "gemini", system_message: str = "You are a text classification expert.", 
                max_tokens: int = 100, temperature: float = 0.7):
      """
      Direct call instructions:
      1. Import the LLM classifier agent.
      2. Call agent_main() with the input text.
      
      Example:
          >>> from agents import llm_classifier
          >>> result = llm_classifier.agent_main(
          ...     "Hi, can you help me?",
          ...     provider="gemini",  # or "openai"
          ...     system_message="You are a text classification expert.",
          ...     max_tokens=100,
          ...     temperature=0.7
          ... )
          >>> print(result)
      """
      agent = LLMClassifierAgent(provider)
      initial_class = agent.rule_based_classify(text)
      refined = agent.refine_classification(text, initial_class, system_message, max_tokens, temperature)
      return {"initial_classification": initial_class, "refined_classification": refined}
  ```
- **Notes:**  
  This agent demonstrates dspy functionality by merging pattern-based classification with LLM-based refinement.

---

### Step 5: Develop the Multi-Step Research Analyzer Agent (Showcasing dspy Functionality)

- **Functionality:**
  - Extracts critical components from a query using dspy-inspired patterns.
  - Performs multi-step analysis on each extracted element via LLM calls.
  - Aggregates and returns a comprehensive analysis.

- **Pseudocode:**
  ```python
  # agents/research_analyzer.py
  import re
  from agents.gemini_agent import GeminiAgent
  from agents.openai_agent import OpenAIAgent

  class ResearchAnalyzerAgent:
      AVAILABLE_PROVIDERS = ["gemini", "openai"]
      
      def __init__(self, provider="gemini"):
          self.provider = provider.lower()
          if self.provider not in self.AVAILABLE_PROVIDERS:
              raise ValueError(f"Invalid provider: {provider}. Available providers: {', '.join(self.AVAILABLE_PROVIDERS)}")
              
          if self.provider == "openai":
              self.agent = OpenAIAgent()
          else:
              self.agent = GeminiAgent()
          # dspy-inspired patterns for extraction
          self.patterns = {
              "Key Points": [r"\bimportant\b", r"\bnotable\b"],
              "Questions": [r"\bwhy\b", r"\bhow\b", r"\bwhat\b"]
          }

      def extract_elements(self, text: str) -> dict:
          extracted = {key: [] for key in self.patterns}
          for key, patterns in self.patterns.items():
              for pattern in patterns:
                  if re.search(pattern, text.lower()):
                      extracted[key].append(pattern)
          return extracted

      def analyze_element(self, element: str, system_message: str = "You are a research analyst.", 
                         max_tokens: int = 120, temperature: float = 0.7) -> str:
          prompt_data = {
              "prompt": f"Provide an in-depth analysis of the element: {element}",
              "system_message": system_message,
              "max_tokens": max_tokens,
              "temperature": temperature
          }
          response = self.agent.process_prompt(prompt_data)
          return response["message"] if response["status"] == "success" else f"Could not analyze element: {element}"

      def multi_step_analysis(self, text: str, system_message: str = "You are a research analyst.", 
                             max_tokens: int = 120, temperature: float = 0.7) -> dict:
          elements = self.extract_elements(text)
          analysis = {}
          for category, elems in elements.items():
              analysis[category] = [self.analyze_element(elem, system_message, max_tokens, temperature) for elem in elems]
          return analysis

  def agent_main(text: str, provider: str = "gemini", system_message: str = "You are a research analyst.", 
                max_tokens: int = 120, temperature: float = 0.7):
      """
      Direct call instructions:
      1. Import the research analyzer agent.
      2. Call agent_main() with the text to be analyzed.
      
      Example:
          >>> from agents import research_analyzer
          >>> result = research_analyzer.agent_main(
          ...     "Discuss the important factors and why they matter in climate change",
          ...     provider="gemini",  # or "openai"
          ...     system_message="You are a climate science expert.",
          ...     max_tokens=150,
          ...     temperature=0.7
          ... )
          >>> print(result)
      """
      agent = ResearchAnalyzerAgent(provider)
      analysis = agent.multi_step_analysis(text, system_message, max_tokens, temperature)
      return {"analysis": analysis}
  ```
- **Notes:**  
  This multi-step agent uses dspy-inspired extraction followed by in-depth analysis to demonstrate advanced functionality.

---

## Integration with FastAPI and Testing

- **Dynamic Endpoint:**  
  Each agent module is loaded via the existing dynamic endpoint `/agent/{agent_name}`.
  
- **Testing:**  
  - Create automated tests under the `/tests` folder verifying:
    - Correct functionality for each agent.
    - Multi-step process outcomes.
    - dspy enhancements in agents 4 and 5.
    - Provider switching between Gemini and OpenAI.
    - Parameter handling for system_message, max_tokens, and temperature.
  
- **Logging:**  
  Document progress, test results, and any issues in **/logs/4-llm-agents-logs.md**.

---

## Summary

This plan outlines the implementation of five LLM agents:

1. **Question Answering Agent** – Provides direct answers to user questions.
2. **Multi-Step Chatbot Agent** – Engages users in a multi-turn conversation for context-aware responses.
3. **Multi-Step Research Agent** – Decomposes research queries into topics and aggregates detailed analyses.
4. **LLM-Enhanced Classifier Agent (dspy)** – Combines rule-based classification with LLM refinement.
5. **Multi-Step Research Analyzer Agent (dspy)** – Extracts key elements using dspy patterns and provides comprehensive analyses.

Each agent includes detailed pseudocode and inline instructions to facilitate easy integration, testing, and future enhancements. All agents will use Gemini as the default LLM provider with the option to switch to OpenAI, and will support common parameters for system message, token limits, and temperature settings.