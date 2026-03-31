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
    conn.close()


init_db()


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


@app.route('/', methods=['GET', 'POST'])
def home():
    selected = list(programs.keys())[0]
    name = ''
    age = ''
    weight = ''
    adherence = ''
    notes = ''
    calories = None
    if request.method == 'POST':
        selected = request.form.get('profile', selected)
        name = request.form.get('name', '')
        age = request.form.get('age', '')
        weight = request.form.get('weight', '')
        adherence = request.form.get('adherence', '')
        notes = request.form.get('notes', '')
        calories = calculate_calories(weight, selected)
        # Save client if requested
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
        # Reset form
        if 'reset' in request.form:
            return redirect(url_for('home'))
    # Load all clients for display
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
        clients=clients
    )


@app.route('/export')
def export_csv():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'SELECT name, age, weight, program, calories, notes FROM clients'
        )
    clients = cur.fetchall()
    conn.close()
    if not clients:
        flash("No clients to export.", "warning")
        return redirect(url_for('home'))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Age", "Weight", "Program", "Calories", "Notes"])
    for c in clients:
        writer.writerow([c[0], c[1], c[2], c[3], c[4], c[5]])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='clients.csv'
    )


@app.route('/progress_chart.png')
def progress_chart():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'SELECT client_name, MAX(adherence) FROM progress GROUP BY client_name'
    )
    rows = cur.fetchall()
    conn.close()
    fig, ax = plt.subplots(figsize=(4, 2))
    if rows:
        adherence = [float(r[1]) if r[1] else 0 for r in rows]
        names = [r[0] for r in rows]
        ax.bar(
            names, adherence, color="#d4af37"
        )
        ax.set_ylabel("Adherence %")
        ax.set_title("Client Progress")
    else:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


# Endpoint to save progress

@app.route('/save_progress', methods=['POST'])
def save_progress():
    name = request.form.get('name', '')
    adherence = request.form.get('adherence', '')
    if not name:
        flash('Client name required to save progress.', 'warning')
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
        flash(
            'Weekly progress logged.',
            'success'
        )
    except Exception as e:
        flash(
            f'Error saving progress: {e}',
            'danger'
        )
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
