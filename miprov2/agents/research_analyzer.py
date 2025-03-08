# llm/agents/research_analyzer.py
from typing import Dict, Any, Optional, List
from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from .openai_agent import OpenAIAgent
from .gemini_agent import GeminiAgent

class ProviderEnum(str, Enum):
    gemini = "gemini"
    openai = "openai"

class ResearchAnalyzerRequest(BaseModel):
    query: str = Field(..., description="The research query to analyze")
    provider: ProviderEnum = Field(ProviderEnum.gemini, description="LLM provider to use (gemini or openai)")
    system_message: Optional[str] = Field("You are a research analysis expert.", description="System message to set context")
    max_tokens: Optional[int] = Field(300, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    
    @field_validator('query')
    def query_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v

class ResearchAnalyzerAgent:
    """
    Multi-Step Research Analyzer Agent
    ----------
    Purpose: Extract key elements from a research query using dspy-inspired patterns
    and provide comprehensive analyses.
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
            
        # Define research analysis patterns (dspy-inspired)
        self.patterns = {
            "entities": {
                "prompt": "Extract the key entities (people, organizations, locations, concepts) from the following research query: '{query}'",
                "output_format": "List the entities in JSON format with categories: {{'people': [], 'organizations': [], 'locations': [], 'concepts': []}}"
            },
            "questions": {
                "prompt": "Generate 3-5 specific research questions that would help investigate the following query: '{query}'",
                "output_format": "List the questions in JSON format: {{'questions': []}}"
            },
            "timeline": {
                "prompt": "Create a potential timeline of key events related to the following research query: '{query}'",
                "output_format": "List the timeline events in JSON format: {{'timeline': []}}"
            },
            "perspectives": {
                "prompt": "Identify 2-3 different perspectives or viewpoints on the following research query: '{query}'",
                "output_format": "List the perspectives in JSON format: {{'perspectives': []}}"
            }
        }

    def extract_entities(self, query: str, system_message: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """
        Extract key entities from the research query.
        
        Args:
            query: The research query
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the extracted entities
        """
        pattern = self.patterns["entities"]
        prompt = pattern["prompt"].format(query=query)
        output_format = pattern["output_format"]
        
        full_prompt = f"{prompt}\n\n{output_format}"
        
        prompt_data = {
            "prompt": full_prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                # Try to extract JSON from the response
                message = response["message"].strip()
                
                # Simple JSON extraction (in a real implementation, use a more robust method)
                import json
                import re
                
                # Look for JSON-like structure
                json_match = re.search(r'\{.*\}', message, re.DOTALL)
                if json_match:
                    try:
                        entities = json.loads(json_match.group(0))
                        return {
                            "status": "success",
                            "entities": entities,
                            "model": response.get("model", "unknown")
                        }
                    except json.JSONDecodeError:
                        pass
                
                # Fallback: return the raw message
                return {
                    "status": "success",
                    "entities": {
                        "raw": message,
                        "note": "Failed to parse JSON, returning raw output"
                    },
                    "model": response.get("model", "unknown")
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "model": "none"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error extracting entities: {str(e)}",
                "model": "none"
            }

    def generate_questions(self, query: str, system_message: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """
        Generate specific research questions based on the query.
        
        Args:
            query: The research query
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the generated questions
        """
        pattern = self.patterns["questions"]
        prompt = pattern["prompt"].format(query=query)
        output_format = pattern["output_format"]
        
        full_prompt = f"{prompt}\n\n{output_format}"
        
        prompt_data = {
            "prompt": full_prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                # Try to extract JSON from the response
                message = response["message"].strip()
                
                # Simple JSON extraction (in a real implementation, use a more robust method)
                import json
                import re
                
                # Look for JSON-like structure
                json_match = re.search(r'\{.*\}', message, re.DOTALL)
                if json_match:
                    try:
                        questions = json.loads(json_match.group(0))
                        return {
                            "status": "success",
                            "questions": questions,
                            "model": response.get("model", "unknown")
                        }
                    except json.JSONDecodeError:
                        pass
                
                # Fallback: return the raw message
                return {
                    "status": "success",
                    "questions": {
                        "raw": message,
                        "note": "Failed to parse JSON, returning raw output"
                    },
                    "model": response.get("model", "unknown")
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "model": "none"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating questions: {str(e)}",
                "model": "none"
            }

    def create_timeline(self, query: str, system_message: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """
        Create a potential timeline of key events related to the query.
        
        Args:
            query: The research query
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the timeline events
        """
        pattern = self.patterns["timeline"]
        prompt = pattern["prompt"].format(query=query)
        output_format = pattern["output_format"]
        
        full_prompt = f"{prompt}\n\n{output_format}"
        
        prompt_data = {
            "prompt": full_prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                # Try to extract JSON from the response
                message = response["message"].strip()
                
                # Simple JSON extraction (in a real implementation, use a more robust method)
                import json
                import re
                
                # Look for JSON-like structure
                json_match = re.search(r'\{.*\}', message, re.DOTALL)
                if json_match:
                    try:
                        timeline = json.loads(json_match.group(0))
                        return {
                            "status": "success",
                            "timeline": timeline,
                            "model": response.get("model", "unknown")
                        }
                    except json.JSONDecodeError:
                        pass
                
                # Fallback: return the raw message
                return {
                    "status": "success",
                    "timeline": {
                        "raw": message,
                        "note": "Failed to parse JSON, returning raw output"
                    },
                    "model": response.get("model", "unknown")
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "model": "none"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error creating timeline: {str(e)}",
                "model": "none"
            }

    def identify_perspectives(self, query: str, system_message: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """
        Identify different perspectives or viewpoints on the query.
        
        Args:
            query: The research query
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the identified perspectives
        """
        pattern = self.patterns["perspectives"]
        prompt = pattern["prompt"].format(query=query)
        output_format = pattern["output_format"]
        
        full_prompt = f"{prompt}\n\n{output_format}"
        
        prompt_data = {
            "prompt": full_prompt,
            "system_message": system_message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                # Try to extract JSON from the response
                message = response["message"].strip()
                
                # Simple JSON extraction (in a real implementation, use a more robust method)
                import json
                import re
                
                # Look for JSON-like structure
                json_match = re.search(r'\{.*\}', message, re.DOTALL)
                if json_match:
                    try:
                        perspectives = json.loads(json_match.group(0))
                        return {
                            "status": "success",
                            "perspectives": perspectives,
                            "model": response.get("model", "unknown")
                        }
                    except json.JSONDecodeError:
                        pass
                
                # Fallback: return the raw message
                return {
                    "status": "success",
                    "perspectives": {
                        "raw": message,
                        "note": "Failed to parse JSON, returning raw output"
                    },
                    "model": response.get("model", "unknown")
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "model": "none"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error identifying perspectives: {str(e)}",
                "model": "none"
            }

    def generate_comprehensive_analysis(self, query: str, entities: Dict[str, Any], questions: Dict[str, Any], 
                                      timeline: Dict[str, Any], perspectives: Dict[str, Any], 
                                      system_message: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis based on all the extracted information.
        
        Args:
            query: The research query
            entities: The extracted entities
            questions: The generated questions
            timeline: The timeline events
            perspectives: The identified perspectives
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the comprehensive analysis
        """
        # Create a prompt that includes all the extracted information
        prompt = (
            f"Based on the following research query and extracted information, provide a comprehensive analysis:\n\n"
            f"QUERY: {query}\n\n"
            f"ENTITIES: {entities}\n\n"
            f"QUESTIONS: {questions}\n\n"
            f"TIMELINE: {timeline}\n\n"
            f"PERSPECTIVES: {perspectives}\n\n"
            f"Your analysis should synthesize this information into a coherent narrative that addresses the key aspects of the research query."
        )
        
        prompt_data = {
            "prompt": prompt,
            "system_message": system_message,
            "max_tokens": max_tokens * 2,  # Allow more tokens for the comprehensive analysis
            "temperature": temperature
        }
        
        try:
            response = self.agent.process_prompt(prompt_data)
            
            if response["status"] == "success":
                return {
                    "status": "success",
                    "analysis": response["message"].strip(),
                    "model": response.get("model", "unknown"),
                    "usage": response.get("usage", {})
                }
            else:
                return {
                    "status": "error",
                    "message": response.get("message", "Unknown error"),
                    "model": "none"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating comprehensive analysis: {str(e)}",
                "model": "none"
            }

    def analyze(self, query: str, system_message: str = "You are a research analysis expert.", 
              max_tokens: int = 300, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Analyze a research query using a multi-step approach.
        
        Args:
            query: The research query
            system_message: System message to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            A dictionary with the analysis results
        """
        try:
            # Step 1: Extract entities
            entities_result = self.extract_entities(query, system_message, max_tokens, temperature)
            if entities_result["status"] == "error":
                return entities_result
            
            # Step 2: Generate questions
            questions_result = self.generate_questions(query, system_message, max_tokens, temperature)
            if questions_result["status"] == "error":
                return questions_result
            
            # Step 3: Create timeline
            timeline_result = self.create_timeline(query, system_message, max_tokens, temperature)
            if timeline_result["status"] == "error":
                return timeline_result
            
            # Step 4: Identify perspectives
            perspectives_result = self.identify_perspectives(query, system_message, max_tokens, temperature)
            if perspectives_result["status"] == "error":
                return perspectives_result
            
            # Step 5: Generate comprehensive analysis
            analysis_result = self.generate_comprehensive_analysis(
                query,
                entities_result.get("entities", {}),
                questions_result.get("questions", {}),
                timeline_result.get("timeline", {}),
                perspectives_result.get("perspectives", {}),
                system_message,
                max_tokens,
                temperature
            )
            
            # Combine all results
            return {
                "status": "success",
                "query": query,
                "entities": entities_result.get("entities", {}),
                "questions": questions_result.get("questions", {}),
                "timeline": timeline_result.get("timeline", {}),
                "perspectives": perspectives_result.get("perspectives", {}),
                "comprehensive_analysis": analysis_result.get("analysis", ""),
                "model": analysis_result.get("model", "unknown"),
                "usage": analysis_result.get("usage", {})
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": "none"
            }

def register_routes(router: APIRouter):
    """
    Register routes for the ResearchAnalyzerAgent.
    """
    @router.post("/research-analyze", summary="Analyze research query using dspy-inspired patterns", tags=["Advanced LLM Agents"])
    async def analyze_research(request: ResearchAnalyzerRequest):
        """
        Analyze a research query using dspy-inspired patterns to extract key elements and provide comprehensive analyses.
        
        **Input:**

        * **query (required, string):** The research query to analyze
        * **provider (optional, string):** The LLM provider to use (gemini or openai). Default: gemini
        * **system_message (optional, string):** System message to set context
        * **max_tokens (optional, integer):** Maximum tokens to generate
        * **temperature (optional, float):** Sampling temperature

        **Process:** This agent demonstrates dspy-inspired functionality by:
        1. Extracting key entities (people, organizations, locations, concepts)
        2. Generating specific research questions
        3. Creating a potential timeline of key events
        4. Identifying different perspectives or viewpoints
        5. Generating a comprehensive analysis that synthesizes all the extracted information

        **Available Providers:**
        * gemini (default)
        * openai

        **Example Input (JSON body):**

        ```json
        {
          "query": "Impact of artificial intelligence on healthcare",
          "provider": "gemini",
          "system_message": "You are a research analysis expert.",
          "max_tokens": 300,
          "temperature": 0.7
        }
        ```

        **Example Output:**

        ```json
        {
          "status": "success",
          "query": "Impact of artificial intelligence on healthcare",
          "entities": {
            "people": ["researchers", "healthcare professionals", "patients"],
            "organizations": ["hospitals", "research institutions", "tech companies"],
            "locations": ["global healthcare systems"],
            "concepts": ["artificial intelligence", "machine learning", "healthcare", "diagnosis", "treatment"]
          },
          "questions": {
            "questions": [
              "How is AI currently being used in diagnostic procedures?",
              "What are the ethical implications of AI in healthcare decision-making?",
              "How does AI impact the role of healthcare professionals?",
              "What are the cost implications of implementing AI in healthcare systems?",
              "How does AI affect patient privacy and data security in healthcare?"
            ]
          },
          "timeline": {
            "timeline": [
              {"year": "1950s-1960s", "event": "Early AI research and theoretical foundations"},
              {"year": "1970s-1980s", "event": "First medical expert systems developed"},
              {"year": "1990s-2000s", "event": "Machine learning applications in medical imaging"},
              {"year": "2010-2015", "event": "Deep learning breakthroughs in medical diagnostics"},
              {"year": "2016-2020", "event": "FDA approvals for AI-based medical devices"},
              {"year": "2020-Present", "event": "Widespread integration of AI in clinical workflows"}
            ]
          },
          "perspectives": {
            "perspectives": [
              {"viewpoint": "Technological Optimism", "description": "AI will revolutionize healthcare by improving accuracy, efficiency, and access to care."},
              {"viewpoint": "Clinical Caution", "description": "AI should complement, not replace, human judgment in healthcare settings."},
              {"viewpoint": "Ethical Concerns", "description": "AI raises issues of privacy, bias, accountability, and the changing doctor-patient relationship."}
            ]
          },
          "comprehensive_analysis": "The integration of artificial intelligence into healthcare represents one of the most significant technological shifts in modern medicine...",
          "model": "gemini-2.0",
          "usage": {
            "prompt_tokens": 450,
            "completion_tokens": 320,
            "total_tokens": 770,
            "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
          }
        }
        ```

        **Example Output (if query is empty):**

        ```json
        {
          "status": "error",
          "message": "Query cannot be empty",
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
            agent = ResearchAnalyzerAgent(provider=request.provider)
            result = agent.analyze(
                query=request.query,
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