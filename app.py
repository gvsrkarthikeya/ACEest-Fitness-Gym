from flask import Flask, render_template, request
from program_data import programs

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    selected = list(programs.keys())[0]
    name = ''
    age = ''
    weight = ''
    adherence = ''
    calories = None
    if request.method == 'POST':
        selected = request.form.get('profile', selected)
        name = request.form.get('name', '')
        age = request.form.get('age', '')
        weight = request.form.get('weight', '')
        adherence = request.form.get('adherence', '')
        # Calculate calories if weight is provided
        try:
            w = float(weight)
            if w > 0:
                calories = int(w * programs[selected]["calorie_factor"])
        except Exception:
            calories = None
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
        calories=calories
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
