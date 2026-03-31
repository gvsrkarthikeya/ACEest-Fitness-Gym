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
    response = client.post('/', data={
        'profile': 'Muscle Gain (MG)',
        'name': 'Test User',
        'age': '25',
        'weight': '70',
        'adherence': '90'
    })
    assert response.status_code == 200
    assert b'Muscle Gain (MG)' in response.data
    assert b'Weekly Workout Chart' in response.data
    assert b'Daily Nutrition Plan' in response.data
    # Check for calories calculation (70 * 35 = 2450)
    assert b'Estimated Calories' in response.data
    assert b'2450 kcal' in response.data


def test_all_programs_calorie_calculation(client):
    # Fat Loss (FL)
    response = client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'A',
        'age': '30',
        'weight': '60',
        'adherence': '80'
    })
    assert b'Fat Loss (FL)' in response.data
    assert b'Estimated Calories' in response.data
    assert b'1320 kcal' in response.data  # 60*22

    # Beginner (BG)
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'B',
        'age': '20',
        'weight': '50',
        'adherence': '70'
    })
    assert b'Beginner (BG)' in response.data
    assert b'Estimated Calories' in response.data
    assert b'1300 kcal' in response.data  # 50*26


def test_missing_weight(client):
    response = client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'NoWeight',
        'age': '30',
        'weight': '',
        'adherence': '80'
    })
    assert b'Estimated Calories' not in response.data


def test_invalid_weight(client):
    response = client.post('/', data={
        'profile': 'Muscle Gain (MG)',
        'name': 'InvalidWeight',
        'age': '25',
        'weight': 'abc',
        'adherence': '90'
    })
    assert b'Estimated Calories' not in response.data


def test_empty_form(client):
    response = client.post('/', data={})
    assert response.status_code == 200
    # Should not crash, should show default program
    assert b'ACEest FUNCTIONAL FITNESS' in response.data


def test_save_client_and_list(client):
    # Save a client
    response = client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'Client1',
        'age': '28',
        'weight': '60',
        'adherence': '85',
        'notes': 'Good progress',
        'save': 'Save Client'
    }, follow_redirects=True)
    assert b'Client Client1 saved successfully.' in response.data
    # Check client appears in table
    assert b'Client1' in response.data
    assert b'28' in response.data
    assert b'60' in response.data
    assert b'85' in response.data
    assert b'Good progress' in response.data

def test_export_csv(client):
    # Save a client first
    client.post('/', data={
        'profile': 'Muscle Gain (MG)',
        'name': 'Client2',
        'age': '30',
        'weight': '80',
        'adherence': '90',
        'notes': 'Strong',
        'save': 'Save Client'
    })
    # Export CSV
    response = client.get('/export')
    assert response.status_code == 200
    assert b'Client2' in response.data
    assert b'Muscle Gain (MG)' in response.data
    assert b'Strong' in response.data
    assert response.headers['Content-Type'].startswith('text/csv')

def test_progress_chart(client):
    # Save a client to have chart data
    client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'Client3',
        'age': '22',
        'weight': '55',
        'adherence': '75',
        'notes': 'Newbie',
        'save': 'Save Client'
    })
    response = client.get('/progress_chart.png')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert len(response.data) > 100  # Should return image bytes

def test_reset_form(client):
    # Fill and reset
    response = client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'Client4',
        'age': '40',
        'weight': '70',
        'adherence': '60',
        'notes': 'To reset',
        'reset': 'Reset'
    }, follow_redirects=True)
    # Should redirect to home and not show client4 in table
    assert b'Client4' not in response.data
