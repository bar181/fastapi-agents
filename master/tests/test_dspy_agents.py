from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_classifier_agent_with_input():
    """Test classifier agent with input text."""
    response = client.get("/agent/classifier?INPUT_TEXT=Hello,%20how%20are%20you?")
    assert response.status_code == 200
    result = response.json()
    assert "classification" in result
    assert "confidence" in result
    assert result["classification"] in ["Greeting/Question", "Greeting", "Question", "Command", "Statement"]
    assert isinstance(result["confidence"], float)

def test_classifier_agent_no_input():
    """Test classifier agent with no input text (should return an error)."""
    response = client.get("/agent/classifier")  # No INPUT_TEXT provided
    assert response.status_code == 200  # Expecting a 200 OK, even with the error message
    result = response.json()
    assert result == {"error": "INPUT_TEXT is not provided or is not a valid string."}

def test_classifier_agent_empty_input():
    """Test with empty input string"""
    response = client.get("/agent/classifier?INPUT_TEXT=")  # Empty INPUT_TEXT
    assert response.status_code == 200
    result = response.json()
    assert result == {"error": "INPUT_TEXT is not provided or is not a valid string."}

def test_classifier_agent_statement():
    """Test with a simple statement."""
    response = client.get("/agent/classifier?INPUT_TEXT=This%20is%20a%20statement.")
    assert response.status_code == 200
    result = response.json()
    # Ensure the response includes the necessary keys
    assert "classification" in result
    assert "confidence" in result
    # For a simple statement, we expect the classification to be "Statement"
    assert result["classification"] == "Statement"
    assert isinstance(result["confidence"], float)

