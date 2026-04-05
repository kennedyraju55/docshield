"""Tests for Flask app endpoints."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"DocShield" in r.data


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert "status" in data
    assert "ollama" in data


def test_analyze_no_input(client):
    r = client.post("/analyze", json={})
    assert r.status_code == 400


def test_analyze_text_input(client):
    """Test that text input returns SSE stream."""
    r = client.post("/analyze", json={"text": "Patient takes warfarin 5mg daily."})
    assert r.status_code == 200
    assert r.content_type.startswith("text/event-stream")
