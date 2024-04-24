import lightning as pl
from torch.optim import Adam
from torch import nn
from torchmetrics.classification import BinaryAccuracy, BinaryPrecision, \
    BinaryRecall, BinaryF1Score

from torchvision.models import mobilenet_v3_large
import torch

class MNet(pl.LightningModule):
    def __init__(self):
        super().__init__()

class MobileNet(pl.LightningModule):
    def __init__(self):
        super().__init__()

        classifier = nn.Sequential(
            nn.Linear(in_features=960, out_features=1280),
            nn.Hardswish(),
            nn.Dropout(p=0.2, inplace=True),
            nn.Linear(in_features=1280, out_features=1),
            nn.Sigmoid()
        )

        model = mobilenet_v3_large(weights="DEFAULT")
        for param in model.parameters():
            param.requires_grad = False

        model.classifier = classifier
        self.model = model

        self.n_classes = 2
        self.save_hyperparameters()
        self.mclass_accuracy = BinaryAccuracy()
        self.mclass_precision = BinaryPrecision()
        self.mclass_recall = BinaryRecall()
        self.mclass_f1 = BinaryF1Score()

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=0.001)
        return optimizer

    def training_step(self, batch, batch_idx):
        inputs, targets = batch
        outputs = self.model(inputs)
        targets = targets.to(torch.float32)

        preds = outputs.squeeze(-1)
        loss = nn.BCELoss()(preds, targets)

        accuracy = self.mclass_accuracy(preds, targets).item()
        precision = self.mclass_precision(preds, targets).item()
        recall = self.mclass_recall(preds, targets).item()
        f1 = self.mclass_f1(preds, targets).item()
        to_log = {"Train Accuracy": accuracy, "Train Precision": precision,
                  "Train Recall": recall, "Train f1": f1,
                  "Train CrossEntropy Loss": loss.item()}
        self.log_dict(to_log, on_epoch=True, on_step=False, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        inputs, targets = batch
        outputs = self.model(inputs)
        targets = targets.to(torch.float32)

        preds = outputs.squeeze(-1)
        loss = nn.BCELoss()(preds, targets)

        accuracy = self.mclass_accuracy(preds, targets).item()
        precision = self.mclass_precision(preds, targets).item()
        recall = self.mclass_recall(preds, targets).item()
        f1 = self.mclass_f1(preds, targets).item()

        to_log = {"Valid Accuracy": accuracy, "Valid Precision": precision,
                  "Valid Recall": recall, "Valid f1": f1,
                  "Valid CrossEntropy Loss": loss.item()}
        self.log_dict(to_log, on_epoch=True, on_step=False, prog_bar=True)
        return loss

    def forward(self, x):
        x = self.model(x)
        return x


if __name__ == "__main__":
    test_batch = torch.rand((16, 3, 32, 32))
    model = MobileNet()
    print(type(model))
    print(model(test_batch))
