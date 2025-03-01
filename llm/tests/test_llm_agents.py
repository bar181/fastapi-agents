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
    assert "note" in data
    assert "OpenAI agent received" in data["message"]

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
    assert "note" in data
    assert "OpenAI agent received" in data["message"]