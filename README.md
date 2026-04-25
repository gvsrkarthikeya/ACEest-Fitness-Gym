
# ACEest Fitness & Gym

## Version 1.1.2

### New in 1.1.2
- Save and manage multiple client profiles
- Export all client data as CSV
- Visualize client adherence with a progress chart
- Add and display coach notes for each client
- Reset form to clear input fields
- All features fully tested and documented



A Flask web app for ACEest Fitness & Gym, now supporting:
- Personalized client profiles
- Calorie estimation
- Client list management (save multiple clients)
- Export client data as CSV
- Progress chart (adherence %)
- Coach notes for each client

Showcases DevOps best practices: version control, automated testing, Docker containerization, and CI/CD pipelines with GitHub Actions and Jenkins.

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
   (Installs Flask, matplotlib, pytest, and more)

3. **Run the app locally:**
   ```sh
   python app.py
   ```

4. **Run with Docker:**
   ```sh
   docker build -t aceest-fitness-gym .
   docker run -p 5000:5000 aceest-fitness-gym

   ## Features (v1.1.2)

   - Add and save multiple client profiles (name, age, weight, program, adherence, notes)
   - Calorie calculation based on program and weight
   - View all clients in a table
   - Export all client data as CSV
   - Visualize client adherence with a progress chart
   - Add and display coach notes for each client
   - Reset form to clear input fields

   ## Testing

   Run all tests with:
   ```sh
   pytest
   ```

   Test coverage includes:
   - Form input and calorie calculation
   - Client save and list
   - CSV export
   - Progress chart endpoint
   - Reset and notes features
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

## Running Jenkins Locally on macOS (Homebrew)

You can install and manage Jenkins using Homebrew on macOS:

1. **Install the latest LTS version:**
   ```sh
   brew install jenkins-lts
   ```

2. **Start the Jenkins service:**
   ```sh
   brew services start jenkins-lts
   ```

3. **Restart the Jenkins service:**
   ```sh
   brew services restart jenkins-lts
   ```

4. **Update Jenkins to the latest version:**
   ```sh
   brew upgrade jenkins-lts
   ```

Jenkins will be available at [http://localhost:8080](http://localhost:8080)

**Note:** The first time you start Jenkins, it will display an initial admin password in the terminal. Use this to unlock Jenkins in your browser.


Test coverage includes:
- Progress chart endpoint
- Weight trend chart endpoint
- BMI info endpoint
- Client save, update, and list (with new fields: height, target_weight, target_adherence, membership_status, membership_end)
- Membership status and end date logic and UI
- User authentication (users table, login, roles)
- AI program generator (per-client, by experience level)
- PDF export for client report
- Workout, exercise, and metrics logging (CRUD, stubs)

## CI/CD Overview

- **GitHub Actions:**
   - Triggers on push and pull requests
   - Installs dependencies, lints, runs tests, and builds Docker image
- **Jenkins:**
   - Uses the Jenkinsfile for pipeline definition
   - Stages: install dependencies, lint, test, build Docker image
   - Set up a Jenkins Pipeline job and point it to this repository
   - Create credentials for Docker Hub and Jenkins will use those credentials to login and push the image

   The app evolves from v1.0 to v3.2.4. Each version's code is placed in `app.py` as the project progresses.

## SonarQube Code Quality and Coverage Analysis Local Setup:

1. **Install SonarQube and SonarScanner:**
   - Download SonarQube: https://www.sonarqube.org/downloads/
   - Download SonarScanner: https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/

2. **Start SonarQube server:**
    - In the SonarQube `bin` directory:
       - **On macOS/Linux:**
          ```sh
          ./sonar.sh start
          ```
       - **On Windows:**
          ```bat
          StartSonar.bat
          ```
    - Open [http://localhost:9000](http://localhost:9000) in your browser (default login: admin/admin).

3. **Configure SonarScanner:**
   - Add SonarScanner’s `bin` directory to your `PATH`.
   - In SonarQube UI, go to **My Account > Security > Generate Tokens** and create a token.
   - Update `sonar-project.properties` with your token.

4. **Run analysis:**
   - Generate coverage report:
     ```sh
     pytest --cov=. --cov-report=xml
     ```
   - Run SonarScanner:
     ```sh
     sonar-scanner
     ```

5. **View results:**
   - Go to [http://localhost:9000](http://localhost:9000) and view your project dashboard.