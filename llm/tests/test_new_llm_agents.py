# llm/tests/test_new_llm_agents.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Sentiment Analyzer Tests
def test_sentiment_analyzer_positive():
    """Test positive sentiment analysis."""
    response = client.post(
        "/llm/sentiment",
        json={"text": "I love this product! It's amazing!", "model": "gpt-4o-mini"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["sentiment"] == "positive"

def test_sentiment_analyzer_negative():
    """Test negative sentiment analysis."""
    response = client.post(
        "/llm/sentiment",
        json={"text": "I hate this product! It's terrible!", "model": "gpt-4o-mini"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["sentiment"] == "negative"

def test_sentiment_analyzer_neutral():
    """Test neutral sentiment analysis."""
    response = client.post(
        "/llm/sentiment",
        json={"text": "This is a product.", "model": "gpt-4o-mini"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["sentiment"] == "neutral"

def test_sentiment_analyzer_error():
    """Test error handling in sentiment analysis."""
    response = client.post(
        "/llm/sentiment",
        json={"text": "", "model": "invalid-model"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "error"

# Summarization Tests
def test_summarization_success():
    """Test successful text summarization."""
    text = "The quick brown fox jumps over the lazy dog. This is a test sentence for summarization."
    response = client.post(
        "/llm/summarize",
        json={"text": text, "model": "gpt-4o-mini", "max_tokens": 20}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "summary" in response.json()
    assert len(response.json()["summary"]) > 0

def test_summarization_empty_text():
    """Test summarization with empty text."""
    response = client.post(
        "/llm/summarize",
        json={"text": "", "model": "gpt-4o-mini"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "error"

def test_summarization_invalid_model():
    """Test summarization with invalid model."""
    text = "This is a test sentence for summarization."
    response = client.post(
        "/llm/summarize",
        json={"text": text, "model": "invalid-model"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "error"

# Multi-Step Chatbot Tests
def test_chatbot_success():
    """Test successful multi-step chatbot conversation."""
    response = client.post(
        "/llm/chatbot",
        json={
            "message": "I need help with my account",
            "provider": "gemini",
            "system_message": "You are a customer service representative.",
            "max_tokens": 150,
            "temperature": 0.7
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "clarification" in response.json()
    assert "final_response" in response.json()
    assert len(response.json()["clarification"]) > 0
    assert len(response.json()["final_response"]) > 0

def test_chatbot_empty_message():
    """Test chatbot with empty message."""
    response = client.post(
        "/llm/chatbot",
        json={
            "message": "",
            "provider": "gemini"
        }
    )
    assert response.status_code == 422  # Validation error

def test_chatbot_invalid_provider():
    """Test chatbot with invalid provider."""
    response = client.post(
        "/llm/chatbot",
        json={
            "message": "I need help with my account",
            "provider": "invalid-provider"
        }
    )
    assert response.status_code == 422  # Validation error
