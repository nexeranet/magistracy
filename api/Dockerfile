# Use the Python3.7.2 image
FROM python:3.7.2-stretch

# Set maintainer
MAINTAINER Oleh Kyslashko "nuxkill@gmail.com"

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Set the working directory to /app
RUN mkdir $APP

WORKDIR $APP

# Copy the current directory contents into the container at /app
ADD . $APP

# Install the dependencies
RUN pip3 install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]
