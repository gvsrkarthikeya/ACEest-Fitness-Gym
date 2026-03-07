# ACEest Fitness & Gym

A Flask web app for ACEest Fitness & Gym, showcasing DevOps best practices: version control, automated testing, Docker containerization, and CI/CD pipelines with GitHub Actions and Jenkins.

## Project Structure

- `app.py`: Main application file (will be updated for each version)
- `requirements.txt`: Python dependencies
- `tests/`: Unit tests
- `.gitignore`: Ignore unnecessary files
- `Dockerfile`: Containerization
- `.github/workflows/main.yml`: CI/CD pipeline
- `Jenkinsfile`: Jenkins pipeline definition

## Local Setup Instructions

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd ACEest-Fitness-Gym
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the app:
   ```sh
   python app.py
   ```
   Or, for Docker:
   ```sh
   docker build -t aceest-fitness-gym .
   docker run -p 5000:5000 aceest-fitness-gym
   ```

## How to Run Tests Manually

Run tests with:
```sh
pytest
# or
python3 -m pytest
```

## Overview of Jenkins Integration

- Jenkins is used for automated CI/CD outside GitHub Actions.
- The Jenkinsfile defines the pipeline: checkout, install dependencies, run tests, build Docker image.
- Jenkins pulls the latest code from GitHub, runs the pipeline, and reports build/test status.
- To use Jenkins:
  1. Set up Jenkins server (locally or cloud).
  2. Create a Pipeline job and point it to this repository.
  3. Jenkins will automatically use the Jenkinsfile for builds.

## CI/CD

- GitHub Actions: Automated build, test, and Docker image creation on push/pull request.
- Jenkins: Pulls latest code, builds, and runs tests in a controlled environment.

## Versions

The app evolves from v1.0 to v3.2.4. Each version's code will be adapted to Flask and placed in `app.py`.
