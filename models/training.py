from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import TensorBoardLogger
from lightning.pytorch.loggers import WandbLogger
import lightning as lt
from MobileNetV3 import MobileNet
from preprocess import create_loaders
import torch
import bentoml
import os


def setup_training(root_path, image_size, batch_size, nworkers, epochs,
                   train: bool):
    if train is True:
        train_loader, valid_loader = create_loaders(root_path, image_size,
                                                    batch_size, nworkers)

        checkpoint_callback = ModelCheckpoint(monitor='Valid f1', mode="max",
                                            verbose=False,
                                            save_weights_only=False)
        trainer = lt.Trainer(max_epochs=epochs, logger=TensorBoardLogger("MobileNet"),
                            callbacks=[checkpoint_callback])
        model = MobileNet()
        trainer.fit(model=model, train_dataloaders=train_loader,
                    val_dataloaders=valid_loader)

    """
    with open("saved_model.pkl", "wb") as f:
        torch.save(trainer, f=f)
    """
    model = MobileNet()
    ROOT_CHECKPOINT_PATH = "MobileNet/lightning_logs"
    latest_verison = os.listdir(ROOT_CHECKPOINT_PATH)[-1]
    checkpoint_path = os.path.join(os.path.join(ROOT_CHECKPOINT_PATH, latest_verison), "checkpoints/MobileNet.ckpt")
    check_point = torch.load(checkpoint_path)
    bentoml.pytorch_lightning.save_model("CD-Classifier", model=model,
                                         custom_objects={"weights": check_point})


if __name__ == "__main__":
    ROOT_DIR = "/home/glace/repos/MLOPS_IMAGE_CLASSIFIER/PetImages/*/*"
    BATCH_SIZE = 64
    N_WORKERS = 4
    IMAGE_SIZE = 256
    EPOCHS = 1
    TRAIN = False

    setup_training(ROOT_DIR, IMAGE_SIZE,
                   BATCH_SIZE, N_WORKERS,
                   EPOCHS, TRAIN)
