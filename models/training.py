from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import TensorBoardLogger
from lightning.pytorch.loggers import WandbLogger
import lightning as lt
from MobileNetV3 import MobileNet
from preprocess import create_loaders


def setup_training(root_path, image_size, batch_size, nworkers, epochs):
    train_loader, test_loader = create_loaders(root_path, image_size,
                                               batch_size, nworkers)

    checkpoint_callback = ModelCheckpoint(monitor='Valid f1', mode="max",
                                          filename="MobileNet",
                                          verbose=False,
                                          save_weights_only=False)
    trainer = lt.Trainer(max_epochs=epochs, logger=TensorBoardLogger("MobileNet"),
                         callbacks=[checkpoint_callback])
    trainer.fit(model=MobileNet(), train_dataloaders=train_loader)


if __name__ == "__main__":
    ROOT_DIR = "/home/glace/repos/MLOPS_IMAGE_CLASSIFIER/PetImages/*/*"
    BATCH_SIZE = 4
    N_WORKERS = 4
    IMAGE_SIZE = 256
    EPOCHS = 1

    setup_training(ROOT_DIR, IMAGE_SIZE,
                   BATCH_SIZE, N_WORKERS,
                   EPOCHS)
