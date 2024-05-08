from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import WandbLogger
import lightning as lt
from src.models.MobileNetV3 import MobileNet
from src.data.preprocess import create_loaders
from src import config
import bentoml
import os
import numpy as np
import glob


def setup_training(root_path, image_size, batch_size, nworkers, epochs,
                   train: bool):
    if train is True:
        train_loader, valid_loader = create_loaders(root_path, image_size,
                                                    batch_size, nworkers)

        checkpoint_callback = ModelCheckpoint(monitor='Valid f1', mode="max",
                                              verbose=False,
                                              save_weights_only=False,
                                              filename="MobileNet")
        trainer = lt.Trainer(max_epochs=epochs,
                             logger=WandbLogger(project="MLOPS",
                                                name="mobilenet",
                                                save_dir=config.model_logs_dir),
                             callbacks=[checkpoint_callback])
        model = MobileNet()

        trainer.fit(model=model, train_dataloaders=train_loader,
                    val_dataloaders=valid_loader)

    #print(os.getcwd())
    ROOT_CHECKPOINT_PATH = str(config.model_checkpoints) + "/*/*/*"
    checkpoints_paths = glob.glob(ROOT_CHECKPOINT_PATH)
    idx = np.argmax(sorted([os.path.getctime(k) for k in checkpoints_paths]))
    latest_verison = checkpoints_paths[idx]
    model = MobileNet.load_from_checkpoint(checkpoint_path=latest_verison).cpu()
    bentoml.picklable_model.save_model("CD-Classifier", model=model)


if __name__ == "__main__":
    setup_training(config.data_dir,
                   config.IMAGE_SIZE,
                   config.BATCH_SIZE,
                   config.N_WORKERS,
                   config.EPOCHS,
                   config.TRAIN)
