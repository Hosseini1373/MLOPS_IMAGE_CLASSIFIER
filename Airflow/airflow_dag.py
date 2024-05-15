import errno
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from pymongo import MongoClient
import io
import base64
from PIL import Image
# from airflow.utils.log.logging_mixin import LoggingMixin
# logger = LoggingMixin().log
import logging

logger = logging.getLogger(__name__)
logger.info("This is a log message")

# Environment variables
database_conn_id = Variable.get('MONGODB_KEY')
PetImages_Folder_Path = Variable.get('PetImages_Folder_Path')
Create_Container_Path = Variable.get('Create_Container_Path')

# MongoDB client setup
client = MongoClient(database_conn_id)
db = client["MLOPS"]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'image_classification_workflow',
    default_args=default_args,
    description='A DAG for retraining an image classification model based on new feedback',
    schedule_interval='@daily',
)


def check_feedback(ti):
    try:
        x = db['MLOPS'].aggregate([{"$match": {"trained": False}}, {"$count": "total not trained"}])
        logger.info(f"Query result: {list(x)}")
    except Exception as e:
        logger.error(f"Error processing check_feedback: {str(e)}", exc_info=True)
        raise

    print(list(x))  # Debugging: Print output to Airflow logs
    
    # Ensure the PetImages folder exists
    try:
        # Ensure the PetImages folder exists
        if not os.path.exists(PetImages_Folder_Path):
            os.makedirs(PetImages_Folder_Path)
    except OSError as e:
        logger.error(f"Failed to create directory {PetImages_Folder_Path}: {e}")
        raise

    # Query for untrained images and update their status after processing
    try:
        images_cursor = db['MLOPS'].find({"trained": False})
        # Rest of your code...
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        raise
    
    for image_doc in images_cursor:
        if 'picture' not in image_doc or not image_doc['picture']:
            logger.warning(f"No image data found for document ID {image_doc['_id']}")
            continue
    
        image_data = image_doc['picture']
        image_id = str(image_doc['_id'])
        breed = image_doc['breed']  # String dog or cat
        if breed == "cat":
            file_path = f'{PetImages_Folder_Path}/Cat/{image_id}.jpg'
        else:
            file_path = f'{PetImages_Folder_Path}/Dog/{image_id}.jpg'
        decoded_data = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(decoded_data)).convert("RGB")
        img.save(file_path)

        """
        with open(file_path, 'wb') as f:
            f.write(image_data)
        """

        db['MLOPS'].update_one({'_id': image_doc['_id']}, {'$set': {'trained': True}})
        print(f"Saved {file_path}")

import subprocess

def update_serving_model(ti):
    try:
        result = subprocess.run([Create_Container_Path], check=True, text=True, capture_output=True)
        logger.info(f"Script output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Script failed with exit code {e.returncode} and error {e.stderr}")
        raise


# Python task to check the database for new feedback
check_feedback_task = PythonOperator(
    task_id='check_feedback',
    python_callable=check_feedback,
    provide_context=True,
    dag=dag,
)

# Python task to update the serving model
update_model_task = PythonOperator(
    task_id='update_serving_model',
    python_callable=update_serving_model,
    provide_context=True,
    dag=dag,
)

# Define task dependencies forming the DAG
check_feedback_task >> update_model_task