from pathlib import Path
from dotenv import find_dotenv, load_dotenv

### Define Parameters for Training
BATCH_SIZE = 64
N_WORKERS = 4
IMAGE_SIZE = 256
EPOCHS = 15
TRAIN = True

### define paths 

# Project root directory
project_dir = Path(__file__).resolve().parents[0]

# data path for the PetImages
data_dir = project_dir / "data" / "PetImages"

model_logs_dir = project_dir / "models" / "checkpoints"

model_checkpoints = project_dir / "models" / "checkpoints" / "MLOPS"
