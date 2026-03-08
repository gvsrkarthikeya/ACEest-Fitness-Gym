import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'ACEest FUNCTIONAL FITNESS' in response.data

def test_home_post(client):
    response = client.post('/', data={'profile': 'Muscle Gain (MG)'})
    assert response.status_code == 200
    assert b'Muscle Gain (MG)' in response.data
    assert b'Weekly Workout Chart' in response.data
    assert b'Daily Nutrition Plan' in response.data
