# Testing and Validation Guide

This document outlines the testing strategy and validation procedures for the FastAPI Agent System.

## Test Coverage

### Core Functionality Tests

1. **Base Application Tests**
   - Root endpoint returns welcome message
   - Health check endpoint returns status
   - Favicon endpoint returns SVG icon
   - `/agents` endpoint returns list of all available agents

2. **Error Handling Tests**
   - Non-existent agent returns 404
   - Invalid agent file returns appropriate error
   - Missing parameters return validation errors

### Agent-Specific Tests

1. **Simple Agents (No Parameters)**
   - **Hello World Agent**
     - Returns correct message
     - Response format validation
   
   - **Goodbye Agent**
     - Returns correct message
     - Response format validation
   
   - **Echo Agent**
     - Returns echo message
     - Response format validation
   
   - **Time Agent**
     - Returns current time
     - Validates ISO 8601 format
     - Response format validation
   
   - **Joke Agent**
     - Returns random joke
     - Validates string content
     - Response format validation
   
   - **Quote Agent**
     - Returns random quote
     - Validates string content
     - Response format validation

2. **Complex Agents (With Parameters)**
   - **Math Agent**
     - Valid token and expression returns correct result
     - Invalid token returns error message
     - Invalid expression returns error message
     - Missing parameters return appropriate errors
   
   - **Classifier Agent**
     - Valid input text returns classification and confidence
     - Validates classification categories
     - Validates confidence score range
     - Missing input text returns appropriate error
   
   - **Summarizer Agent**
     - Valid input text returns summary and explanation
     - Validates summary format
     - Validates explanation presence
     - Missing input text returns appropriate error

## Test Implementation

Tests are implemented in the `/tests` directory:

1. **test_main.py**
   - Tests core application functionality
   - Tests error handling
   - Tests health checks and basic endpoints

2. **test_agents.py**
   - Tests each agent's functionality
   - Tests parameter validation
   - Tests response formats
   - Tests error scenarios

## Running Tests

Execute tests using pytest:
```bash
python -m pytest tests/
```

## Test Examples

### Core Endpoint Tests
```python
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_agents_endpoint():
    response = client.get("/agents")
    assert response.status_code == 200
    assert "agents" in response.json()
```

### Agent Tests
```python
def test_math_agent():
    response = client.get("/agent/math?token=MATH_SECRET&expression=3*(4%2B2)")
    assert response.status_code == 200
    assert response.json() == {"agent": "math", "result": 18}

def test_classifier_agent():
    response = client.get("/agent/classifier?INPUT_TEXT=Hello,%20how%20are%20you?")
    assert response.status_code == 200
    result = response.json()
    assert "classification" in result["result"]
    assert "confidence" in result["result"]
```

## Validation Criteria

1. **Response Format**
   - All responses must follow the standard format:
     ```json
     {
       "agent": "<agent_name>",
       "result": <agent-specific output>
     }
     ```

2. **Error Handling**
   - All errors must return appropriate HTTP status codes
   - Error messages must be clear and informative
   - Sensitive information must not be exposed in error messages

3. **Performance**
   - Response times should be reasonable
   - Memory usage should be efficient
   - No memory leaks in agent loading/unloading

## Continuous Integration

- Tests are run automatically on each commit
- All tests must pass before deployment
- Test coverage should be maintained or improved with new features

## Future Test Improvements

1. **Load Testing**
   - Implement performance tests for concurrent requests
   - Test system behavior under heavy load

2. **Integration Testing**
   - Add tests for future integrations (e.g., Supabase)
   - Test system behavior in production-like environments

3. **Security Testing**
   - Add penetration testing scenarios
   - Test for common vulnerabilities
   - Validate input sanitization
