from torchvision.transforms.v2 import Resize
import re
import glob
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms.v2 import ToPILImage
from torchvision.transforms import functional as F
import PIL
from matplotlib import pyplot as plt


def get_img(path, image_size):
    # dog 11702, cat 666 corrupted
    img = PIL.Image.open(path).convert("RGB")
    tensor = F.to_tensor(img) / 255
    return Resize((image_size, image_size), antialias=True)(tensor)


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


def test_images_not_corrupted():
    folder_path = "/home/glace/repos/MLOPS_IMAGE_CLASSIFIER/PetImages/*/*"  # Update with your folder path
    for filename in glob.glob(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            try:
                plt.imread(filename)
            except Exception as e:
                assert False, f"Error reading image {filename}: {str(e)}"


if __name__ == "__main__":
    ROOT_DIR = "/home/glace/repos/MLOPS_IMAGE_CLASSIFIER/PetImages/*/*"
    BATCH_SIZE = 4
    N_WORKERS = 4
    IMAGE_SIZE = 256

    train_loader, test_loader = create_loaders(ROOT_DIR, IMAGE_SIZE,
                                               BATCH_SIZE, N_WORKERS)