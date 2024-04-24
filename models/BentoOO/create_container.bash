bentoml build .
bentoml containerize animal_classifier:latest

# This part is not yet correc
docker tag 617db0264d1a bethagle/animal_classifier:latest
docker push bethagle/animal_classifier:latest

models:
  - "cd-classifier:latest"
  - tag: "cd-classifier:latest"