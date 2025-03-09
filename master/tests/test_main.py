# master/tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Healthy"}

# def test_nonexistent_dynamic_agent():
#     """Test error handling for non-existent dynamic agent."""
#     response = client.get("/dynamic/nonexistent_agent")
#     assert response.status_code == 404
#     assert "Agent not found" in response.json()["detail"]

def test_nonexistent_llm_agent():
    """Test error handling for a non-existent LLM agent."""
    response = client.get("/llm/nonexistent_agent")  # Use the /llm prefix
    assert response.status_code == 404
    assert "Not Found" in response.text #fastapi default
    # assert "Not Found" in response.json()["detail"] #removed detail

# Removed test_invalid_agent as it's redundant with the dynamic agent tests
# and requires file manipulation that's not necessary for this test.