FROM python:3
MAINTAINER Thegaijin "devoprentice@gmail.com"

# Create a directory where our app will be placed
RUN mkdir -p /usr/src/app

# Change directory so that our commands run inside this new directory
WORKDIR /usr/src/app

# Get all the code needed to run the app
COPY . /usr/src/app

# Update image
RUN apt-get update -y

# install necessary packages
RUN apt-get install -y python3-pip python3-dev build-essential

COPY . /RECIPEAPI
WORKDIR /RECIPEAPI
RUN pip3 install -r requirements.txt
EXPOSE 5000

CMD ["python" "manage.py" "runserver"]