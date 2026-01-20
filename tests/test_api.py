"""
API endpoint tests
"""

from fastapi.testclient import TestClient
from montecarlo_pi.api.main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint returns 200 and correct status"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_check_response_format():
    """Test health endpoint returns valid JSON"""
    response = client.get("/health")
    
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "status" in data