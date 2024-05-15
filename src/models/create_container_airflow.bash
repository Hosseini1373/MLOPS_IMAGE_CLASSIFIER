#!/bin/bash

# Activate the Conda environment
source /home/ubuntu/anaconda3/etc/profile.d/conda.sh
conda activate mlops_image_classifier

# Run the training script with the Python interpreter from the environment
/home/ubuntu/anaconda3/envs/mlops_image_classifier/bin/python -m src.models.training

# Continue with the BentoML and Docker commands

bentoml build /home/ubuntu/MLOPS_IMAGE_CLASSIFIER/src/models/.
bentoml containerize animal_classifier:latest

docker login -u bethagle -p "$DOCKER_TOKEN"

# Tagging and pushing the Docker image
TAG=$(docker images --format "{{.Tag}}" | head -n 1)

docker tag "animal_classifier:$TAG" bethagle/animal_classifier:latest
docker push bethagle/animal_classifier:latest