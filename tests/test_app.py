def test_weight_trend_chart(client):
    # Save a client and some metrics
    client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'WeightChartUser',
        'age': '25',
        'height': '170',
        'weight': '70',
        'adherence': '80',
        'notes': 'For weight chart',
        'save': 'Save Client'
    })
    # Log two metrics
    client.post('/log_metrics', data={
        'name': 'WeightChartUser',
        'date': '2024-01-01',
        'weight': '70',
        'waist': '80',
        'bodyfat': '15'
    })
    client.post('/log_metrics', data={
        'name': 'WeightChartUser',
        'date': '2024-02-01',
        'weight': '68',
        'waist': '78',
        'bodyfat': '14'
    })
    # Request chart
    response = client.get('/weight_trend_chart.png?client=WeightChartUser')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert len(response.data) > 100

def test_bmi_info(client):
    client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'BMIUser',
        'age': '30',
        'height': '180',
        'weight': '80',
        'adherence': '90',
        'notes': 'For BMI',
        'save': 'Save Client'
    })
    response = client.get('/bmi_info?client=BMIUser')
    assert response.status_code == 200
    assert b'bmi' in response.data or b'BMI' in response.data

def test_log_workout_and_metrics(client):
    client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'LogUser',
        'age': '22',
        'height': '165',
        'weight': '60',
        'adherence': '75',
        'notes': 'For logging',
        'save': 'Save Client'
    })
    # Log workout (stub, should return not implemented)
    response = client.post('/log_workout', data={
        'name': 'LogUser',
        'date': '2024-03-01',
        'workout_type': 'Strength',
        'duration_min': '60',
        'notes': 'Test workout',
        'exercise_name': 'Bench Press',
        'sets': '3',
        'reps': '10',
        'weight': '60'
    })
    assert response.status_code == 200
    assert b'not implemented' in response.data
    # Log metrics (now implemented, should return status ok)
    response = client.post('/log_metrics', data={
        'name': 'LogUser',
        'date': '2024-03-01',
        'weight': '60',
        'waist': '80',
        'bodyfat': '15'
    })
    assert response.status_code == 200
    assert b'"status":"ok"' in response.data or b'\'status\': \'ok\'' in response.data
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
        'height': '175',
        'weight': '70',
        'target_weight': '68',
        'target_adherence': '90',
        'adherence': '90',
        'notes': 'Test notes',
        'save': 'Save Client'
    })
    assert response.status_code == 200
    assert b'Muscle Gain (MG)' in response.data
    assert b'Weekly Workout Chart' in response.data or b'Weekly Adherence' in response.data
    assert b'Daily Nutrition Plan' in response.data
    assert b'Estimated Calories' in response.data
    assert b'2450 kcal' in response.data
    assert b'175' in response.data  # height
    assert b'68' in response.data   # target_weight
    assert b'90' in response.data   # target_adherence
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
        'height': '170',
        'weight': '60',
        'target_weight': '55',
        'target_adherence': '95',
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
    # Check client appears in table with adherence and notes and new fields
    assert b'Client1' in response.data
    assert b'28' in response.data
    assert b'170' in response.data  # height
    assert b'60' in response.data
    assert b'55' in response.data   # target_weight
    assert b'95' in response.data   # target_adherence
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
    # Save two clients with progress
    client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'Client3',
        'age': '22',
        'weight': '55',
        'adherence': '75',
        'notes': 'Newbie',
        'save': 'Save Client'
    })
    client.post('/save_progress', data={
        'name': 'Client3',
        'adherence': '75'
    })
    client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'Client4',
        'age': '30',
        'weight': '60',
        'adherence': '60',
        'notes': 'Other',
        'save': 'Save Client'
    })
    client.post('/save_progress', data={
        'name': 'Client4',
        'adherence': '60'
    })
    # Per-client chart for Client3
    response = client.get('/progress_chart.png?client=Client3')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert len(response.data) > 100
    # Per-client chart for Client4
    response2 = client.get('/progress_chart.png?client=Client4')
    assert response2.status_code == 200
    assert response2.headers['Content-Type'] == 'image/png'
    assert len(response2.data) > 100
    # Global chart (all progress)
    response3 = client.get('/progress_chart.png')
    assert response3.status_code == 200
    assert response3.headers['Content-Type'] == 'image/png'
    assert len(response3.data) > 100

def test_progress_chart_content(client):
    # Save a client and progress to ensure chart is generated
    client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'ChartTest',
        'age': '23',
        'weight': '60',
        'adherence': '80',
        'notes': 'Chart test',
        'save': 'Save Client'
    })
    client.post('/save_progress', data={
        'name': 'ChartTest',
        'adherence': '80'
    })
    response = client.get('/progress_chart.png')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'
    assert len(response.data) > 100
    # Optionally, check PNG signature
    assert response.data[:8] == b'\x89PNG\r\n\x1a\n'

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
    # Should redirect to home and form fields should be empty (but client table remains)
    # Use regex to robustly check for empty value fields
    import re
    assert re.search(br'name="name"[^>]*value=""', response.data)
    assert re.search(br'name="age"[^>]*value=""', response.data)
    assert re.search(br'name="weight"[^>]*value=""', response.data)
    assert re.search(br'name="adherence"[^>]*value=""', response.data)
    assert re.search(br'name="notes"[^>]*value=""', response.data)

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


# Additional test cases for new features/UI
def test_load_client_by_name(client):
    # Save two clients
    client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'LoadMe',
        'age': '21',
        'weight': '55',
        'adherence': '80',
        'notes': 'To load',
        'save': 'Save Client'
    })
    client.post('/', data={
        'profile': 'Fat Loss (FL)',
        'name': 'Other',
        'age': '22',
        'weight': '60',
        'adherence': '70',
        'notes': 'Other',
        'save': 'Save Client'
    })
    # Load by name (GET param)
    response = client.get('/?load_name=LoadMe')
    assert b'LoadMe' in response.data
    assert b'To load' in response.data
    assert b'Beginner (BG)' in response.data

def test_summary_profile_rendering(client):
    # Save a client and check for summary/profile area
    client.post('/', data={
        'profile': 'Muscle Gain (MG)',
        'name': 'SummaryUser',
        'age': '27',
        'height': '180',
        'weight': '75',
        'target_weight': '70',
        'target_adherence': '92',
        'adherence': '88',
        'notes': 'Summary test',
        'save': 'Save Client'
    }, follow_redirects=True)
    # Now load by name to trigger summary
    response = client.get('/?load_name=SummaryUser')
    # The summary/profile area should be present and include new fields
    assert b'Client Profile' in response.data
    assert b'SummaryUser' in response.data
    assert b'Summary test' in response.data
    assert b'180' in response.data  # height
    assert b'70' in response.data   # target_weight
    assert b'92' in response.data   # target_adherence

def test_flash_message_invalid_input(client):
    # Submit with missing name
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': '',
        'age': '20',
        'weight': '50',
        'adherence': '80',
        'save': 'Save Client'
    }, follow_redirects=True)
    # Should flash a message about missing name
    assert b'Please fill client name and program.' in response.data

def test_flash_message_invalid_age(client):
    # Submit with invalid age (should still save, as app does not validate age type)
    response = client.post('/', data={
        'profile': 'Beginner (BG)',
        'name': 'InvalidAge',
        'age': 'abc',
        'weight': '50',
        'adherence': '80',
        'save': 'Save Client'
    }, follow_redirects=True)
    # Should still show success message (no strict validation in app)
    assert b'Client InvalidAge saved successfully.' in response.data
