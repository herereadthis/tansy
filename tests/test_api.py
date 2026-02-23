"""
API endpoint tests
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from montecarlo_pi.api.main import app
from montecarlo_pi.exceptions import SimulationError

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


def test_simulation_error_handler():
    """Test that SimulationError returns valid JSON."""
    with patch(
        "montecarlo_pi.api.routers.simulation.run_simulation",
        side_effect=SimulationError("test error message")
    ):
        response = client.get("/simulate/pi")

    assert response.status_code == 500
    assert response.json() == {
        "error": "Simulation failed",
        "detail": "test error message"
    }
