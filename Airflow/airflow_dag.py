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
    x = db['MLOPS'].aggregate([{"$match": {"trained": False}}, {"$count": "total not trained"}])
    print(list(x))  # Debugging: Print output to Airflow logs
    
    # Ensure the PetImages folder exists
    if not os.path.exists(PetImages_Folder_Path):
        os.makedirs(PetImages_Folder_Path)

    # Query for untrained images and update their status after processing
    images_cursor = db['MLOPS'].find({"trained": False})
    for image_doc in images_cursor:
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

def update_serving_model(ti):
    # Assume the Create_Container_Path script is executable and includes shebang to handle environment
    os.system(Create_Container_Path)  # Using os.system to execute the bash script

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
