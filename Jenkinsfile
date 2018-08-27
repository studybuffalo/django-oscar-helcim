pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Setup virtual environment'
        script {
          sh 'pipenv install --dev'
        }

      }
    }
    stage('Test') {
      steps {
        echo 'Running unit tests'
        script {
          sh 'pipenv run pytest'
        }

      }
    }
    stage('Reporting') {
      steps {
        echo 'Generating coverage report'
      }
    }
  }
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }
}