# ACEest Fitness & Gym

This is a modular Flask web application for ACEest Fitness & Gym, demonstrating DevOps best practices:
- Version control with Git
- Automated testing with Pytest
- Docker containerization
- CI/CD pipelines using GitHub Actions and Jenkins

## Features

* Persistent client and progress management using SQLite database
* Save, load, and update client profiles (name, age, weight, program, notes)
* Load client by name and view full client summary/profile
* Track and save weekly adherence progress for each client
* View all clients and their latest adherence in a table
* Export all client data as CSV
* Visualize client adherence with a progress chart (from DB)
* Add and display coach notes for each client
* Reset form to clear all input fields (robust: fields always reset to empty, even if previously set to None or missing)
* Modern web-based UI (Flask, HTML/CSS)
* All features fully tested and documented

## v2.2.1 Highlights

- Robust reset form: All input fields are now guaranteed to be cleared after reset, regardless of previous state or missing values.
- HTML form rendering improved: Uses `{{ variable or '' }}` for all input fields to ensure empty fields display correctly.

## Project Structure

- `app.py`: Main Flask application
- `program_data.py`: Supporting module for app logic
- `requirements.txt`: Python dependencies
- `tests/`: Unit tests (Pytest)
- `Dockerfile`: Containerization instructions
- `.github/workflows/main.yml`: GitHub Actions CI/CD pipeline
- `Jenkinsfile`: Jenkins pipeline definition
- `templates/`: HTML templates for Flask
- `.gitignore`: Ignore unnecessary files


## Local Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd ACEest-Fitness-Gym
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   (Installs Flask, matplotlib, pytest, and more)
3. **Run the app locally:**
   ```sh
   python app.py
   ```
4. **Run with Docker:**
   ```sh
   docker build -t aceest-fitness-gym .
   docker run -p 5000:5000 aceest-fitness-gym
   ```


Test coverage includes:
- Form input and calorie calculation
- Client save and list
- CSV export
- Progress chart endpoint
- Reset form (robust field clearing, regex-based test)
   - Notes features


## Running Tests & Coverage

To run tests manually:
```sh
pytest
# or
python3 -m pytest
```

To check test coverage:
```sh
pytest --cov=.
# or
python3 -m pytest --cov=.
```
For an HTML coverage report:
```sh
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in your browser
```


## CI/CD Overview

- **GitHub Actions:**
   - Triggers on push and pull requests
   - Installs dependencies, lints, runs tests, and builds Docker image
- **Jenkins:**
   - Uses the Jenkinsfile for pipeline definition
   - Stages: install dependencies, lint, test, build Docker image
   - Set up a Jenkins Pipeline job and point it to this repository

   The app evolves from v1.0 to v3.2.4. Each version's code is placed in `app.py` as the project progresses.
