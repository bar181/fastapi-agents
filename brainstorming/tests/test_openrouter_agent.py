import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_setup():
    """Test that the test framework is operational."""
    assert True

def test_openrouter_hello_endpoint():
    """Test that the OpenRouter hello endpoint is accessible."""
    response = client.get("/llm/openrouter-hello")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    # The response format has changed from placeholder to actual API call
    assert data["status"] in ["success", "error"]

def test_openrouter_prompt_endpoint():
    """Test that the OpenRouter prompt POST endpoint is accessible."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/openrouter-prompt", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    assert data["status"] in ["success", "error"]
    if data["status"] == "success":
        assert "usage" in data

def test_openrouter_prompt_endpoint_with_custom_model():
    """Test that the OpenRouter prompt endpoint can use a custom model."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "model": "anthropic/claude-3-haiku",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/openrouter-prompt", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    assert data["status"] in ["success", "error"]
    if data["status"] == "success":
        assert "usage" in data
        assert data["model"] == "anthropic/claude-3-haiku"

def test_openrouter_prompt_endpoint_with_invalid_model():
    """Test that the OpenRouter prompt endpoint handles invalid models correctly."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "model": "invalid_model",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/openrouter-prompt", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    # Should fall back to default model
    assert data["model"] != "invalid_model"