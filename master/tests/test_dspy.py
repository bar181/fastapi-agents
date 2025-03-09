# master/tests/test_dspy.py (Corrected)
import pytest
from fastapi.testclient import TestClient
from app.main import app
from agents.dspy.dspy_classifier import ClassifierInput, ClassifierOutput

client = TestClient(app)

def test_dspy_classifier_greeting_question():
    input_data = ClassifierInput(input_text="Hello, how are you?")
    response = client.post("/dspy/classifier", json=input_data.model_dump())  # Use model_dump()
    assert response.status_code == 200
    assert response.json() == {"classification": "Greeting/Question", "confidence": 0.67}

def test_dspy_classifier_greeting():
    input_data = ClassifierInput(input_text="Hi there!")
    response = client.post("/dspy/classifier", json=input_data.model_dump())  # Use model_dump()
    assert response.status_code == 200
    assert response.json()["classification"] == "Greeting"
    assert response.json()["confidence"] >= 0.33

def test_dspy_classifier_question():
    input_data = ClassifierInput(input_text="What is the time?")
    response = client.post("/dspy/classifier", json=input_data.model_dump())  # Use model_dump()
    assert response.status_code == 200
    assert response.json()["classification"] == "Question"
    assert response.json()["confidence"] >= 0.33

def test_dspy_classifier_command():
    input_data = ClassifierInput(input_text="Run the script")
    response = client.post("/dspy/classifier", json=input_data.model_dump())  # Use model_dump()
    assert response.status_code == 200
    assert response.json()["classification"] == "Command"
    assert response.json()["confidence"] >= 0.33

def test_dspy_classifier_statement():
    input_data = ClassifierInput(input_text="This is a statement.")
    response = client.post("/dspy/classifier", json=input_data.model_dump())  # Use model_dump()
    assert response.status_code == 200
    assert response.json()["classification"] == "Statement"
    assert response.json()["confidence"] == 0.0

def test_dspy_classifier_empty():
    input_data = ClassifierInput(input_text="")
    response = client.post("/dspy/classifier", json=input_data.model_dump())  # Use model_dump()
    assert response.status_code == 400