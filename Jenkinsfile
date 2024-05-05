// TODO: Integrate DVC for data versioning
// TODO: Use Docker here
pipeline {
    agent any
    environment {
        PROJECT_NAME = 'mlops_image_classifier'
        CONDA_HOME = '/home/ubuntu/anaconda3'
    }
    stages {
        stage('Setup Environment') {
            steps {
                // Assuming you've set up Miniconda or similar in your Jenkins environment
                // every sh command is a new shell, so we need to source the conda.sh script every time and in a single shell
                sh '''
                #!/bin/bash
                source "${CONDA_HOME}/etc/profile.d/conda.sh"
                make create_environment
                conda activate "${PROJECT_NAME}" 
                '''
            }
        }
        stage('Run Make Commands') {
            steps {
                // Example of running a make command
                sh '''
                #!/bin/bash 
                source "${CONDA_HOME}/etc/profile.d/conda.sh"
                conda activate "${PROJECT_NAME}"
                make test_environment
                '''
            }
        }
    }
    post {
        always {
            // Clean up or additional steps
            sh '''
            #!/bin/bash 
            make clean
            '''
        }
    }
}
