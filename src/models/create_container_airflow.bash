# Hi Glenn, I have created a bash script that you can use to create a container for the BentoML model.
# This is similar to create_container.bash, but it includes the commands to activate the Conda environment and run the training script.
# for my case, I have a Conda environment called mlops_image_classifier, and the training script is training.py.
# feel free to modify the script to suit your needs regarding the training script. I would use
# the training.py script that you have in the models/BentoOO folder. But you could change the path to the training script in this bash script.

#!/bin/bash

# Activate the Conda environment
source /home/ubuntu/anaconda3/etc/profile.d/conda.sh
conda activate mlops_image_classifier

# Run the training script with the Python interpreter from the environment
/home/ubuntu/anaconda3/envs/mlops_image_classifier/bin/python -m src.models.training

# Continue with the BentoML and Docker commands
bentoml build /src/models/.
bentoml containerize animal_classifier:latest

docker login -u bethagle -p "$DOCKER_TOKEN"

# Tagging and pushing the Docker image
TAG=$(docker images --format "{{.Tag}}" | head -n 1)ls


docker tag "animal_classifier:$TAG" bethagle/animal_classifier:latest
docker push bethagle/animal_classifier:latest