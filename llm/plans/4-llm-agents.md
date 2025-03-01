Below is the proposed **/plans/4-llm-agents.md** document outlining the implementation of five LLM agents. This plan details each agent's objective, functionality, and pseudocode. Inline comments guide users on how to call the agents directly, and progress should be logged in the **/logs/4-llm-agents-logs.md** file.

---

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

Each agent will be developed as a separate module within the `agents/` folder. The agents use LLM calls (e.g., via OpenAI) and, for the dspy-enabled ones, combine rule-based processing with LLM refinement. Detailed pseudocode is provided to illustrate the intended functionality.

---

## Implementation Steps

### Step 1: Develop the Question Answering Agent

- **Functionality:**
  - Receives a question as input.
  - Sends the question to an LLM provider.
  - Returns the generated answer.

- **Pseudocode:**
  ```python
  # agents/question_answering.py
  import openai
  from os import getenv

  class QuestionAnsweringAgent:
      def __init__(self):
          openai.api_key = getenv("OPENAI_API_KEY")

      def get_answer(self, question: str) -> dict:
          response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=f"Answer the following question:\n{question}",
              max_tokens=150
          )
          return {"answer": response.choices[0].text.strip()}

  def agent_main(question: str):
      """
      Direct call instructions:
      1. Import the agent and set your question.
      2. Call agent_main() with the question string.
      
      Example:
          >>> from agents import question_answering
          >>> result = question_answering.agent_main("What is the capital of France?")
          >>> print(result)  # Expected output: {'answer': 'Paris'}
      """
      agent = QuestionAnsweringAgent()
      return agent.get_answer(question)
  ```

---

### Step 2: Develop the Multi-Step Chatbot Agent

- **Functionality:**
  - Begins by asking a clarifying question based on the user input.
  - Uses the clarification to generate a final, context-aware answer.

- **Pseudocode:**
  ```python
  # agents/chatbot.py
  import openai
  from os import getenv

  class ChatbotAgent:
      def __init__(self):
          openai.api_key = getenv("OPENAI_API_KEY")

      def ask_clarification(self, initial_input: str) -> str:
          prompt = f"Ask a clarifying question for the following input:\n{initial_input}"
          response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=prompt,
              max_tokens=50
          )
          return response.choices[0].text.strip()

      def generate_response(self, context: str) -> str:
          prompt = f"Using the following context, provide a helpful answer:\n{context}"
          response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=prompt,
              max_tokens=150
          )
          return response.choices[0].text.strip()

  def agent_main(user_input: str):
      """
      Direct call instructions:
      1. Import the chatbot agent and provide an initial input.
      2. The agent will first generate a clarifying question.
      3. It then uses the combined context to produce a final answer.
      
      Example:
          >>> from agents import chatbot
          >>> result = chatbot.agent_main("I need help with my account")
          >>> print(result)
      """
      agent = ChatbotAgent()
      clarification = agent.ask_clarification(user_input)
      # For demonstration, combine the initial input with the generated clarification.
      combined_context = f"{user_input}\nClarification: {clarification}"
      answer = agent.generate_response(combined_context)
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
  import openai
  from os import getenv

  class ResearchAgent:
      def __init__(self):
          openai.api_key = getenv("OPENAI_API_KEY")

      def extract_topics(self, query: str) -> list:
          prompt = f"Extract key topics from the research query:\n{query}"
          response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=prompt,
              max_tokens=60
          )
          topics = response.choices[0].text.strip().split(',')
          return [topic.strip() for topic in topics if topic.strip()]

      def analyze_topic(self, topic: str) -> str:
          prompt = f"Provide a detailed analysis on the following topic:\n{topic}"
          response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=prompt,
              max_tokens=150
          )
          return response.choices[0].text.strip()

      def aggregate_results(self, analyses: list) -> str:
          return "\n\n".join(analyses)

  def agent_main(query: str):
      """
      Direct call instructions:
      1. Import the research agent.
      2. Pass a research query to agent_main().
      
      Example:
          >>> from agents import research_agent
          >>> result = research_agent.agent_main("Impact of climate change on agriculture")
          >>> print(result)
      """
      agent = ResearchAgent()
      topics = agent.extract_topics(query)
      analyses = [agent.analyze_topic(topic) for topic in topics]
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
  import openai
  from os import getenv

  class LLMClassifierAgent:
      def __init__(self):
          openai.api_key = getenv("OPENAI_API_KEY")
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

      def refine_classification(self, text: str, initial_classification: str) -> str:
          prompt = (
              f"Given the input text: '{text}' and an initial classification of "
              f"'{initial_classification}', provide a refined classification with reasoning."
          )
          response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=prompt,
              max_tokens=100
          )
          return response.choices[0].text.strip()

  def agent_main(text: str):
      """
      Direct call instructions:
      1. Import the LLM classifier agent.
      2. Call agent_main() with the input text.
      
      Example:
          >>> from agents import llm_classifier
          >>> result = llm_classifier.agent_main("Hi, can you help me?")
          >>> print(result)
      """
      agent = LLMClassifierAgent()
      initial_class = agent.rule_based_classify(text)
      refined = agent.refine_classification(text, initial_class)
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
  import openai
  from os import getenv

  class ResearchAnalyzerAgent:
      def __init__(self):
          openai.api_key = getenv("OPENAI_API_KEY")
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

      def analyze_element(self, element: str) -> str:
          prompt = f"Provide an in-depth analysis of the element: {element}"
          response = openai.Completion.create(
              engine="text-davinci-003",
              prompt=prompt,
              max_tokens=120
          )
          return response.choices[0].text.strip()

      def multi_step_analysis(self, text: str) -> dict:
          elements = self.extract_elements(text)
          analysis = {}
          for category, elems in elements.items():
              analysis[category] = [self.analyze_element(elem) for elem in elems]
          return analysis

  def agent_main(text: str):
      """
      Direct call instructions:
      1. Import the research analyzer agent.
      2. Call agent_main() with the text to be analyzed.
      
      Example:
          >>> from agents import research_analyzer
          >>> result = research_analyzer.agent_main("Discuss the important factors and why they matter in climate change")
          >>> print(result)
      """
      agent = ResearchAnalyzerAgent()
      analysis = agent.multi_step_analysis(text)
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

Each agent includes detailed pseudocode and inline instructions to facilitate easy integration, testing, and future enhancements.

--- 

Please review this document and let me know if any additional details or modifications are required.