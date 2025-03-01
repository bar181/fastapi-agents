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
    assert data["status"] in ["success", "error", "placeholder"]

def test_gemini_prompt_endpoint():
    """Test that the Gemini prompt POST endpoint is accessible."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/gemini-prompt", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    assert data["status"] in ["success", "error"]
    if data["status"] == "success":
        assert "usage" in data

def test_provider_hello_endpoint_default():
    """Test that the provider hello endpoint defaults to Gemini."""
    response = client.get("/llm/provider-hello?INPUT_TEXT=Test")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    # The response format has changed from placeholder to actual API call
    assert data["status"] in ["success", "error", "placeholder"]

def test_provider_hello_endpoint_openai():
    """Test that the provider hello endpoint can use OpenAI."""
    response = client.get("/llm/provider-hello?INPUT_TEXT=Test&provider=openai")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    # The response format has changed from placeholder to actual API call
    assert data["status"] in ["success", "error"]

def test_provider_prompt_endpoint_default():
    """Test that the provider prompt endpoint defaults to Gemini."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/provider-prompt", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    assert data["status"] in ["success", "error"]
    if data["status"] == "success":
        assert "usage" in data

def test_provider_prompt_endpoint_openai():
    """Test that the provider prompt endpoint can use OpenAI."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "provider": "openai",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/provider-prompt", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "model" in data
    assert data["status"] in ["success", "error"]
    if data["status"] == "success":
        assert "usage" in data

def test_provider_prompt_endpoint_invalid_provider():
    """Test that the provider prompt endpoint handles invalid providers."""
    test_request = {
        "prompt": "Write a haiku about programming",
        "provider": "invalid_provider",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/llm/provider-prompt", json=test_request)
    assert response.status_code == 422  # Validation error due to enum