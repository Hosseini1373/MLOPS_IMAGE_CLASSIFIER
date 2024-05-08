from pathlib import Path

### Define Parameters for Training
BATCH_SIZE = 64
N_WORKERS = 4
IMAGE_SIZE = 256
EPOCHS = 15

### define paths 

# Project root directory
project_dir = Path(__file__).resolve().parents[1]

# data path for the PetImages
data_dir = project_dir / "data" / "PetImages"
