from __future__ import annotations
import bentoml
from PIL import Image
from torchvision.transforms import functional as F
from torchvision.transforms.v2 import Resize
import io
import base64
from MobileNetV3 import MobileNet  # noqa: F401
# VM_IP:443/inference --> Bento-Server


@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
    name="animal_classifier"
)
class Classifier:
    class_model = bentoml.picklable_model.get("cd-classifier:latest")

    def __init__(self):
        import joblib
        self.model = joblib.load(self.class_model
                                 .path_of("saved_model.pkl")).eval()

    def decode_base64(self, b64_string):
        decoded = base64.b64decode(b64_string)
        return Image.open(io.BytesIO(decoded)).convert("RGB")

    @bentoml.api
    def classify(self, image_b64):
        image = self.decode_base64(image_b64)

        tensor = F.to_tensor(image)
        tensor = F.normalize(tensor, mean=(0.485, 0.456, 0.406),
                             std=(0.229, 0.224, 0.225))
        resized = Resize((256, 256))(tensor)
        input_tensor = resized.reshape((1, 3, 256, 256))

        result = self.model(input_tensor)
        label = result.round().item()
        return label
