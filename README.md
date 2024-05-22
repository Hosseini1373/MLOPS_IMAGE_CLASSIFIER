MLOPS_IMAGE_CLASSIFIER
==============================

MLOPS Class Project

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── Airflow            
    ├── Back-end           <- Flask server and docker file
    ├── Dockercompose_GCS  <- Dockercompose from Google cloud with Watchtower 
    ├── Front-end          <- Front-end and docker file 
    ├── Reversproxy        <- nginx Reverse proxy configuration for GCS
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   ├── config.py      <- Training parameters, directory paths
    │   │
    │   ├── data           <- Scripts to download, preprocess data for training
    │   │   │
    │   │   ├── preprocess.py 
    │   │   ├── download_dataset.bash  
    │   │   └── PetImages
    │   │
    │   │
    │   ├── models         <- Scripts to train model, bento service definition, bash file for airlflow pipeline
    │   │   │                
    │   │   ├── MobileNetv3.py <- model definition
    │   │   ├── training.py 
    │   │   ├── create_contrainer_airflow.bash
    │   │   ├── bentofile.yaml <- yaml file to build a bento
    │   │   ├── checkpoints   <- current modle checkpoint is stored in here
    │   │   └── service.py


--------




# Aiflow

### Docker setup
Install docker-compose:
`sudo apt update`
`sudo apt install docker-compose`


Starting the airflow:
`sudo docker compose up`

Access the Airflow UI:
http://[INTERNAL-VM-IP]:8081

Remember to set the necessary variables in Airflow's UI under "Admin" -> "Variables" for database_conn_id, ssh_conn_id, and model_serving_api_url.

### Or not use the docker and install directly on a vm:
`sudo apt update`
`sudo apt install postgresql postgresql-contrib`

Switch to the PostgreSQL user
`sudo -u postgres psql`

Create the Airflow database and user
`CREATE DATABASE airflow;`
`CREATE USER airflow WITH ENCRYPTED PASSWORD 'airflow';`
`GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;`
`\q`  # Exit the PostgreSQL prompt



#### Environment Variables:
```bash
export AIRFLOW_HOME=~/airflow
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@localhost/airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__WEBSERVER__WEB_SERVER_WORKER_TIMEOUT=160
export AIRFLOW__WEBSERVER__WORKER_CLASS=sync
```


configuration of the airflow:
`airflow config list`


Initialize the db:
`airflow db init` or `airflow db migrate`
`airflow users create --username airflow --password airflow --firstname airflow --lastname airflow --role Admin --email airflow@airflow.com`


psql -h localhost -p 5432 -U airflow -d postgres

Running the server:
`airflow scheduler`
`airflow webserver --port 8081 -w 20`

for more information on how to we can create systemd service from airflow:
[Link to Another README](./Airflow/README.md)

The corresponding Airflow DAG is inside `airflow-dag.py`

Create the conda Environemnt
```bash
conda create --name mlops_image_classifier python=3.11.7
conda activate mlops_image_classifier
pip install -r requirements.txt
```


Port Forwarding for the Airflow UI:
`ssh -L 8081:localhost:8081 ubuntu@[INTERNAL-VM-IP]`



# Jenkins Setup and Configuration

## Install Java
First, update your package list and install Java:
```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version

## Install Jenkins

wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins

#Initial Setup
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins

#Start Jenkins and enable it to run at boot:
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins

```

Configure Jenkins

Update Jenkins global settings to use /bin/bash as the shell executable in the system configuration under Manage Jenkins > Configure System.
Security: Admin User

Create an admin user and configure authentication settings securely. Avoid placing raw credentials in your documentation:
```bash 
    User: <jenkins_user>
    Password: <jenkins_password>
    Authentication Token: <authentication_token>
```
## GitHub Secrets

Configure your GitHub secrets for Jenkins integration:

    ```bash 
    JENKINS_URL: http://<jenkins_server_ip>:8080
    JENKINS_USER: <jenkins_user>
    JENKINS_TOKEN: <jenkins_api_token> 
    ```

## Install Conda in VM

To manage Python versions and packages, install Anaconda:

`curl -O https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh`
`bash ~/Anaconda3-2024.02-1-Linux-x86_64.sh`

Activate the base environment:

`source /home/ubuntu/anaconda3/bin/activate`

## Jenkins Job API Call

Trigger a Jenkins job via API:

`curl "http://<jenkins_server_ip>:8080/job/<job_name>/build?token=<jenkins_api_token>"`

Access Jenkins Environment from Ubuntu Terminal

To work with Jenkins managed environments:

`conda activate /var/lib/jenkins/.conda/envs/<env_name>`

Ensure to replace placeholders with your actual configuration details and credentials. Keep sensitive information such as passwords and tokens secure and out of public documents.



## Achnowledgements
<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
