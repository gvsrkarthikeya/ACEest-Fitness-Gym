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

def test_home_post_and_save_progress(client):
    # Save client
    response = client.post('/', data={
        'profile': 'Muscle Gain (MG)',
        'name': 'Test User',
        'age': '25',
        'weight': '70',
        'adherence': '90',
        'save': 'Save Client'
    })
    assert response.status_code == 200
    assert b'Muscle Gain (MG)' in response.data
    assert b'Weekly Workout Chart' in response.data
    assert b'Daily Nutrition Plan' in response.data
    assert b'Estimated Calories' in response.data
    assert b'2450 kcal' in response.data
    # Save progress
    response = client.post('/save_progress', data={
        'name': 'Test User',
        'adherence': '90'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Weekly progress logged.' in response.data


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
    # Save progress for client
    client.post('/save_progress', data={
        'name': 'Client1',
        'adherence': '85'
    })
    # Check client appears in table with adherence and notes
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
    assert b'Muscle Gain (MG)' in response.data or b'Muscle Gain' in response.data
    assert b'Strong' in response.data
    assert b'80' in response.data
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

def test_duplicate_client_update(client):
    # Save client
    client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'DupClient',
        'age': '30',
        'weight': '60',
        'adherence': '80',
        'notes': 'First',
        'save': 'Save Client'
    })
    # Save again with different data (should update)
    response = client.post('/', data={
        'profile': 'Muscle Gain (MG)',
        'name': 'DupClient',
        'age': '31',
        'weight': '65',
        'adherence': '85',
        'notes': 'Updated',
        'save': 'Save Client'
    }, follow_redirects=True)
    assert b'DupClient' in response.data
    assert b'31' in response.data
    assert b'65' in response.data
    assert b'Updated' in response.data
    assert b'Muscle Gain (MG)' in response.data or b'Muscle Gain' in response.data


def test_save_progress_nonexistent_client(client):
    response = client.post('/save_progress', data={
        'name': 'NoSuchClient',
        'adherence': '50'
    }, follow_redirects=True)
    # Should still flash success, but client won't be in table
    assert b'Weekly progress logged.' in response.data
    assert b'NoSuchClient' not in response.data


def test_export_csv_no_clients(client):
    # Clear all clients to simulate empty DB
    with app.app_context():
        conn = app.config.get('TEST_DB_CONN')
        if not conn:
            import sqlite3
            conn = sqlite3.connect('aceest_fitness.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM clients')
        conn.commit()
        conn.close()
    response = client.get('/export', follow_redirects=True)
    assert b'No clients to export.' in response.data


def test_special_characters_in_name_notes(client):
    special_name = "O'Reilly & Sons"
    special_notes = "Great progress! 💪 #1"
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': special_name,
        'age': '29',
        'weight': '70',
        'adherence': '95',
        'notes': special_notes,
        'save': 'Save Client'
    }, follow_redirects=True)
    # MarkupSafe (used by Jinja2) escapes single quote as &#39;
    def markupsafe_escape(s):
        return (
            s.replace('&', '&amp;')
             .replace('<', '&lt;')
             .replace('>', '&gt;')
             .replace('"', '&quot;')
             .replace("'", '&#39;')
        )
    escaped_name = markupsafe_escape(special_name).encode()
    escaped_notes = markupsafe_escape(special_notes).encode()
    assert escaped_name in response.data
    assert escaped_notes in response.data


def test_empty_notes(client):
    response = client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'EmptyNotes',
        'age': '33',
        'weight': '60',
        'adherence': '70',
        'notes': '',
        'save': 'Save Client'
    }, follow_redirects=True)
    assert b'EmptyNotes' in response.data
    # Should not error if notes are empty


def test_adherence_edge_cases(client):
    # 0%
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'Edge0',
        'age': '20',
        'weight': '50',
        'adherence': '0',
        'save': 'Save Client'
    }, follow_redirects=True)
    assert b'Edge0' in response.data
    # 100%
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'Edge100',
        'age': '20',
        'weight': '50',
        'adherence': '100',
        'save': 'Save Client'
    }, follow_redirects=True)
    assert b'Edge100' in response.data
    # Negative
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'EdgeNeg',
        'age': '20',
        'weight': '50',
        'adherence': '-10',
        'save': 'Save Client'
    }, follow_redirects=True)
    assert b'EdgeNeg' in response.data
    # Over 100
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'EdgeOver',
        'age': '20',
        'weight': '50',
        'adherence': '150',
        'save': 'Save Client'
    }, follow_redirects=True)
    assert b'EdgeOver' in response.data


def test_save_progress_get_not_allowed(client):
    response = client.get('/save_progress', follow_redirects=True)
    # Should redirect or error (405)
    assert response.status_code in (405, 302)
