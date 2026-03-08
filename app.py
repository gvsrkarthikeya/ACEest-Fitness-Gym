from flask import Flask, render_template, request
from program_data import programs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    selected = list(programs.keys())[0]
    if request.method == 'POST':
        selected = request.form.get('profile', selected)
    data = programs[selected]
    return render_template(
        'home.html',
        programs=programs,
        selected=selected,
        workout=data["workout"],
        diet=data["diet"],
        color=data["color"]
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)