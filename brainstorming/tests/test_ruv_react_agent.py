# tests/test_ruv_react_agent.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_setup():
    """Test that the test framework is operational."""
    assert True

def test_ruv_react_endpoint():
    """Test that the RUV ReAct Decision Engine endpoint is accessible."""
    response = client.get("/agent/ruv_react_decision_engine")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "usage" in data

def test_ruv_react_query_endpoint():
    """Test that the RUV ReAct Decision Engine query endpoint is accessible."""
    test_request = {
        "query": "What is 2+2?"
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data

def test_ruv_react_financial_deductive():
    """Test the RUV ReAct Decision Engine with financial deductive reasoning."""
    test_request = {
        "query": '{"domain": "financial", "reasoningType": "deductive", "data": {"expectedReturn": 0.06, "riskLevel": "low"}}'
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should contain information about investing
    assert "invest" in data["answer"].lower() or "investment" in data["answer"].lower()

def test_ruv_react_medical_deductive():
    """Test the RUV ReAct Decision Engine with medical deductive reasoning."""
    test_request = {
        "query": '{"domain": "medical", "reasoningType": "deductive", "symptoms": ["fever", "rash"]}'
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should contain information about measles
    assert "measles" in data["answer"].lower() or "diagnosis" in data["answer"].lower()

def test_ruv_react_legal_deductive():
    """Test the RUV ReAct Decision Engine with legal deductive reasoning."""
    test_request = {
        "query": '{"domain": "legal", "reasoningType": "deductive", "caseType": "contract", "signed": false}'
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should contain information about contract validity
    assert "contract" in data["answer"].lower() and "invalid" in data["answer"].lower()

def test_ruv_react_financial_inductive():
    """Test the RUV ReAct Decision Engine with financial inductive reasoning."""
    test_request = {
        "query": '{"domain": "financial", "reasoningType": "inductive", "data": {"pastReturns": [0.05, 0.06, 0.07, 0.04, 0.05]}}'
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should contain information about estimated return
    assert "return" in data["answer"].lower() or "estimate" in data["answer"].lower()

def test_ruv_react_medical_inductive():
    """Test the RUV ReAct Decision Engine with medical inductive reasoning."""
    test_request = {
        "query": '{"domain": "medical", "reasoningType": "inductive", "symptoms": ["fever", "cough", "headache"]}'
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should contain information about flu
    assert "flu" in data["answer"].lower() or "diagnosis" in data["answer"].lower()

def test_ruv_react_legal_inductive():
    """Test the RUV ReAct Decision Engine with legal inductive reasoning."""
    test_request = {
        "query": '{"domain": "legal", "reasoningType": "inductive", "caseType": "civil"}'
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should contain information about settlement
    assert "settle" in data["answer"].lower() or "outcome" in data["answer"].lower()

def test_ruv_react_calculator_tool():
    """Test the RUV ReAct Decision Engine with the calculator tool."""
    test_request = {
        "query": "What is 123 * 456?"
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should contain the correct result
    assert "56088" in data["answer"]

def test_ruv_react_invalid_query():
    """Test the RUV ReAct Decision Engine with an invalid query."""
    test_request = {
        "invalid_key": "This is not a valid query"
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 400
    
def test_ruv_react_invalid_domain():
    """Test the RUV ReAct Decision Engine with an invalid domain."""
    test_request = {
        "query": '{"domain": "invalid_domain", "reasoningType": "deductive", "data": {}}'
    }
    response = client.post("/agent/ruv_react_decision_engine", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # The answer should indicate that the domain is not supported
    assert "domain" in data["answer"].lower() and "not supported" in data["answer"].lower()