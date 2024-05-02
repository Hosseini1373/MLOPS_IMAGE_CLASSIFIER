# start by pulling the python image
FROM python:3.10.11 AS build-stage
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# switch working directory
WORKDIR /app

# copy every content from the local file to the image
COPY . .

# copy the requirements file into the image
#COPY ./requirements.txt /requirements.txt
# install the dependencies and packages in the requirements file

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8501

# configure the container to run in an executed manner
ENTRYPOINT [ "streamlit", "run", "Userinterface.py", "--server.port=8501", "--server.address=0.0.0.0" ]