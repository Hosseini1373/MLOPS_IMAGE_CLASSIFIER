from torchvision.transforms.v2 import Resize
import re
import glob
from torchvision.io import read_image
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms.v2 import ToPILImage


def get_img(path, size):
    #.to(torch.half)
    return Resize((size, size), antialias=True)(read_image(path)) / 255


def produce_labels(paths):
    data = []
    for path in paths:
        if re.search("cat", path, flags=re.IGNORECASE):
            data.append(0)
        else:
            data.append(1)
    return data


class dset(Dataset):
    def __init__(self, root_path, size):
        self.file_paths = glob.glob(root_path)
        self.labels = produce_labels(self.file_paths)
        self.image_size = size

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, index):
        return get_img(self.file_paths[index], self.image_size), self.labels[index]


def create_loaders(root_path, image_size, bsize, nworkers):
    train_loader = DataLoader(dset(root_path, size=image_size),
                              batch_size=bsize,
                              shuffle=True,
                              num_workers=nworkers)
    test_loader = None
    return train_loader, test_loader


if __name__ == "__main__":
    ROOT_DIR = "/mnt/c/Users/Glenn/Downloads/archive/PetImages/*/*"
    BATCH_SIZE = 4
    N_WORKERS = 4
    IMAGE_SIZE = 256

    train_loader, test_loader = create_loaders(ROOT_DIR, IMAGE_SIZE,
                                               BATCH_SIZE, N_WORKERS)

    #img = ToPILImage()(next(iter(train_loader))[0][0])
    #img.show()
