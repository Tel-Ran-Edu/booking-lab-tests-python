// A sample Jenkins pipeline: the same steps as .github/workflows/tests.yml.
//
// The agent needs: Docker with Compose, Python 3.12+, Node.js 22+ (for the Allure report),
// Google Chrome (for Selenium) and the system libraries Playwright's Chromium needs
// (once, as root: `python -m playwright install-deps chromium`). Plugins: Pipeline.
// The report is archived as allure-report/index.html: open it from the build page.
pipeline {
  agent any
  options {
    timeout(time: 20, unit: 'MINUTES')
    disableConcurrentBuilds() // one local copy of BooKing Lab per agent at a time
  }
  environment {
    API_URL = 'http://localhost:8000'
    WEB_URL = 'http://localhost:5173'
    COHORT = 'DEMO'
    ALLURE_VERSION = '3.33.0'
  }
  stages {
    stage('Start BooKing Lab') {
      steps {
        sh 'docker compose up -d --wait'
      }
    }
    stage('Install') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
          python -m playwright install chromium
        '''
      }
    }
    stage('Test') {
      steps {
        // a failed test marks the build red but lets the report stage run
        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
          sh '. .venv/bin/activate && pytest'
        }
      }
    }
    stage('Report') {
      steps {
        sh 'npx --yes allure@$ALLURE_VERSION generate allure-results'
        sh 'node scripts/report-summary.mjs'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'allure-report/index.html', allowEmptyArchive: true
      sh 'docker compose down -v'
    }
  }
}
