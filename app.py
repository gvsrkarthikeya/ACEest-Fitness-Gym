import io
import csv
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from flask import (
    Flask, render_template, request, redirect, url_for, send_file, flash
)
from program_data import programs
from datetime import datetime
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = 'aceest-secret-key'

DB_NAME = 'aceest_fitness.db'


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            weight REAL,
            program TEXT,
            calories INTEGER,
            notes TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            week TEXT,
            adherence INTEGER
        )
    ''')
    conn.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    selected = list(programs.keys())[0]
    name = ''
    age = ''
    weight = ''
    adherence = ''
    notes = ''
    calories = None
    summary = None
    chart_client = ''
    load_name = request.args.get('load_name', '').strip()
    if load_name:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM clients WHERE name=?', (load_name,))
        row = cur.fetchone()
        if row:
            _, name, age, weight, selected, calories, notes = row
            cur.execute('SELECT MAX(adherence) FROM'
                        ' progress WHERE client_name=?', (name,))
            adherence_row = cur.fetchone()
            adherence = (
                adherence_row[0] if adherence_row and
                adherence_row[0] is not None else ''
                )
            summary = f"""
CLIENT PROFILE
--------------
Name     : {name}
Age      : {age}
Weight   : {weight} kg
Program  : {selected}
Adherence: {adherence}
Notes    : {notes}
"""
            # Save client if requested
        else:
            flash('Client not found.', 'warning')
        conn.close()
    elif request.method == 'POST':
        selected = request.form.get('profile', selected)
        name = request.form.get('name', '')
        age = request.form.get('age', '')
        weight = request.form.get('weight', '')
        adherence = request.form.get('adherence', '')
        notes = request.form.get('notes', '')
        calories = calculate_calories(weight, selected)
        if 'save' in request.form:
            if name and selected:
                try:
                    conn = get_db()
                    cur = conn.cursor()
                    cur.execute('''
                        INSERT OR REPLACE INTO clients
                        (name, age, weight, program, calories, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (name, age, weight, selected, calories, notes))
                    conn.commit()
                    conn.close()
                    flash(
                        f"Client {name} saved successfully.",
                        "success"
                    )
                except Exception as e:
                    flash(
                        f"DB Error: {e}",
                        "danger"
                    )
            else:
                flash(
                    "Please fill client name and program.",
                    "warning"
                )
    if request.method == 'POST':
        selected = request.form.get('profile', selected)
        name = request.form.get('name', '')
        age = request.form.get('age', '')
        weight = request.form.get('weight', '')
        adherence = request.form.get('adherence', '')
        notes = request.form.get('notes', '')
        calories = calculate_calories(weight, selected)
        if 'save' in request.form:
            if name and selected:
                try:
                    conn = get_db()
                    cur = conn.cursor()
                    cur.execute('''
                        INSERT OR REPLACE INTO clients
                        (name, age, weight, program, calories, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (name, age, weight, selected, calories, notes))
                    conn.commit()
                    conn.close()
                    flash(
                        f"Client {name} saved successfully.",
                        "success"
                    )
                except Exception as e:
                    flash(
                        f"DB Error: {e}",
                        "danger"
                    )
            else:
                flash(
                    "Please fill client name and program.",
                    "warning"
                )
        if 'reset' in request.form:
            # Reset all form fields to empty strings
            name = ''
            age = ''
            weight = ''
            adherence = ''
            notes = ''
            calories = None
            # Continue to render the template with empty fields
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT clients.name, clients.age,
        clients.weight, clients.program,
        p.adherence, clients.notes
        FROM clients
        LEFT JOIN (
            SELECT client_name, MAX(adherence) as
            adherence FROM progress GROUP BY client_name
        ) p ON clients.name = p.client_name
    ''')
    clients = cur.fetchall()
    conn.close()
    data = programs[selected]
    return render_template(
        'home.html',
        programs=programs,
        selected=selected,
        workout=data["workout"],
        diet=data["diet"],
        color=data["color"],
        name=name,
        age=age,
        weight=weight,
        adherence=adherence,
        notes=notes,
        calories=calories,
        clients=clients,
        summary=summary,
        chart_client=chart_client or name
    )


@app.route('/progress_chart.png')
def progress_chart():
    client_name = request.args.get('client')
    conn = get_db()
    cur = conn.cursor()
    if client_name:
        cur.execute('SELECT week, adherence FROM progress '
                    'WHERE client_name=? ORDER BY week', (client_name,))
    else:
        cur.execute('SELECT week, adherence FROM progress ORDER BY week')
    data = cur.fetchall()
    conn.close()
    weeks = [row['week'] for row in data]
    adherence = [row['adherence'] for row in data]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(weeks, adherence, marker='o', color='#d4af37')
    title = f"Weekly Adherence{' – ' + client_name if client_name else ''}"
    ax.set_title(title)
    ax.set_xlabel('Week')
    ax.set_ylabel('Adherence (%)')
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/save_progress', methods=['POST'])
def save_progress():
    name = request.form.get('name', '')
    adherence = request.form.get('adherence', '')
    if not name or not adherence:
        flash('Name and adherence required to save progress.', 'warning')
        return redirect(url_for('home'))
    week = datetime.now().strftime('Week %U - %Y')
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO progress (client_name, week, adherence)
            VALUES (?, ?, ?)
        ''', (name, week, adherence))
        conn.commit()
        conn.close()
        flash('Weekly progress logged.', 'success')
    except Exception as e:
        flash(f'Error saving progress: {e}', 'danger')
    return redirect(url_for('home'))


@app.route('/export')
def export_csv():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clients')
    rows = cur.fetchall()
    if not rows:
        flash('No clients to export.', 'warning')
        conn.close()
        return redirect(url_for('home'))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(rows[0].keys())
    for row in rows:
        writer.writerow([row[k] for k in row.keys()])
    conn.close()
    output.seek(0)
    return send_file(
        io.BytesIO(output.read().encode()), mimetype='text/csv',
        as_attachment=True, download_name='clients.csv')


def calculate_calories(weight, program):
    try:
        w = float(weight)
        if w > 0:
            factor = (
                programs[program].get("factor") or
                programs[program].get("calorie_factor")
            )
            return int(w * factor)
    except Exception:
        return None


# Ensure DB tables exist before running app or tests
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
