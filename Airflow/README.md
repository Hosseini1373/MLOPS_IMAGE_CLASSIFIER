## Airflow System service:


To run Airflow as a systemd service, you'll need to create systemd unit files for both the Airflow webserver and the scheduler. This allows you to manage your Airflow services with systemd commands, enabling them to start automatically on system boot, and providing better integration with the system’s logging and maintenance capabilities.

Here’s how you can create systemd services for Airflow:

### 1. Create Systemd Unit File for the Airflow Webserver

Create a file named `airflow-webserver.service` in the `/etc/systemd/system/` directory:

```bash
sudo nano /etc/systemd/system/airflow-webserver.service
```

Add the following content:

```ini
[Unit]
Description=Airflow webserver daemon
After=network.target postgresql.service
Wants=network.target postgresql.service

[Service]
EnvironmentFile=/etc/airflow/airflow.conf
User=ubuntu
Group=ubuntu
Type=simple
ExecStart=/home/ubuntu/anaconda3/envs/mlops_image_classifier/bin/airflow webserver --port 8081
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Replace `YOUR_USER` and `YOUR_GROUP` with the username and group under which you want to run Airflow.

### 2. Create Systemd Unit File for the Airflow Scheduler

Create a file named `airflow-scheduler.service` in the `/etc/systemd/system/` directory:

```bash
sudo nano /etc/systemd/system/airflow-scheduler.service
```

Add the following content:

```ini
[Unit]
Description=Airflow scheduler daemon
After=network.target postgresql.service
Wants=network.target postgresql.service

[Service]
EnvironmentFile=/etc/airflow/airflow.conf
User=ubuntu
Group=ubuntu
Type=simple
ExecStart=/home/ubuntu/anaconda3/envs/mlops_image_classifier/bin/airflow scheduler
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 3. Create Environment File

You mentioned setting environment variables directly in the shell. It's better to place these in a file `/etc/airflow/airflow.conf` (referenced in the systemd unit files) to ensure they are consistently set for the service:

```bash
sudo nano /etc/airflow/airflow.conf
```

Add your environment variables to this file:

```bash
export AIRFLOW_HOME=~/airflow
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@localhost/airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__WEBSERVER__WEB_SERVER_WORKER_TIMEOUT=160
export AIRFLOW__WEBSERVER__WORKER_CLASS=sync
```

### 4. Enable and Start Services

Reload systemd to read the new unit files:

```bash
sudo systemctl daemon-reload
```

Enable the services to start on boot:

```bash
sudo systemctl enable airflow-webserver
sudo systemctl enable airflow-scheduler
```

Start the services:

```bash
sudo systemctl start airflow-webserver
sudo systemctl start airflow-scheduler
```

### 5. Check the Status

To check the status of the services:

```bash
sudo systemctl status airflow-webserver
sudo systemctl status airflow-scheduler
```

### Troubleshooting

If there are any issues, check the logs with:

```bash
journalctl -u airflow-webserver
journalctl -u airflow-scheduler
```

This setup will make Airflow management easier and more robust, suitable for a production environment or regular use on a server.


# Creating the dag files:
Put your dags in this folder
```bash
mkdir ~/airflow/dags/
cp /home/ubuntu/MLOPS_IMAGE_CLASSIFIER/Airflow/airflow_dag.py ~/airflow/dags/
chmod +x /home/ubuntu/MLOPS_IMAGE_CLASSIFIER/models/BentoOO/create_container_airflow.bash

```

Then restart the service:
```bash
sudo systemctl restart airflow-webserver
sudo systemctl restart airflow-scheduler
```

