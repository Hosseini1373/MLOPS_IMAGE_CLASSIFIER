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

# configure the container to run in an executed manner
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app","--timeout","120"]