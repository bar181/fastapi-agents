# tests/test_llm_agents.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_setup():
    """Test that the test framework is operational."""
    assert True

def test_openai_hello_endpoint():
    """Test that the OpenAI hello endpoint is accessible."""
    response = client.get("/llm/openai-hello")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    # The response format has changed from placeholder to actual API call
    assert data["status"] in ["success", "error"]

def test_openai_prompt_endpoint():
    """Test that the OpenAI prompt POST endpoint is accessible."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/openai-prompt", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    assert data["status"] in ["success", "error"]
    if data["status"] == "success":
        assert "usage" in data

def test_gemini_hello_endpoint():
    """Test that the Gemini hello endpoint is accessible."""
    response = client.get("/llm/gemini-hello")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "note" in data
    assert "Gemini agent received" in data["message"]

def test_agent_prompt_endpoint_default():
    """Test that the agent prompt endpoint defaults to Gemini."""
    response = client.get("/llm/agent-prompt?INPUT_TEXT=Test")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "note" in data
    assert "Gemini agent received" in data["message"]

def test_agent_prompt_endpoint_openai():
    """Test that the agent prompt endpoint can use OpenAI."""
    response = client.get("/llm/agent-prompt?INPUT_TEXT=Test&provider=openai")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    # The response format has changed from placeholder to actual API call
    assert data["status"] in ["success", "error"]