from torchvision.transforms.v2 import Resize
import re
import glob
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms.v2 import ToPILImage
from torchvision.transforms import functional as F
import PIL
from matplotlib import pyplot as plt
from torch.utils.data import random_split
from collections import Counter
from pathlib import Path
from src import config


def get_img(path, image_size):
    # dog 11702, cat 666 corrupted
    img = PIL.Image.open(path).convert("RGB")
    tensor = F.to_tensor(img)
    tensor = F.normalize(tensor, mean=(0.485, 0.456, 0.406),
                         std=(0.229, 0.224, 0.225))
    return Resize((image_size, image_size), antialias=True)(tensor)


def produce_labels(paths):
    data = []
    for path in paths:
        if re.search("cat", path, flags=re.IGNORECASE):
            data.append(0)
        else:
            data.append(1)
    #print(Counter(data))
    return data


class dset(Dataset):
    def __init__(self, root_path, size):
        self.file_paths = glob.glob(root_path + "/*")
        self.labels = produce_labels(self.file_paths)
        self.image_size = size

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, index):
        return get_img(self.file_paths[index], self.image_size), self.labels[index]


def create_loaders(root_path, image_size, bsize, nworkers):
    data = dset(root_path, size=image_size)
    train_data, valid_data = random_split(data, (0.7, 0.3))
    train_loader = DataLoader(train_data,
                              batch_size=bsize,
                              shuffle=True,
                              num_workers=nworkers)
    valid_loader = DataLoader(valid_data,
                              batch_size=bsize,
                              shuffle=False,
                              num_workers=nworkers)
    return train_loader, valid_loader


def test_images_not_corrupted():
    folder_path = "/home/glenn/repos/MLOPS_IMAGE_CLASSIFIER/PetImages/*/*"
    for filename in glob.glob(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            try:
                plt.imread(filename)
            except Exception as e:
                assert False, f"Error reading image {filename}: {str(e)}"


if __name__ == "__main__":

    train_loader, valid_loader = create_loaders(config.data_dir,
                                                config.IMAGE_SIZE,
                                                config.BATCH_SIZE,
                                                config.N_WORKERS)