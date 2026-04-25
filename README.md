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

   ## Running Tests

   To run tests manually:
   ```sh
   pytest
   # or
   python3 -m pytest
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