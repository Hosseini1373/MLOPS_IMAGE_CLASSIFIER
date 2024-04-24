from __future__ import annotations
import bentoml
import numpy as np


@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
    name="animal_classifier"
)
class Classifier:
    def __init__(self):
        self.model = bentoml.picklable_model.load_model("cd-classifier:latest")

    @bentoml.api
    def classify(self, input: np.ndarray):
        result = self.model(input)
        return result
