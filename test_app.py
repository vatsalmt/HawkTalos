# test_app.py
import pytest
from app import app  # your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_search_endpoint(client):
    response = client.post('/search', json={"query": "test"})
    assert response.status_code == 200
    data = response.get_json()
    assert "results" in data