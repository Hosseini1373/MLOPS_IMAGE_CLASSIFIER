from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import TensorBoardLogger
from lightning.pytorch.loggers import WandbLogger
import lightning as lt
from MobileNetV3 import MobileNet
from src.data.preprocess import create_loaders
import torch
import bentoml
import os
import wandb
import numpy as np
import glob


def setup_training(root_path, image_size, batch_size, nworkers, epochs,
                   train: bool):
    if train is True:
        train_loader, valid_loader = create_loaders(root_path, image_size,
                                                    batch_size, nworkers)

        checkpoint_callback = ModelCheckpoint(monitor='Valid f1', mode="max",
                                            verbose=False,
                                            save_weights_only=False, filename="MobileNet")
        trainer = lt.Trainer(max_epochs=epochs, logger=WandbLogger(project="MLOPS", name="mobilenet"),
                            callbacks=[checkpoint_callback])
        model = MobileNet()

        trainer.fit(model=model, train_dataloaders=train_loader,
                    val_dataloaders=valid_loader)

    #print(os.getcwd())
    ROOT_CHECKPOINT_PATH = "./MLOPS/*/*/*"
    checkpoints_paths = glob.glob(ROOT_CHECKPOINT_PATH)
    idx = np.argmax(sorted([os.path.getctime(k) for k in checkpoints_paths]))
    latest_verison = checkpoints_paths[idx]
    model = MobileNet.load_from_checkpoint(checkpoint_path=latest_verison).cpu()
    bentoml.picklable_model.save_model("CD-Classifier", model=model)


if __name__ == "__main__":
    ROOT_DIR = "/home/glace/repos/MLOPS_IMAGE_CLASSIFIER/PetImages/*/*"
    BATCH_SIZE = 64
    N_WORKERS = 4
    IMAGE_SIZE = 256
    EPOCHS = 15
    TRAIN = False

    setup_training(ROOT_DIR, IMAGE_SIZE,
                   BATCH_SIZE, N_WORKERS,
                   EPOCHS, TRAIN)
