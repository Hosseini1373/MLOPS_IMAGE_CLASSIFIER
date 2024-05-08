# Download Dataset
cd src/data
pip install kaggle
kaggle datasets download -d shaunthesheep/microsoft-catsvsdogs-dataset
unzip microsoft-catsvsdogs-dataset.zip
rm microsoft-catsvsdogs-dataset.zip
shopt -s extglob
cd PetImages
cd Cat
rm !(*.jpg)
cd ../Dog
rm !(*.jpg)