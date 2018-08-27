FROM ubuntu:latest
MAINTAINER Thegaijin "devoprentice@gmail.com"

# Update image
RUN apt-get update -y && apt-get install -y python3.6 python3-pip python3.6-gdbm nginx

RUN rm -rf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

COPY default /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Create a directory where our app will be placed
RUN mkdir -p /project

# Change directory so that our commands run inside this new directory
WORKDIR /project

# Get all the code needed to run the app
COPY . /project

# Install dependencies from requirements file
RUN pip3 install --no-cache-dir -r requirements.txt

# open up port 5000
EXPOSE 80

# restart nginx
CMD ./project/start_nginx.sh && /usr/bin/python3 manage.py runserver
