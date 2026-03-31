
import io
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from program_data import programs



app = Flask(__name__)
app.secret_key = 'aceest-secret-key'

# In-memory client list
clients = []



def calculate_calories(weight, program):
    try:
        w = float(weight)
        if w > 0:
            return int(w * programs[program]["calorie_factor"])
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
                clients.append((name, age, weight, selected, adherence, notes))
                flash(f"Client {name} saved successfully.", "success")
            else:
                flash("Please fill client name and program.", "warning")
        # Reset form
        if 'reset' in request.form:
            return redirect(url_for('home'))
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
    if not clients:
        flash("No clients to export.", "warning")
        return redirect(url_for('home'))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Age", "Weight", "Program", "Adherence", "Notes"])
    writer.writerows(clients)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='clients.csv'
    )



@app.route('/progress_chart.png')
def progress_chart():
    fig, ax = plt.subplots(figsize=(4, 2))
    if clients:
        adherence = [float(c[4]) if c[4] else 0 for c in clients]
        names = [c[0] for c in clients]
        ax.bar(names, adherence, color="#d4af37")
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
