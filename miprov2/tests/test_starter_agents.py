from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_quote_agent():
    """Test quote agent response format"""
    response = client.get("/agent/quote")
    assert response.status_code == 200
    result = response.json()
    assert "agent" in result and result["agent"] == "quote"
    assert "result" in result and "quote" in result["result"]
    assert isinstance(result["result"]["quote"], str)
    assert len(result["result"]["quote"]) > 0
