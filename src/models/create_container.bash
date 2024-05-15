python training.py
bentoml build .
bentoml containerize animal_classifier:latest
docker tag "animal_classifier:$(docker images --format "{{.Tag}}" | head -n 1)" bethagle/animal_classifier:latest
docker push bethagle/animal_classifier:latest