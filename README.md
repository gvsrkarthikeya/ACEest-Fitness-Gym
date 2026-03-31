# ACEest Fitness & Gym

A Flask web app for ACEest Fitness & Gym, now supporting personalized client profiles and calorie estimation. Showcases DevOps best practices: version control, automated testing, Docker containerization, and CI/CD pipelines with GitHub Actions and Jenkins.

## Project Structure


   - `app.py`: Main application file (Flask web app)
   - `program_data.py`: Program logic and calorie factors
   - `requirements.txt`: Python dependencies
   - `tests/`: Unit tests
   - `.gitignore`: Ignore unnecessary files
   - `Dockerfile`: Containerization
   - `.github/workflows/main.yml`: CI/CD pipeline
   - `Jenkinsfile`: Jenkins pipeline definition
   - `templates/`: HTML templates for Flask

## Local Setup Instructions

1. Clone the repository:

   # ACEest Fitness & Gym

   This is a modular Flask web application for ACEest Fitness & Gym, demonstrating DevOps best practices:
   - Version control with Git
   - Automated testing with Pytest
   - Docker containerization
   - CI/CD pipelines using GitHub Actions and Jenkins

   ## Project Structure

   - `app.py`: Main Flask application
   - `program_data.py`: Supporting module for app logic
   - `requirements.txt`: Python dependencies
   - `tests/`: Unit tests (Pytest)
   - `Dockerfile`: Containerization instructions
   - `.github/workflows/main.yml`: GitHub Actions CI/CD pipeline
   - `Jenkinsfile`: Jenkins pipeline definition
   - `templates/`: HTML templates for Flask


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
3. **Run the app locally:**
   ```sh
   python app.py
   ```
4. **Run with Docker:**
   ```sh
   docker build -t aceest-fitness-gym .
   docker run -p 5000:5000 aceest-fitness-gym
   ```


## Features (v1.1)

- Personalized client profile: Name, Age, Weight, Weekly Adherence
- Program selection: Fat Loss, Muscle Gain, Beginner
- Automatic calorie estimation based on weight and program
- Weekly workout and nutrition plans


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

   ## Versioning

   The app evolves from v1.0 to v3.2.4. Each version's code is placed in `app.py` as the project progresses.
